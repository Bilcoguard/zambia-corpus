# Batch 0402 — Phase 5 Audit-Only Idle Tick

**Tick start (UTC):** 2026-05-01T11:34:15Z
**Tick id:** batch-0402
**Phase:** phase_5_judgments (approved+incomplete)
**Yield:** 0 records / audit-only (no parser run)
**Fresh fetches:** 0
**Cumulative today:** 0 / 2000
**Wall-clock:** under 5 min — well inside 20-min budget

## Status

This is the **27th consecutive substantive audit-only tick** (b0375..b0383 plus b0385..b0402).
The Phase 5 v0.3.1 reparse inventory remains fully exhausted.
The BRIEF.md five-consecutive-zero-discovery completion criterion remains fired (originally
fired b0379 and re-affirmed every substantive tick since).
approvals.yaml has not been touched since 2026-04-30T15:36:40Z (commit b24a938 by Peter,
~20h 0m at tick start, per `git log -1 --format=%cI -- approvals.yaml`). No human approval
has yet arrived for the three queued unblocks (parser_v0.3.2 / OCR pipeline /
ZMSC fresh-DESC-sweep).

Per the Phase 5 human-only confirmation rule (BRIEF.md non-negotiable §4 and tick protocol
step 10), the worker does not flip `approved` or `complete` flags itself.

## Reparse-first inventory audit (step 5 of approvals.yaml `reparse_first` policy)

| Source | raw HTML | raw PDF | records | missing |
|---|---|---|---|---|
| ZMCC  | 142 | 141 | 53 | 89 (all already-deferred under v0.3.1) |
| ZMSC  |  26 |  24 | 24 |  0 (1 HTML stem outside canonical pattern + 1 index page, non-blocking) |
| SCZ   |   1 (record-only, raw under `raw/pilot/judiciary-zm/`) |   — |  1 |  0 |
| **Total records** | | | **78** | |

No new addressable v0.3.1 candidates have appeared since b0378. Inventory is byte-for-byte
identical to b0386–b0401.

## gaps.md frequency cross-check (unchanged since b0379)

| Reason code | line count |
|---|---|
| html_no_summary_pdf_no_match | 114 |
| parser_v0.3.1_judges_no_comma_unhandled | 14 |
| pdf_extraction_empty_likely_scanned | 10 |
| multi_judge_separate_opinions_no_clear_majority_disposition | 2 |
| outcome_not_inferable_under_tightened_policy *(v0.3.0 generic, retained for historical accuracy; banned for new deferrals per approvals.yaml `deferral_reasons_locked`)* | 49 |
| parser_v0.3.1_token_unhandled | 0 |
| outcome_inferred_but_detail_unsafe | 0 |

`gaps.md` mtime: 2026-04-30T21:40:59+00:00 (commit 61d666e). No write since b0379.

## Integrity check

Trivial PASS: no records written or deleted, so the schema/registry/hash/cited_authorities
clauses are not exercised against new material. Repository-wide spot check this tick:

- 78 record JSONs parsed cleanly (0 parse errors).
- 78/78 unique IDs (no duplicates).
- 78/78 records carry the four required provenance fields (`source_url`, `source_hash`,
  `fetched_at`, `parser_version`) — 0 missing.
- 6/6 random-sample `source_hash` recompute matches against on-disk raw bytes
  (mix of `raw/zambialii/judgments/zmcc/...` HTML and `raw/zambialii/judgments/zmsc/...` PDF
  — expected layout). Sample seed=402: zmsc-2025-17, zmcc-2022-28, zmcc-2026-10,
  zmcc-2026-08, zmcc-2025-20, zmsc-2025-25.
- 0 unresolved `cited_authorities`, `amended_by`, or `repealed_by` in-corpus references.

## Fresh DESC sweep — still deferred

Fresh DESC sweep continues to be deferred per b0376–b0401 rationale:

1. ~85% of the existing ZMCC backlog defers `html_no_summary_pdf_no_match` — a
   parser-vocabulary limitation a fresh sweep would only reproduce while consuming fetch
   budget that v0.3.2 will be far more efficient with.
2. ZMSC schema-mixing hazard — the existing 24 ZMSC records use parser_v0.5.0 schema; a
   v0.3.1 sweep would mix two schemas and the integrity checks do not catch
   schema-mixing.

## Escalation (27th consecutive substantive idle tick)

Three non-overlapping unblocks ranked by yield, all subject to Peter approval per BRIEF.md
non-negotiable on parser changes:

1. **parser_v0.3.2 vocabulary widening** — highest yield against existing ZMCC backlog
   (~70/89 deferred candidates).
2. **OCR pipeline** for 4 scanned-PDF candidates: zmcc/2021/14, zmcc/2021/15,
   zmcc/2022/16, zmcc/2025/19.
3. **ZMSC fresh DESC sweep into 2024/2023** — schema-mixing hazard, needs explicit
   approval and a sweep-only-against-v0.5.0 flag.

Recommended ordering: (1) → (2) → (3).

## Housekeeping (carry-forward)

`_stale_locks_b03**_*.lock.bak` quarantine residue at the repo root persists. Harmless to
git operations and worker logic; suggest a single host-side
`rm -f ~/KateWestonCorpus/corpus/_stale_locks_*` (Peter on Mac shell) at a convenient
maintenance window. Worker has not attempted in-sandbox cleanup because every prior unlink
attempt hits "Operation not permitted" (same condition driving the mv-based lock
workaround).

`.git/objects/maintenance.lock` carry-forward warning persists on `git pull`; non-blocking,
git exits 0.

## Outcome

- B2 sync deferred to host (rclone not in sandbox).
- SQLite ingestion deferred to host (corpus.sqlite FTS5 malformed-disk-image carry-forward;
  canonical source remains records/*.json).
- approvals.yaml NOT modified.
- Phase 5 progress: 78/100-160 target — unchanged.
- Phase 5 appears complete, awaiting human confirmation.
