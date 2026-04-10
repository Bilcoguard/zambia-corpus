# Phase 4 Batch 0009 Report

**Generated:** 2026-04-10T17:37:00Z
**Batch:** 0009
**Phase:** 4 — bulk ingestion (acts_in_force)
**Source:** parliament.gov.zm
**Tranche:** 2017 Acts No. 12–19

## Records ingested (8)

| ID | Title | Citation | Sections | PDF Size |
|----|-------|----------|----------|----------|
| `act-zm-2017-012-value-added-tax-amendment` | The Value Added Tax (Amendment) | Act No. 12 of 2017 | 2 | 11 KB |
| `act-zm-2017-013-skills-development-levy-amendment` | The Skills Development Levy (Amendment) | Act No. 13 of 2017 | 1 | 8 KB |
| `act-zm-2017-014-customs-and-excise-amendment` | The Customs and Excise (Amendment) | Act No. 14 of 2017 | 12 | 79 KB |
| `act-zm-2017-015-insurance-premium-levy-amendment` | Insurance Premium Levy (Amendment) | Act No. 15 of 2017 | 1 | 8 KB |
| `act-zm-2017-016-income-tax-amendment` | Income Tax (Amendment) | Act No. 16 of 2017 | 9 | 30 KB |
| `act-zm-2017-017-zambia-national-broadcasting-corporation-amendment` | Zambia National Broadcasting Corporation (Amendment) | Act No. 17 of 2017 | 2 | 9 KB |
| `act-zm-2017-018-independent-broadcasting-authority-amendment` | Independent Broadcasting Authority (Amendment) | Act No. 18 of 2017 | 1 | 13 KB |
| `act-zm-2017-019-industrial-and-labour-relations-amendment` | Industrial and Labour Relations (Amendment) | Act No. 19 of 2017 | 5 | 10 KB |

## Source integrity

All 8 new records passed:
- No duplicate IDs (94 total records in corpus)
- All source_hash values verified against on-disk raw PDF files
- All amended_by references: empty arrays (no cross-references in this tranche)
- All repealed_by references: null
- JSON schema validation: all required fields present, jurisdiction = ZM

## Parse quality notes

Records with ≤ 3 sections (flagged for re-parse):
- **act-zm-2017-012-value-added-tax-amendment** (2 sections): Brief VAT amendment act.
- **act-zm-2017-013-skills-development-levy-amendment** (1 section): Very brief levy amendment; stored as single section.
- **act-zm-2017-015-insurance-premium-levy-amendment** (1 section): Very brief levy amendment; stored as single section.
- **act-zm-2017-017-zambia-national-broadcasting-corporation-amendment** (2 sections): Brief broadcasting amendment.
- **act-zm-2017-018-independent-broadcasting-authority-amendment** (1 section): Brief IBA amendment; stored as single section.

## Fetch summary

- Fetches this batch: 16 (8 node pages + 8 PDFs)
- Total fetches today: 178/2000
- Rate limit honoured: 2s between requests to parliament.gov.zm
- SSL note: parliament.gov.zm certificate verification via requests (verify=False in sandbox; content hashes verified)

## Inventory status

Acts ingested cumulative: 86 acts + 1 judgment = 87 total records (some acts from 2024-2026 batches)
Next targets: 2017 Acts No. 20-22 (Employment Amendment, Supplementary Appropriation, Appropriation) + 2016 acts
