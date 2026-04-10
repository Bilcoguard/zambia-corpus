# Phase 4 Batch 0010 Report

**Generated:** 2026-04-10T21:00:00Z
**Batch:** 0010
**Phase:** 4 — bulk ingestion (acts_in_force)
**Source:** parliament.gov.zm
**Tranche:** 2021 Acts No. 15–23

## Records ingested (8)

| ID | Title | Citation | Sections | PDF Size |
|----|-------|----------|----------|----------|
| `act-zm-2021-023-higher-education-amendment-act-of-2021` | Higher Education (Amendment) Act of 2021 | Act No. 23 of 2021 | 16 | 106 KB |
| `act-zm-2021-021-health-professions-amendment-act-2021` | Health Professions (Amendment) Act, 2021 | Act No. 21 of 2021 | 3 | 9 KB |
| `act-zm-2021-020-rural-electrification-amendment-act-2021` | Rural Electrification (Amendment) Act, 2021 | Act No. 20 of 2021 | 3 | 10 KB |
| `act-zm-2021-019-national-heritage-conservation-commission-amendment-act-2021` | National Heritage Conservation Commission (Amendment) Act, 2021 | Act No. 19 of 2021 | 2 | 8 KB |
| `act-zm-2021-018-examination-council-of-zambia-amendment-act-2021` | Examination Council of Zambia (Amendment) Act, 2021 | Act No. 18 of 2021 | 2 | 9 KB |
| `act-zm-2021-017-zambia-law-development-commission-amendment-act-2021` | Zambia Law Development Commission (Amendment) Act, 2021 | Act No. 17 of 2021 | 3 | 10 KB |
| `act-zm-2021-016-zambia-institute-of-advanced-legal-education-amendment-act-2021` | Zambia Institute of Advanced Legal Education (Amendment) Act, 2021 | Act No. 16 of 2021 | 3 | 10 KB |
| `act-zm-2021-015-zambia-revenue-authority-amendment-act-2021` | Zambia Revenue Authority (Amendment) Act, 2021 | Act No. 15 of 2021 | 2 | 9 KB |

## Skipped

- **Act No. 22 of 2021** (Public-Private Partnership Amendment): No PDF found on node page (https://www.parliament.gov.zm/node/8834). Logged to gaps.md.

## Source integrity

All 8 new records passed:
- No duplicate IDs (102 total records in corpus)
- All source_hash values verified against on-disk raw PDF files
- All amended_by references: empty arrays (no cross-references in this tranche)
- All repealed_by references: null
- JSON schema validation: all required fields present, jurisdiction = ZM

## Parse quality notes

Records with ≤ 3 sections (flagged for re-parse):
- **act-zm-2021-021-health-professions-amendment-act-2021** (3 sections): Brief amendment act.
- **act-zm-2021-020-rural-electrification-amendment-act-2021** (3 sections): Brief amendment act.
- **act-zm-2021-019-national-heritage-conservation-commission-amendment-act-2021** (2 sections): Brief amendment act.
- **act-zm-2021-018-examination-council-of-zambia-amendment-act-2021** (2 sections): Brief amendment act.
- **act-zm-2021-017-zambia-law-development-commission-amendment-act-2021** (3 sections): Brief amendment act.
- **act-zm-2021-016-zambia-institute-of-advanced-legal-education-amendment-act-2021** (3 sections): Brief amendment act.
- **act-zm-2021-015-zambia-revenue-authority-amendment-act-2021** (2 sections): Brief ZRA amendment.

## Fetch summary

- Page fetches: 9 (1 index page + 8 node pages; Act No. 22 node had no PDF)
- PDF fetches: 8
- Total fetches this batch: 17
- Total fetches today: 195/2000
- Rate limit: 2s between requests (parliament.gov.zm)
- SSL: verify=False (sandbox certificate issue); integrity verified via sha256 hashes
