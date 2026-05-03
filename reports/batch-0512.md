# Batch 0512 — Phase 7 batch 1 (Integration brief — initial draft)

- **Tick UTC:** 2026-05-03
- **Phase:** `phase_7_integration_brief` (approved=true, complete=false)
- **Worker:** main (Zambia Authorities Corpus worker)
- **Bounded unit of work:** scaffold INTEGRATION.md + first two example scripts
- **Fetch budget consumed:** 0 / 2000 (Phase 7 is local-only per BRIEF §107)
- **Integrity:** PASS — `scripts/integrity_check_b0512.py` 36/36; Phase 6 regression check `scripts/integrity_check_b0509.py` 25/25.

## Deliverables produced this batch

1. **`INTEGRATION.md`** at workspace root — initial draft covering:
   - Front matter + corpus snapshot metadata (1,791 records, 221 citations).
   - Quick-start example (drop-in import shape for plugin specialists).
   - **Data coverage summary** — live-computed counts for record types,
     year ranges, judgments by court, judgments by outcome, citation graph
     by relation. Every figure is re-derived in the integrity check; the
     check refuses to commit if any value drifts from the live DB.
   - **Full API reference** — all six functions in `scripts/query_corpus.py`
     (`search`, `get_by_id`, `citations_of`, `cited_by`, `judge_profile`,
     `statute_interpretation`) with parameter list, return shape, edge-case
     behaviour, and **at least one example output drawn from real corpus
     data** (not invented). Examples used in this batch:
     - `search("companies act", limit=3)` — top three real corpus hits.
     - `search("electoral", type="si", limit=3)` — three real SI ids.
     - `get_by_id("act-zm-2017-010-companies")` — real Phase-2 pilot record.
     - `citations_of("act-zm-1994-026-companies-act-1994")` — surfaces the
       1994 Act being repealed by the 2017 Act.
     - `cited_by("si-zm-1980-049-zambia-national-provident-fund-...")` —
       the SI's parent Act.
     - `judge_profile("Sitali")` — real (`total=17`, ConCourt only,
       outcome counts: dismissed=14, upheld=2, allowed=1).
     - `statute_interpretation("act-zm-2017-010-companies")` — `[]` under
       current parser coverage; documented as a known limitation.
   - **Stub sections** for specialist integration patterns,
     citation-verification integration, and limitations — a partial
     limitations list is already in place. Remaining sections will be
     populated in subsequent Phase 7 batches.

2. **`examples/corpus_search.py`** — wraps `q.search(...)` with a thin
   CLI; supports `--type`, `--court`, `--year-from`, `--year-to`,
   `--limit`, `--json`. Verified end-to-end against the live corpus
   inside `integrity_check_b0512.py`.

3. **`examples/statute_interpretations.py`** — wraps
   `q.statute_interpretation(...)` with a graceful free-text title
   fallback for the (currently universal) case where
   `key_statutes_json` is empty. Records that surface only via the
   fallback are clearly marked. Errors with a sensible exit code when
   the supplied id is unknown or is not an Act.

4. **`scripts/integrity_check_b0512.py`** — 36-assertion Phase 7
   integrity check covering: file presence, required Markdown headings,
   live-count reproduction (9 separate counts), no-regression vs Phase 6
   baselines (records=1791, fts=1791, citations=221), example-script
   end-to-end execution, and a no-fabrication spot check that confirms
   every record id quoted in `INTEGRATION.md` resolves in `corpus.sqlite`.

## Phase 7 progress

| Deliverable | Status |
|-------------|--------|
| `INTEGRATION.md` — API reference section | done (this batch) |
| `INTEGRATION.md` — Data coverage summary | done (this batch) |
| `INTEGRATION.md` — Quick start | done (this batch) |
| `INTEGRATION.md` — Specialist integration patterns | stub — next batch |
| `INTEGRATION.md` — Citation-verification integration | stub — next batch |
| `INTEGRATION.md` — Limitations (full) | partial — next batch |
| `examples/corpus_search.py` | done (this batch) |
| `examples/statute_interpretations.py` | done (this batch) |
| `examples/amendment_chain.py` | pending |
| `examples/judge_decision_profile.py` | pending |
| `examples/citation_chain.py` | pending |

## Notes

- No fetches consumed (Phase 7 is local-data-only).
- No source-of-truth mutations (`records/`, `corpus.sqlite`, JSON files
  unchanged).
- `approvals.yaml` NOT modified per scheduled-task spec step 10
  (worker only flips `complete:false → true`; that flip is reserved for
  the final Phase 7 batch when all five examples and all six markdown
  sections are complete).
- B2 sync deferred to host (rclone not in sandbox).
