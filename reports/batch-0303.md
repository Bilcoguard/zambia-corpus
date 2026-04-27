# Batch 0303 Report

**Phase:** 4 — bulk (minimal upstream-refresh tick)
**Tick:** 2026-04-27 (UTC) — scheduled tick, 30-min cadence
**Yield:** 0 records committed
**Wall-clock:** ~3 min
**Parser version:** 0.5.0 (probe-only — same as b0290..b0302)

## Summary

This tick is a minimal upstream-refresh probe of the two chronological
Act feeds:

- `zambialii.org/legislation/recent`
- `parliament.gov.zm/acts-of-parliament` (page 0)

All 22 active alphabet letters on zambialii were exhaustively swept
across b0291..b0293, so no alphabet sweep is performed this tick.

**Result:** 0 in-priority candidates; 0 off-priority candidates. All
upstream entries already in corpus. Steady state preserved across
b0290..b0303 (fourteen consecutive ticks).

## Tick context

Pre-tick lock cleanup ran cleanly (no `.lock`/`.lock.bak` files
remaining at tick start; benign `Operation not permitted` on
`.git/objects/maintenance.lock` is a sandbox-cannot-delete artefact and
does not block git ops). `git pull --ff-only` returned "Already up to
date" on first attempt.

## Refresh probe — zambialii /legislation/recent

13 act links enumerated:

- 2025/5  National Road Fund (Amendment) Act
- 2025/6  Building Societies (Amendment) Act
- 2025/7  Animal Health (Amendment) Act
- 2025/8  Border Management and Trade Facilitation Act
- 2025/9  Supplementary Appropriation (2025) Act
- 2025/22 Mobile Money Transaction Levy (Amendment) Act
- 2025/23 Companies (Amendment) Act
- 2025/24 Registration of Business Names (Amendment) Act
- 2025/25 Independent Broadcasting Authority Act
- 2025/26 Zambia National Broadcasting Corporation Act
- 2025/27 Betting Levy Act
- 2025/28 Appropriation Act
- 2025/29 Zambia Institute of Procurement and Supply Act

Cross-check vs `records/acts/`: **all 13 already in corpus** (verified
by year/num prefix match against `act-zm-YYYY-NNN-*.json`).

## Refresh probe — parliament /acts-of-parliament page 0

20 acts enumerated (matched via `Act No. N of YYYY` text pattern):

- 2025/21..29 (nine acts)
- 2026/1..11  (eleven acts)

Cross-check vs `records/acts/`: **all 20 already in corpus**.

## Per-priority sub-phase disposition

| Sub-phase                     | Modern (>=2017) novel | Notes |
|-------------------------------|-----------------------|-------|
| acts_in_force                 | 0                     | all 33 chronological-feed entries already on disk |
| sis_corporate                 | 0                     | alphabet exhaust complete (b0291..b0293) |
| sis_tax                       | 0                     | alphabet exhaust complete |
| sis_employment                | 0                     | alphabet exhaust complete |
| case_law_scz                  | n/a                   | judiciary scope (not in this probe) |
| sis_data_protection           | 0                     | upstream steady state |
| sis_mining                    | 0                     | alphabet exhaust complete |
| sis_family                    | 0                     | alphabet exhaust complete |

## robots.txt re-verification

| Source     | sha256 | Match |
|------------|--------|-------|
| zambialii  | `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` | yes (unchanged from b0193..b0302) |
| parliament | `278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762` | yes (unchanged from b0290..b0302) |

Crawl-delay: zambialii 5s (using 6s margin); parliament 10s (using 11s margin).

## Integrity check

CHECK1..CHECK6 (duplicate IDs, amended_by/repealed_by/cited_authorities
resolution, source_hash match) are **N/A** — zero record writes this
tick, nothing new to integrity-check.

Cumulative-invariant checks (steady-state assertions): **PASS**
- acts cumulative count: 1169 (unchanged from b0302)
- SIs cumulative count: 539 (unchanged from b0302)
- judgments cumulative count: 25 (unchanged from b0302)
- robots SHAs: both match expected
- novel candidates: 0 zambialii, 0 parliament
- `records/` tree: git-clean

## corpus.sqlite

Update **deferred** — established disposition (FTS5 vtable broken,
journal held open). Not regressed this tick.

## B2 sync

`rclone` is not available in the corpus-worker sandbox; B2 sync to
`b2raw:kwlp-corpus-raw/` is **deferred to host**. (No new raw bytes
this tick anyway — probe responses are not corpus raw artefacts.)

## OCR backlog

21 records (unchanged from b0293..b0302). Awaiting host-side OCR flow.

## Disposition

Phase 4 cannot meaningfully advance further with the current
toolset+sources. Awaiting one of:

  (a) human confirmation that Phase 4 is complete (set
      `phase_4_bulk.complete: true` in `approvals.yaml` — worker may
      not flip this flag), or
  (b) approval of Phase 5 / a successor phase, or
  (c) authorisation to expand the source map (out of Phase 4 scope), or
  (d) host-side OCR flow to drain the 21-record OCR backlog.
