# Repair batch b0667 — 8 record(s) fixed, 0 failed

**Worker**: repair-corpus (scheduled-task, v4 prompt)
**Tick**: b0667
**Parser version**: repair-0.6.7
**Date**: 2026-05-15
**Session**: adoring-funny-faraday

## Targets discovered
- Total records needing repair (live DB scan): **113**
  - Condition A (corrupted line-numbers-only body): 0
  - Condition B (acts/SIs with no body): 113
  - Condition C (stub body < 200 chars): 0
- Selected this tick: **8** (MAX_BATCH_SIZE=8)

## Records repaired

| # | ID | Bytes | Source |
|---|---|------:|---|
| 1 | si-zm-2020-052-metrology-verification-fees-regulations-2020 | 13,903 | pdf |
| 2 | si-zm-2020-055-urban-and-regional-planning-designated-local-planning-authorities-regulations-2020 | 926 | pdf |
| 3 | si-zm-2020-056-urban-and-regional-planning-general-regulations-2020 | 96,478 | pdf |
| 4 | si-zm-2020-061-electoral-process-local-government-by-election-election-date-and-time-of-poll-no-5-order-2020 | 2,097 | pdf |
| 5 | si-zm-2020-063-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-6-order-2020 | 1,730 | pdf |
| 6 | si-zm-2020-064-national-market-and-bus-station-development-fund-regulations-2020 | 21,477 | pdf |
| 7 | si-zm-2020-066-local-government-appointment-of-local-government-administrator-lusaka-city-council-order-2020 | 1,537 | pdf |
| 8 | si-zm-2020-067-local-government-appointment-of-local-government-administrator-kitwe-city-council-order-2020 | 1,455 | pdf |

## Quality-gate notes
- All 8 bodies > 200 chars, digit-ratio test passes, contain recognisable legal text keywords.
- One body (si-zm-2020-055) is only 926 chars but passes the gate (genuinely-short order text). No fabrication.

## Integrity
- `records` count: **1925**
- `records_fts` count: **1925** (match ✔)
- `PRAGMA quick_check`: **ok**
- Source fidelity: all bodies extracted from `source.pdf` linked from zambialii.org/akn/zm/act/si/2020/... pages
- No fabrication; all text extracted from upstream PDFs via pdfplumber

## Notes
- 2020-cohort drainage continues (drained 8 more SIs; 113→105 remaining).
- All targets fetched via HTML→PDF discovery pattern (source.pdf link on the AKN page).
- Staging strategy: copy DB to `/tmp/b0667_recover/` for writes, copy back after commit (workspace volume at 95% capacity → virtiofs write-back risk).
- B2 sync: rclone not available on this host → deferred to host.
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- 1-second sleep between fetches honoured (8 fetches in ~39s wall-clock).

## Remaining repair queue
- 105 acts/SIs still needing repair after this batch.
- 148 judgments with no body — skipped (handled by the judgment ingestion worker per v4 prompt).

## Wall-clock
- Tick started: 2026-05-15T~12:13Z
- Elapsed (script): 39s (well under 18-min wall-clock budget)
