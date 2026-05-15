# Repair batch b0664 — 8 record(s) fixed, 0 failed

**Worker**: repair-corpus (scheduled-task, v4 prompt)
**Tick**: b0664
**Parser version**: repair-0.6.4
**Date**: 2026-05-15

## Targets discovered
- Total records needing repair (live DB scan): **121**
  - Condition A (corrupted line-numbers-only body): 0
  - Condition B (acts/SIs with no body): 121
  - Condition C (stub body < 200 chars): 0
- Selected this tick: **8** (MAX_BATCH_SIZE=8)

## Records repaired

| # | ID | Bytes | Source |
|---|---|------:|---|
| 1 | si-zm-2020-012-local-forest-no-p-320-mpande-hills-alteration-of-boundaries-order-2020 | 2,213 | pdf |
| 2 | si-zm-2020-013-national-forest-no-f-12-luano-alteration-of-boundaries-order-2020 | 3,345 | pdf |
| 3 | si-zm-2020-014-local-government-fire-services-order-2020 | 892 | pdf |
| 4 | si-zm-2020-018-compulsory-standards-potable-spirits-declaration-order-2020 | 7,806 | pdf |
| 5 | si-zm-2020-023-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-3-order-2020 | 1,692 | pdf |
| 6 | si-zm-2020-034-laws-of-zambia-revised-edition-act-specified-date-notice-2020 | 845 | pdf |
| 7 | si-zm-2020-043-electoral-process-local-government-by-election-election-date-and-time-of-poll-no-4-order-2020 | 1,864 | pdf |
| 8 | si-zm-2020-050-road-traffic-driving-licence-regulations-2020 | 42,935 | pdf |

## Integrity
- `records` count: **1925**
- `records_fts` count: **1925** (match ✔)
- `PRAGMA quick_check`: **ok**
- Quality gate (all): body > 200 chars, digit-ratio OK, legal-text keywords present
- Source fidelity: all bodies extracted from `source.pdf` linked from zambialii.org/akn/zm/act/si/2020/... pages
- No fabrication

## Notes
- 2020-cohort drainage continues (drained 8 of 34 SIs remaining in 2020).
- All targets fetched via HTML→PDF discovery pattern (source.pdf link on the AKN page).
- Staging strategy: copy DB to `/tmp/b0664_recover/` for writes, copy back after commit (workspace volume at 95% capacity → virtiofs write-back risk).
- B2 sync: rclone not available on this host → deferred to host.

## Remaining repair queue
- 113 acts/SIs still needing repair after this batch.
