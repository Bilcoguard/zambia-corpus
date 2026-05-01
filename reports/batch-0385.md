# Batch 0385 — Audit-only tick (10th substantive; recovers from b0384 git block)

**Timestamp:** 2026-05-01T03:05:37Z
**Phase:** 5 (judgments) — `approved: true, complete: false`
**Action:** Cleared the host-side stale-`.lock.bak` ref residue that hard-blocked b0384 (and the unnumbered 02:03Z attempt before it); ran reparse-first inventory audit; no parser run; no fresh fetches; no records written.
**Outcome:** v0.3.1 reparse inventory remains FULLY EXHAUSTED. Phase 5 progress 78/100–160 (unchanged for 10 substantive consecutive audit ticks: b0375 → b0376 → b0377 → b0378 → b0379 → b0380 → b0381 → b0382 → b0383 → b0385; b0384 was a fail-stop on git pull and produced no audit). 0 fresh fetches; 0 records written; 0 records deferred.

## Recovery from b0384 git block

The previous tick (b0384) — and the unnumbered 02:03Z attempt before it — both fail-stopped at Step 1 (`git pull --ff-only`) on a poisoned `.git/refs/remotes/origin/` directory. Four `main.lock.bak.*` files were sitting in the remote-refs dir from earlier ticks (b0293, b0365, b0383b, plus a numeric-timestamped one), and `git` was reading every regular file in that dir as a ref candidate, then bailing with `fatal: bad object refs/remotes/origin/main.lock.bak.b0383b.20260501T013559Z`. b0384 logged the failure to `worker.log` and exited per Step 1 directive (no commit, no push).

This tick cleared the block by `mv`-ing the four stale lock-bak files into a dated quarantine directory at the repo root:

```
_stale_locks_b0384/
  ├── main.lock.bak.1777588653
  ├── main.lock.bak.b0293_close
  ├── main.lock.bak.b0383b.20260501T013559Z
  └── main.lock.bak_b0365b_2
```

(The pre-existing `_stale_locks_b03**` quarantine pattern is unchanged; this dir is named after the tick whose locks were cleared.)

After the move, `git pull --ff-only` reports "Already up to date" — the remote has nothing new. The pre-existing `.git/objects/maintenance.lock` warning (carry-forward from earlier ticks; sandbox cannot unlink it; non-blocking) persists; `git` exits 0 regardless.

## Completion-criterion note (BRIEF.md)

The five-consecutive-zero-discovery completion criterion fired in b0379 and was logged then per BRIEF.md ("On either trigger the worker logs 'Phase 5 appears complete, awaiting human confirmation' to worker.log and stops; only a human flips complete: true in approvals.yaml"). It is now the TENTH substantive consecutive idle tick (b0384 was a fail-stop and is excluded from the substantive count). `approvals.yaml` is unchanged since 2026-04-30 15:36:40Z (commit `b24a938` — "Lock in parser_v0.3.1 + reparse-first policy across BRIEF.md and approvals.yaml"); ~11h 29m wall-clock at this tick start. Per Phase 5 non-negotiable, the worker does NOT modify `approvals.yaml` — only Peter flips `complete: true`. The phase remains formally `approved+incomplete`, so this tick still ran the bounded reparse-first audit step rather than terminating to "idle - awaiting approval".

The worker's substantive assessment is unchanged from b0379–b0383: Phase 5 is **not substantively complete** — progress is stuck at 78/100–160 (78% of lower target, 49% of upper target) because of a parser-vocabulary ceiling on the existing ZMCC backlog, not because the source is exhausted. The five-tick trigger is firing on a parser-block.

## Pre-flight

