# Batch 0281 Report

- **Phase**: 4 (bulk) — `acts_in_force` (priority_order[0])
- **Worker**: kwlp-worker / peter@bilcoguard.com
- **Tick start (UTC)**: 2026-04-26T20:33:00Z
- **Parser version**: 0.6.0-act-zambialii-2026-04-26 (reused from b0269..0280)
- **Crawl-delay**: 6s (margin over robots.txt Crawl-delay 5s)
- **Robots.txt sha256 prefix**: fce67b697ee4ef44 (unchanged from b0193..0280)

## Source

- Pool inherited from `_work/batch_0280_remaining.json` (70 items).
- Picks: first 8 chronologically-earliest. Pre-flight slug-glob dedup PASS for all 8 (none on disk).

## Picks (8)

| idx | yr/num | alpha | title | result | sections |
|---:|---|---:|---|---|---:|
| 0 | 2006/17 | A | Appropriation Act, 2006 | ok | 2 |
| 1 | 2007/8 | S | Supplementary Appropriation (2005) Act, 2007 | ok | 2 |
| 2 | 2007/9 | A | Appropriation Act, 2007 | ok | 2 |
| 3 | 2007/14 | E | Excess Expenditure Appropriation (2004) Act, 2007 | ok | 2 |
| 4 | 2008/5 | A | Appropriation Act, 2008 | **pdf_too_large_5181722** (>4.5MB) — deferred | — |
| 5 | 2008/6 | E | Excess Expenditure Appropriation (2005) Act, 2008 | ok | 2 |
| 6 | 2008/9 | S | Supplementary Appropriation (2006) Act, 2008 | ok | 105 (OCR over-match — section-tolerant retry queue) |
| 7 | 2009/6 | E | Excess Expenditure Appropriation (2006) Act, 2009 | ok | 2 |

**Yield**: 7/8 (87.5%). Same as b0279, b0280.

## Integrity (`_work/batch_0281_integrity.txt`)

- CHECK1a unique IDs in batch: 7/7 PASS
- CHECK1b corpus presence on disk: 7/7 PASS
- CHECK2 amended_by refs resolve: 0 refs (PASS)
- CHECK3 repealed_by refs resolve: 0 refs (PASS)
- CHECK4 source_hash sha256 verified vs raw HTML: 7/7 PASS
- CHECK5 required 16 fields × 7 records = 112/112 PASS
- CHECK6 cited_authorities refs resolve: 0 refs (PASS)
- **All checks PASS**

## Sub-runs

Ingestion split across 4 sub-runs (slice 0:2 + 2:4 + 4:6 + 6:8) due to 45s sandbox shell timeout × 6s crawl-delay. All sub-runs reuse `ingest_one()` (identical parser, UA, crawl-delay 6s).

## Gaps logged

- act/2008/5: oversize PDF (5,181,722 bytes > 4.5 MB) — added to oversize-pdf queue (now 3 items: 2002/6, 2005/21, 2008/5).
- act/2008/9: 105 sections from PDF OCR over-match — added to section-tolerant retry queue (now 5 items).
- OCR backlog unchanged at 18.

## Pool state

- Remaining after b0281: 62 items (saved to `_work/batch_0281_remaining.json`).
- Next chronological: 2009/7 → 2009/10 → 2009/16 (Non-Governmental Organisations Act — non-fiscal) → 2009/30 → 2010/4 (Public Interest Disclosure / Whistleblowers — non-fiscal) …
- Next-tick plan: sweep next 8 chronological from 2009/7 onwards. The block of remaining 2009 fiscal acts ends at index 3; from 2009/16 onwards yield should improve as non-fiscal acts return.

## B2 sync

`rclone` not available in sandbox. Raw HTML/PDF cached locally; B2 sync deferred to host: `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`.

## Today's budget

- Fetches: ~520 → ~535/2000 (~27% of daily budget after b0281).
- Tokens: well within budget.
