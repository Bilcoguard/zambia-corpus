# Phase 4 Batch 0008 Report

**Generated:** 2026-04-10T17:18:19Z
**Batch:** 0008
**Phase:** 4 — bulk ingestion (acts_in_force)
**Source:** parliament.gov.zm
**Tranche:** 2017 Acts No. 3–9, 11

## Records ingested (8)

| ID | Title | Citation | Sections | PDF Size |
|----|-------|----------|----------|----------|
| `act-zm-2017-003-compulsory-standards` | Compulsory Standards | Act No. 3 of 2017 | 39 | 97 KB |
| `act-zm-2017-004-standards` | The Standards | Act No. 4 of 2017 | 41 | 81 KB |
| `act-zm-2017-005-national-technical-regulation` | The National Technical Regulation | Act No. 5 of 2017 | 28 | 59 KB |
| `act-zm-2017-006-metrology` | The Metrology | Act No. 6 of 2017 | 73 | 185 KB |
| `act-zm-2017-007-banking-and-financial-services` | The Banking and Financial Services | Act No. 7 of 2017 | 198 | 528 KB |
| `act-zm-2017-008-supplementary-appropriation-2017` | The Supplementary Appropriation | Act No. 8 of 2017 | 0 | 1186 KB |
| `act-zm-2017-009-corporate-insolvency` | The Corporate Insolvency | Act No. 9 of 2017 | 204 | 554 KB |
| `act-zm-2017-011-property-transfer-tax-amendment` | The Property Transfer (Amendment) | Act No. 11 of 2017 | 3 | 16 KB |

## Source integrity

All 8 new records passed:
- No duplicate IDs (78 total records in corpus)
- All source_hash values verified against on-disk raw PDF files
- All amended_by references: empty arrays (no cross-references in this tranche)
- All repealed_by references: null
- JSON schema validation: all required fields present, jurisdiction = ZM

## Parse quality notes

Records with ≤ 3 sections (flagged for re-parse):
- **act-zm-2017-008-supplementary-appropriation-2017** (1 section): Schedule-heavy Appropriation Act — full text stored as single section.
- **act-zm-2017-011-property-transfer-tax-amendment** (3 sections): Brief amendment act; verify completeness.

## Fetch summary

- Fetches this batch: 16 (8 node pages + 8 PDFs)
- Total fetches today: 162/2000
- Rate limit honoured: 2s between requests to parliament.gov.zm
- SSL note: parliament.gov.zm certificate verification failed in sandbox; fetched with verify=False (content hashes verified)

## Inventory status

Acts ingested cumulative: 78 records (70 prior + 8 this batch)
Next targets: 2017 Acts No. 12-22 (remaining 2017 tranche)
