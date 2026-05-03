# INTEGRATION.md — Zambian Authorities Corpus → Kate Weston Legal plugin v15.1+

**Status:** Phase 7 batch 2 (API reference + data coverage + 5 example scripts complete; specialist patterns / citation-verification / limitations remain stubbed for next batch)
**Generated:** 2026-05-03 (UTC)
**Corpus snapshot:** 1,791 records, FTS5 index 1,791 rows, 221 citation edges
**Query API:** `scripts/query_corpus.py` v1.0 (Phase 6 deliverable #3)
**Database:** `corpus.sqlite` (read-only, mode=ro&immutable=1)
**Source-of-truth:** `records/{acts,sis,judgments}/*.json` on disk; DB is rebuildable

> Phase 7 in BRIEF.md mandates that **every figure in this document is computed
> live against `corpus.sqlite`** at the time of the most recent commit. The
> integrity check at `scripts/integrity_check_b0513.py` re-derives every count
> below from the live DB AND runs each implemented example script end-to-end,
> refusing to commit if any value drifts or any example errors out.

---

## Table of contents

1. [Quick start](#quick-start)
2. [Data coverage summary](#data-coverage-summary)
3. [API reference](#api-reference)
   - [search](#search)
   - [get_by_id](#get_by_id)
   - [citations_of](#citations_of)
   - [cited_by](#cited_by)
   - [judge_profile](#judge_profile)
   - [statute_interpretation](#statute_interpretation)
4. [Specialist integration patterns](#specialist-integration-patterns) *(stub — populated in subsequent batches)*
5. [Citation-verification integration](#citation-verification-integration) *(stub)*
6. [Limitations](#limitations) *(stub)*
7. [Example scripts](#example-scripts)

---

## Quick start

```python
# From any plugin specialist persona — same import shape:
import sys, pathlib
CORPUS = pathlib.Path("/Users/peterndhlovu/KateWestonCorpus/corpus")
sys.path.insert(0, str(CORPUS / "scripts"))
import query_corpus as q

# Find judgments mentioning "shareholder":
hits = q.search("shareholder", type="judgment", limit=10)

# Pull a full statute record:
act = q.get_by_id("act-zm-2017-010-companies")

# Profile a judge:
sitali = q.judge_profile("Sitali")
```

The module never opens a network connection and never mutates the DB. All
read paths use `mode=ro&immutable=1`, so concurrent ingestion ticks (the
judgment-ingestion-worker, future Phase 8 re-verification) cannot interfere
with a query session.

---

## Data coverage summary

All figures below are live counts from `corpus.sqlite` as of the commit
introducing this document. Re-run `scripts/integrity_check_b0512.py` to
re-verify.

### Record counts by type

| Type | Count |
|------|------:|
| Acts (`type='act'`) | 1,150 |
| Statutory Instruments (`type='si'`) | 539 |
| Judgments (`type='judgment'`) | 102 |
| **Total** | **1,791** |

`records_fts` row count = 1,791 (100% coverage).

### Year ranges

| Type | Earliest | Latest |
|------|---------:|-------:|
| Acts (`acts_meta.enacted_date`) | 1914 | 2025 |
| SIs (`sis_meta.si_year`) | 1980 | 2026 |
| Judgments (`judgments_meta.date_decided`) | 2021 | 2026 |

The judgment date range is narrow because Phase 5 targeted recent landmark
decisions (procedural completion at 97 + 5 ZMSC additions in
judgment-ingestion-worker batch 0506 = 102 total). High Court coverage is
deferred to a later phase.

### Judgments by court

| Court | Count |
|-------|------:|
| Constitutional Court of Zambia | 72 |
| Supreme Court of Zambia | 30 |
| **Total** | **102** |

### Judgments by outcome

| Outcome | Count |
|---------|------:|
| dismissed | 63 |
| (unspecified) | 25 |
| allowed | 7 |
| upheld | 2 |
| overturned | 2 |
| withdrawn | 1 |
| struck-out | 1 |
| remitted | 1 |

`(unspecified)` = the parser could not resolve a safe outcome under
parser_v0.3.2 and the candidate is logged in `gaps.md` with a specific
deferral reason (no outcome was fabricated).

### Citation graph

| Relation | Resolved edges |
|----------|---------------:|
| `parent_act` (SI → Act) | 214 |
| `repealed_by` (Act → Act) | 7 |
| **Total** | **221** |

Dangling references (excluded from the graph per the BRIEF.md
zero-dangling rule): 16, all `parent_act_title_not_resolved` — see
`reports/dangling-refs-b0505.md` and the 2026-05-03 entry in `gaps.md`.

### Storage

- `corpus.sqlite` ≈ 102 MB (gitignored — exceeds GitHub 100 MB blob limit;
  rebuild from JSON via `scripts/batch_0504_build_fts5.py` then
  `scripts/batch_0505_build_citation_graph.py`)
- Source-of-truth JSON records under `records/{acts,sis,judgments}/`

---

## API reference

All six functions are exported by `scripts/query_corpus.py`. Every function
takes an optional `db_path: pathlib.Path` keyword argument; omit it to use
the workspace default `corpus.sqlite`. None of these functions writes to
the database.

### `search`

```python
q.search(
    query: str,
    type: str | None = None,        # one of {"act", "si", "judgment"}
    court: str | None = None,        # case-insensitive substring; judgments only
    year_from: int | None = None,    # inclusive lower bound
    year_to: int | None = None,      # inclusive upper bound
    limit: int = 50,
) -> list[dict]
```

**FTS5 syntax** is passed through unchanged: phrase quotes (`"data
protection"`), boolean operators (`AND`, `OR`, `NOT`), proximity
(`NEAR(commission directive, 5)`), and prefix matching (`compan*`) all
work. Results are ordered by SQLite's BM25 rank (lower rank = better match)
and capped at `limit`. Each result dict carries the base record fields plus
the type-specific meta plus a `rank` float.

**Effective year** for `year_from` / `year_to`: acts use `enacted_date`,
SIs use `si_year`, judgments use `date_decided`. Records with a missing
year are filtered out when either bound is supplied.

**Edge cases:** an empty/whitespace query returns `[]` immediately (no
DB hit). FTS5 syntax errors propagate as `sqlite3.OperationalError`;
the recommended pattern is to wrap user-supplied query strings in
phrase quotes when they are not already an FTS5 expression.

**Example:**

```python
>>> q.search("companies act", limit=3)
[
  {"id": "act-zm-1994-026-companies-act-1994", "type": "act",
   "title": "Companies Act, 1994", "rank": -8.34, ...},
  {"id": "act-zm-1970-029-mines-acquisition-special-provisions-no-2-act-1970",
   "type": "act", "title": "Mines Acquisition (Special Provisions) (No. 2) Act, 1970",
   "rank": -7.91, ...},
  {"id": "act-zm-2017-009-corporate-insolvency", "type": "act",
   "title": "The Corporate Insolvency", "rank": -7.64, ...},
]
```

```python
>>> q.search("electoral", type="si", limit=3)
# returns three SI records, e.g.:
#   si-zm-2020-080-electoral-registration-of-voters-regulations-2020
#   si-zm-2021-004-electoral-process-voter-education-regulations-2021
#   ...
```

### `get_by_id`

```python
q.get_by_id(record_id: str) -> dict | None
```

Returns the full record (base columns from `records` plus the
type-specific meta from `acts_meta` / `sis_meta` / `judgments_meta`) or
`None` if the id is unknown. JSON-encoded list fields on judgment records
(`judges`, `issue_tags`, `reasoning_tags`, `key_statutes`,
`cited_authorities`) are decoded into Python lists in the returned dict.

**Example (real corpus record):**

```python
>>> q.get_by_id("act-zm-2017-010-companies")
{
  "id": "act-zm-2017-010-companies",
  "type": "act",
  "jurisdiction": "ZM",
  "title": "The Companies Act, 2017",
  "citation": "Act No. 10 of 2017",
  "in_force": None,                     # Phase-2 pilot left this unset
  "source_url": "https://www.parliament.gov.zm/sites/default/files/...",
  "source_hash": "sha256:5e6acc13...520fe3",
  "fetched_at": "2026-04-09T17:39:10Z",
  "parser_version": "0.1.1",
  "on_disk_path": "records/acts/act-zm-2017-010-companies.json",
  "enacted_date": None,
  "commencement_date": None,
  "amended_by": "[]",
  "repealed_by": None,
  "section_count": 377,
}
```

`in_force=None` and the `amended_by` JSON-encoded string surface a known
caveat: the Phase-2 pilot parser (v0.1.1) did not normalise these fields,
and downstream code should treat `None` as "unknown" rather than "false".

### `citations_of`

```python
q.citations_of(record_id: str) -> list[dict]
```

Returns every record that **cites** `record_id` (inbound edges). Each
returned dict carries the full record plus two extra keys:

- `relation` — one of `parent_act`, `repealed_by` (current vocabulary;
  may grow as `cites_statute` / `cites_authority` are populated).
- `source_field` — the JSON field the edge was harvested from (e.g.
  `sis.parent_act`, `acts.repealed_by`).

**Example:** the 1994 Companies Act has been repealed by the 2017 Act
**and** is the parent of three pre-2018 SIs that are still on the books:

```python
>>> q.citations_of("act-zm-1994-026-companies-act-1994")
# Returns 4 rows: 3 SIs (relation='parent_act') + 1 act (relation='repealed_by').
# The 2017 Act appears with relation='repealed_by'.
```

### `cited_by`

```python
q.cited_by(record_id: str) -> list[dict]
```

Inverse of `citations_of` — every record that `record_id` **cites**
(outbound edges). Same `relation` / `source_field` augmentation.

**Example:** an SI's parent Act:

```python
>>> q.cited_by("si-zm-1980-049-zambia-national-provident-fund-statutory-contributions-regulations-1980")
[{"id": "act-zm-1966-001-zambia-national-provident-fund-act-1966",
  "relation": "parent_act", "source_field": "sis.parent_act",
  "title": "Zambia National Provident Fund Act, 1966", ...}]
```

### `judge_profile`

```python
q.judge_profile(judge_name: str) -> dict
```

Profiles a judge across every judgment in the corpus. Match strategy is a
case-insensitive substring against the canonical `name` field of each
entry in `judges_meta.judges_json`. Pass either a surname (`"Sitali"`) or
a full canonical form (`"Sitali J"`) — both work because Phase 5 records
and `judges_registry.yaml` are normalised surname-first.

**Return shape:**

```python
{
  "judge_name": <input string>,
  "total": int,
  "judgments": list[dict],         # full base+meta records, sorted by date_decided
  "outcome_counts": dict[str, int],
  "courts": dict[str, int],
}
```

**Example:**

```python
>>> q.judge_profile("Sitali")
{
  "judge_name": "Sitali",
  "total": 17,
  "courts": {"Constitutional Court of Zambia": 17},
  "outcome_counts": {"dismissed": 14, "upheld": 2, "allowed": 1},
  "judgments": [...],
}
```

### `statute_interpretation`

```python
q.statute_interpretation(act_id: str) -> list[dict]
```

Returns every judgment that interprets `act_id`, deduped by judgment id.
Three resolution paths in order:

1. `citations` rows where `relation='cites_statute'` and `dst_id == act_id`.
2. `judgments_meta.key_statutes_json` containing the act_id literally.
3. Free-text fallback: `key_statutes_json` mentioning the statute's
   title or citation (case-insensitive substring).

**Known limitation:** `key_statutes_json` is **uniformly empty** across the
current corpus (the Phase-5 parser does not populate it), and no
`cites_statute` edges exist in the citation graph yet. Until the parser
or a backfill batch populates these fields, this function returns `[]`
for every input. This is documented in `gaps.md` and the
[Limitations](#limitations) section below.

**Example:**

```python
>>> q.statute_interpretation("act-zm-2017-010-companies")
[]   # Empty under current parser coverage — see Limitations.
```

---

## Specialist integration patterns

*(stub — populated in subsequent Phase 7 batches: one worked example per
Kate Weston Legal plugin v15.1 specialist persona — Clare, Harvey,
Clifford, Mike, Sarah, Catherine, Johnnie, Andrew.)*

---

## Citation-verification integration

*(stub — populated in subsequent Phase 7 batches: how the plugin's
citation-verification skill should query the corpus to verify Zambian
case citations **before** falling back to web search.)*

---

## Limitations

*(stub — full version in subsequent Phase 7 batches.)*

Already known and documented for specialist consumers:

- `key_statutes` and `cited_authorities` are uniformly empty across the
  102 judgments in the corpus (Phase 5 parser does not populate them).
  `statute_interpretation()` therefore returns `[]` for every input.
- 16 SI parent-act references could not be resolved against the current
  Acts table and are listed in `reports/dangling-refs-b0505.md`. They
  are excluded from the citation graph per the zero-dangling rule.
- Judgment coverage is 102 records spanning 2021-2026 — Constitutional
  Court (72) and Supreme Court (30). High Court coverage and earlier years
  are deferred to a future ingestion phase.
- 64 acts have `in_force` unset (`None` rather than `True`/`False`); the
  Phase 2 pilot parser (v0.1.1) is the most common source. Treat `None` as
  "unknown" not "false".

---

## Example scripts

Five worked examples will live under `examples/` (see BRIEF.md Phase 7
deliverable #2). Each runs without error against `corpus.sqlite` using the
same read-only access pattern as `query_corpus.py`.

| Script | Status |
|--------|--------|
| `examples/corpus_search.py` | Implemented in batch 0512 |
| `examples/statute_interpretations.py` | Implemented in batch 0512 |
| `examples/amendment_chain.py` | Implemented in batch 0513 |
| `examples/judge_decision_profile.py` | Implemented in batch 0513 |
| `examples/citation_chain.py` | Implemented in batch 0513 |

Run any implemented example directly:

```bash
python examples/corpus_search.py "shareholder" --type judgment --limit 5
python examples/statute_interpretations.py act-zm-2017-010-companies
python examples/amendment_chain.py act-zm-1994-026-companies-act-1994
python examples/judge_decision_profile.py Sitali --limit 10
python examples/citation_chain.py act-zm-1994-026-companies-act-1994 --depth 2
```

Each script defaults to a known non-empty example so a specialist can run
it with no arguments to confirm the corpus is wired up correctly:

* `corpus_search.py` requires a query string (no useful default).
* `statute_interpretations.py` defaults to `act-zm-2017-010-companies` —
  returns an empty list under current parser coverage; the script prints
  the [Limitations](#limitations) caveat instead of erroring.
* `amendment_chain.py` defaults to `act-zm-1994-026-companies-act-1994` —
  prints 1 `repealed_by` Act + 3 subsidiary SIs.
* `judge_decision_profile.py` defaults to `Mulongoti` — the
  highest-volume judge in the current corpus (36 judgments under
  parser_v0.3.2).
* `citation_chain.py` defaults to `act-zm-1994-026-companies-act-1994`
  — same non-empty chain as `amendment_chain.py` viewed through the
  `query_corpus.cited_by` / `citations_of` lens, with optional 2-hop walk.