- `find .git -name "*.lock" -delete` and `*.lock.bak -delete` ran cleanly (no in-`.git` matches; the pre-existing `_stale_locks_b03**_*.lock.bak` entries at repo root from prior ticks are out of `.git/` scope and harmless residue).
- `mv .git/refs/remotes/origin/main.lock.bak* _stale_locks_b0384/` cleared the four stale lock-bak files that had been blocking `git pull` since at least 2026-05-01T02:03Z (≥1 hour of host-side downtime; see "Recovery" above).
- `git pull --ff-only` now reports "Already up to date".
- `approvals.yaml` unchanged since 2026-04-30 15:36:40Z (commit `b24a938`). `phase_5_judgments` remains `approved: true, complete: false`. `parser_v0.3.2` approval, OCR pipeline approval, and ZMSC fresh-DESC-sweep approval all still pending.
- UTC date: 2026-05-01 (this is the 4th substantive tick of the new UTC day after b0380/b0381/b0382/b0383, with b0384's fail-stop in between). Today's cumulative fetches at tick start = 0 / 2000.

## Inventory snapshot (programmatic, identical to b0378–b0383)

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

Identical inventory to b0378 / b0379 / b0380 / b0381 / b0382 / b0383 — no drift across the b0384 fail-stop.

## Programmatic gaps.md cross-check

- Iterated every gaps.md bullet whose deferral line contains `outcome_not_inferable_under_tightened_policy` (the v0.3.0 generic reason that v0.3.1 was meant to address). 19 such bullets exist; **all 19 carry a follow-up `RESOLVED in batch-NNNN (parser_v0.3.1)` or `RECLASSIFIED in batch-NNNN (parser_v0.3.1) — specific reason …` line**. Zero unprocessed v0.3.0-generic candidates remain.
- Scanned remaining gaps.md deferral codes; the 89 missing ZMCC candidates now sit under v0.3.1-specific codes that are NOT addressable by v0.3.1:
  - 114 lines `html_no_summary_pdf_no_match` — needs parser_v0.3.2 vocabulary widening.
  - 14 lines `parser_v0.3.1_judges_no_comma_unhandled` — needs parser_v0.3.2.
  - 10 lines `pdf_extraction_empty_likely_scanned` — needs OCR.
  - 2 lines `multi_judge_separate_opinions_no_clear_majority_disposition` — needs majority-view inference logic.
- (Counts include child / cross-reference lines beyond the per-record bullet headers; the unique deferred-record count remains 89, unchanged.)

## Why the same three options are still on the table this tick

Inputs unchanged from b0379–b0383. Re-stating the unblock list verbatim so the next human review has the full context inline:

1. **parser_v0.3.2 vocabulary widening** — highest yield against existing ZMCC backlog (~70/89 deferred candidates). Adds: declaratory operative verbs ("declares X void"); procedural-refusal patterns ("application is dismissed for lack of jurisdiction", "discontinuance is allowed", "court refused stay"); single-judge composite outcomes ("the single judge declined to grant"); academic-relief patterns ("the declaratory relief was academic"). Subject to Peter approval.
2. **OCR pipeline** for `pdf_extraction_empty_likely_scanned` candidates: zmcc/2021/{14,15}, zmcc/2022/16, zmcc/2025/19. Addresses 4 candidates. Lower yield, parser-orthogonal. Subject to Peter approval (introduces tesseract dependency).
3. **ZMSC fresh DESC sweep** into 2024/2023/etc with parser-baseline extension — highest new-record potential, requires schema-mixing decision (existing 24 ZMSC records use parser_v0.5.0 schema; v0.3.1 sweep would mix two schemas). Subject to Peter approval.

Recommended ordering remains: (1) → (2) → (3).

## Why a fresh DESC sweep was again deferred this tick

Same two considerations as b0379–b0383, unchanged because no inputs have changed:

1. **ZMCC older-year sweep** (pre-2021): pre-2021 ZMCC content is sparse on ZambiaLII (court constituted 2016). Even a successful sweep there would face the same ~85% `html_no_summary_pdf_no_match` defer rate observed in 2021–2026 cohorts under v0.3.1, consuming fetch budget that v0.3.2 will be far more efficient with once approved.
2. **ZMSC older-year sweep**: more attractive parse-success-wise (24/24 in 2025/2026), but introduces the schema-mixing hazard above.

## Integrity check

Trivial PASS — no records written; schema/registry/hash clauses not exercised this tick.

## Persistence

- Files committed this tick: `costs.log`, `worker.log`, `reports/batch-0385.md`, plus the four quarantined lock-bak files now in `_stale_locks_b0384/` (kept under version control to preserve the audit trail of the b0384 git block and the b0385 recovery).
- B2 sync: deferred to host (rclone not in sandbox).
- SQLite ingestion: deferred to host (corpus.sqlite FTS5 malformed-disk-image carry-forward; canonical source remains `records/*.json`).

## Tick budget

Wall-clock well under the 20-minute ceiling. 0 fetches consumed; 0/2000 cumulative for UTC 2026-05-01 at tick end.
