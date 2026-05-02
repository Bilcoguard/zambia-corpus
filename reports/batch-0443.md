# Batch 0443 — Audit-only tick

- **Tick start (UTC):** 2026-05-02T08:44Z
- **Phase:** 5 (judgments) — approved+incomplete
- **Action taken:** reparse-first inventory + integrity sweep, no fetches
- **Records written:** 0
- **Records deferred:** 0
- **Cumulative today:** 0/2000 fetches
- **Tick note:** prior tick (b0442-followup) failed at `git pull` with stale `.git/refs/remotes/origin/main.lock.*` files left behind by upstream maintenance. Host-side cleanup completed by Peter (`chflags -R nouchg .git` + `rm -f .git/refs/remotes/origin/main.lock.* .git/objects/maintenance.lock`). Pull is clean again as of this tick.

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
- Spot-recompute (seed=443): **6/6**
  - judgment-zm-2023-zmcc-07-zulu-v-chilufya-and-ors: OK
  - judgment-zm-2021-zmcc-16-sampa-v-mundubile-and-anor: OK
  - judgment-zm-2025-zmcc-01-dr-godfrey-hampwaya-and-ors-v-the-council-of-the-u: OK
  - judgment-zm-2025-zmcc-29-law-association-of-zambia-and-ors-v-attorney-gener: OK
  - judgment-zm-2025-zmcc-04-brenda-mpashi-v-attorney-general-and-anor: OK
  - judgment-zm-2022-zmcc-29-chisanga-v-chisopa-and-anor: OK
- Unresolved cross-refs (`cited_authorities` / `amended_by` / `repealed_by` / `key_statutes`) within Phase 5 scope: **0**
- Court breakdown: ZMCC=53, ZMSC=24, SCZ-pilot=1.

## Operational status
- approvals.yaml unchanged since 2026-04-30T15:36:40Z (commit b24a938; ~1d 21h at this tick start).
- gaps.md unchanged since 2026-04-30T21:40:59Z (commit 61d666e).
- 68 consecutive substantive audit-only ticks (b0375..b0383 + b0385..b0443; excludes failed-pull tick between b0442 and b0443).
- UTC date 2026-05-02 (15th substantive tick of new day).
- Phase 5 five-consecutive-zero-discovery completion criterion remains fired (originally fired in batch-0379). approvals.yaml NOT modified per Phase 5 human-only confirmation rule.
- B2 sync: deferred to host (rclone not in sandbox).
- SQLite ingestion: deferred to host (corpus.sqlite FTS5 malformed-disk-image carry-forward; canonical source remains records/*.json).

## Recommendation (unchanged from b0441/b0442)
Further Phase 5 progress requires human approval of one or more of:
1. **parser_v0.3.2** vocabulary widening (to address residual ZMCC `html_no_summary_pdf_no_match` and declaratory-operative-phrase deferrals).
2. **OCR pipeline** for `pdf_extraction_empty_likely_scanned` candidates.
3. **ZMSC fresh DESC sweep** beyond the current 25-page corpus.

All three are subject to Peter approval per BRIEF.md non-negotiable on parser changes. Worker continues idle audit-only ticks under the Phase 5 human-only confirmation rule.
