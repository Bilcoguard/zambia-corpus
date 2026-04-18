# Batch 0131 Report

**Date:** 2026-04-18T08:56:00Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Fetches:** 10 (8 HTML + 2 PDF fallback)
**Integrity:** PASS (all checks)

## Committed records (8)

All targets drawn from batch 0130's next-tick notes — N-block Acts located via
the ZambiaLII `/legislation/?q=` search endpoint (HTML search results, not the
paged listing).

| # | Title | Citation | Year | Sections | Source |
|---|-------|----------|------|----------|--------|
| 1 | National Anthem Act | Act No. 40 of 1973 | 1973 | 4 | ZambiaLII HTML |
| 2 | National Archives Act | Act No. 44 of 1969 | 1969 | 21 | ZambiaLII HTML |
| 3 | National Arts Council of Zambia Act | Act No. 31 of 1994 | 1994 | 47 | ZambiaLII HTML |
| 4 | National Assembly Speaker's Retirement Benefits Act | Act No. 20 of 1997 | 1997 | 10 | ZambiaLII PDF (HTML empty) |
| 5 | National College for Management and Development Studies (Repeal) Act | Act No. 18 of 2005 | 2005 | 13 | ZambiaLII PDF (HTML empty) |
| 6 | National Council for Scientific Research Act | Act No. 55 of 1967 | 1967 | 22 | ZambiaLII HTML |
| 7 | National Food and Nutrition Commission Act | Act No. 41 of 1967 | 1967 | 12 | ZambiaLII HTML |
| 8 | National Health Services Act | Act No. 22 of 1995 | 1995 | 36 | ZambiaLII HTML |

**Total sections:** 165

## Integrity checks (batch scope)

- CHECK 1 (batch unique IDs): PASS — 8 distinct IDs
- CHECK 2 (no collision with HEAD): PASS — none of the 8 IDs exist in HEAD tree (689 records in HEAD)
- CHECK 3 (record schema + source_hash on disk): PASS for all 8 records
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — no cross-references in this batch

## Record paths

- `records/acts/1973/act-zm-1973-040-national-anthem-act-1973.json`
- `records/acts/1969/act-zm-1969-044-national-archives-act-1969.json`
- `records/acts/1994/act-zm-1994-031-national-arts-council-of-zambia-act-1994.json`
- `records/acts/1997/act-zm-1997-020-national-assembly-speakers-retirement-benefits-act-1997.json`
- `records/acts/2005/act-zm-2005-018-national-college-for-management-and-development-studies-repeal-act-2005.json`
- `records/acts/1967/act-zm-1967-055-national-council-for-scientific-research-act-1967.json`
- `records/acts/1967/act-zm-1967-041-national-food-and-nutrition-commission-act-1967.json`
- `records/acts/1995/act-zm-1995-022-national-health-services-act-1995.json`

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred to host (rclone not available in sandbox).

## Fetch accounting

- 1 listing discovery fetch prior to batch: `https://zambialii.org/legislation/?q=...` search (8 queries) — used only for URL discovery; content not ingested.
- 8 AKN HTML fetches (one per target)
- 2 PDF fetches (for targets 4 & 5 where HTML returned zero AKN sections)
- Total: 10 content fetches this batch.

## Notes / next tick

- The `/legislation/?q=<query>` endpoint is a reliable search route that returns real `/akn/zm/act/...` links in the HTML (unlike `/search/?q=` which appears to be JS-rendered). Use this endpoint for future title-based discovery.
- 2005 Act No. 18 is a repeal of the 1972 National College for Management and Development Studies Act (which is already in HEAD). A future tick should set the `repealed_by` field of the 1972 record to `act-zm-2005-018-national-college-for-management-and-development-studies-repeal-act-2005` and link back via `amended_by`/`repealed_by` per schema.
- Next batch suggestions (continuing N-block through Health Insurance, Mining, Pension, Prosecution, Registration, Scientific, Tourism sub-themes from the search listings): National Housing Authority Act, National Institute of Public Administration Act (original), National Parks and Wildlife Act, National Pension Scheme Act (original 1996), National Prosecution Authority Act (original), National Registration Act, National Science & Technology Act, National Tourism Board Act.

## Dirty-tree advisory

On entering this tick the working tree contained ~219 untracked records (mostly
under `records/acts/<year>/`) and 65 stale "deleted" index entries inherited from
prior ticks' use of the `GIT_INDEX_FILE` commit workaround. This batch used the
same temp-index workaround (`GIT_INDEX_FILE=/tmp/git_idx_b131_commit`), seeding
the index from HEAD and adding only this batch's new files and three updated
log files (worker.log, costs.log, provenance.log). The accumulated working-tree
cruft was NOT included in this commit — see `worker.log` for a full diagnostic
pointer.
