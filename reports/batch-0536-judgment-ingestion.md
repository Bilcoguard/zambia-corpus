# Batch 0536 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker (scheduled task `judgment-ingestion`)
- **Wall-clock window**: 2026-05-07T07:07Z..07:15Z (UTC, ~8 min, well under 20 min target)
- **Phase**: Phase 5 dedicated post-completion ingestion (continued).
- **Parser**: v0.3.2 baseline frozen at scripts/batch_0498_parse.py + scripts/batch_0506_zmsc_parse.py wrapper. No parser modifications this tick.

## Tick decision (priority order)

a. **REPARSE DEFERRED** — gaps.md cohort of **50** raw-on-disk
   deferrals are flagged `raw-on-disk-pending-v0.3.3` (parser
   v0.3.2 already attempted; awaiting v0.3.3 patterns). Reparsing
   under v0.3.2 would yield identical deferrals — zero progress
   for zero cost. **Not eligible** under existing parser baseline.
b. **SCZ SWEEP** — followed b0535 next-tick recommendation:
   continue ZMSC 2021 most-recent-first DESC sweep with nums
   {35..28} (8 candidates). **Executed this tick.**
c. **ZMCC NEW YEARS** — not reached; SCZ year sweeps still active.

## Fetch / parse results

8 GET targets dispatched against `zambialii.org/akn/zm/judgment/zmsc/2021/{n}/eng`:
- 7 OK on both HTML and PDF (14 GET fetches);
- 1 confirmed 404 on dateless probe (num=33; counts as 1 fetch).
- Total fetches this tick: **15**.

| court / num   | result      | notes |
|---------------|-------------|-------|
| zmsc/2021/35  | **written** | dismissed (Hakainde Hichilema v The Attorney General); panel Mambilima CJ / Mutuna JS / Wood JS / Malila JS / Musonda DCJ; pdf-tail-2pages-v031 "we hereby dismiss" anchor; constitutional law (Art 28 enforcement of Bill of Rights, Art 128 ConCourt jurisdiction, abuse of process / forum shopping). |
| zmsc/2021/34  | deferred    | pdf_extraction_empty_likely_scanned (14.3 MB image-only PDF) |
| zmsc/2021/33  | 404         | internal-gap (302→404 on dateless probe) |
| zmsc/2021/32  | deferred    | pdf_extraction_empty_likely_scanned (15.9 MB image-only PDF) |
| zmsc/2021/31  | deferred    | pdf_extraction_empty_likely_scanned (15.9 MB image-only PDF) |
| zmsc/2021/30  | deferred    | pdf_extraction_empty_likely_scanned (10.0 MB image-only PDF) |
| zmsc/2021/29  | deferred    | pdf_extraction_empty_likely_scanned (10.9 MB image-only PDF) |
| zmsc/2021/28  | deferred    | pdf_extraction_empty_likely_scanned (11.8 MB image-only PDF) |

| metric            | count |
|-------------------|------:|
| GET fetches       |    15 |
| total fetches     |    15 |
| records written   |     1 |
| records deferred  |     6 |
| confirmed 404     |     1 |

## Integrity checks

32 / 32 PASS for the single written record (`judgment-zm-2021-zmsc-35-hakainde-hichilema-v-the-attorney-general`):

- All required fields present (id/type/court/citation/case_name/case_number/date_decided/judges/issue_tags/outcome/outcome_detail/reasoning_tags/key_statutes/raw_sha256/source_url).
- type == "judgment", court == "Supreme Court of Zambia".
- 5 judges, all resolving in canonical registry (Mambilima, Mutuna, Wood, Malila, Musonda).
- issue_tags non-empty (3 tags — Constitutional law / Article 28 enforcement of Bill of Rights / scope-of-High-Court-powers cluster).
- outcome `dismissed` in allowed enum; outcome_detail non-empty.
- raw_sha256 matches on-disk PDF byte-for-byte (sha256: 2aa4c84b…).
- source_url is canonical zambialii.org/akn/zm/judgment/zmsc/...
- Zero duplicate IDs across corpus (155 unique judgment IDs).

## judges_registry.yaml

No new canonical entries this tick; 5 alias resolutions to existing
canonical entries (Mambilima CJ → Mambilima, Mutuna JS → Mutuna,
Wood JS → Wood, Malila JS → Malila, Musonda DCJ → Musonda).

## corpus.sqlite

Inserted 1 record into `records` (1844 → 1845) and 1 row into
`judgments_meta` (154 → 155) using TMPDIR-routed atomic copy
pattern (b0519+ precedent). records_fts deferred to host-side
rebuild via scripts/batch_0504_build_fts5.py.

## Cohort cumulative since b0504

- written: 57 (prior 56 + 1)
- v0.3.3-pending deferred: 50 (unchanged; no interpretive-ratio defers this tick)
- OCR-pending deferred: 10 (prior 4 + 6 this tick)
- confirmed-404: 25 (prior 24 + 1 internal-gap at zmsc/2021/33)

## Year-sweep status

- **ZMSC 2022 — COMPLETE** (since b0535): 61 / 61 nums attempted.
- **ZMSC 2021 — DESC sweep in progress**: max num=39 confirmed.
  12 of ~30+ valid attempted (1 written, 1 v0.3.3-pending deferred,
  9 OCR-pending deferred, 1 internal 404 at num=33; plus 11
  confirmed 404 above max-num=39 boundary).

## Daily fetch budget

- Today fetches: 62 / 500 (47 prior + 15 this tick). 438 remain.

## Next-tick recommendation

Continue ZMSC 2021 most-recent-first DESC sweep with nums {27..20}
(8 candidates). Given the very heavy OCR-pending ratio in this
cohort (6 of 7 successful fetches this tick were image-only), an
OCR backfill workflow should be considered as a parallel track once
the year-sweep has surveyed the breadth of ZMSC 2021.

When v0.3.3 parser ships, prioritise REPARSE DEFERRED of the
50-record raw-on-disk v0.3.3-pending cohort before moving deeper
into year sweeps.

## B2 sync

Deferred to host (rclone not in sandbox). Established pattern
since b0506.

## approvals.yaml

NOT modified. Phase-5 ingestion is complete; this is the dedicated
post-Phase-5 task per Peter's 2026-05-03 directive.
