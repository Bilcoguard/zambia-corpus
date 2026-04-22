# Batch 0161 Report

**Date:** 2026-04-22T12:06:51Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 7
**Repeal-chain links applied:** 0
**Fetches (script):** 18
**Integrity:** PASS

## Strategy

Probe-only pass. No seed candidates this batch — all targets are surfaced via keyword rotation per the batch-0160 next-tick plan. Stage 2 probes the ZambiaLII search API with eight fresh rotation queries: mining act, fisheries, agriculture, marketing, statistics, companies act, investment, referendum. Hits surviving HEAD + title filters fill slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment` (plus OCR variants `amendrnent` and `amendement`), `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections. No unconditional repeal-chain links are pre-declared for this batch.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-2003-016-prohibition-of-anti-personnel-mines-act-2003` | Prohibition of Anti-Personnel Mines Act, 2003 | Act No. 16 of 2003 | 61 | PDF | probe |
| 2 | `act-zm-1916-011-agricultural-statistics-act-1916` | Agricultural Statistics Act, 1916 | Act No. 11 of 1916 | 15 | HTML/AKN | probe |
| 3 | `act-zm-1986-022-zambia-agricultural-development-bank-dissolution-act-1986` | Zambia Agricultural Development Bank (Dissolution) Act, 1986 | Act No. 22 of 1986 | 7 | PDF | probe |
| 4 | `act-zm-1955-010-census-and-statistics-act-1955` | Census and Statistics Act, 1955 | Act No. 10 of 1955 | 14 | HTML/AKN | probe |
| 5 | `act-zm-1970-018-investment-disputes-convention-act-1970` | Investment Disputes Convention Act, 1970 | Act No. 18 of 1970 | 23 | HTML/AKN | probe |
| 6 | `act-zm-1991-019-investment-act-1991` | Investment Act, 1991 | Act No. 19 of 1991 | 37 | PDF | probe |
| 7 | `act-zm-1967-039-referendum-act-1967` | Referendum Act, 1967 | Act No. 39 of 1967 | 30 | HTML/AKN | probe |

**Total sections:** 187

## Repeal-chain links

No repeal-chain links applied this batch — the pre-declared unconditional link list was empty.

## Seed summary

- Seed candidates queued: 0
- Seed candidates committed: 0
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 8 ('mining act', 'fisheries', 'agriculture', 'marketing', 'statistics', 'companies act', 'investment', 'referendum')
- Candidates discovered (novel): 28
- Candidates surviving HEAD + title filters: 7
- Candidates processed this batch: 7

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- 2020/25 'Mines and Minerals Development (Amendment) Act , 2020': pre-fetch reject — title contains 'amendment' (via query 'mining act')
- 2002/5 'Mines and Minerals (Amendment) Act , 2002': pre-fetch reject — title contains 'amendment' (via query 'mining act')
- 1998/8 'Mines and Minerals (Amendment) Act , 1998': pre-fetch reject — title contains 'amendment' (via query 'mining act')
- 1985/18 'Mines and Minerals (Amendment) Act , 1985': pre-fetch reject — title contains 'amendment' (via query 'mining act')
- 2007/22 'Fisheries Act (Amendment) Act, 2007': pre-fetch reject — title contains 'amendment' (via query 'fisheries')
- 1995/21 'Agriculture (Seeds) (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'agriculture')
- 1990/2 'National Agricultural Marketing (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'agriculture')
- 2020/27 'Zambia Institute of Marketing (Amendment) Act, 2020': pre-fetch reject — title contains 'amendment' (via query 'marketing')
- 1988/7 'Markets (Amendment) Act, 1988': pre-fetch reject — title contains 'amendment' (via query 'marketing')
- 1995/6 'Companies (Amendment) Act , 1995': pre-fetch reject — title contains 'amendment' (via query 'companies act')
- 1986/2 'Companies (Amendment) Act , 1986': pre-fetch reject — title contains 'amendment' (via query 'companies act')
- 1983/7 'Companies (Amendment) Act , 1983': pre-fetch reject — title contains 'amendment' (via query 'companies act')
- 1990/27 'Companies (Amendment) Act , 1990': pre-fetch reject — title contains 'amendment' (via query 'companies act')
- 1993/16 'Companies (Amendment) Act , 1993': pre-fetch reject — title contains 'amendment' (via query 'companies act')
- 2011/24 'Companies (Amendment) Act , 2011': pre-fetch reject — title contains 'amendment' (via query 'companies act')
- 1994/3 'Companies (Amendment) Act , 1994': pre-fetch reject — title contains 'amendment' (via query 'companies act')
- 1995/26 'Investment (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'investment')
- 1998/10 'Investment (Amendment) Act, 1998': pre-fetch reject — title contains 'amendment' (via query 'investment')
- 1996/5 'Investment (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'investment')
- 2001/4 'Electoral (Amendment) Act, 2001': pre-fetch reject — title contains 'amendment' (via query 'referendum')
- 2015/10 'Excess Expenditure Appropriation (2012) Act, 2015': pre-fetch reject — title contains 'appropriation' (via query 'referendum')

## Notes

- No SEED stage this batch — batch 0160 next-tick flagged these as probe rotations rather than direct year/number seeds, since narrower prior probes had not surfaced them.
- B-POL-ACT-1 title filter retains the OCR variants `amendrnent` and `amendement` added in batch 0157.
- No unconditional repeal-chain link applied this batch — the pre-declared list is empty.
- Next tick: if probe yield this batch was <= 2 new primary parents, shift to the alphabetical `/akn/zm/act/` listing traversal fallback for unresolved Cap. parents; otherwise continue the primary-statute sweep with a fresh rotation of narrower probe keywords — forestry, veterinary, animal health, education, legal practitioners, public health, food and drugs, land survey.

