# Batch 0083 Report

**Date:** 2026-04-15T12:39:38Z
**Phase:** 4 (Bulk Ingestion)
**Source:** ZambiaLII (zambialii.org)
**Records added:** 3
**Total sections:** 242
**Fetches:** ~10 (3 HTML + 2 PDF fallbacks + search/listing attempts)

## Context

Retry of Batch 0082 targets, which failed entirely due to ZambiaLII SSL errors. ZambiaLII partially reachable this tick — SSL issues intermittent.

## Records

| ID | Title | Sections | Citation | Notes |
|----|-------|----------|---------|-------|
| act-zm-1991-001-constitution-of-zambia-act-1991 | Constitution of Zambia Act, 1991 | 33 | Act No. 1 of 1991 | PDF/pdfplumber |
| act-zm-2016-002-constitution-of-zambia-amendment-act-2016 | Constitution of Zambia (Amendment) Act, 2016 | 127 | Act No. 2 of 2016 | PDF/pdfplumber |
| act-zm-1967-041-dangerous-drugs-act-1967 | Dangerous Drugs Act, 1967 | 82 | Act No. 41 of 1967 | HTML/AKN |

## Integrity Checks

- No duplicate IDs (batch and global): PASS
- Required fields present: PASS
- Source hashes match raw files: PASS (all 3 records)
- amended_by/repealed_by references: PASS (empty in this batch)
- Section structure valid: PASS

## Gaps / Notes

- 5 acts from batch 0082 returned HTTP 404 — act number guesses were incorrect and ZambiaLII search/listing was unreachable (SSL errors on page 2+). These acts may use different AKN numbers or may not be on ZambiaLII. Logged to gaps.md:
  - Consular Conventions Act, 1951
  - Control of Goods Act, 1954
  - Copperbelt University Act, 1987
  - Council of Law Reporting Act, 1967
  - Debtors Act, 1938
- ZambiaLII intermittent SSL errors continue — connections succeed ~60% of the time.

## Corpus Totals

- **Total records:** ~611 (610 acts + 1 judgment)
- **Total sections this batch:** 242
- **Fetches today:** ~142/2000
- **ZambiaLII acts remaining:** ~165 (substantive, excluding appropriation acts)

## Next Batch Candidates

Compulsory Standards Act 2017, Constituency Development Fund Act 2018, Consumer Credit Act 2023, Control of Dogs Act 1964, Copyright and Performance Rights Act 1994, Corporate Insolvency Act 2017, Correctional Service Act 2021, Cotton Act 2005.
