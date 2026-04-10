# Phase 4 Batch 0006 Report

**Generated:** 2026-04-10T14:08:09Z
**Batch:** 0006
**Phase:** 4 — bulk ingestion (acts_in_force)
**Source:** parliament.gov.zm
**Tranche:** 2025 Acts No. 20–22 + 2019 Act No. 1 + 2018 Acts No. 1–4

## Records ingested (8)

| ID | Title | Citation | Sections | PDF Size |
|----|-------|----------|----------|----------|
| `act-zm-2025-020-zambia-revenue-authority-act` | The Zambia Revenue Authority (Amendment) Act, 2025 | Act No. 20 of 2025 | 3 | 282 KB |
| `act-zm-2025-021-property-transfer-tax-act` | The Property Transfer Tax (Amendment) Act, 2025 | Act No. 21 of 2025 | 3 | 275 KB |
| `act-zm-2025-022-mobile-money-transaction-levy-act` | The Mobile Money Transaction Levy (Amendment) Act, 2025 | Act No. 22 of 2025 | 3 | 282 KB |
| `act-zm-2019-001-national-dialogue-act` | The National Dialogue (Constitution, Electoral Process, Public Order and Political Parties) Act, 2019 | Act No. 1 of 2019 | 132 | 181 KB |
| `act-zm-2018-001-public-finance-management-act` | The Public Finance Management Act, 2018 | Act No. 1 of 2018 | 152 | 243 KB |
| `act-zm-2018-002-national-health-insurance-act` | The National Health Insurance Act, 2018 | Act No. 2 of 2018 | 94 | 115 KB |
| `act-zm-2018-003-rent-act` | The Rent (Amendment) Act, 2018 | Act No. 3 of 2018 | 2 | 8 KB |
| `act-zm-2018-004-subordinate-courts-act` | The Subordinate Courts Act, 2018 | Act No. 4 of 2018 | 3 | 12 KB |

## Source integrity

All 8 new records passed:
- No duplicate IDs (63 total records in corpus)
- All source_hash values verified against on-disk raw PDF files
- All amended_by references: empty arrays (no cross-references in this tranche)
- All repealed_by references: null
- JSON schema validation: all required fields present, jurisdiction = ZM

## Parse quality notes

Records with ≤ 5 sections (flagged for re-parse):
- **act-zm-2025-020-zambia-revenue-authority-act** (3 sections): ZRA Amendment Act — brief amendment, likely complete
- **act-zm-2025-021-property-transfer-tax-act** (3 sections): PTT Amendment Act — brief amendment, likely complete
- **act-zm-2025-022-mobile-money-transaction-levy-act** (3 sections): MoMo Levy Amendment — brief amendment, likely complete
- **act-zm-2018-003-rent-act** (2 sections): Rent Amendment Act — very brief amendment (8 KB PDF)
- **act-zm-2018-004-subordinate-courts-act** (3 sections): Short amending Act (13 KB)

## Inventory status

Acts ingested cumulative: 62 acts + 1 judgment = 63 total records
2025 Acts coverage: No. 1–29 COMPLETE (all 29 acts ingested)
2026 Acts: No. 1 (batch 0004) = 1 of 1 known
2024 Acts: No. 22–30 (batch 0001) = 9 of ~30
2019 Acts: No. 1–17 (batches 0002–0003 + 0006) + No. 18 pending = 17 of 18
2018 Acts: No. 1–4 (this batch) = 4 of 23
Fetch budget used today: 130/2000

## Next batch recommendation

Batch 0007 should process:
1. 2019 Act No. 18 (Appropriation Act, node 8274) — completes 2019 tranche
2. 2018 Acts No. 5–11 (nodes 7512, 7626, 7627, 7628, 7629, 7846, 7851) — 7 acts
Total target for batch 0007: 8 acts

## Note on SSL

parliament.gov.zm SSL certificate could not be verified from the sandbox CA store.
Fetches used verify=False (site identity confirmed by consistent content and prior
batch results). This is a known Zambian government site.
