# Batch 0167 Report

**Date:** 2026-04-22T16:34:44Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 3
**Repeal-chain links applied:** 0
**Fetches (script):** 11
**Integrity:** PASS

## Strategy

Probe-only pass. Stage 2 probes the ZambiaLII search API with eight fresh narrower rotation queries per the batch-0166 next-tick plan: fisheries, forests, wildlife, customary law, traditional leadership, chiefs, marriage, succession. Hits surviving HEAD + title filters fill slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment` (plus OCR variants `amendrnent` and `amendement`), `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections. No SEED candidates this batch; no unconditional repeal-chain links are pre-declared.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-1965-067-chiefs-act-1965` | Chiefs Act, 1965 | Act No. 67 of 1965 | 15 | HTML/AKN | probe |
| 2 | `act-zm-1926-006-deceased-brothers-widows-marriage-act-1926` | Deceased Brother's Widow's Marriage Act, 1926 | Act No. 6 of 1926 | 6 | HTML/AKN | probe |
| 3 | `act-zm-1926-021-land-perpetual-succession-act-1926` | Land (Perpetual Succession) Act, 1926 | Act No. 21 of 1926 | 12 | HTML/AKN | probe |

**Total sections:** 33

## Repeal-chain links

No repeal-chain links applied this batch — the pre-declared unconditional link list was empty.

## Seed summary

- Seed candidates queued: 0
- Seed candidates committed: 0
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 8 ('fisheries', 'forests', 'wildlife', 'customary law', 'traditional leadership', 'chiefs', 'marriage', 'succession')
- Candidates discovered (novel): 7
- Candidates surviving HEAD + title filters: 3
- Candidates processed this batch: 3

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- 2007/22 'Fisheries Act (Amendment) Act, 2007': pre-fetch reject — title contains 'amendment' (via query 'fisheries')
- 1981/15 'Forest (Amendment) Act, 1981': pre-fetch reject — title contains 'amendment' (via query 'forests')
- 1982/33 'National Parks and Wildlife (Amendment) Act, 1982': pre-fetch reject — title contains 'amendment' (via query 'wildlife')
- 2020/26 'Appropriation Act, 2020': pre-fetch reject — title contains 'appropriation' (via query 'traditional leadership')

## Notes

- No SEED stage this batch — no seed candidates were deferred into 0167 from batch 0166.
- B-POL-ACT-1 title filter retains the OCR variants `amendrnent` and `amendement` added in batch 0157.
- No unconditional repeal-chain link applied this batch — the pre-declared list is empty.
- Next tick: if probe yield this batch is <= 2 new primary parents, shift to the alphabetical `/akn/zm/act/` listing traversal fallback for unresolved Cap. parents (Juveniles Cap. 53, Patents Cap. 400, Copyright Cap. 406, Hire Purchase, Stamp Duty, Sale of Goods, Bills of Exchange); otherwise continue the primary-statute sweep with another fresh rotation of narrower probe keywords — agriculture, cooperatives, electoral, elections, national assembly, parliament, public health, food safety.

