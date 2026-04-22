# Batch 0157 Report

**Date:** 2026-04-22T10:52:26Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 5
**Repeal-chain links applied:** 0
**Fetches (script):** 13
**Integrity:** PASS

## Strategy

Probe-only pass — batch-0156 left no deferred SEED queue behind. Stage 2 probes the ZambiaLII search API with eight queries targeting fresh primary-parent targets flagged unresolved by the batch-0156 wrap-up: arbitration (primary 2000), copyright (Cap. 406 parent), higher education (pre-2013), electoral (pre-2016), Zambia Revenue Authority (1993 parent), lands tribunal, mental disorders (synonym for mental-health parent), and refugees (2017 repealer of the 1970 Refugees (Control) Act ingested batch 0155). Hits surviving HEAD + title filters fill slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment` (plus OCR variants `amendrnent` and `amendement`), `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-1996-024-electoral-commission-act-1996` | Electoral Commission Act, 1996 | Act No. 24 of 1996 | 19 | HTML/AKN | probe |
| 2 | `act-zm-1993-028-zambia-revenue-authority-act-1993` | Zambia Revenue Authority Act, 1993 | Act No. 28 of 1993 | 27 | HTML/AKN | probe |
| 3 | `act-zm-2001-014-prohibition-and-prevention-of-money-laundering-act-2001` | Prohibition and Prevention of Money Laundering Act, 2001 | Act No. 14 of 2001 | 32 | HTML/AKN | probe |
| 4 | `act-zm-1965-032-contempt-of-court-miscellaneous-provisions-act-1965` | Contempt of Court (Miscellaneous Provisions) Act, 1965 | Act No. 32 of 1965 | 5 | HTML/AKN | probe |
| 5 | `act-zm-1967-001-suicide-act-1967` | Suicide Act, 1967 | Act No. 1 of 1967 | 9 | HTML/AKN | probe |

**Total sections:** 92

## Repeal-chain links

No new repeal-chain links applied this batch — the conditional Refugees 1970 -> 2017 link was not triggered (no 2017 Refugees Act record was committed this batch).

## Seed summary

- Seed candidates queued: 0
- Seed candidates committed: 0
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 8 ('arbitration', 'copyright', 'higher education', 'electoral', 'zambia revenue authority', 'lands tribunal', 'mental disorders', 'refugees')
- Candidates discovered (novel): 16
- Candidates surviving HEAD + title filters: 5
- Candidates processed this batch: 5

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- 2008/8 'Industrial and Labour Relations (Amendment) Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'arbitration')
- 1999/4 'Customs and Excise (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'copyright')
- 2020/27 'Zambia Institute of Marketing (Amendment) Act, 2020': pre-fetch reject — title contains 'amendment' (via query 'higher education')
- 1996/23 'Electoral (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'electoral')
- 1986/19 'Electoral (Amendment) Act, 1986': pre-fetch reject — title contains 'amendment' (via query 'electoral')
- 1995/7 'Electoral (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'electoral')
- 1988/20 'Electoral (Amendment) Act, 1988': pre-fetch reject — title contains 'amendment' (via query 'electoral')
- 2001/4 'Electoral (Amendment) Act, 2001': pre-fetch reject — title contains 'amendment' (via query 'electoral')
- 2014/10 'Zambia Revenue Authority (Amendment) Act, 2014': pre-fetch reject — title contains 'amendment' (via query 'zambia revenue authority')
- 1996/32 'Zambia Revenue Authority (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'zambia revenue authority')
- 2010/42 'Housing (Statutory andImprovement Areas) (Amendment) Act, 2010': pre-fetch reject — title contains 'amendment' (via query 'lands tribunal')

## Notes

- No SEED stage this batch — batch-0156 was a probe-only pass that left no deferred probe queue behind.
- B-POL-ACT-1 title filter extended this batch to include the OCR variants `amendrnent` (rn->m digraph, per batch 0156 diagnostic) and `amendement` (stray 'e'). This should prevent the 2000/18 'Banking and Financial Services (Amendrnent) Act' style slip-through observed in batch 0156.
- Conditional repeal-chain link: if the 2017 Refugees Act surfaces as a probe hit and is committed, a repeal link from `act-zm-1970-040-refugees-control-act-1970` to the 2017 record is applied after Stage 2. This reflects the 2017 Refugees Act s.64 repeal-and-savings clause.
- Next tick: continue primary-statute sweep with the next rotation of probe keywords — extradition, treason, immigration (pre-1965 parent, Cap. 123 if not already in HEAD), arms-and-ammunition, aviation, industrial-relations (pre-1993 parent), money-laundering (pre-2001 parent), and Patents/Copyright Cap. parents if they have not surfaced by alphabetical-listing browse. Patents Cap. 400 and any pre-independence ordinances may require a direct /akn alphabetical listing fallback rather than keyword probes.

