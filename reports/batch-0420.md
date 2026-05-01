# Batch 0420 — Phase 5 audit-only no-write idle tick

- **Tick start (UTC):** 2026-05-01T20:34:05Z
- **Phase:** 5 (judgments) — approved+incomplete (worker does not flip approval flags)
- **Outcome:** No fetches. No records written. No records deferred. No mutations to corpus state.
- **Substantive consecutive audit-only ticks:** 45 (b0375..b0383 + b0385..b0420)
- **UTC date 2026-05-01:** 34th substantive tick of the day; today's `cumulative_today=0/2000` (well inside `max_fetches_per_day` budget); no token spend.

## Reparse-first inventory (parser_v0.3.1) — unchanged vs b0386..b0419

- ZMCC: 142 HTML / 141 PDF / 53 records / **89 missing — all 89 already deferred in `gaps.md`** under one of the four locked v0.3.1 reason codes.
- ZMSC: 25 HTML / 24 PDF / 24 records / 0 missing (the residual HTML stem is an index page, non-blocking).
- SCZ pilot: 1 record (Konkola Copper Mines PLC v Attorney General & 2 Ors, Appeal No. 09 of 2024, Mar-2026 coram Musonda DCJ / Kaoma JS / Mutuna JS).
- **Total Phase 5 records:** 78 / target 100–160. No movement.

## gaps.md frequency cross-check (line counts via grep)

- `html_no_summary_pdf_no_match` — 114
- `parser_v0.3.1_judges_no_comma_unhandled` — 14
- `pdf_extraction_empty_likely_scanned` — 10
- `multi_judge_separate_opinions_no_clear_majority_disposition` — 2
- `outcome_not_inferable_under_tightened_policy` — 49 (v0.3.0 historical, retained for audit)
- `parser_v0.3.1_token_unhandled` — 0
- `outcome_inferred_but_detail_unsafe` — 0
- gaps.md unchanged since 2026-04-30T21:40:59Z (commit `61d666e`).

## Integrity (trivial, no-write)

Phase 5 full-set check:

- 78 / 78 unique IDs (no duplicates).
- 78 / 78 provenance-complete (`source_url`, `source_hash`, `fetched_at`, `parser_version` all populated).
- 78 / 78 `source_hash` is a valid `sha256:` + 64-char hex.
- 78 / 78 `source_hash → raw file` resolution OK using a fresh sha256 index over the full `raw/` tree (3203 raw files / 2926 unique sha256 — identical inventory size as b0418/b0419).
- 6 / 6 spot-recompute OK (seed=420).
- 0 unresolved `cited_authorities` / `amended_by` / `repealed_by` / `key_statutes` references (Phase 5 scope).
- By-court split: Constitutional Court of Zambia 53 / Supreme Court of Zambia 25 (= ZMSC 24 + SCZ-pilot 1).

## State of governance gates

`approvals.yaml` unchanged since 2026-04-30T15:36:40Z (commit `b24a938`) — ~28h 57m at this tick start. Phase 5 completion criterion (five consecutive zero-discovery / zero-write substantive ticks) was first fired in batch-0379 and has been re-affirmed every substantive tick since. Per the BRIEF.md non-negotiable on parser changes and the Phase 5 human-only confirmation rule, the worker does not flip `complete: false → true` and continues to log "Phase 5 appears complete, awaiting human confirmation".

The three approvals required to make further Phase 5 progress remain outstanding (recommended order, unchanged):

1. **parser_v0.3.2 vocabulary widening** — to address the 114 `html_no_summary_pdf_no_match` and the 14 `parser_v0.3.1_judges_no_comma_unhandled` deferrals (a single pass would re-classify the addressable subset without consuming any fresh fetch budget).
2. **OCR pipeline approval** — to address the 10 `pdf_extraction_empty_likely_scanned` deferrals (true scanned PDFs; will not yield text under any pure-text extractor).
3. **ZMSC fresh-DESC-sweep approval** — to expand beyond ZMCC into a second ZambiaLII court with smaller per-record review burden; budgets in `approvals.yaml` (2000 fetches/day, 1M tokens/day) remain untouched today.

## Deferrals and host-side work

- **B2 sync** — deferred to host; `rclone` is not in this sandbox. Once the host runs `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`, the 3203 raw files / 2926 unique sha256 inventory will be mirrored.
- **SQLite ingestion** — `corpus.sqlite` carries a long-running FTS5 malformed-disk-image carry-forward; canonical truth remains the `records/*.json` tree and is what every audit reads from. Not blocking Phase 5; will be addressed once the FTS index is rebuilt host-side.
- **Folds in:** the b0419 post-push log lines (`batch-0419 push OK to origin/main`, commit `e3b5f7b`) that landed in `worker.log` / `costs.log` after the b0419 commit was sealed.

## What changed this tick

Nothing. This is the 45th substantive consecutive audit-only no-write idle tick. The worker is in a steady-state loop pending Peter's approvals on (1) parser_v0.3.2 widening, (2) OCR pipeline, (3) ZMSC fresh sweep.
