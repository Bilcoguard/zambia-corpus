# Batch 0372 — Phase 5 ZMCC reparse-first continuation under parser_v0.3.1

**Date (UTC):** 2026-04-30
**Phase:** phase_5_judgments (approved + incomplete)
**Parser version:** 0.3.1 (frozen baseline `scripts/batch_0360_parse.py`)
**Parser script:** `scripts/batch_0372_parse.py` — copied from
`scripts/batch_0371_parse.py` with TARGETS slice + `_work` directory
+ docstring/comment edits. Carries the b0368 defensive
`judges_no_comma` guard (additive, not a vocabulary change). No
outcome-vocabulary changes.
**Integrity check:** `scripts/integrity_check_b0372.py` — PASS
(1 record).

## Slice

Reparse-first triage continuation per `approvals.yaml`
`reparse_first` policy. b0371 took
{2022/7, 2022/5, 2022/4, 2022/3, 2022/2, 2022/1, 2021/22, 2021/21}
(1 written = zmcc/2021/22 Bozy Simutanda, 7 deferred). This batch
attempts the next 2021 ZMCC DESC candidates that have not yet been
re-parsed under v0.3.1 + judges_no_comma guard.

| court | year | num | expression date | source |
|-------|------|-----|-----------------|--------|
| zmcc  | 2021 |  19 | 2021-03-25 | raw HTML+PDF on disk |
| zmcc  | 2021 |  18 | 2021-08-18 | raw HTML+PDF on disk |
| zmcc  | 2021 |  12 | 2021-06-30 | raw HTML+PDF on disk |

