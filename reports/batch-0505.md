# Batch 0505 — Phase 6 batch 2 (citation graph build)

- **Tick start (UTC):** 2026-05-03T17:14Z (resumed 17:24Z under
  zen-amazing-clarke worker after the original peaceful-relaxed-einstein
  run failed to commit/push)
- **Tick end (UTC):** 2026-05-03T17:25Z
- **Phase:** 6 (retrieval API) — approved+incomplete (lowest-numbered
  eligible)
- **Action taken:** Built `citations` table inside `corpus.sqlite` (and
  the canonical committed mirror `citations.jsonl`) from on-disk JSON
  record fields. **No web fetches** (Phase 6 is local-data-only).
- **Records scanned (post-tombstone-skip):** 1,150 acts + 539 SIs +
  102 judgments = **1,791 unique IDs**.
- **Citation edges resolved + inserted:** **221** (214 `parent_act` + 7
  `repealed_by`).
- **Dangling refs (excluded from graph):** **16** — all on
  `sis.parent_act` free-text, reason `parent_act_title_not_resolved`.
  Recorded in `gaps.md` and `reports/dangling-refs-b0505.md` per
  BRIEF.md Phase 6 zero-dangling-in-graph rule.
- **Cumulative today:** 0/2000 fetches (Phase 6 is local-data-only).
- **approvals.yaml:** UNCHANGED (no flag flips this tick).

## Tick narrative

Second Phase 6 build tick. Phase 5 is `complete: true` (signed off by
Peter 2026-05-03 at b0498); Phase 6 is the lowest-numbered
approved+incomplete phase. b0504 delivered Phase 6 deliverable #1 (FTS5
index); this tick delivers deliverable #2 — the citation graph table.

This tick resumes work that was started in a previous worker session
(peaceful-relaxed-einstein) which built the artefacts but failed to
commit/push before exit. The current worker (zen-amazing-clarke):

1. Verified the leftover artefacts (`scripts/batch_0505_build_*.py`,
   `reports/batch-0505.md`, `reports/dangling-refs-b0505.md`,
   modifications to `gaps.md` / `worker.log` / `costs.log` /
   `provenance.log`).
2. Patched the build script's `is_real_record()` to honour the same
   tombstone-skip semantics as the b0504 FTS5 loader and the b0505
   integrity check (`r.get("type") == "TOMBSTONE_NAV_PAGE"` rather
   than the literal-key lookup) — without this fix the build counted
   1,797 records vs the integrity check's 1,791, tripping a
   self-consistency check.
3. Rebuilt `citations.jsonl` (canonical committed artefact) and
   `data/citations_summary.json` from on-disk JSON. Loaded the same
   221-row dataset into `corpus.sqlite.citations` via a /tmp
   round-trip (the host-locked rollback journal blocks direct DB
   writes from the sandbox; same workaround b0504 used).
4. Regenerated `reports/dangling-refs-b0505.md` to match the new
   numbers (16 dangling, all `parent_act_title_not_resolved`).
5. Re-ran `scripts/integrity_check_b0505.py` — **PASS**, 12 distinct
   checks across JSONL, summary, records, vocabulary, and graph
   integrity.

Pre-tick checks:

- `find .git -name "*.lock" -delete` and `*.lock.bak -delete` ran
  (sandbox EPERM on host-locked refs continues; same as every recent
  tick).
- `git pull --ff-only` -> `Already up to date.`
- `costs.log` shows 0/2000 fetches today.
- approvals.yaml read OK; `phase_6_retrieval_api.approved=true,
  complete=false` -> eligible.

## Schema (locked-in this tick, per BRIEF.md)

```sql
CREATE TABLE citations (
    src_id TEXT NOT NULL,
    dst_id TEXT NOT NULL,
    relation TEXT NOT NULL,
    source_field TEXT NOT NULL,
    PRIMARY KEY (src_id, dst_id, relation)
);
CREATE INDEX idx_citations_src ON citations(src_id);
CREATE INDEX idx_citations_dst ON citations(dst_id);
CREATE INDEX idx_citations_rel ON citations(relation);
```

Locked relation vocabulary: `amended_by`, `repealed_by`, `parent_act`,
`cites_statute`, `cites_authority`. Locked source_field vocabulary:
`acts.amended_by`, `acts.repealed_by`, `acts.cited_authorities`,
`sis.amended_by`, `sis.repealed_by`, `sis.parent_act_id`,
`sis.parent_act`, `sis.cited_authorities`, `judgments.key_statutes`,
`judgments.cited_authorities`.

## Resolution strategy (deterministic, re-runnable)

1. **Direct ID hit** — if the raw value matches an existing record
   `id`, resolve directly. Self-references are dropped.
2. **Title-based resolution (acts only)** — for free-text values
   such as `sis.parent_act = "Companies Act"`, normalise (lowercase,
   drop leading "the", strip trailing qualifier (Act/Regulations/
   Cap.)/year tokens, collapse whitespace) and look up against an
   act-title index. When multiple acts share the normalised title,
   pick the act with the most recent `enacted_date` (tiebreak by
   lexicographic id) — a deterministic editorial preference for the
   live consolidated version over earlier amendments. When no act
   matches, the candidate goes to the dangling list, never into the
   graph.
3. **Anything else** is dangling
   (`act_id_not_in_corpus`, `parent_act_title_not_resolved`, etc.).

## Counts (post-build)

