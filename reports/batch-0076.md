# Batch 0076 Report

**Date:** 2026-04-15T08:04:58Z
**Phase:** 4 (Bulk Ingestion)
**Source:** ZambiaLII (zambialii.org)
**Records added:** 8
**Total sections:** 598
**Fetches used:** 11 (8 HTML + 3 PDF fallbacks)
**Integrity checks:** ALL PASS

## Records

| # | ID | Title | Sections | Source |
|---|---|---|---|---|
| 1 | act-zm-1996-021-actions-for-smoke-damage-prohibition-repeal-1996 | Actions for Smoke Damage (Prohibition) (Repeal), 1996 | 3 (PDF) | ZambiaLII |
| 2 | act-zm-1954-037-african-war-memorial-fund-act-1954 | African War Memorial Fund Act, 1954 | 40 | ZambiaLII |
| 3 | act-zm-1957-019-agricultural-products-levy-act-1957 | Agricultural Products Levy Act, 1957 | 68 | ZambiaLII |
| 4 | act-zm-1972-011-air-passenger-service-charge-act-1972 | Air Passenger Service Charge Act, 1972 | 33 | ZambiaLII |
| 5 | act-zm-1964-008-air-services-act-1964 | Air Services Act, 1964 | 114 | ZambiaLII |
| 6 | act-zm-1982-002-amalgamation-of-mining-companies-special-provisions-act-1982 | Amalgamation of Mining Companies (Special Provisions) Act, 1982 | 48 (PDF) | ZambiaLII |
| 7 | act-zm-2010-028-animal-identification-act-2010 | Animal Identification Act, 2010 | 8 (PDF) | ZambiaLII |
| 8 | act-zm-2024-002-animal-identification-and-traceability-act-2024 | Animal Identification and Traceability Act, 2024 | 284 | ZambiaLII |

## Notes
- 3 acts had no extractable AKN HTML sections; fell back to PDF source via pdfplumber.
- Animal Identification and Traceability Act 2024 is the largest with 284 sections — comprehensive modern legislation.
- corpus.sqlite rebuilt: 569 records (568 acts + 1 judgment), 28,296 sections total.
- DB size reduced to 31.4 MB after clean rebuild (previously ~50 MB with fragmentation).
- No gaps or errors in this batch.

## Corpus Status
- **Total records:** 569 (568 acts + 1 judgment)
- **Total sections:** 28,296
- **ZambiaLII acts remaining:** ~418
- **Next targets:** Anti-Terrorism and Non-Proliferation Act 2018, Appropriation Acts, Births and Deaths Registration Act, etc.
