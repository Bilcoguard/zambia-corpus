# Batch 0162 Report

**Date:** 2026-04-22T12:36:19Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Repeal-chain links applied:** 0
**Fetches (script):** 17
**Integrity:** PASS

## Strategy

Probe-only pass. No seed candidates this batch — all targets are surfaced via keyword rotation per the batch-0161 next-tick plan. Stage 2 probes the ZambiaLII search API with eight fresh rotation queries: forestry, veterinary, animal health, education, legal practitioners, public health, food and drugs, land survey. Hits surviving HEAD + title filters fill slots up to MAX_RECORDS=8. Title filter rejects any slot whose AKN-page title contains `amendment` (plus OCR variants `amendrnent` and `amendement`), `appropriation`, `repeal`, `supplementary`, `validation`, or `transitional` — applied pre-write, so rejected slots produce no raw or record file. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections. No unconditional repeal-chain links are pre-declared for this batch.

## Committed records

| # | ID | Title | Citation | Sections | Source | Origin |
|---|----|-------|----------|----------|--------|--------|
| 1 | `act-zm-1920-020-prevention-of-cruelty-to-animals-act-1920` | Prevention of Cruelty to Animals Act, 1920 | Act No. 20 of 1920 | 14 | HTML/AKN | probe |
| 2 | `act-zm-1930-015-cattle-cleansing-act-1930` | Cattle Cleansing Act, 1930 | Act No. 15 of 1930 | 18 | HTML/AKN | probe |
| 3 | `act-zm-1959-028-cattle-slaughter-control-act-1959` | Cattle Slaughter (Control) Act, 1959 | Act No. 28 of 1959 | 7 | HTML/AKN | probe |
| 4 | `act-zm-1961-008-stock-diseases-act-1961` | Stock Diseases Act, 1961 | Act No. 8 of 1961 | 15 | HTML/AKN | probe |
| 5 | `act-zm-1964-012-veterinary-surgeons-act-1964` | Veterinary Surgeons Act, 1964 | Act No. 12 of 1964 | 18 | HTML/AKN | probe |
| 6 | `act-zm-1951-038-african-education-act-1951` | African Education Act, 1951 | Act No. 38 of 1951 | 5 | HTML/AKN | probe |
| 7 | `act-zm-1966-028-education-act-1966` | Education Act, 1966 | Act No. 28 of 1966 | 42 | HTML/AKN | probe |
| 8 | `act-zm-1998-013-technical-education-vocational-and-entrepreneurship-training-act-1998` | Technical Education, Vocational and Entrepreneurship Training Act, 1998 | Act No. 13 of 1998 | 76 | PDF | probe |

**Total sections:** 195

## Repeal-chain links

No repeal-chain links applied this batch — the pre-declared unconditional link list was empty.

## Seed summary

- Seed candidates queued: 0
- Seed candidates committed: 0
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 8 ('forestry', 'veterinary', 'animal health', 'education', 'legal practitioners', 'public health', 'food and drugs', 'land survey')
- Candidates discovered (novel): 17
- Candidates surviving HEAD + title filters: 9
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

- 1994/20 'Standards Act, 1994': batch cap reached (MAX_RECORDS=8) — deferred
- 1985/16 'Appropriation Act, 1985': pre-fetch reject — title contains 'appropriation' (via query 'forestry')
- 1999/12 'Environment Protection and Pollution Control (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'animal health')
- 1993/2 'Education Levy (Repeal) Act, 1993': pre-fetch reject — title contains 'repeal' (via query 'education')
- 1981/11 'Education Levy (Amendment) Act, 1981': pre-fetch reject — title contains 'amendment' (via query 'education')
- 1986/6 'Education Levy (Amendment) Act, 1986': pre-fetch reject — title contains 'amendment' (via query 'education')
- 2006/14 'Legal Practitioners (Amendment) Act, 2006': pre-fetch reject — title contains 'amendment' (via query 'legal practitioners')
- 1981/21 'Legal Practitioners (Amendment) Act, 1981': pre-fetch reject — title contains 'amendment' (via query 'legal practitioners')
- 2021/40 'Land Survey (Amendment) Act, 2021': pre-fetch reject — title contains 'amendment' (via query 'land survey')

## Notes

- No SEED stage this batch — batch 0161 next-tick flagged these as probe rotations rather than direct year/number seeds, since narrower prior probes had not surfaced them.
- B-POL-ACT-1 title filter retains the OCR variants `amendrnent` and `amendement` added in batch 0157.
- No unconditional repeal-chain link applied this batch — the pre-declared list is empty.
- Next tick: if probe yield this batch was <= 2 new primary parents, shift to the alphabetical `/akn/zm/act/` listing traversal fallback for unresolved Cap. parents; otherwise continue the primary-statute sweep with another fresh rotation of narrower probe keywords — water resources, wildlife, national parks, insurance, pensions, securities, telecommunications, energy regulation.

