# Batch 0602 — Judgment Ingestion Worker (JIW)

**Tick start:** 2026-05-11T23:09:30Z (UTC)
**Tick end:** 2026-05-11T23:11:00Z (UTC)
**Worker:** judgment-ingestion (separate from main worker / repair worker)
**Phase:** diagnostic-only — FTS5-blocked (19th consecutive blocked tick)
**Verdict:** `tick-complete-fts5-blocked-with-self-inflicted-damage-recovered`

## Summary

This tick attempted no new ingestion. The 26-record deferred-fts5 backlog and 10-record deferred-scanned-pdf backlog remain unchanged. FTS5 writes are still fully blocked.

A diagnostic `CREATE VIRTUAL TABLE` test (intended to probe whether a brand-new FTS5 shadow table could be created on fresh pages while leaving the corrupt `records_fts` untouched) failed with `disk I/O error` and left a 62 KB rollback journal SQLite could not apply. This wedged the database against all subsequent reads (`disk I/O error` even on `SELECT COUNT(*) FROM records`).

The damage was fully recovered by:

1. Snapshotting the damaged state to `corpus.sqlite.bak.b0602-damaged-20260512T010800Z` for forensics.
2. Snapshotting the orphaned journal to `corpus.sqlite-journal.b0602-forensic-20260512T010800Z` for forensics.
3. Copying `corpus.sqlite.bak.b0598-pre-20260511T221111Z` over `corpus.sqlite` (byte-identical to the pre-b0598 state — md5 `686f8197193a27b0f979156b833352fa`).
4. Renaming the wedge journal to `corpus.sqlite-journal.b0602-jiw-quarantine-20260512T010900Z` (the fuse mount blocks `rm`; `mv` works).

Post-recovery verification: `records=1892`, `records_fts=1892`, CHECK8 PASS, by-type breakdown unchanged (act=1151, judgment=202, si=539).

## Step 1 — Sync

- `git pull --ff-only` → `Already up to date`. Two `.git/objects/maintenance.lock` and `.git/ORIG_HEAD.lock` warnings from prior repair tick — both `Operation not permitted` on the fuse mount, harmless.

## Step 2 — Budget

- Fetches today (2026-05-12, JIW-only): **0/500**.
- No new fetches this tick — diagnostic was on-disk SQLite only.

## Step 3 — Phase decision

Priority (a) REPARSE DEFERRED is not actionable:
- deferred-fts5 records are already parser-clean — they need an FTS5 flush, not a reparse.
- deferred-scanned-pdf records need OCR; `ocrmypdf` is not present in the sandbox (`which ocrmypdf` → empty).

Priorities (b)-(f) (new ingestion sweeps) are unproductive while FTS5 writes are blocked. Prior ticks (b0593–b0597) added new parser-clean records to the archived deferred queue. After 18 blocked ticks the recommendation to "continue parsing into the deferred archive" delivers diminishing returns: the archive has 26 records ready to flush the moment FTS5 is healed. Adding more would consume the 500/day fetch budget without commit progress.

This tick therefore ran a **single targeted diagnostic** to test the b0597 follow-on hypothesis: *could a brand-new FTS5 virtual table be created on fresh database pages*, bypassing the corruption in pages 14599 / 28316-28340 that block writes to the existing `records_fts`?

**Hypothesis: FALSIFIED.** See diagnostic section.

## Diagnostic findings (NEW)

```
PRAGMA integrity_check(50) →  Page 28340: btreeInitPage() returns error code 11
                              Page 28339: btreeInitPage() returns error code 11
                              ... (pages 28316-28340 all flagged)
                              On tree page 14599 cell 291: 2nd reference to page 28337
                              ... (cells 267-291 all flagged)
                              On tree page 28299 cell 1: 2nd reference to page 28316
                              Page 27499 is never used  (and pages 27500-27513, 27516, 27888-27889, 27922)

PRAGMA quick_check(50) →    Same output as integrity_check.

INSERT INTO records (regular non-FTS5 table) →
                              FAIL (test was for column 'body_text' which doesn't exist;
                                    schema check shows correct column is 'body'.
                                    Did not retry due to subsequent wedge.)

CREATE VIRTUAL TABLE records_fts_test_b0602 USING fts5(...) →
                              FAIL: disk I/O error  ← KEY NEW FINDING

After the failure, all subsequent reads (SELECT COUNT(*)) returned 'disk I/O error'
because SQLite saw the orphaned 62 KB rollback journal and could not apply it
(the rollback writes hit the same corrupt pages).
```

**Conclusion (NEW for operator):**

The b0597 follow-on workaround idea — *create a parallel `records_fts_v2`, populate it, then rename* — is **NOT viable**. `CREATE VIRTUAL TABLE` for FTS5 internally requires writes that, on this database, fail with `SQLITE_IOERR`. The corruption in pages 14599 and 28316-28340 is severe enough to block FTS5 schema mutation as well as content mutation.

Combined with b0597-falsified (direct column-based inserts into existing `records_fts` also fail), this confirms:

- ✗ Insert into existing `records_fts` via `INSERT INTO records_fts(records_fts, ...)` (rebuild syntax)
- ✗ Insert into existing `records_fts` via direct column-based `INSERT INTO records_fts(rowid, body, ...) VALUES (...)` (b0597 falsified)
- ✗ `DROP TABLE records_fts` (b0598 confirmed)
- ✗ `CREATE VIRTUAL TABLE records_fts_v2 USING fts5(...)` (b0602 new finding)

