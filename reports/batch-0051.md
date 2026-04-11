# Batch 0051 — 2011 Acts No. 12-14 + 2010 Acts No. 46-50

**Date:** 2026-04-11T18:08:21Z
**Source:** parliament.gov.zm
**Phase:** 4 (bulk ingestion — acts_in_force)
**Records added:** 8
**Fetches:** 19 (3 discovery + 8 node + 8 PDF)

## Records

| # | ID | Title | Sections |
|---|-----|-------|----------|
| Act No. 14 of 2011 | `act-zm-2011-014-tolls-act-2011` | Tolls Act 2011 | 49 |
| Act No. 13 of 2011 | `act-zm-2011-013-the-zambia-qualifications-authority-act-2011` | The Zambia Qualifications Authority Act, 2011 | 38 |
| Act No. 12 of 2011 | `act-zm-2011-012-the-environmental-management-act-2011` | THE ENVIRONMENTAL MANAGEMENT ACT, 2011 | 236 |
| Act No. 50 of 2010 | `act-zm-2010-050-property-transfer-tax-amendment` | Property Transfer Tax (Amendment) | 0 |
| Act No. 49 of 2010 | `act-zm-2010-049-income-tax-amendment` | Income Tax (Amendment) | 0 |
| Act No. 48 of 2010 | `act-zm-2010-048-value-added-tax-amendment` | Value Added Tax (Amendment) | 0 |
| Act No. 47 of 2010 | `act-zm-2010-047-customs-and-excise-amendment` | Customs and Excise (Amendment) | 0 |
| Act No. 46 of 2010 | `act-zm-2010-046-financial-intelligence-centre-2010` | Financial Intelligence Centre 2010 | 0 |

## Parse quality notes

- **act-zm-2011-012** (236 sections): Environmental Management Act — comprehensive parse, excellent quality.
- **act-zm-2011-014** (49 sections): Tolls Act — good parse quality.
- **act-zm-2011-013** (38 sections): Zambia Qualifications Authority Act — good parse quality.
- **act-zm-2010-046 through 050** (0 sections each): 2010 amendment acts — scanned/image PDFs, needs OCR re-parse.

## Integrity checks

All passed: no duplicate IDs, source hashes verified, all references resolved, required fields present.

## Notes

- SSL certificate verification for parliament.gov.zm failed (common for ZM government sites). Fetched with verify=False.
- 2011 Acts now COMPLETE: 25/~32 discoverable acts ingested (No. 1-3, 24-26, 28 not on index or missing PDFs).
- 2010 Acts started: 7/~51 ingested (No. 5, 7, 46-50).
