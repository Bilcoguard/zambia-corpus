# Batch 0139 Report

**Date:** 2026-04-19T05:05:49Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 4
**Fetches (script):** 8
**Integrity:** PASS

## Strategy

Continuation of the alphabetical-listing-first strategy from batches 0134–0138. I-block tail targets picked up after "Industrial and Labour Relations Act, 1993" (_work/batch_0135_discovery.json entries 66–70): Income Tax (Special Provisions) 1982/3, Income Tax (Special Provisions) 1988/16, Industrial Hemp 2021/34, Industrial Relations 1990/36. Fetched via AKN URL pattern with PDF fallback when HTML returned fewer than 2 parsed sections.

Batch size is 4 (below MAX_RECORDS=8) because _work/batch_0135_discovery.json terminated at the end of the I-block. After the four target acts, a single discovery probe of `/legislation/?page=7` was performed to seed batch 0140+ with J-block targets (0 candidates, saved to `_work/batch_0139_discovery.json`).

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1982-003-income-tax-special-provisions-act-1982` | Income Tax (Special Provisions) Act, 1982 | Act No. 3 of 1982 | 5 | PDF |
| 2 | `act-zm-1988-016-income-tax-special-provisions-act-1988` | Income Tax (Special Provisions) Act, 1988 | Act No. 16 of 1988 | 47 | PDF |
| 3 | `act-zm-2021-034-industrial-hemp-act-2021` | Industrial Hemp Act, 2021 | Act No. 34 of 2021 | 26 | HTML/AKN |
| 4 | `act-zm-1990-036-industrial-relations-act-1990` | Industrial Relations Act, 1990 | Act No. 36 of 1990 | 170 | PDF |

**Total sections:** 248

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-refs in this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Notes

- Discovery probe `/legislation/?page=7` returned 0 fresh (year,num) AKN candidates (filtered: already in HEAD, Appropriation / Supplementary Appropriation rows excluded). Candidates written to `_work/batch_0139_discovery.json` for batch 0140+.
- Next tick: consume the J/K/L block from `_work/batch_0139_discovery.json`. If the J-block is sparse, probe `/legislation/?page=8` next.
- Deferred for dedicated batches: Constitution of Zambia Act, 1996 (1996/17); the full Appropriation / Excess Expenditure Appropriation series.

