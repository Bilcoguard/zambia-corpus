# Phase 4 Batch 0245 Report

**Tick**: 2026-04-26T00:40:52Z  
**Phase**: 4 (bulk)  
**Attempted**: 13  
**OK**: 7  
**Yield**: 7/13 (54%)  
**Skips**: 0  
**Fails**: 6 (all pdf_parse_empty -> OCR backlog)

## Records committed (7)
| yr/num | sub_phase | parent_act | id |
|---|---|---|---|
| 2022/34 | sis_transport | Tolls Act | si-zm-2022-034-tolls-toll-exemption-order-2022 |
| 2022/50 | sis_tax | Customs and Excise Act | si-zm-2022-050-customs-and-excise-general-amendment-regulations-2022 |
| 2022/55 | sis_tax | Customs and Excise Act | si-zm-2022-055-customs-and-excise-public-benefit-organisation-rebate-refund-or-remission-amendment-regulations-2022 |
| 2022/56 | sis_industry | Zambia Development Agency Act | si-zm-2022-056-zambia-development-agency-kalumbila-multi-facility-economic-zone-declaration-order-2022 |
| 2022/62 | sis_tax | Customs and Excise Act | si-zm-2022-062-customs-and-excise-suspension-fuel-no-8-regulations-2022 |
| 2022/65 | sis_governance | Public Protector Act | si-zm-2022-065-public-protector-rules-2022 |
| 2022/66 | sis_mining | Customs and Excise Act | si-zm-2022-066-customs-and-excise-suspension-manganese-ores-and-concentrates-regulations-2022 |

## Sub-phase footprint
- **sis_tax FIRST cluster +3** (Customs and Excise Act parent): 2022/50 (General Amendment), 2022/55 (Public Benefit Organisation Rebate/Refund), 2022/62 (Fuel Suspension No. 8) — **priority_order item 3 advanced from 0 to 3**.
- **sis_mining FIRST +1**: 2022/66 (Customs and Excise Suspension on Manganese Ores) — **priority_order item 7 advanced from 0 to 1** (Customs cross-listed under sis_mining for the manganese-specific suspension).
- **sis_governance +2**: 2022/65 (Public Protector Rules), and... wait — sis_governance picks were 2022/7, 2022/12, 2022/65; only 2022/65 made it through (other two failed pdf_parse_empty). So sis_governance +1 in this batch.
- **sis_industry +1**: 2022/56 (ZDA Act on Kalumbila Multi-Facility Economic Zone).
- **sis_transport +1**: 2022/34 (Tolls Toll Exemption Order).

PRIORITY MILESTONE: this is the **third consecutive tick** to advance a brand-new priority sub-phase from zero (sis_corporate at 0243, sis_industry at 0244, **sis_tax + sis_mining at 0245**). priority_order item 3 (sis_tax) and item 7 (sis_mining) both unlocked this tick.

## Discovery
- robots.txt re-verified: sha256 prefix `fce67b697ee4ef44` (unchanged from batches 0193-0244).
- Probes:
  - year=2024 p4: HTTP 404 (year=2024 listing exhausted at p3).
  - year=2023 p2: HTTP 404 (year=2023 listing exhausted at p1).
  - year=2023 p3: HTTP 404.
  - year=2022 p1: 18 novel candidates.

## Fails (6) -> OCR backlog
All 6 failures are ZambiaLII scanned-image PDFs that pdfplumber cannot extract text from. They join the existing OCR backlog (now 18 items including the 12 carried from batch 0244 + 2022/2, 2022/3, 2022/4 (already), 2022/7 (already), 2022/12 (already), 2022/13 (already)). Net new on OCR backlog this tick: 2022/2 + 2022/3 (the others were already present).

| yr/num | parent_act | error |
|---|---|---|
| 2022/2 | Customs and Excise Act | pdf_parse_empty (NEW) |
| 2022/3 | Customs and Excise Act | pdf_parse_empty (NEW) |
| 2022/4 | Value Added Tax Act | pdf_parse_empty (already in backlog) |
| 2022/7 | National Archives Act | pdf_parse_empty (already in backlog) |
| 2022/12 | Societies Act | pdf_parse_empty (already in backlog) |
| 2022/13 | Minimum Wages Act | pdf_parse_empty (already in backlog) |

OCR backlog after this tick: 14 items (12 from batch 0244 + 2 net new: 2022/2, 2022/3).

## Cumulative SI count
After batch 0244: 536. After batch 0245: 543 (+7).

## Costs (this tick)
- robots reverify: 1 fetch.
- 4 listing probes: 4 fetches.
- per-record ingest: 13 attempted x 2 = 26 raw fetches. (HTML + PDF for each of 13.)
- Total tick fetches: ~31.
- Today total fetches (UTC day): 13 (pre-tick) + 31 = 44 / 2000 (2.2% of daily budget).

## Integrity
ALL 6 CHECKS PASS (CHECK1a, CHECK1b, CHECK2, CHECK3, CHECK4, CHECK5, CHECK6).

## B2 raw sync
DEFERRED to host (rclone unavailable in sandbox).

## Next-tick plan
- (a) Drain remainder of year=2022 p1 cache (4 untried novel: 2022/17, 2022/20, 2022/36, 2022/46) — likely some will text-extract.
- (b) Probe year=2022 p2/p3 listings.
- (c) Probe year=2021 p2+ if not exhausted.
- (d) Rotate to acts_in_force priority_order item 1 (Acts-listing endpoint discovery).
- (e) OCR retry on backlog (now 14 items) once tesseract is wired.
