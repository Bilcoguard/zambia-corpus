# Batch 0159 Report

**Date:** 2026-04-22T11:09:01Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 1
**Repeal-chain links applied:** 0
**Fetches (script):** 9
**Integrity:** PASS

## Strategy

Probe-only pass. No seed candidates this batch — all of the batch-0158 next-tick primary-parent targets are probed, not seeded, since prior probe rounds failed to surface them by keyword alone. Stage 2 probes the ZambiaLII search API with eight fresh rotation queries: hire purchase, stamp duty, juveniles, patents, road traffic, immigration, bills of exchange, extradition. Hits surviving HEAD + title filters fill slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment` (plus OCR variants `amendrnent` and `amendement`), `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections. No unconditional repeal-chain links are pre-declared for this batch.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-1971-018-tokyo-convention-act-1971` | Tokyo Convention Act, 1971 | Act No. 18 of 1971 | 6 | HTML/AKN | probe |

**Total sections:** 6

## Repeal-chain links

No repeal-chain links applied this batch — the pre-declared unconditional link list was empty.

## Seed summary

- Seed candidates queued: 0
- Seed candidates committed: 0
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 8 ('hire purchase', 'stamp duty', 'juveniles', 'patents', 'road traffic', 'immigration', 'bills of exchange', 'extradition')
- Candidates discovered (novel): 19
- Candidates surviving HEAD + title filters: 1
- Candidates processed this batch: 1

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- 1999/12 'Environment Protection and Pollution Control (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'hire purchase')
- 1994/17 'Stamp Duty (Repeal) Act, 1994': pre-fetch reject — title contains 'repeal' (via query 'stamp duty')
- 1992/8 'Stamp Duty (Amendment) Act, 1992': pre-fetch reject — title contains 'amendment' (via query 'stamp duty')
- 1990/32 'Stamp Duty (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'stamp duty')
- 1984/3 'Stamp Duty (Amendment) Act, 1984': pre-fetch reject — title contains 'amendment' (via query 'stamp duty')
- 2011/3 'Juveniles (Amendment) Act, 2011': pre-fetch reject — title contains 'amendment' (via query 'juveniles')
- 1987/26 'Patents (Amendment) Act, 1987': pre-fetch reject — title contains 'amendment' (via query 'patents')
- 1980/18 'Patents (Amendment) Act, 1980': pre-fetch reject — title contains 'amendment' (via query 'patents')
- 1997/4 'Roads and Road Traffic (Amendment) Act, 1997': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1996/4 'Roads and Road Traffic (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1989/29 'Roads and Road Traffic (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1994/12 'Roads and Road Traffic (Amendment) Act, 1994': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 2006/6 'Road Traffic (Amendment) Act, 2006': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1992/7 'Roads and Road Traffic (Amendment) Act, 1992': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 2008/4 'Road Traffic (Amendment)Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1985/4 'Roads and Road Traffic (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1997/25 'Immigration and Deportation (Amendment) Bill, I997': pre-fetch reject — title contains 'amendment' (via query 'immigration')
- 2012/16 'Appropriation Act, 2012': pre-fetch reject — title contains 'appropriation' (via query 'immigration')

## Notes

- No SEED stage this batch — batch 0158 next-tick explicitly flagged these as probe rotations rather than direct year/number seeds, since prior probe rounds had not surfaced them.
- B-POL-ACT-1 title filter retains the OCR variants `amendrnent` and `amendement` added in batch 0157.
- No unconditional repeal-chain link applied this batch — the pre-declared list is empty.
- Next tick: continue primary-statute sweep with a fresh rotation of probe keywords — sale of goods, juveniles (Cap. 53) if still not surfaced, hire purchase if still not surfaced, stamp duty if still not surfaced, Patents Cap. 400 via alphabetical listing fallback if keyword probes continue to return only amendment variants, Copyright Cap. 406 parent, and any new candidates surfaced but deferred by MAX_RECORDS=8 this batch.

