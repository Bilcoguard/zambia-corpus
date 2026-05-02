# Batch 0444 — Audit-only tick

- **Tick start (UTC):** 2026-05-02T09:04Z
- **Phase:** 5 (judgments) — approved+incomplete
- **Action taken:** reparse-first inventory + integrity sweep, no fetches
- **Records written:** 0
- **Records deferred:** 0
- **Cumulative today:** 0/2000 fetches
- **Tick note:** clean tick — `git pull --ff-only` reports `Already up to date.` (host-side stale-lock cleanup applied at b0443 still holding). No new approvals.yaml or BRIEF.md amendments since b0443; reparse inventory unchanged.

## Reparse-first inventory (parser_v0.3.1)
| Court | raw HTML | raw PDF | records | missing |
|-------|---------:|--------:|--------:|--------:|
| ZMCC  | 142      | 141     | 53      | 89 (all deferred under v0.3.1) |
| ZMSC  | 25 (incl. 1 index) | 24 | 24 | 0 |
| SCZ pilot | n/a  | n/a     | 1       | n/a |
| **Total** |      |         | **78**  |     |

All 89 ZMCC missing candidates remain deferred under specific reason codes — none addressable by parser_v0.3.1. ZMSC slice fully ingested across the 24 case HTML files (the 25th is the listing index page). Inventory exhausted; no fresh fetches initiated this tick.

## Integrity check
- Unique IDs: **78/78** (0 duplicates)
- Provenance complete (`source_url` + `source_hash` + `fetched_at` + `parser_version`): **78/78**
- `source_hash` shape valid (`sha256:` + 64 hex): **78/78**
- `source_hash` resolves into `raw/` tree: **78/78** (sha256 index over 3203 files / 2926 unique sha256)
- Spot-recompute (seed=444): **6/6**
  - judgment-zm-2025-zmcc-27-munir-zuu-and-anor-v-attorney-general-and-ors: OK
  - judgment-zm-2025-zmcc-31-munir-zulu-and-anor-v-attorney-general-and-ors: OK
  - judgment-zm-2025-zmsc-17-ronald-v-anti: OK
  - judgment-zm-2021-zmcc-22-bozy-simutanda-as-attorney-for-his-royal-highness: OK
  - judgment-zm-2026-zmcc-07-climate-action-professionals-zambia-v-attorney-gen: OK
  - judgment-zm-2025-zmcc-23-emmanuel-kayuni-suing-as-administrator-of-the-esta: OK
- Unresolved cross-refs (`cited_authorities` / `amended_by` / `repealed_by` / `key_statutes`) within Phase 5 scope: **0**
- Court breakdown: ZMCC=53, ZMSC=24, SCZ-pilot=1.

## Operational status
- approvals.yaml unchanged since 2026-04-30T15:36:40Z (commit b24a938; ~1d 21h 28m at this tick start).
- gaps.md unchanged since 2026-04-30T21:40:59Z (commit 61d666e).
- 69 consecutive substantive audit-only ticks (b0375..b0383 + b0385..b0444; excludes the failed-pull tick between b0442 and b0443).
- UTC date 2026-05-02 (16th substantive tick of new day).
- Phase 5 five-consecutive-zero-discovery completion criterion remains fired (originally fired in batch-0379). approvals.yaml NOT modified per Phase 5 human-only confirmation rule.
- B2 sync: deferred to host (rclone not in sandbox).
- SQLite ingestion: deferred to host (corpus.sqlite FTS5 malformed-disk-image carry-forward; canonical source remains records/*.json).

## Recommendation (unchanged from b0441/b0442/b0443)
Further Phase 5 progress requires human approval of one or more of:
1. **parser_v0.3.2** vocabulary widening (to address residual ZMCC `html_no_summary_pdf_no_match` and declaratory-operative-phrase deferrals).
2. **OCR pipeline** for `pdf_extraction_empty_likely_scanned` candidates.
3. **ZMSC fresh DESC sweep** beyond the current 25-page corpus.

All three are subject to Peter approval per BRIEF.md non-negotiable on parser changes. Worker continues idle audit-only ticks under the Phase 5 human-only confirmation rule.
