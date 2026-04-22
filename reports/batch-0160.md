# Batch 0160 Report

**Date:** 2026-04-22T11:36:22Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 6
**Repeal-chain links applied:** 0
**Fetches (script):** 15
**Integrity:** PASS

## Strategy

Probe-only pass. No seed candidates this batch — all targets are surfaced via keyword rotation per the batch-0159 next-tick plan. Stage 2 probes the ZambiaLII search API with eight fresh rotation queries: trade, sale of goods, customs, exchange control, local government, traffic, national assembly, citizenship. Hits surviving HEAD + title filters fill slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment` (plus OCR variants `amendrnent` and `amendement`), `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections. No unconditional repeal-chain links are pre-declared for this batch.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-1939-029-trading-with-the-enemy-act-1939` | Trading with the Enemy Act, 1939 | Act No. 29 of 1939 | 16 | HTML/AKN | probe |
| 2 | `act-zm-1956-034-national-assembly-powers-and-privileges-act-1956` | National Assembly (Powers and Privileges) Act, 1956 | Act No. 34 of 1956 | 35 | HTML/AKN | probe |
| 3 | `act-zm-1987-017-zambezi-river-authority-act-1987` | Zambezi River Authority Act, 1987 | Act No. 17 of 1987 | 11 | HTML/AKN | probe |
| 4 | `act-zm-1991-023-national-assembly-staff-act-1991` | National Assembly Staff Act, 1991 | Act No. 23 of 1991 | 8 | PDF | probe |
| 5 | `act-zm-1991-025-national-assembly-staff-act-1991` | National Assembly Staff Act, 1991 | Act No. 25 of 1991 | 7 | HTML/AKN | probe |
| 6 | `act-zm-1991-001-constitution-of-zambia-act-1991` | Constitution of Zambia Act, 1991 | Act No. 1 of 1991 | 16 | HTML/AKN | probe |

**Total sections:** 93

## Repeal-chain links

No repeal-chain links applied this batch — the pre-declared unconditional link list was empty.

## Seed summary

- Seed candidates queued: 0
- Seed candidates committed: 0
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 8 ('trade', 'sale of goods', 'customs', 'exchange control', 'local government', 'traffic', 'national assembly', 'citizenship')
- Candidates discovered (novel): 36
- Candidates surviving HEAD + title filters: 6
- Candidates processed this batch: 6

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- 1993/6 'Trades Licensing (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'trade')
- 2007/15 'Trades Licensing (Amendment) Act, 2007': pre-fetch reject — title contains 'amendment' (via query 'trade')
- 1994/10 'Trades Licensing (Amendment) Act, 1994': pre-fetch reject — title contains 'amendment' (via query 'trade')
- 1990/26 'Trades Licensing (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'trade')
- 1984/10 'Gold Trade (Amendment) Act, 1984': pre-fetch reject — title contains 'amendment' (via query 'trade')
- 2001/2 'Customs and Excise (Amendment) Act, 2001': pre-fetch reject — title contains 'amendment' (via query 'customs')
- 1985/1 'Customs and Excise (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'customs')
- 2008/2 'Customs and Excise (Amendment) Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'customs')
- 1989/25 'Customs and Excise (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'customs')
- 2005/4 'Customs and Excise (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'customs')
- 2004/11 'Customs and Excise (Amendment) (No. 2) Act, 2004': pre-fetch reject — title contains 'amendment' (via query 'customs')
- 1982/8 'Exchange Control (Amendment) Act, 1982': pre-fetch reject — title contains 'amendment' (via query 'exchange control')
- 1988/27 'Exchange Control (Amendment) (No. 2) Act, 1988': pre-fetch reject — title contains 'amendment' (via query 'exchange control')
- 1988/11 'Exchange Control (Amendment) Act, 1988': pre-fetch reject — title contains 'amendment' (via query 'exchange control')
- 1993/30 'Local Government (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 2014/12 'Local Government (Amendment) Act, 2014': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 2004/9 'Local Government (Amendment) Act, 2004': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 1995/30 'Local Government (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 1993/31 'Local Government Elections (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 2006/6 'Road Traffic (Amendment) Act, 2006': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 1997/4 'Roads and Road Traffic (Amendment) Act, 1997': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 1996/4 'Roads and Road Traffic (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 1994/12 'Roads and Road Traffic (Amendment) Act, 1994': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 1989/29 'Roads and Road Traffic (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 2008/4 'Road Traffic (Amendment)Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 2021/49 'Road Traffic (Amendment) Act, 2021': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 1990/10 'Citizenship of Zambia (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'citizenship')
- 1988/24 'Citizenship of Zambia (Amendment) Act, 1988': pre-fetch reject — title contains 'amendment' (via query 'citizenship')
- 1994/34 "President's Citizenship College (Amendment) Act, 1994": pre-fetch reject — title contains 'amendment' (via query 'citizenship')
- 1996/18 'Constitution of Zambia (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'citizenship')

## Notes

- No SEED stage this batch — batch 0159 next-tick flagged these as probe rotations rather than direct year/number seeds, since narrower prior probes had not surfaced them.
- B-POL-ACT-1 title filter retains the OCR variants `amendrnent` and `amendement` added in batch 0157.
- No unconditional repeal-chain link applied this batch — the pre-declared list is empty.
- Next tick: continue primary-statute sweep with a fresh rotation of probe keywords — mining act, fisheries, agriculture, marketing, statistics, companies act, investment, and constitutional referendum. If probe yields continue to fall, shift to alphabetical `/akn/zm/act/` listing traversal for unresolved Cap. parents.

