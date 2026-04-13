# Batch 0062 Report

**Date:** 2026-04-13T05:35:00Z
**Phase:** 4 (Bulk ingestion — acts_in_force)
**Source:** parliament.gov.zm (pages 35-36: Laws of Zambia Chapter Acts)
**Records added:** 8
**Fetches this batch:** ~12 (4 node pages + 8 PDFs)
**Total fetches today:** ~96/2000
**Integrity checks:** ALL PASS
**corpus.sqlite rebuilt:** 461 records

## Records Added

| # | ID | Title | Cap. | Sections | OCR? |
|---|---|---|---|---|---|
| 1 | act-zm-cap-184-lands-act | Lands Act | Cap. 184 | 175 | No |
| 2 | act-zm-cap-185-lands-and-deeds-registry-act | Lands and Deeds Registry Act | Cap. 185 | 249 | No |
| 3 | act-zm-cap-188-land-survey-act | Land Survey Act | Cap. 188 | 262 | No |
| 4 | act-zm-cap-189-lands-acquisition-act | Lands Acquisition Act | Cap. 189 | 62 | No |
| 5 | act-zm-cap-153-hotels-act | Hotels Act | Cap. 153 | 265 | No |
| 6 | act-zm-cap-166-betting-control-act | Betting Control Act | Cap. 166 | 106 | No |
| 7 | act-zm-cap-167-liquor-licensing-act | Liquor Licensing Act | Cap. 167 | 178 | No |
| 8 | act-zm-cap-199-forests-act | Forests Act | Cap. 199 | 604 | No |

## Notable Acts

- **Lands Act (Cap. 184)**: Key land tenure legislation — leasehold continuation, presidential vesting of land, customary tenure (175 sections)
- **Lands and Deeds Registry Act (Cap. 185)**: Registry framework for land transactions (249 sections)
- **Forests Act (Cap. 199)**: National and Local Forest management, conservation, licensing of forest produce (604 sections — largest in batch)
- **Land Survey Act (Cap. 188)**: Survey regulation for Zambia (262 sections)

## Strategy Note

This batch transitions from year-numbered Acts ("Act No. X of YYYY") to **Laws of Zambia Chapter Acts** ("Cap. XXX"). Pages 35+ of parliament.gov.zm list consolidated Laws of Zambia organized by Chapter number rather than by enactment year. These are critical in-force legislation. The Chapter number is extracted from the first page of each PDF.

## Progress

- Total records in corpus.sqlite: 461 (460 acts + 1 judgment)
- Now includes Laws of Zambia Chapter Acts (Cap. series) alongside year-numbered Acts
- Next tick: continue Cap. series from pages 36+ (Tourism Act, Water Act, National Heritage, Rating Act, National Housing Authority Act, Agricultural Lands Act, ZNBC Act, etc.)
