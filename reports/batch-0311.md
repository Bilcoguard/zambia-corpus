# Batch 0311 Report

**Phase:** 4 — bulk (minimal upstream-refresh tick)
**Tick:** 2026-04-28 (UTC) — scheduled tick, 30-min cadence
**Yield:** 0 records committed
**Wall-clock:** ~2 min
**Parser version:** 0.5.0 (probe-only — same as b0290..b0310)

## Summary

This tick is a minimal upstream-refresh probe of the two chronological
Act feeds:

- `zambialii.org/legislation/recent`
- `parliament.gov.zm/acts-of-parliament` (page 0)

All 22 active alphabet letters on zambialii were exhaustively swept
across b0291..b0293, so no alphabet sweep is performed this tick.

**Result:** 0 in-priority candidates; 0 off-priority candidates. All
upstream entries already in corpus. Steady state preserved across
b0290..b0311 (twenty-two consecutive ticks).

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

Page bytes: 94,772.
Page sha256: `452f6ec2c4d177e306881f24ecc21d17294e09d6e12b4a06059687ad738b0cfa`.

## Refresh probe — parliament /acts-of-parliament page 0

20 acts enumerated (matched via `Act No. N of YYYY` text pattern):

- 2025/21..29 (nine acts)
- 2026/1..11  (eleven acts)

Cross-check vs `records/acts/`: **all 20 already in corpus**.

Page bytes: 38,208 (sha differs across ticks due to session/CSRF token
churn, but byte-count and extracted act-list are stable).
Page sha256 this tick: `c432dcd1ad4cba35d34a8ce17657b6b5ca103c0f8c7726d73d706a7dc99fcc25`.

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
| zambialii  | `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` | yes (unchanged from b0193..b0310) |
| parliament | `278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762` | yes (unchanged from b0290..b0310) |

Crawl-delay: zambialii 5s (using 6s margin); parliament 10s (using 11s margin).

## Integrity check

CHECK1..CHECK6 (duplicate IDs, amended_by/repealed_by/cited_authorities
resolution, source_hash match) are **N/A** — zero record writes this
tick, nothing new to integrity-check.

Cumulative-invariant checks (steady-state assertions): **PASS**

| Assertion                  | Result |
|----------------------------|--------|
| acts == 1169               | PASS   |
| sis  == 539                | PASS   |
| judgments == 25            | PASS   |
| `records/` git-clean       | PASS   |
| zambialii novel == 0       | PASS   |
| parliament novel == 0      | PASS   |
| zambialii robots SHA match | PASS   |
| parliament robots SHA match| PASS   |

See `_work/integrity_b0311.json`.

## Cost / budget

- Today (UTC) fetches before tick: 4 (b0310 ran earlier on 2026-04-28)
- Fetches this tick: 4 (2 robots + 2 page probes)
- Today (UTC) fetches after tick: 8 / 2000 (~0.4%)

## B2 sync

Deferred to host (rclone not available in sandbox).

## corpus.sqlite

Update deferred — established disposition (FTS5 vtable broken, journal
held open). Not regressed this tick.

## Phase 4 disposition

Phase 4 appears at upstream steady state for the **twenty-second**
consecutive tick (b0290..b0311). Worker does **not** flip
`approvals.yaml`. Awaiting human confirmation per non-negotiable #4.

Cannot meaningfully advance further without one of:
1. Human flip of `phase_4_bulk.complete` to `true`, or
2. Approval of Phase 5 / a successor phase, or
3. Authorisation to expand the source map (out of Phase 4 scope), or
4. Host-side OCR flow to drain the 21-record OCR backlog.
