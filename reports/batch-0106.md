# Batch 0106 — Phase 4 Bulk Ingestion

**Date:** 2026-04-16T17:50Z
**Phase:** 4 (bulk)
**Records added:** 8
**Total sections:** 1303
**Fetches:** 8
**Source:** ZambiaLII (PDF)

## Strategy

This batch prioritised corporate/substantive SIs from ZambiaLII page 3, aligned with the `priority_order` in approvals.yaml (`sis_corporate` category). Skipped Chiefs Recognition orders (100+ low-value SIs) to focus on high-impact regulatory instruments.

## Records

| # | ID | Title | Year | SI No. | Sections | Source |
|---|---|---|---|---|---|---|
| 1 | si-zm-2019-014-companies-general-regulations-2019 | Companies (General) Regulations, 2019 | 2019 | 14 | 21 | PDF |
| 2 | si-zm-2019-015-companies-fees-regulations-2019 | Companies (Fees) Regulations, 2019 | 2019 | 15 | 55 | PDF |
| 3 | si-zm-2019-021-companies-prescribed-forms-regulations-2019 | Companies (Prescribed Forms) Regulations, 2019 | 2019 | 21 | 1066 | PDF |
| 4 | si-zm-2012-037-competition-and-consumer-protection-tribunal-rules-2012 | Competition and Consumer Protection (Tribunal) Rules, 2012 | 2012 | 37 | 47 | PDF |
| 5 | si-zm-2019-040-corporate-insolvency-practitioner-accreditation-regulations-2019 | Corporate Insolvency (Insolvency Practitioner Accreditation) Regulations, 2019 | 2019 | 40 | 27 | PDF |
| 6 | si-zm-2019-022-citizens-economic-empowerment-reservation-scheme-regulations-2019 | Citizens Economic Empowerment (Reservation Scheme) Regulations, 2019 | 2019 | 22 | 3 | PDF |
| 7 | si-zm-2017-050-citizenship-of-zambia-regulations-2017 | Citizenship of Zambia Regulations, 2017 | 2017 | 50 | 46 | PDF |
| 8 | si-zm-2016-071-civil-aviation-authority-fees-regulations-2016 | Civil Aviation Authority (Fees) Regulations, 2016 | 2016 | 71 | 38 | PDF |

## Integrity Checks
- ✓ All required fields present (id, type, jurisdiction, title, source_url, source_hash, fetched_at, parser_version, sections)
- ✓ No duplicate IDs (batch or corpus-wide)
- ✓ Source hashes verified against raw PDF files (8/8)
- ✓ All amended_by/repealed_by references resolve (none declared)

## Notes
- Companies (Prescribed Forms) Regulations yielded 1066 sections — this is a large forms schedule with many numbered form entries
- Citizens Economic Empowerment (Reservation Scheme) Regulations yielded only 3 sections — short instrument
- All 8 items are statutory instruments supporting corporate/commercial legislation
- ~100+ Chiefs Recognition orders on page 3 were deprioritised in favour of substantive SIs
- SQLite rebuild deferred — root filesystem capacity constraints
- B2 sync deferred — rclone not available in sandbox
- Next tick: continue with remaining substantive SIs from pages 3-4 (Constitutional Court Rules, Citizenship Amendment Regs, Civil Aviation SIs, Control of Goods SIs, Co-operative Societies Regulations)
