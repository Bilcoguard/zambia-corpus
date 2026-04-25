# Phase 4 Batch 0226

- **Started**: 2026-04-25T14:04:45Z
- **Completed**: 2026-04-25T14:08:00Z
- **Mode**: drain V/S/B/F/T/N cache from batch 0225 (no fresh alphabet probes)
- **Records OK**: 8 / 8 (yield 100%)
- **Failures**: 0
- **Skips**: 0
- **Fetches today after batch**: 448 / 2000 (22.4%)

## Records

| ID | Sub-phase | Pages | Chars | Effective |
|---|---|---|---|---|
| si-zm-2022-025-tourism-and-hospitality-registration-of-hotel-managers-temporary-disapplication-of-registration-fee-regulations-2022 | sis_tourism | 2 | 1565 | 2022-04-01 |
| si-zm-2020-122-tourism-and-hospitality-licensing-temporary-disapplication-of-renewal-and-retention-fee-regulations-2020 | sis_tourism | 2 | 1332 | 2020-12-31 |
| si-zm-2019-030-national-dialogue-forum-extension-no-2-order-2019 | sis_governance | 1 | 991 | 2019-08-23 |
| si-zm-2019-028-national-dialogue-forum-extension-order-2019 | sis_governance | 1 | 920 | 2019-07-26 |
| si-zm-2026-008-fisheries-management-area-declaration-order-2025 | sis_fisheries | 4 | 10309 | 2026-01-23 |
| si-zm-2017-028-dambwa-local-forest-no-f22-alteration-of-boundaries-order-2017 | sis_environment | 2 | 3197 | 2017-03-03 |
| si-zm-2017-063-local-forest-no-42-kawena-cessation-order-2017 | sis_environment | 2 | 880 | 2017-08-25 |
| si-zm-2020-012-local-forest-no-p-320-mpande-hills-alteration-of-boundaries-order-2020 | sis_environment | 2 | 2213 | 2020-02-21 |

## Sub-phase progress

- **FIRST sis_fisheries record** in corpus: 2026/008 Fisheries (Management Area) (Declaration) Order, 2025 — substantive 4pp / 10.3K-char declaration designating fisheries management areas under the Fisheries Act.
- **FIRST sis_governance record** in corpus: 2019/028 National Dialogue Forum (Extension) Order, 2019 + 2019/030 No.2 Order — extensions issued under the National Dialogue (Constitution, Electoral Process, Public Order and Political Parties Acts) Act.
- **sis_tourism cluster expansion**: 2 more Tourism and Hospitality Act SIs (the 2020/122 + 2022/025 disapplication-of-fee pair complementing the 2022/026 + 2020/123 already in corpus from batch 0225).
- **sis_environment cluster expansion** under Forests Act: 3 alteration-of-boundaries / cessation orders (2017/028 Dambwa + 2017/063 Kawena + 2020/012 Mpande Hills) — all parsed cleanly despite prior tick's note that F-alphabet alteration orders were "likely scanned"; this cohort proves modern Forest alteration orders are mostly text-extractable.

## Integrity check (PASS)

- CHECK1a (batch unique IDs): 8/8 unique
- CHECK1b (corpus presence on disk): 8/8 record JSON files present
- CHECK2 (amended_by refs): 0 refs (none referenced)
- CHECK3 (repealed_by refs): 0 refs (none referenced)
- CHECK4 (source_hash sha256 verified): 8/8 PDF sha256 matches on-disk raw under `raw/zambialii/si/(2017,2019,2020,2022,2026)/`
- CHECK5 (required fields): 10 fields × 8 records all present (id, type, jurisdiction, title, source_url, source_hash, fetched_at, parser_version, sub_phase, parent_act)
- CHECK6 (cited_authorities refs): 0 refs

## Cumulative

- SI records after this batch: **403** (+8 over batch 0225's 395)
- Judgments: **25** (paused per robots Disallow on /akn/zm/judgment/)

## Next-tick plan

- Cache empty after this drain — next tick must spend fresh discovery fetches.
- Options:
  - Fresh alphabet probes from unprobed set: A/D/E/G/H/K/L/P/R/U/W/X/Y/Z (15 alphabets, with A/G/W/E/M/I/J/L most recently probed several batches ago).
  - Rotate to acts_in_force priority_order item 1 — would require Acts-listing endpoint discovery.
  - Re-probe the 4 OCR-backlog candidates from batch 0225 (2017/068, 2018/011, 2022/004, 2022/007, 2022/012) with a tesseract OCR fallback — defer until tesseract is wired up.

## Infrastructure follow-up (non-blocking)

- 16 batch-0226 raw SI files (8 HTML + 8 PDF) + 1 robots.txt re-verify (~2 KB) plus accumulated batches 0192-0225 raw files awaiting host-driven B2 sync (rclone unavailable in sandbox).
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild; SI records remain on-disk-only.
- Persistent virtiofs unlink-failure warnings non-fatal (workaround stable across batches 0192-0226 — write-tree/commit-tree path bypasses lock).
- 34 pre-existing flat-vs-year-subdir duplicate paths under records/acts/ unchanged.
- 488+ pre-existing untracked records/sis + records/acts files on disk (not in HEAD) unchanged.
- OCR backlog: 5 items (2017/068, 2018/011, 2022/004, 2022/007, 2022/012) from batch 0225 — raw PDFs preserved.

## Tick wall-clock

~3.5 min total (started 14:04:45Z robots fetch, last record ingested 14:08:00Z) — well under 20-min cap.
