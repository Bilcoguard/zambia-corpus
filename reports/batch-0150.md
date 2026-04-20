# Batch 0150 Report

**Date:** 2026-04-20T19:08:19Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Repeal-chain links applied:** 1
**Fetches (script):** 14
**Integrity:** PASS

## Strategy

Continuation of the batch 0149 next-tick plan — continue the primary-statute sweep for Cap-era parents (Sale of Goods, Employers and Workers, Probate and Administration of Estates, Hire-Purchase, Bills of Exchange, Landlord and Tenant (Residential)). Candidate (year, number) pairs were surfaced by probing the ZambiaLII search API (`/search/api/documents/?search=<q>&nature=Act`) for 6 hint queries at batch-0150-probe; each hit was cross-referenced against HEAD by (year, number) tuple via `git ls-tree -r HEAD records/acts/`. Slots whose AKN-page title contained `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` were rejected pre-write without producing any raw or record file. The processor fetches each surviving candidate's AKN page in priority order and stops at MAX_RECORDS=8 accepted primary statutes. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1992-013-casino-act-1992` | Casino Act, 1992 | Act No. 13 of 1992 | 18 | HTML/AKN |
| 2 | `act-zm-1996-029-small-enterprise-development-act-1996` | Small Enterprise Development Act, 1996 | Act No. 29 of 1996 | 36 | HTML/AKN |
| 3 | `act-zm-2009-024-health-professions-act-2009` | Health Professions Act, 2009 | Act No. 24 of 2009 | 78 | HTML/AKN |
| 4 | `act-zm-1914-015-lands-and-deeds-registry-act-1914` | Lands and Deeds Registry Act, 1914 | Act No. 15 of 1914 | 92 | HTML/AKN |
| 5 | `act-zm-1923-009-british-acts-extension-act-1923` | British Acts Extension Act, 1923 | Act No. 9 of 1923 | 5 | HTML/AKN |
| 6 | `act-zm-1959-005-cheques-act-1959` | Cheques Act, 1959 | Act No. 5 of 1959 | 8 | HTML/AKN |
| 7 | `act-zm-1967-026-law-reform-miscellaneous-provisions-act-1967` | Law Reform (Miscellaneous Provisions) Act, 1967 | Act No. 26 of 1967 | 15 | HTML/AKN |
| 8 | `act-zm-1982-017-railways-act-1982` | Railways Act, 1982 | Act No. 17 of 1982 | 105 | HTML/AKN |

**Total sections:** 357

## Repeal-chain links

| # | Source record | Previous `repealed_by` | New `repealed_by` | Note |
|---|----|----|----|----|
| 1 | `records/acts/1972/act-zm-1972-010-rent-act-1972.json` | `None` | `act-zm-2018-003-rent-act` | Rent Act 1972 superseded by Rent Act 2018 (No. 3 of 2018) |

## Probe summary

- Probe queries issued: 6 ('sale of goods', 'employers and workers', 'probate administration estates', 'hire purchase', 'bills of exchange', 'landlord tenant residential')
- Candidates discovered (raw): 45
- Candidates surviving HEAD + title filters: 10
- Candidates processed this batch: 8

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — all new repealed_by targets verified in HEAD before write
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- 1995/10 'Tanzania-Zambia Railway Act, 1995': batch cap reached (MAX_RECORDS=8) — deferred
- 1971/34 'Landlord and Tenant (Business Premises) Act, 1971': batch cap reached (MAX_RECORDS=8) — deferred
- 1968/25 'Misrepresentation Act, 1968': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2019/3 'Employment Code Act, 2019': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2017/9 'Corporate Insolvency Act, 2017': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2010/38 'Anti-Corruption Act, 2010': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2012/3 'Anti-Corruption Act, 2012': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2002/11 'Road Traffic Act, 2002': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2010/24 'Competition and Consumer Protection Act, 2010': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2009/15 'Information and Communication Technologies Act, 2009': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2015/15 'Employment (Amendment) Act, 2015': pre-fetch reject — already in HEAD (via query 'employers and workers')
- 2010/18 'Immigration and Deportation Act, 2010': pre-fetch reject — already in HEAD (via query 'employers and workers')
- 1999/10 "Workers ' Compensation Act, 1999": pre-fetch reject — already in HEAD (via query 'employers and workers')
- 1973/20 'Medical Examination of Young Persons (Underground Work) Act, 1973': pre-fetch reject — already in HEAD (via query 'employers and workers')
- 1993/27 'Industrial and Labour Relations Act, 1993': pre-fetch reject — already in HEAD (via query 'employers and workers')
- 2008/11 'Anti-Human Trafficking Act, 2008': pre-fetch reject — already in HEAD (via query 'employers and workers')
- 1982/25 'Minimum Wages and Conditions of Employment , 1982': pre-fetch reject — already in HEAD (via query 'employers and workers')
- 1989/6 'Wills and Administration of Testate Estates Act, 1989': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1960/41 'High Court Act': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1925/20 "Administrator -General's Act, 1925": pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 2021/1 'Legal Aid Act, 2021': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1949/21 'Mental Disorders Act, 1949': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1936/22 'Probates (Resealing) Act, 1936': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1951/2 'Consular Conventions Act, 1951': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1973/22 'Legal Practitioners Act, 1973': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1967/27 'Bankruptcy Act, 1967': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1998/12 'Zambia Wildlife Act, 1998': pre-fetch reject — already in HEAD (via query 'hire purchase')
- 2011/12 'Environmental Management Act, 2011': pre-fetch reject — already in HEAD (via query 'hire purchase')
- 2008/12 'Public Procurement Act, 2008': pre-fetch reject — already in HEAD (via query 'hire purchase')
- 2010/27 'Animal Health Act, 2010': pre-fetch reject — already in HEAD (via query 'hire purchase')
- 2015/14 'Zambia Wildlife Act, 2015': pre-fetch reject — already in HEAD (via query 'hire purchase')
- 1999/12 'Environment Protection and Pollution Control (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'hire purchase')
- 2018/8 'Credit Reporting Act, 2018': pre-fetch reject — already in HEAD (via query 'hire purchase')
- 2017/10 'Companies Act, 2017': pre-fetch reject — already in HEAD (via query 'bills of exchange')
- 1996/43 'Bank of Zambia Act, 1996': pre-fetch reject — already in HEAD (via query 'bills of exchange')
- 1972/21 'National College for Management and Development Studies Act, 1972': pre-fetch reject — already in HEAD (via query 'bills of exchange')
- 1990/32 'Stamp Duty (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'bills of exchange')

## Notes

- B-POL-ACT-1 title filter applied pre-write: any candidate whose AKN-page title contained `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` was rejected without producing a raw or record file.
- Next tick: continue the primary-statute sweep with further probe queries on Wills, Succession, Intestate, Insurance, Pensions (where gaps remain), and Co-operatives; also revisit the Trade Marks 1957/14 → Trade Marks Act 2023/11 repeal-link question if the 2023 Trade Marks Act is a successor rather than a pure amendment.

