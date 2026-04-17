# Batch 0125 Report

**Date:** 2026-04-17
**Phase:** 4 (Bulk Ingestion)
**Source:** ZambiaLII (zambialii.org)
**Parser version:** 0.3.0 / 0.3.0-pdf

## Records Added (8)

| # | ID | Title | Type | Sections | Source |
|---|---|---|---|---|---|
| 1 | act-zm-1985-014-medical-services-act--1985 | Medical Services Act, 1985 | act | 13 | PDF |
| 2 | act-zm-2013-006-millennium-challenge-compact-act--2013 | Millennium Challenge Compact Act, 2013 | act | 73 | PDF |
| 3 | act-zm-1982-025-minimum-wages-and-conditions-of-employment--1982 | Minimum Wages and Conditions of Employment, 1982 | act | 10 | HTML |
| 4 | act-zm-1968-025-misrepresentation-act--1968 | Misrepresentation Act, 1968 | act | 6 | HTML |
| 5 | act-zm-1992-031-ministerial-and-parliamentary-offices--emoluments--act--1992 | Ministerial and Parliamentary Offices (Emoluments) Act, 1992 | act | 8 | HTML |
| 6 | act-zm-1975-021-medical-aid-societies-and-nursing-homes--dissolution-and-prohibition--act--1975 | Medical Aid Societies and Nursing Homes (Dissolution and Prohibition) Act, 1975 | act | 10 | HTML |
| 7 | act-zm-1973-020-medical-examination-of-young-persons--underground-work--act--1973 | Medical Examination of Young Persons (Underground Work) Act, 1973 | act | 9 | HTML |
| 8 | act-zm-1969-013-merchant-shipping--temporary-provisions--act--1969 | Merchant Shipping (Temporary Provisions) Act, 1969 | act | 37 | HTML |

**Total sections:** 166

## Fetches
- HTML pages: 8
- PDF downloads: 2 (Medical Services Act 1985, Millennium Challenge Compact Act 2013 — no HTML body, fell back to PDF)
- Total fetches this batch: 10
- Today's cumulative fetches: ~141/2000

## Integrity Checks
- Duplicate IDs in batch: NONE
- Missing required fields: NONE
- Source hash validation: PASS
- Pre-existing Appropriation Act duplicates: 38 (noted for manual cleanup, pre-date this batch)

## Notes
- Medical Services Act 1985 and Millennium Challenge Compact Act 2013 had no AKN HTML body on ZambiaLII — content extracted from source PDFs via pdfplumber.
- Millennium Challenge Compact Act 2013 is unusually large (73 sections, ~240K chars) as it incorporates the full MCC compact text.
- ~190 new candidates identified on ZambiaLII pages 8-10 for future batches.

## Next Batch Targets
- Mineral Royalty (Repeal) Act 1997, Mineral Tax Act 1989, Mines Acquisition Acts 1970, Ministers (Prescribed Number) Act 2016, Lotteries Act 1957, Maintenance Orders Act 1960, Mashona Railway Company Act 1922, and remaining SIs from page 8.
