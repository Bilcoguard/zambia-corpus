# Batch 0149 Report

**Date:** 2026-04-20T18:40:29Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 6
**Repeal-chain links applied:** 2
**Fetches (script):** 13
**Integrity:** PASS

## Strategy

Continuation of the batch 0148 next-tick plan. Targets primary parents for Trade Marks / Patents / National Parks and Wildlife / Judges (Emoluments) / Chartered Institute of Public Relations / Local Government Elections / Zambia Tourism Board / Citizens Economic Empowerment. Candidate (year, num) pairs were surfaced by probing the ZambiaLII search API (`/search/api/documents/?search=<q>&nature=Act`) for 8 hint queries at batch-0149-probe; each hit was cross-referenced against HEAD by (year, num) tuple via `git ls-tree -r HEAD records/acts/`. Free slots were queued in priority order (primary parents first); the processor fetches each AKN page, applies a title-token filter (rejects `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`) BEFORE any raw or record file is written, and stops at MAX_RECORDS=8 accepted primary statutes. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1957-014-trade-marks-act-1957` | Trade Marks Act, 1957 | Act No. 14 of 1957 | 91 | HTML/AKN |
| 2 | `act-zm-1971-027-international-game-park-and-wildlife-act-1971` | International Game Park and Wildlife Act, 1971 | Act No. 27 of 1971 | 9 | HTML/AKN |
| 3 | `act-zm-1976-022-supreme-court-and-high-court-number-of-judges-act-1976` | Supreme Court and High Court (Number of Judges) Act, 1976 | Act No. 22 of 1976 | 3 | HTML/AKN |
| 4 | `act-zm-2003-015-zambia-institute-of-purchasing-and-supply-act-2003` | Zambia Institute of Purchasing and Supply Act, 2003 | Act No. 15 of 2003 | 72 | PDF |
| 5 | `act-zm-1979-029-tourism-act-1979` | Tourism Act, 1979 | Act No. 29 of 1979 | 31 | HTML/AKN |
| 6 | `act-zm-1988-021-supreme-court-and-high-court-number-of-judges-act-1988` | Supreme Court and High Court (Number of Judges) Act, 1988 | Act No. 21 of 1988 | 4 | PDF |

**Total sections:** 210

## Repeal-chain links

| # | Source record | Previous `repealed_by` | New `repealed_by` | Note |
|---|----|----|----|----|
| 1 | `records/acts/1994/act-zm-1994-026-companies-act-1994.json` | `None` | `act-zm-2017-010-companies` | Companies Act 1994 repealed by Companies Act 2017 (No. 10 of 2017) |
| 2 | `records/acts/1993/act-zm-1993-039-investment-act-1993.json` | `None` | `act-zm-2006-011-zambia-development-agency` | Investment Act 1993 repealed by Zambia Development Agency Act 2006 (No. 11 of 2006) |

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — all new repealed_by targets verified in HEAD before write
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- citizens-economic-empowerment-2006 (Act 9/2006): no parseable sections in HTML or PDF
- local-government-elections-2004 (Act 9/2004): title rejected (contains 'amendment'): 'Local Government (Amendment) Act, 2004'
- patents-1987 (Act 26/1987): title rejected (contains 'amendment'): 'Patents (Amendment) Act, 1987'
- zambia-tourism-board-1985 (Act 22/1985): title rejected (contains 'amendment'): 'Tourism (Amendment) Act, 1985'

## Notes

- B-POL-ACT-1 title filter applied pre-write: any candidate whose AKN-page title contained `amendment`, `appropriation`, `repeal`, `supplementary`, or `validation` was rejected without producing a raw or record file.
- Next tick: continue the primary-statute sweep — any deferred candidates from this tick, plus National Parks and Wildlife Act 2015/14 (already in HEAD per search hit — verify link chain), and additional Cap-era parents surfaced by further probes (Probate and Administration of Estates, Rent Cap, Sale of Goods, Employers and Workers). Repeal-chain targets to investigate next: Trade Marks 1957/14 -> Trade Marks Act 2023/11 (if 2023 is a successor, else amended_by); Patents 1987/26 relationship to Patents Act 2016/40 (already in HEAD).

