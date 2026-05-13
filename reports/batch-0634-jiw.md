# Batch b0634-jiw — Judgment ingestion tick aborted (8th consecutive)

**Tick start:** 2026-05-13T15:07:29Z
**Worker:** judgment-ingestion-worker
**Verdict:** tick-aborted-no-mutation
**Wall-clock:** ~2 minutes
**Records written:** 0
**Records deferred:** 0
**Fetches:** 0 (cumulative today: 21/500)

## Why this tick aborted

This is the **8th consecutive JIW abort** since b0626-jiw. The chronic
host-side blockers are unchanged from b0631-jiw / b0632-jiw / b0633-jiw.
The b0627-jiw handoff rule #1 mandates that the worker not spend fetch
budget when commit will deterministically fail on CHECK8 (records ↔
records_fts parity).

### Blocker matrix (unchanged)

| # | Blocker | First seen | Status this tick |
|---|---------|-----------|------------------|
| 1 | CHECK8 parity fail (records=1928, records_fts=1924, gap=4) | repair-040 | unchanged |
| 2 | `quick_check` NOT OK — fts5 shadow page 5733 cell 71 (2nd ref to page 21836); invalid page numbers on pages 12466/29610/22491; overflow length mismatch page 5387 cell 0 | b0637/b0638 | unchanged |
| 3 | `integrity_check` NOT OK — same head signature | b0637/b0638 | unchanged |
| 4 | Sandbox `/` 100% full (14 MB free) | b0608 | unchanged |
| 5 | `.git/*.lock` FUSE EPERM (cannot rm) | b0608 | unchanged |
| 6 | Host-side FTS5 rebuild not yet performed | repair-040 handoff | unchanged |

### Pre-flight read-only checks

- `git pull --ff-only` → already up to date (with benign EPERM warnings
  on maintenance.lock + ORIG_HEAD.lock).
- `df -h /` → 100% full, 14 MB free.
- `df -h /sessions` → 75% used, 2.4 GB free.
- `corpus.sqlite` mtime: 2026-05-13T14:36:48Z (host-side quiescent
  ~31 min since repair-batch-042).
- `SELECT COUNT(*) FROM records` = 1928.
- `SELECT COUNT(*) FROM records_fts` = 1924.
- `PRAGMA quick_check` = NOT OK.
- `PRAGMA integrity_check(5)` = NOT OK.
- Missing FTS IDs (4, unchanged):
  - `act-zm-2023-022-the-income-tax-amendment-act-2023`
  - `act-zm-2023-025-the-customs-and-excise-amendment-act-2023-act-no-25-of-2023`
  - `act-zm-2023-029-the-appropriation-act-2023-act-no-29-of-2023`
  - `act-zm-2024-003-investment-trade-and-business-development-amendment-act-2024`

## Integrity check matrix (read-path)

| Check | Result | Notes |
|-------|--------|-------|
| CHECK1 | n/a | no judgment records iterated this tick |
| CHECK2 | n/a | no judgment records iterated this tick |
| CHECK3 | n/a | no judgment records iterated this tick |
| CHECK4 | n/a | no new judges encountered this tick |
| CHECK5 | n/a | no new records |
| CHECK6 | n/a | no new raw files |
| CHECK7 | n/a | no new records |
| CHECK8 | **FAIL** | records=1928, records_fts=1924, gap=4 — defers commit per protocol |

## Files written this tick

- `worker.log` (appended)
- `costs.log` (appended)
- `gaps.md` (appended)
- `reports/batch-0634-jiw.md` (this file)

No DB mutation. No raw file added. No record file added or removed.

## Sweep cursor state (preserved for handoff)

- judiciary-coa-sweep: page-9 (scanned-PDF cliff confirmed b0618)
- judiciary-scz-sweep: page-2 (b0620 baseline)
- judiciary-zmcc-sweep: not yet started
- judiciary-hc-sweep: not yet started
- zambialii-zmsc-sweep: 2024 cluster (next: zmsc-32..end of 2024)
- zambialii-zmcc-sweep: not yet started

## Recommended host-side actions (priority order)

1. **FTS5 rebuild on stable host:** DROP `records_fts`, recreate as
   contentless mirror of `records`, run `INSERT INTO
   records_fts(records_fts) VALUES('rebuild');`, then VACUUM. Verify
   `quick_check = ok` and parity == 0 before swapping in.
2. **Rotate sandbox `/`** — reclaim space so pdfplumber cache and
   VACUUM scratch can land.
3. **Clear FUSE git locks** (`.git/objects/maintenance.lock`,
   `.git/ORIG_HEAD.lock`, etc.) at the host mount layer.
4. **Install `ocrmypdf`** to unblock 2 SI scanned-PDF gaps + the
   ZambiaLII image-PDF cohort.

## Git policy this tick

- `corpus.sqlite` **NOT staged** — parity rule (gap=4 unchanged).
- Logs + this report staged only (same pattern as b0630-jiw / b0631-jiw
  / b0632-jiw / b0633-jiw / repair-039 / 040 / 041 / 042).
- Commit + push **deferred to host-side sweep** — `.git/index.lock`
  EPERM blocks sandbox commit. Files-on-disk pending host action.

## B2 sync

Deferred to host. `rclone` is absent in the sandbox, and corpus.sqlite
has no mutation to sync anyway.

## Handoff to b0635-jiw

- Re-check parity, integrity, and disk before any fetch.
- If blockers persist, continue to abort per protocol.
- If FTS rebuild + sandbox rotation has occurred host-side, run a full
  pre-flight + small (≤2 record) judgment ingestion smoke test before
  attempting a real ≤8 record batch.
- Repair worker note: repair-042 drained 6/8 condB SI body updates but
  did not touch the parity gap. Same 4 missing-FTS IDs remain.
