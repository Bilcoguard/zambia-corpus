# Batch 0114 Report

**Date:** 2026-04-16T20:06:46Z
**Phase:** 4 (Bulk Ingestion)
**Records:** 8
**Total sections:** 81
**Fetches:** 16 (today total: ~276/2000)

## Records

| # | ID | Title | Sections | Source |
|---|-----|-------|----------|--------|
| 1 | `si-zm-2021-102-customs-and-excise-electronic-machinery-and-equipment-suspension-regulations-2021` | Customs and Excise (Electronic Machinery and Equipment) (Suspension) Regulations, 2021 | 3 | PDF |
| 2 | `si-zm-2020-041-customs-and-excise-ethyl-alcohol-refunds-rebates-and-remissions-regulations-2020` | Customs and Excise (Ethyl Alcohol) (Refunds, Rebates and Remissions) Regulations, 2020 | 8 | PDF |
| 3 | `si-zm-2019-066-customs-and-excise-excise-duty-suspension-ethyl-alcohol-regulations-2019` | Customs and Excise (Excise Duty) (Suspension) (Ethyl Alcohol) Regulations, 2019 | 3 | PDF |
| 4 | `si-zm-2019-005-customs-and-excise-nickel-and-particle-board-export-duty-remission-regulations-2019` | Customs and Excise (Nickel and Particle Board) (Export Duty) (Remission) Regulations, 2019 | 3 | PDF |
| 5 | `si-zm-2021-108-income-tax-turnover-tax-amendment-regulations-2021` | Income Tax (Turnover Tax) (Amendment) Regulations, 2021 | 2 | PDF |
| 6 | `si-zm-2021-107-income-tax-transfer-pricing-amendment-regulations-2021` | Income Tax (Transfer Pricing) (Amendment) Regulations, 2021 | 4 | PDF |
| 7 | `si-zm-2020-048-employment-code-exemption-regulations-2020` | Employment Code (Exemption) Regulations, 2020 | 3 | PDF |
| 8 | `si-zm-2020-105-service-commissions-local-government-service-commission-regulations-2020` | Service Commissions (Local Government Service Commission) Regulations, 2020 | 55 | PDF |

## Notes
- All 8 records are statutory instruments from ZambiaLII pages 5-6
- Focus on customs/excise (4), income tax (2), employment (1), service commissions (1)
- All PDFs parsed successfully with pdfplumber
- Source hashes verified at fetch time
- SQLite rebuild deferred (root filesystem at 100% capacity)
- B2 sync deferred to host (rclone not available in sandbox)
- Next batch: continue with ZambiaLII page 5-6 remaining items (Value Added Tax SIs, Road Traffic Regs, Worker's Compensation Regs, Disaster Management Regs)