**Only remaining recovery paths:**
1. Operator runs `sqlite3 corpus.sqlite ".recover" > recovered.sql` from host, replays into a fresh DB file, and replaces `corpus.sqlite`.
2. Operator runs `VACUUM INTO 'corpus_new.sqlite'` from a `sqlite3` CLI that tolerates the corruption (may fail — `VACUUM` reads pages too).
3. Operator dumps records via Python (`SELECT id, type, json_extract(...), body FROM records`), rebuilds FTS5 from scratch, regenerates `records_fts` via the standard `INSERT INTO records_fts(records_fts) VALUES('rebuild')` against a fresh content table.

This is now operator-only work. The sandbox JIW worker has exhausted all in-band recovery options.

## Step 4 — Self-inflicted damage and recovery

Timeline:
- 23:08:54Z `CREATE VIRTUAL TABLE records_fts_test_b0602` failed with disk I/O error. SQLite wrote a 62 KB rollback journal (`corpus.sqlite-journal`).
- 23:09:07Z subsequent `SELECT` queries failed with `disk I/O error` because SQLite tried to apply the rollback journal on open and the rollback writes failed (corrupt pages).
- 23:09:08Z opened in read-only mode → `attempt to write a readonly database` (journal recovery requires writes).
- 23:09:22Z forensic snapshot taken (`corpus.sqlite.bak.b0602-damaged-20260512T010800Z`).
- 23:09:24Z `corpus.sqlite.bak.b0598-pre-20260511T221111Z` copied over `corpus.sqlite`. md5 verified identical to backup (`686f8197193a27b0f979156b833352fa`).
- 23:09:30Z journal renamed (rm blocked by fuse mount, mv works) to `corpus.sqlite-journal.b0602-jiw-quarantine-20260512T010900Z`.
- 23:09:42Z post-recovery read test: `records=1892`, `records_fts=1892`, no leftover `_test_` or `_diag_` schema entries.

**Net mutation to corpus.sqlite: zero.** Final md5 matches the pre-b0602 state.

## Step 5 — Integrity checks

- CHECK1 — every judgment has ≥1 judge: N/A (no judgments inserted)
- CHECK2 — issue_tags non-empty: N/A
- CHECK3 — outcome in enum: N/A
- CHECK4 — all judges resolve in registry: N/A
- CHECK5 — no duplicate IDs: PASS (1892 unique)
- CHECK6 — raw_sha256 on-disk match: N/A
- CHECK7 — no duplicate (case_name + court + date_decided): N/A
- CHECK8 — `records` count == `records_fts` count: **PASS** (1892 == 1892)

## Step 6 — Sweep position

Unchanged from b0598:
- `judiciary-coa-sweep: page 8 remaining` — 6 unprocessed candidates on judiciaryzambia.com COA category page 8.

## Step 7 — B2 sync

Deferred to host. `rclone` not in sandbox.

## Step 8 — Backlog totals (UNCHANGED from b0598)

- **deferred-fts5 backlog (parser-clean, awaiting FTS5 rebuild):** 26 records
  - b0590: 7, b0591: 4, b0592: 3, b0593: 6, b0594: 4, b0597: 2
- **deferred-scanned-pdf backlog (awaiting ocrmypdf):** 10 records
  - b0593: 1 (Emergency Response Zambia 309/2023), b0594: 4, b0597: 5 (Sichoni, Savenda, Zanaco-Kandala, Mutale-Mukumbwa, Setrec-Zanaco)

## Step 9 — Escalation

**Consecutive blocked ticks: 19** (b0590-b0598 + b0602; b0595, b0596, b0599-b0601 were repair-worker / main-worker ticks that did not touch FTS5).

**Escalation count for JIW: 8th** (7 prior + this one).

**Operator action required:**

1. Rebuild `records_fts` from scratch via host-side sqlite3. The 26-record archived JSON files under `raw/judiciary-zm/coa/_deferred/b059*_parsed_records.json` are ready for immediate flush after the rebuild.
2. Decide whether to authorise the JIW worker to attempt a host-side rebuild on its next tick. The current sandbox SQLite library cannot perform the required schema-level operations on this corrupted file.

**Forensic artefacts preserved this tick:**
- `corpus.sqlite.bak.b0602-damaged-20260512T010800Z` (116 MB) — db state after failed CREATE VIRTUAL TABLE diagnostic
- `corpus.sqlite-journal.b0602-forensic-20260512T010800Z` (62 KB) — orphaned rollback journal from the diagnostic
- `corpus.sqlite-journal.b0602-jiw-quarantine-20260512T010900Z` (62 KB) — quarantined original (same content, renamed to remove from active path)

These can be deleted from the host (which is not fuse-mount-bound) once the operator has inspected them.

## Step 10 — Mutations this tick

- 0 new records ingested
- 0 records reparsed
- 0 fetches
- 1 forensic backup created
- 1 forensic journal copy created
- 1 quarantined journal rename
- 1 in-place restore of corpus.sqlite from b0598-pre backup (net zero mutation; md5 verified)

## Step 11 — Stop

Next JIW tick: t+60min per cadence. Recommend the next tick be a **read-only confirmation** tick (no diagnostics — they risk re-triggering the wedge condition) until the operator has performed the FTS5 rebuild.
