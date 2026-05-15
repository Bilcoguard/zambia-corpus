# Repair batch b0659 — 8 record(s) fixed, 0 failed

**Worker**: repair-corpus (scheduled-task, v4 prompt)
**Tick**: b0659
**Parser version**: repair-0.6.3
**Wall-clock**: 81.1s (budget 1080s)
**Date**: 2026-05-15T07:34:32Z

## Targets discovered
- Total records needing repair (live DB scan): **137**
- Selected this tick: **8** (MAX_BATCH_SIZE=8)

## Records repaired

| # | ID | Bytes |
|---|---|------:|
| 1 | si-zm-2019-043-urban-and-regional-planning-designated-local-planning-authorities-no-2-regulations-2019 | 1,041 |
| 2 | si-zm-2019-044-local-government-fire-inspectors-and-fire-officers-order-2019 | 4,500 |
| 3 | si-zm-2019-045-urban-and-regional-planning-designated-local-planning-authorities-no-3-regulations-2019 | 1,025 |
| 4 | si-zm-2019-047-local-government-fire-services-order-2019 | 2,019 |
| 5 | si-zm-2019-061-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-4-order-2019 | 1,698 |
| 6 | si-zm-2019-064-control-of-goods-import-and-export-agriculture-prohibition-of-export-order-2019 | 4,926 |
| 7 | si-zm-2019-069-palabana-university-declaration-order-2019 | 739 |
| 8 | si-zm-2019-076-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-5-order-2019 | 1,907 |

## Integrity
- `records` count: **1925**
- `records_fts` count: **1925**
- Integrity OK: **True**
- `PRAGMA quick_check`: **ok**

## Pipeline

Standard v4 pipeline: live-DB discovery (Conditions A/B/C) → fetch (curl + RapidSSL CA) → pdfplumber extract → section-number normalise → quality gate (length + digit-line ratio + legal markers) → per-record UPDATE + FTS rebuild + commit (crash-safe).

Crawl delay 5 s between fetches.  Judgments with no body skipped (handled by judgment-ingestion worker).