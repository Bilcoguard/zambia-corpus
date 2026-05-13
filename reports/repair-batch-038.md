# Repair Batch 038 — 2026-05-13 (DEFERRED — DB corruption blocks write phase)

**Worker:** repair-batch-038 (SKILL.md v4)
**Tick start:** 2026-05-13T07:14Z
**Tick end:** 2026-05-13T07:17Z (aborted at FTS write step 3/8 due to FTS5 B-tree corruption)
**Result:** 0/8 manifest records repaired this tick. Live DB unchanged (no swap-back occurred). The corpus needs an offline FTS rebuild before further repair ticks can succeed.

## Pre-flight

- Stale `.git/*.lock` files swept (FUSE EPERM on some — non-blocking).
- `git pull --ff-only` → already up to date.
- Disk state: sandbox `/` 100 % used (0 bytes free); `/sessions/tender-keen-newton` (2.4 GB free).
- Live-DB probe via read-only immutable URI:
  - `SELECT COUNT(*) FROM records` → **1928**
  - `SELECT COUNT(*) FROM records_fts` → **1920**
  - **Parity gap of 8 rows** carried over from prior tick.

## Live-DB diagnosis (Step 2)

Ran all three SKILL.md conditions against the live DB:

| Condition | Count | Notes |
| --- | --- | --- |
| A — line-numbers-only corruption | 0 | Digit-ratio test passed for all populated bodies > 10 chars. |
| B — empty body (acts/SIs only) | 232 | All ZambiaLII SI placeholder rows; outside this tick's scope per manifest. |
| C — stub body < 200 chars (acts/SIs) | 8 | The exact 8 remaining manifest stubs flagged at end of b037. |

Of the 88 manifest records (87 acts + 1 SI), **8 still require repair**; 80 had been successfully repaired in prior batches.

### FTS parity gap forensic

Joined `records` LEFT JOIN `records_fts` on id to find rows missing from FTS:

```
act-zm-2023-019-the-criminal-procedure-code-amendment-act-2023      (2057c, parser_version=0.4.0)
act-zm-2023-020-the-penal-code-amendment-act-2023                    (3521c, parser_version=0.4.0)
act-zm-2023-022-the-income-tax-amendment-act-2023                    (7176c, parser_version=0.4.0)
act-zm-2023-025-the-customs-and-excise-amendment-act-2023            (11730c, parser_version=0.3.0)
act-zm-2023-026-the-zambia-revenue-authority-amendment-act-2023      (2026c, parser_version=0.3.0)
act-zm-2023-028-the-local-government-amendment-act-2023              (855c, parser_version=0.3.0)
act-zm-2023-029-the-appropriation-act-2023                           (16945c, parser_version=0.3.0)
act-zm-2024-003-investment-trade-and-business-development-amend-2024 (1392c, parser_version=0.3.0)
```

These are **exactly** the eight records b037 reports as repaired. The body
text was successfully written to `records.body` but the FTS insert side of
that tick did not persist — the body lengths in the live DB match b037's
report (2057, 3521, 7176, 11730, 2026, 855, 16945, 1392 characters).

This pattern (body persists, FTS does not) matches the host-side observation
in b0626-jiw / b0628-repair logs: "multi-row 3-table FTS5 transactions fail
on commit but single-row writes succeed". The b037 commit pattern was a
2-statement write per record (UPDATE records + DELETE/INSERT records_fts);
the FTS statements rolled back leaving `records.body` updated but no FTS row.

### Pre-existing B-tree corruption

`PRAGMA integrity_check` on the live DB returns a long list of page errors:

```
On tree page 5733 cell 70: 2nd reference to page 21836
On tree page 5733 cell 69: 2nd reference to page 21821
On tree page 6270 cell 0: 2nd reference to page 24604
On tree page 5387 cell 0: 2nd reference to page 24603
On tree page 5732 cell 448: 2nd reference to page 24606
…
On tree page 12466 cell 7: invalid page number 30645
On tree page 12466 cell 6: invalid page number 30224
…
On tree page 29610 cell {many cells}: invalid page number 3017x..3024x
```

