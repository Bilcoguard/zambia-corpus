# Repair batch 0657 — 8 record(s) fixed, 0 failed

**Worker**: repair-corpus (scheduled-task, v4 prompt)
**Tick**: b0657
**Parser version**: repair-0.6.3
**Wall-clock**: 77.9s (budget 1080s)
**Date**: 2026-05-15T05:20:34Z

## Targets discovered
- Total records needing repair (live DB scan): **145**
- Selected this tick: **8** (MAX_BATCH_SIZE=8)

## Records repaired

| # | ID | Bytes |
|---|---|------:|
| 1 | si-zm-2019-024-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-2-order-2019 | 1,882 |
| 2 | si-zm-2019-028-national-dialogue-forum-extension-order-2019 | 920 |
| 3 | si-zm-2019-030-national-dialogue-forum-extension-no-2-order-2019 | 991 |
| 4 | si-zm-2019-031-defence-regular-forces-officers-amendment-regulations-2019 | 2,167 |
| 5 | si-zm-2019-033-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-3-order-2019 | 1,809 |
| 6 | si-zm-2019-038-national-assembly-by-election-katuba-constituency-no-01-election-date-and-time-of-poll-order-2019 | 2,066 |
| 7 | si-zm-2019-040-corporate-insolvency-insolvency-practitioner-accreditation-regulations-2019 | 4,870 |
| 8 | si-zm-2019-042-urban-and-regional-planning-designated-local-planning-authorities-regulations-2019 | 1,014 |

## Integrity
- `records` count: **1922**
- `records_fts` count: **1922**
- Integrity OK: **True**
- `PRAGMA quick_check`: **ok**

## Pipeline

Standard v4 pipeline: live-DB discovery (Conditions A/B/C) → fetch (curl + RapidSSL CA) → pdfplumber extract → section-number normalise → quality gate (length + digit-line ratio + legal markers) → per-record UPDATE + FTS rebuild + commit (crash-safe).

Crawl delay 5 s between fetches.  Judgments with no body skipped (handled by judgment-ingestion worker).