Excluded from the slice (deliberate): zmcc/2021/{15, 14} are
already classified `pdf_extraction_empty_likely_scanned` (parser
cannot help — needs OCR pass per b0371 recommendation #2);
zmcc/2021/21 was just attempted in b0371 (deferred
`html_no_summary_pdf_no_match`) and re-running v0.3.1 would yield
an identical deferral.

Slice size 3 (under MAX_BATCH_SIZE=8): the 2021 ZMCC raw-on-disk
no-record backlog has only these three v0.3.1-amenable candidates
remaining; the batch is intentionally not padded with
already-classified deferreds.

Expression dates were verified via `grep` over each raw HTML's
canonical `/eng@YYYY-MM-DD` link before the slice was locked.

## Result

- **Records written: 1** (Wang Shunxue and Attorney General and
  Another [2021] ZMCC 19, decided 2021-03-25, outcome `dismissed`,
  outcome_source `pdf-tail-2pages` — the PDF final-2-pages fallback
  introduced in parser v0.3.1 produced the safe match. Single-judge
  bench: Munalula JCC).
- **Records deferred: 2** with specific reason codes per
  `approvals.yaml deferral_reasons_locked`:
  - `html_no_summary_pdf_no_match` × 2
    (zmcc/2021/{18, 12})
- **Fresh fetches: 0** (all raw bytes already on disk from earlier
  batches; reparse-first protocol).

## New written record

| field | value |
|-------|-------|
| id | judgment-zm-2021-zmcc-19-wang-shunxue-and-attorney-general-and-another |
| citation | [2021] ZMCC 19 |
| court | Constitutional Court of Zambia |
| case_name | WANG SHUNXUE AND ATTORNEY GENERAL AND ANOTHER |
| case_number | 2021/CCZ/003 |
| date_decided | 2021-03-25 |
| outcome | dismissed |
| outcome_detail | The application is accordingly dismissed |
| outcome_source | pdf-tail-2pages |
| judges | Munalula (presiding, JCC) |
| issue_tags | Constitutional law; stay of criminal proceedings; private prosecution; Article 180(8) DPP consent; interlocutory relief; jurisdiction of single judge; three-pronged test (serious question, irreparable harm, balance of convenience) |
| source_hash | sha256:cbaa0aaf21bfcd26b980a987162323d2c747c774cd3ce5437f6a2e0ee01a8fab |
| raw_sha256 | 4f9320d2237efdd9d319df42f56797b7ce010819a74dcc98b1823858f34fb3a4 |
| parser_version | 0.3.1 |

## Phase 5 progress

- Before this tick: 47 / 100–160 target.
- After this tick: **48 / 100–160** target.
- Target window remains open; phase is approved + incomplete; worker
  does not flip approval flags.

## Integrity

`scripts/integrity_check_b0372.py` ran the standard Phase 5 checks
against `_work/b0372/parse_summary.json`:

- 20 required fields present on the written record.
- id pattern `^judgment-zm-[a-z0-9-]+$` matched.
- `date_decided` matches `YYYY-MM-DD`.
- `outcome` ∈ enum (dismissed).
- `court` ∈ enum (Constitutional Court of Zambia).
- `judges[*].role` ∈ enum (presiding).
- `Munalula` resolves against `judges_registry.yaml` (canonical
  entry exists from prior batches; the `Munalula JCC` alias and
  the `JCC` title were already present from earlier ZMCC batches,
  so no registry write was needed this tick). No new canonical
  names were added.
- ≥ 1 `issue_tag` present (7 tags from the HTML flynote block).
- `source_hash` matches the on-disk raw HTML byte-for-byte.
- `raw_sha256` matches the on-disk raw PDF byte-for-byte.
- `id` is globally unique within `records/judgments/`.
- `outcome_detail` passes the safety filter (no blacklisted
  substrings, ≥ 12 alphabetic chars, no leading lowercase mid-word
  fragment).

Result: **PASS**.

## 2021 ZMCC raw-on-disk no-record backlog status

After this tick the 2021 ZMCC raw-on-disk no-record set is now
fully classified under v0.3.1:

- Written across all batches: zmcc/2021/{13, 16, 17, 19, 20, 22,
  23, 24}.
- Deferred `pdf_extraction_empty_likely_scanned` (OCR-pending):
  zmcc/2021/{14, 15}.
- Deferred `html_no_summary_pdf_no_match` under v0.3.1:
  zmcc/2021/{12, 18, 21}.

The 2021 ZMCC DESC backlog is **empty for v0.3.1 reparse**. The
3 OCR-pending candidates (zmcc/2021/{14, 15}, zmcc/2025/19,
zmcc/2022/16 — total 4) require an OCR pipeline that is outside
v0.3.1 vocabulary. The remaining ~60 raw-on-disk no-record
candidates in 2022/2024/2025 are dominated by the
`parser_v0.3.1_judges_no_comma_unhandled` and
`html_no_summary_pdf_no_match` deferral codes, both of which
require parser v0.3.2 vocabulary widening — subject to Peter's
approval per BRIEF.md non-negotiable on parser changes.

## Recommendations

Five-tick stable signal across b0368 → b0372: 35 candidates →
3 written (yield ≈ 8.6%). The reparse-first policy has now exhausted
the v0.3.1-amenable inventory of the 2021 ZMCC backlog. Future
ticks have three mutually exclusive options, in priority order:

1. **Parser v0.3.2 vocabulary widening (highest leverage).** The
   ~60 remaining 2022/2024/2025 raw-on-disk no-record candidates
   are dominated by judges-no-comma and operative-verb gaps that
   v0.3.2 was scoped to address. Subject to Peter's approval per
   BRIEF.md non-negotiable on parser vocabulary changes.
2. **OCR pipeline for the 4 `pdf_extraction_empty_likely_scanned`
   candidates** (zmcc/2021/{14, 15}, zmcc/2025/19, zmcc/2022/16).
   Smaller surface area; complementary to v0.3.2.
3. **Resume fresh DESC sweep on a non-ZMCC court** (zmsc, zmca,
   zmhc) under v0.3.1. The reparse-first inventory is now empty
   for ZMCC, so this would shift fetch budget back into discovery.
   Per `reparse_first_note`, only valid once no addressable
   deferreds remain — which is the case for v0.3.1 ZMCC.

## Operational notes

- B2 sync deferred to host (rclone is not present in the sandbox).
- SQLite ingestion deferred to host (`corpus.sqlite` FTS5 index
  reports malformed disk image on read; canonical source-of-truth
  remains `records/*.json`, per the b0351..b0371 policy).
- Wall-clock comfortably under the 20-minute tick budget.
- Worker did not modify `approvals.yaml` (non-negotiable #5).
