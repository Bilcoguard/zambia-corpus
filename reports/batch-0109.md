# Batch 0109 Report

**Date:** 2026-04-16
**Phase:** 4 (Bulk Ingestion)
**Source:** ZambiaLII (zambialii.org) — PDF source files
**Fetches:** 17 (1 discovery + 16 record fetches)
**Total sections parsed:** 344

## Records Added

| # | ID | Title | Sections | Source |
|---|---|---|---|---|
| 1 | si-zm-2021-058-data-protection-registration-and-licensing-regulations-2021 | Data Protection (Registration and Licensing) Regulations, 2021 | 62 | PDF |
| 2 | act-zm-2011-012-environmental-management-act-2011 | Environmental Management Act, 2011 | 236 | PDF |
| 3 | si-zm-2023-048-employment-code-minimum-wages-and-conditions-of-employment-general-order-2023 | Employment Code (Minimum Wages and Conditions of Employment) (General) Order, 2023 | 3 | PDF |
| 4 | si-zm-2023-049-employment-code-domestic-workers-minimum-wages-and-conditions-of-employment-order-2023 | Employment Code (Domestic Workers Minimum Wages and Conditions of Employment) Order, 2023 | 3 | PDF |
| 5 | si-zm-2023-050-employment-code-shop-workers-minimum-wages-and-conditions-of-employment-order-2023 | Employment Code (Shop Workers Minimum Wages and Conditions of Employment) Order, 2023 | 10 | PDF |
| 6 | si-zm-2021-052-cyber-security-and-cyber-crimes-national-cyber-security-advisory-and-coordination-council-regulations-2021 | Cyber Security and Cyber Crimes (National Cyber Security, Advisory and Coordination Council) Regulations, 2021 | 6 | PDF |
| 7 | si-zm-2016-065-court-of-appeals-rules-2016 | Court of Appeals Rules, 2016 | 1 | PDF |
| 8 | si-zm-2024-010-criminal-procedure-code-economic-and-financial-crimes-court-rules-2024 | Criminal Procedure Code (Economic and Financial Crimes Court) Rules, 2024 | 23 | PDF |

## Deduplication

Removed 32 pre-existing duplicate records from git tracking:
- 24 year-subdirectory copies (records/acts/{year}/*.json) that duplicate canonical flat records
- 8 -000- numbered variants (incorrect act numbers from early batches)

## Integrity Checks

- **New batch records:** ALL PASS (8/8 hash verified)
- **Pre-existing duplicates:** Removed from git tracking to resolve ID conflicts
- **Post-cleanup unique IDs:** ~762 (794 - 32 duplicates)

## Priority Categories Covered

- **sis_data_protection:** Data Protection (Registration and Licensing) Regulations, 2021
- **sis_employment:** 3 Employment Code minimum wage orders (2023)
- **sis_corporate/cyber:** Cyber Security and Cyber Crimes Regulations, 2021
- **procedural:** Court of Appeals Rules 2016, Economic and Financial Crimes Court Rules 2024
- **acts_in_force:** Environmental Management Act, 2011

## Notes

- ZambiaLII page 4 has ~145 legislation links; many substantive acts already in corpus
- Remaining high-value targets on page 4: Energy Regulation Regs, Environmental Management SIs, Electoral Process Regs, Electronic Government Regs, Electricity SIs (2026)
- Next batch should continue with ZambiaLII page 4 remaining items
