# Batch 0061 Report

**Date:** 2026-04-13T06:45:00Z
**Phase:** 4 (Bulk ingestion — acts_in_force)
**Source:** parliament.gov.zm (pages 27-34: 2002, 2001, 2000 Acts + 2016 Constitution Amendment)
**Records added:** 8
**Fetches this batch:** 34 (discovery + 8 node + 8 PDF)
**Total fetches today:** ~42/2000
**Integrity checks:** ALL PASS
**corpus.sqlite rebuilt:** 453 records

## Records Added

| # | ID | Title | Year | No. | Sections | OCR? |
|---|---|---|---|---|---|---|
| 1 | act-zm-2016-002-constitution-amendment-act-2016 | Constitution of Zambia (Amendment) Act | 2016 | 2 | 127 | No |
| 2 | act-zm-2002-002-value-added-tax-amendment-act-no-2-of-2002 | Value Added Tax (Amendment) Act | 2002 | 2 | 3 | No |
| 3 | act-zm-2001-009-the-customs-and-excise-amendment-act-no-9-of-2001 | Customs and Excise (Amendment) Act | 2001 | 9 | 0 | Yes |
| 4 | act-zm-2001-008-the-income-tax-amendment-act-no-8-of-2001 | Income Tax (Amendment) Act | 2001 | 8 | 0 | Yes |
| 5 | act-zm-2000-021-estate-agents-act-no-21-of-2000 | Estate Agents Act | 2000 | 21 | 79 | No |
| 6 | act-zm-2000-020-the-penal-code-amendment-act-no-20-of-2000 | Penal Code (Amendment) Act | 2000 | 20 | 0 | Yes |
| 7 | act-zm-2000-007-excess-expenditure-appropriation-1994-act-no-7-of-2000 | Excess Expenditure Appropriation (1994) Act | 2000 | 7 | 0 | Yes |
| 8 | act-zm-2000-006-the-value-added-tax-amendment-act-no-6-of-2000 | Value Added Tax (Amendment) Act | 2000 | 6 | 0 | Yes |

## Notable Acts

- **Constitution of Zambia (Amendment) Act, 2016** (No. 2): 127 sections — major constitutional amendment
- **Estate Agents Act, 2000** (No. 21): 79 sections — regulation of estate agents

## Gaps

- 5 acts are scanned PDFs needing OCR re-parse (2001 No. 8-9, 2000 No. 6-7, 20)
- Discovery pages 27-34 contained many non-act navigation links (About Parliament, etc.) — filtered out

## Progress

- Corpus now spans 2000-2026 (previously 2005-2026)
- First pre-2005 acts ingested: 3 from 2000, 2 from 2001, 1 from 2002
- Total records in corpus.sqlite: 453 (452 acts + 1 judgment)
- Next tick: continue discovery of 2000-2004 Acts from remaining pages, then try 1990s Acts
