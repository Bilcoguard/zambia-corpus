# Batch 0368 — Phase 5 ZMCC reparse-first continuation under parser_v0.3.1

**Date (UTC):** 2026-04-30
**Phase:** phase_5_judgments (approved + incomplete)
**Parser version:** 0.3.1 (frozen baseline `scripts/batch_0360_parse.py`)
**Parser script:** `scripts/batch_0368_parse.py` — copied from
`scripts/batch_0367_parse.py` with TARGETS slice + `_work` directory
+ comment edits, plus a defensive `judges_no_comma` guard (see
"New defensive guard" below). No outcome-vocabulary changes.
**Integrity check:** `scripts/integrity_check_b0368.py` — PASS
(0 record(s) — vacuously true; no records written this tick).

## Slice

Reparse-first triage continuation per approvals.yaml `reparse_first`
policy. The 2023 ZMCC backlog has been swept end-to-end across
b0364..b0367 (records written for `{01, 02, 07, 10, 13, 15, 22, 24}`;
remaining numbers deferred with specific reason codes). This batch
**pivoted to the 2022 ZMCC backlog**, taking the next eight
raw-on-disk no-record candidates (year-DESC then num-DESC):

| court | year | num | expression date | source |
|-------|------|-----|-----------------|--------|
| zmcc  | 2022 |  34 | 2022-02-15 | raw HTML+PDF on disk |
| zmcc  | 2022 |  33 | 2022-05-05 | raw HTML+PDF on disk |
| zmcc  | 2022 |  32 | 2022-07-15 | raw HTML+PDF on disk |
| zmcc  | 2022 |  31 | 2022-01-19 | raw HTML+PDF on disk |
| zmcc  | 2022 |  30 | 2022-11-11 | raw HTML+PDF on disk |
| zmcc  | 2022 |  27 | 2022-11-10 | raw HTML+PDF on disk |
| zmcc  | 2022 |  25 | 2022-10-21 | raw HTML+PDF on disk |
| zmcc  | 2022 |  24 | 2022-10-20 | raw HTML+PDF on disk |

Expression dates were verified via `grep` over each raw HTML's
canonical `/eng@YYYY-MM-DD` link before the slice was locked; no
fabrication.

## Result

