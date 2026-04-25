# Phase 4 Batch 0228 — Drain L-alphabet residuals from 0227

## Summary

- **Mode**: drain_L_alphabet_residuals_from_0227 (no fresh discovery probe — used 0227's cached L candidates)
- **Attempted**: 7
- **OK**: 7
- **Fail**: 0
- **Skip**: 0
- **Yield**: 100% (fifth consecutive 100%-yield batch — 0223/0224/0226/0227/0228; 0225 was 73% due to scanned-image cohort)
- **Sub-phases**: sis_local_government (+6), sis_governance (+1, FIRST sis_governance record after first-time entry in 0226 paired with the Laws of Zambia Revised Edition Act specified-date notice)

## Picks (7)

| # | yr/num | Title | sub_phase | parent_act | pages | chars |
|---|--------|-------|-----------|------------|-------|-------|
| 0 | 2020/34 | Laws of Zambia (Revised Edition) Act (Specified Date) Notice, 2020 | sis_governance | Laws of Zambia (Revised Edition) Act | 2 | 845 |
| 1 | 2022/71 | Local Government (Appointment of Local Government Administrator) (Kafue Town Council) Order, 2022 | sis_local_government | Local Government Act | 2 | 1379 |
| 2 | 2020/95 | Local Government (Appointment of Local Government Administrator) (Kalumbila Town Council) Order, 2020 | sis_local_government | Local Government Act | 2 | 1465 |
| 3 | 2020/67 | Local Government (Appointment of Local Government Administrator) (Kitwe City Council) Order, 2020 | sis_local_government | Local Government Act | 2 | 1455 |
| 4 | 2020/66 | Local Government (Appointment of Local Government Administrator) (Lusaka City Council) Order, 2020 | sis_local_government | Local Government Act | 2 | 1537 |
| 5 | 2019/77 | Chembe Town Council (Sugar Cane Levy) By-laws, 2019 | sis_local_government | Local Government Act | 2 | 2174 |
| 6 | 2019/47 | Local Government (Fire Services) Order, 2019 | sis_local_government | Local Government Act | 4 | 2016 |

## Discovery cost

- 0 fresh alphabet probes (drained 0227's cached L candidates; the 7 picks above are exactly the L-residuals that 0227 reserved for the next tick)
- 1 robots.txt re-verify (sha256 prefix fce67b697ee4ef44 — unchanged from batches 0193-0227; Crawl-delay 5 honoured at 6s margin; Disallow on /akn/zm/judgment/ + /akn/zm/officialGazette/ enforced)

## Per-record fetches

- 7 picks × 2 fetches (HTML + PDF) = 14 fresh fetches
- 0 reused entries from prior cache

## Integrity (CHECK1a/1b/2/3/4/5/6)

- CHECK1a (batch unique IDs): **PASS** — 7 unique
- CHECK1b (corpus presence on disk): **PASS** — 7/7 records/sis/{year}/*.json present
- CHECK2 (amended_by refs resolve): **PASS** — 0 refs (vacuously)
- CHECK3 (repealed_by refs resolve): **PASS** — 0 refs (vacuously)
- CHECK4 (source_hash sha256 vs raw): **PASS** — 7/7 PDF sha256 verified against raw/zambialii/si/(2019,2020,2022)/*.pdf
- CHECK5 (required fields): **PASS** — 10 required fields × 7 records all present
- CHECK6 (cited_authorities resolve): **PASS** — 0 refs

## Notes

- **Surprise yield (100% on appointment orders)**: the worker.log close-out for batch 0227 anticipated the 4 LG-Administrator appointment orders (Kafue/Kalumbila/Kitwe/Lusaka) might be short scanned-image declarations with low text-extract yield (1-3 of 7 expected). All 4 in fact text-extract cleanly (1379-1537 chars across 2 pages each — short formal proclamations but native text, not scanned). 0% scanned-image rate matches batches 0226/0227.
- **First sis_governance after 0226**: 2020/34 Laws of Zambia (Revised Edition) Act Specified Date Notice — second-ever sis_governance record; the parent-Act (Laws of Zambia Revised Edition Act) is itself a meta-act about codification, useful as a reference anchor for downstream consolidated-text citation work.
- **L-cohort fully drained**: with 0227 (4 L picks) and 0228 (7 L picks), all 11 candidates surfaced by the L-alphabet probe in 0227 are now ingested.

## Cumulative state after this batch

- SI records: 418 (+7 over batch 0227's 411)
- Judgments: 25 (paused per robots Disallow on /akn/zm/judgment/)
- Today fetches: 480/2000 (24.0%, all on zambialii.org under robots-declared 5s crawl-delay using 6s margin)

## Next-tick options

(a) Fresh probes from U/X/Y/Z unprobed alphabets (high-novelty risk; may surface few candidates).
(b) Re-probe earlier alphabet (e.g. M, A, D, E) for candidates not picked previously (lower discovery cost; bigger backlog).
(c) Rotate to acts_in_force priority_order item 1 (requires Acts-listing endpoint discovery — separate path from SI ingest).
(d) OCR backlog from batches 0225/0226 (5 items: 2017/068, 2018/011, 2022/004, 2022/007, 2022/012).
(e) Reconcile pre-existing flat-vs-year-subdir duplicate paths under records/acts/ (34 entries) and 488+ untracked records/sis + records/acts files on disk (queued backlog).

Robots.txt re-verify at start of next tick remains required.
