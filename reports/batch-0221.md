# Batch 0221 Report — Phase 4 Bulk SI Cross-Sub_Phase Fill

- **Started:** 2026-04-25T09:07:01Z
- **Completed:** 2026-04-25T09:09:18Z
- **Records written:** 7 / 8 attempted
- **Fetches used:** 17 (1 robots-reverify + 16 ingest = 8 HTML + 8 PDF)
- **Parser version:** 0.5.0
- **Sub-phase mix:** sis_employment (1 ok / 2 attempted), sis_education (3 ok / 3), sis_courts (3 ok / 3)
- **Robots:** sha256 prefix fce67b697ee4ef44 verified (unchanged from batches 0193-0220)

## Records ingested

### sis_employment

- **SI 040 of 1993** — Privatisation (Trade Sales and Management or Employee Buyouts) (Sale Tender) Regulations, 1993
  - id: `si-zm-1993-040-privatisation-trade-sales-and-management-or-employee-buyouts-sale-tender-regulat`
  - sections: 39
  - source: https://zambialii.org/akn/zm/act/si/1993/40/eng@1993-03-11/source.pdf
  - sha256: 4a846ef7984154c4989e727a763aa67ea59975af171a1fcd33d9162816fa56bd

### sis_education

- **SI 085 of 2015** — Education (Teacher Training College Boards) (Establishment) Order, 2015
  - id: `si-zm-2015-085-education-teacher-training-college-boards-establishment-order-2015`
  - sections: 2
  - source: https://zambialii.org/akn/zm/act/si/2015/85/eng@2015-11-13/source.pdf
  - sha256: c941298def9ce801fe121449290f51ee2c361722696a156bd9c423d21750b100
- **SI 004 of 2021** — Electoral Process (Voter Education) Regulations, 2021
  - id: `si-zm-2021-004-electoral-process-voter-education-regulations-2021`
  - sections: 36
  - source: https://zambialii.org/akn/zm/act/si/2021/4/eng@2021-01-08/source.pdf
  - sha256: e6cceb97d78c1860793f379db7d1888950b66c67ef85645c827dd2f05ec1d465
- **SI 080 of 2020** — Electoral (Registration of Voters) Regulations, 2020
  - id: `si-zm-2020-080-electoral-registration-of-voters-regulations-2020`
  - sections: 109
  - source: https://zambialii.org/akn/zm/act/si/2020/80/eng@2020-09-25/source.pdf
  - sha256: f5f48bb4d2bb04ef0efa627c197485c111443ffbde57718491cedefadeff8ee1

### sis_courts

- **SI 060 of 2016** — Local Government Elections Tribunals Rules, 2016
  - id: `si-zm-2016-060-local-government-elections-tribunals-rules-2016`
  - sections: 77
  - source: https://zambialii.org/akn/zm/act/si/2016/60/eng@2016-08-05/source.pdf
  - sha256: 44b38077464ad7af87c6370cc6bc99fa6f6428a76f250700eb4e70d8b11e8d65
- **SI 025 of 2008** — National Constitutional Conference (Procedure) Rules, 2008
  - id: `si-zm-2008-025-national-constitutional-conference-procedure-rules-2008`
  - sections: 77
  - source: https://zambialii.org/akn/zm/act/si/2008/25/eng@2008-02-22/source.pdf
  - sha256: ff2332f013869df7c4fb2aadda3fbf81deb971e1139f6936f024cee68e341749
- **SI 026 of 2008** — National Constitutional Conference (Disciplinary Committee Proceedings) Rules, 2008
  - id: `si-zm-2008-026-national-constitutional-conference-disciplinary-committee-proceedings-rules-2008`
  - sections: 32
  - source: https://zambialii.org/akn/zm/act/si/2008/26/eng@2008-02-22/source.pdf
  - sha256: 9523a348009d7276e536d06f2cf35ce12a8cd5048520babea6985663e2a6b36a

## Failures (logged to gaps.md)

- **SI 013 of 2022** [sis_employment] — status: `pdf_parse_empty` — discovery_text: minimum wages and conditions of employment (truck and bus drivers) (amendment) order, 2022

## Integrity check summary

- CHECK1a (batch-scoped id uniqueness): **PASS** (7/7 unique)
- CHECK1b (corpus-wide id collision): **PASS** (0 within-batch collisions; 364 total SI ids)
- CHECK2 (amended_by ref resolution): **PASS** (0 refs in this batch)
- CHECK3 (repealed_by ref resolution): **PASS** (0 refs in this batch)
- CHECK4 (source_hash sha256 vs raw): **PASS** (7/7 verified)
- CHECK5 (required fields): **PASS** (10 fields × 7 records)

## Notes

- This tick used the cached `_work/batch_0219_discovery.json` `novel_pre_keyword_sample` for candidate selection, spending **0 alphabet-probe fetches** — only 1 robots-reverify fetch on top of the 16 ingest fetches.
- Cross-sub_phase rotation: the cached pool of sis_education (5) + sis_employment (2) + sis_courts (3) was tapped to fill batch capacity; previously-ingested 2 sis_education records (2013/012, 2021/045 — batch 0220) and 0 sis_courts records made room for first-time-in-corpus sis_courts ingestion this tick.
- **First sis_courts records in corpus history**: 2008/025 NCC procedure rules, 2008/026 NCC disciplinary committee rules, 2016/060 Local Government Elections Tribunals Rules. Sub_phase footprint established (cross-rotation; sis_courts not in priority_order but added as adjacent procedural-law category for cross-sub_phase efficiency).
- **One PDF parse failure**: SI 13 of 2022 (Minimum Wages and Conditions of Employment — Truck and Bus Drivers — Amendment) → `pdf_parse_empty`. Same failure pattern as SI 04/2022 (batch 0208) and SI 12/2022 (batch 0213) — pdfplumber fails to extract text from this 2022 amendment-order PDF format. Logged to gaps.md.
- Cumulative SI records after this batch: **364** (357 → 364 = +7).
- Cumulative judgment records: **25** (paused per zambialii.org/robots.txt Disallow on /akn/zm/judgment/).
- Today's fetches: ~373 / 2000 (18.65% of daily budget). Tokens within budget.
- B2 raw sync deferred to host (rclone unavailable in sandbox; pending host run for batches 0192-0221).
- Next-tick plan: cached cross-sub_phase pool from batch-0219 is now drained (sis_health 6/6 + sis_education 3/3 of 5 cached + sis_employment 2/2 + sis_courts 3/3). Next tick will need fresh alphabet probes — recommended: W (Wills, Workers' Compensation), J (Juveniles, Justices), I (Industrial, Insurance) for sis_family/sis_courts/sis_employment derivatives; also probe S (Skills Development, Securities), T (Teaching Profession), N (NAPSA, NHIMA, National Pension Scheme).
