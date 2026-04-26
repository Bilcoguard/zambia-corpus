# Phase 4 — Batch 0284 report

- Tick start: 2026-04-26T22:03Z (UTC)
- Phase: phase_4_bulk (acts_in_force)
- Pool inherited from batch 0283: 46 items
- Picks this tick (8 chronologically-earliest):
  1. 2014/5  — Supplementary Appropriation (2012) Act, 2014           (alpha S, fiscal)
  2. 2014/6  — Excess Expenditure Appropriation (2011) Act, 2014      (alpha E, fiscal)
  3. 2014/14 — Appropriation Act, 2014                                (alpha A, fiscal)
  4. 2015/9  — Supplementary Appropriation (2013) Act, 2015           (alpha S, fiscal)
  5. 2015/10 — Excess Expenditure Appropriation (2012) Act, 2015      (alpha E, fiscal)
  6. 2015/23 — Appropriation Act, 2015                                (alpha A, fiscal)
  7. 2016/7  — Court of Appeal Act, 2016                              (alpha C, NON-FISCAL)
  8. 2016/15 — Public Protector Act, 2016                             (alpha P, NON-FISCAL)

## Outcomes

| idx | year/num | status | id | sections |
|-----|----------|--------|----|---------:|
| 0 | 2014/5  | ok | act-zm-2014-005-supplementary-appropriation-2012-act      |  2 |
| 1 | 2014/6  | ok | act-zm-2014-006-excess-expenditure-appropriation-2011-act |  2 |
| 2 | 2014/14 | ok | act-zm-2014-014-appropriation-act                         |  3 |
| 3 | 2015/9  | ok | act-zm-2015-009-supplementary-appropriation-2013-act      |  2 |
| 4 | 2015/10 | ok | act-zm-2015-010-excess-expenditure-appropriation-2012-act |  2 |
| 5 | 2015/23 | ok | act-zm-2015-023-appropriation-act                         |  2 |
| 6 | 2016/7  | ok | act-zm-2016-007-court-of-appeal-act                       | 49 |
| 7 | 2016/15 | ok | act-zm-2016-015-public-protector-act                      | 71 |

Yield: **8/8 (100%)**. No deferrals. All 8 picks triggered the PDF fallback (HTML akn-section count was <2 in each case for this 2014–2016 cohort, consistent with prior batches in this fiscal series and with the canonical Court of Appeal / Public Protector Act renderings on ZambiaLII). PDFs parsed cleanly within the 4.5 MB cap (largest = 1.87 MB for 2014/14 Appropriation Act). Court of Appeal Act yielded 49 sections, Public Protector Act 71 — the two non-fiscal picks contributed the bulk of section content. Fiscal Appropriation/Supplementary Acts each parsed at their canonical 2–3 section structure.

## Provenance

All 8 records carry source_url, sha256 source_hash (verified against on-disk raw HTML), fetched_at (ISO 8601 UTC), parser_version `0.6.0-act-zambialii-2026-04-26`. Raw HTML cached under `raw/zambialii/act/{year}/{year}-{nnn}.html` (gitignored).

## Integrity

- CHECK1a (batch unique IDs): PASS 8/8
- CHECK1b (corpus on-disk presence): PASS 8/8
- CHECK2 (amended_by resolution): PASS 0 refs
- CHECK3 (repealed_by resolution): PASS 0 refs
- CHECK4 (source_hash sha256 vs raw HTML): PASS 8/8
- CHECK5 (required 16 fields × 8 = 128 cells): PASS 128/128
- CHECK6 (cited_authorities resolution): PASS 0 refs

## Source compliance

- robots.txt fetched at tick start, sha256 = `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` (unchanged from batches 0193..0283).
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.
- Crawl-delay: 6s between fetches (margin over robots Crawl-delay 5).

## Budget

- Today fetches at tick start: 564/2000 (~28.2%).
- Today fetches after batch: 580/2000 (~29.0%) — 16 fetches consumed (8 HTML + 8 PDF fallbacks).
- Tokens within budget.

## Pool state

- Inherited pool: 46 items.
- Consumed this batch: 8.
- Carry-forward to batch 0285: 38 items (written to `_work/batch_0284_remaining.json`).
- Next-tick plan: sweep next 8 chronological from 2016/36 onwards (6 fiscal-series + 2017/22 boundary; 2018/1 Public Finance Management Act is 10th, just outside the next-8 window).

## B2 sync

`rclone` not available in sandbox — host-side sync deferred. Peter to run:

    rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
