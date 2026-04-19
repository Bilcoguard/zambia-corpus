# Batch 0141 Report

**Date:** 2026-04-19T08:23:23Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Fetches (script):** 11
**Integrity:** PASS

## Strategy

Continuation of the ZambiaLII AKN-URL ingestion from batches 0134–0140. Targets drawn from the `_work/batch_0140_discovery.json` queue (J/K/L/M candidates) plus adjacent N-R primary statutes resolved via the ZambiaLII search API (`/search/api/documents/?search=<q>&nature=Act`). Eight targets selected (all primary statutes, no amendment acts, no appropriation acts): Matrimonial Causes 2007/20, Lands Acquisition 1970/2, Forests 1973/39, Zambia Institute of Marketing 2003/14, Public Roads 2002/12, Public Service Pensions 1996/35, Electoral 2006/12, Roads and Road Traffic 1958/37. Fetched via AKN URL pattern with PDF fallback when HTML returned fewer than 2 parsed sections.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-2007-020-matrimonial-causes-act-2007` | Matrimonial Causes Act, 2007 | Act No. 20 of 2007 | 105 | HTML/AKN |
| 2 | `act-zm-1970-002-lands-acquisition-act-1970` | Lands Acquisition Act, 1970 | Act No. 2 of 1970 | 30 | HTML/AKN |
| 3 | `act-zm-1973-039-forests-act-1973` | Forests Act, 1973 | Act No. 39 of 1973 | 71 | HTML/AKN |
| 4 | `act-zm-2003-014-zambia-institute-of-marketing-act-2003` | Zambia Institute of Marketing Act, 2003 | Act No. 14 of 2003 | 75 | PDF |
| 5 | `act-zm-2002-012-public-roads-act-2002` | Public Roads Act, 2002 | Act No. 12 of 2002 | 121 | PDF |
| 6 | `act-zm-1996-035-public-service-pensions-act-1996` | Public Service Pensions Act, 1996 | Act No. 35 of 1996 | 84 | HTML/AKN |
| 7 | `act-zm-2006-012-electoral-act-2006` | Electoral Act, 2006 | Act No. 12 of 2006 | 194 | PDF |
| 8 | `act-zm-1958-037-roads-and-road-traffic-act-1958` | Roads and Road Traffic Act, 1958 | Act No. 37 of 1958 | 286 | HTML/AKN |

**Total sections:** 966

## Integrity checks
- CHECK 1 (batch unique IDs): PASS
- CHECK 2 (no HEAD collision): PASS
- CHECK 3 (source_hash matches raw on disk): PASS
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-refs in this batch
- CHECK 5 (required fields present): PASS

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Notes

- Next tick: continue N-R block — Public Roads (2002/12 done this batch), Public Service Pensions (done), then tackle Roads and Road Traffic repeal/amendment chain, National Parks and Wildlife (2015 recast), National Health Insurance 2018, National Council for Construction 2003 predecessor vs 2020 recast, Public Finance Management Act 2018 (Act 1/2018), Public Procurement Act 2020 (Act 8/2020).
- Roads and Road Traffic Act 1958 is superseded by the Road Traffic Act 2002 (2002/11, not yet in HEAD) — historical primary included for completeness; cross-ref links deferred to a future amendment-linking batch.

