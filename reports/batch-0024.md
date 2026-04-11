# Batch Report 0024

**Date:** 2026-04-11
**Phase:** 4 (Bulk Acts Ingest)
**Batch:** 0024
**Records:** +8 acts (2022 No. 1-8)
**Note:** Re-fetch of lost batch 0023 (push failed, /tmp clone cleaned up)

## Acts Processed

| Citation | Title | Sections |
|----------|-------|----------|
| Act No. 1 of 2022 | The Emoluments Commission Act, 2022 | 62 |
| Act No. 2 of 2022 | The Zambia Institute of Marketing Act, 2022 | 103 |
| Act No. 3 of 2022 | The Zambia Institute of Human Resource Management Act, 2022 | 107 |
| Act No. 4 of 2022 | The Social Workers' Association of Zambia Act, 2022 | 83 |
| Act No. 5 of 2022 | The Bank of Zambia Act, 2022 | 130 |
| Act No. 6 of 2022 | The Judges (Conditions of Service) Act, 2022. | 5 |
| Act No. 7 of 2022 | The Supplementary Appropriation (2022) Act, 2022. | 2 |
| Act No. 8 of 2022 | Road Traffic (Amendment) Act, 2022. | 41 |

## Budget

- Fetches this batch: 22 (6 index + 8 node + 8 PDF)
- Rate limit: 2s between requests (parliament.gov.zm)
- SSL: verify=False (parliament.gov.zm missing intermediate RapidSSL cert)

## Integrity Checks

- No duplicate IDs: PASS (198 total records in SQLite)
- Source hash verification: PASS (all 8 PDFs verified)
- ID format validation: PASS

## Notable

- Bank of Zambia Act (130 sections) — major financial legislation
- ZIHRM Act (107 sections), ZIM Act (103 sections) — professional bodies
- Judges Act (5 sections), Supplementary Appropriation (2 sections) — brief acts flagged in gaps.md