- **Records written: 0**
- **Records deferred: 8**
  - 3 × `parser_v0.3.1_judges_no_comma_unhandled` —
    zmcc/2022/{34, 32, 25}. The 2022 ZMCC HTML uses *space*-
    separated judge strings (e.g.,
    `Chibomba PC Mulenga JCC Musaluke JCC Chisunka JCC
    Mulongoti JCC`) whereas the parser was designed for the
    *comma*-separated 2023+ format. `parse_judges()` collapses a
    no-comma string into a single bogus entry whose name is the
    last token. The new defensive guard detects this case and
    defers, holding the candidate for parser_v0.3.2 vocabulary
    widening (subject to Peter's approval). For 2-of-3 of these
    candidates (zmcc/2022/{32, 25}) the outcome path
    (pdf-tail-2pages) WAS able to produce a `dismissed` finding;
    for zmcc/2022/34 the outcome path produced `overturned`. All
    three records are NOT written this tick — the judges block
    is the gating problem.
  - 5 × `html_no_summary_pdf_no_match` — zmcc/2022/{33, 31, 30,
    27, 24}. The summaries use non-standard operative verbs
    ("reversed nullification", "refused to interpret", "joinder
    refused", "dismisses ... and allows ... to proceed",
    interpretive declaratory patterns) that do not match
    `SUMMARY_PATTERNS`, and the PDF anchor / tail-2-pages paths
    also produced no safe match. Summary heads logged.

All 8 deferred entries appended to `gaps.md` under a new "Batch
0368" section with case names, expression dates, summary heads,
and reason codes per BRIEF.md non-negotiable #1.

### New defensive guard (`parser_v0.3.1` + b0368, additive only)

```python
title_token_count = len(re.findall(
    r"\b(?:PC|DPC|CJ|DCJ|JCC|JJC|JJS|JC|JS|JA|JJA|JJ|J)\b\.?",
    judges_text,
))
if len(judges) == 1 and title_token_count >= 2:
    return None, {"reason": "parser_v0.3.1_judges_no_comma_unhandled",
                  ...}
```

This is **not** a vocabulary change to the parser — it is a
sanity check that catches a degenerate parsing result and
re-routes it to the deferral path with a specific reason code
matching the approvals.yaml `parser_v<X.Y.Z>_<token>_unhandled`
template. The parser's outcome-inference logic and judges-comma-
splitting logic are unchanged. The frozen baseline
`scripts/batch_0360_parse.py` is preserved.

### Quarantine of transient bad records

A first parser run (before the guard was added) briefly wrote 3
bogus single-judge records to `records/judgments/zmcc/2022/`
(zmcc/2022/{34, 32, 25}, each with `judges = [{"name":
"Mulongoti", ...}]` or similar — the last token of the raw
string). Those files were moved to `_stale_b0368_bad_records/`
(mirroring the b0343 precedent) before any commit; the
`judges_registry.yaml` diff that the first run added was reverted
to the committed HEAD via `git show HEAD:judges_registry.yaml`
+ targeted Edit reverts. **No bogus record was committed to git.**

## Integrity

`scripts/integrity_check_b0368.py` was run; with 0 records to
validate this tick the check passes vacuously. The schema
validation, registry-resolution, hash-match, and uniqueness
clauses were not exercised. Result: **PASS**.

## Provenance and budget

- **Fresh fetches this tick:** 0 (reparse pass; raw bytes
  already on disk).
- **Cumulative today:** 19 / 2000 (~0.95%); budgets not
  exhausted.
- **B2 sync:** deferred to host (rclone not in sandbox).
- **SQLite ingestion:** deferred to host. The pre-existing
  `corpus.sqlite` B-tree corruption (FTS5 pages 84..99) persists
  per b0360..b0367 policy; the canonical source-of-truth remains
  `records/*.json`.

## Phase 5 progress

45 → 45 / 100-160 target (no change this tick).

## Recommendations

This batch surfaces a clear unblock: **parser_v0.3.2 vocabulary
widening** is now the highest-leverage next step.

1. **Judges-no-comma fix** — accept space-separated
   `<NAME> <TITLE>` tuples in `parse_judges()`. Likely a small
   change: detect the no-comma case (no `,` in `judges_text`,
   ≥2 title-token matches) and split on the title regex
   instead. This unlocks at least 3 of the 8 candidates above
   and very likely most of the 27 remaining 2022 ZMCC
   raw-on-disk candidates (the format is consistent within the
   year).
2. **Operative-verb vocabulary widening** — add verbs/phrases
   like `reverse the nullification`, `refuse to interpret`,
   `joinder is refused`, `objection is dismissed and ... allowed
   to proceed`, and interpretive declaratory patterns ("cannot
   be stopped or extended"). This unlocks the remaining 5
   candidates from this batch.

Subject to Peter's approval per the BRIEF.md non-negotiable on
parser vocabulary changes. Until then, raw bytes remain on disk
and re-parsing under v0.3.2 will be cost-free.

## Next tick

Three viable paths, in approximately decreasing leverage:

1. **Pause for parser_v0.3.2 approval** (highest leverage). The
   2022 ZMCC backlog will mostly require it; continued v0.3.1
   reparse on 2022 will yield poor returns.
2. **Continue v0.3.1 reparse on the next 2022 slice**
   (zmcc/2022/{23, 22, 21, 20, 18, 17, 16, 15} — yields likely
   to remain low; primarily catalogues more
   `parser_v0.3.1_judges_no_comma_unhandled` deferrals so that
   v0.3.2 has a complete target list).
3. **OCR pass** for the three
   `pdf_extraction_empty_likely_scanned` candidates accumulated
   to date (zmcc/2021/{15, 14}, zmcc/2025/19) or a single
   targeted fetch for zmcc/2023/17 PDF (currently deferred with
   `raw bytes not on disk`).

The b0367 next-tick plan referenced "next eight raw-on-disk
candidates after zmcc/2023/3 exhausts the 2023 queue" — that
plan was carried out this tick. The new finding (judges-no-
comma) supersedes it.
