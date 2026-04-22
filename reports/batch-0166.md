# Batch 0166 Report

**Date:** 2026-04-22T16:06:04Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 5
**Repeal-chain links applied:** 0
**Fetches (script):** 13
**Integrity:** PASS

## Strategy

Probe-only pass. Stage 2 probes the ZambiaLII search API with eight fresh narrower rotation queries per the batch-0165 next-tick plan: tourism, fertiliser, tobacco, dairy, radiation, public roads, local government, chieftaincy. Hits surviving HEAD + title filters fill slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment` (plus OCR variants `amendrnent` and `amendement`), `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections. No SEED candidates this batch; no unconditional repeal-chain links are pre-declared.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-1958-011-plant-pests-and-diseases-act-1958` | Plant Pests and Diseases Act, 1958 | Act No. 11 of 1958 | 32 | HTML/AKN | probe |
| 2 | `act-zm-1929-016-dairies-and-dairy-produce-act-1929` | Dairies and Dairy Produce Act, 1929 | Act No. 16 of 1929 | 3 | HTML/AKN | probe |
| 3 | `act-zm-1964-003-dairy-produce-board-establishment-act-1964` | Dairy Produce Board (Establishment) Act, 1964 | Act No. 3 of 1964 | 13 | HTML/AKN | probe |
| 4 | `act-zm-1972-019-ionising-radiation-act-1972` | Ionising Radiation Act, 1972 | Act No. 19 of 1972 | 26 | HTML/AKN | probe |
| 5 | `act-zm-1990-012-environmental-protection-and-pollution-control-act-1990` | Environmental Protection and Pollution Control Act, 1990 | Act No. 12 of 1990 | 103 | HTML/AKN | probe |

**Total sections:** 177

## Repeal-chain links

No repeal-chain links applied this batch — the pre-declared unconditional link list was empty.

## Seed summary

- Seed candidates queued: 0
- Seed candidates committed: 0
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 8 ('tourism', 'fertiliser', 'tobacco', 'dairy', 'radiation', 'public roads', 'local government', 'chieftaincy')
- Candidates discovered (novel): 18
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

- 1985/22 'Tourism (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'tourism')
- 1989/25 'Customs and Excise (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'fertiliser')
- 1981/5 'Customs and Excise (Amendment) Act, 1981': pre-fetch reject — title contains 'amendment' (via query 'fertiliser')
- 1982/4 'Customs and Excise (Amendment) Act, 1982': pre-fetch reject — title contains 'amendment' (via query 'tobacco')
- 2021/45 'Customs and Excise (Amendment) Act, 2021': pre-fetch reject — title contains 'amendment' (via query 'tobacco')
- 1981/10 'Income Tax (Amendment) Act, 1981': pre-fetch reject — title contains 'amendment' (via query 'dairy')
- 2006/10 'Public Roads (Amendment) Act, 2006': pre-fetch reject — title contains 'amendment' (via query 'public roads')
- 1993/30 'Local Government (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 2014/12 'Local Government (Amendment) Act, 2014': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 2004/9 'Local Government (Amendment) Act, 2004': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 1995/30 'Local Government (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 1993/31 'Local Government Elections (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 1996/18 'Constitution of Zambia (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'chieftaincy')

## Notes

- No SEED stage this batch — no seed candidates were deferred into 0166 from batch 0165.
- B-POL-ACT-1 title filter retains the OCR variants `amendrnent` and `amendement` added in batch 0157.
- No unconditional repeal-chain link applied this batch — the pre-declared list is empty.
- Next tick: if probe yield this batch is <= 2 new primary parents, shift to the alphabetical `/akn/zm/act/` listing traversal fallback for unresolved Cap. parents (Juveniles Cap. 53, Patents Cap. 400, Copyright Cap. 406, Hire Purchase, Stamp Duty, Sale of Goods, Bills of Exchange); otherwise continue the primary-statute sweep with another fresh rotation of narrower probe keywords — fisheries, forests, wildlife, customary law, traditional leadership, chiefs, marriage, succession.

