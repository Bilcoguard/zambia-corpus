# Batch 0151 Report

**Date:** 2026-04-20T19:37:29Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Repeal-chain links applied:** 1
**Fetches (script):** 14
**Integrity:** PASS

## Strategy

Continuation of the batch 0150 next-tick plan — primary-statute sweep for Wills / Succession / Intestate, Insurance / Pensions, and Co-operative / Friendly Societies parents. Candidate (year, number) pairs were surfaced by probing the ZambiaLII search API (`/search/api/documents/?search=<q>&nature=Act`) for 6 hint queries at batch-0151-probe; each hit was cross-referenced against HEAD by (year, number) tuple via `git ls-tree -r HEAD records/acts/`. Slots whose AKN-page title contained `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` were rejected pre-write without producing any raw or record file. The processor fetches each surviving candidate's AKN page in priority order and stops at MAX_RECORDS=8 accepted primary statutes. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1930-042-penal-code-1930` | Penal Code, 1930 | Act No. 42 of 1930 | 434 | HTML/AKN |
| 2 | `act-zm-1967-030-legal-aid-act-1967` | Legal Aid Act, 1967 | Act No. 30 of 1967 | 27 | HTML/AKN |
| 3 | `act-zm-1996-014-judges-conditions-of-service-act-1996` | Judges (Conditions of Service) Act, 1996 | Act No. 14 of 1996 | 13 | HTML/AKN |
| 4 | `act-zm-1990-025-insurance-levy-act-1990` | Insurance Levy Act, 1990 | Act No. 25 of 1990 | 9 | HTML/AKN |
| 5 | `act-zm-1927-010-european-officers-pensions-act-1927` | European Officers' Pensions Act, 1927 | Act No. 10 of 1927 | 22 | HTML/AKN |
| 6 | `act-zm-1929-031-widows-and-orphans-pension-act-1929` | Widows and Orphans Pension Act, 1929 | Act No. 31 of 1929 | 49 | HTML/AKN |
| 7 | `act-zm-1951-027-pensions-increase-act-1951` | Pensions (Increase) Act, 1951 | Act No. 27 of 1951 | 6 | HTML/AKN |
| 8 | `act-zm-1965-004-transferred-federal-officers-dependants-pensions-act-1965` | Transferred Federal Officers (Dependants) Pensions Act, 1965 | Act No. 4 of 1965 | 13 | HTML/AKN |

**Total sections:** 573

## Repeal-chain links

| # | Source record | Previous `repealed_by` | New `repealed_by` | Note |
|---|----|----|----|----|
| 1 | `records/acts/1957/act-zm-1957-014-trade-marks-act-1957.json` | `None` | `act-zm-2023-011-the-trade-marks-act-2023` | Trade Marks Act 1957 (Cap. 401) superseded by Trade Marks Act 2023 (No. 11 of 2023); 2023 Act transitional provisions reference 'the repealed Act Cap.401'. |

## Probe summary

- Probe queries issued: 6 ('wills administration estates', 'intestate succession', 'insurance act', 'pensions act', 'co-operative societies', 'friendly societies')
- Candidates discovered (raw): 48
- Candidates surviving HEAD + title filters: 17
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

