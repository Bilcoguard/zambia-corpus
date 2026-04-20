# Batch 0148 Report

**Date:** 2026-04-20T18:XX:XXZ (see worker.log for exact push time)
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 6
**Repeal-chain links committed:** 2
**Fetches (script):** 23 (10 search-API probes + 13 AKN page fetches)
**Integrity:** PASS

## Strategy

Continuation of the batch 0147 next-tick plan: pursue primary statutes at specific AKN slots flagged by prior tick notes — Valuation Surveyors 1976/34, National Parks and Wildlife 1971/27 and 1982/33, Judges (Emoluments) 1976/22 and 1988/21, Zambia Tourism Board 1979/29 and 1985/22, Chartered Institute of Public Relations 2003/15, Local Government Elections 2004/9, Town and Country Planning 1961/32 and 1974/30, and the Citizens Economic Empowerment Act 2006 correct slot. Candidate (year, num) pairs were obtained by parsing the `results_html` fragment of the ZambiaLII search API (`/search/api/documents/?search=<q>&nature=Act`) across 10 hint queries (trade marks, patents, town country planning, valuation surveyors, local government elections, judges emoluments, national parks wildlife, zambia tourism board, chartered institute public relations, citizens economic empowerment); each hit was cross-referenced against HEAD by (year, num) tuple via a filesystem index of `records/acts/**`. Twenty non-HEAD candidate slots were queued, ranked with known-target slots first. The processor fetches each AKN page, applies a pre-write title-token filter (rejects `amendment`, `appropriation`, `repeal`, `supplementary`, `validation`, `transitional`), and stops at MAX_RECORDS=6 accepted primary statutes. PDF fallback is armed for any candidate with fewer than 2 parsed sections from HTML (not exercised in this batch — every accepted candidate parsed cleanly from AKN HTML).

Additionally, two repeal-chain links were written to already-existing records per batch 0145/0146 next-tick notes:

- `act-zm-1965-056-prisons-act-1965.repealed_by = "act-zm-2021-037-zambia-correctional-service-act-2021"`
- `act-zm-1996-042-anti-corruption-commission-act-1996.repealed_by = "act-zm-2012-003-anti-corruption-act-2012"`

Both target IDs were verified as present in HEAD before the repealed_by field was set.

## Committed records

| # | ID | Title | Citation | Sections | Source |
|---|----|-------|----------|----------|--------|
| 1 | `act-zm-1976-034-valuation-surveyors-act-1976` | Valuation Surveyors Act, 1976 | Act No. 34 of 1976 | 14 | HTML/AKN |
| 2 | `act-zm-1961-032-town-and-country-planning-act-1961` | Town and Country Planning Act, 1961 | Act No. 32 of 1961 | 55 | HTML/AKN |
| 3 | `act-zm-1974-030-housing-statutory-and-improvement-areas-act-1974` | Housing (Statutory and Improvement Areas) Act, 1974 | Act No. 30 of 1974 | 48 | HTML/AKN |
| 4 | `act-zm-1997-012-rating-act-1997` | Rating Act, 1997 | Act No. 12 of 1997 | 42 | HTML/AKN |
| 5 | `act-zm-1994-026-companies-act-1994` | Companies Act, 1994 | Act No. 26 of 1994 | 413 | HTML/AKN |
| 6 | `act-zm-1993-039-investment-act-1993` | Investment Act, 1993 | Act No. 39 of 1993 | 55 | HTML/AKN |

**Total sections:** 627

## Repeal-chain updates

| Existing record | Updated field | New value |
|---|---|---|
| `act-zm-1965-056-prisons-act-1965` | `repealed_by` | `act-zm-2021-037-zambia-correctional-service-act-2021` |
| `act-zm-1996-042-anti-corruption-commission-act-1996` | `repealed_by` | `act-zm-2012-003-anti-corruption-act-2012` |

## Integrity checks

- CHECK 1 (batch unique IDs): PASS — 6 distinct IDs within the batch
- CHECK 2 (no HEAD collision): PASS — each new record written exactly once at `records/acts/<year>/<id>.json`; 31 pre-existing legacy duplicate IDs across the `records/acts/` root and the year subfolders were noted as WARN only (not introduced by this batch; candidates for a future consolidation pass)
- CHECK 3 (source_hash matches raw on disk): PASS — all 6 sha256 values recomputed from `raw/zambialii/<year>/<id>.html` match the stored `source_hash`
- CHECK 4 (amended_by / repealed_by reference resolution): PASS — the 2 repeal-chain `repealed_by` targets both resolve to JSON files in HEAD (`records/acts/2021/act-zm-2021-037-zambia-correctional-service-act-2021.json`, `records/acts/act-zm-2012-003-anti-corruption-act-2012.json`). No cross-references in new records this batch.
- CHECK 5 (required fields present): PASS — all 6 new records carry id, type, jurisdiction, title, citation, source_url, source_hash, fetched_at, parser_version, sections.

