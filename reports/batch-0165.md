# Batch 0165 Report

**Date:** 2026-04-22T15:36:34Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Repeal-chain links applied:** 0
**Fetches (script):** 16
**Integrity:** PASS

## Strategy

Probe-only pass. Stage 2 probes the ZambiaLII search API with eight fresh narrower rotation queries per the batch-0164 next-tick plan: mines and minerals, environmental management, postal, railways, civil aviation, housing, prisons, correctional. Hits surviving HEAD + title filters fill slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment` (plus OCR variants `amendrnent` and `amendement`), `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections. No SEED candidates this batch; no unconditional repeal-chain links are pre-declared.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-1922-005-rhodesia-railways-act-1922` | Rhodesia Railways Act, 1922 | Act No. 5 of 1922 | 10 | HTML/AKN | probe |
| 2 | `act-zm-1922-007-mashona-railway-company-limited-act-1922` | Mashona Railway Company Limited Act, 1922 | Act No. 7 of 1922 | 10 | HTML/AKN | probe |
| 3 | `act-zm-1927-027-nkana-nchanga-branch-railway-act-1927` | Nkana-Nchanga Branch Railway Act, 1927 | Act No. 27 of 1927 | 8 | HTML/AKN | probe |
| 4 | `act-zm-1928-008-roan-antelope-branch-railway-act-1928` | Roan Antelope Branch Railway Act, 1928 | Act No. 8 of 1928 | 8 | HTML/AKN | probe |
| 5 | `act-zm-1931-022-railways-deviations-act-1931` | Railways (Deviations) Act, 1931 | Act No. 22 of 1931 | 10 | HTML/AKN | probe |
| 6 | `act-zm-1935-002-railways-transfer-of-statutory-powers-act-1935` | Railways Transfer of Statutory Powers Act, 1935 | Act No. 2 of 1935 | 3 | HTML/AKN | probe |
| 7 | `act-zm-1949-025-rhodesia-railways-act-1949` | Rhodesia Railways Act, 1949 | Act No. 25 of 1949 | 89 | HTML/AKN | probe |
| 8 | `act-zm-1971-011-zambia-educational-publishing-house-act-1971` | Zambia Educational Publishing House Act, 1971 | Act No. 11 of 1971 | 19 | HTML/AKN | probe |

**Total sections:** 157

## Repeal-chain links

No repeal-chain links applied this batch — the pre-declared unconditional link list was empty.

## Seed summary

- Seed candidates queued: 0
- Seed candidates committed: 0
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 8 ('mines and minerals', 'environmental management', 'postal', 'railways', 'civil aviation', 'housing', 'prisons', 'correctional')
- Candidates discovered (novel): 20
- Candidates surviving HEAD + title filters: 8
- Candidates processed this batch: 8

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- 2020/25 'Mines and Minerals Development (Amendment) Act, 2020': pre-fetch reject — title contains 'amendment' (via query 'mines and minerals')
- 2002/5 'Mines and Minerals (Amendment) Act, 2002': pre-fetch reject — title contains 'amendment' (via query 'mines and minerals')
- 1998/8 'Mines and Minerals (Amendment) Act, 1998': pre-fetch reject — title contains 'amendment' (via query 'mines and minerals')
- 1996/41 'Mines and Minerals (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'mines and minerals')
- 2011/28 'Mines and Minerals Development (Amendment) Act, 2011': pre-fetch reject — title contains 'amendment' (via query 'mines and minerals')
- 1985/18 'Mines and Minerals (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'mines and minerals')
- 2013/10 'Environmental Management (Amendment) Act, 2013': pre-fetch reject — title contains 'amendment' (via query 'environmental management')
- 2010/42 'Housing (Statutory andImprovement Areas) (Amendment) Act, 2010': pre-fetch reject — title contains 'amendment' (via query 'housing')
- 1998/5 'Zambia Publishing House (Amendment) Act, 1998': pre-fetch reject — title contains 'amendment' (via query 'housing')
- 2004/16 'Prisons (Amendment) Act, 2004': pre-fetch reject — title contains 'amendment' (via query 'prisons')
- 2000/14 'Prisons (Amendment) Act, 2000': pre-fetch reject — title contains 'amendment' (via query 'prisons')
- 1996/18 'Constitution of Zambia (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'prisons')

## Notes

- No SEED stage this batch — no seed candidates were deferred into 0165 from batch 0164.
- B-POL-ACT-1 title filter retains the OCR variants `amendrnent` and `amendement` added in batch 0157.
- No unconditional repeal-chain link applied this batch — the pre-declared list is empty.
- Next tick: if probe yield this batch is <= 2 new primary parents, shift to the alphabetical `/akn/zm/act/` listing traversal fallback for unresolved Cap. parents (Juveniles Cap. 53, Patents Cap. 400, Copyright Cap. 406, Hire Purchase, Stamp Duty, Sale of Goods, Bills of Exchange); otherwise continue the primary-statute sweep with another fresh rotation of narrower probe keywords — tourism, fertiliser, tobacco, dairy, radiation, public roads, local government, chieftaincy.

