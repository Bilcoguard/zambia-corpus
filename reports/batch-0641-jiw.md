# Batch b0641-jiw — Judgment Ingestion Worker

**Tick start:** 2026-05-14T03:05:40Z
**Worker:** judgment-ingestion-worker
**Verdict:** TICK ABORTED (15th consecutive JIW abort since b0626-jiw)
**Wall-clock:** ~5 min
**Budget used this tick:** 0 fetches (cumulative today: 0 / 500 — new UTC day, daily counter reset)

## Summary

No fetch, no parse, no write, no DB mutation. Chronic host-side blockers
unchanged since b0640-jiw. Logs and this report are the only mutations
committed this tick. Bogus lock-style refs in
`.git/refs/remotes/origin/` were re-seeded with the current HEAD SHA
(`32ac09b…`) to keep `git pull --ff-only` functional.

## Preflight observations

| Metric | Value |
| --- | --- |
| `records` count | 1928 |
| `records_fts` count | 1924 |
| Parity gap | **4** (CHECK8 FAIL) |
| `judgments` count | 238 |
| Coverage vs target | 238 / 800 = **30 %** |
| `corpus.sqlite` mtime | 2026-05-13T12:36:48Z |
| Host-side quiescent for | ~14.5 h |
| Sandbox `/` free | 14 MB (100 % full) |
| `/sessions` free | 2.4 GB |
| Corpus FS free | 13 GB |
| `PRAGMA quick_check(8)` | NOT OK |
| `PRAGMA integrity_check` | NOT OK (assumed — same shadow pages) |

## Persistent FTS5 shadow-table corruption (unchanged since b037/b038)

```
*** in database main ***
On tree page 5733 cell 71: 2nd reference to page 21836
On tree page 5733 cell 69: Rowid 1185 out of order
On tree page 6270 cell 0: 2nd reference to page 24604
On tree page 5387 cell 0: overflow list length is 1 but should be 3
On tree page 5732 cell 455: 2nd reference to page 24606
On tree page 5732 cell 439: 2nd reference to page 21821
On tree page 5732 cell 262: 2nd reference to page 21850
On tree page 12466 cell 7: invalid page number 30645
On tree page 29610 cell 0: invalid page number 32486
On tree page 22491 cell 0: invalid page number 30667
On tree page 12465 cell 7: child page depth differs
...
```

## Missing FTS rows (unchanged since repair-040)

| ID | Domain |
| --- | --- |
| `act-zm-2023-022-the-income-tax-amendment-act-2023` | acts (not JIW scope) |
| `act-zm-2023-025-the-customs-and-excise-amendment-act-2023-act-no-25-of-2023` | acts (not JIW scope) |
| `act-zm-2023-029-the-appropriation-act-2023-act-no-29-of-2023` | acts (not JIW scope) |
| `act-zm-2024-003-investment-trade-and-business-development-amendment-act-2024` | acts (not JIW scope) |

All four missing IDs are in the **acts** namespace, owned by the main
corpus worker / repair worker. JIW cannot fix these. But the global
`records_fts` table is shared — any new INSERT touching the shadow
tables risks propagating the existing corruption. Per CHECK8 protocol,
this worker MUST defer all commits while the gap is open.

## Sweep position (unchanged — preserved for resume)

| Sweep | Position | Status |
| --- | --- | --- |
| `judiciary-coa-sweep` | page 1 | not yet started — new source, zero coverage |
| `judiciary-scz-sweep` | page 1 | not yet started |
| `judiciary-zmcc-sweep` | page 1 | not yet started |
| `judiciary-zmhc-sweep` | page 1 | not yet started |

## Git / refs status

- `git pull --ff-only` succeeded (after quarantine of three stale
  branch refs in `.git/refs/heads/` that had `bad object` content:
  `_test`, `test_create`, `testfile`, plus the residual
  `main.lock.bak.b0640.1778706534` empty file). All four were renamed
  out of `refs/heads/` via `mv` (sandbox cannot `rm` — EPERM) and the
  pull then succeeded.
- HEAD = `32ac09b` = origin/main (unchanged from b0640).
- Bogus lock-style refs in `.git/refs/remotes/origin/` still present.
  SHA-reseed updated this tick from `9ae9919` → `32ac09b` so all six
  bogus files point at the live HEAD; `git pull` continues to work.
- Standard commit + push will proceed for the log files only.

## CHECK1–CHECK8 status (read-path)

| Check | Status |
| --- | --- |
| CHECK1 (judges present) | n/a — no new records |
| CHECK2 (issue_tags non-empty) | n/a — no new records |
| CHECK3 (outcome enum) | n/a — no new records |
| CHECK4 (judges registry resolution) | n/a — not iterated |
| CHECK5 (duplicate IDs) | n/a — no new records |
| CHECK6 (raw_sha256 match) | n/a — no new raw files |
| CHECK7 (duplicate case_name/court/date) | n/a — no new records |
| **CHECK8 (records == records_fts)** | **FAIL — gap=4** → defer commit per protocol |

## Decision rationale

Per b0627-jiw handoff rule 1 ("do not waste budget on retries that
will fail on commit"), JIW must not fetch, parse, or write while
CHECK8 fails. The repair-041 result (deterministic FTS insert failure
for the 4 residual `act-zm-…` IDs) and the unchanged corpus.sqlite
mtime (~14.5 h quiescent) confirm that the host has not run the
recommended FTS5 rebuild since the last tick. No mitigation available
to JIW.

## Recommended operator (host-side) actions

1. **Rebuild FTS5** on host:
   ```
   DROP TABLE records_fts;
   CREATE VIRTUAL TABLE records_fts USING fts5(id UNINDEXED, body, ...);
   INSERT INTO records_fts(rowid, id, body, ...)
     SELECT rowid, id, body, ... FROM records;
   VACUUM;
   PRAGMA integrity_check;
   ```
2. **Permanent `rm`** of bogus lock-style refs and quarantined files:
   ```
   rm .git/refs/remotes/origin/main.lock*
   rm .git/objects/maintenance.lock
   rm _quarantine_lock _quarantine_test_ref _quarantine_testfile_ref _quarantine_testcreate_ref
   ```
3. **Rotate sandbox `/`** — currently 14 MB free, blocks pdfplumber
   cache and VACUUM headroom.
4. **Install `ocrmypdf`** in sandbox — `condB` SI backlog drain still
   blocked without it.

## Handoff

- Next tick: **b0642-jiw** at t+60 min.
- If host-side rebuild has happened by then, b0642 should resume from
  `judiciary-coa-sweep page 1` (highest-priority new source — zero
  coverage today).
- If chronic blockers remain, b0642 will abort with the same pattern.
- 15 consecutive aborts now exceed the "5 consecutive zero-discovery
  ticks" completion-criterion threshold in the brief, but the cause
  here is upstream DB corruption rather than source exhaustion, so
  this worker MUST NOT flip `complete: true`. Escalate to human
  operator for the host-side FTS5 rebuild.
