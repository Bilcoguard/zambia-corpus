# Batch 0514 — Phase 7 batch 3 (Integration brief — Specialist patterns + Citation-verification + full Limitations)

- **Tick UTC:** 2026-05-03
- **Phase:** `phase_7_integration_brief` (approved=true, complete=false)
- **Worker:** main (Zambia Authorities Corpus worker)
- **Bounded unit of work:** populate the three remaining stub sections
  in `INTEGRATION.md` — eight specialist integration patterns (Clare,
  Harvey, Clifford, Mike, Sarah, Catherine, Johnnie, Andrew), the full
  Citation-verification integration section, and a nine-section
  Limitations inventory. Add a Phase 7 batch-3 integrity check that
  verifies every record id and function name referenced in the new
  prose actually resolves against `corpus.sqlite` and
  `query_corpus.py`, and that 18 live-count claims in the document
  reproduce against the live DB.
- **Fetch budget consumed:** 0 / 2000 (Phase 7 is local-only per BRIEF §107)
- **Token budget consumed:** trivial (documentation; no LLM calls)
- **Integrity:** PASS — `scripts/integrity_check_b0514.py` 20 new
  assertions plus delegated `integrity_check_b0513.py` (18 batch-2
  assertions) plus delegated `integrity_check_b0512.py` (36 batch-1
  assertions) = 74 cumulative assertions across the Phase 7 chain.

## Deliverables produced this batch

1. **`INTEGRATION.md` — Specialist integration patterns** (~140 lines):
   - **Clare** (case-law-research) — phrase-quoted FTS5 search on
     `"Article 128"`, full-record fetch of
     `judgment-zm-2022-zmcc-26-michelo-v-sampa-and-anor` showing real
     `issue_tags` content, and the citation-graph walk caveat.
   - **Harvey** (corporate-commercial-finance) — three real SCZ
     shareholder hits (`SEC v Zambia Breweries`, `Kapsch Trafficom`,
     `SA Airlink`), the 1994 → 2017 Companies Act repealed_by edge,
     and the 3 subsidiary 2019 SIs.
   - **Clifford** (constitutional-law, tax-fiscal) — ConCourt FTS5
     filter pattern, two real Income Tax Amendment Acts (2022 and
     2025), and the empty-result caveat for
     `statute_interpretation()`.
   - **Mike** (litigation-strategy) — five real ConCourt judges with
     live total / outcome counts (Mulongoti=36, Musaluke=35,
     Chisunka=34, Munalula=31, Sitali=17) plus the corpus-wide outcome
     base rate (dismissed=63, allowed=7, …).
   - **Sarah** (document-analysis) — Companies Act lookup workflow
     (canonical id resolution by FTS5 → 377-section record →
     subsidiary-SI children → repealed_by chain).
   - **Catherine** (family-law) — verified-existing family-law statute
     ids (`act-zm-1989-005-intestate-succession-act-1989`,
     `act-zm-2007-020-matrimonial-causes-act-2007`,
     `act-zm-1918-010-marriage-act-1918`,
     `act-zm-2023-013-the-marriage-amendment-act-2023`) plus two real
     judgments (`Chama Cheelemu`, `Thelma Maunga`). Documents the
     no-High-Court caveat.
   - **Johnnie** (statutory-compliance) — top-five most-cited Acts by
     SI volume from the live citations table (Electoral Process=54,
     Urban and Regional Planning=19, Animal Health=10, Local
     Government=9, Forests=8); compliance-pack workflow uses three
     real SI children of the Electoral Process Act with full ids.
   - **Andrew** (litigation-trial-prep) — judge-profile + outcome %
     for two top-volume judges with real numbers; top issue tags from
     the live `issue_tags_json` distribution.

2. **`INTEGRATION.md` — Citation-verification integration** (~50 lines):
   - `verify_zambian_citation()` reference implementation showing the
     three return states (`verified`, `partial_match`,
     `no_match_in_corpus`).
   - Recommended fallback order (local corpus → ZambiaLII →
     Parliament).
   - Four safety notes covering read-only access, "verified" semantics,
     date-range and court-coverage caveats, and the no-fabrication
     rule when both corpus and web search fail.

3. **`INTEGRATION.md` — Limitations** (full, nine-section inventory):
   §1 `key_statutes_json` and `cited_authorities_json` uniformly empty;
   §2 16 dangling `parent_act` refs (14 ambiguous + 2 no-match);
   §3 `sis_meta.parent_act_id` uniformly NULL — graph table is canonical;
   §4 judgment coverage (102 records, 2021-2026, ConCourt + SCZ only,
       SCZ metadata thin: 5/30 issue_tags, 6/30 judges; 22 distinct
       judge surnames);
   §5 acts metadata gaps (770/1150 NULL `enacted_date`, 64/1150 NULL
       `in_force`, `amended_by` chain not derived);
   §6 `reasoning_tags_json` empty across all 102 judgments;
   §7 no High Court statute-by-statute interpretation;
   §8 `corpus.sqlite` gitignored — rebuild instructions inline;
   §9 no write API — JSON records are the source-of-truth.

