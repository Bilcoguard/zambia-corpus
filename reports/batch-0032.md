# Batch 0032 — Phase 4 (Bulk Ingestion)

**Date:** 2026-04-11T08:12:56Z
**Phase:** 4 (Bulk Ingestion)
**Source:** parliament.gov.zm
**Records:** 5
**Fetches:** 10 (5 node pages + 5 PDFs)

## Records

- **Act No. 1 of 2017** — Refugees, 2017 (111 sections)
- **Act No. 2 of 2017** — Agricultural Institute of Zambia, 2017 (89 sections)
- **Act No. 20 of 2017** — Employment (Amendment), 2017 (2 sections)
- **Act No. 21 of 2017** — Supplementary Appropriation, 2017 (3 sections)
- **Act No. 22 of 2017** — Appropriation, 2017 (2 sections)

## Integrity

- Duplicate check: PASS (238 record files, 238 unique IDs)
- Hash check: PASS (5/5)
- Reference check: PASS

## Notes

- SSL workaround: parliament.gov.zm missing intermediate cert, using verify=False
- This batch fills the 2017 Acts gap: previously had No. 3-19, now complete No. 1-22
- Notable: Refugees Act (111 sections), Agricultural Institute of Zambia Act (89 sections)
- Low section count: Employment (Amendment) (2 sections), Supplementary Appropriation (3 sections), Appropriation (2 sections) — expected for amendment/appropriation acts
- Corpus.sqlite rebuilt from all record files: 238 rows
- Remaining known gap: 2021 Act No. 22 (Public Private Partnership Amendment) — PDF not available on parliament.gov.zm
