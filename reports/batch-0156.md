# Batch 0156 Report

**Date:** 2026-04-20T22:06:28Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 4
**Repeal-chain links applied:** 0
**Fetches (script):** 14
**Integrity:** PASS

## Strategy

Probe-only pass — batch-0155 processed all three surviving probe candidates, so no SEED stage runs this batch. Stage 2 probes the ZambiaLII search API with eight queries targeting fresh primary-parent targets flagged unresolved by the batch-0155 wrap-up: banking and financial services, mental health, fisheries, forests, national health insurance, securities, plus a direct 'patents act' retry and 'roads and road traffic' (parent not surfaced by batch-0155's narrower probe). Hits surviving HEAD + title filters fill slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-1999-007-forests-act-1999` | Forests Act, 1999 | Act No. 7 of 1999 | 107 | HTML/AKN | probe |
| 2 | `act-zm-1960-005-preservation-of-public-security-act-1960` | Preservation of Public Security Act, 1960 | Act No. 5 of 1960 | 6 | HTML/AKN | probe |
| 3 | `act-zm-1964-054-government-securities-act-1964` | Government Securities Act, 1964 | Act No. 54 of 1964 | 5 | HTML/AKN | probe |
| 4 | `act-zm-1969-036-state-security-act-1969` | State Security Act, 1969 | Act No. 36 of 1969 | 19 | HTML/AKN | probe |

**Total sections:** 137

## Repeal-chain links

No new repeal-chain links applied this batch — deferred until remaining parent-Act anchors are confirmed.

## Seed summary

- Seed candidates queued: 0
- Seed candidates committed: 0
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 8 ('banking and financial services', 'mental health', 'fisheries', 'forests', 'national health insurance', 'securities', 'patents act', 'roads and road traffic')
- Candidates discovered (novel): 21
- Candidates surviving HEAD + title filters: 5
- Candidates processed this batch: 5

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no new cross-references introduced this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- 2000/18 'Banking and Financial Services (Amendrnent) Act, 2000': no parseable sections in HTML or PDF
- 1995/28 'Banking and Financial Services (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'banking and financial services')
- 2005/25 'Banking and Financial Services (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'banking and financial services')
- 2007/22 'Fisheries Act (Amendment) Act, 2007': pre-fetch reject — title contains 'amendment' (via query 'fisheries')
- 1981/15 'Forest (Amendment) Act, 1981': pre-fetch reject — title contains 'amendment' (via query 'forests')
- 1985/27 'State Security (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'securities')
- 1987/26 'Patents (Amendment) Act , 1987': pre-fetch reject — title contains 'amendment' (via query 'patents act')
- 1980/18 'Patents (Amendment) Act , 1980': pre-fetch reject — title contains 'amendment' (via query 'patents act')
- 1989/29 'Roads and Road Traffic (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1997/4 'Roads and Road Traffic (Amendment) Act, 1997': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1996/4 'Roads and Road Traffic (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1994/12 'Roads and Road Traffic (Amendment) Act, 1994': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1985/4 'Roads and Road Traffic (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1990/30 'Roads and Road Traffic (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1993/14 'Roads and Road Traffic (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1992/7 'Roads and Road Traffic (Amendment) Act, 1992': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1991/14 'Roads and Road Traffic (Amendment) Act, 1991': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')

## Notes

- No SEED stage this batch — batch-0155 processed all three surviving probe candidates in that tick, so no deferred probe queue carries forward.
- B-POL-ACT-1 title filter applied pre-write for probe-stage candidates: any slot whose AKN-page title contained an amendment-style token was rejected without raw or record file.
- Next tick: continue the primary-statute sweep with the next rotation of probe keywords — arbitration (primary 2000), copyright (Cap. 406 parent), refugees-control (2017 parent), higher-education (pre-2013), electoral (pre-2016), zambia-revenue-authority (1993 parent), and lands-tribunal. Patents Cap. 400 and Copyright Cap. 406 parents remain unresolved by all prior probes and may be pre-independence ordinances not carried on ZambiaLII — consider alphabetical listing browse as fallback if this tick's direct 'patents act' probe does not surface them.

