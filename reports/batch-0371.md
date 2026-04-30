# Batch 0371 — Phase 5 ZMCC reparse-first continuation under parser_v0.3.1

**Date (UTC):** 2026-04-30
**Phase:** phase_5_judgments (approved + incomplete)
**Parser version:** 0.3.1 (frozen baseline `scripts/batch_0360_parse.py`)
**Parser script:** `scripts/batch_0371_parse.py` — copied from
`scripts/batch_0370_parse.py` with TARGETS slice + `_work` directory
+ docstring/comment edits. Carries the b0368 defensive
`judges_no_comma` guard (additive, not a vocabulary change). No
outcome-vocabulary changes.
**Integrity check:** `scripts/integrity_check_b0371.py` — PASS
(1 record).

## Slice

Reparse-first triage continuation per `approvals.yaml`
`reparse_first` policy. b0370 swept the 2022 ZMCC DESC slice
{14, 13, 12, 11, 10, 9, 8, 6} (1 written / 7 deferred). This
batch completes the 2022 ZMCC raw-on-disk no-record backlog and
crosses into 2021. **Correction**: b0370's report stated
`zmcc/2022/7` had no raw on disk and skipped it in the DESC walk;
verification of `raw/zambialii/judgments/zmcc/2022/` in this
tick shows that raw HTML+PDF for `zmcc/2022/7` (Law Association
of Zambia v Attorney-General, /eng@2022-03-22) ARE on disk, so
it is included here.

| court | year | num | expression date | source |
|-------|------|-----|-----------------|--------|
| zmcc  | 2022 |   7 | 2022-03-22 | raw HTML+PDF on disk |
| zmcc  | 2022 |   5 | 2022-02-28 | raw HTML+PDF on disk |
| zmcc  | 2022 |   4 | 2022-02-25 | raw HTML+PDF on disk |
| zmcc  | 2022 |   3 | 2022-01-25 | raw HTML+PDF on disk |
| zmcc  | 2022 |   2 | 2022-01-27 | raw HTML+PDF on disk |
| zmcc  | 2022 |   1 | 2022-02-02 | raw HTML+PDF on disk |
| zmcc  | 2021 |  22 | 2021-02-12 | raw HTML+PDF on disk |
| zmcc  | 2021 |  21 | 2021-03-30 | raw HTML+PDF on disk |

Expression dates were verified via `grep` over each raw HTML's
canonical `/eng@YYYY-MM-DD` link before the slice was locked; no
fabrication.

## Result

- **Records written: 1** (Bozy Simutanda (as Attorney for HRH
  Chief Tafuña) v Kaoma and Anor [2021] ZMCC 22, decided
  2021-02-12, outcome `dismissed`, outcome_source `summary` — the
  high-confidence HTML summary path, no PDF fallback needed.
  Three-judge bench: Chibomba PC presiding, Musaluke and Mulenga
  concurring).
- **Records deferred: 7** with specific reason codes per
  `approvals.yaml deferral_reasons_locked`:
  - `html_no_summary_pdf_no_match` × 3
    (zmcc/2022/{7, 1}, zmcc/2021/21)
  - `parser_v0.3.1_judges_no_comma_unhandled` × 4
    (zmcc/2022/{5, 4, 3, 2})
- **Fresh fetches: 0** (all raw bytes already on disk from earlier
  batches; reparse-first protocol).
- **Cumulative today: ~13 / 2000 fetches (~0.65 %)** — well under
  the daily budget.

## New written record

| field | value |
|-------|-------|
| id | judgment-zm-2021-zmcc-22-bozy-simutanda-as-attorney-for-his-royal-highness |
| citation | [2021] ZMCC 22 |
| court | Constitutional Court of Zambia |
| case_name | Bozy Simutanda (As Attorney for HRH Chief Tafuña of the Tafuna Chieftaincy) v Kaoma (As Chief Mukupa Kaoma) and Another |
| case_number | 2020/CCZ/002 |
| date_decided | 2021-02-12 |
| outcome | dismissed |
| outcome_detail | Constitutional Court lacks jurisdiction over chieftaincy succession and criminal inquiries; amended petition dismissed with each party bearing costs |
| outcome_source | summary |
| judges | Chibomba (presiding, PC); Musaluke (concurring, JCC); Mulenga (concurring, JCC) |
| issue_tags | Constitutional Court jurisdiction; Article 128/Article 28; chieftaincy succession not a constitutional question; criminal/restitution outside CC jurisdiction; res judicata |
| source_hash | sha256:9837e53618ae552548e8d1eac148326524ff1dfe06f371e20e550a25f9a2ec35 |
| raw_sha256 | d2fc958426afa436b6a2fb59c7836103ac1086680f962899f965afa63a99c709 |
| parser_version | 0.3.1 |

