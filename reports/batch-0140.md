# Batch 0140 Report

**Date:** 2026-04-19T06:35:40Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Fetches (script):** 10
**Integrity:** PASS

## Strategy

Continuation of the alphabetical-listing-first strategy from batches 0134–0139. Because the batch 0139 discovery probe of `/legislation/?page=7` returned 0 fresh AKN candidates (HTML structure changed), this batch used the ZambiaLII search API (`/search/api/documents/?search=<q>&nature=Act`) to find substantive primary statutes in the J/K/L/M families not yet in HEAD. Eight targets selected (all primary statutes, no amendment acts, no appropriation acts): Intestate Succession 1989/5, Judicature Administration 1994/42, Judicial (Code of Conduct) 1999/13, Prisons 1965/56, Transfer of Convicted Persons 1998/26, Marriage 1918/10, Markets 1937/21, Money-Lenders 1938/11. Fetched via AKN URL pattern with PDF fallback when HTML returned fewer than 2 parsed sections.

A discovery pass before the batch returned 32 additional J/K/L/M candidates, stashed in `_work/batch_0140_discovery.json` for future ticks.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1989-005-intestate-succession-act-1989` | Intestate Succession Act, 1989 | Act No. 5 of 1989 | 48 | HTML/AKN |
| 2 | `act-zm-1994-042-judicature-administration-act-1994` | Judicature Administration Act, 1994 | Act No. 42 of 1994 | 16 | HTML/AKN |
| 3 | `act-zm-1999-013-judicial-code-of-conduct-act-1999` | Judicial (Code of Conduct) Act, 1999 | Act No. 13 of 1999 | 11 | PDF |
| 4 | `act-zm-1965-056-prisons-act-1965` | Prisons Act, 1965 | Act No. 56 of 1965 | 147 | HTML/AKN |
| 5 | `act-zm-1998-026-transfer-of-convicted-persons-act-1998` | Transfer of Convicted Persons Act, 1998 | Act No. 26 of 1998 | 11 | PDF |
| 6 | `act-zm-1918-010-marriage-act-1918` | Marriage Act, 1918 | Act No. 10 of 1918 | 49 | HTML/AKN |
| 7 | `act-zm-1937-021-markets-act-1937` | Markets Act, 1937 | Act No. 21 of 1937 | 11 | HTML/AKN |
| 8 | `act-zm-1938-011-money-lenders-act-1938` | Money lenders Act, 1938 | Act No. 11 of 1938 | 22 | HTML/AKN |

**Total sections:** 315

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-refs in this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Notes

- Pre-batch discovery pass (J/K/L/M search families) produced 32 fresh (year,num) AKN candidates filtered against HEAD — saved to `_work/batch_0140_discovery.json`. 8 primary statutes selected for this batch; remaining candidates include amendment acts and adjacent substantive statutes (Transfer of Convicted Persons, Matrimonial Causes, Local Government, etc.) for batch 0141+.
- Next tick: consume the remaining J/K/L/M primary statutes from `_work/batch_0140_discovery.json` (excluding already-in-HEAD entries such as Cap. 189 Lands Acquisition), then move to the N–R block via search API.
- Deferred for dedicated batches: Constitution of Zambia Act, 1996 (1996/17); the full Appropriation / Excess Expenditure Appropriation series.

