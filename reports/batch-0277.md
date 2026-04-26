# Batch 0277 — Phase 4 bulk ingest (acts_in_force, page-2 cross-alphabet)

**Date:** 2026-04-26
**Phase:** phase_4_bulk
**Sub-phase:** acts_in_force (priority_order item 1)
**Yield:** 6 / 8 (75%) — 2 deferred to gaps.md (1 duplicate-existing, 1 pdf_parse_no_sections)
**Cumulative records (post-batch):** acts 1084 (+6 over 1078), SIs 539 (unchanged), judgments 25 (unchanged), **total 1648**

## Summary
Per next-tick plan in batch 0276 worker.log entry, this tick swept the next 8
chronologically earliest from the inherited 102-item page-2 missing pool persisted
in `_work/batch_0276_missing.json`. No new page-2 listing fetches needed. Pool was
re-deduped against on-disk records at tick start (485 unique `(yr,num)` tuples on disk
pre-tick; pool still 102 missing).

Outcome: 6 records committed; 2 deferred (see Gaps section). The 100%-yield streak
across batches 0246-0276 (31 consecutive) ends at this batch — first sub-100% yield in
~32 batches, driven by a stealth duplicate (1988/21 was already in corpus under a
non-`/akn/` source_url that escaped pre-flight dedup) and an OCR-corrupted PDF (1988/32
canonical section "1." misread as "i." breaking the section regex).

## Picks (chronological)

| # | Year/Num | Alpha | Title | Slug | Status | Sections | Source |
|---|---|---|---|---|---|---|---|
| 1 | 1970/55 | N | Nurses and Midwives Act, 1970                                 | nurses-and-midwives-act                                  | OK  | (HTML primary) | HTML primary |
| 2 | 1973/41 | S | Supreme Court of Zambia Act, 1973                             | supreme-court-of-zambia-act                              | OK  | (HTML primary) | HTML primary |
| 3 | 1979/22 | P | Public Officers' Pensions (Zambia) Agreement (Implementation) Act, 1979 | public-officers-pensions-zambia-agreement-implementation-act | OK  | (HTML primary) | HTML primary |
| 4 | 1988/21 | S | Supreme Court and High Court (Number of Judges) Act, 1988     | (deferred — duplicate-existing) | GAP | n/a | n/a |
| 5 | 1988/31 | S | Supplementary Appropriation (1987) Act, 1988                  | supplementary-appropriation-1987-act                     | OK  | (PDF fallback) | PDF fallback |
| 6 | 1988/32 | A | Appropriation (No. 2) Act, 1988                                | (deferred — pdf_parse_no_sections) | GAP | 0 | n/a |
| 7 | 1989/31 | S | Supplementary Appropriation (1988) Act, 1989                  | supplementary-appropriation-1988-act                     | OK  | (PDF fallback) | PDF fallback |
| 8 | 1990/39 | S | Supplementary Appropriation (1989) Act, 1990                  | supplementary-appropriation-1989-act                     | OK  | (PDF fallback) | PDF fallback |

## Gaps (this batch)

- **1988/21** Supreme Court and High Court (Number of Judges) Act, 1988 — DUPLICATE-EXISTING. Pre-flight dedup against on-disk records used the `/akn/zm/act/<yr>/<num>` source_url pattern, but the existing record (`act-zm-1988-021-supreme-court-and-high-court-number-of-judges-act-1988`, fetched 2026-04-20T18:40:15Z, 4 sections) was ingested via the `media.zambialii.org/media/legislation/...` PDF source URL pattern, so it slipped past the dedup. New record file (slug missing trailing -1988) was created and then quarantined to `_stale_locks/act-zm-1988-021-supreme-court-and-high-court-number-of-judges-act.json.b0277-dup` (virtiofs unlink restriction prevented direct removal). No new record committed for this pick. Detail in `gaps.md` Batch 0277 entry.
- **1988/32** Appropriation (No. 2) Act, 1988 — `no_sections`. PDF (5 pages, 12,570 chars extracted) is OCR'd legibly but section "1." was misread as "i." breaking the section regex. Parser refused to fabricate. Raw HTML+PDF preserved at `raw/zambialii/act/1988/1988-032.{html,pdf}` for future OCR-tolerant retry. Detail in `gaps.md` Batch 0277 entry.

## Provenance
- All 6 committed records use `parser_version` `0.6.0-act-zambialii-2026-04-26` (unchanged from batches 0269-0276).
- All HTML sourced from `https://zambialii.org/akn/zm/act/{yr}/{num}` under
  `User-Agent: KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` with
  6s crawl-delay (margin over robots-declared 5s).
- Raw HTML cached at `raw/zambialii/act/{yr}/{yr}-{num:03d}.html`; PDF fallback engaged
  for the 4 Appropriation/Supplementary picks (HTML returned <2 akn-sections).
- `source_hash` is sha256 of raw HTML bytes (CHECK4 verified 6/6).

## Discovery cost
- 1 robots.txt re-verify (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0276).
- 0 alphabet listing fetches (page-1 cached since batch 0269; page-2 cached during batch 0276; pool persisted in `_work/batch_0276_missing.json`).

## Per-record cost
- 8 record HTML fetches (all 8 picks attempted; 7 succeeded HTML fetch; 1988/21 HTML succeeded but quarantined as duplicate; 1988/32 HTML succeeded but PDF parser returned 0 sections).
- 4 PDF fallback fetches (1988/31, 1988/32, 1989/31, 1990/39 — Supplementary/Appropriation fiscal-series format with empty HTML akn-sections).

## Today's fetches
- Pre-tick: 457
- This tick: 1 robots + 8 record HTML + 4 PDF = 13
- Post-tick: **470 / 2000** (23.50% of daily budget)
- Tokens: within budget.

## Integrity (all PASS — 6 records)
- CHECK1a: batch IDs unique 6/6
- CHECK1b: on-disk presence 6/6
- CHECK2: amended_by references resolved (0 refs)
- CHECK3: repealed_by references resolved (0 refs)
- CHECK4: source_hash sha256 verified 6/6 against raw HTML on disk
- CHECK5: required fields 16 × 6 = 96/96
- CHECK6: cited_authorities references resolved (0 refs)

## Notes
- Page-2 missing pool now 96 remaining (102 inherited - 6 committed; 1988/21 and
  1988/32 stay in pool nominally but flagged in gaps.md so they will not be re-picked
  by future ticks via `_work/batch_0277_remaining.json` filter).
- Future ticks can sweep ~12 more 8-batches before exhausting page-2 surface.
- Page-3 listings still not probed — defer until page-2 surface drained.
- 1956/4 disambiguator-deferred item still pending.
- 2 alphabet=C deferred large items (Citizens Economic Empowerment 2006/9 +
  Constitution of Zambia 1996/17) and OCR backlog (17 items) unchanged this tick.
- New parser action items surfaced: (a) extend dedup pre-flight to glob
  `act-zm-<yr>-<num:03d>-*.json` (catches stealth media.zambialii.org-sourced
  duplicates); (b) add OCR-tolerant variant `^[1iIl]\.` for fiscal Appropriation
  Act series. Both deferred to a future parser revision.
- B2 sync: rclone unavailable in sandbox; raw files for batches 0192-0277 await
  host-driven `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`.
- corpus.sqlite snapshot drift unchanged this batch (drift preserved per established
  workflow; expects periodic full rebuild from host).
