# Batch 0336 Report

**Phase:** 4 — bulk (minimal upstream-refresh tick)
**Tick:** 2026-04-29 (UTC) — scheduled tick, 30-min cadence
**Yield:** 0 records committed
**Wall-clock:** ~3 min (probe + commit)
**Parser version:** 0.5.0 (probe-only — same as b0290..b0335)

## Summary

This tick is a minimal upstream-refresh probe of the two chronological
Act feeds:

- `zambialii.org/legislation/recent`
- `parliament.gov.zm/acts-of-parliament` (page 0)

All 22 active alphabet letters on zambialii were exhaustively swept
across b0291..b0293, so no alphabet sweep is performed this tick.

**Result:** 0 in-priority candidates; 0 off-priority candidates. All
upstream entries already in corpus. Steady state preserved across
b0290..b0336 (forty-seventh consecutive tick).

## Tick context

Pre-tick lock cleanup ran cleanly. Benign `Operation not permitted` on
`.git/objects/maintenance.lock` is the sandbox-cannot-delete artefact
and does not block git operations. `git pull --ff-only` returned
"Already up to date" on first attempt.

## Refresh probe — zambialii /legislation/recent

15 act links enumerated (year/num pairs):

- 2026/1, 2026/2, 2026/3, 2026/4, 2026/5, 2026/6, 2026/7, 2026/8, 2026/9, 2026/10, 2026/11
- 2025/6, 2025/7, 2025/8, 2025/9

Cross-check vs `records/acts/` (full-tree walk):
**all 15 already in corpus** (verified by year/num prefix match against
`act-zm-YYYY-NNN-*.json`).

Page bytes: 95,392 (unchanged vs b0329..b0335).
Page sha256: `507f7542eddc74c7089f669398fc86861aea75d60dc9dabe0fbddb922d79321c`
(UNCHANGED vs b0329..b0335 — feed surface and ranking are byte-for-byte
identical for the eighth consecutive tick).

## Refresh probe — parliament /acts-of-parliament page 0

20 acts enumerated (matched via `Act No. N of YYYY` text pattern):

- 2025/21..29 (nine acts)
- 2026/1..11  (eleven acts)

Cross-check vs `records/acts/`: **all 20 already in corpus**.

Page bytes: 38,208 (unchanged across all 47 steady-state ticks).
Page sha256 this tick: `6f9d7206070e7e08388579bbc96174953ce58f2117793381b01e44019c24e4c9`
(differs across ticks — session/CSRF token churn; byte-count and
extracted act-list are stable).

## Per-priority sub-phase disposition

| Sub-phase                     | Modern (>=2017) novel | Notes |
|-------------------------------|-----------------------|-------|
| acts_in_force                 | 0                     | all 35 chronological-feed entries already on disk (15 zam + 20 parl, intersecting set) |
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
| zambialii  | `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` | yes (unchanged from b0193..b0335) |
| parliament | `278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762` | yes (unchanged from b0290..b0335) |

Crawl-delay: zambialii 5s (using 6s margin); parliament 10s (using 11s margin).

## Integrity check

CHECK1..CHECK6 (duplicate IDs, amended_by/repealed_by/cited_authorities
resolution, source_hash match) are **N/A** — zero record writes this
tick, nothing new to integrity-check.

Cumulative-invariant checks (steady-state assertions): **PASS**

| Assertion                       | Result |
|---------------------------------|--------|
| acts files == 1169              | PASS   |
| sis  files == 539               | PASS   |
| judgments files == 25           | PASS   |
| records JSON parse-fail == 0    | PASS (1733 records scanned) |
| references unresolved == 0      | PASS (7 refs total)         |
| source_hash mismatch == 0       | PASS (0/50 sampled raws resolvable in sandbox; 50/50 deferred host-side) |
| `records/` git-clean            | PASS   |
| zambialii novel == 0            | PASS   |
| parliament novel == 0           | PASS   |
| zambialii robots SHA match      | PASS   |
| parliament robots SHA match     | PASS   |

Long-standing pre-tick file/id gap on records (1733 files / 1720 unique
ids; 5 duplicate ids) is pre-tick state, not a regression introduced
this tick.

See `_work/batch_0336_probe.json`.

## Cost / budget

- Today (UTC) fetches before tick: 24 (b0330..b0335)
- Fetches this tick: 4 (2 robots + 2 page probes)
- Today (UTC) fetches after tick: 28 / 2000 (~1.4%)

## B2 sync

Deferred to host (rclone not available in sandbox).

## Phase 4 disposition

Forty-seventh consecutive steady-state tick. Phase 4 cannot meaningfully
advance under the current toolset/scope. Awaiting one of:

  (a) human confirmation that Phase 4 is complete (set `complete: true`
      in `approvals.yaml` — worker may not flip this flag);
  (b) approval of Phase 5 (retrieval API) or a successor phase;
  (c) authorisation to expand the source map (out of Phase 4 scope);
  (d) host-side OCR flow to drain the 21-record OCR backlog.