## Phase 5 progress

- Before this tick: 46 / 100–160 target.
- After this tick: **47 / 100–160** target.
- Target window remains open; phase is approved + incomplete; worker
  does not flip approval flags.

## Integrity

`scripts/integrity_check_b0371.py` ran the standard Phase 5 checks
against `_work/b0371/parse_summary.json`:

- 20 required fields present on the written record.
- id pattern `^judgment-zm-[a-z0-9-]+$` matched.
- `date_decided` matches `YYYY-MM-DD`.
- `outcome` ∈ enum (dismissed).
- `court` ∈ enum (Constitutional Court of Zambia).
- `judges[*].role` ∈ enum (presiding, concurring, concurring).
- `Chibomba`, `Musaluke`, and `Mulenga` resolve against existing
  canonical entries in `judges_registry.yaml`. Minor registry
  update: the `Chibomba` canonical gained one new title alias
  (`JJS`) and one new aliased token (`Chibomba JJS`) — the raw
  HTML for [2021] ZMCC 22 used the `JJS` spelling, which the
  registry had not previously recorded for this canonical. No
  new canonical names were added; `Musaluke` and `Mulenga` were
  fully covered by existing aliases.
- ≥ 1 `issue_tag` present (5 tags from the HTML flynote block).
- `source_hash` matches the on-disk raw HTML byte-for-byte.
- `raw_sha256` matches the on-disk raw PDF byte-for-byte.
- `id` is globally unique within `records/judgments/`.
- `outcome_detail` passes the safety filter (no blacklisted
  substrings, ≥ 12 alphabetic chars, no leading lowercase mid-word
  fragment).

Result: **PASS**.

## Recommendations

Four-tick stable signal across b0368 → b0371: 32 candidates →
2 written (yield ≈ 6 %). The 1-record yield this tick rescued an
under-represented item: a 2021 ZMCC three-judge majority opinion
where the HTML summary block survived (the rare high-confidence
path). The 4 × `parser_v0.3.1_judges_no_comma_unhandled` deferrals
in this slice (all of zmcc/2022/{5, 4, 3, 2}) reinforce the
diagnosis that the 2022 ZMCC corpus is dominated by the
space-separated judges format which the v0.3.1 comma-splitter
cannot decode.

The 2022 ZMCC raw-on-disk no-record backlog is now empty
(zmcc/2022 raw set spans 1–34; written set is {12, 19, 26, 28,
29}; deferred set is {1–11, 13–18, 20–25, 27, 30–34}). Future
reparse ticks should now focus on:

1. **Continue the 2021 ZMCC backlog.** Remaining unwritten
   raw-on-disk: zmcc/2021/{12, 14, 15, 18, 19} (zmcc/2021/15 and
   /14 are already classified `pdf_extraction_empty_likely_scanned`;
   zmcc/2021/12, /18, /19 are next-up DESC candidates).
2. **OCR pass** for the four `pdf_extraction_empty_likely_scanned`
   candidates (zmcc/2021/{15, 14}, zmcc/2025/19, zmcc/2022/16).
3. **Parser v0.3.2 vocabulary widening** (judges-no-comma fix +
   operative-verb additions for the 2022 election-petition style)
   remains the dominant unblock for the 18+ deferred 2022 ZMCC
   targets — subject to Peter's approval per BRIEF.md
   non-negotiable on parser vocabulary changes.

## Operational notes

- B2 sync deferred to host (rclone is not present in the sandbox).
- SQLite ingestion deferred to host (`corpus.sqlite` FTS5 index
  reports malformed disk image on read; canonical source-of-truth
  remains `records/*.json`, per the b0351..b0370 policy).
- Wall-clock comfortably under the 20-minute tick budget.
- Worker did not modify `approvals.yaml` (non-negotiable #5).
- Documentation correction logged: b0370 incorrectly reported
  `zmcc/2022/7` as having no raw on disk; this batch confirms the
  raw HTML+PDF are present and parses the candidate (deferred
  `html_no_summary_pdf_no_match`).
