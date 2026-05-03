# Batch 0502 — Audit-only tick (4th post-v0.3.2-exhaustion)

- **Tick start (UTC):** 2026-05-03T16:02Z
- **Tick end (UTC):** 2026-05-03T16:08Z
- **Phase:** 5 (judgments) — approved+incomplete
- **Action taken:** reparse-first inventory + integrity sweep, no fetches, no new attempts
- **Records written:** 0
- **Records deferred:** 0 (no new attempts; inventory exhausted under v0.3.2 per b0498)
- **Cumulative today:** 0/2000 fetches; ~3k tokens (integrity script + report + log appends); within budgets
- **Five-consecutive-zero-discovery counter:** 3 → 4 (b0499, b0500, b0501, b0502 each zero; 1 more zero-yield tick before completion criterion fires at b0503)
- **approvals.yaml:** UNCHANGED (Phase 5 human-only confirmation rule)

## Tick narrative

Fourth consecutive audit-only zero-yield tick after the v0.3.2 reparse-first inventory was declared FORMALLY EXHAUSTED across all ZMCC years (2021..2026) at b0498. Continues the post-exhaustion idle pattern established at b0499 and held through b0500 / b0501.

Tick prelude:
- `find .git -name "*.lock" -delete; find .git -name "*.lock.bak" -delete` ran cleanly. Carry-forward `Operation not permitted` on host-locked refs (e.g. `.git/objects/maintenance.lock`) continues as a sandbox-EPERM no-op — same behaviour observed since b0460; not blocking.
- `git pull --ff-only` returned `Already up to date.` cleanly (11th consecutive clean pull including b0488..b0501).
- Pre-tick housekeeping: the locally-modified `worker.log` carrying b0501's push-OK + tick-complete markers was committed first as `batch-0501 push markers (sha 637ffb1); B2 sync deferred to host` (commit `a1196c2`), matching the b0498/b0500 marker-commit pattern. After that, `git status` showed a clean working tree and the b0502 tick proceeded.
- `costs.log` showed cumulative fetches today = 0/2000; well within budget (no fetches expected this tick either).
- `approvals.yaml` unchanged since the b0488 commit (last meaningful edit timestamp 2026-05-03 from the v0.3.2 launch); ZMSC older-year sweep remains gated on Peter confirming the canonical source URL pattern.

## Reparse-first inventory state (parser_v0.3.2)

Recomputed this tick (no change since b0498 / b0499 / b0500 / b0501):

| Court | raw HTML pairs | records on disk | raw-on-disk no-record |
|-------|---------------:|----------------:|----------------------:|
| ZMCC  | 142            | 72              | **70** (all v0.3.2-deferred) |
| ZMSC  | 24             | 24              | 0 (records cover all raw stems) |
| SCZ pilot | n/a        | 1               | n/a                   |
| **Total** |            | **97**          | **70**                |

Year-breakdown of the 70 ZMCC raw-on-disk no-record candidates (unchanged):

| Year | Missing |
|------|--------:|
| 2021 |   4     |
| 2022 |  18     |
| 2023 |  14     |
| 2024 |  15     |
| 2025 |  18     |
| 2026 |   1     |

All 70 candidates were tested under parser_v0.3.2 across b0488..b0498 (cumulative 79 attempts, 19 records written, 60 v0.3.2-deferred + 10 carried-forward-from-v0.3.1-deferred = 70 currently deferred). None are addressable by the current parser; subset of 4 (`zmcc/2021/14`, `zmcc/2021/15`, `zmcc/2022/16`, `zmcc/2025/19`) are OCR-required (`pdf_extraction_empty_likely_scanned`) and out of reach of any parser-only widening.

Inventory exhausted; no fresh fetches initiated this tick.

## Integrity check (post-pull, pre-commit) — Phase 5 scope

Light-touch, no-regression sweep matching the b0499/b0500/b0501 audit scope. Script: `scripts/integrity_check_b0502.py` (cloned from b0500 with seed/batch number bumped).

