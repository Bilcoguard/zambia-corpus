# Batch 0499 — Audit-only tick (1st post-v0.3.2-exhaustion)

- **Tick start (UTC):** 2026-05-03T14:33Z
- **Tick end (UTC):** 2026-05-03T14:36Z
- **Phase:** 5 (judgments) — approved+incomplete
- **Action taken:** reparse-first inventory + integrity sweep, no fetches
- **Records written:** 0
- **Records deferred:** 0 (no new attempts; inventory already exhausted under v0.3.2 per b0498)
- **Cumulative today:** 0/2000 fetches; 0/1,000,000 tokens
- **Tick note:** First audit-only zero-yield tick after the v0.3.2 reparse-first inventory was declared FORMALLY EXHAUSTED across all ZMCC years (2021..2026) at b0498. Returns the worker to the b0375..b0487 idle pattern under the post-exhaustion regime. Initial cleanup glob `find .git -name "*.lock" -delete; find .git -name "*.lock.bak" -delete` ran cleanly; carry-forward `Operation not permitted` on host-locked `.git/objects/maintenance.lock` continues (sandbox cannot unlink — same behaviour as b0460..b0498; not blocking). `git pull --ff-only` returned `Already up to date.` cleanly on first try this tick (8th consecutive clean pull including b0488..b0498 substantive ticks). approvals.yaml unchanged since 2026-05-03T (commit 09eafb0; b0488 v0.3.2 launch). gaps.md last touched at b0498 commit 1392880 (2026-05-03T14:13:58Z). 18th substantive tick of UTC date 2026-05-03 (rolls forward from b0498 at 14:14:12Z).

## Reparse-first inventory (parser_v0.3.2)

| Court | raw HTML | raw PDF | records | missing |
|-------|---------:|--------:|--------:|--------:|
| ZMCC  | 142      | ~141    | 72      | 70 (all deferred under v0.3.2-locked codes) |
| ZMSC  | 25 (incl. 1 index) | 24 | 24 | 0 |
| SCZ pilot | n/a  | n/a     | 1       | n/a |
| **Total** |      |         | **97**  |     |

The 70 ZMCC missing candidates have all been re-tested under parser_v0.3.2 across b0488..b0498 (cumulative attempts = 79; written = 19; deferred = 60; carried-forward-from-v0.3.1-deferred = 10). All 70 remain deferred under v0.3.2-locked reason codes — none addressable by the current parser. Inventory exhausted; no fresh fetches initiated this tick.

The 4 `pdf_extraction_empty_likely_scanned` candidates (zmcc/2021/14, zmcc/2021/15, zmcc/2022/16, zmcc/2025/19) are OCR-required and remain out of reach of any parser-only widening.

The ZMSC slice remains fully ingested across the 24 case HTML files. Older-year ZMSC sweep is approved (`zmsc_older_year_sweep_approved: true`, 2026-05-03) but gated on Peter confirming the canonical source URL pattern; not actionable by scheduled tick until that confirmation lands.

### Deferred-reason histogram (gaps.md grep, post-b0498)

| Reason code | Count |
|-------------|------:|
| html_no_summary_pdf_no_match | 190 |
| outcome_not_inferable_under_tightened_policy (legacy, banned for new) | 49 |
| parser_v0.3.1_judges_no_comma_unhandled (legacy) | 16 |
| pdf_extraction_empty_likely_scanned | 15 |
| multi_judge_separate_opinions_no_clear_majority_disposition | 4 |
| parser_v0.3.0_jjs_title_unhandled (legacy) | 1 |
| parser_v0.3.1_token_unhandled (legacy) | 0 |
| parser_v0.3.2_token_unhandled | 0 |
| outcome_inferred_but_detail_unsafe | 0 |
| canonical_url_date_unrecoverable | 0 |
| **Total occurrences** | **275** |

(Counts via `re.findall` over gaps.md content. Total occurrences include RECONFIRMED-DEFERRED notes appended across multiple ticks for the same candidate; raw candidate count remains 70 ZMCC raw-on-disk-no-record + 4 `pdf_extraction_empty_likely_scanned` overlapping subset.)

## Integrity check (post-pull, pre-commit) — Phase 5 scope

- Unique IDs: **97/97** (0 duplicates)
- Provenance complete (`source_url` + `source_hash` + `fetched_at` + `parser_version`): **97/97**
- `source_hash` shape valid (`sha256:` + 64 hex): **97/97**
- `source_hash` resolves into `raw/` tree: **97/97** (sha256 index over raw/ tree, 3203 files / 2926 unique sha256)
- Spot-recompute (seed=499, 6 records sampled): **6/6 PASS**
- Unresolved cross-refs (`cited_authorities` / `amended_by` / `repealed_by`) within Phase 5 scope: **0**
- Court breakdown: Supreme Court of Zambia=25 (24 ZMSC + 1 SCZ pilot), Constitutional Court of Zambia=72.

