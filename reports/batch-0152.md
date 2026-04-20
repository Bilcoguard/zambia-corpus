# Batch 0152 Report

**Date:** 2026-04-20T20:07:59Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Repeal-chain links applied:** 0
**Fetches (script):** 16
**Integrity:** PASS

## Strategy

Continuation of the batch 0151 next-tick plan — primary-statute sweep for Patents (Cap. 400 parent), Copyright and Performance Rights (Cap. 406 parent), Chartered Institute of Public Relations, Tobacco, Co-operative Societies, Property Transfer Tax, Carriage by Air, and Loans and Guarantees families. Candidate (year, number) pairs were surfaced by probing the ZambiaLII search API (`/search/api/documents/?search=<q>&nature=Act`) for 8 hint queries at batch-0152-probe; each hit was cross-referenced against HEAD by (year, number) tuple via `git ls-tree -r HEAD records/acts/`. Slots whose AKN-page title contained `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` were rejected pre-write without producing any raw or record file. The processor fetches each surviving candidate's AKN page in priority order and stops at MAX_RECORDS=8 accepted primary statutes. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1965-027-state-proceedings-act-1965` | State Proceedings Act, 1965 | Act No. 27 of 1965 | 32 | HTML/AKN |
| 2 | `act-zm-1967-064-tobacco-act-1967` | Tobacco Act, 1967 | Act No. 64 of 1967 | 108 | HTML/AKN |
| 3 | `act-zm-1967-065-tobacco-levy-act-1967` | Tobacco Levy Act, 1967 | Act No. 65 of 1967 | 17 | HTML/AKN |
| 4 | `act-zm-1961-027-dairy-produce-marketing-and-levy-act-1961` | Dairy Produce Marketing and Levy Act, 1961 | Act No. 27 of 1961 | 32 | HTML/AKN |
| 5 | `act-zm-1969-028-loans-and-guarantees-authorisation-act-1969` | Loans and Guarantees (Authorisation) Act, 1969 | Act No. 28 of 1969 | 29 | HTML/AKN |
| 6 | `act-zm-1970-063-co-operative-societies-act-1970` | Co-operative Societies Act, 1970 | Act No. 63 of 1970 | 172 | HTML/AKN |
| 7 | `act-zm-1971-030-registration-and-development-of-villages-act-1971` | Registration and Development of Villages Act, 1971 | Act No. 30 of 1971 | 20 | HTML/AKN |
| 8 | `act-zm-1984-012-property-transfer-tax-act-1984` | Property Transfer Tax Act, 1984 | Act No. 12 of 1984 | 14 | HTML/AKN |

**Total sections:** 424

## Repeal-chain links

No new repeal-chain links applied this batch — deferred until the Insurance Act Cap.392 parent and the Patents Act Cap.400 parent are confirmed.

## Probe summary

