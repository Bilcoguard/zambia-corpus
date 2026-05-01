# Batch 0381 — Audit-only tick (7th consecutive)

**Timestamp:** 2026-05-01T00:32:27Z
**Phase:** 5 (judgments) — `approved: true, complete: false`
**Action:** Inventory audit; no parser run; no fresh fetches; no records written.
**Outcome:** v0.3.1 reparse inventory remains FULLY EXHAUSTED. Phase 5 progress 78/100–160 (unchanged for 7 consecutive ticks: b0375 → b0376 → b0377 → b0378 → b0379 → b0380 → b0381).

## Completion-criterion note (BRIEF.md)

The five-consecutive-zero-discovery completion criterion fired in b0379 and was logged then per BRIEF.md ("On either trigger the worker logs 'Phase 5 appears complete, awaiting human confirmation' to worker.log and stops; only a human flips complete: true in approvals.yaml"). It is now the SEVENTH consecutive idle tick. `approvals.yaml` is unchanged since 2026-04-30 15:36:40Z (~33 hours and 56 minutes — the v0.3.1 / reparse-first policy lock-in commit, ref `da50ee5`-era). Per Phase 5 non-negotiable, the worker does NOT modify `approvals.yaml` — only Peter flips `complete: true`. The phase remains formally `approved+incomplete`, so this tick still ran the bounded reparse-first audit step rather than terminating to "idle - awaiting approval".

The worker's substantive assessment is unchanged: Phase 5 is **not substantively complete** — progress is stuck at 78/100–160 (78% of lower target, 49% of upper target) because of a parser-vocabulary ceiling on the existing ZMCC backlog, not because the source is exhausted. The five-tick trigger is firing on a parser-block.

## Pre-flight

- `find .git -name "*.lock" -delete` and `*.lock.bak -delete` ran cleanly (no matches; the persistent `.git/refs/heads/main.lock.bak.b0380.1777594024` and its sibling `.lock` are zero-byte FUSE-pinned residue from b0380 and harmless to operations on `main` — they only break operations on the bogus ref itself).
- `git pull --ff-only` reports "Already up to date". (`.git/objects/maintenance.lock` remains permission-bound and is warned-but-skipped — non-blocking carry-forward.)
- `approvals.yaml` unchanged since 2026-04-30 15:36:40Z. `phase_5_judgments` remains `approved: true, complete: false`. `parser_v0.3.2` approval and OCR pipeline approval both still pending.
- UTC date: 2026-05-01 (same day as b0380). Today's cumulative fetches at tick start = 0 / 2000.

## Inventory snapshot (programmatic, identical to b0378 / b0379 / b0380)

| Source | Raw HTML | Records | Missing |
|--------|---------|---------|---------|
| ZMCC 2021 | 13 | 8 | 5 |
| ZMCC 2022 | 34 | 5 | 29 |
| ZMCC 2023 | 25 | 8 | 17 |
| ZMCC 2024 | 27 | 12 | 15 |
| ZMCC 2025 | 33 | 11 | 22 |
| ZMCC 2026 | 10 | 9 | 1 |
| **ZMCC total** | **142** | **53** | **89** |
| ZMSC 2025 | 20 | 20 | 0 |
| ZMSC 2026 | 4 | 4 | 0 |
| **ZMSC total** | **24** | **24** | **0** |
| Root judgment records | — | 1 | — |
| **Phase 5 total** | **166 raw HTML** | **78 records** | **89** |

## Programmatic gaps.md cross-check

- Iterated every raw HTML slug under `raw/zambialii/judgments/zmcc/{2021..2026}/`.
- Extracted canonical `(year, num)` from each slug via `judgment-zm-(\d{4})-zmcc-(\d+)-`.
- Compared against the same key set extracted from `records/judgments/zmcc/` records (id field `judgment-zm-YYYY-zmcc-NN-…`).
- 89 missing candidates found; **89/89 referenced in `gaps.md`** under v0.3.1-specific reason codes (zero uncatalogued candidates). Identical to b0378 / b0379 / b0380 — no drift across day 2 of the holding pattern.

## Why the same three options are still on the table this tick

Inputs unchanged from b0379 / b0380. Re-stating the unblock list verbatim so the next human review has the full context inline:

1. **parser_v0.3.2 vocabulary widening** — highest yield against existing ZMCC backlog (~70/89 deferred candidates). Adds: declaratory operative verbs ("declares X void"); procedural-refusal patterns ("application is dismissed for lack of jurisdiction", "discontinuance is allowed", "court refused stay"); single-judge composite outcomes ("the single judge declined to grant"); academic-relief patterns ("the declaratory relief was academic"). Subject to Peter approval.
2. **OCR pipeline** for `pdf_extraction_empty_likely_scanned` candidates: zmcc/2021/{14,15}, zmcc/2022/16, zmcc/2025/19. Addresses 4 candidates. Lower yield, parser-orthogonal. Subject to Peter approval (introduces tesseract dependency).
3. **ZMSC fresh DESC sweep** into 2024/2023/etc with parser-baseline extension — highest new-record potential, requires schema-mixing decision (existing 24 ZMSC records use parser_v0.5.0 schema; v0.3.1 sweep would mix two schemas). Subject to Peter approval.

Recommended ordering remains: (1) → (2) → (3).

## Why a fresh DESC sweep was again deferred this tick

Same two considerations as b0379 / b0380, unchanged because no inputs have changed:

1. **ZMCC older-year sweep** (pre-2021): pre-2021 ZMCC content is sparse on ZambiaLII (court constituted 2016). Even a successful sweep there would face the same ~85% `html_no_summary_pdf_no_match` defer rate observed in 2021–2026 cohorts under v0.3.1, consuming fetch budget that v0.3.2 will be far more efficient with once approved.
2. **ZMSC older-year sweep**: more attractive parse-success-wise (ZMSC 2025/2026 is 24/24), but introduces the schema-mixing hazard above.

## Integrity check

Trivial PASS — no records written; schema/registry/hash clauses not exercised this tick.

## Persistence

- Files committed this tick: `costs.log`, `worker.log`, `reports/batch-0381.md`.
- B2 sync: deferred to host (rclone not in sandbox).
- SQLite ingestion: deferred to host (corpus.sqlite FTS5 malformed-disk-image carry-forward; canonical source remains `records/*.json`).

## Tick budget

Wall-clock well under the 20-minute ceiling. 0 fetches consumed.
