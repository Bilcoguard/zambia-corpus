# Batch 0063 Report

**Date:** 2026-04-13T06:08:09Z
**Phase:** 4 (Bulk ingestion — acts_in_force)
**Source:** parliament.gov.zm (page 35: Laws of Zambia Chapter Acts)
**Records added:** 8
**Fetches this batch:** 16 (8 node pages + 8 PDFs)
**Total fetches today:** ~112/2000
**Integrity checks:** ALL PASS
**corpus.sqlite rebuilt:** 469 records

## Records Added

| # | ID | Title | Cap. | Sections | OCR? |
|---|---|---|---|---|---|
| 1 | act-zm-cap-155-tourism-act | Tourism Act | Cap. 155 | 83 | No |
| 2 | act-zm-cap-154-zambia-national-broadcasting-corporation-act | Zambia National Broadcasting Corporation Act | Cap. 154 | 196 | No |
| 3 | act-zm-cap-157-casino-act | Casino Act | Cap. 157 | 35 | No |
| 4 | act-zm-cap-158-theatres-and-cinematograph-exhibition-act | Theatres and Cinematograph Exhibition Act | Cap. 158 | 136 | No |
| 5 | act-zm-cap-168-traditional-beer-act | Traditional Beer Act | Cap. 168 | 74 | No |
| 6 | act-zm-cap-175-printed-publications-act | Printed Publications Act | Cap. 175 | 19 | No |
| 7 | act-zm-cap-162-clubs-registration-act | Clubs' Registration Act | Cap. 162 | 36 | No |
| 8 | act-zm-cap-92-lotteries-act | Lotteries Act | Cap. 92 | 53 | No |

## Notable Acts

- **Zambia National Broadcasting Corporation Act (Cap. 154)**: Establishes ZNBC, broadcasting regulation framework (196 sections — largest in batch)
- **Theatres and Cinematograph Exhibition Act (Cap. 158)**: Regulation of theatres, cinemas, and public performances (136 sections)
- **Tourism Act (Cap. 155)**: Tourism regulation, licensing of tourism enterprises, Zambia Tourism Board (83 sections)
- **Traditional Beer Act (Cap. 168)**: Regulation of traditional beer brewing and sale (74 sections)

## Strategy Note

Continuing through page 35 of parliament.gov.zm Laws of Zambia listing. All 8 PDFs were text-based (no OCR needed). This completes most of page 35. Remaining on page 35: Radiocommunications Act, National Arts Council Act, National Heritage Conservation Commission Act. Page 36+ has many more Cap. Acts to process.

## Progress

- Total records in corpus.sqlite: 469 (468 acts + 1 judgment)
- Laws of Zambia Chapter Acts now includes Cap. 92, 153-158, 162, 166-168, 175, 184-185, 188-189, 199
- Next tick: continue with remaining page 35 Acts (Radiocommunications, National Arts Council, National Heritage Conservation Commission) then page 36 (National Museums, National Archives, Water Act, Agricultural Lands, Rating Act, etc.)
