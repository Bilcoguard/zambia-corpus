# Phase 4 Batch 0005 Report

**Generated:** 2026-04-10T14:30:00Z
**Batch:** 0005
**Phase:** 4 — bulk ingestion (acts_in_force)
**Source:** parliament.gov.zm
**Tranche:** 2025 Acts No. 12–19

## Records ingested (8)

| ID | Title | Citation | Sections | PDF Size |
|----|-------|----------|----------|----------|
| `act-zm-2025-012-superior-courtsnumber-of-judgesact` | The Superior Courts(Number of Judges)Act, 2025 | Act No. 12 of 2025 | 4 | 13 KB |
| `act-zm-2025-013-constitution-of-zambia-amendment-act` | The Constitution of Zambia (Amendment) Act, 2025 | Act No. 13 of 2025 | 11 | 312 KB |
| `act-zm-2025-014-cotton-act` | The Cotton Act, 2025 | Act No. 14 of 2025 | 89 | 548 KB |
| `act-zm-2025-015-small-claims-court-amendment-act` | The Small Claims Court (Amendment) Act, 2025 | Act No. 15 of 2025 | 12 | 311 KB |
| `act-zm-2025-016-occupational-health-and-safety-act` | The Occupational Health and Safety Act, 2025 | Act No. 16 of 2025 | 89 | 468 KB |
| `act-zm-2025-017-income-tax-amendment-no20-act` | The Income Tax (Amendment) (No. 2) Act, 2025 | Act No. 17 of 2025 | 17 | 315 KB |
| `act-zm-2025-018-custom-and-excise-amendment-no-2-act` | The Custom And Excise (Amendment) (No. 2) Act, 2025 | Act No. 18 of 2025 | 13 | 377 KB |
| `act-zm-2025-019-value-added-tax-amendment-act` | The Value Added Tax (Amendment) Act, 2025 | Act No. 19 of 2025 | 2 | 285 KB |

## Source integrity

All 8 new records passed:
- No duplicate IDs (55 total records in corpus)
- All source_hash values verified against on-disk raw PDF files
- All amended_by references: empty arrays (no cross-references in this tranche)
- All repealed_by references: null
- JSON schema validation: all required fields present, jurisdiction = ZM

## Parse quality notes

Records with ≤ 5 sections (flagged for re-parse):
- **act-zm-2025-012-superior-courtsnumber-of-judgesact** (4 sections): Brief amending Act — expected
- **act-zm-2025-019-value-added-tax-amendment-act** (2 sections): Amendment Act — likely schedule-heavy

## Inventory status

Acts ingested cumulative: 54 (46 prior + 8 this batch) + 1 judgment = 55 total records
2025 Acts coverage: No. 1–19 (batches 0001 + 0005) + No. 23–29 (batch 0004) = 26 of 29
2025 Acts still missing: No. 20, 21, 22 (nodes 12773, 12768, 12916)
2026 Acts: No. 1 (batch 0004) = 1 of 1 known
2024 Acts: No. 22–30 (batch 0001) = 9 of ~30
2019 Acts: No. 2–17 (batches 0002–0003) = 16 of ~17
Fetch budget used today: 109/2000

## Next batch recommendation

Batch 0006 should process:
1. 2025 Acts No. 20–22 (nodes 12773, 12768, 12916) — completes 2025 tranche
2. Act No. 1 of 2019 (node 7942 or nearby — needs inventory check)
3. 2018 Acts (nodes to be discovered from listing pages 1–12 inventory)

Total target for batch 0006: 8 acts (3 from 2025 + 1 from 2019 + 4 from 2018)
