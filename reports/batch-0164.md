# Batch 0164 Report

**Date:** 2026-04-22T15:06:07Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 6
**Repeal-chain links applied:** 0
**Fetches (script):** 17
**Integrity:** PASS

## Strategy

Probe-only pass. Stage 2 probes the ZambiaLII search API with eight fresh narrower rotation queries per the batch-0163 next-tick plan: water, environment, communications, roads, traffic, lands, petroleum, banking. Hits surviving HEAD + title filters fill slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment` (plus OCR variants `amendrnent` and `amendement`), `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections. No SEED candidates this batch; no unconditional repeal-chain links are pre-declared.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-1948-034-water-act-1948` | Water Act, 1948 | Act No. 34 of 1948 | 59 | HTML/AKN | probe |
| 2 | `act-zm-1960-034-inland-waters-shipping-act-1960` | Inland Waters Shipping Act, 1960 | Act No. 34 of 1960 | 26 | HTML/AKN | probe |
| 3 | `act-zm-1991-009-zambia-institute-of-mass-communication-act-1991` | Zambia Institute of Mass Communication Act, 1991 | Act No. 9 of 1991 | 13 | PDF | probe |
| 4 | `act-zm-1930-028-petroleum-act-1930` | Petroleum Act, 1930 | Act No. 28 of 1930 | 5 | HTML/AKN | probe |
| 5 | `act-zm-1985-013-petroleum-exploration-and-production-act-1985` | Petroleum (Exploration and Production) Act, 1985 | Act No. 13 of 1985 | 51 | HTML/AKN | probe |
| 6 | `act-zm-1963-075-international-bank-loan-act-1963` | International Bank Loan Act, 1963 | Act No. 75 of 1963 | 5 | HTML/AKN | probe |

**Total sections:** 159

## Repeal-chain links

No repeal-chain links applied this batch — the pre-declared unconditional link list was empty.

## Seed summary

- Seed candidates queued: 0
- Seed candidates committed: 0
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 8 ('water', 'environment', 'communications', 'roads', 'traffic', 'lands', 'petroleum', 'banking')
- Candidates discovered (novel): 27
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

- 2009/21 'Electronic Communications and Transactions Act, 2009': no parseable sections in HTML or PDF
- 2005/10 'Water Supply and Sanitation (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'water')
- 1999/12 'Environment Protection and Pollution Control (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'environment')
- 2005/15 'Penal Code (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'environment')
- 1996/19 'Zambia Institute of Mass Communications (Repeal) Act, 1996': pre-fetch reject — title contains 'repeal' (via query 'communications')
- 2010/3 'Information and Communication Technologies Amendment) Act, 2010': pre-fetch reject — title contains 'amendment' (via query 'communications')
- 1994/12 'Roads and Road Traffic (Amendment) Act, 1994': pre-fetch reject — title contains 'amendment' (via query 'roads')
- 1997/4 'Roads and Road Traffic (Amendment) Act, 1997': pre-fetch reject — title contains 'amendment' (via query 'roads')
- 1993/14 'Roads and Road Traffic (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'roads')
- 1990/30 'Roads and Road Traffic (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'roads')
- 1985/4 'Roads and Road Traffic (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'roads')
- 1989/29 'Roads and Road Traffic (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'roads')
- 2006/6 'Road Traffic (Amendment) Act, 2006': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 1996/4 'Roads and Road Traffic (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 2008/4 'Road Traffic (Amendment)Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 2021/49 'Road Traffic (Amendment) Act, 2021': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 1985/15 'Land (Conversion of Titles) (Amendment) (No. 2) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'lands')
- 1996/20 'Lands (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'lands')
- 1995/8 'Petroleum (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'petroleum')
- 1996/2 'Bank of Zambia (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'banking')
- 2001/11 'Development Bank of Zambia (Amendment) Act, 2001': pre-fetch reject — title contains 'amendment' (via query 'banking')

## Notes

- No SEED stage this batch — batch 0163's seed (Standards Act 1994/20) was standalone and no new seed candidates were deferred into 0164.
- B-POL-ACT-1 title filter retains the OCR variants `amendrnent` and `amendement` added in batch 0157.
- No unconditional repeal-chain link applied this batch — the pre-declared list is empty.
- Next tick: if probe yield this batch is <= 2 new primary parents, shift to the alphabetical `/akn/zm/act/` listing traversal fallback for unresolved Cap. parents; otherwise continue the primary-statute sweep with another fresh rotation of narrower probe keywords — mines and minerals, environmental management, postal, railways, civil aviation, housing, prisons, correctional.

