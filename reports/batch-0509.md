# Batch 0509 — Phase 6 deliverable #4: tests/test_query_corpus.py

**Tick:** 2026-05-03 (UTC)
**Phase:** `phase_6_retrieval_api` (approved 2026-05-03 by Peter; complete: false)
**Builder:** scheduled `zambia-corpus-tick`
**Source-of-truth:** `records/**/*.json` + `citations.jsonl` (corpus.sqlite is rebuildable, gitignored)

## Goal

Land Phase 6 deliverable **#4 of 4** — the integration test suite. After this batch all four BRIEF.md §3 deliverables hold:

- Deliverable #1 — FTS5 full-text search index (b0504, commit 3c073ad)
- Deliverable #2 — Citation graph (b0505 + 0507 cleanup, commits 4aeafaa..92d56d3)
- Deliverable #3 — `scripts/query_corpus.py` (b0508, commit d91b717)
- Deliverable #4 — `tests/test_query_corpus.py` (this batch)

## What landed

### `tests/test_query_corpus.py` (new, 374 LOC, 34 tests)

A `unittest`-based integration suite that validates the six BRIEF.md §3
public functions against the live `corpus.sqlite`. The suite is
organised into seven `TestCase` classes:

| Class | Function under test | Assertions |
| --- | --- | --- |
| `CorpusFixturePresent` | DB shape / parity / fixture pre-flight | 4 |
| `SearchTests` | `search` | 9 |
| `GetByIdTests` | `get_by_id` | 5 |
| `CitationsOfAndCitedByTests` | `citations_of`, `cited_by` | 6 |
| `JudgeProfileTests` | `judge_profile` | 4 |
| `StatuteInterpretationTests` | `statute_interpretation` | 4 |
| `CrossFunctionConsistencyTests` | round-trip composition | 2 |

Run with:

```
python3 -m unittest tests.test_query_corpus -v
```

Result: `Ran 34 tests in 0.818s — OK`.

### Re-runnability — re-runnable per BRIEF.md

Two design choices keep the suite stable across future batches:

1. **Frozen seeds** — the seven `repealed_by` pairs in `REPEALED_BY_PAIRS`
   are anchored to the canonical edges built by
   `scripts/batch_0505_build_citation_graph.py`. Those edges are part of
   the corpus integrity contract (BRIEF.md Phase 6 §2 zero-dangling
   rule), so the worker may not mutate them.
2. **Drift-tolerant filters** — every `search` assertion uses a query
   broad enough that future ingestion ticks cannot accidentally drop
   below 1 result. Year filters are pinned to 2017 (companies-2017) and
   court filters to "Constitutional" (72 ZMCC records), both of which
   have plenty of headroom.

The integrity check (`scripts/integrity_check_b0509.py`) runs the
suite **twice** in the same process to verify the re-runnable property
directly.

### Coverage — ≥10 known records, all six functions, all three types

`KNOWN_RECORDS` pins ten records (7 acts + 1 SI + 2 judgments). The
union with the seven `REPEALED_BY_PAIRS` covers **17 unique record ids**
in total — well above the BRIEF.md ≥10 threshold. All three required
record types (act, SI, judgment) are present, validated by
`CorpusFixturePresent.test_known_records_present`.

The six BRIEF.md §3 functions are covered by dedicated `TestCase`
classes:

| Function | Class |
| --- | --- |
| `search` | `SearchTests` |
| `get_by_id` | `GetByIdTests` |
| `citations_of` | `CitationsOfAndCitedByTests` |
| `cited_by` | `CitationsOfAndCitedByTests` |
| `judge_profile` | `JudgeProfileTests` |
| `statute_interpretation` | `StatuteInterpretationTests` |

`CrossFunctionConsistencyTests` then composes pairs of functions
(search → get_by_id, cited_by → get_by_id) to prove the API is
internally consistent.

### `scripts/integrity_check_b0509.py` (new)

A Phase 6 batch-scoped integrity check that:

1. Imports `tests.test_query_corpus` cleanly and verifies the seven
   expected `TestCase` classes are present.
2. Runs the suite via `unittest.TextTestRunner` and asserts ≥30 tests
   ran with zero failures and zero errors.
3. Verifies the function-coverage matrix above.
4. Confirms the fixture-coverage matrix (≥10 unique ids spanning all
   three types, every fixture id present in the live DB).
5. Re-runs the suite a second time (re-runnable check).
6. Re-runs `scripts/integrity_check_b0508.py` to prove no regression
   on deliverables #1-#3.
7. Confirms records / records_fts parity unchanged from b0508 baseline
   (records=1791, records_fts=1791) and citations ≥221.

Result: **25 assertions PASS** (over the test suite + no-regression
checks).

## Integrity (Phase 6 scope)

| Check | Result |
| --- | --- |
| `tests/test_query_corpus.py` runs (1st pass) | PASS — 34 tests, 0 failures |
| `tests/test_query_corpus.py` runs (2nd pass — re-runnable check) | PASS — 34 tests, 0 failures |
| Six BRIEF.md §3 functions covered | PASS |
| ≥10 unique fixture ids | PASS — 17 |
| At least one act + SI + judgment | PASS |
| `records` row count vs b0508 baseline | PASS — 1791 (unchanged) |
| `records_fts` row count vs b0508 baseline | PASS — 1791 (unchanged) |
| `records` ↔ `records_fts` parity | PASS |
| `citations` row count | PASS — 221 (≥ b0508 minimum) |
| `scripts/integrity_check_b0508.py` (delegated) | PASS — 23 assertions |

`scripts/integrity_check_b0509.py`: **25/25 assertions PASS**.

## Phase 6 — full completion criteria check (BRIEF.md §3)

| Criterion | Status |
| --- | --- |
| All 4 deliverables pass their own integrity checks | ✓ (b0504, b0505, b0508, b0509) |
| FTS5 index covers 100% of records currently in `corpus.sqlite` | ✓ — records=records_fts=1791 |
| Citation graph has zero dangling references | ✓ — 221 resolved edges; dangling refs in `gaps.md` per b0505 |
| Query API returns correct results for ≥10 sample queries fixed in `tests/test_query_corpus.py` and re-runnable | ✓ — 34 tests, 17 unique fixture ids, re-runnable |

All four Phase 6 completion criteria hold. Per the scheduled-task spec
(step 10), the worker does NOT flip `phase_6_retrieval_api.complete`
to `true` — that is reserved for human confirmation. Worker logs
"Phase 6 appears complete, awaiting human confirmation" to
`worker.log` instead.

## Provenance

- No web fetches; no records written; no records deferred.
- No mutation of `corpus.sqlite` (test suite opens with
  `mode=ro&immutable=1`, same as `query_corpus.py`).
- No mutation of `records/**/*.json` (source-of-truth untouched).
- `approvals.yaml` unchanged.

## Next tick recommendation

Phase 7 (`phase_7_integration_brief`) is the next logical phase but is
currently `approved: false`. Until Peter approves Phase 7, the worker
should:

1. Idle on the audit-only zero-yield pattern (5-consecutive-zero
   completion-criterion lap is not in scope outside Phase 5);
2. Or pivot to ZMSC older-year sweep (separate dedicated
   judgment-ingestion-worker, blocked on Peter URL pattern
   confirmation per `approvals.yaml` `zmsc_older_year_sweep_approval_note`);
3. Or run integrity smoke-checks on the existing corpus (`audit-only`
   ticks are documented in costs.log b0499..b0503).

Worker exits cleanly. Tick complete.
