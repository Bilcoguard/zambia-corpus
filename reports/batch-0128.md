# Batch 0128 Report

**Date:** 2026-04-17
**Phase:** 4 (Bulk Ingestion)
**Worker:** KateWestonLegal-CorpusBuilder/1.0
**Parser version:** 0.5.0

## Records Added: 8

| # | ID | Title | Year | Sections | Source |
|---|---|---|---|---|---|
| 1 | act-zm-2013-002-national-health-research-act-2013 | National Health Research Act, 2013 | 2013 | 7 | HTML |
| 2 | act-zm-2007-001-national-payment-systems-act-2007 | National Payment Systems Act, 2007 | 2007 | 10 | HTML |
| 3 | act-zm-2002-010-national-hiv-aids-sti-tb-council-act-2002 | National HIV/AIDS/STI/TB Council Act, 2002 | 2002 | 7 | HTML |
| 4 | act-zm-2002-013-national-road-fund-act-2002 | National Road Fund Act, 2002 | 2002 | 27 | HTML |
| 5 | act-zm-2016-026-ministers-prescribed-number-and-responsibilities-act-2016 | Ministers (Prescribed Number and Responsibilities) Act, 2016 | 2016 | 7 | HTML |
| 6 | act-zm-1989-023-national-heritage-conservation-commission-act-1989 | National Heritage Conservation Commission Act, 1989 | 1989 | 51 | HTML |
| 7 | act-zm-1995-034-national-road-safety-council-act-1995 | National Road Safety Council Act, 1995 | 1995 | 7 | HTML |
| 8 | act-zm-2025-002-geological-and-minerals-development-act-2025 | Geological and Minerals Development Act, 2025 | 2025 | 19 | HTML |

## Statistics

- **Total sections parsed:** 135
- **Total fetches this batch:** 8
- **Today's cumulative fetches:** ~165/2000
- **Source:** ZambiaLII HTML (all 8 records)
- **Integrity checks:** ALL PASS (0 errors, 48 pre-existing duplicate warnings from prior batches)

## Subject Coverage

- **Health/Research:** National Health Research Act 2013, National HIV/AIDS/STI/TB Council Act 2002
- **Finance/Infrastructure:** National Payment Systems Act 2007, National Road Fund Act 2002, National Road Safety Council Act 1995
- **Governance:** Ministers (Prescribed Number and Responsibilities) Act 2016
- **Heritage:** National Heritage Conservation Commission Act 1989
- **Mining/Geology:** Geological and Minerals Development Act 2025

## Notes

- All records sourced from ZambiaLII HTML pages (Akoma Ntoso format)
- National Heritage Conservation Commission Act 1989 had the richest content (51 sections)
- Geological and Minerals Development Act 2025 is the newest legislation added to corpus
- Some Acts with low section counts (7 sections) may have additional content in PDF that could be enriched in a future pass; HTML section boundaries reflect Akoma Ntoso markup which may group subsections differently

## Next Batch Targets

Remaining unprocessed Acts from pages 8-10:
- Mineral Tax Act, 1989
- Mines Acquisition (Special Provisions) Act, 1970
- Mineral Royalty (Repeal) Act, 1997
- Plus ~60 additional items on pages 9-10 (National Assembly Staff Acts, National College Acts, etc.)
