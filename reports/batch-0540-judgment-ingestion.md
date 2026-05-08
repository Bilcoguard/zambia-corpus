# Batch 0540 — judgment-ingestion-worker (2026-05-08)

## Summary

Fifteenth substantive tick of the dedicated judgment-ingestion-worker
scheduled task. Pivoted to **ZMSC 2020 boundary probe + initial
sweep** per b0539 next-tick recommendation. The b0536 → b0539 ZMSC 2021
DESC sweep had hit a heavy scan-PDF cluster (8/8 OCR-pending in b0539);
pivoting to ZMSC 2020 lets us survey breadth before committing more
fetches to the OCR-pending cohort.

Probed 8 candidate nums spread across the 2020 num space
({50, 40, 30, 20, 15, 10, 5, 1}) via the
`https://zambialii.org/akn/zm/judgment/zmsc/2020/{N}/eng` pattern.
**All 8 fetched OK, zero 404s** — confirms ZMSC 2020 max-num ≥ 50
(upper boundary not yet probed).

**1 record written**, 7 deferred under
`pdf_extraction_empty_likely_scanned`.

| Field | Value |
|-------|-------|
| Phase | `phase_5_judgments` (post-completion ingestion via dedicated tick) |
| Batch | `0540` |
| Parser version | `0.3.2` (no parser changes) |
| Wrapper | `scripts/batch_0540_zmsc_parse.py` + reuse of `batch_0539_zmsc_fetch.py` for fetch (targets-driven, no script changes); `scripts/batch_0540_sqlite_insert.py` for DB insert |
| Started | 2026-05-08T15:42:??Z |
| Completed | 2026-05-08T15:5?:??Z |
| Wall-clock | ~12 min (under 20-min cap) |
| Fetches issued | 16 (8 HTML + 8 PDF) |
| Records written | 1 |
| Records deferred | 7 |
| Confirmed 404s | 0 |
| Daily fetch budget | 32 / 500 (cumulative_today after this tick: 16 from b0539 + 16 from b0540) |

## Per-candidate results

| court / num | result   | judgment date | PDF bytes  | reason / case name |
|-------------|----------|---------------|-----------:|-------------------|
| zmsc/2020/50 | deferred | 2020-03-26 | 9,511,017 | pdf_extraction_empty_likely_scanned |
| zmsc/2020/40 | deferred | 2020-02-28 | 6,197,297 | pdf_extraction_empty_likely_scanned |
| zmsc/2020/30 | deferred | 2020-05-15 | 4,261,406 | pdf_extraction_empty_likely_scanned |
| zmsc/2020/20 | deferred | 2020-02-04 | 5,248,240 | pdf_extraction_empty_likely_scanned |
| zmsc/2020/15 | deferred | 2020-01-02 | 5,651,538 | pdf_extraction_empty_likely_scanned |
| zmsc/2020/10 | deferred | 2020-05-14 | 6,118,694 | pdf_extraction_empty_likely_scanned |
| zmsc/2020/05 | deferred | 2020-01-14 | 3,256,554 | pdf_extraction_empty_likely_scanned |
| zmsc/2020/01 | **written** | 2020-03-11 | 2,641,685 | overturned — Hiteshbhai Partel v Kofi & Another |

## Written record details

**`judgment-zm-2020-zmsc-01-hiteshbhai-partel-v-kofi-another`**

- Citation: `[2020] ZMSC 1`
- Case number: `Appeal 13 of 2017`
- Court: Supreme Court of Zambia
- Date decided: `2020-03-11` (sourced from URL canonical
  `/eng@2020-03-11` and cross-verified against title parenthetical
  "(11 March 2020)" — see *Date-decided handling* below)
- Panel (3 judges, all resolved against existing canonical entries
  in `judges_registry.yaml`; no new aliases needed):
  - Wood JS — presiding
  - Musonda JS — concurring
  - Kajimanga JS — concurring
- Outcome: `overturned` (allowed enum)
- Outcome detail: "We set aside the judgment of the court below
  and enter…"
- Outcome source: HTML summary anchor (parser_v0.3.2 standard
  `set aside` operative-verb pattern)
- Issue tags (7): Property transfer tax; understatement of purchase
  price; illegality; effect on enforceability of contract; restitution
  of monies paid; specific performance; Statute of Frauds evidence.
- Source URL: `https://zambialii.org/akn/zm/judgment/zmsc/2020/1/eng@2020-03-11`
- raw_sha256 (PDF): `8c8c0808b8a59d61…` — verified against on-disk PDF
- source_hash (HTML): `sha256:72b529e0a9f0a862…`
- Parser version: `0.3.2`

### Date-decided handling

The parser_v0.3.2 metadata extraction for the "Judgment date" field
returned empty for this older 2020-format ZambiaLII page (the metadata
table layout differs from the 2021–2025 pages where the parser was
calibrated). The parser therefore wrote `date_decided: null`.

Post-parse, `date_decided` was populated from the canonical URL date
(`/eng@2020-03-11/`) and cross-verified against the title parenthetical
"(11 March 2020)" — both agreeing on `2020-03-11`. This is a
deterministic source-grounded derivation (the URL is recorded as
`source_url` in the same record) and is consistent with the integrity
contract's "no fabrication" rule. A future parser_v0.3.3+ should add
URL-date fallback to its `date_decided` extraction. Marked as a
gap-log item below for tracking.

