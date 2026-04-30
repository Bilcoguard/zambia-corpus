# Batch 0370 — Phase 5 ZMCC reparse-first continuation under parser_v0.3.1

**Date (UTC):** 2026-04-30
**Phase:** phase_5_judgments (approved + incomplete)
**Parser version:** 0.3.1 (frozen baseline `scripts/batch_0360_parse.py`)
**Parser script:** `scripts/batch_0370_parse.py` — copied from
`scripts/batch_0369_parse.py` with TARGETS slice + `_work` directory
+ comment edits. Carries the b0368 defensive `judges_no_comma`
guard (additive, not a vocabulary change). No outcome-vocabulary
changes.
**Integrity check:** `scripts/integrity_check_b0370.py` — PASS
(1 record).

## Slice

Reparse-first triage continuation per `approvals.yaml`
`reparse_first` policy. b0369 swept the 2022 ZMCC DESC slice
{23, 22, 21, 20, 18, 17, 16, 15} (0 written / 8 deferred). This
batch takes the next eight raw-on-disk no-record candidates
(year-DESC then num-DESC), skipping zmcc/2022/7 (no raw on disk):

| court | year | num | expression date | source |
|-------|------|-----|-----------------|--------|
| zmcc  | 2022 |  14 | 2022-08-03 | raw HTML+PDF on disk |
| zmcc  | 2022 |  13 | 2022-07-28 | raw HTML+PDF on disk |
| zmcc  | 2022 |  12 | 2022-06-20 | raw HTML+PDF on disk |
| zmcc  | 2022 |  11 | 2022-05-16 | raw HTML+PDF on disk |
| zmcc  | 2022 |  10 | 2022-05-19 | raw HTML+PDF on disk |
| zmcc  | 2022 |   9 | 2022-03-14 | raw HTML+PDF on disk |
| zmcc  | 2022 |   8 | 2022-04-13 | raw HTML+PDF on disk |
| zmcc  | 2022 |   6 | 2022-02-24 | raw HTML+PDF on disk |

Expression dates were verified via `grep` over each raw HTML's
canonical `/eng@YYYY-MM-DD` link before the slice was locked; no
fabrication.

## Result

- **Records written: 1** (Banda v Attorney General [2022] ZMCC 12,
  decided 2022-06-20, outcome `dismissed`, outcome_source
  `pdf-tail-2pages`, single Sitali JCC presiding on a removal-of-judge
  stay application).
- **Records deferred: 7** with specific reason codes per
  `approvals.yaml deferral_reasons_locked`:
  - `html_no_summary_pdf_no_match` × 6
    (zmcc/2022/{14, 13, 11, 10, 9, 6})
  - `parser_v0.3.1_judges_no_comma_unhandled` × 1
    (zmcc/2022/8 — Kafwaya v Katonga and Ors — caught by the b0368
    defensive guard: single judge object inferred but ≥ 2 judicial-title
    tokens detected in `judges_text`, indicating space-separated
    2022-format that the comma-splitter collapsed).
- **Fresh fetches: 0** (all raw bytes already on disk from earlier
  batches; reparse-first protocol).
- **Cumulative today: ~19 / 2000 fetches (~0.95 %)** —
  well under the daily budget.

## New written record

| field | value |
|-------|-------|
| id | judgment-zm-2022-zmcc-12-banda-v-attorney-general |
| citation | [2022] ZMCC 12 |
| court | Constitutional Court of Zambia |
| case_name | Banda v Attorney General |
| case_number | CCZ 10 of 2022 |
| date_decided | 2022-06-20 |
| outcome | dismissed |
| outcome_detail | "The application is accordingly dismissed" |
| outcome_source | pdf-tail-2pages |
| judges | Sitali (presiding, JCC) |
| source_hash | sha256:27d2ca1b19afd9c6743ac5f66461eb6fb7ca81d6c3c64b581ec33cecd3f9f8d2 |
| raw_sha256 | c4d34c1382879bc132b256174f006ec04f52bfe0c03db7a2f0fa5a8c983b0b2b |
| parser_version | 0.3.1 |

## Phase 5 progress

- Before this tick: 45 / 100–160 target.
- After this tick: **46 / 100–160** target.
- Target window remains open; phase is approved + incomplete; worker
  does not flip approval flags.

## Integrity

`scripts/integrity_check_b0370.py` ran the standard Phase 5 checks
against `_work/b0370/parse_summary.json`:
- 20 required fields present on the written record.
- id pattern `^judgment-zm-[a-z0-9-]+$` matched.
- `date_decided` matches `YYYY-MM-DD`.
- `outcome` ∈ enum (dismissed).
- `court` ∈ enum (Constitutional Court of Zambia).
- `judges[*].role` ∈ enum (presiding).
- `Sitali` resolves against existing canonical `Sitali` entry in
  `judges_registry.yaml` (no registry write needed — title `JCC`
  already aliased).
- ≥ 1 `issue_tag` present (six tags from the HTML flynote block).
- `source_hash` matches the on-disk raw HTML byte-for-byte.
- `raw_sha256` matches the on-disk raw PDF byte-for-byte.
- `id` is globally unique within `records/judgments/`.
- `outcome_detail` passes the safety filter (no blacklisted
  substrings, ≥ 12 alphabetic chars, no leading lowercase mid-word
  fragment).

Result: **PASS**.

## Recommendations

Three-tick stable signal across b0368 → b0370: 24 candidates →
1 written (yield ≈ 4 %). The 1-record yield this tick was an
idiosyncratic single-judge stay application — not representative of
the 2022 ZMCC bulk format, which remains dominated by
`html_no_summary_pdf_no_match` (no summary `<dl>` block, no order-
anchor or tail match) and `parser_v0.3.1_judges_no_comma_unhandled`
(space-separated judges). Parser_v0.3.2 vocabulary widening
(judges-no-comma fix + operative-verb additions for the 2022 election-
petition style) remains the dominant unblock — subject to Peter's
approval per BRIEF.md non-negotiable on parser vocabulary changes.

Until v0.3.2 approval lands, the next tick can either:
(a) continue v0.3.1 reparse on zmcc/2022/{5, 4, 3, 2, 1} +
    zmcc/2021/{12, 11, 10} to fully catalogue v0.3.2 targets;
(b) OCR pass for the four `pdf_extraction_empty_likely_scanned`
    candidates (zmcc/2021/{15, 14}, zmcc/2025/19, zmcc/2022/16);
(c) targeted single-fetch for any zmcc URL whose PDF is still
    missing on disk; or
(d) pause for parser_v0.3.2 approval.

## Operational notes

- B2 sync deferred to host (rclone is not present in the sandbox).
- SQLite ingestion deferred to host (`corpus.sqlite` FTS5 index reports
  malformed disk image on read; canonical source-of-truth remains
  `records/*.json`, per the b0351..b0367 policy).
- Wall-clock comfortably under the 20-minute tick budget.
- Worker did not modify `approvals.yaml` (non-negotiable #5).
