# Batch 0117 — Phase 4 Bulk Ingestion

**Date:** 2026-04-17T06:36:34Z  
**Worker:** KateWestonLegal-CorpusBuilder/1.0  
**Source:** ZambiaLII (HTML + PDF)  
**Parser version:** 0.5.0  

## New Records (6 committed)

| # | ID | Title | Citation | Sections | Bytes |
|---|-----|-------|----------|----------|-------|
| 1 | act-zm-2000-019-arbitration-act-2000 | Arbitration Act, 2000 | Act No. 19 of 2000 | 0* | 2,641,019 |
| 2 | act-zm-1967-027-bankruptcy-act-1967 | Bankruptcy Act, 1967 | Act No. 27 of 1967 | 91 | 729,754 |
| 3 | act-zm-2007-010-biosafety-act-2007 | Biosafety Act, 2007 | Act No. 10 of 2007 | 52 | 638,071 |
| 4 | act-zm-1955-010-census-and-statistics-act-1955 | Census and Statistics Act, 1955 | Act No. 10 of 1955 | 9 | 75,013 |
| 5 | act-zm-2008-013-accountants-act-2008 | Accountants Act, 2008 | Act No. 13 of 2008 | 119 | 4,416,870 |
| 6 | act-zm-1913-012-brands-act-1913 | Brands Act, 1913 | Act No. 12 of 1913 | 4 | 66,497 |

*\*Arbitration Act 2000: source PDF is scanned image, 0 sections extracted. Logged in gaps.md for OCR.*

## Skipped (pre-existing duplicates, NOT committed)

| ID | Reason |
|----|--------|
| act-zm-1959-005-cheques-act-1959 | Already exists at records/acts/1959/ (16 sections vs 3 new) |
| act-zm-1965-067-chiefs-act-1965 | Already exists at records/acts/1965/ (37 sections vs 9 new) |

## Statistics

- **Fetches this batch:** 10 (8 HTML + 2 PDF re-fetch for 0-section items)
- **Total fetches today:** ~20/2000
- **Total sections added:** 275
- **Total raw bytes:** ~8.6 MB
- **Integrity checks:** PASS (batch records only; 27 pre-existing Appropriation Act year-subdir duplicates noted)

## Categories

- **Commercial/Financial:** Arbitration Act 2000, Bankruptcy Act 1967, Accountants Act 2008, Cheques Act 1959
- **Regulatory/Environmental:** Biosafety Act 2007
- **Governance/Constitutional:** Chiefs Act 1965, Census and Statistics Act 1955
- **Agricultural/Property:** Brands Act 1913

## Notes

- ZambiaLII AKN URLs require exact date suffixes from the listing page; generic dates 404.
- Arbitration Act 2000 PDF is scanned (image-only, 35 pages). Needs OCR. Raw saved.
- Accountants Act 2008 required PDF fallback (HTML page had no inline text). 119 sections parsed from PDF.
- Pre-existing year-subdirectory duplicates (Cheques, Chiefs) have better section coverage; our new flat files NOT committed.
- ~90 new substantive items identified on ZambiaLII pages 2-10 for future batches.

## Next Batch Candidates

From ZambiaLII pages 2-10:
- Citizens Economic Empowerment (Amendment) Act, 2010
- Casino (Amendment) Acts (1984, 1987, 1993, 1994, 2000)
- Banking and Financial Services SIs
- Animal Health / Biosafety SIs
- Anti-Terrorism SIs
