# Batch b0631-jiw — JIW Tick Aborted (5th consecutive)

**Date:** 2026-05-13T12:32:30Z
**Worker:** judgment-ingestion-worker
**Verdict:** tick aborted pre-fetch — no corpus mutation
**Wall clock:** ~1 minute

## Summary

This is the 5th consecutive JIW tick to abort (after b0626, b0627, b0629, b0630).
The chronic host-side blockers identified in b0630-jiw remain unchanged.

## Pre-flight checks

| Check | Status | Detail |
|-------|--------|--------|
| `git pull --ff-only` | OK | Already up to date with origin/main |
| `.git/*.lock` cleanup | OK | None present |
| Daily budget | OK | 21 / 500 fetches today (well under) |
| Sandbox `/` disk | **FAIL** | 14 MB free / 100% used |
| `/sessions` disk | OK | 2.4 GB free |
| `corpus.sqlite` mtime | quiescent | 12:15:34 Z (17 min ago) |
| `PRAGMA quick_check` | **FAIL** | tree page 5733 cell 71 → page 21836 |
| `PRAGMA integrity_check` | **FAIL** | same signature, unchanged since b037/b038 |
| CHECK8 parity | **FAIL** | records=1928, records_fts=1924, gap=4 |

## Decision rationale

Per non-negotiables in the task spec:
- *"Never commit if records count ≠ records_fts count — log the gap and defer"*
- *"Never commit broken data"*

Repair-batch-041 (2026-05-13T10:15:59Z) confirmed that
`INSERT INTO records_fts` and atomic `DELETE+INSERT` against `records_fts`
fail deterministically with `database disk image is malformed` for any row
touched. Therefore a JIW write path of "INSERT records + INSERT records_fts"
would also fail at the FTS step, leaving the gap to grow rather than shrink.

The correct action is to abort, log, and wait for host-side FTS5 rebuild.

## Actions taken this tick

- Appended status entry to `worker.log`
- Appended cost entry to `costs.log` (0 fetches)
- Appended status block to `gaps.md` (preserves sweep position)
- Wrote this report to `reports/batch-0631-jiw.md`
- `corpus.sqlite` not touched; not staged for commit (parity rule)

## Sweep position (unchanged since b0622-jiw)

- **ZambiaLII ZMSC 2024** gap-fill: 26/33; next IDs #11, #12, #14.
- **judiciaryzambia.com Court of Appeal**: page 1 not yet started.
  Highest-priority NEW source per Step 3(b).
- **judiciaryzambia.com Constitutional / Supreme / High Court**: not yet
  started; defer until host FTS rebuild lands.

## Recommendation to host operator

1. Run offline FTS5 rebuild:
   ```sql
   PRAGMA journal_mode = PERSIST;
   DROP TABLE records_fts;
   CREATE VIRTUAL TABLE records_fts USING fts5(...);
   INSERT INTO records_fts(rowid, ...) SELECT rowid, ... FROM records;
   VACUUM;
   PRAGMA integrity_check;
   ```
2. Rotate sandbox `/` cache (clear `_stale_locks_*`, old `corpus.sqlite.bak.*`).
3. Confirm `integrity_check = ok` AND `records = records_fts` before next JIW tick.

## Citations / sources accessed

None this tick (zero fetches).

## UA

`KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
