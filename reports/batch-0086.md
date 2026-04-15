# Batch 0086 Report

**Date:** 2026-04-15T14:05:29Z
**Phase:** 4 (Bulk Ingestion)
**Category:** acts_in_force (Appropriation Acts 1986-1994)
**Parser Version:** 0.4.2

## Records Added: 8

| # | ID | Title | Sections | Source |
|---|---|---|---|---|
| 1 | act-zm-1986-012-appropriation-act-1986 | Appropriation Act, 1986 | 2 | PDF |
| 2 | act-zm-1987-015-appropriation-act-1987 | Appropriation Act, 1987 | 34 | PDF |
| 3 | act-zm-1988-019-appropriation-act-1988 | Appropriation Act, 1988 | 1 | PDF |
| 4 | act-zm-1989-034-appropriation-act-1989 | Appropriation Act, 1989 | 2 | PDF |
| 5 | act-zm-1990-044-appropriation-act-1990 | Appropriation Act, 1990 | 3 | PDF |
| 6 | act-zm-1992-017-appropriation-act-1992 | Appropriation Act, 1992 | 2 | PDF |
| 7 | act-zm-1993-022-appropriation-act-1993 | Appropriation Act, 1993 | 1 | PDF |
| 8 | act-zm-1994-005-appropriation-act-1994 | Appropriation Act, 1994 | 2 | PDF |

**Total sections:** 47
**Fetches this batch:** 16 (8 HTML stub pages + 8 PDFs)
**Budget usage today:** ~200/2000 fetches

## Notes
- All 8 acts had HTML stub pages on ZambiaLII (no AKN markup) — content extracted from PDF source files.
- Appropriation Acts are typically short (authorize expenditure from Consolidated Fund). Section counts are low as expected.
- Appropriation Act 1987 had 34 sections (unusually detailed schedule content).
- Several acts yielded only 1-2 sections due to scanned/image PDF quality — pdfplumber extracted available text.
- 5 remaining Appropriation Acts (1995-1999) still on ZambiaLII listing for next batch.

## Integrity Checks
- No duplicate IDs (637 unique across corpus)
- All source_hash values match raw PDF files on disk
- No unresolved amended_by or repealed_by references
- **ALL CHECKS PASS**

## B2 Sync
- rclone not available in sandbox — deferred to host