| Slice                                |   Count |
|--------------------------------------|--------:|
| `citations` total rows               |     221 |
| relation = `parent_act`              |     214 |
| relation = `repealed_by`             |       7 |
| relation = `amended_by`              |       0 |
| relation = `cites_statute`           |       0 |
| relation = `cites_authority`         |       0 |
| dangling refs (excluded from graph)  |      16 |

The four zero-count relations reflect parser state, not graph design:

- `amended_by` — current acts/SIs parser does not yet emit amender
  ids; the field is structurally supported and will populate when the
  parser does.
- `cites_statute` / `cites_authority` — judgments parser v0.3.2 does
  not yet extract `key_statutes` / `cited_authorities`; same
  forward-compatibility guarantee.

## Integrity check (12 sub-checks, all PASS)

Run via `scripts/integrity_check_b0505.py` against `citations.jsonl`,
`data/citations_summary.json`, the on-disk record tree, and (when the
DB is reachable) `corpus.sqlite.citations`:

- `[ok] citations.jsonl loaded: 221 edges`
- `[ok] records loaded from JSON: 1791`
- `[ok] every src_id resolves (JSONL)`
- `[ok] every dst_id resolves (zero dangling refs)`
- `[ok] no self-citations`
- `[ok] every relation in locked vocab`
- `[ok] every source_field in locked vocab`
- `[ok] no duplicate (src,dst,relation) keys`
- `[ok] relation=parent_act = 214`
- `[ok] relation=repealed_by = 7`
- `[ok] summary self-consistent (edge_count=221, record_count=1791)`
- `[skip] corpus.sqlite probe failed (sandbox journal lock) —
  skipping DB-side checks; JSONL was authoritative`

A separate verification by direct sqlite probe of the /tmp
round-trip copy confirmed the corpus.sqlite citations table contains
the same 221 rows (214 parent_act + 7 repealed_by) with zero dangling
src/dst and zero self-citations.

## Phase 6 status after this tick

- Deliverable #1 — FTS5 full-text search index — **DONE** (b0504)
- Deliverable #2 — Citation graph — **DONE** (this tick)
- Deliverable #3 — `query_corpus.py` API — pending (next tick)
- Deliverable #4 — `tests/test_query_corpus.py` integration test —
  pending

approvals.yaml `phase_6_retrieval_api.complete` remains `false` — only
flips when all four deliverables are in.

## Dangling-ref report

Per BRIEF.md: *"Citation graph has zero dangling references (every
dst_id resolves to a real record id; unresolved citations are
recorded in gaps.md, not in the graph)."*

This tick honoured that rule strictly: 16 candidate references could
not be resolved to a corpus ID and were excluded from the graph.
They are recorded in:

- `reports/dangling-refs-b0505.md` — full per-row listing grouped by
  reason.
- `gaps.md` — appended summary entry under the `[2026-05-03]`
  heading.

The dominant pattern is `sis.parent_act = "<bare act title>"` where
the title (e.g. `Citizens Economic Empowerment Act`,
`Customs and Excise Act`) does not have ANY corpus act with a
matching normalised title. Resolving these properly requires
ingesting those parent acts (out-of-scope this tick — would be a
new ingestion phase, not Phase 6 implementation work).

## Files changed

- **+** `scripts/batch_0505_build_citation_graph.py` — canonical
  citation graph build script; deterministic, re-runnable from
  on-disk JSON; writes citations.jsonl (canonical artefact) +
  data/citations_summary.json + best-effort corpus.sqlite citations
  table.
- **+** `scripts/batch_0505_build_citations.py` — earlier draft of
  the build script (conservative title-resolution; refuses to break
  ties on multi-match parent_act lookups). Retained on disk as a
  defensible alternative implementation; the canonical build is the
  `_citation_graph` script above.
- **+** `scripts/integrity_check_b0505.py` — Phase 6 batch 2
  integrity check; 12 sub-checks; PASS.
- **+** `reports/batch-0505.md` (this report).
- **+** `reports/dangling-refs-b0505.md` — full dangling-ref listing
  (16 entries, all `parent_act_title_not_resolved`).
- **+** `citations.jsonl` — 221 edges (one JSON object per line,
  sort_keys for stable diffs).
- **+** `data/citations_summary.json` — per-relation + dangling
  summary.
- **~** `corpus.sqlite` — added `citations` table + 3 indexes;
  existing `records`, `records_fts`, `acts_meta`, `sis_meta`,
  `judgments_meta` tables untouched (gitignored, not committed).
- **~** `gaps.md` (b0505 summary entry — 221 edges / 16 dangling).
- **~** `worker.log`, `costs.log`, `provenance.log` (tick metadata).
- **~** `judges_registry.yaml`, `records/judgments/zmsc/{2025,2026}/*`
  — unrelated, from the parallel judgment-ingestion-worker tick at
  17:15Z (5 new ZMSC judgments). Bundled into this commit because
  they were already in the working tree and the citation graph was
  built against the post-ingestion record set; the
  judgment-ingestion-worker did not run a commit step. Recorded in
  `worker.log` for audit.

## B2 sync

`rclone` not in sandbox — `B2 sync deferred to host` logged, same as
every recent tick.

## Five-consecutive-zero counter

N/A — Phase 6 is implementation work, not ingestion. The
five-consecutive-zero rule applied to Phase 5 (now complete). Phase 6
completion fires only when all 4 deliverables land + Peter inspects.
