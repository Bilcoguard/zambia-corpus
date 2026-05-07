# Batch 0535 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker (scheduled task `judgment-ingestion`)
- **Wall-clock window**: 2026-05-07T06:44Z..06:55Z (UTC, ~11 min, well under 20 min target)
- **Phase**: Phase 5 dedicated post-completion ingestion (continued).
- **Parser**: v0.3.2 baseline frozen at scripts/batch_0498_parse.py + scripts/batch_0506_zmsc_parse.py wrapper.
- **Batch number note**: advanced from b0534 to b0535 because the main corpus worker's idle-tick post-push commit (c32bd49) had already attached the "b0534 idle" label. Mirrors the b0524/b0525 precedent.

## Tick decision (priority order)

a. **REPARSE DEFERRED** — gaps.md cohort of **46** raw-on-disk
   deferrals are flagged `raw-on-disk-pending-v0.3.3` (parser
   v0.3.2 already attempted; awaiting v0.3.3 patterns). Reparsing
   under v0.3.2 would yield identical deferrals — zero progress
   for zero cost. **Not eligible** under existing parser baseline.

b. **SCZ SWEEP** — followed b0531 next-tick recommendation:
   close out ZMSC 2022 with nums {4, 3, 2, 1} (4 candidates), and
   start ZMSC 2021 with a boundary probe + most-recent-first
   DESC sweep of the top 4 nums. **Executed this tick.**

c. **ZMCC NEW YEARS** — not reached; SCZ year sweeps still active.

## Boundary probe — ZMSC 2021

15 HEAD requests issued against `zambialii.org/akn/zm/judgment/zmsc/2021/{n}/eng`:

| n   | status |
|-----|--------|
| 10  | 404 |
| 30  | 200 |
| 35  | 200 |
| 38  | 200 |
| 39  | 200 |
| 40  | 404 |
| 41  | 404 |
| 42  | 404 |
| 45  | 404 |
| 50  | 404 |
| 60  | 404 |
| 70  | 404 |
| 80  | 404 |
| 90  | 404 |
| 100 | 404 |

**Max num = 39 confirmed.** Lower bound and any internal-gap
clusters not yet probed.

## Fetch / parse results

8 GET targets (4 ZMSC 2022 + 4 ZMSC 2021), all 200 OK on both HTML
and PDF (16 GET fetches total).

| court / num   | result   | outcome / notes |
|---------------|----------|-----------------|
| zmsc/2022/4   | deferred | html_no_summary_pdf_no_match — interpretive-ratio family |
| zmsc/2022/3   | **written** | allowed (Natural Valley Ltd v Fairly Bottling (Z) Ltd and Ors); panel Malila / Kaoma / Kajimanga JS; pdf-tail-2pages-v032 anchor |
| zmsc/2022/2   | deferred | html_no_summary_pdf_no_match — interpretive-ratio family |
| zmsc/2022/1   | deferred | html_no_summary_pdf_no_match — interpretive-ratio family |
| zmsc/2021/39  | deferred | html_no_summary_pdf_no_match — interpretive-ratio family |
| zmsc/2021/38  | deferred | pdf_extraction_empty_likely_scanned (8.3 MB scanned PDF) |
| zmsc/2021/37  | deferred | pdf_extraction_empty_likely_scanned (9.3 MB scanned PDF) |
| zmsc/2021/36  | deferred | pdf_extraction_empty_likely_scanned (13.6 MB scanned PDF) |

| metric            | count |
|-------------------|------:|
| HEAD probes       |    15 |
| GET fetches       |    16 |
| total fetches     |    31 |
| records written   |     1 |
| records deferred  |     7 |
| confirmed 404     |     0 |

## Integrity checks

30 / 30 PASS for the single written record (`judgment-zm-2022-zmsc-03-natural-valley-ltd-v-fairly-bottling-z-ltd-and-ors`):

- All required fields present.
- type == "judgment", court == "Supreme Court of Zambia".
- 3 judges, all resolving in canonical registry (Malila, Kaoma, Kajimanga).
- issue_tags non-empty (6 tags).
- outcome `allowed` in allowed enum; outcome_detail non-empty.
- raw_sha256 matches on-disk PDF byte-for-byte.
- source_url is canonical zambialii.org/akn/zm/judgment/zmsc/...
- Zero duplicate IDs across corpus (154 unique judgment IDs).

## judges_registry.yaml

No new canonical entries this tick; 3 alias resolutions to existing
canonical entries (Malila JS → Malila, Kaoma JS → Kaoma, Kajimanga
JS → Kajimanga).

## corpus.sqlite

Inserted 1 record into `records` (1843 → 1844) and 1 row into
`judgments_meta` (153 → 154) using TMPDIR-routed atomic copy
pattern (b0519+ precedent). records_fts deferred to host-side
rebuild via scripts/batch_0504_build_fts5.py.

## Cohort cumulative since b0504

- written: 56 (prior 55 + 1)
- v0.3.3-pending deferred: 50 (prior 46 + 4)
- OCR-pending deferred: 4 (prior 1 + 3)
- confirmed-404: 24 (unchanged)

## Year-sweep status

- **ZMSC 2022 — COMPLETE**: 61 / 61 nums attempted. 18 written, 28
  v0.3.3-pending deferred, 1 OCR-pending deferred, 14 internal-gap
  404s at contiguous span {13..26}.
- **ZMSC 2021 — top probe done**: max num=39 confirmed; 4 of ~30+
  valid attempted (0 written, 1 v0.3.3-pending deferred, 3
  OCR-pending deferred); 11 confirmed 404s above the max-num
  boundary.

## Daily fetch budget

- Today fetches: 47 / 500 (16 from b0531 + 31 this tick). 453 remain.

## Next-tick recommendation

Continue ZMSC 2021 most-recent-first DESC sweep with nums {35..28}
(8 candidates). Defer the three scanned-image PDFs (zmsc/2021/{38,
37, 36}) to a dedicated OCR backfill workflow.

When v0.3.3 parser ships, prioritise REPARSE DEFERRED of the
50-record raw-on-disk cohort before moving deeper into year sweeps.

## B2 sync

Deferred to host (rclone not in sandbox). Established pattern
since b0506.

## approvals.yaml

NOT modified. Phase-5 ingestion is complete; this is the dedicated
post-Phase-5 task per Peter's 2026-05-03 directive.
