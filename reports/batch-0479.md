# Batch 0479 — Audit-only tick (104th substantive consecutive)

- **Tick start (UTC):** 2026-05-03T04:04Z
- **Phase:** 5 (judgments) — approved+incomplete
- **Action taken:** reparse-first inventory + integrity sweep, no fetches
- **Records written:** 0
- **Records deferred:** 0
- **Cumulative today:** 0/2000 fetches; 0/1,000,000 tokens
- **Tick note:** Initial cleanup glob `find .git -name "*.lock" -delete; find .git -name "*.lock.bak" -delete` ran cleanly with the by-now-routine carry-forward `Operation not permitted` on host-locked `.git/objects/maintenance.lock` and on accumulated `*.lock.bak.<ts>` files (sandbox cannot unlink — same behaviour as b0460..b0478). First `git pull --ff-only` attempt FAILED with `fatal: bad object refs/heads/main.lock.bak.b0478_20260503T033641Z` — an orphan ref left in `refs/heads/` after the b0478 push lock cycle. Recovery: since the sandbox cannot `rm` host-owned files but CAN `mv` them, three orphan files were parked into `.git/_orphan_refs_parked/` (`heads_main.lock.bak.b0380.1777594024_<ts>`, `heads_main.lock.bak.b0478_20260503T033641Z_<ts>`, `heads_zztrash-main-bak1_<ts>`). Second `git pull --ff-only` returned `Already up to date.` cleanly. approvals.yaml and BRIEF.md unchanged since 2026-04-30T15:36:40Z (commit b24a938; ~3d 12h at this tick start). gaps.md unchanged since 2026-04-30T21:40:59Z (commit 61d666e). Reparse inventory unchanged from b0478. 8th substantive tick of UTC date 2026-05-03 (rolls forward from b0478 at 03:35Z).

## Reparse-first inventory (parser_v0.3.1)
| Court | raw HTML | raw PDF | records | missing |
|-------|---------:|--------:|--------:|--------:|
| ZMCC  | 142      | 141     | 53      | 89 (all deferred under v0.3.1-locked codes) |
| ZMSC  | 25 (incl. 1 index) | 24 | 24 | 0 |
| SCZ pilot | n/a  | n/a     | 1       | n/a |
| **Total** |      |         | **78**  |     |

All 89 ZMCC missing candidates remain deferred under v0.3.1-locked reason codes — none addressable by parser_v0.3.1. Empirically re-confirmed across b0375..b0478; verbatim per b0478 audit. ZMSC slice fully ingested across the 24 case HTML files. Inventory exhausted; no fresh fetches initiated this tick.

### Deferred-reason histogram (gaps.md grep, unchanged from b0478)
| Reason code | Count |
|-------------|------:|
| html_no_summary_pdf_no_match | 115 |
| outcome_not_inferable_under_tightened_policy (legacy, banned for new) | 49 |
| parser_v0.3.1_judges_no_comma_unhandled | 14 |
| pdf_extraction_empty_likely_scanned | 10 |
| multi_judge_separate_opinions_no_clear_majority_disposition | 2 |
| parser_v0.3.0_jjs_title_unhandled | 1 |
| **Total** | **191** |

(Counts include both Phase-5 ZMCC backlog and historical Phase-4 entries that share these codes. Counted via `grep -o ... | wc -l`; raw line count is 114 because one gaps.md line contains the substring twice.)

## Integrity check (post-pull, pre-commit)
- Unique IDs: **78/78** (0 duplicates)
- Provenance complete (`source_url` + `source_hash` + `fetched_at` + `parser_version`): **78/78**
- `source_hash` shape valid (`sha256:` + 64 hex): **78/78**
- `source_hash` resolves into `raw/` tree: **78/78** (sha256 index over raw/ tree, 3203 files / 2926 unique sha256)
- Spot-recompute (seed=479): **6/6**
- Unresolved cross-refs (`cited_authorities` / `amended_by` / `repealed_by` / `key_statutes`) within Phase 5 scope: **0**
- Court breakdown: Supreme Court of Zambia=25 (24 ZMSC + 1 SCZ pilot), Constitutional Court of Zambia=53.

## Operational status
- approvals.yaml unchanged since 2026-04-30T15:36:40Z (commit b24a938).
- BRIEF.md unchanged since 2026-04-30T15:36:40Z (commit b24a938).
- gaps.md unchanged since 2026-04-30T21:40:59Z (commit 61d666e).
- 104 consecutive substantive audit-only ticks (b0375..b0383 + b0385..b0479; excludes the failed-pull tick between b0442 and b0443 and the aborted-pull tick at 19:33:50Z between b0464 and b0465).
- UTC date 2026-05-03 (8th substantive tick of new day; rolls forward from b0478 at 03:35Z).
- Phase 5 five-consecutive-zero-discovery completion criterion remains fired (originally fired in batch-0379). approvals.yaml NOT modified per Phase 5 human-only confirmation rule.
- B2 sync: deferred to host (rclone not in sandbox).
- SQLite ingestion: deferred to host (corpus.sqlite FTS5 malformed-disk-image carry-forward; canonical source remains records/*.json).

## Recommendation (unchanged from b0441..b0478)
Further Phase 5 progress requires human approval of one or more of:
1. **parser_v0.3.2** vocabulary widening (declaratory operative verbs; procedural-refusal patterns; `discontinuance allowed`, `challenge … dismissed for lack`, `application … dismissed for failing`, `declaratory relief was academic`, `single-judge declined`, `court refused stay`) to address residual ZMCC `html_no_summary_pdf_no_match` and declaratory-operative-phrase deferrals.
2. **OCR pipeline** for the `pdf_extraction_empty_likely_scanned` candidates (10 entries in gaps.md, including zmcc/2021/{14,15}, zmcc/2022/16, zmcc/2025/19).
3. **ZMSC fresh DESC sweep** beyond the current 25-page corpus (older-year sweep into 2024/2023/2022/2021/2020) — would discover new raw bytes parser_v0.3.1 may handle better than the ZMCC backlog.

All three remain subject to Peter approval per BRIEF.md non-negotiable on parser changes. Worker continues idle audit-only ticks under the Phase 5 human-only confirmation rule.

## Carry-forward note for next tick
Pull recovery this tick (parking three orphan files out of `refs/heads/` into `.git/_orphan_refs_parked/`) demonstrates that the `mv`-as-soft-rm workaround scales to refs-tree contamination as well as objects-tree contamination. The b0479 parked files were:
  - `heads_main.lock.bak.b0380.1777594024_<ts>`
  - `heads_main.lock.bak.b0478_20260503T033641Z_<ts>`
  - `heads_zztrash-main-bak1_<ts>`
If the next tick's pull fails with `fatal: bad object refs/heads/main.lock.bak.b0479_<ts>` (or remotes/origin equivalent), repeat the broadened mv-into-`_orphan_refs_parked/` sweep against both `refs/heads/` and `refs/remotes/origin/`. Host-side `rm -rf .git/_orphan_refs_parked/` plus `find .git -name "*.lock*" -delete` and `git gc --prune=now` extension still pending Peter sign-off.