### parser_version histogram (Phase 5 scope, post-tick)

| parser_version | records |
|----------------|--------:|
| 0.5.0 | 24 |
| 0.3.1 | 23 |
| 0.3.0 | 21 |
| 0.3.2 | 19 |
| 0.2.0 | 10 |
| **Total** | **97** |

(Records written before parser_v0.3.2 launch retain their original parser_version stamp per BRIEF.md provenance non-negotiable; none are re-stamped on later ticks.)

## Operational status

- approvals.yaml unchanged since commit 09eafb0 (2026-05-03 b0488 — parser_v0.3.2 launch + ZMSC older-year sweep approval pending URL confirmation).
- BRIEF.md unchanged since commit b24a938 (2026-04-30 — parser_v0.3.1 lock-in + reparse-first policy).
- gaps.md last touched at commit 1392880 (2026-05-03T14:13:58Z, b0498 RECONFIRMED-DEFERRED + RESOLVED notes).
- 1 audit-only zero-yield tick this run (b0499). Five-consecutive-zero-discovery counter at **1** (resets on next non-zero tick).
- UTC date 2026-05-03 (18th substantive tick of new day; rolls forward from b0498 at 14:14:12Z).
- Phase 5 progress 97/100-160 (3 short of low end of approved target). approvals.yaml NOT modified per Phase 5 human-only confirmation rule.
- B2 sync: deferred to host (rclone not in sandbox).
- SQLite ingestion: deferred to host (corpus.sqlite FTS5 malformed-disk-image carry-forward since b0474; canonical source remains records/*.json).

## v0.3.2 yield summary (b0488..b0498, frozen at b0499 audit boundary)

- Cumulative attempts: 79
- Records written: 19
- Records deferred: 60
- Yield: 19/79 = 24.1%
- Per-year written breakdown: ZMCC 2021={1}, ZMCC 2022={2}, ZMCC 2023={3}, ZMCC 2024={4}, ZMCC 2025={8}, ZMCC 2026={1}
- Inventory exhaustion declared at b0498

## Recommendation (carry forward from b0498)

Further Phase 5 progress requires human approval of one or more of:

1. **ZMSC older-year sweep URL pattern** — Peter approved the sweep itself on 2026-05-03 (`zmsc_older_year_sweep_approved: true`); confirmation of the canonical source URL pattern still pending. Once provided, the worker can resume net-new fetches under the existing rate limits and budgets.
2. **OCR pipeline approval** for the `pdf_extraction_empty_likely_scanned` candidates (15 entries in gaps.md, including zmcc/2021/{14,15}, zmcc/2022/16, zmcc/2025/19). Required to address the irreducible-by-parser-widening tail.
3. **parser_v0.3.3 vocabulary widening** for the recurring v0.3.2-deferred families: declaratory/interpretive ratios with no operative dispositive verb (the dominant `html_no_summary_pdf_no_match` driver in 2024/2025/2026 cohorts), jurisdictional-routing rulings ("must proceed by judicial review"), joinder-as-disposition outcomes, subordinate-clause dismissed forms, and "nullified and discharged" double-disposition phrasings. Requires Peter approval per BRIEF.md non-negotiable on parser vocabulary changes.

All three remain subject to Peter approval. Worker continues idle audit-only ticks under the Phase 5 human-only confirmation rule.

## Carry-forward note for next tick

Clean tick: first-try pull succeeded, no orphan-ref or stale-lock recovery needed (8th consecutive clean pull spanning b0488..b0499). Single residual `.git/objects/maintenance.lock` remains a host-side artefact (sandbox cannot unlink); does not block git operations and is not a recovery target. Host-side `rm -rf .git/_orphan_refs_parked/ .git/_orphan_locks_parked/` plus `find .git -name "*.lock*" -delete` and `git gc --prune=now` extension still pending Peter sign-off.

Five-consecutive-zero-discovery completion criterion will fire at b0503 if the next four ticks remain audit-only (no human unblock landing). Per BRIEF.md, the worker MAY NOT flip `approved: true` to `approved: false` and MAY NOT flip `approved: false` to `approved: true`; on completion criterion firing, the worker only appends a "Phase 5 appears complete, awaiting human confirmation" line to worker.log and continues idle audit ticks.

## Files changed

- new: `reports/batch-0499.md`
- modified: `worker.log` (tick start/end markers)
- modified: `costs.log` (batch-0499 audit line)
- modified: `provenance.log` (audit-only marker line)