## Integrity check

All required-field checks pass on the 1 written record:

- `id`, `type`, `court`, `citation`, `case_name`, `case_number`,
  `date_decided`, `judges`, `issue_tags`, `outcome`, `outcome_detail`,
  `reasoning_tags`, `key_statutes`, `raw_sha256`, `source_url` —
  all present and non-null.
- `judges` non-empty (3 entries).
- `issue_tags` non-empty (7 entries).
- `outcome` ∈ allowed enum (`overturned`).
- All 3 `judges[].name` resolve in `judges_registry.yaml` against
  existing canonical entries (Wood, Musonda, Kajimanga) — no new
  aliases or canonical entries added; registry unchanged.
- `raw_sha256` matches on-disk PDF (verified via fresh sha256 over
  `raw/zambialii/judgments/zmsc/2020/judgment-zm-2020-zmsc-01-*.pdf`).
- No duplicate IDs across the 156-record judgment corpus
  (was 155; +1 this tick).

7 deferred records: raw HTML+PDF pairs written to disk under
`raw/zambialii/judgments/zmsc/2020/` for OCR-backfill workflow.

## SQLite insertion

`scripts/batch_0540_sqlite_insert.py` (TMPDIR-routed atomic copy via
b0531 wrapper; idempotent INSERT OR REPLACE):

- `records`: 1845 → 1846 (+1)
- `judgments_meta`: 155 → 156 (+1)
- `records_fts`: deferred to host-side rebuild via
  `scripts/batch_0504_build_fts5.py` (b0517 precedent)

## What was NOT modified this tick

- `approvals.yaml` — untouched per human-only confirmation rule
- `judges_registry.yaml` — unchanged (all 3 judges already canonical)
- `corpus.sqlite` `records_fts` — deferred to host
- raw act/SI files — out of scope for this worker
- ZMSC 2021 sweep state — stays at 20-of-30+ as of b0539

## Cohort cumulative tracking (since b0504)

- 59 written (was 58 + 1 from this tick)
- 50 v0.3.3-pending deferred (unchanged — none of this tick's
  deferrals are interpretive-ratio family)
- 25 OCR-pending deferred (was 18; +7 this tick — all from ZMSC 2020)
- 26 confirmed 404 (unchanged)

## ZMSC year-status snapshot

- ZMSC 2026: in progress (ongoing year)
- ZMSC 2025: prior coverage
- ZMSC 2024: prior coverage
- ZMSC 2023: prior coverage
- ZMSC 2022: SWEEP COMPLETE (61 of 61 attempted as of b0535)
- ZMSC 2021: 20 of ~30+ valid attempted (1 written, 1 v0.3.3-pending
  deferred, 17 OCR-pending deferred, 1 internal 404 at num=33,
  plus 11 confirmed 404 above num=39 boundary)
- **ZMSC 2020 (NEW): 8 of ≥50 attempted (1 written, 7 OCR-pending
  deferred). Max-num ≥ 50 confirmed; upper boundary still unknown.**

## Gap-log items added

- ZMSC 2020 OCR-pending cohort (zmsc/2020/{50,40,30,20,15,10,5}):
  7 image-only PDFs deferred to OCR backfill workflow.
- ZMSC 2020 upper-boundary unprobed: max-num ≥ 50 confirmed; nums
  > 50 not yet HEAD-probed (defer to next tick).
- parser_v0.3.2 `date_decided` regression on older ZMSC HTML format
  (no "Judgment date" in metadata table). URL-date fallback should
  be added in v0.3.3.

## B2 sync

`B2 sync deferred to host (rclone not in sandbox)` — same as
b0504-onwards.

## Reproducibility

- Targets: `_work/b0540/targets.json`
- Fetcher: `scripts/batch_0539_zmsc_fetch.py _work/b0540/targets.json`
  (existing fetcher invoked with new targets file — no script
  changes needed)
- Parser: `python3 scripts/batch_0540_zmsc_parse.py`
- DB insert: `python3 scripts/batch_0540_sqlite_insert.py`
- Date-decided patch: deterministic URL-date derivation post-parse
  (one-line patch, see commit diff for the JSON record)

## Next-tick recommendation

Three competing options for the next judgment-ingestion tick:

1. **Continue ZMSC 2020 mid-range sweep** (e.g. nums {2, 3, 4, 6, 7,
   8, 9, 11}). Expected ratio similar to this tick (~1 written,
   ~7 OCR-pending) given the consistent scan-PDF dominance in older
   ZMSC years.
2. **Probe ZMSC 2020 upper boundary** (nums {60, 70, 80, 90, 100})
   to find the year-max. HEAD-only equivalents (single GET each)
   would consume ≤ 5 fetches.
3. **Pivot to ZMSC 2019 boundary probe** to keep moving the breadth
   frontier. Same approach as this tick: spread sample across the
   num space.

Recommend option 1 (continue ZMSC 2020 mid-range) — it accumulates
records monotonically and the deferred PDFs feed directly into the
growing OCR-pending cohort which is now substantive enough (25
records) to warrant escalating an OCR backfill workflow as a parallel
track.

approvals.yaml NOT modified per human-only confirmation rule.
