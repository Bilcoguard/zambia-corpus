# Batch 0134 Report

**Date:** 2026-04-18T08:18:28Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Fetches (script):** 12
**Integrity:** PASS

## Strategy

Target selection used ZambiaLII's alphabetical `/legislation/?page=1..10` index as ground truth, filtered against HEAD's (year, num) pairs. This replaces the speculative AKN URL guessing and misleading `/legislation/?q=` usage seen in earlier batches. The batch 0133 next-tick list items (Optometry, Open University, Organs of Government Dispersal, Protected Disclosures, Private Security Services, Personal Property Security Interests, National Water Supply and Sanitation) were all confirmed NOT to appear in ZambiaLII's Act listing under those titles and have been logged to gaps.md for human verification against alternative sources (parliament.gov.zm, Gazette).

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-2016-042-zambia-institute-for-tourism-and-hospitality-studies-act-2016` | Zambia Institute for Tourism and Hospitality Studies Act, 2016 | Act No. 42 of 2016 | 37 | PDF |
| 2 | `act-zm-2007-010-biosafety-act-2007` | Biosafety Act, 2007 | Act No. 10 of 2007 | 61 | HTML/AKN |
| 3 | `act-zm-1973-021-births-and-deaths-registration-act-1973` | Births and Deaths Registration Act, 1973 | Act No. 21 of 1973 | 22 | HTML/AKN |
| 4 | `act-zm-1968-046-building-societies-act-1968` | Building Societies Act, 1968 | Act No. 46 of 1968 | 139 | HTML/AKN |
| 5 | `act-zm-2016-043-compensation-fund-act-2016` | Compensation Fund Act, 2016 | Act No. 43 of 2016 | 37 | PDF |
| 6 | `act-zm-2004-013-computer-misuse-and-crimes-act-2004` | Computer Misuse and Crimes Act, 2004 | Act No. 13 of 2004 | 11 | PDF |
| 7 | `act-zm-1987-019-copperbelt-university-act-1987` | Copperbelt University Act, 1987 | Act No. 19 of 1987 | 43 | PDF |
| 8 | `act-zm-1967-058-council-of-law-reporting-act-1967` | Council of Law Reporting Act, 1967 | Act No. 58 of 1967 | 11 | HTML/AKN |

**Total sections:** 361

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS (fixed from first-run bug: process_act now returns explicit raw_path rather than inferring from source_url, which ZambiaLII rewrites to a media.zambialii.org CDN path)
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-refs in this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Notes

- The 2016/42 Tourism & Hospitality Studies Act was inherited from an aborted first run of this script; the PDF/HTML raw were already on disk and were rewritten by this run (same bytes, same hash).
- 7 targets from batch 0133's next-tick list proved to be phantom targets (no ZambiaLII Act with those titles); they have been logged to gaps.md under batch 0134.
- Pagination-based discovery (pages 1–10 of /legislation/) surfaced 188 non-Appropriation Acts absent from HEAD, providing a large queue for subsequent batches.

