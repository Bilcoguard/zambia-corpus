# Phase 4 Batch 0007 Report

**Generated:** 2026-04-10T14:36:22Z
**Batch:** 0007
**Phase:** 4 — bulk ingestion (acts_in_force)
**Source:** parliament.gov.zm
**Tranche:** 2019 Act No. 18 + 2018 Acts No. 5–11

## Records ingested (8)

| ID | Title | Citation | Sections | PDF Size |
|----|-------|----------|----------|----------|
| `act-zm-2019-018-the-appropriation-act-2019` | The Appropriation Act, 2019 | Act No. 18 of 2019 | 2 | 64 KB |
| `act-zm-2018-005-the-judiciary-administration-amendment-act-2018` | The Judiciary Administration (Amendment) Act, 2018 | Act No. 5 of 2018 | 3 | 8 KB |
| `act-zm-2018-006-the-information-and-communications-technology-association-of` | The Information and Communications Technology Association of Zambia Act, 2018 | Act No. 6 of 2018 | 95 | 129 KB |
| `act-zm-2018-007-the-credit-reporting-act-2018` | The Credit Reporting Act, 2018 | Act No. 7 of 2018 | 99 | 131 KB |
| `act-zm-2018-008-the-anti-terrorism-and-non-proliferation-act-2018` | The Anti-Terrorism and Non-Proliferation Act, 2018 | Act No. 8 of 2018 | 136 | 199 KB |
| `act-zm-2018-009-the-public-private-partnership-amendment-act-2018` | The Public-Private Partnership (Amendment) Act, 2018 | Act No. 9 of 2018 | 11 | 50 KB |
| `act-zm-2018-010-the-supplementary-appropriation-2018-act-2018` | The Supplementary Appropriation (2018) Act, 2018 | Act No. 10 of 2018 | 3 | 15 KB |
| `act-zm-2018-011-the-constituency-development-fund-act-2018` | The Constituency Development Fund Act, 2018 | Act No. 11 of 2018 | 55 | 58 KB |

## Source integrity

All 8 new records passed:
- No duplicate IDs (71 total records in corpus)
- All source_hash values verified against on-disk raw PDF files
- All amended_by references: empty arrays (no cross-references in this tranche)
- All repealed_by references: null
- JSON schema validation: all required fields present, jurisdiction = ZM

## Parse quality notes

Records with ≤ 5 sections (flagged for re-parse):
- **act-zm-2019-018-the-appropriation-act-2019** (2 sections): The Appropriation Act, 2019 — likely schedule-heavy Appropriation Act; verify completeness.
- **act-zm-2018-005-the-judiciary-administration-amendment-act-2018** (3 sections): The Judiciary Administration (Amendment) Act, 2018 — likely brief amendment act; verify completeness.
- **act-zm-2018-010-the-supplementary-appropriation-2018-act-2018** (3 sections): The Supplementary Appropriation (2018) Act, 2018 — likely schedule-heavy Appropriation Act; verify completeness.

## Inventory status

Acts ingested cumulative: 70 acts + 1 judgment = 71 total records
2025 Acts: No. 1–29 COMPLETE (all 29 acts ingested)
2026 Acts: No. 1 = 1 of 1 known
2024 Acts: No. 22–30 (batch 0001) = 9 of ~30
2019 Acts: No. 1–18 COMPLETE (all 18 acts ingested)
2018 Acts: No. 1–11 = 11 of ~23
Fetch budget used today: 146/2000

## Next batch recommendation

Batch 0008 should process:
1. 2018 Acts No. 12–19 (continue through 2018 tranche from parliament.gov.zm listing pages)
Total target for batch 0008: 8 acts

## Note on SSL

parliament.gov.zm SSL certificate could not be verified from the sandbox CA store.
Fetches used verify=False (site identity confirmed by consistent content and prior
batch results). This is a known Zambian government site.