## Raw snapshots

All raw bytes saved to `raw/zambialii/<year>/<id>.html`. B2 sync deferred to host (rclone not available in sandbox). Raw files are gitignored per `.gitignore:8 raw/*` policy; the remote authoritative copy is Backblaze B2 via the pending `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4` on the host.

## Gaps / skipped targets

Seven candidate slots were title-rejected by the pre-write filter (no raw or record file written):

- 1982/33: 'National Parks and Wildlife (Amendment) Act, 1982'
- 2006/15: 'Judges (Conditions of Service) (Amendment) Act, 2006'
- 2004/8:  'Local Government Elections (Amendment) Act, 2004'
- 1999/9:  'Rating (Amendment) Act, 1999'
- 1997/21: 'Town and Country Planning (Amendment) Act, 1997'
- 1997/17: 'Local Government Elections (Amendment) Act, 1997'
- 1993/31: 'Local Government Elections (Amendment) Act, 1993'

Seven additional discovery-queue candidate slots (beyond the 13 fetched this tick) were not processed because MAX_RECORDS=6 was reached — logged in `_work/batch_0148_discovery.json`.

## Notes

- Hint/slug drift: Two known targets turned out to resolve to different AKN-page titles than the hint query anticipated. Slot 1974/30 returned the Housing (Statutory and Improvement Areas) Act, 1974 (primary statute, kept) rather than a Town and Country Planning variant. Slot 1994/26 (surfaced via the "investment" / "companies" queries) turned out to be the Companies Act, 1994 — a genuine primary statute (predecessor to the Companies Act, 2017 which is the Phase-2 pilot target). Record IDs are derived from the AKN-page title, so the corpus entries are accurate; hint slugs were diagnostic only.
- Primary statute wins this tick: Companies Act, 1994 (413 sections, pre-2017 parent — repealed_by link to `act-zm-2017-010-companies-act-2017` pending), Town and Country Planning Act, 1961 (55 sections, pre-1995 land-use parent), Rating Act, 1997 (42 sections), Investment Act, 1993 (55 sections, pre-ZDA 2006 parent), Housing (Statutory and Improvement Areas) Act, 1974 (48 sections), Valuation Surveyors Act, 1976 (14 sections).
- Repeal-chain links added this tick: Prisons Act 1965/56 → Zambia Correctional Service Act 2021/37 and Anti-Corruption Commission Act 1996/42 → Anti-Corruption Act 2012/3. A duplicate-id note: the 2012 Anti-Corruption Act exists in HEAD under two filenames (`act-zm-2012-003-the-anti-corruption-act-2012.json` and `act-zm-2012-003-anti-corruption-act-2012.json`, both at `records/acts/` root); the repealed_by link uses the cleaner form (`act-zm-2012-003-anti-corruption-act-2012`). A future consolidation batch should pick one canonical ID and remove the other.
- Next tick — primary-statute sweep candidates still pending:
  - Companies Act, 1994 → 2017 repeal-chain link (already both in HEAD, just needs `repealed_by` on 1994/26)
  - Investment Act, 1993 → Zambia Development Agency Act 2006 repeal-chain link (check if ZDA is in HEAD)
  - Trade Marks Act parent (probe by year ranges 1956–1960)
  - Patents Act parent (probe by year ranges 1955–1960)
  - National Parks and Wildlife Act 1971/27 principal (not surfaced by this tick's search — probe directly)
  - Zambia Tourism Board Act 1979/29 principal (not surfaced — probe directly)
  - Judges (Emoluments) Act 1976/22 principal (not surfaced — probe directly)
  - Chartered Institute of Public Relations Act 2003/15 (not surfaced — probe directly)
  - Citizens Economic Empowerment Act 2006 correct AKN slot (still open — try alphabetical listing pagination)
  - 13 unprobed candidate slots from `_work/batch_0148_discovery.json` (ranks 12+): review for primary statutes vs amendments on next tick.
