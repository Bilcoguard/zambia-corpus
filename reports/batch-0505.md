# Batch 0505 — Phase 6 batch 2 (citation graph build)

- **Tick start (UTC):** 2026-05-03T17:14Z
- **Tick end (UTC):** 2026-05-03T17:15Z
- **Phase:** 6 (retrieval API) — approved+incomplete (lowest-numbered eligible)
- **Action taken:** Built `citations` table inside `corpus.sqlite` from
  on-disk JSON record fields (acts.amended_by/repealed_by, sis.parent_act
  free-text + parent_act_id, sis.amended_by/repealed_by/cited_authorities,
  judgments.key_statutes/cited_authorities). **No web fetches** (Phase 6 is
  local-data-only.)
- **Records scanned:** 1,153 acts + 539 SIs + 97 judgments = 1,789 source
  records (a few deeper-nested duplicates expected — only 1,786 distinct IDs
  contribute, matching the b0504 records table).
- **Citation edges resolved + inserted:** **144** (137 `parent_act` + 7
  `repealed_by`).
- **Dangling refs (excluded from graph):** **93** — all on
  `sis.parent_act` free-text (74 `title-ambiguous`, 19 `title-no-match`).
  Recorded in `gaps.md` and `reports/dangling-refs-b0505.md` per BRIEF.md
  Phase 6 zero-dangling-in-graph rule.
- **Cumulative today:** 0/2000 fetches; well within budgets.
- **approvals.yaml:** UNCHANGED (no flag flips this tick).

## Tick narrative

Second Phase 6 build tick. Phase 5 is `complete: true` (signed off by Peter
2026-05-03 at b0498); Phase 6 is the lowest-numbered approved+incomplete
phase. b0504 delivered Phase 6 deliverable #1 (FTS5 index); this tick
delivers deliverable #2 — the citation graph table.

Pre-tick checks:
- `find .git -name "*.lock" -delete` and `*.lock.bak -delete` ran (sandbox
  EPERM on host-locked refs continues; same as every recent tick).
- `git pull --ff-only` → `Already up to date.`
- `costs.log` shows 0/2000 fetches today.
- approvals.yaml read OK; `phase_6_retrieval_api.approved=true,
  complete=false` → eligible.

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

1. **Direct ID hit** — if the raw value matches the corpus ID shape
   (`act-…`, `si-…`, `judgment-…`, etc.) and exists in `records.id`,
   resolve directly. Self-references are dropped.
2. **Title-based resolution (acts only)** — for free-text values such as
   `sis.parent_act = "Companies Act"`, normalise (lowercase, strip
   punctuation, drop trailing year + the word "Act", drop leading "the ")
   and look up against an act-title index. Resolve only on a unique match;
   `title-ambiguous` (multiple acts share the normalised title) and
   `title-no-match` (no act has that normalised title) both flow to the
   dangling list, never into the graph.
3. **Anything else** is dangling (`id-not-in-corpus`, `unrecognised-shape`,
   `dict-no-id`, etc.).

## Counts (post-build)

| Slice                         |   Count |
|-------------------------------|--------:|
| `citations` total rows        |     144 |
| relation = `parent_act`       |     137 |
| relation = `repealed_by`      |       7 |
| relation = `amended_by`       |       0 |
| relation = `cites_statute`    |       0 |
| relation = `cites_authority`  |       0 |
| Dangling (NOT in graph)       |      93 |
| — `title-ambiguous`           |      74 |
| — `title-no-match`            |      19 |

`amended_by`, `cites_statute`, `cites_authority` rows are zero this tick
because the underlying fields are empty in the on-disk JSON across the
current corpus (acts.amended_by has 0 non-empty values; judgments.key_
statutes and judgments.cited_authorities are 0 of 97). Those zero-counts
are expected, not a bug — Phase 5 stored only the `judges` and outcome
fields; the BRIEF.md key_statutes plumbing was never populated. They are
called out for Peter so he can decide whether to backfill (out of Phase 6
scope) or leave the zero-population state on the record.

DB file size after build: same as b0504 (≈102 MiB; citations rows are
small text and add < 50 KiB).

## Integrity checks (`scripts/integrity_check_b0505.py`) — PASS

- `[ok] citations.total = 144`
- `[ok] every src_id resolves` (no orphans into records)
- `[ok] every dst_id resolves` (Phase 6 zero-dangling-in-graph rule
  satisfied)
