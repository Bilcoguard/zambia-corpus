# Batch 0539 — judgment-ingestion-worker (2026-05-08)

## Summary

Fourteenth substantive tick of the dedicated judgment-ingestion-worker
scheduled task. Continued the ZMSC 2021 most-recent-first DESC sweep
per the b0536 next-tick recommendation. Probed 8 candidate nums
(27..20) via the `https://zambialii.org/akn/zm/judgment/zmsc/2021/{N}/eng`
pattern; **all 8 fetched OK, zero 404s**.

**No records written.** All 8 candidates are image-only scanned PDFs
that the v0.3.2 parser cannot extract operative text from; deferred
under reason code `pdf_extraction_empty_likely_scanned` for the OCR
backfill cohort.

| Field | Value |
|-------|-------|
| Phase | `phase_5_judgments` (post-completion ingestion via dedicated tick) |
| Batch | `0539` (renumbered from b0538 mid-tick — see *Batch number collision* below) |
| Parser version | `0.3.2` (no parser changes) |
| Wrapper | `scripts/batch_0539_zmsc_{fetch,parse}.py` (thin wrappers around `batch_0506_zmsc_{fetch,parse}.py`) |
| Started | 2026-05-08T07:18:??Z |
| Completed | 2026-05-08T07:25:08Z |
| Wall-clock | ~7 min (well under 20-min cap) |
| Fetches issued | 16 (8 HTML + 8 PDF) |
| Records written | 0 |
| Records deferred | 8 |
| Confirmed 404s | 0 |
| Daily fetch budget | 16 / 500 (cumulative_today after this tick) |

## Batch number collision

