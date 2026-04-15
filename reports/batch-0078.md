# Batch 0078 Report

**Date:** 2026-04-15T09:10:06Z  
**Phase:** 4 (Bulk Ingestion)  
**Source:** ZambiaLII (zambialii.org)  
**Records added:** 8  
**Total sections:** 186  
**Fetches:** 8  

## Records

| ID | Title | Sections | Citation |
|----|-------|----------|---------|
| act-zm-2007-010-biosafety-act | Biosafety Act, 2007 | 61 | Act No. 10 of 2007 |
| act-zm-1973-021-births-and-deaths-registration-act | Births and Deaths Registration Act, 1973 | 22 | Chapter 51 |
| act-zm-1931-003-boy-scouts-and-girl-guides-associations-act | Boy Scouts and Girl Guides Associations Act, 1931 | 6 | Chapter 141 |
| act-zm-1965-051-bretton-woods-agreement-act | Bretton Woods Agreement Act, 1965 | 40 | Chapter 367 |
| act-zm-1923-009-british-acts-extension-act | British Acts Extension Act, 1923 | 5 | Act No. 9 of 1923 |
| act-zm-1968-018-calculation-of-taxes-act | Calculation of Taxes (Consequential Provisions) Act, 1968 | 3 | Chapter 339 |
| act-zm-1968-059-carriage-by-air-act | Carriage by Air Act, 1968 | 25 | Chapter 447 |
| act-zm-1964-007-central-african-civil-air-transport-act | Central African Civil Air Transport Act, 1964 | 24 | Chapter 451 |

## Integrity Checks

- No duplicate IDs: PASS (585 total records)
- amended_by/repealed_by references: PASS (all empty — no cross-refs in this batch)
- cited_authorities references: PASS
- source_hash verification: PASS (all 8 records matched raw files)
- Required fields: PASS

## Parser Notes

- Parser version 0.4.2 introduced improved AKN section extraction that handles both:
  (a) akn-num/akn-heading child elements (e.g., Biosafety Act 2007)
  (b) Embedded section numbers in text (e.g., "1. Short title...")
- Biosafety Act 2007: 61 sections — major environmental/biotech legislation
- Bretton Woods Agreement Act: 40 sections — international financial conventions
- Carriage by Air Act: 25 sections — aviation/transport law
- Births and Deaths Registration: 22 sections — civil registration
- Central African Civil Air Transport: 24 sections — historical federation-era legislation
- Calculation of Taxes: 3 sections — short consequential provisions act
- Boy Scouts/Girl Guides: 6 sections — civil society organisations

## Corpus Totals

- **Total records:** 585 (584 acts + 1 judgment)
- **Total sections:** 30,237
- **ZambiaLII acts remaining (approx):** ~177 substantive acts
- **Appropriation Acts remaining:** ~1 (from ZambiaLII catalogue)
- **corpus.sqlite size:** ~21 MB (rebuilt from scratch this tick)
