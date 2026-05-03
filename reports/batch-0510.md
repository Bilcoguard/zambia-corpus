# Batch 0510 — Phase 6 audit-only tick (post-completion, awaiting Peter)

**Tick:** 2026-05-03T18:04Z (UTC)
**Phase:** `phase_6_retrieval_api` (approved 2026-05-03 by Peter; complete: false)
**Worker:** scheduled `zambia-corpus-tick` (30-min cadence)
**Source-of-truth:** `records/**/*.json` + `citations.jsonl` (corpus.sqlite gitignored, rebuildable)
**Pre-tick HEAD:** 951130b
**Post-tick HEAD:** unchanged (no source-of-truth mutations this tick)

## Why this is an audit-only tick

All four Phase 6 deliverables landed across batches 0504–0509 and the
completion criteria all hold (re-confirmed below). The scheduled-task
spec step 10 prohibits the worker from flipping `complete: true` —
that is reserved to Peter. Phase 7 (`phase_7_integration_brief`) is
`approved: false`, so it is out of scope until Peter unlocks it.
There is no other approved + incomplete phase. The only legitimate
work this tick is therefore: (a) re-verify the corpus has not drifted
since b0509, (b) refresh the "Phase 6 appears complete, awaiting
human confirmation" marker, (c) report.

## What landed in source-of-truth

Nothing. No fetches. No record writes or deletes. No schema changes.
No script changes. The single new file is this batch report.

## Integrity check (Phase 6 scope, b0510)

Re-ran `scripts/integrity_check_b0509.py` (which delegates to
`scripts/integrity_check_b0508.py`) against the working tree.

| Probe | Baseline (b0509) | b0510 actual | Result |
| --- | --- | --- | --- |
| `records` row count | 1791 | 1791 | PASS |
| `records_fts` row count | 1791 | 1791 | PASS |
| `records` / `records_fts` parity | equal | equal | PASS |
| `citations` row count (≥221) | 221 | 221 | PASS |
| `citations` dangling-in-graph | 0 | 0 | PASS |
| `records` self-citations | 0 | 0 | PASS |
| `records` unique ids | 1791 | 1791 | PASS |
| `records` missing core provenance (`source_url` ∨ `source_hash` ∨ `fetched_at` ∨ `parser_version`) | 0 | 0 | PASS |
| `tests/test_query_corpus.py` | 34 PASS | 34 PASS (0.832 s) | PASS |
| `integrity_check_b0509.py` | 25/25 | 25/25 | PASS |
| `integrity_check_b0508.py` (delegated) | 23/23 | 23/23 | PASS |

Type breakdown unchanged from b0509: 1150 acts + 539 SIs + 102
judgments = 1791. Note: judgment count is 102 not 97 because the
dedicated `judgment-ingestion-worker` added 5 ZMSC records in b0506
(commit `4dd8ba3`); that's that worker's lane and is already accounted
for in b0508/b0509 baselines.

## Phase 6 completion criteria — re-confirmation

Quoting BRIEF.md §3:

1. **All 4 deliverables pass their own integrity checks.**
   Deliverables #1 (FTS5, b0504), #2 (citation graph, b0505 + 0507),
   #3 (`query_corpus.py`, b0508), #4 (`tests/test_query_corpus.py`,
   b0509) — all hold under b0510 re-verification. ✓
2. **FTS5 index covers 100% of records.** records=1791 / records_fts=1791. ✓
3. **Citation graph has zero dangling references.** dangling-in-graph=0;
   the 16 unresolved free-text title references remain logged in
   `gaps.md` (b0505 entry) and never enter the graph. ✓
4. **Query API returns correct results for ≥10 sample queries — fixed
   and re-runnable.** 17 fixture record ids spanning act+SI+judgment;
   suite re-runs PASS in 0.832 s. ✓

All four hold. Phase 6 procedurally complete; only Peter's flip of
`approvals.yaml::phase_6_retrieval_api::complete` remains.

## Budgets

- Fetches: 0 / 2000
- Tokens (this tick, approximate): trivial; well under 1 000 000 daily
- Per-domain rate limits: not exercised (no fetches)

## What the next tick should do

If Peter has not flipped `phase_6_retrieval_api.complete: true` and
has not approved `phase_7_integration_brief`, this remains an
audit-only loop — repeat the b0510 integrity probe and refresh the
marker. No fetch budget is consumed. If Peter has flipped Phase 6 and
approved Phase 7, the next tick begins drafting `INTEGRATION.md`
(BRIEF.md Phase 7 deliverable: how the Kate Weston Legal plugin
should call `query_corpus.py` and format citations).

## Provenance / housekeeping notes

- Lock-file workaround unchanged from b0509: sandbox FUSE forbids
  `unlink` on `.git/objects/maintenance.lock`; warning logged, harmless.
- B2 sync deferred to host (`rclone` not present in sandbox).
- `corpus.sqlite` was copied to a writable scratch path for read-only
  query during this tick (the FUSE mount returned `disk I/O error` on
  direct sqlite3 connect); the on-disk source-of-truth file under
  `corpus/` is unchanged.
