# Batch 0145 Report

**Date:** 2026-04-20T12:12:50Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 7
**Fetches (script):** 11
**Integrity:** PASS

## Strategy

Continuation of the batch 0144 next-tick plan: Lands Act parent (1995), Juveniles Act parent, Defence Act parent, Banking and Financial Services Act parent (pre-2017), Securities Act parent, Public Finance Management Act, plus additional National Parks and Wildlife / Banking / Juveniles candidates. Candidate (year, num) pairs were obtained by parsing the `results_html` fragment of the ZambiaLII search API (`/search/api/documents/?search=<q>&nature=Act`) for eight hint queries; each hit was cross-referenced against HEAD by (year, num) tuple via `git ls-tree -r HEAD records/acts/`. Ten non-HEAD candidates were queued; the processor fetches each AKN page, applies a title-token filter (rejects `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`) BEFORE any raw or record file is written, and stops at MAX_RECORDS=8 accepted primary statutes. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1995-029-lands-act` | Lands Act | Act No. 29 of 1995 | 32 | HTML/AKN |
| 2 | `act-zm-1994-021-banking-and-financial-services-act-1994` | Banking and Financial Services Act, 1994 | Act No. 21 of 1994 | 160 | HTML/AKN |
| 3 | `act-zm-1993-038-securities-act-1993` | Securities Act, 1993 | Act No. 38 of 1993 | 92 | HTML/AKN |
| 4 | `act-zm-1964-045-defence-act-1964` | Defence Act, 1964 | Act No. 45 of 1964 | 214 | HTML/AKN |
| 5 | `act-zm-1956-005-adoption-act-1956` | Adoption Act, 1956 | Act No. 5 of 1956 | 38 | HTML/AKN |
| 6 | `act-zm-2021-037-zambia-correctional-service-act-2021` | Zambia Correctional Service Act, 2021 | Act No. 37 of 2021 | 123 | HTML/AKN |
| 7 | `act-zm-1960-059-land-survey-act-1960` | Land Survey Act, 1960 | Act No. 59 of 1960 | 42 | HTML/AKN |

**Total sections:** 701

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-refs in this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- banking-2000-018 (Act 18/2000): no parseable sections in HTML or PDF
- banking-2005-025 (Act 25/2005): title rejected (contains 'amendment'): 'Banking and Financial Services (Amendment) Act, 2005'
- lands-1985-015 (Act 15/1985): title rejected (contains 'amendment'): 'Land (Conversion of Titles) (Amendment) (No. 2) Act, 1985'

## Notes

- B-POL-ACT-1 title filter applied pre-write: any candidate whose AKN-page title contained `amendment`, `appropriation`, `repeal`, `supplementary`, or `validation` was rejected without producing a raw or record file.
- Next tick: continue the primary-statute sweep — remaining candidates include the Securities Act 1993 / Securities Act 2016 (if distinct), Defence Act subsidiary/parent variants, and the pre-1964 Juveniles / Protection of Children Act parent; plus probes for National Health Insurance, Tourism and Hospitality 2015, Solid Waste 2018, Environmental Management Act 2011, Narcotic Drugs 1993, Bank of Zambia 1996 parent.

