# Batch 0379 — Audit-only tick (5th consecutive)

**Timestamp:** 2026-04-30T23:32:00Z
**Phase:** 5 (judgments) — approved+incomplete
**Action:** Inventory audit; no parser run; no fresh fetches; no records written.
**Outcome:** v0.3.1 reparse inventory remains FULLY EXHAUSTED. Phase 5 progress 78/100–160 (unchanged for 5 consecutive ticks).

## Completion-criterion note (BRIEF.md)

This is the FIFTH consecutive audit-only tick (b0375 → b0376 → b0377 → b0378 → b0379) where v0.3.1 has produced zero records and zero net inventory change. Per BRIEF.md Phase 5: "five consecutive zero-discovery ticks OR 160 judgments reached. On either trigger the worker logs 'Phase 5 appears complete, awaiting human confirmation' to worker.log and stops; only a human flips complete: true in approvals.yaml."

**Worker is logging "Phase 5 appears complete, awaiting human confirmation" per BRIEF.md.** `approvals.yaml` is NOT modified — only Peter flips `complete: true`.

That said, the worker assessment is that Phase 5 is **NOT substantively complete**. Progress is stuck at 78/100–160 (78% of lower target, 49% of upper target) due to a parser-vocabulary ceiling on the existing ZMCC backlog rather than source exhaustion. The five-tick trigger is firing on a parser-block, not a discovery-block. Human review and one of the dominant unblocks (parser_v0.3.2 vocabulary widening, OCR pipeline, or ZMSC fresh DESC sweep with parser baseline extension) is required to push toward the 100–160 target.

## Pre-flight

- `find .git -name "*.lock" -delete` and `*.lock.bak -delete` ran without sandbox-permission errors this tick. `.git/objects/maintenance.lock` remains permission-bound and was warned-but-skipped under `git pull --ff-only Already up to date` (carry-forward; non-blocking).
- `approvals.yaml` unchanged since 2026-04-30 03:23:12Z. `parser_v0.3.2` approval and OCR pipeline approval both still pending. `phase_5_judgments` remains `approved: true, complete: false`.
- `git pull --ff-only` reports "Already up to date".

## Inventory snapshot (programmatic, identical to b0378)

| Source | Raw HTML+PDF | Records | Missing |
|--------|--------------|---------|---------|
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
| **Phase 5 total** | **167 raw HTML** | **78 records** | **89** |

## Programmatic gaps.md cross-check

- Iterated every raw HTML slug under `raw/zambialii/judgments/zmcc/{2021..2026}/`.
- Extracted canonical `(court, year, num)` from each slug.
- Compared against the same key set extracted from `records/judgments/zmcc/`.
- 89 candidates appear as raw-on-disk no-record. All 89 are referenced in `gaps.md` under v0.3.1-specific reason codes (zero uncatalogued candidates).

## Why a fresh DESC sweep into older years was again deferred this tick

Two distinct considerations:

1. **ZMCC older-year sweep** would extend into pre-2021 territory. Pre-2021 ZMCC content is sparse on ZambiaLII (the court was constituted in 2016). Even a successful sweep there would face the same ~85% `html_no_summary_pdf_no_match` defer rate observed in 2021–2024 cohorts under v0.3.1, consuming fetch budget that v0.3.2 will be far more efficient with once approved.

2. **ZMSC older-year sweep into 2024/2023/etc** is the more attractive candidate (ZMSC 2025/2026 has a 100% parse-success rate at 24/24). HOWEVER, the existing 24 ZMSC records were written under a DIFFERENT schema than parser_v0.3.1 produces (they have `delivery_date`, `parties` block, `paragraphs` array; parser_v0.5.0). Running v0.3.1 against a fresh ZMSC DESC sweep would produce records with the v0.3.1 schema (`date_decided`, `case_name`, `judges[*]` with role/dissented, `outcome` enum, etc.) — mixing two schemas in the same `records/judgments/zmsc/` tree creates an integrity hazard that is NOT addressed by the integrity check suite. The parser_baseline locked in approvals.yaml is `scripts/batch_0360_parse.py`, which hardcodes `"Constitutional Court of Zambia"` and `[YYYY] ZMCC NN` citation defaults — a ZMSC adapter requires explicit Peter approval per BRIEF.md non-negotiable on parser changes. The worker is escalating this rather than implementing it unilaterally.

## Escalation recommendation (5th consecutive tick — strongest yet)

Phase 5 is at a structural standstill. Three non-overlapping unblocks (any ONE of which would resume forward progress):

1. **parser_v0.3.2 vocabulary widening.** Highest yield against existing ZMCC backlog (would address ~70/89 deferred candidates). Adds: declaratory operative verbs ("declares X void"); procedural-refusal patterns ("application is dismissed for lack of jurisdiction", "discontinuance is allowed", "court refused stay"); single-judge composite outcomes ("the single judge declined to grant"); academic-relief patterns ("the declaratory relief was academic"). Subject to Peter approval.

2. **OCR pipeline** for `pdf_extraction_empty_likely_scanned` candidates: zmcc/2021/{14,15}, zmcc/2022/16, zmcc/2025/19. Addresses 4 candidates. Lower yield but parser-orthogonal — would unblock a class that v0.3.2 alone cannot reach. Subject to Peter approval (introduces a new dependency: `tesseract` + a layout-aware OCR wrapper).

3. **ZMSC fresh DESC sweep with explicit parser-baseline extension.** Highest *new-record* potential (likely 8 records/tick at the v0.3.1 success rate observed on ZMSC 2025/26). Requires:
   - explicit approval to fetch ZMSC older years (2024 → 2022 → ...) under the existing budget (5s/req rate limit; max_fetches_per_day=2000);
   - a parser-baseline extension that parameterises `court_full` and citation prefix so v0.3.1 can produce schema-compliant ZMSC records;
   - a decision on whether to leave the 24 v0.5.0-schema ZMSC records as-is (mixed schema) or back-fill them to v0.3.1 schema in a future re-parse pass.

The recommended ordering is **(1) → (3) → (2)**. (1) unblocks the largest existing backlog with zero new fetches. (3) opens fresh territory but requires more co-ordination. (2) is the longest-tail unblock and addresses the smallest cohort.

## Integrity check

Trivial PASS — no records written, schema/registry/hash clauses not exercised.

## B2 sync / SQLite ingestion

- B2 sync deferred to host (rclone not in sandbox).
- SQLite ingestion deferred to host (corpus.sqlite FTS5 malformed-disk-image carry-forward; canonical source remains `records/*.json`).

## Yield

- Records written: 0
- Records deferred: 0
- Fresh fetches: 0
- Cumulative today: ~22/2000 (UTC date still 2026-04-30 at tick start 23:32Z)
- Wall-clock: well under 20-min budget
- Phase 5 progress: 78/100–160 (unchanged)
