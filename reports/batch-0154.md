# Batch 0154 Report

**Date:** 2026-04-20T21:06:40Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 6
**Repeal-chain links applied:** 0
**Fetches (script):** 13
**Integrity:** PASS

## Strategy

Two-stage candidate generation. Stage 1 processes the 5 MAX_RECORDS-deferred candidates that batch 0153's probe flagged in `gaps.md` (year/number already verified in that probe): Workers' Compensation 1963/65, National Council for Construction 2003/13, Value Added Tax 1995/4, Mines and Minerals 1995/31, Pension Scheme Regulation 1996/28. (Control of Goods 1954/12 was also on the batch-0153 deferred list but is already present in HEAD, so it is omitted.) Stage 2 probes the ZambiaLII search API with six broader queries (arbitration, adult literacy, cotton, water resources management, patents 1958, insurance); hits surviving HEAD + title filters fill remaining slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-1963-065-workers-compensation-act-1963` | Workers' Compensation Act, 1963 | Act No. 65 of 1963 | 131 | HTML/AKN | seed |
| 2 | `act-zm-2003-013-national-council-for-construction-act-2003` | National Council for Construction Act, 2003 | Act No. 13 of 2003 | 74 | PDF | seed |
| 3 | `act-zm-1995-004-value-added-tax-act-1995` | Value Added Tax Act, 1995 | Act No. 4 of 1995 | 73 | HTML/AKN | seed |
| 4 | `act-zm-1995-031-mines-and-minerals-act-1995` | Mines and Minerals Act, 1995 | Act No. 31 of 1995 | 136 | HTML/AKN | seed |
| 5 | `act-zm-1996-028-pension-scheme-regulation-act-1996` | Pension Scheme Regulation Act, 1996 | Act No. 28 of 1996 | 46 | HTML/AKN | seed |
| 6 | `act-zm-1914-004-cotton-act-1914` | Cotton Act, 1914 | Act No. 4 of 1914 | 3 | HTML/AKN | probe |

**Total sections:** 463

## Repeal-chain links

No new repeal-chain links applied this batch — deferred until remaining parent-Act anchors are confirmed.

## Seed summary

- Seed candidates queued: 5
- Seed candidates committed: 5
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 6 ('arbitration', 'adult literacy', 'cotton', 'water resources management', 'patents 1958', 'insurance')
- Candidates discovered (novel): 12
- Candidates surviving HEAD + title filters: 1
- Candidates processed this batch: 1

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no new cross-references introduced this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- 2008/8 'Industrial and Labour Relations (Amendment) Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'arbitration')
- 2021/53 'Appropriation Act, 2021': pre-fetch reject — title contains 'appropriation' (via query 'adult literacy')
- 2020/26 'Appropriation Act, 2020': pre-fetch reject — title contains 'appropriation' (via query 'adult literacy')
- 2008/2 'Customs and Excise (Amendment) Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'cotton')
- 2001/2 'Customs and Excise (Amendment) Act, 2001': pre-fetch reject — title contains 'amendment' (via query 'cotton')
- 1984/2 'Sales Tax (Amendment) Act, 1984': pre-fetch reject — title contains 'amendment' (via query 'cotton')
- 2005/26 'Insurance (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'insurance')
- 2021/47 'Insurance Premium Levy (Amendment) Act, 2021': pre-fetch reject — title contains 'amendment' (via query 'insurance')
- 1992/2 'Insurance (Amendment) Act, 1992': pre-fetch reject — title contains 'amendment' (via query 'insurance')
- 1991/17 'Insurance Brokers (Cessation and Transfer) (Repeal) Act, 1991': pre-fetch reject — title contains 'repeal' (via query 'insurance')
- 1989/28 'Insurance (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'insurance')

## Notes

- Seed candidates are primary statutes that batch 0151/0152 title-filtered in prior probes and verified as not-in-HEAD by (year, number) tuple lookup; no re-probe was required.
- B-POL-ACT-1 title filter applied pre-write for probe-stage candidates: any slot whose AKN-page title contained an amendment-style token was rejected without raw or record file.
- Next tick: continue the primary-statute sweep — Juveniles Act parent (Cap. 53), Hire Purchase Act parent, Stamp Duty parent, Sale of Goods parent, Bills of Exchange parent, Insurance Cap. 392 parent (if not surfaced by this probe); Patents Cap. 400 and Copyright Cap. 406 parents remain unresolved by batches 0146, 0152 and 0153 probes.

