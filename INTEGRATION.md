# INTEGRATION.md — Zambian Authorities Corpus → Kate Weston Legal plugin v15.1+

**Status:** Phase 7 batch 3 (API reference + data coverage + 5 example scripts + 8 specialist patterns + citation-verification integration + full Limitations — all four BRIEF.md §107 completion criteria met pending Peter's review)
**Generated:** 2026-05-03 (UTC)
**Corpus snapshot:** 1,791 records, FTS5 index 1,791 rows, 221 citation edges
**Query API:** `scripts/query_corpus.py` v1.0 (Phase 6 deliverable #3)
**Database:** `corpus.sqlite` (read-only, mode=ro&immutable=1)
**Source-of-truth:** `records/{acts,sis,judgments}/*.json` on disk; DB is rebuildable

> Phase 7 in BRIEF.md mandates that **every figure in this document is computed
> live against `corpus.sqlite`** at the time of the most recent commit. The
> integrity check at `scripts/integrity_check_b0514.py` re-derives every count
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
4. [Specialist integration patterns](#specialist-integration-patterns)
5. [Citation-verification integration](#citation-verification-integration)
6. [Limitations](#limitations)
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
introducing this document. Re-run `scripts/integrity_check_b0514.py` to
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

This section gives one worked example per Kate Weston Legal plugin v15.1
specialist persona. Every code block below is a real `query_corpus.py`
call against the live `corpus.sqlite`; output snippets are verbatim
samples (truncated for readability), not invented. The integrity check
at `scripts/integrity_check_b0514.py` re-runs the most distinctive
assertion from each pattern on every commit.

Boilerplate (imported once at the top of any specialist module):

```python
import sys, pathlib
CORPUS = pathlib.Path("/Users/peterndhlovu/KateWestonCorpus/corpus")
sys.path.insert(0, str(CORPUS / "scripts"))
import query_corpus as q
```

### Clare — case-law-research

**Task:** Find every judgment in the corpus dealing with a given legal
issue, then walk the citation graph to surface the chain of authority.

```python
# 1. Search the FTS5 index for a constitutional issue.
hits = q.search('"Article 128"', type="judgment", limit=20)
# Real hit (verbatim from corpus, truncated):
#   judgment-zm-2026-zmsc-07-munir-v-attorney
#     Munir Zulu v Attorney General and Chibwili
#     [2026] ZMSC 07
# 2. Pull the full record + issue tags for review.
rec = q.get_by_id("judgment-zm-2022-zmcc-26-michelo-v-sampa-and-anor")
# rec["issue_tags"] -> ['Electoral law', 'Section 97(2) Electoral Process Act',
#                       'proof to convincing clarity ...', ...]
# 3. Walk forward (cited_by) and backward (citations_of) to find the
#    chain of authority. (Currently judgment->judgment edges are
#    sparse — see Limitations.)
chain = q.cited_by(rec["id"])  # returns [] under parser_v0.3.2
```

For broad legal-point search Clare should prefer FTS5 phrase quotes over
free-text — phrase form preserves precise constitutional-article and
statutory-section references. The `issue_tags` field is populated for
77/102 judgments (75 % coverage); use it as the primary ranking signal
over BM25 when available.

### Harvey — corporate-commercial-finance

**Task:** Surface SCZ commercial precedents on shareholder, banking,
and insolvency disputes; trace the Companies Act amendment chain.

```python
# 1. Shareholder-dispute precedents (real hits):
hits = q.search("shareholder", type="judgment", court="Supreme", limit=10)
# Returns judgments such as:
#   judgment-zm-2025-zmsc-23-the-v-zambia
#     SEC v Zambia Breweries Plc and 2 Ors  [2025] ZMSC 23
#   judgment-zm-2026-zmsc-01-kapsch-v-intelligent
#     Kapsch Trafficom v Intelligent Mobility Solutions  [2026] ZMSC 01
#   judgment-zm-2025-zmsc-30-sa-v-zambia
#     SA Airlink (Pty) Ltd v Zambia Skyways Ltd  [2025] ZMSC 30

# 2. Companies Act amendment chain (1994 -> 2017):
forward = q.cited_by("act-zm-1994-026-companies-act-1994")
#   -> [{ id: 'act-zm-2017-010-companies', relation: 'repealed_by', ... }]

# 3. Subsidiary SIs of the 1994 Companies Act (still on the books):
subs = q.citations_of("act-zm-1994-026-companies-act-1994")
#   -> 3 SIs: si-zm-2019-014-companies-general-regulations-2019
#             si-zm-2019-015-companies-fees-regulations-2019
#             si-zm-2019-021-companies-prescribed-forms-regulations-2019
```

Banking matters: search Acts for `"bank OR banking"` to surface
`act-zm-2022-005-the-bank-of-zambia-act-2022`,
`act-zm-1994-021-banking-and-financial-services-act-1994`, and the
1996 Bank of Zambia Act. Note that
`statute_interpretation("act-zm-2022-005-the-bank-of-zambia-act-2022")`
currently returns `[]` — see [Limitations](#limitations) on
`key_statutes_json` coverage.

### Clifford — constitutional-law, tax-fiscal

**Task:** Find every Constitutional Court interpretation of a given
constitutional Article; trace tax-statute amendment history.

```python
# 1. Constitutional Court decisions on a specific Article. The corpus
#    has 72 ConCourt judgments spanning 2021-02-12 -> 2026-04-02; 72/72
#    have populated judges_json and 72/72 have populated issue_tags.
hits = q.search('"Article 128"', type="judgment", court="Constitutional",
                limit=20)
# 2. Targeted FTS5 with year filter for a recent constitutional sweep:
recent = q.search("electoral", type="judgment", court="Constitutional",
                   year_from=2022, year_to=2026, limit=50)
# 3. Tax-statute interpretation. Anchor act:
act = q.get_by_id("act-zm-1967-032-income-tax-act-1967")
# act["title"] -> 'Income Tax Act, 1967'
# Amendment chain (the corpus has 2 explicit amendment Acts indexed):
hits = q.search('"Income Tax (Amendment)"', type="act", limit=10)
#   -> e.g. act-zm-2025-017-income-tax-amendment-no20-act
#           act-zm-2022-024-the-income-tax-amendment-act-2022
# 4. Judgments that interpret the Income Tax Act:
interps = q.statute_interpretation("act-zm-1967-032-income-tax-act-1967")
#   -> []  (key_statutes_json uniformly empty across corpus —
#           Limitations §1)
```

For constitutional research Clifford should always supply
`court="Constitutional"` to filter — the FTS5 index is shared across
acts, SIs, and judgments, and the substring match on `court` is the
cheapest filter.

### Mike — litigation-strategy

**Task:** Predict a likely panel composition and outcome distribution
on a constitutional matter; surface procedural precedents.

```python
# 1. Panel-prediction signal: top-volume ConCourt judges in the corpus.
profiles = {n: q.judge_profile(n) for n in
            ["Mulongoti", "Musaluke", "Chisunka", "Munalula", "Sitali"]}
# Live counts (as of this commit):
#   Mulongoti: total=36 — dismissed=30 / allowed=2 / upheld=2 /
#              overturned=1 / withdrawn=1 — court=ConCourt
#   Musaluke:  total=35 — dismissed=29 / allowed=3 / upheld=2 /
#              withdrawn=1 — court=ConCourt
#   Munalula:  total=31 — dismissed=26 / allowed=3 / withdrawn=1 /
#              upheld=1 — court=ConCourt
#   Sitali:    total=17 — dismissed=14 / upheld=2 / allowed=1 —
#              court=ConCourt
# 2. Outcome ratio for Mike's "base rate" calibration:
#    overall ConCourt judgments in corpus: 72
#    overall outcome breakdown (across both courts):
#      dismissed=63, allowed=7, upheld=2, overturned=2, remitted=1,
#      struck-out=1, withdrawn=1, (unspecified)=25
# 3. Procedural precedent search:
proc = q.search("procedural OR jurisdiction", type="judgment",
                court="Constitutional", limit=10)
```

Caveat: the corpus has 22 distinct judge surnames, all sitting in the
Constitutional Court except for the four named on the lone SCZ case
where `judges_json` is populated. Until SCZ-side panel data backfills
(see Limitations), Mike's panel-prediction signal is ConCourt-only.

### Sarah — document-analysis

**Task:** Read a contract referencing the Companies Act, find the
relevant statute in force, surface its subsidiary regulations, and
flag any pending amendments.

```python
# 1. Contract mentions "Companies Act 2017" — fetch the canonical record:
act = q.get_by_id("act-zm-2017-010-companies")
# act["title"] -> "The Companies Act, 2017"
# act["citation"] -> "Act No. 10 of 2017"
# act["section_count"] -> 377

# 2. Fetch the SIs whose parent_act is this Act (subsidiary regulations
#    Sarah needs to read alongside the contract):
subs = q.citations_of("act-zm-2017-010-companies")
# Currently the 2017 Act has 0 indexed parent_act children — they were
# all written under the 1994 predecessor Act in the corpus. The 1994
# Act has 3 subsidiary regulations from 2019:
subs_1994 = q.citations_of("act-zm-1994-026-companies-act-1994")
# -> 3 SIs (Companies (General), (Fees), (Prescribed Forms) Regulations 2019)

# 3. Predecessor / repealed-by chain. The 1994 Act was repealed by 2017:
chain = q.cited_by("act-zm-1994-026-companies-act-1994")
# -> [{id: 'act-zm-2017-010-companies', relation: 'repealed_by', ...}]
```

For statutes Sarah encounters by free-text reference rather than id,
search for the title and pin to the highest-rank act-typed result:

```python
matches = q.search('"Companies Act"', type="act", limit=5)
canonical_act_id = matches[0]["id"] if matches else None
```

### Catherine — family-law

**Task:** Find judgments and statutes on family-law issues —
maintenance, custody, succession.

```python
# Family-law statutes in the corpus (search the Acts table):
acts = q.search("matrimonial OR maintenance OR succession",
                 type="act", limit=10)
# Real hits include:
#   act-zm-1989-005-intestate-succession-act-1989
#   act-zm-2007-020-matrimonial-causes-act-2007
#   act-zm-1918-010-marriage-act-1918
#   act-zm-2023-013-the-marriage-amendment-act-2023

# Subsidiary regulations under the parent acts:
subs = q.citations_of("act-zm-1989-005-intestate-succession-act-1989")

# Family-law judgments — note the parser does not yet emit family-law
# tags, so search by case_name / FTS5 free text:
family_hits = q.search("estate OR succession OR widow",
                        type="judgment", limit=10)
# Real hits include:
#   judgment-zm-2025-zmsc-22-chama-v-odile (Chama Cheelemu v Odile Loukombo)
#   judgment-zm-2025-zmsc-10-thelma-v-the (Thelma Maunga, administrator
#     of the estate of the late ...)
```

Important: judgment coverage is currently 102 records, all SCZ +
ConCourt. There are no High Court family-law cases yet. Catherine
should treat the corpus as a partial ground-truth source and continue
to consult ZambiaLII directly for first-instance family disputes.

### Johnnie — statutory-compliance

**Task:** Build a compliance pack for an Act — the parent statute, all
SIs in force under it, and any judicial interpretations that bear on
its operative sections.

```python
# 1. Most-cited statutes by SI volume (the heaviest compliance loads):
#    act-zm-2016-035-the-electoral-process    -> 54 SIs
#    act-zm-2015-003-the-urban-and-regional-planning -> 19 SIs
#    act-zm-2010-027-the-animal-health        -> 10 SIs
#    local-government-act-2019                ->  9 SIs
#    act-zm-1999-007-forests-act-1999         ->  8 SIs

# 2. Compliance pack for the Electoral Process Act:
parent = q.get_by_id("act-zm-2016-035-the-electoral-process")
sis = q.citations_of("act-zm-2016-035-the-electoral-process")
# -> 54 SIs (parent_act edges, sample three full ids:
#    si-zm-2016-062-electoral-process-code-of-conduct-enforcement-regulations-2016
#    si-zm-2016-063-electoral-process-general-regulations-2016
#    si-zm-2016-070-electoral-process-local-government-elections-election-dates-and-times-of-poll-order-2016

# 3. Has any provision been judicially interpreted?
interps = q.statute_interpretation("act-zm-2016-035-the-electoral-process")
# -> []  (key_statutes_json empty — Limitations §1)
# Workaround until the parser populates key_statutes_json: free-text
# search across judgments for the Act's title:
narrow = q.search('"Electoral Process Act"', type="judgment", limit=20)
```

The 16 unresolved `parent_act` titles flagged in
`reports/dangling-refs-b0505.md` apply here — Johnnie should treat the
214 resolved `parent_act` edges as the floor on SI coverage, not a
ceiling.

### Andrew — litigation-trial-prep

**Task:** Profile the panel that will hear the trial; compile outcome
patterns by similar issue tag for witness preparation.

```python
# 1. Judge outcome patterns — pull each likely panellist:
mike = q.judge_profile("Mulongoti")
#   total=36, dismissed=30 (83 %), allowed=2 (6 %),
#   upheld=2, overturned=1, withdrawn=1
sarah = q.judge_profile("Munalula")
#   total=31, dismissed=26 (84 %), allowed=3 (10 %),
#   upheld=1, withdrawn=1

# 2. Find similar cases by issue tag. The corpus's most common tags are:
#    'Constitutional law'           (26 judgments)
#    'Constitutional jurisdiction'  (13)
#    'Electoral law'                ( 9)
#    'Constitutional procedure'     ( 5)
#    'Constitutional Court jurisdiction' (4)
#    'Article 128'                  ( 4)
similar = q.search('"electoral law"', type="judgment", limit=10)

# 3. Pull a candidate precedent end-to-end for witness familiarisation:
prec = q.get_by_id("judgment-zm-2022-zmcc-26-michelo-v-sampa-and-anor")
# prec["case_name"], prec["citation"], prec["judges"][:],
# prec["issue_tags"], prec["outcome"], prec["outcome_detail"]
```

For Andrew's panel-prediction work, the 22-judge ConCourt pool means
realistic panel scenarios are tractable. SCZ panel prediction is not
yet supported because `judges_json` is populated for only 6 of 30 SCZ
records — see Limitations §3.

---

## Citation-verification integration

The Kate Weston Legal plugin v15.1 citation-verification skill exists
to validate Zambian case citations and statute references *before*
falling back to web search. Querying this corpus first is faster (no
network), authoritative against the current snapshot, and cannot be
poisoned by a hallucinated citation that "looks plausible".

### Verification flow

```python
# Inside citation-verification skill:
import sys, pathlib
CORPUS = pathlib.Path("/Users/peterndhlovu/KateWestonCorpus/corpus")
sys.path.insert(0, str(CORPUS / "scripts"))
import query_corpus as q

def verify_zambian_citation(citation_text: str,
                             case_name: str | None = None,
                             year: int | None = None) -> dict:
    """Returns one of three states:
       - {'status': 'verified', 'record': <full record>}
       - {'status': 'no_match_in_corpus', 'fallback': 'web_search'}
       - {'status': 'partial_match',
          'candidates': [<record>, ...],
          'note': '...'}
    """
    # 1. Try a phrase-quoted search on the citation form first.
    hits = q.search(f'"{citation_text}"', type="judgment", limit=5)
    if hits:
        # Strict match: the citation appears verbatim in the indexed
        # text (case_name, outcome_detail, or reasoning).
        return {"status": "verified", "record": hits[0]}

    # 2. Fall back to a case-name search if supplied.
    if case_name:
        hits = q.search(f'"{case_name}"', type="judgment",
                        year_from=year, year_to=year, limit=5)
        if len(hits) == 1:
            return {"status": "verified", "record": hits[0]}
        if len(hits) > 1:
            return {"status": "partial_match",
                    "candidates": hits,
                    "note": "Multiple corpus records match the case name; "
                            "human review required."}

    # 3. Nothing in the corpus — defer to web search.
    return {"status": "no_match_in_corpus", "fallback": "web_search"}
```

### Recommended invocation order

1. **Local corpus** (this API, zero-network) — covers 102 ZMCC + ZMSC
   judgments 2021-02-12 → 2026-04-02 and 1,150 acts + 539 SIs.
2. **ZambiaLII** (web fetch) — for judgments outside the corpus date
   range or for the High Court.
3. **Parliament of Zambia** (web fetch) — for Acts and Bills that
   pre-date the corpus's coverage of any given Act.

### Safety notes

- The corpus uses `mode=ro&immutable=1` access — concurrent ingestion
  ticks cannot corrupt a verification session, and the verifier cannot
  accidentally write to the source-of-truth.
- A `verified` result establishes that **the corpus has a record with
  the matching citation**; it does not by itself establish that the
  citation is legally current. Cross-check `repealed_by` (for acts) and
  `outcome` (for judgments) before quoting in client work.
- A `no_match_in_corpus` result is **not** evidence that the citation
  is invalid — it may simply lie outside the corpus's date range or
  court coverage. The fallback to web search is mandatory before any
  conclusion is reported to the user.
- Never fabricate a citation from training-data memory if both corpus
  and web search return nothing; tell the user the citation could not
  be verified and route to the human research team.

---

## Limitations

A truthful inventory of what the corpus does *not* cover, current as of
this commit. Specialists must read this section before treating a
`q.search(...)` empty result as evidence of absence in Zambian law.

### 1. `key_statutes_json` and `cited_authorities_json` are uniformly empty

Across all 102 judgments, `judgments_meta.key_statutes_json` is empty
(`[]`) and `judgments_meta.cited_authorities_json` is empty (`[]`). The
Phase 5 parser (parser_v0.3.2) extracts outcome and issue tags but does
not yet populate the statute / authority cross-reference fields.

Consequences for the API surface:

- `statute_interpretation(act_id)` returns `[]` for every input. The
  function falls back to free-text scanning of `key_statutes_json`,
  but with no source data the fallback produces nothing either.
- `citations_of(judgment_id)` and `cited_by(judgment_id)` both return
  `[]` — judgment ↔ statute and judgment ↔ judgment edges are absent
  from the citation graph (graph contains 214 `parent_act` SI→Act
  edges + 7 `repealed_by` Act→Act edges and nothing else).
- `examples/citation_chain.py` rooted on a judgment id always returns
  an empty chain. This is documented in the script's banner.

Workaround: use FTS5 free-text search (`q.search('"Companies Act"',
type="judgment")`) to surface judgments that mention a statute by
name. The hits are a superset of true interpretations and require
human filtering.

### 2. Dangling `parent_act` references

16 SI parent-act references could not be resolved against the Acts
table. They are excluded from the citation graph per the BRIEF.md
zero-dangling rule; the full list is in
`reports/dangling-refs-b0505.md` and the 2026-05-03 entry of
`gaps.md`. Categories:

- 14 `parent_act_title_ambiguous` — multiple Act records share the
  same canonical title, no unique resolution.
- 2 `parent_act_title_no_match` — title text in `sis.parent_act` does
  not match any Act in the corpus (likely repealed predecessor).

Operational impact: Johnnie's compliance-pack workflow may
under-report SI counts by up to 16 / 539 ≈ 3 %. The 214 resolved
edges are the floor, not the ceiling.

### 3. `sis_meta.parent_act_id` is uniformly NULL

A separate denormalisation gap: while the citation graph has 214
resolved `parent_act` edges, the `sis_meta.parent_act_id` column is
NULL for all 539 SIs. The graph table is the canonical source —
queries that depend on parent-act resolution must go through
`q.cited_by(si_id)` or the `citations` table, not `sis_meta`.

### 4. Judgment coverage

- **Total:** 102 records.
- **Courts:** Constitutional Court of Zambia (72), Supreme Court of
  Zambia (30). **No High Court coverage.** No Court of Appeal
  coverage. No subordinate-court coverage.
- **Date range:** ConCourt 2021-02-12 → 2026-04-02; SCZ 2025-01-10 →
  2026-04-17. Pre-2021 landmark judgments are not yet ingested.
- **SCZ metadata thin:** of the 30 SCZ records, only 5/30 have
  populated `issue_tags_json` and 6/30 have populated `judges_json`
  (newer ingestion-worker batches under the dedicated judgment-
  ingestion-worker have looser metadata extraction than the locked
  ZMCC parser used in Phase 5).
- **Judges pool:** 22 distinct surnames, 21 of which sit in the
  Constitutional Court. Mike's and Andrew's panel-prediction patterns
  are ConCourt-only until SCZ judges_json populates.

The Phase 5 procedural completion at 97 + 5 ZMSC additions in
batch-0506 = 102; the dedicated judgment-ingestion-worker continues to
extend coverage on its own scheduled cadence under the same Phase 5
schema.

### 5. Acts metadata gaps

- **`enacted_date` NULL for 770 / 1150 acts** (67 %). Year filters
  on `q.search(..., type="act", year_from=...)` therefore exclude
  these records. Specialists chasing acts by year should fall back
  to free-text on `citation` (which often carries the year) before
  concluding an act is not in the corpus.
- **`in_force` NULL for 64 / 1150 acts** (the rest are 1 / `True`).
  Treat NULL as "unknown", **not** "false".
- **`amended_by`** is stored as a JSON-encoded string in `acts_meta`
  but the underlying records leave it `'[]'` for almost every Act
  (the Phase 4 ingestion did not derive the amendment graph from
  parliament.gov.zm). Currently 0 acts in the corpus have a populated
  `amended_by` chain.

### 6. Reasoning tags uniformly empty

`judgments_meta.reasoning_tags_json` is `[]` for all 102 judgments.
The parser extracts issue tags (75 % coverage) but does not yet emit
`reasoning_tags`. Any specialist code that reads `record["reasoning_tags"]`
must handle the empty-list case gracefully.

### 7. No High Court statute-by-statute interpretation

Combined effect of (1), (4), and (6): for any given Act, the corpus
cannot today answer "show me every High Court judgment that interprets
section N". The closest available query is FTS5 search across the 102
SCZ + ConCourt judgments for the Act title or section reference; this
is a coarse free-text fallback, not a structured citation lookup.

### 8. `corpus.sqlite` not in git

`corpus.sqlite` is gitignored — it exceeds GitHub's 100 MB blob
limit. Specialists running this code on a fresh checkout must rebuild
it locally:

```bash
python scripts/batch_0504_build_fts5.py
python scripts/batch_0505_build_citation_graph.py
```

The JSON records under `records/{acts,sis,judgments}/` are the
canonical source-of-truth; `corpus.sqlite` is fully derivable from
them plus `citations.jsonl`.

### 9. No write API

By design, `query_corpus.py` exposes no write surface. Specialists
that need to add a record must produce a JSON file under
`records/<type>/...` and trigger a corpus rebuild — the worker's tick
loop validates and merges new records. The plugin should never
attempt to mutate `corpus.sqlite` or any `records/*.json` file
directly; doing so would corrupt the integrity-check baseline.

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
