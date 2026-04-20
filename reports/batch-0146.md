# Batch 0146 Report

**Date:** 2026-04-20T12:37:42Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Fetches (script):** 12
**Integrity:** PASS

## Strategy

Continuation of the batch 0145 next-tick plan: Narcotic Drugs and Psychotropic Substances Act (1993/37), Bank of Zambia Act (1996/43 parent), Anti-Corruption Commission Act (1996/42), Citizens Economic Empowerment Act (2006/9), Probate / Administration parent (1960/41 AKN slot — turned out to be the High Court Act), Rent Act parent (1972/10), Food and Drugs Act (1972/22), Arbitration 1995/23 AKN slot (turned out to be the Agricultural Credits Act, 1995), plus buffer candidates from Children / Bank / Mines searches. Candidate (year, num) pairs were obtained by parsing the `results_html` fragment of the ZambiaLII search API (`/search/api/documents/?search=<q>&nature=Act`) for 14 hint queries; each hit was cross-referenced against HEAD by (year, num) tuple via `git ls-tree -r HEAD records/acts/`. Twelve non-HEAD candidates were queued; the processor fetches each AKN page, applies a title-token filter (rejects `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`) BEFORE any raw or record file is written, and stops at MAX_RECORDS=8 accepted primary statutes. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections.

Note on slug/hint drift: three AKN slots returned titles different from the hint slug (1960/41 is the High Court Act, not Probate; 1995/23 is Agricultural Credits Act, not Arbitration; 1995/5 is the Affiliation and Maintenance of Children Act). The `slug` in each final record ID is derived from the AKN-page title (not the hint), so the corpus IDs are accurate. Hint slugs are diagnostic only.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1993-037-narcotic-drugs-and-psychotropic-substances-act-1993` | Narcotic Drugs and Psychotropic Substances Act, 1993 | Act No. 37 of 1993 | 60 | HTML/AKN |
| 2 | `act-zm-1996-043-bank-of-zambia-act-1996` | Bank of Zambia Act, 1996 | Act No. 43 of 1996 | 63 | HTML/AKN |
| 3 | `act-zm-1996-042-anti-corruption-commission-act-1996` | Anti-Corruption Commission Act, 1996 | Act No. 42 of 1996 | 68 | HTML/AKN |
| 4 | `act-zm-1960-041-high-court-act` | High Court Act | Act No. 41 of 1960 | 48 | HTML/AKN |
| 5 | `act-zm-1972-022-food-and-drugs-act-1972` | Food and Drugs Act, 1972 | Act No. 22 of 1972 | 34 | HTML/AKN |
| 6 | `act-zm-1972-010-rent-act-1972` | Rent Act, 1972 | Act No. 10 of 1972 | 32 | HTML/AKN |
| 7 | `act-zm-1995-023-agricultural-credits-act-1995` | Agricultural Credits Act, 1995 | Act No. 23 of 1995 | 15 | HTML/AKN |
| 8 | `act-zm-1995-005-affiliation-and-maintenance-of-children-act-1995` | Affiliation and Maintenance of Children Act, 1995 | Act No. 5 of 1995 | 62 | PDF |

**Total sections:** 382

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-refs in this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- citizens-economic-empowerment-2006 (Act 9/2006): no parseable sections in HTML or PDF
- children-candidate-1989 (Act 14/1989): title rejected (contains 'amendment'): 'Employment of Women, Young Persons and Children (Amendment) Act, 1989'
- bank-of-zambia-2001 (2001/11): batch cap reached (MAX_RECORDS=8) — deferred
- mines-minerals-2011 (2011/28): batch cap reached (MAX_RECORDS=8) — deferred

## Notes

- B-POL-ACT-1 title filter applied pre-write: rejected `Employment of Women, Young Persons and Children (Amendment) Act, 1989` at (1989/14) — no raw or record file written for that target.
- citizens-economic-empowerment-2006 (2006/9) returned an empty AKN page and an unparseable PDF (no sections extracted by the regex pattern). Logged as a gap; next tick should try the PDF with a stronger parser or search the alphabetical listing for the CEE Act's correct AKN slot.
- Primary statute wins this tick: Narcotic Drugs and Psychotropic Substances Act (1993) and Bank of Zambia Act (1996) are foundational modern statutes; Anti-Corruption Commission Act (1996/42) is the predecessor of the current ACC Act 2012/3 (already in HEAD) — repeal-chain linking deferred to a dedicated pass.
- Next tick: probe for Citizens Economic Empowerment Act correct AKN slot (alphabetical listing); Arbitration Act 2000 principal (search 'Arbitration 2000'); Probate and Administration of Estates principal (search 'Probate and Administration'); Environmental Management Act 2011 principal (if the 2011/12 entry in HEAD is the amendment, find parent); additional Mines and Minerals / Road Traffic / Customs amendments that escape the filter.

