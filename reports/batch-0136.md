# Batch 0136 Report

**Date:** 2026-04-19T03:39:16Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Fetches (script):** 9
**Integrity:** PASS

## Strategy

Continuation of the alphabetical-listing-first strategy from batches 0134–0135. A fresh discovery step at the start of this tick scraped ZambiaLII `/legislation/?page=1..6` and filtered against a union of HEAD (555 pairs) and working-tree record pairs (706 pairs total). That surfaced 63 absent (year, num) pairs. We skip the annual Appropriation / Excess Expenditure Appropriation clusters (28 substantive pairs remain after this filter) and defer the Constitution of Zambia Act, 1996 (1996/17) for a dedicated batch. The 8 targets here are the next substantive Acts alphabetically after batch 0135's last target (Decimal Currency System (Arrangements) Act, 1966).

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1968-058-deeds-of-arrangement-act-1968` | Deeds of Arrangement Act, 1968 | Act No. 58 of 1968 | 29 | HTML/AKN |
| 2 | `act-zm-1972-035-development-bank-of-zambia-act-1972` | Development Bank of Zambia Act, 1972 | Act No. 35 of 1972 | 27 | HTML/AKN |
| 3 | `act-zm-1967-013-disposal-of-uncollected-goods-act-1967` | Disposal of Uncollected Goods Act, 1967 | Act No. 13 of 1967 | 6 | HTML/AKN |
| 4 | `act-zm-1982-016-district-councils-estimates-act-1982` | District Councils Estimates Act, 1982 | Act No. 16 of 1982 | 102 | PDF |
| 5 | `act-zm-1966-029-employment-special-provisions-act-1966` | Employment (Special Provisions) Act, 1966 | Act No. 29 of 1966 | 6 | HTML/AKN |
| 6 | `act-zm-1996-003-entertainment-tax-repeal-act` | Entertainment Tax (Repeal) Act | Act No. 3 of 1996 | 2 | HTML/AKN |
| 7 | `act-zm-1982-011-equity-levy-act-1982` | Equity Levy Act, 1982 | Act No. 11 of 1982 | 10 | HTML/AKN |
| 8 | `act-zm-1996-008-estate-duty-repeal-act-1996` | Estate Duty (Repeal) Act, 1996 | Act No. 8 of 1996 | 2 | HTML/AKN |

**Total sections:** 184

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-refs in this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Notes

- Batch 0136 discovery surfaced 63 (year, num) pairs absent from HEAD+working-tree at start of tick. 28 pairs remain after filtering out Appropriation / Excess Expenditure Appropriation clusters and the deferred 1996/17 Constitution Act. After this batch's 8, ~20 substantive Acts from pages 1–6 of /legislation/ remain queued for subsequent batches (Evidence Act 1967/8, Fees and Fines Act 1994/13, Finance (Control and Management) Act 1969/24, Flying Doctor Service Act 1967/37, Gaming Machines (Prohibition) Act 1974/2, General Loans (International Bank) Act 1966/35, General Loans (Mediobanca) Act 1967/19, Gwembe District Special Fund (Dissolution) Act 1968/5, Higher Authority for Power (Special Provisions) Act 1970/41, Home Guard Act 1971/32, Honours and Decorations (Prevention of Abuses) Act 1967/5, Hotels Act 1987/27, plus a tail of items further down the alphabet).
- Deferred for dedicated batches: Constitution of Zambia Act, 1996 (1996/17); the full Appropriation / Excess Expenditure Appropriation series.

