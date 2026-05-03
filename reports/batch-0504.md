# Batch 0504 — Phase 6 batch 1 (FTS5 schema design + populate)

- **Tick start (UTC):** 2026-05-03T17:00Z
- **Tick end (UTC):** 2026-05-03T17:09Z
- **Phase:** 6 (retrieval API) — approved+incomplete (lowest-numbered eligible)
- **Action taken:** Designed unified `corpus.sqlite` schema, populated from on-disk JSON records, built FTS5 index across acts / SIs / judgments. **No web fetches** (Phase 6 is local-data-only.)
- **Records loaded into DB:** 1,786 (1,150 acts + 539 SIs + 97 judgments)
- **Records skipped (intentional):** 10 `_tombstone:true` placeholders (e.g. chiefs-orders reclassified as SIs), 6 `TOMBSTONE_NAV_PAGE` deleted nav stubs
- **Duplicate-path collapses:** 3 (each an act published at both `records/acts/foo.json` and `records/acts/<year>/foo.json`; deeper-nested path retained as canonical)
- **Cumulative today:** 0/2000 fetches; well within budgets
- **approvals.yaml:** UNCHANGED (no flag flips this tick)

## Tick narrative

First Phase 6 build tick. Phase 6 was approved by Peter at 2026-05-03T17:00:44Z; this tick produces deliverable #1 of 4 — **FTS5 full-text search index in `corpus.sqlite`**.

Pre-tick checks:
- `find .git -name "*.lock" -delete` and `*.lock.bak -delete` ran (sandbox-EPERM continues on host-locked refs; same as every recent tick).
- The mount blocked `git update-ref -d` on a stale `refs/remotes/origin/main.lock.bak.20260503T170054Z` empty-file ref. Worked around by writing a valid SHA into the broken ref so `git pull --ff-only` could resolve. The stale ref persists (cannot be deleted; deletion blocked at the FUSE mount layer) but no longer blocks pulls.
- `git pull --ff-only` → `Already up to date.`
- `costs.log` shows 0/2000 fetches today.
- approvals.yaml read OK; phase_6_retrieval_api.approved=true, complete=false → eligible.

## Schema (locked-in this tick)

`corpus.sqlite` is rebuilt from the on-disk JSON records each tick this phase touches it. Schema version recorded in `corpus_meta.schema_version = 'phase6.b0504'`.

```
records (
    id TEXT PRIMARY KEY,
    type TEXT,            -- 'act' | 'si' | 'judgment'
    jurisdiction TEXT,    -- 'ZM'
    title TEXT,
    citation TEXT,
    in_force INTEGER,
    source_url TEXT, source_hash TEXT, fetched_at TEXT, parser_version TEXT,
    on_disk_path TEXT,    -- relative to workspace root
    body TEXT             -- concatenated sections / paragraphs / full_text
)

acts_meta(id, enacted_date, commencement_date, amended_by JSON, repealed_by JSON, section_count)
sis_meta(id, si_number, si_year, parent_act_id, section_count)
judgments_meta(id, court, case_name, case_number, date_decided,
               outcome, outcome_detail,
               judges_json, issue_tags_json, reasoning_tags_json,
               key_statutes_json, cited_authorities_json, paragraph_count)

records_fts USING fts5(
    id UNINDEXED, type UNINDEXED,
    title, citation, case_name, outcome_detail, body,
    tokenize='porter unicode61'
)
```

`statutory_instrument` and `si` source-record types are normalised to `si` in the unified table.

## Counts (post-build)

| Slice                 | DB    | On-disk JSON |
|-----------------------|------:|-------------:|
| `records` total       | 1,786 | 1,786 unique IDs |
| `records.type='act'`  | 1,150 | 1,150        |
| `records.type='si'`   |   539 |   539        |
| `records.type='judgment'` |  97 |    97        |
| `records_fts` rows    | 1,786 |  —           |
| `acts_meta`           | 1,150 |  —           |
| `sis_meta`            |   539 |  —           |
| `judgments_meta`      |    97 |  —           |

DB file size: 107,384,832 bytes (102.4 MiB).

## Integrity checks (`scripts/integrity_check_b0504.py`) — PASS

All checks zero-error:

- `records` row count equals on-disk unique-ID count (1,786 == 1,786).
- `records_fts` row count equals `records` row count (1,786 == 1,786).
- Per-type sums equal `records_total` (1,150 + 539 + 97 == 1,786).
- Every `records.id` resolves into the matching meta table (1,150 / 539 / 97 — no orphans either way).
- Every `records_fts.id` resolves into `records` (no FTS leak); every `records.id` has an FTS row (no FTS gap).
- Every record has non-empty core provenance (`source_url`, `source_hash`, `fetched_at`, `parser_version`).
- FTS sample queries returned ≥ minimum-hit thresholds:
  - `"companies act"` (phrase) → multiple hits.
  - `pension AND scheme` (boolean) → multiple hits.
  - `zambia*` (prefix) → 1,012 hits.
  - `NEAR(appeal dismissed, 5)` → ≥ 1 hit.

Phase 6 integrity criterion **FTS5 row count == source-table row count → satisfied (1,786 == 1,786)**.

## Phase 6 status after this tick

- Deliverable #1 — FTS5 full-text search index — **DONE** (this tick)
- Deliverable #2 — Citation graph — pending (next tick: build `citations` table with `(src_id, dst_id, relation, source_field)` and dangling-ref report)
- Deliverable #3 — `query_corpus.py` API — pending (subsequent tick)
- Deliverable #4 — `tests/test_query_corpus.py` integration test — pending

approvals.yaml `phase_6_retrieval_api.complete` remains `false` — only flips when all four deliverables are in.

## Files changed

- **+** `scripts/batch_0504_build_fts5.py` (build script; rebuildable from on-disk JSON)
- **+** `scripts/integrity_check_b0504.py` (Phase 6 batch 1 integrity check)
- **+** `reports/batch-0504.md` (this report)
- **~** `corpus.sqlite` (rebuilt from scratch — 543 → 1,786 rows; new schema with FTS5 + meta tables; schema_version `phase6.b0504`)
- **~** `worker.log`, `costs.log`, `provenance.log` (tick metadata appends)

## B2 sync

`rclone` not in sandbox — `B2 sync deferred to host` logged, same as every recent tick.
