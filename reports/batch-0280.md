# Batch 0280 — Phase 4 acts_in_force (chronological-first across page-2 fiscal series)

- Date (UTC): 2026-04-26
- Sub-phase: `acts_in_force`
- Pool source: `_work/batch_0279_remaining.json` (78 inherited)
- Picks: first 8 chronologically-earliest from inherited pool
- MAX_BATCH_SIZE: 8
- Robots.txt re-verified at tick start (sha256 prefix `fce67b697ee4ef44`, unchanged from b0193..0279)
- Crawl-delay: 6 s (1 s margin over robots-declared 5 s)
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- Parser version: `0.6.0-act-zambialii-2026-04-26`

## Picks (8)

| idx | yr/num | title | alpha | status | sections | id |
|----|--------|-------|------|--------|----------|----|
| 0 | 2004/7  | Appropriation Act, 2004                              | A | ok                          | 2 | act-zm-2004-007-appropriation-act |
| 1 | 2005/5  | Appropriation Act, 2005                              | A | ok                          | 2 | act-zm-2005-005-appropriation-act |
| 2 | 2005/6  | Excess Expenditure Appropriation (2001) Act, 2005    | E | ok                          | 2 | act-zm-2005-006-excess-expenditure-appropriation-2001-act |
| 3 | 2005/7  | Excess Expenditure Appropriation (2002) Act, 2005    | E | ok                          | 2 | act-zm-2005-007-excess-expenditure-appropriation-2002-act |
| 4 | 2005/8  | Supplementary Appropriation (2003) Act, 2005         | S | ok                          | 3 | act-zm-2005-008-supplementary-appropriation-2003-act |
| 5 | 2005/21 | Cotton Act, 2005                                     | C | pdf_too_large_6931314       | 0 | — (deferred, oversized PDF) |
| 6 | 2006/1  | Supplementary Appropriation (2004) Act, 2006         | S | ok                          | 2 | act-zm-2006-001-supplementary-appropriation-2004-act |
| 7 | 2006/2  | Excess Expenditure Appropriation (2003) Act, 2006    | E | ok                          | 2 | act-zm-2006-002-excess-expenditure-appropriation-2003-act |

Yield: **7 / 8 (87.5 %)** — matches batch 0279.

## Deferrals

- **2005/21 Cotton Act, 2005** — PDF 6,931,314 B > MAX_PDF_BYTES (4,500,000). HTML returned `<2` akn-sections so PDF fallback engaged; over-cap ⇒ no record written; parser refused fabrication. Logged to `gaps.md` and added to oversized-pdf queue (now 2 items: 2002/6, 2005/21).

## Integrity

```
CHECK1a: PASS (7 unique batch IDs)
CHECK1b: PASS (7 records on disk)
CHECK2:  PASS (0 amended_by refs all resolved)
CHECK3:  PASS (0 repealed_by refs all resolved)
CHECK4:  PASS (7 source_hash sha256 verified vs raw/zambialii/act/<yr>/<yr>-<num:03d>.html)
CHECK5:  PASS (16 × 7 = 112 fields)
CHECK6:  PASS (0 cited_authorities refs all resolved)
INTEGRITY: PASS (all 6 checks)
```

## Costs (this tick)

| kind | url | bytes |
|------|-----|------:|
| robots | https://zambialii.org/robots.txt | 2,022 |
| record HTML × 8 | /akn/zm/act/{2004/7, 2005/5, 2005/6, 2005/7, 2005/8, 2005/21, 2006/1, 2006/2} | varies |
| record PDF × 7 (committed) + 1 oversize-rejected | /akn/zm/act/.../source.pdf | varies |

Today (2026-04-26): pre-tick fetches 503 → post-tick ~520 / 2000 (≈26 % of daily budget). Tokens within budget.

## Pool state

- Inherited remaining (after b0279): 78
- This batch processed: 8 (7 committed + 1 deferred)
- New remaining: **70** (persisted in `_work/batch_0280_remaining.json`)

## Cumulative records

- Acts: 1,097 (1,090 from b0279 + 7 this batch)
- SIs: 539 (unchanged)
- Judgments: 25 (paused per robots Disallow on `/akn/zm/judgment/`)

## Infrastructure follow-ups (non-blocking, unchanged across recent batches)

- B2 sync deferred to host: `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4` (rclone unavailable in sandbox).
- corpus.sqlite snapshot drift preserved (full rebuild expected from host).
- Persistent virtiofs unlink-failure on `.git/objects/tmp_obj_*` — non-fatal (rename succeeds).
- Pre-existing FTS5 vtable malformed (`records_fts`) — non-blocking, awaits full rebuild.
- This tick's start was unblocked by moving stale ref `.git/refs/heads/main.lock.b0279_1777230702` (and a `test_delete` probe file) into `.git/_stale_locks_int/` — virtiofs prevents direct unlink but allows rename. After move, `git pull --ff-only` succeeded ("Already up to date.").

## Next-tick plan

1. Re-verify robots.txt at start.
2. Refresh inherited pool (`_work/batch_0280_remaining.json`, 70 items) and glob-dedup against `records/acts/<yr>/act-zm-<yr>-<num:03d>-*.json`.
3. Sweep next 8 chronologically-earliest, avoiding gaps.md-listed items (2005/21 oversize now filtered).
4. Continue acts_in_force; expect continued fluctuation in fiscal-series yield. Once page-2 pool drains (~9 more ticks at current yield), advance to next priority sub-phase (`sis_corporate`).
5. Implement disambiguator-aware fetch handler for 1956/4 (still deferred from b0278).
6. OCR backlog (18 items) and section-tolerant retry queue (4 items: 1988/32, 1994/40, 1995/33, 2004/6) unchanged this batch — addressed by separate dedicated OCR sub-phase.
