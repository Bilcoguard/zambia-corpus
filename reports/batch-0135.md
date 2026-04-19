# Batch 0135 Report

**Date:** 2026-04-18T08:38:03Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Fetches (script):** 10
**Integrity:** PASS

## Strategy

Same alphabetical-listing-first strategy as batch 0134. A fresh discovery step at the start of this tick scraped ZambiaLII `/legislation/?page=1..6` and filtered against HEAD's (year, num) pairs. From the 71 absent pairs surfaced, we selected the next 8 substantive Acts alphabetically after batch 0134's last target (Council of Law Reporting Act, 1967), skipping the annual Appropriation Act and Excess Expenditure Appropriation (YYYY) Act clusters (low legal content, better handled as a single dedicated batch later) and deferring the Constitution of Zambia Act, 1996 (1996/17) for a dedicated batch (it edits the Constitution itself and warrants careful individual review).

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1985-012-cold-storage-board-of-zambia-dissolution-act-1985` | Cold Storage Board of Zambia (Dissolution) Act, 1985 | Act No. 12 of 1985 | 5 | PDF |
| 2 | `act-zm-1964-046-combined-cadet-force-act-1964` | Combined Cadet Force Act, 1964 | Act No. 46 of 1964 | 11 | HTML/AKN |
| 3 | `act-zm-1966-031-commercial-travellers-special-provisions-act-1966` | Commercial Travellers (Special Provisions) Act, 1966 | Act No. 31 of 1966 | 6 | HTML/AKN |
| 4 | `act-zm-1969-029-companies-certificates-validation-act-1969` | Companies (Certificates Validation) Act, 1969 | Act No. 29 of 1969 | 3 | HTML/AKN |
| 5 | `act-zm-1992-032-constitutional-offices-emoluments-act-1992` | Constitutional Offices (Emoluments) Act, 1992 | Act No. 32 of 1992 | 2 | PDF |
| 6 | `act-zm-1993-041-constitutional-offices-emoluments-act-1993` | Constitutional Offices (Emoluments) Act, 1993 | Act No. 41 of 1993 | 2 | HTML/AKN |
| 7 | `act-zm-1967-042-dangerous-drugs-act-1967` | Dangerous Drugs Act, 1967 | Act No. 42 of 1967 | 23 | HTML/AKN |
| 8 | `act-zm-1966-040-decimal-currency-system-arrangements-act-1966` | Decimal Currency System (Arrangements) Act, 1966 | Act No. 40 of 1966 | 17 | HTML/AKN |

**Total sections:** 69

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-refs in this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Notes

- Batch 0135 discovery (pages 1–6 of /legislation/) surfaced 71 (year, num) pairs absent from HEAD at start of tick. The 8 targets here are the next alphabetical substantive Acts; the remaining 63 absent pairs (dominated by Appropriation / Excess Expenditure Appropriation annual Acts plus a handful of substantive items further down the alphabet) remain queued for subsequent batches.
- Deferred for dedicated batches: Constitution of Zambia Act, 1996 (1996/17), and the full Appropriation / Excess Expenditure Appropriation series.

