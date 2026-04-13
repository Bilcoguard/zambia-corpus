# Batch 0065 Report

**Date:** 2026-04-13T07:12:12Z
**Phase:** 4 (Bulk ingestion — acts_in_force)
**Source:** parliament.gov.zm (2015, 2014, 2002 Acts from pages 17-26)
**Records added:** 5
**Fetches this batch:** 13 (node pages + PDFs)
**Total fetches today:** ~170/2000
**Integrity checks:** ALL PASS
**corpus.sqlite:** 480 records

## Records Added

| # | ID | Title | Year | No. | Sections | OCR? |
|---|---|---|---|---|---|---|
| 1 | act-zm-2014-001-the-legal-practitioner-amendment-act | The Legal Practitioner (Amendment) Act | 2014 | 1 | 0 | Yes |
| 2 | act-zm-2002-020-zambia-national-broadcasting | Zambia National Broadcasting | 2002 | 20 | 16 | No |
| 3 | act-zm-2002-017-independent-broadcasting-authority | Independent Broadcasting Authority | 2002 | 17 | 80 | No |
| 4 | act-zm-2002-016-high-court-amendment | High Court (Amendment) | 2002 | 16 | 2 | No |
| 5 | act-zm-2002-015-supreme-court-amendment | Supreme Court (Amendment) | 2002 | 15 | 2 | No |

## Notable Acts

- **Independent Broadcasting Authority Act, 2002 (No. 17)**: Establishment of IBA, broadcasting regulation framework (80 sections — largest in batch)
- **Zambia National Broadcasting Act, 2002 (No. 20)**: ZNBC governance and broadcasting regulation (16 sections)
- **Legal Practitioner (Amendment) Act, 2014 (No. 1)**: Scanned PDF, needs OCR for full text extraction
- **High Court (Amendment) Act, 2002 (No. 16)**: Short amendment act (2 sections)
- **Supreme Court (Amendment) Act, 2002 (No. 15)**: Short amendment act (2 sections)

## Gaps (3 acts with no PDF on parliament.gov.zm)

- Anti-Terrorism (Amendment) Act, 2015: no PDF link on node page (https://www.parliament.gov.zm/node/4542)
- The Zambia Revenue Authority (Amendment): no PDF link on node page (https://www.parliament.gov.zm/node/2907)
- The Companies (Amendment) Act (2011): no PDF link on node page (https://www.parliament.gov.zm/node/3368)

## Strategy Note

Discovery phase scanned pages 15-48 of the acts-of-parliament listing, identifying ~389 new acts not yet in the corpus. This batch processed the first 8 targets (5 successful, 3 with no PDF). Remaining new acts span 2015, 2014, 2011, 2002, 1998-1999, and many earlier years through to the full Laws of Zambia chapter acts.

## Progress

- Total records in corpus.sqlite: 480 (479 acts + 1 judgment)
- ~389 remaining new acts discovered across pages 15-48
- Next tick: continue 2002 Acts (No. 7-14), then 1999/1998 Acts
- 1 scanned PDF needs OCR (Legal Practitioner Amendment 2014)
