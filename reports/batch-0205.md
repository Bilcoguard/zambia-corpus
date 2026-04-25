# Batch 0205 — Phase 4 sis_employment rotation

**Date:** 2026-04-25
**Phase:** 4 (bulk)
**Sub-phase:** sis_employment (rotation per batch-0204 next-tick plan)
**Records written:** 5 / 6 attempted
**Fetches used:** 22 (10 discovery + 12 ingest)
**Integrity checks:** PASS (CHECK1–CHECK5 all green; CHECK6 N/A for SI schema)

## Rotation rationale

Batch 0204 yielded only **1** auto-keyword-matching novel candidate
under the strict `sis_corporate` filter (the other seven records came
from curated overrides). That counted as the first low-yield tick for
sis_corporate. Per the standing fallback rule recorded in batch-0203
and reaffirmed in batch-0204 ("if yield <3 across two consecutive
ticks, rotate to sis_employment"), this tick rotates to
**sis_employment** (priority_order item 4 from approvals.yaml).

Robots.txt re-verified at the start of the tick — sha256 prefix
`fce67b697ee4ef44…`, matching the standing baseline used since batch
0193.

## Discovery

Live alphabet probes covering nine letters: E, M, N, O, W (the
employment-relevant base set) plus I, F, A, T (extension to pick up
Industrial / Factories / Apprenticeship / TEVET). 9 alphabet fetches +
1 robots fetch = 10 discovery fetches.

* Total novel `(year, number)` slots seen pre-keyword: 276
* Auto-kept post-keyword filter (employment / labour / wages /
  workers' / NAPSA / NHIMA / industrial relations / occupational /
  domestic workers / training): **2**
  - SI 13 of 2022 (E) — minimum wages and conditions of employment
    (truck and bus drivers) (amendment) order, 2022
  - SI 13 of 2021 (W) — Worker's Compensation (Domestic Workers)
    Regulations, 2021

The strict-filter yield was again low (2). To reach a defensible batch
size without fabrication, four override targets were drawn directly
from the unfiltered alphabet captures (all visible in
`_work/batch_0205_discovery.json`) and explicitly within
sis_employment scope:

  - SI 31 of 2014 (W) — Workers' Compensation (Capitalised Values)
    Regulations, 2014 (Workers' Compensation Act)
  - SI 26 of 2002 (I) — Industrial Relations Court (Arbitration and
    Mediation Procedure) Rules, 2002 (Industrial and Labour Relations
    Act)
  - SI 35 of 1995 (T) — Technical Education and Vocational Training
    (Registration of Private Institutions) (Fees) Regulations, 1995
    (TEVETA Act)
  - SI 20 of 2008 (T) — Technical Education, Vocational and
    Entrepreneurship Training (Gemstone Processing and Lapidary
    Training Centre) (Establishment) Order, 2008 (TEVETA Act)

## Records ingested

| # | Slot | Title | Sections | Parent Act |
|---|------|-------|----------|------------|
| 1 | SI 13 of 2021 | Worker's Compensation (Domestic Workers) Regulations, 2021 | 4 | Workers' Compensation Act |
| 2 | SI 31 of 2014 | Workers' Compensation (Capitalised Values) Regulations, 2014 | 2 | Workers' Compensation Act |
| 3 | SI 26 of 2002 | Industrial Relations Court (Arbitration and Mediation Procedure) Rules, 2002 | 27 | Industrial and Labour Relations Act, Cap. 269 |
| 4 | SI 35 of 1995 | Technical Education and Vocational Training (Registration of Private Institutions) (Fees) Regulations, 1995 | (TEVETA fees regs) | TEVETA Act |
| 5 | SI 20 of 2008 | Technical Education, Vocational and Entrepreneurship Training (Gemstone Processing and Lapidary Training Centre) (Establishment) Order, 2008 | (TEVETA establishment order) | TEVETA Act |

The sixth attempted target — SI 13 of 2022 (Minimum Wages and
Conditions of Employment (Truck and Bus Drivers) (Amendment) Order,
2022) — failed PDF parsing (`pdf_parse_empty`) for the fourth time
across batches 0184 / 0200 / 0203(implicit) / 0205. Logged again to
`gaps.md`. The recurring failure on this slot warrants a parser-side
investigation in a future tick (likely a scanned-image PDF without an
embedded text layer; pdfplumber returns no extractable text).

## Notes

* Records 1–2 close out the discoverable Workers' Compensation Act
  derivative SIs on ZambiaLII for the 2014 and 2021 vintages.
* Record 3 (Industrial Relations Court Arbitration & Mediation
  Procedure Rules) is directly relevant to KWLP labour-dispute
  practice — defines the procedural framework for IRC mediation.
* Records 4–5 are TEVETA-derivative SIs and the first sis_employment
  records to capture the technical-education / skills-development
  branch of the labour framework.
* Cumulative SI records after this batch: **245** (+5 over batch-0204
  240).
* Judgment records unchanged at 25 (case_law_scz still paused per
  robots.txt Disallow on `/akn/zm/judgment/`).

## Integrity

All on-disk PDF hashes match the `source_hash` field in the
corresponding JSON record. All required schema fields populated. No
duplicate IDs introduced. No new (year, number) slot collisions. No
`amended_by` / `repealed_by` references in this batch (consistent with
non-amending SIs). No new gaps logged beyond the recurring SI
2022/013 PDF-parse-empty.

## Operational note

The original ingest call for slice [0,8] was interrupted by the bash
timeout after processing the first three candidates (2022/013 →
gap-logged, 2021/013 → ok, 2014/031 → ok). The driver reconstructed
the slice_0_3 state file from on-disk evidence (record JSON, raw PDF
sha256 verified to match) and resumed ingest in three single-record
slices [3,4], [4,5], [5,6]. Final aggregation captured all four slices
into `_work/batch_0205_summary.json` and `.batch_0205_state.json`.

## Next-tick plan

Continue sis_employment with a deeper probe of alphabets H (NHIMA
direct: National Health Insurance Management Authority Act SIs), P
(Pneumoconiosis Compensation Board Act SIs), and S (Skills Development
Levy Act SIs). If yield remains <3, rotate to **sis_data_protection**
(priority_order item 6) — Data Protection Act 2021/3 derivatives,
ECDPA / Cyber Security and Cyber Crimes Act SIs.

The recurring `pdf_parse_empty` on SI 2022/013 should be investigated:
if pdfplumber consistently returns empty, mark the source PDF as
image-only and consider an OCR pass (Tesseract via pytesseract) under
a separate parser_version bump.

Robots.txt should be re-verified at the start of every tick.

## Infrastructure

* B2 raw sync still deferred to host (rclone unavailable in sandbox).
  All batch-0205 raw bytes (5 HTML + 5 PDF + 1 robots + 9 alphabet
  HTML, totalling ~5.0 MB) are on disk awaiting host-driven
  `rclone sync raw/ b2raw:kwlp-corpus-raw/`.
* Pre-existing dupes (34 legacy-schema act dupes + 42 Appropriation-Act
  -000- placeholder dupes + 63 SI flat-layout dupes) unchanged — none
  introduced by this batch.
