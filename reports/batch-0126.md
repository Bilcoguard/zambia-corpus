# Batch 0126 Report

**Date:** 2026-04-17T11:09:15Z
**Phase:** 4 (Bulk Ingestion)
**Records:** 8
**Total sections:** 1990
**Fetches:** 12 (8 HTML + 4 PDF)
**Source:** ZambiaLII (pages 8-9)

## Records

| # | Title | Type | Sections | Source |
|---|-------|------|----------|--------|
| 1 | Occupational Health and Safety Act, 2025 | act | 474 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/2025/16/eng@2025-12-30) |
| 2 | National Council for Construction Act, 2020 | act | 487 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/2020/10/eng@2020-11-26) |
| 3 | National Forensic Act, 2020 | act | 294 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/2020/2/eng@2020-10-26) |
| 4 | National Planning and Budgeting Act, 2020 | act | 326 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/2020/1/eng@2020-10-26) |
| 5 | National Dialogue (Constitution, Electoral Process, Public Order and Political Parties) Act, 2019 | act | 132 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/2019/1/eng@2019-04-10) |
| 6 | Nurses and Midwives Act, 2019 | act | 147 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/2019/10/eng@2019-12-06) |
| 7 | National Health Insurance Act, 2018 | act | 94 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/2018/2/eng@2018-04-11) |
| 8 | National Technical Regulation Act, 2017 | act | 36 | [ZambiaLII](https://www.zambialii.org/akn/zm/act/2017/5/eng@2017-04-13) |

## Notes

- 4 records (Occupational Health & Safety 2025, National Council for Construction 2020, National Forensic 2020, National Planning & Budgeting 2020) parsed from HTML with AKN section extraction.
- 4 records (National Dialogue 2019, Nurses & Midwives 2019, National Health Insurance 2018, National Technical Regulation 2017) were PDF-only pages — PDFs fetched and parsed with pdfplumber.
- 2 records (Nurses & Midwives 2019, National Council for Construction 2020) had pre-existing entries from earlier batches. Existing records updated with improved section extraction; year-subfolder copies tombstoned.
- 30 pre-existing duplicate IDs noted from prior batches (Appropriation Acts etc.) — flagged for manual cleanup.
- All integrity checks PASS.

## Integrity checks
- [x] No duplicate IDs in batch
- [x] All source_hash values match raw files on disk
- [x] All required provenance fields present
- [x] No broken cross-references
