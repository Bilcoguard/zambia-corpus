# Batch 0107 Report

**Date:** 2026-04-16
**Phase:** 4 (Bulk Ingestion)
**Source:** ZambiaLII (zambialii.org) — PDF source files
**Fetches:** 8
**Total sections parsed:** 476

## Records Added

| # | ID | Title | Sections | Source |
|---|---|---|---|---|
| 1 | si-zm-2016-037 | Constitutional Court Rules, 2016 | 179 | PDF |
| 2 | si-zm-2016-054 | Constitutional Court (Fees) Rules, 2016 | 47 | PDF |
| 3 | si-zm-2022-027 | Citizenship of Zambia (Amendment) Regulations, 2022 | 8 | PDF |
| 4 | si-zm-2020-073 | Civil Aviation Authority (Search and Rescue) Regulations, 2020 | 121 | PDF |
| 5 | si-zm-2011-036 | Citizens Economic Empowerment (Preferential Procurement) Regulations, 2011 | 6 | PDF |
| 6 | si-zm-2021-035 | Citizens Economic Empowerment (Transportation of Heavy and Bulk Commodities by Road) (Reservation) Regulations, 2021 | 3 | PDF |
| 7 | si-zm-1999-026 | Co-operative Societies Regulations, 1999 | 24 | PDF |
| 8 | si-zm-1998-041 | House of Chiefs Regulations, 1998 | 88 | PDF |

## Integrity Checks

- **Batch records:** ALL PASS (hashes match, no duplicates, all required fields present)
- **Pre-existing duplicates noted:** 32 duplicate Appropriation Act IDs from earlier batches (not from this batch). These should be deduped in a future maintenance tick.

## Priority Coverage

This batch expanded SI coverage across multiple priority categories:
- **Constitutional/judicial:** Constitutional Court Rules + Fees Rules (226 sections)
- **Corporate:** Citizens Economic Empowerment SIs (9 sections)
- **Regulatory:** Civil Aviation Authority SAR Regulations (121 sections)
- **General:** Co-operative Societies Regs (24 sections), House of Chiefs Regs (88 sections), Citizenship Amendment Regs (8 sections)

## Notes

- ZambiaLII serves these SIs as PDF-only (no AKN HTML content). Parser used pdfplumber for extraction.
- HTML landing pages were initially fetched but contained no AKN markup; source.pdf URLs used instead.
- Stale HTML files from first attempt remain on disk (permission denied for deletion) but are not tracked in git.
- SQLite rebuild deferred due to root filesystem capacity constraints.
- B2 sync deferred to host.

## Next Batch

Continue with ZambiaLII page 3/4 substantive SIs: Compulsory Standards Orders, Control of Goods SIs, Constitutional Offices Emoluments Regulations, Civil Aviation (Designated Provincial) Regulations 2025.
