# Batch 0077 Report

**Date:** 2026-04-15T08:35:12Z  
**Phase:** 4 (Bulk Ingestion)  
**Source:** ZambiaLII (zambialii.org)  
**Records added:** 8  
**Total sections:** 1,755  
**Fetches:** 9  

## Records

| ID | Title | Sections | Source |
|----|-------|----------|--------|
| act-zm-2018-006-anti-terrorism-and-non-proliferation-act-2018 | Anti-Terrorism and Non-Proliferation Act, 2018 | 770 | HTML |
| act-zm-1914-001-authentication-of-documents-act-1914 | Authentication of Documents Act, 1914 | 13 | HTML |
| act-zm-1954-010-aviation-act-1954 | Aviation Act, 1954 | 166 | HTML |
| act-zm-2022-005-bank-of-zambia-act-2022 | Bank of Zambia Act, 2022 | 645 | HTML |
| act-zm-1993-040-benefits-of-former-presidents-act-1993 | Benefits of Former Presidents Act, 1993 | 32 | HTML |
| act-zm-1957-027-betting-control-act-1957 | Betting Control Act, 1957 | 89 | HTML |
| act-zm-2025-027-betting-levy-act-2025 | Betting Levy Act, 2025 | 37 | HTML |
| act-zm-1961-015-bills-of-sale-registration-act-1961 | Bills of Sale (Registration) Act, 1961 | 3 | PDF |

## Integrity Checks

- No duplicate IDs: PASS (577 total records)
- amended_by/repealed_by references: PASS
- cited_authorities references: PASS
- source_hash verification: PASS (all 8 records)
- Required fields: PASS

## Notes

- Bills of Sale (Registration) Act, 1961 had only 1 section in HTML; fell back to PDF source (3 pages).
- Anti-Terrorism Act 2018 is the largest in this batch with 770 sections (consolidated version @2024-12-26).
- Bank of Zambia Act 2022 has 645 sections — major financial legislation.
- corpus.sqlite rebuilt: 577 records, 30,051 sections (73.8 MB).
- B2 sync deferred: rclone not available in sandbox.

## Corpus Totals

- **Total records:** 577 (576 acts + 1 judgment)
- **Total sections:** 30,051
- **ZambiaLII acts remaining (approx):** ~410 substantive + ~84 appropriation acts
