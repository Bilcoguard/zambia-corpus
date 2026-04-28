# Batch 0327 Report

**Phase:** 4 — bulk (minimal upstream-refresh tick)
**Tick:** 2026-04-28 (UTC) — scheduled tick, 30-min cadence
**Yield:** 0 records committed
**Wall-clock:** ~3 min
**Parser version:** 0.5.0 (probe-only — same as b0290..b0326)

## Summary

This tick is a minimal upstream-refresh probe of the two chronological
Act feeds:

- `zambialii.org/legislation/recent`
- `parliament.gov.zm/acts-of-parliament` (page 0)

All 22 active alphabet letters on zambialii were exhaustively swept
across b0291..b0293, so no alphabet sweep is performed this tick.

**Result:** 0 in-priority candidates; 0 off-priority candidates. All
upstream entries already in corpus. Steady state preserved across
b0290..b0327 (thirty-eighth consecutive tick).

## Tick context

Pre-tick lock cleanup ran cleanly. Benign `Operation not permitted` on
`.git/objects/maintenance.lock` is the sandbox-cannot-delete artefact
and does not block git operations.
`git pull --ff-only` returned "Already up to date" on first attempt.

## Refresh probe — zambialii /legislation/recent

16 act links enumerated (year/num pairs):

- 2026/1, 2026/2, 2026/3, 2026/4, 2026/5, 2026/6, 2026/7, 2026/8, 2026/10
- 2025/5, 2025/6, 2025/7, 2025/8, 2025/9
- 2025/28, 2025/29

Cross-check vs `records/acts/` (full-tree walk; the records tree mixes
flat-root modern files with per-year subdirectories for legacy years):
**all 16 already in corpus** (verified by year/num prefix match against
`act-zm-YYYY-NNN-*.json`).

Page bytes: 95,192 (b0326: 94,772 — feed re-ranked to lead with 2026/*
entries; no new act IDs appeared).
Page sha256: `1c1bb006edda00f240e42e0fc8c0ca1804301fe4f90918c949c153ebda191665`
(differs from b0316..b0326 due to feed re-ranking, not new content).

Note: `2026/9` and `2026/11` did not appear in the recent feed surface
this tick, but both are present in `records/acts/` (sourced via
parliament's chronological feed, where they remain visible).

## Refresh probe — parliament /acts-of-parliament page 0

20 acts enumerated (matched via `Act No. N of YYYY` text pattern):

- 2025/21..29 (nine acts)
- 2026/1..11  (eleven acts)

Cross-check vs `records/acts/`: **all 20 already in corpus**.

Page bytes: 38,208 (sha differs across ticks due to session/CSRF token
churn, but byte-count and extracted act-list are stable).
Page sha256 this tick: `16fd6f327d1bf9f24ba74bc78c90346aa3a0118f8968bdc27b1f4af8d0a35588`.

## Per-priority sub-phase disposition

| Sub-phase                     | Modern (>=2017) novel | Notes |
|-------------------------------|-----------------------|-------|
| acts_in_force                 | 0                     | all 36 chronological-feed entries already on disk (16 zam + 20 parl, intersecting set) |
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
| zambialii  | `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` | yes (unchanged from b0193..b0326) |
| parliament | `278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762` | yes (unchanged from b0290..b0326) |

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

See `_work/batch_0327_probe.json`.

## Cost / budget

- Today (UTC) fetches before tick: 68 (b0310..b0326 ran earlier on 2026-04-28)
- Fetches this tick: 4 (2 robots + 2 page probes)
- Today (UTC) fetches after tick: 72 / 2000 (~3.6%)

## B2 sync

Deferred to host (rclone not available in sandbox).

## corpus.sqlite

Update deferred — established disposition (FTS5 vtable broken, journal
held open). Not regressed this tick.

## Phase 4 disposition

Phase 4 appears at upstream steady state for the **thirty-eighth**
consecutive tick (b0290..b0327). Worker does **not** flip
`approvals.yaml`. Awaiting human confirmation per non-negotiable #4.

Cannot meaningfully advance further without one of:
1. Human flip of `phase_4_bulk.complete` to `true`, or
2. Approval of Phase 5 / a successor phase, or
3. Authorisation to expand the source map (out of Phase 4 scope), or
4. Host-side OCR flow to drain the 21-record OCR backlog.
