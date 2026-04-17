# Batch 0124 Report

**Date:** 2026-04-17T10:08:51Z
**Phase:** 4 (Bulk Ingestion)
**Source:** ZambiaLII (page 8)
**Records added:** 8
**Total sections:** 228
**Fetches:** 12 (8 HTML + 4 PDF fallback)
**Budget today:** ~131/2000 fetches

## Records

| # | Title | Sections | Source |
|---|-------|----------|--------|
| 1 | Medicines and Allied Substances Act, 2013 | 48 | HTML |
| 2 | Metrology Act, 2017 | 47 | HTML |
| 3 | Markets and Bus Stations Act, 2007 | 10 | PDF |
| 4 | Narcotic Drugs and Psychotropic Substances Act, 2021 | 71 | HTML |
| 5 | Mutual Legal Assistance in Criminal Matters Act, 1993 | 26 | HTML |
| 6 | Mobile Money Transaction Levy Act, 2024 | 6 | PDF |
| 7 | Mineral Royalty Tax Act, 1994 | 9 | PDF |
| 8 | Management Services Board Act, 1981 | 11 | PDF |

## Notes

- 4 records initially had 0 sections from HTML parsing (Medicines & Allied Substances, Metrology, Markets & Bus Stations, Mineral Royalty Tax). PDF fallback successfully extracted sections for all 4.
- 38 pre-existing duplicate ID errors noted (all Appropriation Acts from prior batches stored in multiple paths). No batch 0124 records are affected. Flagged for future cleanup.
- ZambiaLII page 8 has ~34 remaining unprocessed items (local government SIs, medical/medicines SIs, metrology SIs, minimum wages SIs, etc.).
- Pages 9-10 have additional substantive items.

## Next Batch Targets

Continue with page 8 remaining high-value Acts: Lotteries Act 1957, Maintenance Orders Act 1960, Markets Act 1937, Marriage Act 1918, Medical Services Act 1985, Millennium Challenge Compact Act 2013, Mines Acquisition Acts 1970, Minimum Wages Act 1982.

## Integrity

- Duplicate ID check: PASS (for batch records)
- Required fields: PASS
- Source hash: PASS
- Cross-references: PASS
