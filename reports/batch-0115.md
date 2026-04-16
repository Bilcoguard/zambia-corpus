# Batch 0115 Report

**Date:** 2026-04-16T20:39:49Z
**Phase:** 4 (Bulk Ingestion)
**Records added:** 8
**Total sections:** 660
**Fetches used:** 10 (today's total: ~286/2000)

## Records

| # | ID | Title | Sections | Source |
|---|-----|-------|----------|--------|
| 1 | `act-zm-2011-001-anti-gender-based-violence-act-2010` | Anti-Gender-Based Violence Act, 2010 | 30 | [ZambiaLII](https://zambialii.org/akn/zm/act/2011/1/eng@2011-04-15) |
| 2 | `act-zm-2015-022-gender-equity-and-equality-act` | Gender Equity and Equality Act, 2015 | 89 | [ZambiaLII](https://zambialii.org/akn/zm/act/2015/22/eng@2015-12-24/source.pdf) |
| 3 | `act-zm-2018-012-border-management-and-trade-facilitation-act` | Border Management and Trade Facilitation Act, 2018 | 95 | [ZambiaLII](https://zambialii.org/akn/zm/act/2018/12/eng@2018-12-26/source.pdf) |
| 4 | `act-zm-2021-002-cyber-security-and-cyber-crimes-act` | Cyber Security and Cyber Crimes Act, 2021 | 69 | [ZambiaLII](https://zambialii.org/akn/zm/act/2021/2/eng@2021-03-24) |
| 5 | `act-zm-2021-003-data-protection-act` | Data Protection Act, 2021 | 65 | [ZambiaLII](https://zambialii.org/akn/zm/act/2021/3/eng@2021-03-24) |
| 6 | `act-zm-2021-033-cannabis-act` | Cannabis Act, 2021 | 35 | [ZambiaLII](https://zambialii.org/akn/zm/act/2021/33/eng@2021-05-20) |
| 7 | `act-zm-2022-012-childrens-code-act` | Children’s Code Act, 2022 | 242 | [ZambiaLII](https://zambialii.org/akn/zm/act/2022/12/eng@2022-08-11) |
| 8 | `act-zm-2022-018-investment-trade-and-business-development-act` | Investment, Trade and Business Development Act, 2022 | 35 | [ZambiaLII](https://zambialii.org/akn/zm/act/2022/18/eng@2024-04-18) |

## Integrity Checks

- Duplicate IDs: **PASS**
- Required fields: **PASS**  
- Cross-references: **PASS**
- ID format: **PASS**
- Source hash: **PASS**

## Notes

- Batch focused on high-value substantive Acts from ZambiaLII's updated listing pages.
- 2 Acts (Border Management, Gender Equity) were PDF-only; extracted via pdfplumber.
- 6 Acts had structured HTML (Akoma Ntoso) content on ZambiaLII.
- All records are modern, high-impact legislation (2010-2022).
- ~962 unique unprocessed items remain on ZambiaLII (pages 0-10).
- Next batch: continue with Corporate Insolvency Act 2017, Geological and Minerals Development Act 2025, Minerals Regulation Commission Act 2024, Occupational Health and Safety Act 2025, etc.

## B2 Sync Status

rclone not available in sandbox. Peter to run:
```
rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
```
