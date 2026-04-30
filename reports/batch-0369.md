# Batch 0369 — Phase 5 ZMCC reparse-first continuation under parser_v0.3.1

**Date (UTC):** 2026-04-30
**Phase:** phase_5_judgments (approved + incomplete)
**Parser version:** 0.3.1 (frozen baseline `scripts/batch_0360_parse.py`)
**Parser script:** `scripts/batch_0369_parse.py` — copied from
`scripts/batch_0368_parse.py` with TARGETS slice + `_work` directory
+ comment edits. Carries the b0368 defensive `judges_no_comma`
guard (additive, not a vocabulary change). No outcome-vocabulary
changes.
**Integrity check:** `scripts/integrity_check_b0369.py` — PASS
(0 record(s) — vacuously true; no records written this tick).

## Slice

Reparse-first triage continuation per `approvals.yaml`
`reparse_first` policy. b0368 swept the 2022 ZMCC DESC slice
{34, 33, 32, 31, 30, 27, 25, 24} (0 written / 8 deferred). This
batch takes the next eight raw-on-disk no-record candidates
(year-DESC then num-DESC), skipping numbers that already have
records (19, 26, 28, 29):

| court | year | num | expression date | source |
|-------|------|-----|-----------------|--------|
| zmcc  | 2022 |  23 | 2022-10-17 | raw HTML+PDF on disk |
| zmcc  | 2022 |  22 | 2022-09-23 | raw HTML+PDF on disk |
| zmcc  | 2022 |  21 | 2022-09-29 | raw HTML+PDF on disk |
| zmcc  | 2022 |  20 | 2022-09-21 | raw HTML+PDF on disk |
| zmcc  | 2022 |  18 | 2022-09-07 | raw HTML+PDF on disk |
| zmcc  | 2022 |  17 | 2022-08-31 | raw HTML+PDF on disk |
| zmcc  | 2022 |  16 | 2022-08-25 | raw HTML+PDF on disk |
| zmcc  | 2022 |  15 | 2022-07-29 | raw HTML+PDF on disk |

Expression dates were verified via `grep` over each raw HTML's
canonical `/eng@YYYY-MM-DD` link before the slice was locked; no
fabrication.

## Result

- **Records written: 0**
- **Records deferred: 8**
  - 4 × `html_no_summary_pdf_no_match` —
    zmcc/2022/{23, 22, 18, 17}. The summaries describe
    procedural/declaratory dispositions whose operative verbs
    are not in `SUMMARY_PATTERNS`, and the PDF anchor /
    tail-2-pages paths produced no safe match. Summary heads
    captured in `gaps.md`.
  - 3 × `parser_v0.3.1_judges_no_comma_unhandled` —
    zmcc/2022/{21, 20, 15}. Confirmed space-separated
    judges_text observed (e.g., zmcc/2022/15:
    `Sitali JCC Mulenga JCC Mulonda JCC Chisunka JCC Mulongoti JCC`).
    The b0368 defensive guard correctly flagged each and routed
    to deferral with the locked-in reason code; no bogus
    single-judge record was written.
  - 1 × `pdf_extraction_empty_likely_scanned` —
    zmcc/2022/16 (Malanji and Anor v Attorney General and Anor).
    Verified via direct pdfplumber probe: 10 pages, zero
    extractable text on every page. Held for an OCR pass.

All 8 deferred entries appended to `gaps.md` under a new "Batch
0369" section with case names, expression dates, summary heads
(where present), and reason codes per BRIEF.md non-negotiable
#1.

### Defensive guard performance (b0368 → b0369)

The `judges_no_comma` guard added in b0368 is now operating as
designed. In this tick it caught all three space-separated
candidates upstream of any record write — no transient bogus
records hit `records/judgments/zmcc/2022/`, so no quarantine to
`_stale_b0369_bad_records/` was required. The b0368 precedent
of moving transient records to a quarantine directory was a
one-time clean-up; the guard now prevents the failure mode
entirely.

## Integrity

`scripts/integrity_check_b0369.py` was run; with 0 records to
validate this tick the check passes vacuously. The schema
validation, registry-resolution, hash-match, and uniqueness
clauses were not exercised. Result: **PASS**.

## Provenance and budget

- **Fresh fetches this tick:** 0 (reparse pass; raw bytes
  already on disk).
- **Cumulative today:** 19 / 2000 (~0.95%); budgets not
  exhausted. Token usage 0 of 1,000,000.
- **B2 sync:** deferred to host (rclone not in sandbox).
- **SQLite ingestion:** deferred to host. The pre-existing
  `corpus.sqlite` B-tree corruption (FTS5 pages 84..99) persists
  per b0360..b0368 policy; the canonical source-of-truth remains
  `records/*.json`.

## Phase 5 progress

45 → 45 / 100-160 target (no change this tick).

## Recommendations

This batch reinforces b0368's recommendation: **parser_v0.3.2
vocabulary widening** is the dominant unblock for the 2022 ZMCC
backlog. The findings are now fully consistent across two
consecutive ticks (b0368, b0369: 0 written across 16 candidates).

1. **Judges-no-comma fix** (highest leverage) — accept
   space-separated `<NAME> <TITLE>` tuples in `parse_judges()`.
   This is now a confirmed pattern across 6 candidates
   ({34, 32, 25, 21, 20, 15}); the fix will likely unlock most
   of the remaining 2022 raw-on-disk inventory.
2. **Operative-verb vocabulary widening** — add the verb classes
   surfaced across b0368/b0369 deferrals (electoral
   "reverse the nullification", interpretive "cannot be stopped
   or extended", procedural "joinder is refused", interlocutory
   mixed-disposition "objection dismissed and challenge allowed
   to proceed", declaratory Article-interpretation patterns).
3. **OCR pass** for the now four
   `pdf_extraction_empty_likely_scanned` candidates (zmcc/2021/15,
   zmcc/2021/14, zmcc/2025/19, zmcc/2022/16). A Tesseract
   one-shot over the four PDFs is bounded scope and would clear
   them without any new fetch budget.

Subject to Peter's approval per BRIEF.md non-negotiable on
parser vocabulary changes. Until then, raw bytes remain on disk
and re-parsing under v0.3.2 will be cost-free.

## Next tick

Three viable paths, in approximately decreasing leverage:

1. **Pause for parser_v0.3.2 approval** (highest leverage). The
   2022 ZMCC backlog is dominated by judges-no-comma + summary
   vocabulary issues; continued v0.3.1 reparse will keep
   yielding zero writes.
2. **Continue v0.3.1 reparse on the next 2022 slice**
   (zmcc/2022/{14, 13, 12, 11, 10, 9, 8, 6} — yields likely to
   remain zero; primarily catalogues more
   `parser_v0.3.1_judges_no_comma_unhandled` and
   `html_no_summary_pdf_no_match` deferrals so v0.3.2 has a
   complete target list).
3. **OCR pass** for the four
   `pdf_extraction_empty_likely_scanned` candidates accumulated
   to date — a separate, bounded scope that does not interact
   with the parser-vocabulary blockers.

The b0368 next-tick plan referenced 2022 slice {23..15}; that
plan was carried out this tick. The dominant finding (judges-no-
comma + summary-vocabulary gaps) is now a stable two-tick
signal.
