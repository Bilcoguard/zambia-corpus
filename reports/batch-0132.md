# Batch 0132 Report

**Date:** 2026-04-18T07:12:00Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 8
**Fetches:** 10 (8 HTML + 2 PDF fallback)
**Integrity:** PASS (all 5 checks)

## Committed records (8)

All targets drawn from batch 0131's next-tick notes — N-block + adjacent Acts
located via the ZambiaLII `/legislation/?q=` search endpoint. One target from
batch 0131's list ("National Tourism Board Act") was dropped after discovery
returned only the Zambia Tourism Board Act 2007 (already in HEAD as
`act-zm-2007-024-zambia-tourism-board`). National Water Supply and Sanitation
yielded no ZambiaLII hits for any query tried and is deferred to `gaps.md`.
Added two adjacent targets: Zambia National Broadcasting Corporation Act 1987
(original, predating the 2002/2025 records in HEAD) and National Savings and
Credit Bank (Dissolution) Act 1991.

| # | Title | Citation | Year | Sections | Source |
|---|-------|----------|------|----------|--------|
| 1 | National Housing Authority Act | Act No. 16 of 1971 | 1971 | 74 | ZambiaLII HTML |
| 2 | National Institute of Public Administration Act | Act No. 15 of 1998 | 1998 | 51 | ZambiaLII PDF (HTML empty) |
| 3 | National Parks and Wildlife Act | Act No. 10 of 1991 | 1991 | 185 | ZambiaLII HTML |
| 4 | National Pension Scheme Act | Act No. 40 of 1996 | 1996 | 68 | ZambiaLII HTML |
| 5 | National Registration Act | Act No. 19 of 1964 | 1964 | 14 | ZambiaLII HTML |
| 6 | Science and Technology Act | Act No. 26 of 1997 | 1997 | 63 | ZambiaLII PDF (HTML empty) |
| 7 | Zambia National Broadcasting Corporation Act | Act No. 16 of 1987 | 1987 | 37 | ZambiaLII HTML |
| 8 | National Savings and Credit Bank of Zambia (Dissolution) Act | Act No. 7 of 1991 | 1991 | 8 | ZambiaLII HTML |

**Total sections:** 500

## Integrity checks (batch scope)

- CHECK 1 (batch unique IDs): PASS — 8 distinct IDs
- CHECK 2 (no HEAD collision): PASS — none of the 8 IDs exist in HEAD tree
- CHECK 3 (source_hash matches raw on disk): PASS for all 8 records
- CHECK 4 (amended_by / repealed_by / cited_authorities reference resolution): PASS — no cross-references in this batch
- CHECK 5 (required fields present): PASS

## Record paths

- `records/acts/1971/act-zm-1971-016-national-housing-authority-act-1971.json`
- `records/acts/1998/act-zm-1998-015-national-institute-of-public-administration-act-1998.json`
- `records/acts/1991/act-zm-1991-010-national-parks-and-wildlife-act-1991.json`
- `records/acts/1996/act-zm-1996-040-national-pension-scheme-act-1996.json`
- `records/acts/1964/act-zm-1964-019-national-registration-act-1964.json`
- `records/acts/1997/act-zm-1997-026-science-and-technology-act-1997.json`
- `records/acts/1987/act-zm-1987-016-zambia-national-broadcasting-corporation-act-1987.json`
- `records/acts/1991/act-zm-1991-007-national-savings-and-credit-bank-dissolution-act-1991.json`

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.{html|pdf}`. B2 sync deferred
to host (rclone not available in sandbox).

## Fetch accounting

- Discovery fetches (URL hunt for targets): 11 search pages — used only for
  URL discovery, not ingested.
- 8 AKN HTML fetches (one per target)
- 2 PDF fetches (targets 2 & 6 where HTML returned zero AKN sections)
- Total: 10 content fetches this batch → today 10/2000 (well under cap).

## Notes / next tick

- The `/legislation/?q=<query>` endpoint remains a reliable route for
  title-based discovery. Server-rendered results include real `/akn/zm/act/...`
  links, unlike the JS-rendered `/search/?q=`.
- National Water Supply and Sanitation Act (usually cited as Act No. 28 of
  1997) did not appear in `/legislation/?q=` under any of the queries tried
  ("Water Supply", "Water and Sanitation", "Zambian Water"). Append to
  `gaps.md` with a note to try the ZambiaLII subject-browse index or a Gazette
  search next tick.
- National Tourism Board Act was identified as a phantom target — the
  canonical tourism Act on ZambiaLII is Zambia Tourism Board Act 2007 (Act No.
  24 of 2007), already in HEAD. Drop from future target lists.
- 1987 Zambia National Broadcasting Corporation Act is the original Act
  predating the 2002, 2010, 2017, and 2025 amendments already in the corpus.
  A future tick should link `repealed_by`/`amended_by` edges between these
  records per schema.
- 1991 National Savings and Credit Bank (Dissolution) Act formally dissolves
  the institution — no predecessor "Establishment" Act is currently in HEAD.
  A future tick may want to chase the predecessor for completeness.
- Next batch suggestions (continuing through N- and O-block): Non-Governmental
  Organisations Act 2009 (Act No. 16 of 2009), National Prosecution Authority
  Act 2010 (already in HEAD — skip), Occupational Health and Safety Act 2010
  (Act No. 36 of 2010), Optometry Act 2007, Open University Act 2009,
  Ombudsman Act (Public Protector), Organs of Government (Dispersal) Act,
  Oaths and Affirmations Act.

## Dirty-tree advisory (carry-forward)

The working tree continues to carry ~219 orphan untracked record JSONs and
stale "deleted" index entries from pre-0130 ticks (see batch 0131 report
§ "Dirty-tree advisory"). This batch again used the `GIT_INDEX_FILE=<tmp>`
workaround, seeding from HEAD and adding only this batch's outputs plus the
three updated log files. Host-side cleanup still recommended per batch 0131
diagnostic in `worker.log`.
