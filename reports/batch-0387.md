# Batch 0387 — Audit-only tick (12th substantive consecutive idle)

**Timestamp:** 2026-05-01T04:03:10Z
**Phase:** 5 (judgments) — `approved: true, complete: false`
**Action:** Reparse-first inventory audit. No parser run; no fresh fetches; no records written; no records deferred.
**Outcome:** v0.3.1 reparse inventory remains FULLY EXHAUSTED. Phase 5 progress 78 / 100–160 (unchanged). 12th substantive consecutive audit-only tick (b0375 → b0376 → b0377 → b0378 → b0379 → b0380 → b0381 → b0382 → b0383 → b0385 → b0386 → b0387; b0384 was a fail-stop on a stale-`.lock.bak` ref condition that b0385 cleared). 0 fresh fetches; 0 records written; 0 records deferred.

## Pre-flight

- `find .git -name "*.lock" -delete` and `*.lock.bak -delete` ran cleanly. The pre-existing `_stale_locks_b03**_*.lock.bak` quarantine entries at the repo root are out of `.git/` scope and harmless residue.
- Only carry-forward stale lock in `.git/` is `.git/objects/maintenance.lock` ("Operation not permitted" on unlink in sandbox; non-blocking — `git` exits 0). No stale `main.lock*` refs in `.git/refs/remotes/origin/` this tick (b0385's mv-quarantine into `_stale_locks_b0384/` cleared them; b0386 ran clean; b0387 confirms).
- `git pull --ff-only` reports "Already up to date".
- `approvals.yaml` unchanged since 2026-04-30 15:36:40Z (commit `b24a938`). `phase_5_judgments` remains `approved: true, complete: false`. No `parser_v0.3.2` approval, no OCR pipeline approval, no ZMSC fresh-DESC-sweep approval. Wall-clock since approvals last touched: ~12h 27m at this tick start.
- UTC date: 2026-05-01 (the 6th substantive tick of the new UTC day after b0380, b0381, b0382, b0383, b0385, b0386). Today's cumulative fetches at tick start = 0 / 2000.

## Inventory snapshot (programmatic; identical to b0378 through b0386)

| Source | Raw HTML/PDF candidates | Records on disk | Missing |
|--------|------------------------|-----------------|---------|
| ZMCC 2021 | 13 | 8 | 5 |
| ZMCC 2022 | 34 | 5 | 29 |
| ZMCC 2023 | 25 | 8 | 17 |
| ZMCC 2024 | 27 | 12 | 15 |
| ZMCC 2025 | 33 | 11 | 22 |
| ZMCC 2026 | 10 | 9 | 1 |
| **ZMCC total** | **142** | **53** | **89** |
| ZMSC 2025/2026 | 24 | 24 | 0 |
| **Total judgment record files** | — | **78** | — |

Identical to b0378–b0386. No drift across 12 substantive consecutive ticks.

## Programmatic gaps.md cross-check (line-frequency, unchanged since b0386)

`gaps.md` modification time: 2026-04-30 21:40:59 UTC (commit `61d666e`) — unchanged since b0379. Counts are stable:

- 114 lines `html_no_summary_pdf_no_match` — needs **parser_v0.3.2** vocabulary widening.
- 14 lines `parser_v0.3.1_judges_no_comma_unhandled` — needs **parser_v0.3.2**.
- 10 lines `pdf_extraction_empty_likely_scanned` — needs **OCR**.
- 2 lines `multi_judge_separate_opinions_no_clear_majority_disposition` — needs majority-view inference logic.
- 49 lines `outcome_not_inferable_under_tightened_policy` (v0.3.0 generic, banned for new deferrals; existing entries retained for historical accuracy).

Unique deferred-record count remains 89 — identical to disk inventory ZMCC missing count.

The 12-of-37 lagging-back-tag bullets noted in b0386 (gaps.md tidiness, not data integrity) remain unchanged this tick. Logged as low-priority back-tag candidates for a future tidy pass.

## Completion-criterion note (BRIEF.md)

The five-consecutive-zero-discovery completion criterion fired in b0379. As of b0387 it is the **12th substantive consecutive audit-only tick**. Per BRIEF.md and `approvals.yaml` Phase 5 non-negotiable, the worker does NOT modify `approvals.yaml`. The phase remains formally `approved+incomplete`, so this tick still ran the bounded reparse-first audit step rather than terminating to "idle - awaiting approval".

The worker's substantive assessment is unchanged from b0379–b0386: Phase 5 is **not substantively complete** at 78 / 100–160. The ceiling is a parser-vocabulary block on the ZMCC backlog, not source exhaustion. Three orthogonal unblocks (all subject to Peter approval) remain on the table.

## Three unblocks — recommended ordering unchanged

1. **parser_v0.3.2 vocabulary widening** — highest yield against existing ZMCC backlog (~70/89 deferred candidates). Adds: declaratory operative verbs ("declares X void"); procedural-refusal patterns ("application is dismissed for lack of jurisdiction", "discontinuance is allowed", "court refused stay"); single-judge composite outcomes ("the single judge declined to grant"); academic-relief patterns ("the declaratory relief was academic"). Subject to Peter approval per BRIEF.md non-negotiable on parser changes.
2. **OCR pipeline** for `pdf_extraction_empty_likely_scanned` candidates: zmcc/2021/{14,15}, zmcc/2022/16, zmcc/2025/19. Addresses 4 candidates. Lower yield, parser-orthogonal. Subject to Peter approval (introduces tesseract dependency).
3. **ZMSC fresh DESC sweep** into 2024/2023/etc with parser-baseline extension — highest new-record potential, requires schema-mixing decision (existing 24 ZMSC records use parser_v0.5.0 schema; v0.3.1 sweep would mix two schemas). Subject to Peter approval.

Recommended ordering: (1) → (2) → (3).

## Why a fresh DESC sweep was again deferred

Same two considerations as b0379–b0386, unchanged because no inputs have changed:

1. **ZMCC older-year sweep** (pre-2021): pre-2021 ZMCC content is sparse on ZambiaLII (court constituted 2016). Even a successful sweep there would face the same ~85% `html_no_summary_pdf_no_match` defer rate observed in 2021–2026 cohorts under v0.3.1, consuming fetch budget that v0.3.2 will be far more efficient with once approved.
2. **ZMSC schema-mixing hazard**: existing 24 ZMSC records use parser_v0.5.0 schema; an unapproved v0.3.1 sweep would mix two schemas. Integrity check suite does not catch schema-mixing — the hazard is a silent corpus-quality regression that a later FTS5 ingestion would surface only as inconsistent search facets.

## Integrity check

Trivial PASS (no records written or deleted; schema/registry/hash/cited_authorities clauses not exercised). No `corpus.sqlite` write attempted (FTS5 malformed-disk-image carry-forward — canonical source remains `records/*.json`).

## Outputs this tick

- `reports/batch-0387.md` — this file.
- `worker.log` append — pre-flight, audit findings, completion-criterion re-affirm, recommendation re-affirm, commit + push log.
- `costs.log` append — `0/2000` cumulative-today; `audit-only-…-TWELFTH-consecutive-idle-tick`.
- `provenance.log` append — audit-only entry (no fetched_at; parser_version=0.3.1 idle).

## Deferred to host (carry-forward)

- **B2 raw sync** (`rclone sync raw/ b2raw:kwlp-corpus-raw/`): `rclone` not present in sandbox PATH. Logged.
- **SQLite ingestion**: `corpus.sqlite` FTS5 "malformed disk image" since b0339; canonical source remains `records/*.json`. Logged.

## Wall-clock

Tick start: 2026-05-01T04:03:10Z. Well under the 20-minute budget (no I/O-heavy work; pure inventory + cross-check pass).
