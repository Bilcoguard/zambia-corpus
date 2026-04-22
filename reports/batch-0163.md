# Batch 0163 Report

**Date:** 2026-04-22T14:43:28Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 5
**Repeal-chain links applied:** 0
**Fetches (script):** 13
**Integrity:** PASS

## Strategy

Seed + probe pass. Stage 1 seeds the Standards Act 1994/20 (deferred from batch 0162 via batch cap after probe 'food and drugs' surfaced it). Stage 2 probes the ZambiaLII search API with eight fresh rotation queries per the batch-0162 next-tick plan: water resources, wildlife, national parks, insurance, pensions, securities, telecommunications, energy regulation. Hits surviving HEAD + title filters fill slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment` (plus OCR variants `amendrnent` and `amendement`), `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections. No unconditional repeal-chain links are pre-declared for this batch.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-1994-020-standards-act-1994` | Standards Act, 1994 | Act No. 20 of 1994 | 39 | HTML/AKN | seed |
| 2 | `act-zm-1915-023-plumage-birds-protection-act-1915` | Plumage Birds Protection Act, 1915 | Act No. 23 of 1915 | 6 | HTML/AKN | probe |
| 3 | `act-zm-1994-023-telecommunications-act-1994` | Telecommunications Act, 1994 | Act No. 23 of 1994 | 44 | HTML/AKN | probe |
| 4 | `act-zm-1995-015-electricity-act-1995` | Electricity Act, 1995 | Act No. 15 of 1995 | 31 | HTML/AKN | probe |
| 5 | `act-zm-1995-016-energy-regulation-act-1995` | Energy Regulation Act, 1995 | Act No. 16 of 1995 | 29 | HTML/AKN | probe |

**Total sections:** 149

## Repeal-chain links

No repeal-chain links applied this batch — the pre-declared unconditional link list was empty.

## Seed summary

- Seed candidates queued: 1
- Seed candidates committed: 1
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 8 ('water resources', 'wildlife', 'national parks', 'insurance', 'pensions', 'securities', 'telecommunications', 'energy regulation')
- Candidates discovered (novel): 17
- Candidates surviving HEAD + title filters: 4
- Candidates processed this batch: 4

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- 2005/10 'Water Supply and Sanitation (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'water resources')
- 2021/53 'Appropriation Act, 2021': pre-fetch reject — title contains 'appropriation' (via query 'water resources')
- 1982/33 'National Parks and Wildlife (Amendment) Act, 1982': pre-fetch reject — title contains 'amendment' (via query 'wildlife')
- 2005/26 'Insurance (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'insurance')
- 2021/47 'Insurance Premium Levy (Amendment) Act, 2021': pre-fetch reject — title contains 'amendment' (via query 'insurance')
- 1992/2 'Insurance (Amendment) Act, 1992': pre-fetch reject — title contains 'amendment' (via query 'insurance')
- 1991/17 'Insurance Brokers (Cessation and Transfer) (Repeal) Act, 1991': pre-fetch reject — title contains 'repeal' (via query 'insurance')
- 1989/28 'Insurance (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'insurance')
- 2005/27 'Pension Scheme Regulation (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'pensions')
- 1985/27 'State Security (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'securities')
- 1999/8 'Telecommunications (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'telecommunications')
- 2007/17 'Penal Code (Amendment) Act, 2007': pre-fetch reject — title contains 'amendment' (via query 'telecommunications')
- 2003/23 'Energy Regulation (Amendment) Act, 2003': pre-fetch reject — title contains 'amendment' (via query 'energy regulation')

## Notes

- SEED stage includes Standards Act 1994/20 (deferred from batch 0162 via batch cap after 'food and drugs' probe).
- B-POL-ACT-1 title filter retains the OCR variants `amendrnent` and `amendement` added in batch 0157.
- No unconditional repeal-chain link applied this batch — the pre-declared list is empty.
- Next tick: if probe yield this batch was <= 2 new primary parents, shift to the alphabetical `/akn/zm/act/` listing traversal fallback for unresolved Cap. parents; otherwise continue the primary-statute sweep with another fresh rotation of narrower probe keywords — water, environment, communications, roads, traffic, lands, petroleum, banking.

