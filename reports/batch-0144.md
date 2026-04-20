# Batch 0144 Report

**Date:** 2026-04-20T12:03:35Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 7
**Fetches (script):** 11
**Integrity:** PASS

## Strategy

Continuation of the batch 0143 next-tick plan: resolve the Public Order parent, Matrimonial Causes pre-2007 originals, Postal Services Act 2009 (and its 1994 predecessor), Probate and Administration of Estates pre-1989 parent, Registered Designs parent(s), and pre-Employment-Code Industrial/Labour Relations originals. Candidate (year, num) pairs were obtained by parsing the `results_html` fragment of the ZambiaLII search API (`/search/api/documents/?search=<q>&nature=Act`) for the six hint queries; each hit was cross-referenced against HEAD by (year, num) tuple via `git ls-tree -r HEAD records/acts/`. Ten non-HEAD candidates were queued; the processor fetches each AKN page, applies a title-token filter (rejects `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`) BEFORE any raw or record file is written, and stops at MAX_RECORDS=8 accepted primary statutes. PDF fallback is invoked only when the HTML returns fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-2009-022-postal-services-act-2009` | Postal Services Act, 2009 | Act No. 22 of 2009 | 155 | PDF |
| 2 | `act-zm-1955-038-public-order-act-1955` | Public Order Act, 1955 | Act No. 38 of 1955 | 15 | HTML/AKN |
| 3 | `act-zm-1960-039-maintenance-orders-act-1960` | Maintenance Orders Act, 1960 | Act No. 39 of 1960 | 19 | HTML/AKN |
| 4 | `act-zm-1994-024-postal-services-act-1994` | Postal Services Act, 1994 | Act No. 24 of 1994 | 48 | HTML/AKN |
| 5 | `act-zm-1951-002-consular-conventions-act-1951` | Consular Conventions Act, 1951 | Act No. 2 of 1951 | 4 | HTML/AKN |
| 6 | `act-zm-1958-012-registered-designs-act-1958` | Registered Designs Act, 1958 | Act No. 12 of 1958 | 61 | HTML/AKN |
| 7 | `act-zm-1989-006-wills-and-administration-of-testate-estates-act-1989` | Wills and Administration of Testate Estates Act, 1989 | Act No. 6 of 1989 | 70 | HTML/AKN |

**Total sections:** 372

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-refs in this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

- registered-designs-1987 (Act 25/1987): title rejected (contains 'amendment'): 'Registered Designs (Amendment) Act, 1987'
- industrial-relations-act-1983 (Act 13/1983): title rejected (contains 'amendment'): 'Industrial Relations (Amendment) Act, 1983'
- candidate-2008-008 (Act 8/2008): title rejected (contains 'amendment'): 'Industrial and Labour Relations (Amendment) Act, 2008'

## Notes

- B-POL-ACT-1 title filter applied pre-write: any candidate whose AKN-page title contained `amendment`, `appropriation`, `repeal`, `supplementary`, or `validation` was rejected without producing a raw or record file. The filter runs on the cleaned HTML title (whitespace-normalised, leading 'ACT' prefix stripped).
- Next tick: continue the primary-statute sweep — candidates still outstanding include the Electoral Commission parent Act, the National Pension Scheme Authority base Act, and the Road Traffic Act parent; plus any remaining pre-independence Cap-base statutes on Marriage, Chiefs, and Probate that survived this batch's title filter.

