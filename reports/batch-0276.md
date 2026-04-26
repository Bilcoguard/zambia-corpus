# Batch 0276 — Phase 4 bulk ingest (acts_in_force, page-2 cross-alphabet)

**Date:** 2026-04-26
**Phase:** phase_4_bulk
**Sub-phase:** acts_in_force (priority_order item 1)
**Yield:** 8 / 8 (100%)
**Cumulative records (post-batch):** acts 1078, SIs 539, judgments 25, **total 1642**

## Summary
Per next-tick plan in batch 0275 worker.log entry, this tick fetched `?page=2` listings
for the 6 alphabets that paginate (A, C, E, N, P, S). Page-2 surface enumerated 126
total act entries; 110 missing from corpus after dedup against all on-disk
`records/acts/**/*.json` `source_url` `/akn/zm/act/{yr}/{num}` keys (476 unique
`(yr,num)` tuples on disk pre-tick; 1633 unique `id`s post-tick). The 8 chronologically
earliest missing picks span alphabets E, N, P (no A/C/S in the earliest 8: earliest A
page-2 entry is 1914/1 Authentication of Documents but already in corpus under cap-001
slug; earliest S page-2 entry is 1973/41 Supreme Court).

## Picks (chronological)

| # | Year/Num | Alpha | Title | Slug | Sections | Source |
|---|---|---|---|---|---|---|
| 1 | 1920/2  | P | Public Pounds and Trespass Act, 1920          | public-pounds-and-trespass-act          | 83 | HTML primary |
| 2 | 1925/24 | E | Export of Pigs Act, 1925                       | export-of-pigs-act                       | 4  | HTML primary |
| 3 | 1929/20 | P | Public Officers (Change of Titles) Act, 1929   | public-officers-change-of-titles-act     | 3  | HTML primary |
| 4 | 1944/13 | E | Extermination of Mosquitoes Act, 1944          | extermination-of-mosquitoes-act          | 8  | HTML primary |
| 5 | 1953/59 | N | Noxious Weeds Act, 1953                        | noxious-weeds-act                        | 14 | HTML primary |
| 6 | 1964/14 | P | Public Holidays Act, 1964                      | public-holidays-act                      | 3  | HTML primary |
| 7 | 1964/56 | P | Public Seal Act, 1964                          | public-seal-act                          | 5  | HTML primary |
| 8 | 1968/40 | N | Notaries Public and Notarial Functions Act, 1968 | notaries-public-and-notarial-functions-act | 32 | HTML primary |

## Provenance
- All 8 records use `parser_version` `0.6.0-act-zambialii-2026-04-26` (unchanged from batches 0269-0275).
- All HTML sourced from `https://zambialii.org/akn/zm/act/{yr}/{num}` under
  `User-Agent: KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` with
  6s crawl-delay (margin over robots-declared 5s).
- Raw HTML cached at `raw/zambialii/act/{yr}/{yr}-{num:03d}.html`; no PDF fallback
  triggered this batch (every pick returned ≥2 akn-sections from HTML).
- `source_hash` is sha256 of raw HTML bytes (CHECK4 verified).

## Discovery cost
- 1 robots.txt re-verify (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0275).
- 6 page-2 alphabet listing fetches: A (150220 b), C (125301 b), E (133291 b), N (107493 b), P (138339 b), S (156811 b).

## Per-record cost
- 8 record HTML fetches.
- 0 PDF fallback fetches (every pick returned ≥2 HTML akn-sections; PDF gate at <2 not tripped).

## Today's fetches
- Pre-tick: 386
- This tick: 1 robots + 6 page-2 listings + 8 record HTML = 15
- Post-tick: **401 / 2000** (20.05% of daily budget)
- Tokens: within budget.

## Integrity (all PASS)
- CHECK1a: batch IDs unique 8/8
- CHECK1b: on-disk presence 8/8
- CHECK2: amended_by references resolved (0 refs)
- CHECK3: repealed_by references resolved (0 refs)
- CHECK4: source_hash sha256 verified 8/8 against raw HTML on disk
- CHECK5: required fields 16 × 8 = 128/128
- CHECK6: cited_authorities references resolved (0 refs)

## Notes
- Page-2 surface significantly expanded the residual pool (110 missing remaining after
  this batch's 8). Future ticks can sweep ~13 more 8-batches before exhausting page-2.
- Page-3 listings not yet probed — defer to a tick after page-2 surface is consumed.
- 1956/4 disambiguator-deferred item still pending implementation of disambiguator-aware
  fetch handler.
- 2 alphabet=C deferred large items (Citizens Economic Empowerment 2006/9 +
  Constitution of Zambia 1996/17) and OCR backlog (17 items) unchanged this tick.
- B2 sync: rclone unavailable in sandbox; raw files for batches 0192-0276 await
  host-driven `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`.
- corpus.sqlite snapshot drift unchanged this batch (drift preserved per established
  workflow; expects periodic full rebuild from host).
