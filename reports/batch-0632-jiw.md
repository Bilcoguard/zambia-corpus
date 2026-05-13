# Batch b0632-jiw — JIW Tick Aborted (6th consecutive)

**Date:** 2026-05-13T13:07:30Z
**Worker:** judgment-ingestion-worker
**Verdict:** tick aborted pre-fetch — no corpus mutation
**Wall clock:** ~2 minutes

## Summary

This is the 6th consecutive JIW tick to abort (after b0626, b0627, b0629,
b0630, b0631). The chronic host-side blockers identified in b0630-jiw and
re-confirmed in b0631-jiw remain unchanged. Repair-batch-042 ran in the
intervening hour and applied 6 body updates to the Condition-B SI backlog,
but did not touch the parity gap (UPDATE-only fallback).

## Pre-flight checks

| Check | Status | Detail |
|-------|--------|--------|
| `git pull --ff-only` | OK | Already up to date with origin/main |
| `.git/*.lock` cleanup | OK | maintenance.lock EPERM (benign, host-owned) |
| Daily budget | OK | 21 / 500 fetches today (well under) |
| Sandbox `/` disk | **FAIL** | 14 MB free / 100% used |
| `/sessions` disk | OK | 2.4 GB free |
| `corpus.sqlite` mtime | quiescent | 12:36:48 Z (31 min ago) |
| `PRAGMA quick_check` | **FAIL** | tree page 5733 cell 71 → page 21836 + extensive invalid-page errors on pages 12466 / 29610 |
| `PRAGMA integrity_check` | **FAIL** | same signature, unchanged since b037/b038 |
| CHECK8 parity | **FAIL** | records=1928, records_fts=1924, gap=4 |

## Decision rationale

Per non-negotiables in the task spec:
- *"Never commit if records count ≠ records_fts count — log the gap and defer"*
- *"Never commit broken data"*

Repair-batch-041 (2026-05-13T10:15:59Z) confirmed deterministic failure of
`INSERT INTO records_fts` and atomic `DELETE+INSERT` against `records_fts`
with `database disk image is malformed` for the residual 4 IDs. Repair-042
chose UPDATE-only fallback to avoid growing the gap. Therefore a JIW write
path of "INSERT records + INSERT records_fts" would also fail at the FTS
step, leaving the gap to grow rather than shrink.

The correct action is to abort, log, and wait for host-side FTS5 rebuild.

## Actions taken this tick

- Appended status entry to `worker.log`
- Appended cost entry to `costs.log` (0 fetches)
- Appended status block to `gaps.md` (preserves sweep position)
- Wrote this report to `reports/batch-0632-jiw.md`
- `corpus.sqlite` not touched; not staged for commit (parity rule)

## Intervening repair worker activity

`repair-batch-042` (2026-05-13T12:35:30Z, ~32 min before this tick) made
progress on a different front: 6 Condition-B SI body updates from the
`records.body IS NULL OR length(body)<200` cohort.

- BODY_UPDATE_OK: si-zm-1980-049, si-zm-1981-047, si-zm-1982-049,
  si-zm-1985-014, si-zm-1985-024, si-zm-1985-045
- FETCH_FAIL (scanned PDFs requiring ocrmypdf):
  local-courts-administration-of-estates-rules-1969, local-courts-rules-1966
- New backlog discovery: 232 SI records in Condition B (NULL/empty body)
- Parity gap unchanged at 4 (UPDATE-only on `records.body`, no FTS touch)

This is informational; it does not unblock the JIW write path.

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
2. Rotate sandbox `/` cache: `_stale_locks_*`, old `corpus.sqlite.bak.*`,
   stale `_repair_b03N_*` workspaces, `_b0612_jiw_inline.py` and similar
   ad-hoc scripts left under `/sessions/amazing-gifted-cray/mnt/corpus/`.
3. Install `ocrmypdf` to clear the 2 scanned-PDF Condition-B IDs and the
   broader ZambiaLII image-PDF cohort.
4. Confirm `integrity_check = ok` AND `records = records_fts` before next
   JIW tick.

## Pattern observation

Six consecutive JIW aborts on the same blocker set is now the dominant
operational signal. The repair-worker is making forward progress on
Condition-B body updates but cannot rebuild the FTS shadow table from
inside the sandbox (insufficient `/` disk for `VACUUM` headroom, and
DELETE+INSERT against the malformed shadow pages fails deterministically).
Until a host-side rebuild lands, JIW remains permanently blocked on the
"new INSERT must touch records_fts" path.

## Citations / sources accessed

None this tick (zero fetches).

## UA

`KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