A scheduling collision was discovered mid-tick: the main corpus worker
had already claimed `batch-0538` for its third Phase 8 nightly reverify
(executed 2026-05-08T07:18:16Z — ~3 minutes before this
judgment-ingestion tick's parse step completed). All artefacts were
renumbered from `b0538` → `b0539` before commit:

- `_work/b0538/` → `_work/b0539/`
- `scripts/batch_0538_zmsc_fetch.py` → `scripts/batch_0539_zmsc_fetch.py`
- `scripts/batch_0538_zmsc_parse.py` → `scripts/batch_0539_zmsc_parse.py`
- `scripts/integrity_check_b0539.py` (new this tick)
- `reports/batch-0539-judgment-ingestion.md` (this file)

This mirrors the b0524 collision (Phase 8 reverify vs. judgment-ingestion
ZMSC 2022 sweep) precedent.

## Per-candidate results

| court / num | result   | judgment date | PDF bytes  | reason / case name |
|-------------|----------|---------------|-----------:|-------------------|
| zmsc/2021/27 | deferred | 2021-04-21 | 11,718,368 | pdf_extraction_empty_likely_scanned — Chishimba Chonya v The People |
| zmsc/2021/26 | deferred | 2021-04-21 |  8,190,760 | pdf_extraction_empty_likely_scanned — William Mufungulwa Sipalo v The People |
| zmsc/2021/25 | deferred | 2021-04-21 | 11,767,265 | pdf_extraction_empty_likely_scanned — Derrick Mungaila & 3 ors v The People |
| zmsc/2021/24 | deferred | 2021-04-21 |  9,111,542 | pdf_extraction_empty_likely_scanned — James Sichimba v The People |
| zmsc/2021/23 | deferred | 2021-04-14 |  2,813,164 | pdf_extraction_empty_likely_scanned — Ronald Musonda & 2 ors v The People |
| zmsc/2021/22 | deferred | 2021-04-23 |  3,868,798 | pdf_extraction_empty_likely_scanned — Peter Sampa v The People |
| zmsc/2021/21 | deferred | 2021-04-23 |  6,425,803 | pdf_extraction_empty_likely_scanned — Chancy Mtambalika & anor v The People |
| zmsc/2021/20 | deferred | 2021-04-23 |  7,369,885 | pdf_extraction_empty_likely_scanned — Mwiya Zunga Zunga & anor v The People |

Pattern note: **all 8 candidates are criminal appeals against the State**
(`v The People`) clustered in a single fortnight of April 2021. Total
deferred PDF bytes ≈ 62 MB. This reproduces and extends the b0536
finding that the early-2021 ZMSC cohort is overwhelmingly scan-only.

## Integrity check

`scripts/integrity_check_b0539.py` — 17 / 17 PASS:

- corpus-wide duplicate-id check across `records/judgments/**/*.json`
  (155 unique IDs; unchanged from b0536).
- 8 raw-HTML files exist and are unique-per-num under
  `raw/zambialii/judgments/zmsc/2021/`.
- 8 raw-PDF files exist and are unique-per-num under
  `raw/zambialii/judgments/zmsc/2021/`.

Per-record SKILL.md required-field checks were trivially N/A (zero
records written).

## What was NOT modified this tick

- `corpus.sqlite` — unchanged. No INSERT or REPLACE issued.
  `records` count remains 1845; `judgments_meta` remains 155.
- `judges_registry.yaml` — unchanged. Zero judge resolutions (zero
  records written).
- `records/judgments/**/*.json` — no new files written; no existing
  files modified.
- `approvals.yaml` — NOT modified per human-only confirmation rule.

## What WAS modified this tick

- `raw/zambialii/judgments/zmsc/2021/` — 8 new HTML+PDF pairs
  (16 files) for nums {27..20}.
- `_work/b0539/` — `targets.json`, `fetch_results.json`,
  `parse_summary.json`.
- `scripts/batch_0539_zmsc_fetch.py`, `scripts/batch_0539_zmsc_parse.py`,
  `scripts/integrity_check_b0539.py` — new wrapper / validator scripts.
- `gaps.md` — new "## Batch 0539 update" section with full per-num table.
- `costs.log` — 3 new lines (TSV summary, JSON detail, B2 sync deferred).
- `provenance.log` — 19 new lines (1 batch summary, 8 FETCH, 8 DEFER,
  1 REGISTRY, 1 SQLITE, 1 INTEGRITY).
- `reports/batch-0539-judgment-ingestion.md` — this file.

## Cohort cumulative since b0504

| Cohort                                        | Count |
|-----------------------------------------------|------:|
| Records written                               |    58 |
| Deferred — `raw-on-disk-pending-v0.3.3` family|    50 |
| Deferred — `pdf_extraction_empty_likely_scanned` (OCR-pending) |    18 |
| Confirmed 404s                                |    26 |

OCR-pending cohort has grown materially: 4 → 10 (b0536) → 18 (b0539).

## ZMSC 2021 status after b0539

- 20 of ~30+ valid (non-404) attempts probed.
- 1 written (zmsc/2021/35 — *Hakainde Hichilema v The Attorney General*).
- 1 v0.3.3-pending deferred.
- 17 OCR-pending deferred (zmsc/2021/{34,32,31,30,29,28,27,26,25,24,23,22,21,20}).
- 1 internal 404 at num=33.
- 11 confirmed 404 above max-num=39 boundary (established in b0535).

## B2 sync

`rclone` not in sandbox → B2 sync deferred to host (per b0506+
precedent).

## Next-tick recommendation

The early-2021 ZMSC cohort is overwhelmingly scan-only PDFs that
v0.3.2 cannot extract. Two parallel options for the next tick:

1. **Continue ZMSC 2021 DESC sweep nums {19..12}** (skipping known
   internal 404 at num=33). Expectation: similar scan-PDF ratio; will
   keep growing the OCR-pending cohort but will eventually find the
   2021 lower-num boundary.
2. **Pivot to ZMSC 2020 boundary probe** (HEAD-only, low fetch cost)
   to identify the year-max num for 2020 and start a fresh DESC sweep
   there.

Either way, the 18-record OCR-pending cohort is now substantive enough
to warrant escalating the OCR backfill workflow as a parallel track —
this would convert the OCR-pending cohort into either written records
or a more specific "OCR-attempted-but-still-empty" deferral.

## Reproducibility

- Targets: `_work/b0539/targets.json`.
- Re-runnable via:
    `python3 scripts/batch_0539_zmsc_fetch.py`
    `python3 scripts/batch_0539_zmsc_parse.py`
    `python3 scripts/integrity_check_b0539.py`
- Full per-fetch JSON: `_work/b0539/fetch_results.json`.
- Full parse summary: `_work/b0539/parse_summary.json`.

## User-Agent and rate-limit compliance

- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- Per-request delay: 5 s (between every HTTP fetch, per
  `zambialii_seconds_between_requests`).
- robots.txt: honoured.
