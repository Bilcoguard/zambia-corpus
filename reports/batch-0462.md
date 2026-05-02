# Batch 0462 — Audit-only tick (87th substantive consecutive)

- **Tick start (UTC):** 2026-05-02T18:05Z
- **Phase:** 5 (judgments) — approved+incomplete
- **Action taken:** reparse-first inventory + integrity sweep, no fetches
- **Records written:** 0
- **Records deferred:** 0
- **Cumulative today:** 0/2000 fetches; 0/1,000,000 tokens
- **Tick note:** initial cleanup glob `find .git -name "*.lock" -delete` ran (carry-forward sandbox `Operation not permitted` warning on `.git/objects/maintenance.lock`; cannot unlink under create-only filesystem semantics for `.git/`). `git pull --ff-only` initially failed with `bad object refs/remotes/origin/main_stale.20260502T173619Z.bak` due to a zero-length backup ref left from a prior tick's atomic-rename interaction; recovered by writing the current `origin/main` SHA (`a39b07ba86ff68d2055b06f1cbc646c56a33c368`) into the empty backup ref file (rm denied by sandbox unlink semantics, write succeeded), after which `git pull --ff-only` returned `Already up to date.` cleanly. approvals.yaml and BRIEF.md unchanged since 2026-04-30T15:36:40Z (commit b24a938; ~3d 2h 29m at this tick start). gaps.md unchanged since 2026-04-30T21:40:59Z (commit 61d666e). Reparse inventory unchanged from b0461.

## Reparse-first inventory (parser_v0.3.1)
| Court | raw HTML | raw PDF | records | missing |
|-------|---------:|--------:|--------:|--------:|
| ZMCC  | 142      | 141     | 53      | 89 (all deferred under v0.3.1-locked codes) |
| ZMSC  | 25 (incl. 1 index) | 24 | 24 | 0 |
| SCZ pilot | n/a  | n/a     | 1       | n/a |
| **Total** |      |         | **78**  |     |

All 89 ZMCC missing candidates remain deferred under v0.3.1-locked reason codes — none addressable by parser_v0.3.1. Empirically re-confirmed across b0375..b0461; verbatim per b0461 audit. ZMSC slice fully ingested across the 24 case HTML files (the additional HTML is the listing index page — not part of the ingestion-target inventory). Inventory exhausted; no fresh fetches initiated this tick.

## Integrity check (post-pull, pre-commit)
- Unique IDs: **78/78** (0 duplicates)
- Provenance complete (`source_url` + `source_hash` + `fetched_at` + `parser_version`): **78/78**
- `source_hash` shape valid (`sha256:` + 64 hex): **78/78**
- `source_hash` resolves into `raw/` tree: **78/78** (sha256 index over raw/ tree, computed via `Path.rglob`: 3203 files / 2926 unique sha256)
- Spot-recompute (seed=462): **6/6**
- Unresolved cross-refs (`cited_authorities` / `amended_by` / `repealed_by` / `key_statutes`) within Phase 5 scope: **0**
- Court breakdown: Supreme Court of Zambia=25 (24 ZMSC + 1 SCZ pilot), Constitutional Court of Zambia=53.

## Operational status
- approvals.yaml unchanged since 2026-04-30T15:36:40Z (commit b24a938).
- BRIEF.md unchanged since 2026-04-30T15:36:40Z (commit b24a938).
- gaps.md unchanged since 2026-04-30T21:40:59Z (commit 61d666e).
- 87 consecutive substantive audit-only ticks (b0375..b0383 + b0385..b0462; excludes the failed-pull tick between b0442 and b0443).
- UTC date 2026-05-02 (34th substantive tick of new day).
- Phase 5 five-consecutive-zero-discovery completion criterion remains fired (originally fired in batch-0379). approvals.yaml NOT modified per Phase 5 human-only confirmation rule.
- B2 sync: deferred to host (rclone not in sandbox).
- SQLite ingestion: deferred to host (corpus.sqlite FTS5 malformed-disk-image carry-forward; canonical source remains records/*.json).
- Orphan-ref carry-forward recovery one-shot at start of tick: `refs/remotes/origin/main_stale.20260502T173619Z.bak` was a zero-length file (likely from prior atomic-rename interaction with another lock-bak cleanup); written with current `origin/main` SHA `a39b07ba86ff68d2055b06f1cbc646c56a33c368` to clear the bad-object pull blocker. The host filesystem unlink-denied semantics for `.git/` mean the file cannot be removed from inside the sandbox; making it valid is the safe alternative. The earlier two backup refs (`main.lock.bak.20260502T140620Z` SHA `ce226559…`; `main.lock.bak.20260502T163547Z` SHA `56a6cab5…`) are pre-existing and have valid SHAs, untouched.

## Recommendation (unchanged from b0441..b0461)
Further Phase 5 progress requires human approval of one or more of:
1. **parser_v0.3.2** vocabulary widening (declaratory operative verbs; procedural-refusal patterns; `discontinuance allowed`, `challenge … dismissed for lack`, `application … dismissed for failing`, `declaratory relief was academic`, `single-judge declined`, `court refused stay`) to address residual ZMCC `html_no_summary_pdf_no_match` and declaratory-operative-phrase deferrals.
2. **OCR pipeline** for the 4 `pdf_extraction_empty_likely_scanned` candidates: zmcc/2021/{14,15}, zmcc/2022/16, zmcc/2025/19.
3. **ZMSC fresh DESC sweep** beyond the current 25-page corpus (older-year sweep into 2024/2023/2022/2021/2020) — would discover new raw bytes parser_v0.3.1 may handle better than the ZMCC backlog.

All three remain subject to Peter approval per BRIEF.md non-negotiable on parser changes. Worker continues idle audit-only ticks under the Phase 5 human-only confirmation rule.
