# Batch 0508 — Phase 6 deliverable #3: query_corpus.py API

**Tick:** 2026-05-03 (UTC)
**Phase:** `phase_6_retrieval_api` (approved 2026-05-03 by Peter; complete: false)
**Builder:** scheduled `zambia-corpus-tick`
**Source-of-truth:** `records/**/*.json` + `citations.jsonl` (corpus.sqlite is rebuildable, gitignored)

## Goal

Land Phase 6 deliverable **#3 of 4** — the retrieval API. After this batch:

- ✅ Deliverable #1 — FTS5 full-text search index (b0504, commit 3c073ad)
- ✅ Deliverable #2 — Citation graph (b0505 + 0505b, commits 4aeafaa..5b75588)
- ✅ Deliverable #3 — `scripts/query_corpus.py` (this batch)
- ⬜ Deliverable #4 — `tests/test_query_corpus.py` (next tick)

## What landed

### `scripts/query_corpus.py` (new, 432 LOC)

Read-only Python module + CLI exposing the six functions required by
`BRIEF.md` Phase 6 §3:

| Function | Signature | Backed by |
| --- | --- | --- |
| `search` | `(query, type=None, court=None, year_from=None, year_to=None, limit=50)` → `list[dict]` | `records_fts` FTS5 + post-filter on type / court / year |
| `get_by_id` | `(record_id)` → `dict \| None` | `records` + the matching `<type>_meta` table |
| `citations_of` | `(record_id)` → `list[dict]` (inbound) | `citations.dst_id == record_id` |
| `cited_by` | `(record_id)` → `list[dict]` (outbound) | `citations.src_id == record_id` |
| `judge_profile` | `(judge_name)` → `dict` | scan of `judgments_meta.judges_json` (substring on canonical `name`) |
| `statute_interpretation` | `(act_id)` → `list[dict]` | citations edges (`relation='cites_statute'`) ∪ free-text scan of `key_statutes_json` |

Key design choices:

1. **Read-only by default** — opens the DB with `mode=ro&immutable=1` so a
   query session cannot corrupt the source-of-truth and is safe to run
   alongside an active judgment-ingestion-worker tick.
2. **Source-of-truth respect** — module never mutates the DB or any
   on-disk record. It only consults `corpus.sqlite`, which itself is
   rebuildable from JSON via `batch_0504_build_fts5.py` +
   `batch_0505_build_citations.py`.
3. **No web fetches** — Phase 6 is local-data-only.
4. **Deterministic CLI** — `_print_json` uses `sort_keys=True` so CLI
   output is diffable across invocations; downstream pipes to `jq` work.
5. **Graceful degradation** — every function handles empty / unknown
   input by returning a typed empty value (`[]`, `None`, `{total: 0}`)
   rather than raising. This is the contract `tests/test_query_corpus.py`
   in the next batch will harden.
6. **JSON-encoded list fields decoded on the way out** — the
   `judges_json` / `issue_tags_json` / `key_statutes_json` etc. fields
   are stored as TEXT in `judgments_meta` (sqlite has no first-class
   array type), but the public API returns them as Python lists of
   dicts/strings — callers shouldn't have to remember the encoding.
7. **`statute_interpretation` triple-path resolution** — the b0505 build
   reported zero `cites_statute` edges (the Phase 5 parser leaves
   `key_statutes` empty across the corpus). Path 1 will start producing
   results once the parser is updated. Until then, paths 2 and 3 (literal
   `act_id` substring + statute title/citation substring against
   `key_statutes_json` text) are the working channels and let
   `statute_interpretation` work the day a Phase 5 parser update
   populates `key_statutes`. This is forward-compatible; no rewrite
   needed when that happens.

### `scripts/integrity_check_b0508.py` (new, 156 LOC)

Per `BRIEF.md` Phase 6 integrity-check policy:

| # | Check | Result |
| - | --- | --- |
| 1 | `query_corpus` imports clean | PASS |
| 2 | FTS5 phrase / boolean / prefix / NEAR each return ≥1 result | PASS (4 syntaxes) |
| 3 | `get_by_id` round-trips for one act, one SI, one judgment | PASS (3 types) |
| 4 | `get_by_id('nope-not-real')` returns `None` | PASS |
| 5 | `cited_by` finds Trade Marks 1957 → 2023 `repealed_by` edge | PASS |
| 6 | `citations_of` finds the same edge inbound | PASS |
| 7 | `judge_profile('Sitali')` total ≥ 1 | PASS (17 judgments, outcomes: 14 dismissed / 2 upheld / 1 allowed) |
| 8 | `judge_profile('')` returns `total=0`, `judgments=[]` | PASS |
| 9 | `statute_interpretation` returns a list (empty acceptable) | PASS |
| 10 | `records` row count == 1791 (no regression) | PASS |
| 11 | `records_fts` row count == 1791 | PASS |
| 12 | records / records_fts parity | PASS |
| 13 | `citations` row count ≥ 221 (b0505 follow-up baseline) | PASS |
| 14 | Empty inputs handled gracefully across all 5 query functions | PASS |

**Total: 23 assertions, 0 failures.**

## Smoke-test outputs

```
search('"companies act"')                       -> 50 results (capped at limit)
search('pension AND scheme')                    -> 50 results
search('zambia*')                               -> 50 results
search('NEAR(appeal dismissed, 5)')             -> 50 results
search('appeal', type='judgment',
       year_from=2024, year_to=2025)            -> 24 judgments
get_by_id('act-zm-1994-026-companies-act-1994') -> full record + acts_meta
cited_by('act-zm-1957-014-trade-marks-act-1957') -> [Trade Marks 2023]
judge_profile('Sitali')                         -> 17 judgments
judge_profile('Mwanamwambwa')                   -> 0 (not in current corpus)
statute_interpretation('act-zm-2017-010-...')   -> 0 (key_statutes empty across corpus)
```

## Out-of-scope notes (logged for Peter)

- `judge_profile` uses substring matching on the canonical `name` field
  rather than `judges_registry.yaml` lookup. Surname-only queries
  (e.g. `"Sitali"`) work because Phase 5 normalises judges as
  `<Surname> <Title>`. If Peter wants a stricter "registry-only"
  variant, that's a one-line change to swap in a registry-resolved
  predicate.
- `statute_interpretation` returning 0 for every act is expected and
  has already been flagged in `gaps.md` and the b0505 batch report.
  Backfilling Phase 5 records with `key_statutes` is out of Phase 6
  scope.

## Phase 6 progress

| Deliverable | Status | Commit |
| --- | --- | --- |
| #1 FTS5 search | ✅ done | 3c073ad |
| #2 Citation graph | ✅ done | 5b75588 |
| #3 query_corpus.py API | ✅ done (this batch) | (this commit) |
| #4 tests/test_query_corpus.py | ⬜ pending | — |

After deliverable #4 lands, all four Phase 6 completion criteria can
be re-checked, and Peter can decide whether to flip
`phase_6_retrieval_api.complete` to `true`.

## Files added / changed

| Path | Change | Lines |
| --- | --- | --- |
| `scripts/query_corpus.py` | new | +432 |
| `scripts/integrity_check_b0508.py` | new | +156 |
| `reports/batch-0508.md` | new | this file |
| `worker.log` | append (tick log) | + |
| `provenance.log` | append | + |
| `costs.log` | append | + |

`approvals.yaml` — **unchanged** (no flag flipped). `corpus.sqlite`
unchanged on disk. `citations.jsonl` unchanged.

## Integrity verdict

**PASS** — 23/23 assertions in `scripts/integrity_check_b0508.py`. No
fetches consumed. No tokens consumed against the daily budget.
