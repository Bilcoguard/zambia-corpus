# Phase 4 Batch 0237 Report

**Date:** 2026-04-25
**Sub-phase footprint:** sis_elections +8 (drain, cohort 3 from batch 0233 E-probe cache)
**Yield:** 8/8 (100%)
**Cumulative SI records after batch:** 482 (+8 over batch 0236's 474)
**First-instance sub-phases this tick:** 0 (sis_elections established in batch 0233)

## Records ingested

| # | ID | Title | Year/Num | Parent Act |
|---|----|----|----|----|
| 1 | si-zm-2020-063-... | Electoral Process (LG By-Elections) (No. 6) Order, 2020 | 2020/63 | Electoral Process Act |
| 2 | si-zm-2020-061-... | Electoral Process (LG By-Election) (No. 5) Order, 2020 | 2020/61 | Electoral Process Act |
| 3 | si-zm-2020-043-... | Electoral Process (LG By-Election) (No. 4) Order, 2020 | 2020/43 | Electoral Process Act |
| 4 | si-zm-2020-023-... | Electoral Process (LG By-Elections) (No. 3) Order, 2020 | 2020/23 | Electoral Process Act |
| 5 | si-zm-2020-004-... | Electoral Process (LG By-Elections) (No. 2) Order, 2020 | 2020/4 | Electoral Process Act |
| 6 | si-zm-2020-003-... | Electoral Process (LG By-Elections) Order, 2020 | 2020/3 | Electoral Process Act |
| 7 | si-zm-2020-002-... | National Assembly By-Election (Chilubi No. 095) Order, 2020 | 2020/2 | Electoral Process Act |
| 8 | si-zm-2023-008-... | Electoral Process (LG By-Elections) Order, 2023 | 2023/8 | Electoral Process Act |

## Integrity checks (all PASS)

- CHECK1a: 8/8 unique batch ids
- CHECK1b: 8/8 corpus presence on disk
- CHECK2/3: amended_by + repealed_by — 0 refs
- CHECK4: source_hash sha256 verified 8/8 against `raw/zambialii/si/(2020,2023)/`
- CHECK5: required fields 10×8 all present
- CHECK6: cited_authorities — 0 refs

## Discovery / fetches

- Discovery cost: 1 robots reverify (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0236)
- Per-record fetches: 16 (8 HTML + 8 PDF) on zambialii.org under robots-declared 5s crawl-delay (CRAWL=6s margin)
- Cache reuse from batch_0233 E-probe (no fresh alphabet probes needed)

## E residuals after this tick

~30 left from batch-0233 cache (38 - 8). Remaining cohort (truncated): 2019/76, 2019/61, 2019/38, 2019/33, 2019/24, 2019/23 + 2023/36/40/46 + 2024/2/6/15 + earlier 2017/* and 2018/* novel entries.

## Tick recovery note

Tick-start `git pull --ff-only` failed due to stale virtiofs `.git/index.lock` + diverged worker.log (carried over from batch 0236 close-out). Resolved by syncing local worker.log/costs.log/gaps.md to `origin/main` blob content + `update-ref refs/heads/main origin/main` (workaround stable across batches 0192-0237 — write-tree/commit-tree path bypasses lock).

## Next-tick plan

(a) continue draining E residuals (~30 left); (b) rotate to acts_in_force priority_order item 1 (requires Acts-listing endpoint discovery — separate path); (c) re-attempt OCR backlog (6 items: 2017/068, 2018/011, 2022/004, 2022/007, 2022/008, 2022/012); (d) fresh alphabet re-probes G/H/K/P. Re-verify robots.txt at start of next tick.
