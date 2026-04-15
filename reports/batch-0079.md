# Batch 0079 Report

**Date:** 2026-04-15T09:52:00Z
**Phase:** 4 (Bulk Ingestion)
**Source:** ZambiaLII (zambialii.org)
**Records added:** 8
**Total sections:** 176
**Fetches:** 10 (8 HTML + 2 PDF fallbacks)

## Records

| ID | Title | Sections | Citation |
|----|-------|----------|---------|
| act-zm-1992-013-casino-act-1992 | Casino Act, 1992 | 56 | Act No. 13 of 1992 |
| act-zm-1963-064-central-african-power-corporation-financial-provis | Central African Power Corporation (Financial Provisions) Act, 1963 | 12 | Chapter 432 |
| act-zm-1981-003-central-committee-members-ministerial-and-parliame | Central Committee Members', Ministerial and Parliamentary Offices (Emoluments) Act, 1981 | 1 | Act No. 3 of 1981 |
| act-zm-1959-005-cheques-act-1959 | Cheques Act, 1959 | 16 | Chapter 398 |
| act-zm-1965-067-chiefs-act-1965 | Chiefs Act, 1965 | 37 | Chapter 287 |
| act-zm-1940-012-civil-courts-attachment-of-debts-act-1940 | Civil Courts (Attachment of Debts) Act, 1940 | 12 | Chapter 32 |
| act-zm-1926-020-clubs-registration-act-1926 | Clubs' Registration Act, 1926 | 37 | Chapter 119 |
| act-zm-2004-013-computer-misuse-and-crimes-act-2004 | Computer Misuse and Crimes Act, 2004 | 5 | Act No. 13 of 2004 |

## Integrity Checks

- No duplicate IDs: PASS (592 total records)
- amended_by/repealed_by references: PASS (all empty — no cross-refs in this batch)
- cited_authorities references: PASS
- source_hash verification: PASS (all 8 records matched raw files)
- Required fields: PASS

## Parser Notes

- Parser version 0.4.2 (AKN dual-pattern extractor)
- Casino Act 1992: 56 sections — gambling regulation legislation
- Chiefs Act 1965: 37 sections — customary authority governance
- Clubs' Registration Act 1926: 37 sections — colonial-era club registration
- Cheques Act 1959: 16 sections — commercial paper/negotiable instruments
- Central African Power Corporation Act 1963: 12 sections — historical federation-era financial provisions
- Civil Courts (Attachment of Debts) Act 1940: 12 sections — debt enforcement procedure
- Central Committee Members' Emoluments Act 1981: 1 section (PDF, possible scanned document) — logged to gaps.md for OCR review
- Computer Misuse and Crimes Act 2004: 5 sections from PDF (possible partial extraction) — logged to gaps.md for review

## Parser Warnings

- **Central Committee Members' Emoluments Act 1981**: HTML page returned 0 sections; PDF (881KB) yielded only 1 section — likely scanned or non-standard formatting. Needs OCR.
- **Computer Misuse and Crimes Act 2004**: HTML returned 0 sections; PDF (1.48MB) yielded only 5 numbered sections — PDF may be scanned or have complex layout.

## Corpus Totals

- **Total records:** 593 (592 acts + 1 judgment)
- **Total fetches today:** 98
- **ZambiaLII acts remaining (approx):** ~169 substantive principal acts
- **B2 sync:** deferred to host (rclone not available in sandbox)