- 1996/28 'Pension Scheme Regulation Act , 1996': batch cap reached (MAX_RECORDS=8) — deferred
- 1961/27 'Dairy Produce Marketing and Levy Act, 1961': batch cap reached (MAX_RECORDS=8) — deferred
- 1967/64 'Tobacco Act, 1967': batch cap reached (MAX_RECORDS=8) — deferred
- 1967/65 'Tobacco Levy Act, 1967': batch cap reached (MAX_RECORDS=8) — deferred
- 1969/28 'Loans and Guarantees (Authorisation) Act, 1969': batch cap reached (MAX_RECORDS=8) — deferred
- 1970/63 'Co - operative Societies Act, 1970': batch cap reached (MAX_RECORDS=8) — deferred
- 1971/30 'Registration and Development of Villages Act, 1971': batch cap reached (MAX_RECORDS=8) — deferred
- 1984/12 'Property Transfer Tax Act, 1984': batch cap reached (MAX_RECORDS=8) — deferred
- 1968/59 'Carriage by Air Act, 1968': batch cap reached (MAX_RECORDS=8) — deferred
- 1989/6 'Wills and Administration of Testate Estates Act, 1989': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 2022/12 'Children’s Code Act, 2022': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 1989/5 'Intestate Succession Act, 1989': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 1996/40 'National Pension Scheme Act, 1996': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 2021/1 'Legal Aid Act, 2021': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 1994/26 'Companies Act, 1994': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 1967/27 'Bankruptcy Act, 1967': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 1960/57 'Agricultural Lands Act, 1960': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 2019/3 'Employment Code Act, 2019': pre-fetch reject — already in HEAD (via query 'intestate succession')
- 1996/35 'Public Service Pensions Act, 1996': pre-fetch reject — already in HEAD (via query 'intestate succession')
- 1966/20 'Local Courts Act, 1966': pre-fetch reject — already in HEAD (via query 'intestate succession')
- 1989/4 'Interpretation and General Provisions (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'intestate succession')
- 1991/8 'Local Courts (Amendment) Act, 1991': pre-fetch reject — title contains 'amendment' (via query 'intestate succession')
- 2018/2 'National Health Insurance Act , 2018': pre-fetch reject — already in HEAD (via query 'insurance act')
- 2005/26 'Insurance (Amendment) Act , 2005': pre-fetch reject — title contains 'amendment' (via query 'insurance act')
- 2015/21 'Insurance Premium Levy Act': pre-fetch reject — already in HEAD (via query 'insurance act')
- 1989/28 'Insurance (Amendment) Act , 1989': pre-fetch reject — title contains 'amendment' (via query 'insurance act')
- 1992/2 'Insurance (Amendment) Act , 1992': pre-fetch reject — title contains 'amendment' (via query 'insurance act')
- 2021/47 'Insurance Premium Levy (Amendment) Act , 2021': pre-fetch reject — title contains 'amendment' (via query 'insurance act')
- 2024/28 'Insurance Premium Levy (Amendment) Act , 2024': pre-fetch reject — already in HEAD (via query 'insurance act')
- 2018/16 'Insurance Premium Levy (Amendment) Act , 2018': pre-fetch reject — already in HEAD (via query 'insurance act')
- 1991/17 'Insurance Brokers (Cessation and Transfer) (Repeal) Act , 1991': pre-fetch reject — title contains 'repeal' (via query 'insurance act')
- 1990/13 'Civil Service (Local Condition) (Amendment) Pensions Act , 1990': pre-fetch reject — title contains 'amendment' (via query 'pensions act')
- 2021/11 'Public Service Pensions (Amendment) Act , 2021': pre-fetch reject — already in HEAD (via query 'pensions act')
- 2015/7 'National Pension Scheme (Amendment) Act , 2015': pre-fetch reject — already in HEAD (via query 'pensions act')
- 1989/24 'Coffee Act, 1989': pre-fetch reject — already in HEAD (via query 'co-operative societies')
- 1993/27 'Industrial and Labour Relations Act, 1993': pre-fetch reject — already in HEAD (via query 'co-operative societies')
- 1995/29 'Lands Act': pre-fetch reject — already in HEAD (via query 'co-operative societies')
- 1923/9 'British Acts Extension Act, 1923': pre-fetch reject — already in HEAD (via query 'friendly societies')
- 1968/46 'Building Societies Act, 1968': pre-fetch reject — already in HEAD (via query 'friendly societies')
- 1956/5 'Adoption Act, 1956': pre-fetch reject — already in HEAD (via query 'friendly societies')

## Notes

- B-POL-ACT-1 title filter applied pre-write: any candidate whose AKN-page title contained `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` was rejected without producing a raw or record file.
- Next tick: continue the primary-statute sweep with further probe queries on Insurance, Copyright, Patents, Companies (secondary caps), and Land / Lands Tribunal where gaps remain; also revisit the Patents Act Cap.400 parent and the Copyright and Performance Rights Act Cap.406 parent.

