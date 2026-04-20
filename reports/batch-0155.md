# Batch 0155 Report

**Date:** 2026-04-20T21:36:07Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 3
**Repeal-chain links applied:** 0
**Fetches (script):** 11
**Integrity:** PASS

## Strategy

Probe-only pass — batch-0154 deferred no probe candidates, so no SEED stage runs this batch. Stage 2 probes the ZambiaLII search API with eight queries targeting remaining primary parents flagged unresolved by batch-0154's wrap-up: juveniles, hire purchase, sale of goods, bills of exchange, road traffic, public health, firearms, local government. Hits surviving HEAD + title filters fill slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-1930-012-public-health-act-1930` | Public Health Act, 1930 | Act No. 12 of 1930 | 116 | HTML/AKN | probe |
| 2 | `act-zm-1969-045-firearms-act-1969` | Firearms Act, 1969 | Act No. 45 of 1969 | 63 | HTML/AKN | probe |
| 3 | `act-zm-1970-040-refugees-control-act-1970` | Refugees (Control) Act, 1970 | Act No. 40 of 1970 | 18 | HTML/AKN | probe |

**Total sections:** 197

## Repeal-chain links

No new repeal-chain links applied this batch — deferred until remaining parent-Act anchors are confirmed.

## Seed summary

- Seed candidates queued: 0
- Seed candidates committed: 0
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 8 ('juveniles', 'hire purchase', 'sale of goods', 'bills of exchange', 'road traffic', 'public health', 'firearms', 'local government')
- Candidates discovered (novel): 21
- Candidates surviving HEAD + title filters: 3
- Candidates processed this batch: 3

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no new cross-references introduced this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- 2011/3 'Juveniles (Amendment) Act, 2011': pre-fetch reject — title contains 'amendment' (via query 'juveniles')
- 1999/12 'Environment Protection and Pollution Control (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'hire purchase')
- 1990/32 'Stamp Duty (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'bills of exchange')
- 1997/4 'Roads and Road Traffic (Amendment) Act, 1997': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1996/4 'Roads and Road Traffic (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1989/29 'Roads and Road Traffic (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1994/12 'Roads and Road Traffic (Amendment) Act, 1994': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 2006/6 'Road Traffic (Amendment) Act, 2006': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1992/7 'Roads and Road Traffic (Amendment) Act, 1992': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 2008/4 'Road Traffic (Amendment)Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1985/4 'Roads and Road Traffic (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1986/16 'Firearms (Amendment) Act, 1986': pre-fetch reject — title contains 'amendment' (via query 'firearms')
- 1985/29 'Firearm (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'firearms')
- 1993/30 'Local Government (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 2014/12 'Local Government (Amendment) Act, 2014': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 2004/9 'Local Government (Amendment) Act, 2004': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 1995/30 'Local Government (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 1993/31 'Local Government Elections (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'local government')

## Notes

- No SEED stage this batch — batch-0154 deferred no probe candidates; all batch-0154 seeds were committed in that tick.
- B-POL-ACT-1 title filter applied pre-write for probe-stage candidates: any slot whose AKN-page title contained an amendment-style token was rejected without raw or record file.
- Next tick: continue the primary-statute sweep — rotate probe keywords to surface remaining unresolved parents (banking-and-financial-services pre-2017, mental-health pre-2019, fisheries pre-2011 parent, forests pre-2015 parent, road-traffic parent if not surfaced this batch); Patents Cap. 400 and Copyright Cap. 406 parents remain unresolved by prior probes and may be pre-independence ordinances not carried on ZambiaLII.

