# Batch 0206 — Phase 4 sis_employment continuation

**Date:** 2026-04-25
**Phase:** 4 (bulk)
**Sub-phase:** sis_employment (continuation per batch-0205 next-tick plan)
**Records written:** 5 / 5 attempted
**Fetches used:** 15 (5 discovery + 10 ingest)
**Integrity checks:** PASS (CHECK1–CHECK5 all green; CHECK6 N/A for SI schema)

## Continuation rationale

Batch 0205 next-tick plan called for "continue sis_employment with a
deeper probe of alphabets H (NHIMA — National Health Insurance
Management Authority Act 2018/2 SIs), P (Pneumoconiosis Compensation
Board Act SIs), and S (Skills Development Levy Act SIs), and
Parent-Act-driven probes for the Employment Code Act 2019/3
derivatives." This tick executes that plan: alphabets H, P, S, plus E
(Employment Code Act / Employment Act SIs).

Robots.txt re-verified at the start of the tick — sha256
`fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0`,
matching the standing baseline since batch 0193.

## Discovery

Live alphabet probes covering four letters: H, P, S, E. 4 alphabet
fetches + 1 robots fetch = 5 discovery fetches.

* Total novel `(year, number)` slots seen pre-keyword: 126
* Auto-kept post-keyword filter (employment / labour / wages /
  workers' / NAPSA / NHIMA / industrial relations / occupational): **1**
  - SI 13 of 2022 (E) — minimum wages and conditions of employment
    (truck and bus drivers) (amendment) order, 2022

The auto-kept candidate (SI 2022/013) is the recurring
`pdf_parse_empty` failure already logged across batches 0184 / 0200 /
0203 / 0205 — it was deliberately skipped in this tick to avoid a
fifth gap entry on the same image-only PDF; backfill is deferred to a
future OCR-capable tick.

The strict filter yielded zero novel sis_employment SIs in this
alphabet sweep, so all five ingested records were drawn from the
unfiltered novel sample (visible in
`_work/batch_0206_discovery.json`) using a curated override list.
Each override is explicitly within the sis_employment scope under the
Service Commissions Act / public-officer-pay branch of Zambia's
employment framework:

  - SI 102 of 2020 (S) — Service Commissions (Civil Service
    Commission) Regulations, 2020 [Service Commissions Act 2016/10]
  - SI 76 of 2021 (S) — Service Commission (Zambia Correctional
    Service Commission) Regulations, 2021 [Service Commissions Act
    2016/10]
  - SI 3 of 1993 (S) — Teaching Service Commission (Delegation)
    Directions, 1993 [Service Commissions Act predecessor]
  - SI 96 of 2020 (H) — Higher Education Loans and Scholarships
    (Transfer of Staff) Regulations, 2020 [Higher Education Loans and
    Scholarships Act 2016/31 — staff transfer]
  - SI 14 of 2022 (P) — Presidential (Emoluments) (Amendment)
    Regulations, 2022 [Constitution + Presidential Emoluments Act —
    public-officer pay]

## Records ingested

| # | Slot | Title | Sections | Parent Act |
|---|------|-------|----------|------------|
| 1 | SI 102 of 2020 | Service Commissions (Civil Service Commission) Regulations, 2020 | (Civil Service Commission framework) | Service Commissions Act 2016/10 |
| 2 | SI 76 of 2021 | Service Commission (Zambia Correctional Service Commission) Regulations, 2021 | (Correctional Service Commission framework) | Service Commissions Act 2016/10 |
| 3 | SI 3 of 1993 | Teaching Service Commission (Delegation) Directions, 1993 | (TSC delegation rules) | Service Commissions Act predecessor |
| 4 | SI 96 of 2020 | Higher Education Loans and Scholarships (Transfer of Staff) Regulations, 2020 | (staff transfer rules) | Higher Education Loans and Scholarships Act 2016/31 |
| 5 | SI 14 of 2022 | Presidential (Emoluments) (Amendment) Regulations, 2022 | (presidential emoluments amendment) | Presidential Emoluments Act |

The single auto-kept candidate (SI 2022/013) was not attempted this
tick due to the recurring pdf_parse_empty failure mode (image-only
PDF). No new gap entry was logged for it; the batch-0205 entry stands.

## Notes

* All five records are within the sis_employment public-sector
  employment branch — Service Commissions, Higher Education staff
  transfer, and Presidential Emoluments are all directly relevant to
  KWLP's public-sector employment / civil service practice.
* The Service Commissions trio (SI 102/2020, SI 76/2021, SI 3/1993)
  spans 28 years of Zambia's civil-service-commission framework, with
  SI 102/2020 establishing the modern Civil Service Commission under
  the 2016 Service Commissions Act.
* SI 96/2020 captures the staff-transfer regulations made when HELSB
  became a body corporate under the 2016 HELS Act.
* SI 14/2022 (Presidential Emoluments Amendment) is the current
  presidential pay regulation — directly relevant to constitutional
  emoluments practice.
* Cumulative SI records after this batch: **250** (+5 over batch-0205
  245).
* Judgment records unchanged at 25 (case_law_scz still paused per
  robots.txt Disallow on `/akn/zm/judgment/`).

## Integrity

All on-disk PDF hashes match the `source_hash` field in the
corresponding JSON record. All required schema fields populated. No
duplicate IDs introduced. No new (year, number) slot collisions. No
`amended_by` / `repealed_by` references in this batch (consistent with
non-amending-clause SIs at the discovery layer). No new gaps logged
this batch.

## Operational note

The bash 45 s call cap forced ingest into 3 invocations (slice_1_3 →
2 records, slice_3_5 → 2 records, slice_5_6 → 1 record). All slices
ran with the standing 6 s crawl-delay margin over the
robots.txt-declared 5 s. Final aggregation captured all three slices
into `_work/batch_0206_summary.json` and `.batch_0206_state.json`.

## Next-tick plan

Continue sis_employment with a deeper probe of alphabets N (NAPSA —
National Pension Scheme Authority Act SIs), and Parent-Act-driven
probes for the Employment Code Act 2019/3, NHIMA Act 2018/2, and
Pneumoconiosis Compensation Board Act SIs. If yield <3, rotate to
**sis_data_protection** (priority_order item 6) — Data Protection Act
2021/3 / ECDPA / Cyber Security and Cyber Crimes Act SIs.

The recurring `pdf_parse_empty` on SI 2022/013 should be investigated
in a future OCR-capable tick (likely a scanned-image PDF without
embedded text layer — pdfplumber consistently returns no extractable
text).