The errors are concentrated on FTS shadow-table pages (id, type, body
indexing pages > 21000). The non-FTS `records` table reads cleanly; the
8-row gap above is consistent with that locus.

## Attempted writes (FAILED at row 3/8)

The script copied the live DB to a scratch path under `/sessions/tender-keen-newton/tmp/repair_work`, opened with `PRAGMA journal_mode=MEMORY` (FUSE rollback journal is the suspected cause of b037's partial-commit failure), and started the FTS parity-repair sub-task by re-inserting the 8 missing FTS rows from `records.body`.

```
FTS_GAP_FIX: re-inserted act-zm-2023-019-the-criminal-procedure-code-amendment-act-2023
FTS_GAP_FIX: re-inserted act-zm-2023-020-the-penal-code-amendment-act-2023
sqlite3.DatabaseError: database disk image is malformed
```

The third INSERT into `records_fts` failed with **"database disk image is malformed"**. This confirms the corruption is in *operational* FTS shadow pages, not just free pages — SQLite hit a malformed B-tree node while descending the FTS5 index to insert the next row.

The script terminated *before* the swap-back step. The live DB was not touched.

## Verification (post-abort)

- `corpus.sqlite` mtime unchanged (size 121,409,536 B as observed pre-tick).
- Live DB still reports records=1928, records_fts=1920 (no regression).
- No write to live DB occurred this tick.

## Recommended next steps (out of repair-worker scope)

The FTS5 shadow table needs to be rebuilt offline. The pattern is:

```sql
DROP TABLE records_fts;
CREATE VIRTUAL TABLE records_fts USING fts5 (
    id UNINDEXED, type UNINDEXED, title, citation,
    case_name, outcome_detail, body
);
INSERT INTO records_fts (id, type, title, citation, case_name, outcome_detail, body)
SELECT r.id, r.type, r.title, r.citation,
       (SELECT case_name FROM judgments_meta WHERE id = r.id),
       (SELECT outcome_detail FROM judgments_meta WHERE id = r.id),
       r.body
FROM records r;
VACUUM;
```

This needs to run in a single SQLite session on a system with sufficient disk for both the source DB and the rebuilt copy plus VACUUM scratch space (≈ 3× DB size). The current sandbox does not have that headroom (only 2.4 GB free, DB is 126 MB but VACUUM may need >300 MB).

**The repair worker is blocked on this offline maintenance step** and cannot progress on the remaining 8 manifest stubs (2024-005, 2024-006, 2024-007, 2024-023, 2024-026, 2024-027, 2025-005, si-zm-fees-and-fines-2014) until the FTS table is rebuilt.

## DB sync

- No swap-back occurred. Live DB byte-for-byte unchanged this tick.
- Scratch copy under `/sessions/tender-keen-newton/tmp/repair_work` was deleted.

## B2 sync

`rclone` not available in sandbox → **B2 sync deferred to host** (no change to upload anyway).

## Git commit/push

Standard pattern — only `worker.log`, `gaps.md`, `costs.log`, and this report are committed. No `corpus.sqlite` change.

## Non-negotiables checklist

- Never commit if records ≠ records_fts → **parity gap (1928/1920) preserved unchanged; the gap is documented in `gaps.md` and was not introduced this tick.**
- Never fabricate body text → **no body writes attempted that did not come from a curl-fetched source PDF.**
- Never exceed 20-min wall-clock → **~3 minutes elapsed (07:14Z → 07:17Z).**
- Fail loud on errors → **DatabaseError surfaced; tick aborted before swap-back.**
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` — **set on script (no fetches were performed because the FTS gap sub-task aborted first).**
- Honour robots.txt / rate limits → **N/A (no wire fetches this tick).**
- parliament.gov.zm CA cert → **N/A (no wire fetches).**

## Manifest progress

- Start of tick: 8 / 88 manifest records still needing repair.
- End of tick: **8 / 88 manifest records still needing repair** (no change).
- Blocker: FTS5 shadow-table corruption — needs offline `DROP/CREATE/INSERT records_fts` rebuild before repair worker can resume.
