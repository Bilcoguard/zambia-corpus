# Batch 0074 — Phase 4 Bulk Ingestion

**Date:** 2026-04-15
**Worker:** KateWestonLegal-CorpusBuilder/1.0
**Source:** ZambiaLII (zambialii.org)

## Records Added (8)

| # | ID | Title | Citation | Sections | Source |
|---|---|---|---|---|---|
| 1 | act-zm-2008-013-accountants-act-2008 | Accountants Act, 2008 | Act No. 13 of 2008 | 119 | PDF |
| 2 | act-zm-1956-027-administration-of-estates-trust-corporations-act-1956 | Administration of Estates (Trust Corporations) Act, 1956 | Cap. 56 | 9 | HTML/AKN |
| 3 | act-zm-2012-003-anti-corruption-act-2012 | Anti-Corruption Act, 2012 | Act No. 3 of 2012 | 96 | HTML/AKN |
| 4 | act-zm-1933-003-arbitration-act-1933 | Arbitration Act, 1933 | Cap. 40 | 31 | HTML/AKN |
| 5 | act-zm-2000-019-arbitration-act-2000 | Arbitration Act, 2000 | Act No. 19 of 2000 | 0 | PDF (scanned) |
| 6 | act-zm-2017-007-banking-and-financial-services-act-2017 | Banking and Financial Services Act, 2017 | Act No. 7 of 2017 | 260 | PDF |
| 7 | act-zm-1967-027-bankruptcy-act-1967 | Bankruptcy Act, 1967 | Cap. 82 | 163 | HTML/AKN |
| 8 | act-zm-2025-008-border-management-and-trade-facilitation-act-2025 | Border Management and Trade Facilitation Act, 2025 | Act No. 8 of 2025 | 53 | HTML/AKN |

## Summary

- **Total sections:** 731 (across 8 records; 1 record has 0 sections due to scanned PDF)
- **Fetches:** 11 (8 HTML pages + 3 PDF downloads)
- **Integrity checks:** ALL PASS (no duplicate IDs, all hashes verified, all required fields present)
- **corpus.sqlite rebuilt:** 552 records, 27,441 sections

## Gaps

- **Arbitration Act, 2000** (act-zm-2000-019-arbitration-act-2000): ZambiaLII PDF is 35 pages of scanned images — no extractable text. Needs OCR or alternative source (parliament.gov.zm). Logged to gaps.md.

## Notable Acts

- **Anti-Corruption Act, 2012**: Key anti-corruption legislation (96 sections) — covers ACC powers, offences, asset forfeiture.
- **Banking and Financial Services Act, 2017**: Major financial regulation (260 sections) — banking licences, prudential standards, consumer protection.
- **Bankruptcy Act, 1967**: Insolvency framework (163 sections).
- **Accountants Act, 2008**: Professional regulation of accountants (119 sections).
- **Border Management and Trade Facilitation Act, 2025**: Very recent legislation on border/trade.

## Next Tick

Continue ZambiaLII bulk ingestion — priority candidates include: Bank of Zambia Act 2022, Building Societies Act 1968, Business Regulatory Act 2014, Cannabis Act 2021, Competition and Consumer Protection Act 2010, Cyber Security Act 2021.
