# Batch 0431 Report — Phase 5 Audit-Only Idle Tick (56th consecutive)

**Tick start (UTC):** 2026-05-02T02:04:00Z
**Phase:** 5 (judgments) — approved=true, complete=false
**Batch number:** 0431
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
- 6/6 spot-recompute samples recomputed cleanly (seed=431).
- 0 unresolved internal references across `cited_authorities` / `amended_by` / `repealed_by` / `key_statutes` (Phase 5 scope).
- Court breakdown of records: ZMCC=53, ZMSC=24, SCZ pilot=1 — matches b0430.

**Result:** PASS.

## Gaps inventory (snapshot)

`gaps.md` is unchanged since 2026-04-30T21:40:59Z (commit `61d666e`, ~28h 23m at tick start; sha256 `6cfc1bf4a61ed78e99cc2714041ac8dbc34b51485cf7636a0df1926dee663820`, 223,367 bytes). The 89 distinct ZMCC deferrals continue to be distributed across the locked-in specific reason codes. Substring-count of reason tokens in `gaps.md` (some entries reference the same code multiple times):

- 115 `html_no_summary_pdf_no_match`
- 14 `parser_v0.3.1_judges_no_comma_unhandled`
- 10 `pdf_extraction_empty_likely_scanned`
- 2 `multi_judge_separate_opinions_no_clear_majority_disposition`
- 0 `parser_v0.3.1_token_unhandled`
- 0 `outcome_inferred_but_detail_unsafe`

(Substring counts pick up multiple-token references on a single line; the count of distinct deferred candidates remains 89, all ZMCC.)

## Approvals state

`approvals.yaml` is unchanged since 2026-04-30T15:36:40Z (commit `b24a938`, ~34h 28m at tick start; sha256 `6e04c9ca876cd678fee273cd27d28d0a88506ddbe1624b46d1e6868cc4735e1a`, 3,027 bytes). The worker has therefore had no further Phase 5 work to do for 56 consecutive substantive ticks (b0375..b0383, b0385..b0431).

The three open items continue to require Peter's review before progress can resume:

1. **parser_v0.3.2 vocabulary widening** — to address the 14 ZMCC candidates currently deferred under `parser_v0.3.1_judges_no_comma_unhandled`, plus widen `PDF_TAIL_PATTERNS` for the 115/89 `html_no_summary_pdf_no_match` candidates.
2. **OCR pipeline** — to address the 10 `pdf_extraction_empty_likely_scanned` ZMCC candidates whose final pages defeat pdfplumber.
3. **ZMSC fresh DESC sweep approval** — to extend coverage beyond the 24 ZMSC records currently on disk.

All three are subject to Peter approval per the BRIEF.md non-negotiable on parser changes and the Phase 5 human-only confirmation rule.

## Side-effects

- `worker.log`, `costs.log`, `provenance.log`, and this report were written.
- `corpus.sqlite` FTS5 ingestion remained deferred to the host (malformed-disk-image carry-forward; canonical source remains `records/*.json`).
- B2 sync deferred to the host (rclone not present in this sandbox).
- `approvals.yaml` was **not** modified.
- `gaps.md` was **not** modified (no new deferrals, no resolutions).

## Next tick

Continues to be governed by `approvals.yaml`. If Peter has flipped any of the three pending items by then, the tick will pick up the corresponding work. Otherwise the worker will perform another audit-only confirmation. The 20-minute wall-clock budget for this tick was respected (audit-only path; ~5s of Python + a handful of git commands).
