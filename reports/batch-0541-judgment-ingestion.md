# Batch 0541 — judgment-ingestion-worker (2026-05-08)

## Summary

Sixteenth substantive tick of the dedicated judgment-ingestion-worker
scheduled task. Continued **ZMSC 2020 mid-range DESC sweep** per b0540
next-tick recommendation: nums {2, 3, 4, 6, 7, 8, 9, 11}. 8 candidate
nums, 16 fetches issued.

**0 records written, 8 deferred** — 7 under
`pdf_extraction_empty_likely_scanned` (image-only scanned PDFs) and 1
under `html_no_summary_pdf_no_match` (PDF text extracted but neither
the HTML summary nor PDF tail anchors matched any operative-verb
outcome pattern in parser_v0.3.2).

The scan-PDF dominance pattern documented in b0536 → b0540 reproduces
again in this cohort. Combined with the b0539 (8/8 OCR-pending in
ZMSC 2021 nums 27..20) and b0540 (7/8 OCR-pending in ZMSC 2020 spread
sample) cohorts, the OCR-pending backlog is now **33 records**.

| Field | Value |
|-------|-------|
| Phase | `phase_5_judgments` (post-completion ingestion via dedicated tick) |
| Batch | `0541` |
| Parser version | `0.3.2` (no parser changes) |
| Wrapper | `scripts/batch_0541_zmsc_fetch.py`, `scripts/batch_0541_zmsc_parse.py` |
| Started | 2026-05-08T15:55Z (after b0540 push) |
| Completed | 2026-05-08T16:11Z |
| Wall-clock | ~16 min (under 20-min cap) |
| Fetches issued | 16 (8 HTML + 8 PDF) |
| Records written | 0 |
| Records deferred | 8 |
| Confirmed 404s | 0 |
| Daily fetch budget | 48 / 500 (cumulative_today: 32 from b0540 + 16 from b0541) |

## Per-candidate results

| court / num | result   | judgment date | PDF bytes  | reason |
|-------------|----------|---------------|-----------:|--------|
| zmsc/2020/02 | deferred | 2020-03-18 | 3,322,544 | html_no_summary_pdf_no_match (PDF text extracted; no operative-verb anchor matched in v0.3.2) |
| zmsc/2020/03 | deferred | 2020-01-09 | 8,000,211 | pdf_extraction_empty_likely_scanned |
| zmsc/2020/04 | deferred | 2020-03-03 | 4,709,269 | pdf_extraction_empty_likely_scanned |
| zmsc/2020/06 | deferred | 2020-03-31 | 4,544,942 | pdf_extraction_empty_likely_scanned |
| zmsc/2020/07 | deferred | 2020-05-14 | 8,682,175 | pdf_extraction_empty_likely_scanned |
| zmsc/2020/08 | deferred | 2020-05-13 | 2,989,470 | pdf_extraction_empty_likely_scanned |
| zmsc/2020/09 | deferred | 2020-05-13 | 6,233,014 | pdf_extraction_empty_likely_scanned |
| zmsc/2020/11 | deferred | 2020-05-13 | 3,336,547 | pdf_extraction_empty_likely_scanned |

Total deferred PDF bytes: ~41.8 MB. Of these, ~38.5 MB are scanned
(image-only) and ~3.3 MB are textual but lacked an outcome anchor.

## Notable: zmsc/2020/02 (Chen Den Limited & Others v IMS Financial Services Ltd)

Single deferral under `html_no_summary_pdf_no_match`. The HTML summary
field stated:

> "Single judge lacked jurisdiction to dismiss an appeal filed before
>  S.I. No.26/2012; the statutory instrument is not retrospective."

This is a flynote-style legal-issue summary (not an operative outcome
verb), and the PDF tail extracted-text did not contain any of the
parser_v0.3.2 anchor patterns ("appeal allowed/dismissed", "we
dismiss/allow/uphold/grant/refuse/set aside", "is hereby set aside/
quashed", "it is ordered that", "petition is dismissed", "conviction
is upheld", "court refused"). This is a candidate for parser_v0.3.3
which would extend the operative-verb anchor patterns to handle:

- Issue summaries paired with retrospective/prospective rulings
- "the appeal succeeds/fails" variants
- "the matter is remitted to the court below"
- Implicit set-asides: "we hold that the [lower judge / single judge /
  registrar] lacked jurisdiction" → likely outcome=set-aside, but
  v0.3.2 does not infer this without an explicit anchor.

