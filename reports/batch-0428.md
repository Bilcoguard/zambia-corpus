# Batch 0428 Report — Phase 5 Audit-Only Idle Tick (53rd consecutive)

**Tick start (UTC):** 2026-05-02T00:34:13Z
**Phase:** 5 (judgments) — approved=true, complete=false
**Batch number:** 0428
**Outcome:** audit-only, no writes, no fresh fetches, no records added or deferred

## Reparse-first sweep (zero fetch budget)

| Source | raw HTML | raw PDF | records | missing | status |
|---|---:|---:|---:|---:|---|
| ZMCC | 142 | 141 | 53 | 89 | all 89 already deferred under specific reason codes (locked-in 2026-04-30) |
| ZMSC | 25 | 24 | 24 | 0 | exhausted under v0.3.1 |
| SCZ pilot | — | — | 1 | — | retained from Phase 3 |
| **Total** | | | **78** | | reparse inventory **exhausted** under parser_v0.3.1 |

No addressable v0.3.1 deferreds remained. No fresh DESC-sweep fetches were authorised because the BRIEF.md five-consecutive-zero-discovery completion criterion has been fired since b0379. `approvals.yaml` has not been edited (human-only confirmation rule).

## Integrity check (full corpus, Phase 5 scope)

- 78/78 unique record IDs (no duplicates).
- 78/78 records carry the four mandatory provenance fields (`source_url`, `source_hash`, `fetched_at`, `parser_version`).
- 78/78 `source_hash` values match the `^sha256:[0-9a-f]{64}$` shape.
- 78/78 `source_hash` values resolve into the raw/ tree (sha256 index built over 3203 raw files / 2926 unique sha256 digests, full os.walk recount).
- 6/6 spot-recompute samples recomputed cleanly (seed=428).
- 0 unresolved internal references across `cited_authorities` / `amended_by` / `repealed_by` / `key_statutes` (Phase 5 scope).
- Court breakdown of records: ZMCC=53, ZMSC=24, SCZ pilot=1 — matches b0427.

**Result:** PASS.

## Gaps inventory (snapshot)

`gaps.md` is unchanged since 2026-04-30T21:40:59Z (commit `61d666e`, ~26h 53m at tick start). The 89 ZMCC deferrals are still distributed across the locked-in specific reason codes:

- 114 `html_no_summary_pdf_no_match`
- 14 `parser_v0.3.1_judges_no_comma_unhandled`
- 10 `pdf_extraction_empty_likely_scanned`
- 2 `multi_judge_separate_opinions_no_clear_majority_disposition`

(Note: total 140 deferral lines — multiple lines per candidate where appropriate; 89 distinct candidates.)

## Approvals state

`approvals.yaml` is unchanged since 2026-04-30T15:36:40Z (commit `b24a938`, ~32h 57m at tick start). The worker has therefore had no further Phase 5 work to do for 53 consecutive substantive ticks (b0375..b0383, b0385..b0428).

The three open items continue to require Peter's review before progress can resume:

1. **parser_v0.3.2 vocabulary widening** — to address the 14 ZMCC candidates currently deferred under `parser_v0.3.1_judges_no_comma_unhandled`, plus widen `PDF_TAIL_PATTERNS` for the 114 `html_no_summary_pdf_no_match` candidates.
2. **OCR pipeline** — to address the 10 `pdf_extraction_empty_likely_scanned` ZMCC candidates whose final pages defeat pdfplumber.
3. **ZMSC fresh DESC sweep approval** — to extend coverage beyond the 24 ZMSC records currently on disk.

All three are subject to Peter approval per the BRIEF.md non-negotiable on parser changes and the Phase 5 human-only confirmation rule.

## Side-effects

- `worker.log`, `costs.log`, and this report were written.
- `corpus.sqlite` FTS5 ingestion remained deferred to the host (malformed-disk-image carry-forward).
- B2 sync deferred to the host (rclone not present in this sandbox).
- `approvals.yaml` was **not** modified.
- `gaps.md` was **not** modified (no new deferrals, no resolutions).

## Next tick

Continues to be governed by `approvals.yaml`. If Peter has flipped any of the three pending items by then, the tick will pick up the corresponding work. Otherwise the worker will perform another audit-only confirmation. The 20-minute wall-clock budget for this tick was respected (audit-only path; ~5s of Python + a handful of git commands).