- Unique IDs: **97/97** (0 duplicates)
- Core provenance complete (`source_url` + `source_hash` + `fetched_at` + `parser_version`): **97/97**
- `source_hash` shape valid (`sha256:` + 64 hex): **97/97**
- `source_hash` resolves into `raw/` tree: **97/97** (sha256-by-content index over `raw/`, **3203 files / 2926 unique sha256** — unchanged from b0501)
- Spot-recompute (seed=502, 6 random records): **6/6 PASS**
- Internal cross-refs (`cited_authorities` / `amended_by` / `repealed_by`) within Phase 5 scope: **0 unresolved** (0 total — Phase 5 records do not yet declare cross-refs)

### parser_version histogram (Phase 5 scope, post-tick — unchanged from b0501)

| parser_version | records |
|----------------|--------:|
| 0.5.0 | 24 |
| 0.3.1 | 23 |
| 0.3.0 | 21 |
| 0.3.2 | 19 |
| 0.2.0 | 10 |
| **Total** | **97** |

### Court histogram

| Court | records |
|-------|--------:|
| Constitutional Court of Zambia | 72 |
| Supreme Court of Zambia | 25 (24 ZMSC + 1 SCZ pilot) |

## Phase 5 progress

97 of 100–160 target. **3 short of low end.**

The five-consecutive-zero-discovery completion criterion advances 3 → 4 this tick. If this audit-only pattern continues uninterrupted, the criterion would fire at b0503 (1 more tick). Per the Phase 5 protocol, completion still requires human confirmation — the tick will NOT flip `approved`/`complete` flags in `approvals.yaml`. The expected behaviour at b0503 is: append `Phase 5 appears complete, awaiting human confirmation` to `worker.log` and stop.

Note that "Phase appears complete at 97 of 100–160" is a tension between two BRIEF.md criteria — five consecutive zero-discovery ticks satisfies the procedural exhaustion criterion, while the 100–160 target is not yet met. Peter's intervention (one of the unblockers below) would close the gap; otherwise the worker correctly stops and waits for that intervention rather than fabricating records.

## Unblockers (none new this tick — same as b0499/b0500/b0501)

To resume substantive Phase 5 progress, one of the following must land:
1. **ZMSC older-year sweep URL pattern confirmed by Peter.** Approval already in place (`zmsc_older_year_sweep_approved: true` since 2026-05-03); awaiting URL pattern confirmation before any fetch budget is consumed. Same MAX_BATCH_SIZE=8 / metadata / integrity / provenance requirements apply.
2. **OCR pipeline approved.** Would unblock the 4 `pdf_extraction_empty_likely_scanned` candidates — a separate approval gate, not yet requested.
3. **parser_v0.3.3 widening approved.** Would unblock some subset of the 60 `html_no_summary_pdf_no_match` candidates (ratio/declaratory holdings outside v0.3.2 vocabulary). No proposal yet.

## SQLite ingestion / corpus.sqlite

Carry-forward FTS5 malformed-disk-image condition continues since b0474 — `corpus.sqlite` read-fails `database disk image is malformed` under sandbox virtiofs; same condition as b0474..b0501; no new corruption introduced this tick (no records written → no FTS update attempted). Host-side rebuild remains pending.

## Notes for next tick (b0503)

- Maintain audit-only zero-yield pattern until one of the three unblockers lands.
- If b0503 is also zero-yield (still no human unblock), the five-consecutive-zero-discovery counter reaches 5 and the BRIEF.md completion-criterion fires: append `Phase 5 appears complete, awaiting human confirmation` to `worker.log` and stop. **Do not edit `approvals.yaml`.**
- Reparse-first inventory unchanged from b0498/b0499/b0500/b0501/b0502 expected at b0503.
- `gaps.md` not modified this tick (no new deferrals; same as b0499/b0500/b0501).
- `approvals.yaml` unchanged (must remain so until human confirmation).