Per non-fabrication rule: **NOT** writing a record where the outcome
cannot be deterministically anchored from the source text. Deferred
to v0.3.3+.

## Integrity checks

`scripts/integrity_check_b0541.py` — 17 / 17 PASSED:

- Corpus-wide duplicate-ID check: 156 unique judgment IDs, 0 duplicates.
- 8 raw HTML on-disk verifications (one per deferred candidate)
- 8 raw PDF on-disk verifications (one per deferred candidate)

The seven required per-record checks from SKILL.md are trivially N/A
(0 records written this tick).

## State changes

- `corpus.sqlite` — UNCHANGED (zero records written; record count remains
  at 1845, judgments_meta count remains at 156).
- `judges_registry.yaml` — UNCHANGED (no new judges; deferred records
  do not invoke judge resolution).
- `records/judgments/` tree — UNCHANGED.
- `raw/zambialii/judgments/zmsc/2020/` — 8 new HTML+PDF pairs added
  (16 files, ~41.8 MB total).
- `approvals.yaml` — NOT modified (per human-only confirmation rule;
  this worker does not touch approvals).

## Cohort cumulative tracking (since b0504)

- 59 written (unchanged from b0540)
- 50 v0.3.3-pending deferred (unchanged)
- 33 OCR-pending deferred (was 25; +7 from this tick — all from
  ZMSC 2020 mid-range)
- 1 v0.3.3-pending deferred (this tick: zmsc/2020/2)
- 26 confirmed 404 (unchanged)

The OCR-pending cohort (33 records, ~243 MB total scanned PDFs) is now
clearly the dominant backlog and increasingly warrants escalating an
OCR backfill workflow as a parallel track.

## ZMSC 2020 sweep status after b0541

| metric | value |
|--------|-------|
| Total nums attempted | 16 of ≥50 |
| Written | 1 (zmsc/2020/01) |
| OCR-pending deferred | 14 (zmsc/2020/{50,40,30,20,15,10,5,3,4,6,7,8,9,11}) |
| v0.3.3-pending deferred | 1 (zmsc/2020/02) |
| Confirmed 404 | 0 |
| Internal 404 | 0 |
| Max-num confirmed | ≥ 50 (upper boundary still unprobed) |

Sweep coverage is now fairly dense in low nums (1–11 fully attempted)
plus a sparse spread sample at higher nums (15, 20, 30, 40, 50). Mid
nums (12–14, 16–19, 21–29, 31–39, 41–49) and upper-boundary nums
(>50) remain unattempted.

## Next-tick recommendation

Two parallel options, both with similar low expected-yield ratios:

1. **Continue ZMSC 2020 fill-in DESC sweep** — nums {19, 18, 17, 16,
   14, 13, 12, 25}. Expectation: similar ~1-of-8 written ratio
   based on b0539+b0540+b0541 trend (3/24 ≈ 12.5% written).
2. **Probe ZMSC 2020 upper boundary** — HEAD-only on nums
   {51, 55, 60, 65, 70, 75, 80, 90} to find the year-max num. This
   would consume only 8 fetches (no PDFs) and would tell us how much
   more of the year remains. If max-num is ~55, the year is small
   enough to finish in 4–5 more sweep ticks; if it's 80+, the OCR
   backfill becomes the only realistic path forward.

**Recommended: option 2 (boundary probe).** It's cheaper (8 fetches
vs 16) and gives information that constrains all future planning for
the year. The OCR-pending backlog (33 records) is now substantive
enough that low-yield text-PDF sweeps are no longer the highest-value
work.

## Renumbering note

This batch uses `b0541` (continuation from b0540). No collision with
the main worker — b0540 was the last numbered batch and the
phase-8-nightly-reverify pool tap (b0538) is independent.

## B2 sync

Deferred to host (rclone not available in this sandbox). Per b0517+
precedent, the host-side sync runs separately on a Mac with rclone
installed; this worker logs the deferral and moves on.
