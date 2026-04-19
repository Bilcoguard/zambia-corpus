# Batch 0137 Report

**Date:** 2026-04-19T04:05:11Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Fetches (script):** 8
**Integrity:** PASS

## Strategy

Continuation of the alphabetical-listing-first strategy from batches 0134–0136. Targets drawn directly from batch 0136's next-tick list: the next 8 substantive Acts alphabetically after "Estate Duty (Repeal) Act, 1996" in the ZambiaLII /legislation/ ordering — Evidence (1967/8), Fees and Fines (1994/13), Finance (Control and Management) (1969/24), Flying Doctor Service (1967/37), Gaming Machines (Prohibition) (1974/2), General Loans (International Bank) (1966/35), General Loans (Mediobanca) (1967/19), Gwembe District Special Fund (Dissolution) (1968/5). Fetched via AKN URL pattern with PDF fallback when HTML returned fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1967-008-evidence-act-1973` | Evidence Act, 1973 | Act No. 8 of 1967 | 9 | HTML/AKN |
| 2 | `act-zm-1994-013-fees-and-fines-act-1994` | Fees and Fines Act, 1994 | Act No. 13 of 1994 | 9 | HTML/AKN |
| 3 | `act-zm-1969-024-finance-control-and-management-act-1969` | Finance (Control and Management) Act, 1969 | Act No. 24 of 1969 | 18 | HTML/AKN |
| 4 | `act-zm-1967-037-flying-doctor-service-act-1967` | Flying Doctor Service Act, 1967 | Act No. 37 of 1967 | 13 | HTML/AKN |
| 5 | `act-zm-1974-002-gaming-machines-prohibition-act-1974` | Gaming Machines (Prohibition) Act, 1974 | Act No. 2 of 1974 | 4 | HTML/AKN |
| 6 | `act-zm-1966-035-general-loans-international-bank-act-1966` | General Loans (International Bank) Act, 1966 | Act No. 35 of 1966 | 7 | HTML/AKN |
| 7 | `act-zm-1967-019-general-loans-mediobanca-act-1967` | General Loans (Mediobanca) Act, 1967 | Act No. 19 of 1967 | 6 | HTML/AKN |
| 8 | `act-zm-1968-005-gwembe-district-special-fund-dissolution-act-1968` | Gwembe District Special Fund (Dissolution) Act, 1968 | Act No. 5 of 1968 | 6 | HTML/AKN |

**Total sections:** 72

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-refs in this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Notes

- After this batch, remaining queued from batch 0136's discovery tail: Higher Authority for Power (Special Provisions) Act 1970/41, Home Guard Act 1971/32, Honours and Decorations (Prevention of Abuses) Act 1967/5, Hotels Act 1987/27, plus the items further down the alphabet (I–L blocks).
- Deferred for dedicated batches: Constitution of Zambia Act, 1996 (1996/17); the full Appropriation / Excess Expenditure Appropriation series.

