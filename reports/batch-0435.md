# Batch 0435 Report — Phase 5 Audit-Only Idle Tick (60th consecutive)

**Tick start (UTC):** 2026-05-02T04:35:27Z
**Phase:** 5 (judgments) — approved=true, complete=false
**Batch number:** 0435
**Outcome:** audit-only, no writes, no fresh fetches, no records added or deferred

## Tick recovery note

The 04:03:45Z tick attempt aborted before any work because of a stale empty-broken ref left in `.git/refs/remotes/origin/main.lock.bak.20260502T033556Z` (and a matching `.lock` file). The ref was created during the b0434 push (the timestamped `.lock.bak.<ts>` filename pattern post-dates the worker's standard `find .git -name "*.lock.bak" -delete` cleanup, which only matches the bare-suffix form). Both files were created with mode 0600 owned by the sandbox uid but the FUSE bindfs mount on this sandbox refused removal at the syscall layer (`Operation not permitted`). The b0435 tick recovered by overwriting the empty broken ref with the canonical `origin/main` SHA (`0daaf76801d189b9112e00d4a3b71b82aa2d40d0`), which made it a valid ref and unblocked `git pull --ff-only`. The orphan ref will be cleaned up by the host on the next regular maintenance pass; the in-band hostside cleanup commands suggested in the 04:03:45Z worker.log entry remain valid. **Recommendation (carry-forward):** extend the FIRST-step lock cleanup glob in the tick instructions to include `*.lock.bak.*` (timestamped form) in addition to the bare `*.lock.bak` form so this class of stale ref does not block future `git pull --ff-only`.

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
- 6/6 spot-recompute samples recomputed cleanly (seed=435).
- 0 unresolved internal references across `cited_authorities` / `amended_by` / `repealed_by` / `key_statutes` (Phase 5 scope).
- Court breakdown of records: ZMCC=53, ZMSC=24, SCZ pilot=1 — matches b0434.

**Result:** PASS.

## Gaps inventory (snapshot)

`gaps.md` is unchanged since 2026-04-30T21:40:59Z (commit `61d666e`, ~1d 6h 54m at tick start; sha256 `6cfc1bf4a61ed78e99cc2714041ac8dbc34b51485cf7636a0df1926dee663820`, 223,367 bytes). The 89 distinct ZMCC deferrals continue to be distributed across the locked-in specific reason codes. Substring-count of reason tokens in `gaps.md` (some entries reference the same code multiple times):

- 115 `html_no_summary_pdf_no_match`
- 14 `parser_v0.3.1_judges_no_comma_unhandled`
- 10 `pdf_extraction_empty_likely_scanned`
- 2 `multi_judge_separate_opinions_no_clear_majority_disposition`
- 0 `parser_v0.3.1_token_unhandled`
- 0 `outcome_inferred_but_detail_unsafe`

(Substring counts pick up multiple-token references on a single line; the count of distinct deferred candidates remains 89, all ZMCC.)

## Approvals state

`approvals.yaml` is unchanged since 2026-04-30T15:36:40Z (commit `b24a938`, ~1d 12h 58m at tick start; sha256 `6e04c9ca876cd678fee273cd27d28d0a88506ddbe1624b46d1e6868cc4735e1a`, 3,027 bytes). The worker has therefore had no further Phase 5 work to do for 60 consecutive substantive ticks (b0375..b0383, b0385..b0435).

The three open items continue to require Peter's review before progress can resume:

1. **parser_v0.3.2 vocabulary widening** — to address the 14 ZMCC candidates currently deferred under `parser_v0.3.1_judges_no_comma_unhandled`, plus widen `PDF_TAIL_PATTERNS` for the 115/89 `html_no_summary_pdf_no_match` candidates.
2. **OCR pipeline** — to address the 10 `pdf_extraction_empty_likely_scanned` ZMCC candidates whose final pages defeat pdfplumber.
3. **ZMSC fresh DESC sweep approval** — to extend coverage beyond the 25 ZMSC HTML / 24 ZMSC PDF / 24 records currently on disk.

All three are subject to Peter approval per the BRIEF.md non-negotiable on parser changes and the Phase 5 human-only confirmation rule.

## Side-effects

- `worker.log`, `costs.log`, `provenance.log`, and this report were written. The b0434 post-push log lines (which were staged but never committed because the 04:03:45Z tick aborted before reaching the commit step) are folded into this commit so the audit trail stays continuous.
- `corpus.sqlite` FTS5 ingestion remained deferred to the host (malformed-disk-image carry-forward; canonical source remains `records/*.json`).
- B2 sync deferred to the host (rclone not present in this sandbox).
- `approvals.yaml` was **not** modified.
- `gaps.md` was **not** modified (no new deferrals, no resolutions).

## Next tick

Continues to be governed by `approvals.yaml`. If Peter has flipped any of the three pending items by then, the tick will pick up the corresponding work. Otherwise the worker will perform another audit-only confirmation. The 20-minute wall-clock budget for this tick was respected (audit-only path; ~7s of Python + a handful of git commands; with the b0434-orphan-ref recovery overhead of about 4 minutes).
