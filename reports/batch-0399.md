# Batch 0399 — Phase 5 Audit-Only Idle Tick

**Tick start (UTC):** 2026-05-01T10:02:39Z
**Tick id:** batch-0399
**Phase:** phase_5_judgments (approved+incomplete)
**Yield:** 0 records / audit-only (no parser run)
**Fresh fetches:** 0
**Cumulative today:** 0 / 2000
**Wall-clock:** under 5 min — well inside 20-min budget

## Status

This is the **24th consecutive substantive audit-only tick** (b0375..b0383 plus b0385..b0399 = 24).
The Phase 5 v0.3.1 reparse inventory remains fully exhausted.
The BRIEF.md five-consecutive-zero-discovery completion criterion remains fired (originally
fired b0379 and re-affirmed every substantive tick since).
approvals.yaml has not been touched since 2026-04-30T15:36:40Z (commit b24a938 by Peter,
~18h 26m at tick start). No human approval has yet arrived for the three queued unblocks
(parser_v0.3.2 / OCR pipeline / ZMSC fresh-DESC-sweep).

Per the Phase 5 human-only confirmation rule (BRIEF.md non-negotiable §4 and tick protocol
step 10), the worker does not flip approved/complete flags itself.

## Reparse-first inventory audit (step 5 of approvals.yaml `reparse_first` policy)

| Source | raw HTML | raw PDF | records | missing |
|---|---|---|---|---|
| ZMCC  | 142 | 141 | 53 | 89 |
| ZMSC  |  25 |  24 | 24 |  0 (1 HTML stem outside canonical pattern, non-blocking — `zmsc-index-page-1-20260424.html`) |
| SCZ   |   1 (record-only) |   — |  1 |  0 |
| **Total records** | | | **78** | |

No new addressable v0.3.1 candidates have appeared since b0378. Inventory is byte-for-byte
identical to b0386–b0398.

## gaps.md frequency cross-check (unchanged since b0379)

| Reason code | line count |
|---|---|
| html_no_summary_pdf_no_match | 114 |
| parser_v0.3.1_judges_no_comma_unhandled | 14 |
| pdf_extraction_empty_likely_scanned | 10 |
| multi_judge_separate_opinions_no_clear_majority_disposition | 2 |
| outcome_not_inferable_under_tightened_policy *(v0.3.0 generic, retained for historical accuracy; banned for new deferrals per approvals.yaml `deferral_reasons_locked`)* | 49 |

`gaps.md` mtime: 2026-04-30T21:39:41Z (commit 61d666e). Unchanged since b0379.

## Integrity check (step 6)

Trivial PASS: no records written or deleted, so the schema/registry/hash/cited_authorities
clauses are not exercised against new material. Spot-check on last 3 ZMCC + last 3 ZMSC
record JSONs:

- All required provenance fields present: `source_url`, `source_hash`, `fetched_at`,
  `parser_version`.
- All JSON parses cleanly.
- `source_hash` recompute against on-disk raw files: 6/6 match.
- Repository-wide invariants: 78 records / 78 unique IDs / 0 duplicates / 0 unresolved
  `cited_authorities` / `amended_by` / `repealed_by` references.

## Fresh DESC sweep — still deferred

Fresh DESC sweep continues to be deferred per b0376–b0398 rationale:

1. ~85% of the existing ZMCC backlog defers `html_no_summary_pdf_no_match` — a
   parser-vocabulary limitation a fresh sweep would only reproduce while consuming fetch
   budget that v0.3.2 will be far more efficient with.
2. ZMSC schema-mixing hazard — the existing 24 ZMSC records use parser_v0.5.0 schema; a
   v0.3.1 sweep would mix two schemas and the integrity checks do not catch schema-mixing.

## Escalation (24th consecutive substantive idle tick)

Three non-overlapping unblocks ranked by yield, all subject to Peter approval per BRIEF.md
non-negotiable on parser changes:

1. **parser_v0.3.2 vocabulary widening** — highest yield against existing ZMCC backlog
   (~70/89 deferred candidates).
2. **OCR pipeline** for 4 scanned-PDF candidates: zmcc/2021/14, zmcc/2021/15, zmcc/2022/16,
   zmcc/2025/19.
3. **ZMSC fresh DESC sweep into 2024/2023** — schema-mixing hazard, needs explicit
   approval and a sweep-only-against-v0.5.0 flag.

Recommended ordering: (1) → (2) → (3).

## Housekeeping (carry-forward)

`_stale_locks_b03**_*.lock.bak` quarantine residue at the repo root continues to grow
(~30+ files visible). Harmless to git operations and worker logic; suggest a single
host-side `rm -f ~/KateWestonCorpus/corpus/_stale_locks_*` (Peter on Mac shell) at a
convenient maintenance window. Worker has not attempted in-sandbox cleanup because every
prior unlink attempt hits "Operation not permitted" (same condition driving the mv-based
lock workaround).

`.git/objects/maintenance.lock` carry-forward warning persists; non-blocking, git exits 0.

## Outcome

- B2 sync deferred to host (rclone not in sandbox).
- SQLite ingestion deferred to host (corpus.sqlite FTS5 malformed-disk-image carry-forward;
  canonical source remains records/*.json).
- approvals.yaml NOT modified.
- Phase 5 progress: 78/100-160 target — unchanged.
- Phase 5 appears complete, awaiting human confirmation.