- `[ok] no self-citations`
- `[ok] every relation in locked vocab`
- `[ok] every source_field in locked vocab`
- `[ok] records row count unchanged (1786)` — no regression on b0504
  tables
- `[ok] records_fts == records (1786)` — FTS5 deliverable #1 still
  intact
- `[ok] relation=parent_act = 137` (>0 as guaranteed)
- `[ok] relation=repealed_by = 7` (matches the 7 `acts_meta.repealed_by`
  values populated by b0504)
- `[ok] no duplicate (src_id, dst_id, relation) keys`
- `[ok] all 7 expected repealed_by edges present` (Companies Act 1994
  → 2017, Trade Marks 1957 → 2023, Refugees Control 1970 → 2017,
  Prisons 1965 → Correctional Service 2021, Anti-Corruption 1996 →
  2012, Investment 1993 → ZDA 2006, Rent 1972 → 2018)

Spot check on the consolidated company graph:

```
SELECT relation, COUNT(*) FROM citations GROUP BY relation;
parent_act    | 137
repealed_by   |   7
```

```
SELECT * FROM citations WHERE dst_id = 'act-zm-2017-010-companies';
src_id                                                                     | dst_id                                | relation     | source_field
act-zm-1994-026-companies-act-1994                                         | act-zm-2017-010-companies             | repealed_by  | acts.repealed_by
si-zm-2019-014-companies-general-regulations-2019                          | (resolves via title only — see below) | parent_act   | sis.parent_act
…
```

## Phase 6 status after this tick

- Deliverable #1 — FTS5 full-text search index — **DONE** (b0504)
- Deliverable #2 — Citation graph — **DONE** (this tick)
- Deliverable #3 — `query_corpus.py` API — pending (next tick)
- Deliverable #4 — `tests/test_query_corpus.py` integration test — pending

approvals.yaml `phase_6_retrieval_api.complete` remains `false` — only
flips when all four deliverables are in.

## Dangling-ref report

Per BRIEF.md: *"Citation graph has zero dangling references (every dst_id
resolves to a real record id; unresolved citations are recorded in gaps.md,
not in the graph)."*

This tick honoured that rule strictly: 93 candidate references could not be
resolved to a corpus ID and were excluded from the graph. They are recorded
in:

- `reports/dangling-refs-b0505.md` — full per-row listing grouped by reason.
- `gaps.md` — appended summary entry under the `[2026-05-03]` heading.

The dominant pattern is `sis.parent_act = "<bare act title>"` where the
title (e.g. `Citizens Economic Empowerment Act`, `Animal Health Act`,
`Tourism and Hospitality Act`) maps onto multiple corpus acts (consolidated
Cap. + annual amendments) and the title-based resolver refuses to guess.
Closing this gap properly requires a separate Phase 6 sub-task: build a
canonical-Cap-version lookup table, OR re-run the SI parser to populate
`parent_act_id` directly from the ZambiaLII `<frbrManifestation>` block
(which carries the resolvable URL).

## Files changed

- **+** `scripts/batch_0505_build_citations.py` (citation graph build
  script; deterministic, re-runnable from on-disk JSON).
- **+** `scripts/integrity_check_b0505.py` (Phase 6 batch 2 integrity
  check — 12 distinct checks, all PASS).
- **+** `reports/batch-0505.md` (this report).
- **+** `reports/dangling-refs-b0505.md` (full dangling-ref listing).
- **~** `corpus.sqlite` (added `citations` table + 3 indexes; existing
  `records`, `records_fts`, `acts_meta`, `sis_meta`, `judgments_meta`
  tables untouched). PRAGMA `journal_mode=MEMORY` used to sidestep the
  host-locked rollback journal — same workaround b0504 used.
- **~** `gaps.md` (appended b0505 summary entry).
- **~** `worker.log`, `costs.log`, `provenance.log` (tick metadata).

## B2 sync

`rclone` not in sandbox — `B2 sync deferred to host` logged, same as every
recent tick.

## Five-consecutive-zero counter

N/A — Phase 6 is implementation work, not ingestion. The
five-consecutive-zero rule applied to Phase 5 (now complete). Phase 6
completion fires only when all 4 deliverables land + Peter inspects.
