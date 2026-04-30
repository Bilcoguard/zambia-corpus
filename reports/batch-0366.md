# Batch 0366 — Phase 5 ZMCC reparse-first continuation under parser_v0.3.1

**Date (UTC):** 2026-04-30
**Phase:** phase_5_judgments (approved + incomplete)
**Parser version:** 0.3.1 (frozen baseline `scripts/batch_0360_parse.py`)
**Parser script:** `scripts/batch_0366_parse.py` — copied from
`scripts/batch_0365_parse.py` with TARGETS slice change + `_work`
directory bump only. No logic changes.
**Integrity check:** `scripts/integrity_check_b0366.py` — PASS
(1 record validated).

## Slice

Reparse-first triage continuation per approvals.yaml `reparse_first`
policy. Candidates already on disk (raw HTML+PDF) but never written
under the older parser were re-parsed first, before any fresh fetch
budget is consumed (BRIEF.md "Phase 5 — Reparse-first policy").

Targets (year-DESC then num-DESC, raw-on-disk no-record continuation
of the b0365 slice):

| court | year | num | expression date | source |
|-------|------|-----|-----------------|--------|
| zmcc  | 2023 |  21 | 2023-10-27 | raw HTML+PDF on disk |
| zmcc  | 2023 |  20 | 2023-10-26 | raw HTML+PDF on disk |
| zmcc  | 2023 |  19 | 2023-10-26 | raw HTML+PDF on disk |
| zmcc  | 2023 |  18 | 2023-10-02 | raw HTML+PDF on disk |
| zmcc  | 2023 |  17 | 2023-03-09 | raw HTML on disk; PDF MISSING |
| zmcc  | 2023 |  16 | 2023-07-11 | raw HTML+PDF on disk |
| zmcc  | 2023 |  15 | 2023-10-26 | raw HTML+PDF on disk |
| zmcc  | 2023 |  14 | 2023-03-10 | raw HTML+PDF on disk |

Expression dates were verified via `grep` over each raw HTML's
canonical `/eng@YYYY-MM-DD` link before locking the slice; no
fabrication.

## Result

- **Records written:** 1
  - **[2023] ZMCC 15** — Joshua Ndipyola Banda v Attorney General
    (2022/CCZ/0010, 2023-10-26). Outcome: `dismissed`. Detail:
    "30] In sum, the Petition fails for the reasons advanced
    herein". Outcome source: `pdf-tail-2pages`
    (numbered-active-voice "Petition fails" pattern). Judges:
    Munalula PC, Sitali JJC, Mulenga JJC, Chisunka JJC, Mulongoti
    JJC.
- **Records deferred:** 7
  - 6 × `html_no_summary_pdf_no_match` (zmcc/2023/{21, 20, 19, 18,
    16, 14}) — supersede earlier "outcome not inferable under
    v0.3.0" generic deferrals from b0354.
  - 1 × `raw bytes not on disk` (zmcc/2023/17 — Nickson Chilangwa
    in his capacity as Secretary General, 2023-03-09; raw HTML
    on disk but PDF was never captured during earlier sweeps).
    Future remediation: single targeted fetch of
    `…/eng@2023-03-09/source.pdf` will unblock a parser_v0.3.1
    reparse.

All 7 deferred entries appended to `gaps.md` under a new
"Batch 0366" section with case name, expression date, summary head,
and reason code per BRIEF.md non-negotiable #1.

## Integrity

`scripts/integrity_check_b0366.py` validated the 1 written record:

- All 20 required fields present.
- `id` matches /^judgment-zm-[a-z0-9-]+$/ schema.
- `date_decided` ISO; `outcome ∈ {dismissed, allowed, …}` enum;
  `court ∈ {Constitutional Court of Zambia, …}` enum;
  `judges[*].role ∈ {presiding, concurring, dissenting}` enum.
- All 5 judges resolve in `judges_registry.yaml` (Munalula, Sitali,
  Mulenga, Chisunka, Mulongoti — all pre-existing entries; no new
  rows added this tick).
- `outcome_detail` safety: 47 alphabetic chars (≥12 floor); no
  blacklisted substrings; leading char "3" is a digit (not a
  lowercase mid-word fragment).
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
  `corpus.sqlite` B-tree corruption (FTS5 pages 84..99 — see worker.log
  b0360-b0365) persists; the canonical source-of-truth remains
  `records/*.json` until the host can rebuild the SQLite index.

## Phase 5 progress

42 → 43 / 100-160 target.

## Sandbox notes

- macOS-side `.git/refs/remotes/origin/main.lock.bak.*` and
  `…/main.lock.bak_*.lock` files could not be unlinked from the
  Linux mount (`Operation not permitted`). The recovery applied was
  to overwrite each stale ref backup with the current `origin/main`
  SHA so `git pull` could parse the loose refs cleanly. No
  commit-affecting state was changed; `refs/remotes/origin/main`
  itself was not touched. This is an isolated sandbox artefact and
  does not affect the corpus.

## Next tick

Continue reparse-first pass on the next eight raw-on-disk no-record
candidates from the 2023 backlog (descending after the 2023/14-21
slice): `zmcc/2023/{13, 12, 10, 8, 6, 5, 4, 3}`. Subsequent ticks
should consider pivoting to:

1. **parser_v0.3.2 vocabulary widening** — subject to Peter's
   approval. Five-tick reparse trend (b0361..b0366 yields 2,0,0,2,3,1
   ≈ 17.0%) shows the dominant deferral mode is
   `html_no_summary_pdf_no_match` driven by ratio- or issue-style
   summaries with no operative disposition token in the tail PDF
   text — vocabulary widening is the most likely to lift recall
   on the 2023 backlog.
2. **OCR pass** for the three `pdf_extraction_empty_likely_scanned`
   candidates accumulated to date (zmcc/2021/{15,14}, zmcc/2025/19).
3. **Single targeted fetch** for zmcc/2023/17 (PDF missing) once
   the budget situation supports it.

