# Batch 0513 — Phase 7 batch 2 (Integration brief — 3 remaining example scripts)

- **Tick UTC:** 2026-05-03
- **Phase:** `phase_7_integration_brief` (approved=true, complete=false)
- **Worker:** main (Zambia Authorities Corpus worker)
- **Bounded unit of work:** implement the three remaining `examples/`
  scripts (amendment_chain, judge_decision_profile, citation_chain),
  update the INTEGRATION.md "Example scripts" table to mark them all
  Implemented, and add a Phase 7 batch-2 integrity check that runs
  every example end-to-end against the live `corpus.sqlite`.
- **Fetch budget consumed:** 0 / 2000 (Phase 7 is local-only per BRIEF §107)
- **Token budget consumed:** trivial (documentation + scripting; no LLM calls)
- **Integrity:** PASS — `scripts/integrity_check_b0513.py` 18/18 new
  assertions plus delegated `integrity_check_b0512.py` 36/36 (Phase 7
  batch 1 + Phase 6 row-count baseline both still hold).

## Deliverables produced this batch

1. **`examples/amendment_chain.py`** — given an Act id, returns the
   forward (`repealed_by`) chain, backward (`repeals`) chain, the raw
   `acts_meta.amended_by` value (with the Phase 2/4 caveat printed
   explicitly), and the inbound `parent_act` SI list. Defaults to
   `act-zm-1994-026-companies-act-1994`, which produces the canonical
   non-empty chain: 1 `repealed_by` Act (the 2017 Companies Act) plus
   3 subsidiary SIs from 2019. Supports `--json` for piping to `jq`.
   Pure read-only via `query_corpus.cited_by` / `citations_of`; never
   writes to `corpus.sqlite`.

2. **`examples/judge_decision_profile.py`** — wraps
   `query_corpus.judge_profile()` with a CLI tuned for trial-prep /
   panel-prediction work (Mike & Andrew specialists). Produces a
   compact court + outcome breakdown plus a chronological judgment
   table. Defaults to `Mulongoti` (the highest-volume judge in the
   current corpus, 36 judgments under parser_v0.3.2; 30 dismissed,
   2 allowed, 2 upheld, 1 overturned, 1 withdrawn — all in the
   Constitutional Court). Supports `--limit` and `--json`.

3. **`examples/citation_chain.py`** — given any record id (act / SI /
   judgment), traces outbound (`cited_by`) and inbound (`citations_of`)
   neighbours with optional 2-hop walk via `--depth 2`. Defaults to
   `act-zm-1994-026-companies-act-1994` so the script produces a
   non-empty chain on every run. The script handles judgment-rooted
   inputs gracefully — they're expected to return `[]` under
   parser_v0.3.2 because `key_statutes_json` and
   `cited_authorities_json` are uniformly empty across the corpus
   (already documented in `gaps.md` and the Limitations section of
   `INTEGRATION.md`).

4. **INTEGRATION.md** — the "Example scripts" table now marks all five
   scripts Implemented, and a per-script bullet list documents each
   script's default-input behaviour so a specialist can run any
   example with no arguments and confirm the corpus is wired up
   correctly. Status header bumped from "batch 1" to "batch 2"; the
   integrity check pointer is updated to
   `scripts/integrity_check_b0513.py`.

5. **`scripts/integrity_check_b0513.py`** — Phase 7 batch-2 integrity
   check. Always delegates to `integrity_check_b0512.py` first so any
   regression on the previous batch surfaces verbatim. Then runs each
   of the three new example scripts with realistic args, asserts a
   non-empty stdout containing a known marker substring, and
   round-trips the JSON output for `amendment_chain.py`,
   `citation_chain.py`, and `judge_decision_profile.py` to verify the
   schema we promise in the inline docstring. Adds a strict-shape
   check on the 1+3 chain at `act-zm-1994-026-companies-act-1994` so a
   regression on the citation graph would be caught here too.

## Verifications run live this tick

| Run | stdout chars | Outcome |
|-----|------:|---------|
| `amendment_chain.py` (default 1994 Companies Act) | 785 | 1 repealed_by + 3 SIs |
| `amendment_chain.py act-zm-2017-010-companies --json` | 385 | repeals[]: 1 entry (1994 Act) |
| `judge_decision_profile.py --limit 5` | 1137 | total=36, 5 outcomes, 1 court |
| `judge_decision_profile.py Sitali --limit 3` | 803 | total=17, ConCourt only |
| `citation_chain.py` (default) | 686 | outbound=1, inbound=3 |
| `citation_chain.py act-zm-1957-014-trade-marks-act-1957 --depth 2` | 399 | depth=2, 1 outbound (2023 Act) |

Plus delegated batch-1 runs: `corpus_search.py shareholder` (3 hits),
`corpus_search.py electoral --type si` (3 hits), `statute_interpretations.py
act-zm-2017-010-companies` (returns `[]` cleanly per known limitation).

## Phase 7 deliverable status

- Deliverable 1 (INTEGRATION.md):
  - Front matter + Quick-start ✓
  - Data coverage summary ✓
  - API reference (all six functions) ✓
  - Specialist integration patterns — **stub** (next batch)
  - Citation-verification integration — **stub** (next batch)
  - Limitations — partial (next batch will fold in the full version
    referencing `gaps.md` and the dangling-refs report)
- Deliverable 2 (examples/): **5 / 5 implemented**
  - corpus_search.py ✓ (b0512)
  - statute_interpretations.py ✓ (b0512)
  - amendment_chain.py ✓ (b0513 — this batch)
  - judge_decision_profile.py ✓ (b0513 — this batch)
  - citation_chain.py ✓ (b0513 — this batch)

Completion criteria not yet held (specialist patterns + citation-verification
section + final Limitations); Phase 7 stays at `complete: false`. Next
substantive tick: write the eight specialist integration patterns
(Clare, Harvey, Clifford, Mike, Sarah, Catherine, Johnnie, Andrew) using
real worked examples that bottom out in `query_corpus.py` calls.

## Provenance

- No web fetches.
- No record writes; no record deferrals.
- `corpus.sqlite` opened read-only via temp-copy pattern in the
  integrity check (FUSE journal-recovery workaround unchanged from
  b0512). Source-of-truth JSON records under `records/` untouched.
- `approvals.yaml` NOT modified (human-only flip per BRIEF
  non-negotiable #5 / scheduled-task spec step 10).

## Files added / changed this batch

```
A  examples/amendment_chain.py
A  examples/judge_decision_profile.py
A  examples/citation_chain.py
A  scripts/integrity_check_b0513.py
A  reports/batch-0513.md
M  INTEGRATION.md
M  worker.log
M  costs.log
M  provenance.log
```

## Integrity check output

```
INTEGRITY CHECK PASS — 18 new assertions over Phase 7 batch 2
(plus delegated b0512 PASS — 36 prior-batch assertions)
  records=1791, records_fts=1791, citations=221 (no regression)
```
