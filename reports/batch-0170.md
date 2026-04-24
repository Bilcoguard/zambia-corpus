# Batch 0170 Report

**Date:** 2026-04-24T05:39:03Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 1
**Repeal-chain links applied:** 0
**Fetches (script):** 3
**Integrity:** PASS

## Strategy

PIVOT per batch-0169 next-tick plan. Two successive 0-yield ticks on the ZambiaLII `search/api/documents/` probe (batches 0168, 0169) triggered a pivot to the parliament.gov.zm `acts-of-parliament` listing for candidate discovery. The 12 cached listing pages (fetched 2026-04-10, already on disk under `raw/discovery/parliament-zm/`) were re-parsed in-sandbox and cross-referenced against HEAD. Five novel primary-Act candidates surfaced, all from 2021 (filling HEAD gaps 2021/34, 35, 37, 38, 41). Each candidate was ingested from ZambiaLII's AKN endpoint (`https://zambialii.org/akn/zm/act/<year>/<number>`) with the pre-write B-POL-ACT-1 title filter (+OCR variants) and PDF fallback when HTML returned fewer than 2 parsed sections. No new fetches against parliament.gov.zm this tick (discovery-only re-parse).

## Seed candidates

| # | Year/Num | Title hint | Source | Outcome |
|---|----------|------------|--------|---------|
| 1 | 2021/41 | electronic-government-act-2021 | parliament.gov.zm listing | committed (act-zm-2021-041-electronic-government-act-2021) |
| 2 | 2021/38 | insurance-act-2021 | parliament.gov.zm listing | gapped |
| 3 | 2021/37 | zambia-correctional-service-act-2021 | parliament.gov.zm listing | gapped |
| 4 | 2021/35 | narcotic-drugs-and-psychotropic-substances-act-2021 | parliament.gov.zm listing | gapped |
| 5 | 2021/34 | industrial-hemp-act-2021 | parliament.gov.zm listing | gapped |

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-2021-041-electronic-government-act-2021` | Electronic Government Act, 2021 | Act No. 41 of 2021 | 58 | PDF |

**Total sections:** 58

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by resolution): PASS (no cross-refs this batch)
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- 2021/38 'insurance-act-2021': HTML fetch failed: status=404 len=17595
- 2021/37 'zambia-correctional-service-act-2021': pre-queue reject — already in HEAD (parliament.gov.zm /node/9008 — primary Act, absent from HEAD)
- 2021/35 'narcotic-drugs-and-psychotropic-substances-act-2021': pre-queue reject — already in HEAD (parliament.gov.zm /node/9005 — primary Act, absent from HEAD)
- 2021/34 'industrial-hemp-act-2021': pre-queue reject — already in HEAD (parliament.gov.zm /node/9004 — primary Act, absent from HEAD)

## Notes

- Parliament.gov.zm pivot established a stable discovery channel after ZambiaLII probe exhaustion in 0168-0169.
- B-POL-ACT-1 title filter retained.
- No unconditional repeal-chain link applied this batch.
- Next tick: continue the parliament.gov.zm re-parse sweep — the page parse yielded only 5 novel primary parents across 12 pages, suggesting HEAD already covers most post-1994 primary Acts indexed there. If this tick commits all 5, next tick probes the 2021/22, 2021/36, 2021/39, 2021/40 slots and cross-year remaining gaps (1990s/early-2000s); otherwise continues the deferred parliament candidates. Remain on the parliament.gov.zm rail until it exhausts, then restart ZambiaLII probe rotation with new keyword families.

