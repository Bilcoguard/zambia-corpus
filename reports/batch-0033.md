# Batch 0033 Report — Phase 4 (Bulk Ingestion)

**Date:** 2026-04-11T08:45:00Z  
**Phase:** 4 — bulk ingestion (acts_in_force)  
**Source:** parliament.gov.zm  
**Batch size:** 8 records  

## Records Ingested

| # | ID | Title | Sections | PDF Size |
|---|-----|-------|----------|----------|
| 1 | act-zm-2016-001-the-constitution-of-zambia | The Constitution of Zambia, 2016 | 30 | 29,499 |
| 2 | act-zm-2016-003-the-movable-property-security-interest | The Movable Property (Security Interest), 2016 | 155 | 101,031 |
| 3 | act-zm-2016-004-financial-intelligence-centre-amendment | Financial Intelligence Centre (Amendment), 2016 | 15 | 58,232 |
| 4 | act-zm-2016-005-the-civil-aviation | The Civil Aviation, 2016 | 263 | 234,242 |
| 5 | act-zm-2016-006-layout-designs-of-integrated-circuits-act-2016 | Layout-designs of Integrated Circuits Act, 2016 | 134 | 94,261 |
| 6 | act-zm-2016-007-the-court-of-appeal | The Court of Appeal, 2016 | 49 | 39,888 |
| 7 | act-zm-2016-008-the-constitutional-court | The Constitutional Court, 2016 | 1 | 2,519,942 |
| 8 | act-zm-2016-009-the-superior-courts-number-of-judges | The Superior Courts (Number of Judges), 2016 | 1 | 303,993 |

## Notable

- **Civil Aviation Act** (263 sections) — comprehensive aviation regulation
- **Movable Property (Security Interest) Act** (155 sections) — major commercial law statute
- **Layout-designs of Integrated Circuits Act** (134 sections) — IP legislation
- **Constitutional Court Act** and **Superior Courts Act** parsed as single sections due to scanned PDF format — may need re-parse

## Parse Quality Flags

- **act-zm-2016-008-the-constitutional-court** (1 section, 2.5 MB): Large scanned PDF. Text extraction yielded single block. Flag for manual review / OCR re-parse.
- **act-zm-2016-009-the-superior-courts-number-of-judges** (1 section): Scanned PDF. Same issue as above.

## Integrity

- Duplicate IDs: 0
- Hash mismatches: 0
- Unresolved references: 0
- **ALL CHECKS PASSED**

## Fetches

- Node pages: 8
- PDF downloads: 8
- Total this batch: 16
- Total today: ~183 / 2,000

## Next Steps

- Continue 2016 Acts No. 10-49 (40 remaining)
- After 2016 complete, fill 2018 gaps (Acts No. 12-23, 12 remaining)
