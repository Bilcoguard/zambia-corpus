# Batch 0307 Report

**Phase:** 4 — bulk (minimal upstream-refresh tick)
**Tick:** 2026-04-27/28 (UTC) — scheduled tick, 30-min cadence
**Yield:** 0 records committed
**Wall-clock:** ~3 min
**Parser version:** 0.5.0 (probe-only — same as b0290..b0306)

## Summary

This tick is a minimal upstream-refresh probe of the two chronological
Act feeds:

- `zambialii.org/legislation/recent`
- `parliament.gov.zm/acts-of-parliament` (page 0)

All 22 active alphabet letters on zambialii were exhaustively swept
across b0291..b0293, so no alphabet sweep is performed this tick.

**Result:** 0 in-priority candidates; 0 off-priority candidates. All
upstream entries already in corpus. Steady state preserved across
b0290..b0307 (eighteen consecutive ticks).

## Tick context

Pre-tick lock cleanup ran cleanly (no `.lock`/`.lock.bak` files
remaining at tick start; benign `Operation not permitted` on
`.git/objects/maintenance.lock` is the sandbox-cannot-delete artefact
and does not block git ops).
`git pull --ff-only` returned "Already up to date" on first attempt.

## Refresh probe — zambialii /legislation/recent

13 act links enumerated (year/num pairs):

- 2025/5, 2025/6, 2025/7, 2025/8, 2025/9
- 2025/22, 2025/23, 2025/24, 2025/25, 2025/26, 2025/27, 2025/28, 2025/29

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
| zambialii  | `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` | yes (unchanged from b0193..b0306) |
| parliament | `278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762` | yes (unchanged from b0290..b0306) |

Crawl-delay: zambialii 5s (using 6s margin); parliament 10s (using 11s margin).

## Integrity check

CHECK1..CHECK6 (duplicate IDs, amended_by/repealed_by/cited_authorities
resolution, source_hash match) are **N/A** — zero record writes this
tick, nothing new to integrity-check.

Cumulative-invariant checks (steady-state assertions): **PASS**

- acts cumulative count: 1169 (unchanged from b0306)
- SIs cumulative count: 539 (unchanged from b0306)
- judgments cumulative count: 25 (unchanged from b0306)
- robots SHAs match expected for both sources
- novel_true=0/0 (zambialii/parliament refresh probes)
- `records/` tree git-clean

## Budget posture

- Today fetches at tick start: 116/2000 (~5.8%).
- Tick fetches: 4 (2 robots + zambialii recent + parliament page 0).
- Tokens within budget.

## B2 sync

`rclone` is not available in the sandbox. B2 sync deferred to host
(established disposition since the worker.log entries documenting the
sandbox missing rclone from b0193 onward).

## Phase 4 disposition

Phase 4 remains at upstream steady state for the eighteenth consecutive
tick (b0290..b0307). Worker does not flip the `complete:` flag —
awaiting human confirmation per BRIEF.md non-negotiable #4.

`worker.log` line: "Phase 4 appears complete, awaiting human confirmation".