- Probe queries issued: 8 ('patents act', 'copyright performance rights', 'chartered institute public relations', 'tobacco act', 'co-operative societies', 'property transfer tax', 'carriage by air', 'loans and guarantees')
- Candidates discovered (raw): 71
- Candidates surviving HEAD + title filters: 13
- Candidates processed this batch: 8

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no new cross-references introduced this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- 1968/59 'Carriage by Air Act, 1968': batch cap reached (MAX_RECORDS=8) — deferred
- 1950/18 'Rhodesia Railways Loans Guarantee Act, 1950': batch cap reached (MAX_RECORDS=8) — deferred
- 1964/51 'General Loans ( Guarantee ) Act, 1964': batch cap reached (MAX_RECORDS=8) — deferred
- 1972/24 'National Savings and Credit Act, 1972': batch cap reached (MAX_RECORDS=8) — deferred
- 1980/14 'Corrupt Practice Act, 1980': batch cap reached (MAX_RECORDS=8) — deferred
- 2016/40 'Patents Act , 2016': pre-fetch reject — already in HEAD (via query 'patents act')
- 1987/26 'Patents (Amendment) Act , 1987': pre-fetch reject — title contains 'amendment' (via query 'patents act')
- 2010/14 'Patents (Amendment) Act , 2010': pre-fetch reject — already in HEAD (via query 'patents act')
- 2010/15 'Patents and Companies Registration Agency Act , 2010': pre-fetch reject — already in HEAD (via query 'patents act')
- 2020/4 'Patents and Companies Registration Agency Act , 2020': pre-fetch reject — already in HEAD (via query 'patents act')
- 1980/18 'Patents (Amendment) Act , 1980': pre-fetch reject — title contains 'amendment' (via query 'patents act')
- 2013/12 'Patents and Companies Registration Agency (Amendment) Act , 2013': pre-fetch reject — already in HEAD (via query 'patents act')
- 2016/41 'Securities Act , 2016': pre-fetch reject — already in HEAD (via query 'patents act')
- 2017/10 'Companies Act , 2017': pre-fetch reject — already in HEAD (via query 'patents act')
- 2017/9 'Corporate Insolvency Act , 2017': pre-fetch reject — already in HEAD (via query 'patents act')
- 1994/44 'Copyright and Performance Rights Act, 1994': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 2010/25 'Copyright and Performance Rights (Amendment) Act, 2010': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 2010/24 'Competition and Consumer Protection Act, 2010': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 2024/27 'Property Transfer Tax (Amendment) Act, 2024': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 1987/16 'Zambia National Broadcasting Corporation Act, 1987': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 1994/26 'Companies Act, 1994': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 2013/6 'Millennium Challenge Compact Act, 2013': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 1967/27 'Bankruptcy Act, 1967': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 2019/12 'Energy Regulation Act, 2019': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2010/18 'Immigration and Deportation Act, 2010': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2002/12 'Public Roads Act, 2002': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2023/18 'Public -Private Partnership Act, 2023': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2008/13 'Accountants Act, 2008': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2018/13 'Statistics Act, 2018': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2014/4 'Zambia Chartered Institute of Logistics and Transport Act, 2014': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2022/5 'Bank of Zambia Act, 2022': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2015/13 'Tourism and Hospitality Act, 2015': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2022/10 'Tobacco Act , 2022': pre-fetch reject — already in HEAD (via query 'tobacco act')
- 2022/12 'Children’s Code Act , 2022': pre-fetch reject — already in HEAD (via query 'tobacco act')
- 2023/25 'Customs and Excise (Amendment) Act , 2023': pre-fetch reject — already in HEAD (via query 'tobacco act')
- 2011/20 'Liquor Licensing Act , 2011': pre-fetch reject — already in HEAD (via query 'tobacco act')
- 2023/2 'Controlled Substances Act , 2023': pre-fetch reject — already in HEAD (via query 'tobacco act')
- 1965/56 'Prisons Act , 1965': pre-fetch reject — already in HEAD (via query 'tobacco act')
- 1999/4 'Customs and Excise (Amendment) Act , 1999': pre-fetch reject — title contains 'amendment' (via query 'tobacco act')
- 2020/3 'Food and Nutrition Act , 2020': pre-fetch reject — already in HEAD (via query 'tobacco act')
- 1989/24 'Coffee Act, 1989': pre-fetch reject — already in HEAD (via query 'co-operative societies')
- 1993/27 'Industrial and Labour Relations Act, 1993': pre-fetch reject — already in HEAD (via query 'co-operative societies')
- 1995/29 'Lands Act': pre-fetch reject — already in HEAD (via query 'co-operative societies')
- 2025/21 'Property Transfer Tax (Amendment) Act, 2025': pre-fetch reject — already in HEAD (via query 'property transfer tax')
- 2003/4 'Property Transfer Tax (Amendment) Act, 2003': pre-fetch reject — title contains 'amendment' (via query 'property transfer tax')

## Notes

- B-POL-ACT-1 title filter applied pre-write: any candidate whose AKN-page title contained `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` was rejected without producing a raw or record file.
- Next tick: continue the primary-statute sweep with further probe queries on Sale of Goods, Bills of Exchange, Juveniles Act parent (Cap. 53), Hire Purchase Act, Stamp Duty Act parent, and Insurance Act Cap. 392 parent (likely 1997); also revisit any deferred candidates from the batch cap.

