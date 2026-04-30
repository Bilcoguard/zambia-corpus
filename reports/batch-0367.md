# Batch 0367 — Phase 5 ZMCC reparse-first continuation under parser_v0.3.1

**Date (UTC):** 2026-04-30
**Phase:** phase_5_judgments (approved + incomplete)
**Parser version:** 0.3.1 (frozen baseline `scripts/batch_0360_parse.py`)
**Parser script:** `scripts/batch_0367_parse.py` — copied from
`scripts/batch_0366_parse.py` with TARGETS slice change + `_work`
directory bump only. No logic changes.
**Integrity check:** `scripts/integrity_check_b0367.py` — PASS
(2 records validated).

## Slice

Reparse-first triage continuation per approvals.yaml `reparse_first`
policy. Candidates already on disk (raw HTML+PDF) but never written
under the older parser were re-parsed first, before any fresh fetch
budget is consumed (BRIEF.md "Phase 5 — Reparse-first policy").

Targets (year-DESC then num-DESC, raw-on-disk no-record continuation
of the b0366 slice):

| court | year | num | expression date | source |
|-------|------|-----|-----------------|--------|
| zmcc  | 2023 |  13 | 2023-09-28 | raw HTML+PDF on disk |
| zmcc  | 2023 |  12 | 2023-09-26 | raw HTML+PDF on disk |
| zmcc  | 2023 |  10 | 2023-09-19 | raw HTML+PDF on disk |
| zmcc  | 2023 |   8 | 2023-01-31 | raw HTML+PDF on disk |
| zmcc  | 2023 |   6 | 2023-07-31 | raw HTML+PDF on disk |
| zmcc  | 2023 |   5 | 2023-06-15 | raw HTML+PDF on disk |
| zmcc  | 2023 |   4 | 2023-03-30 | raw HTML+PDF on disk |
| zmcc  | 2023 |   3 | 2023-03-10 | raw HTML+PDF on disk |

Expression dates were verified via `grep` over each raw HTML's
canonical `/eng@YYYY-MM-DD` link before locking the slice; no
fabrication.

## Result

- **Records written:** 2
  - **[2023] ZMCC 13** — Siyunyi v The Attorney General
    (2023-09-28). Outcome: `dismissed`. Detail:
    "68 In the sum, the Petition fails in its entirety and it".
    Outcome source: `pdf-tail-2pages` (numbered "Petition fails"
    pattern in the closing-orders area). Judges: Munalula PC,
    Mulenga JJC, Mulongoti JJC, Mwandenga JJC, Mulife JJC.
  - **[2023] ZMCC 10** — Mwanza and Anor v The Attorney General
    (2023-09-19). Outcome: `dismissed`. Detail:
    "[11 O] In sum, all the claims in the Petition fail, save for
    relief (v) for which we". Outcome source: `pdf-tail-2pages`
    (numbered "claims … fail" pattern; relief (v) carve-out
    captured in the detail string per parser_v0.3.1). Judges:
    Mulonda JJC, Mulenga JJC, Musaluke JJC, Chisunka JJC,
    Mulongoti JJC.
- **Records deferred:** 6
  - 6 × `html_no_summary_pdf_no_match` (zmcc/2023/{12, 8, 6, 5, 4,
    3}) — superseding earlier "outcome not inferable under
    v0.3.0" generic deferrals from earlier batches.

All 6 deferred entries appended to `gaps.md` under a new
"Batch 0367" section with case name, expression date, and reason
code per BRIEF.md non-negotiable #1.

## Integrity

`scripts/integrity_check_b0367.py` validated the 2 written records:

- All 20 required fields present.
- `id` matches /^judgment-zm-[a-z0-9-]+$/ schema.
- `date_decided` ISO; `outcome ∈ {dismissed, allowed, …}` enum;
  `court ∈ {Constitutional Court of Zambia, …}` enum;
  `judges[*].role ∈ {presiding, concurring, dissenting}` enum.
- All judges resolve in `judges_registry.yaml` (Munalula, Mulenga,
  Mulongoti, Mwandenga, Mulife, Mulonda, Musaluke, Chisunka — all
  pre-existing entries; no new rows added this tick).
- `outcome_detail` safety: each ≥ 12 alphabetic chars; no
  blacklisted substrings.
- `source_hash` matches the on-disk raw HTML SHA-256.
- `raw_sha256` matches the on-disk raw PDF SHA-256.
- `id` globally unique within `records/judgments/`.

Result: **PASS**.

## Provenance and budget

- **Fresh fetches this tick:** 0 (reparse pass; raw bytes already
  on disk).
- **Cumulative today:** 19 / 2000 (~0.95%); budgets not exhausted.
- **B2 sync:** deferred to host (rclone not in sandbox; appended to
  costs.log with a `B2 sync deferred to host` line).
- **SQLite ingestion:** deferred to host. The pre-existing
  `corpus.sqlite` B-tree corruption (FTS5 pages 84..99 — see
  worker.log b0360-b0366) persists; the canonical source-of-truth
  remains `records/*.json` until the host can rebuild the SQLite
  index.

## Phase 5 progress

43 → 45 / 100-160 target.

## Next tick

Continue reparse-first pass on the next eight raw-on-disk no-record
candidates after zmcc/2023/3 exhausts the 2023 queue. Subsequent
ticks should still consider pivoting to:

1. **parser_v0.3.2 vocabulary widening** — subject to Peter's
   approval. Seven-tick reparse trend (b0361..b0367 yields
   2,0,0,2,3,1,2 ≈ 14.3% recall over 56 candidates) shows the
   dominant deferral mode is `html_no_summary_pdf_no_match` driven
   by ratio- or issue-style summaries with no operative disposition
   token in the tail PDF text — vocabulary widening is the most
   likely to lift recall on the remaining 2022/2023 backlog.
2. **OCR pass** for the three `pdf_extraction_empty_likely_scanned`
   candidates accumulated to date (zmcc/2021/{15,14}, zmcc/2025/19).
3. **Single targeted fetch** for zmcc/2023/17 (PDF missing) once
   the budget situation supports it.