4. **`scripts/integrity_check_b0514.py`** (~280 lines, 20 new
   assertions). Always delegates to `integrity_check_b0513.py` first
   (which itself delegates to `b0512.py`), so any prior-batch
   regression surfaces verbatim. New assertions:
   - `INTEGRATION.md` no longer carries any `*(stub)*` markers.
   - All three populated section headers exist in their expected order.
   - All 8 specialist persona headings (`### Clare —` … `### Andrew —`)
     are present under the Specialist patterns section.
   - All 8 numbered Limitations subsections are present.
   - All 26 record ids referenced in the new Specialist patterns
     resolve via `q.get_by_id()` — zero fabrication.
   - All 6 BRIEF.md §80 functions exist on `query_corpus` AND are
     mentioned in `INTEGRATION.md`.
   - 18 live-count claims in `INTEGRATION.md` reproduce within tight
     bounds (exact match, not range): records=1791, records_fts=1791,
     citations=221, judgments=102, ZMCC=72, SCZ=30, SCZ-tagged=5,
     SCZ-judged=6, judgments-tagged=77, reasoning-populated=0,
     key-statutes-populated=0, cited-authorities-populated=0,
     acts=1150, acts-null-enacted=770, acts-null-in-force=64, sis=539,
     sis-null-parent=539, distinct-judge-surnames=22.
   - Citation-verification section covers all 6 required substrings
     (`verify_zambian_citation`, `no_match_in_corpus`, `verified`,
     `partial_match`, `ZambiaLII`, `Parliament of Zambia`).
   - Status header bumped to "Phase 7 batch 3".
   - Row-count snapshot — no regression on Phase 6 baseline.

## Verifications run live this tick

| Run | Outcome |
|-----|---------|
| `integrity_check_b0514.py` | PASS — 20 new assertions |
| Delegated `integrity_check_b0513.py` | PASS — 18 batch-2 assertions |
| Delegated `integrity_check_b0512.py` | PASS — 36 batch-1 assertions |
| 26 record-id resolutions via `q.get_by_id()` | 26/26 OK |
| 18 live-count expectations vs INTEGRATION.md | 18/18 within bounds |

Sample numeric verifications (re-derivable from `corpus.sqlite`):

- 770/1150 acts have NULL `enacted_date` (matches Limitations §5).
- 64/1150 acts have NULL `in_force` (matches Limitations §5).
- 539/539 SIs have NULL `sis_meta.parent_act_id` (matches §3).
- 0/102 judgments have populated `reasoning_tags_json` (matches §6).
- 5/30 SCZ judgments have populated `issue_tags_json` (matches §4).
- 6/30 SCZ judgments have populated `judges_json` (matches §4).
- 77/102 judgments overall have populated `issue_tags_json` (matches
  Specialist patterns / Clare's "75 % coverage" claim).
- 22 distinct judge surnames (matches Specialist patterns / Mike +
  Andrew + Limitations §4).

## Phase 7 deliverable status

- Deliverable 1 (INTEGRATION.md):
  - Front matter + Quick-start ✓
  - Data coverage summary ✓
  - API reference (all six functions) ✓
  - Specialist integration patterns (8 personas) ✓ **(b0514)**
  - Citation-verification integration ✓ **(b0514)**
  - Limitations (full, nine-section) ✓ **(b0514)**
  - Example scripts table (all 5 marked Implemented) ✓
- Deliverable 2 (`examples/`): 5 / 5 implemented
  - `corpus_search.py` ✓ (b0512)
  - `statute_interpretations.py` ✓ (b0512)
  - `amendment_chain.py` ✓ (b0513)
  - `judge_decision_profile.py` ✓ (b0513)
  - `citation_chain.py` ✓ (b0513)

**All four BRIEF.md §107 completion criteria for Phase 7 now hold:**

1. `INTEGRATION.md` renders correctly (valid Markdown, no broken
   anchors). ✓
2. All five example scripts run without error against the live
   `corpus.sqlite` and produce non-empty output for at least one
   realistic example. ✓ (verified end-to-end in delegated b0513.)
3. Specialist integration patterns accurately reflect the current
   `query_corpus.py` API surface (no fabricated function names,
   parameters, or return-shape claims). ✓ (verified by assertions
   #5 and #6 in the b0514 check.)
4. Data-coverage statistics in `INTEGRATION.md` match the actual
   counts in `corpus.sqlite` at the time of this commit. ✓
   (verified by the 18-count expectations block.)

Phase 7 appears complete pending Peter's review. **`approvals.yaml`
NOT modified** per scheduled-task spec step 10 (human-only flip of
`complete: true` for the integration-brief sign-off).

## Provenance

- No web fetches.
- No record writes; no record deferrals.
- `corpus.sqlite` opened read-only via temp-copy pattern in the
  integrity check (FUSE journal-recovery workaround unchanged from
  b0512/b0513). Source-of-truth JSON records under `records/`
  untouched. Temp-copy directory routed through
  `TMPDIR=/sessions/fervent-vibrant-edison/tmp` rather than `/tmp`
  (root filesystem is at 98 % usage in this sandbox; `/sessions` has
  6.4 GB free). The b0512/b0513 scripts already respect `TMPDIR`
  via `tempfile.mkdtemp()`, so this routing required no script
  edit.
- `approvals.yaml` NOT modified (human-only flip per BRIEF
  non-negotiable #5 / scheduled-task spec step 10).

## Files added / changed this batch

```
A  scripts/integrity_check_b0514.py
A  reports/batch-0514.md
M  INTEGRATION.md
M  worker.log
M  costs.log
M  provenance.log
```

## Integrity check output

```
INTEGRITY CHECK PASS — 20 new assertions over Phase 7 batch 3
(plus delegated b0513 PASS — 18 batch-2 assertions
 plus delegated b0512 PASS — 36 batch-1 assertions)
  records=1791, records_fts=1791, citations=221 (no regression)
```
