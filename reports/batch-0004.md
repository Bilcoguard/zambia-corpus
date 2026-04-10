# Batch 0004 Report — Phase 4 Bulk Ingestion

**Date:** 2026-04-10
**Worker:** KateWestonLegal-CorpusBuilder/1.0
**Phase:** 4 (bulk ingestion — acts_in_force)
**Source:** parliament.gov.zm
**Tranche:** 2025 Acts No. 23–29 + 2026 Act No. 1

## Records ingested (8)

| ID | Title | Citation | Sections | PDF Size |
|----|-------|----------|----------|----------|
| `act-zm-2026-001-teaching-profession-act` | The Teaching Profession Act, 2026 | Act No. 1 of 2026 | 94 | 525 KB |
| `act-zm-2025-029-zambia-institute-of-procurement-and-supply-act` | The Zambia Institute of Procurement and Supply Act, 2025 | Act No. 29 of 2025 | 107 | 478 KB |
| `act-zm-2025-028-appropriation-act` | The Appropriation Act, 2025 | Act No. 28 of 2025 | 2 | 336 KB |
| `act-zm-2025-027-betting-act` | The Betting Act, 2025 | Act No. 27 of 2025 | 5 | 299 KB |
| `act-zm-2025-026-zambia-national-broadcasting-corporation-act` | The Zambia National Broadcasting Corporation Act, 2025 | Act No. 26 of 2025 | 51 | 375 KB |
| `act-zm-2025-025-independent-broadcasting-authority-act` | The Independent Broadcasting Authority Act, 2025 | Act No. 25 of 2025 | 77 | 486 KB |
| `act-zm-2025-024-registration-of-business-names-amendment-act` | The Registration of Business Names (Amendment) Act, 2025 | Act No. 24 of 2025 | 5 | 300 KB |
| `act-zm-2025-023-companies-amendment-act` | The Companies (Amendment) Act, 2025 | Act No. 23 of 2025 | 28 | 384 KB |

## Source integrity

All 8 new records passed:
- No duplicate IDs (47 total records in corpus)
- All source_hash values verified against on-disk raw PDF files
- All amended_by references: empty arrays (no cross-references in this tranche)
- All repealed_by references: null
- JSON schema validation (Draft 2020-12): all 8 records PASS

## Parse quality notes

Records with ≤ 5 sections (may need re-parse for schedule-heavy or brief Acts):
- **act-zm-2025-028-appropriation-act** (2 sections): Appropriation Act — typically schedule-heavy
- **act-zm-2025-027-betting-act** (5 sections): May have schedules not captured
- **act-zm-2025-024-registration-of-business-names-amendment-act** (5 sections): Amendment act — expected to be brief

## Inventory status

Acts ingested cumulative: 46 (38 prior + 8 this batch) + 1 judgment = 47 total records
2025 Acts coverage: No. 1–11 (batch 0001) + No. 23–29 (this batch) = 18 of 29
2026 Acts coverage: No. 1 of 1 known
2024 Acts coverage: No. 22–30 (batch 0001) = 9 of ~30
2019 Acts coverage: No. 2–17 (batches 0002–0003) = 16 of ~17
Fetch budget used today: 98/2000

## Next batch recommendation

Batch 0005 should process 2025 Acts No. 12–19 (nodes 12765, 12766, 12767, 12768, 12773, 12774 already done → continue with 12916, 12765, 12766, 12767, 12768) to complete the 2025 tranche.
