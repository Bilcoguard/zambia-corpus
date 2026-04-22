# Batch 0158 Report

**Date:** 2026-04-22T11:01:10Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 4
**Repeal-chain links applied:** 1
**Fetches (script):** 12
**Integrity:** PASS

## Strategy

Probe-only pass. A pre-write HEAD audit (`git ls-tree HEAD records/acts/`) confirmed that the six primary-parent targets flagged by the batch-0157 next-tick plan (Arbitration 2000/19, Copyright 1994/44, Higher Education 2013/4, Lands Tribunal 2010/39, Mental Disorders 1949/21, Refugees 2017/1) are already in HEAD — so none of them enter this batch's seed queue. Stage 2 probes the ZambiaLII search API with eight fresh rotation queries: treason, immigration, arms and ammunition, aviation, industrial relations, money laundering, sale of goods, bills of exchange. Hits surviving HEAD + title filters fill slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment` (plus OCR variants `amendrnent` and `amendement`), `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections. Additionally, this batch applies one unconditional repeal-chain link (Refugees 1970 -> 2017) against a target already in HEAD.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-1933-023-criminal-procedure-code-1933` | Criminal Procedure Code, 1933 | Act No. 23 of 1933 | 428 | HTML/AKN | probe |
| 2 | `act-zm-1965-043-zambia-police-act-1965` | Zambia Police Act, 1965 | Act No. 43 of 1965 | 64 | HTML/AKN | probe |
| 3 | `act-zm-1971-035-zambia-national-service-act-1971` | Zambia National Service Act, 1971 | Act No. 35 of 1971 | 58 | HTML/AKN | probe |
| 4 | `act-zm-1989-018-safety-of-civil-aviation-act-1989` | Safety of Civil Aviation Act, 1989 | Act No. 18 of 1989 | 28 | HTML/AKN | probe |

**Total sections:** 578

## Repeal-chain links

| # | Source record | Previous `repealed_by` | New `repealed_by` | Note |
|---|----|----|----|----|
| 1 | `records/acts/1970/act-zm-1970-040-refugees-control-act-1970.json` | `None` | `act-zm-2017-001-refugees` | Refugees Act, 2017 s.64 repeals the Refugees (Control) Act, 1970 (Cap. 120). 2017 Act verified in HEAD by pre-write ls-tree audit; target id 'act-zm-2017-001-refugees' confirmed. |

## Seed summary

- Seed candidates queued: 0
- Seed candidates committed: 0
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 8 ('treason', 'immigration', 'arms and ammunition', 'aviation', 'industrial relations', 'money laundering', 'sale of goods', 'bills of exchange')
- Candidates discovered (novel): 13
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

- 1993/35 'Criminal Procedure Code (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'treason')
- 1997/25 'Immigration and Deportation (Amendment) Bill, I997': pre-fetch reject — title contains 'amendment' (via query 'immigration')
- 2012/16 'Appropriation Act, 2012': pre-fetch reject — title contains 'appropriation' (via query 'immigration')
- 1989/16 'Aviation (Amendment) Act) 1989': pre-fetch reject — title contains 'amendment' (via query 'aviation')
- 2007/17 'Penal Code (Amendment) Act, 2007': pre-fetch reject — title contains 'amendment' (via query 'aviation')
- 1983/13 'Industrial Relations (Amendment) Act, 1983': pre-fetch reject — title contains 'amendment' (via query 'industrial relations')
- 2008/8 'Industrial and Labour Relations (Amendment) Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'industrial relations')
- 1996/18 'Constitution of Zambia (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'industrial relations')
- 1990/32 'Stamp Duty (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'bills of exchange')

## Notes

- No SEED stage this batch — pre-write ls-tree audit confirmed all six batch-0157 next-tick primary-parent targets (Arbitration 2000/19, Copyright 1994/44, Higher Education 2013/4, Lands Tribunal 2010/39, Mental Disorders 1949/21, Refugees 2017/1) are already in HEAD.
- B-POL-ACT-1 title filter retains the OCR variants `amendrnent` and `amendement` added in batch 0157 to guard against the 2000/18 'Banking and Financial Services (Amendrnent) Act' style slip-through observed in batch 0156.
- Unconditional repeal-chain link applied: `act-zm-1970-040-refugees-control-act-1970` -> `act-zm-2017-001-refugees`. The 2017 Refugees Act (Act No. 1 of 2017) at section 64 repeals the Refugees (Control) Act 1970 (Cap. 120); target verified in HEAD by pre-write ls-tree audit.
- Next tick: continue primary-statute sweep with a fresh rotation of probe keywords — extradition (already in HEAD 1968/47 — skip), treason, hire purchase, stamp duty, juveniles (Cap. 53), Patents Cap. 400, road traffic pre-2002, immigration pre-1965 (Cap. 123) if not already in HEAD, Zambia Institute of Purchasing and Supply siblings. Patents Cap. 400 and any pre-independence ordinances may require a direct /akn alphabetical-listing fallback rather than keyword probes.

