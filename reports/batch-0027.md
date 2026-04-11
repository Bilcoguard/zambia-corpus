# Batch Report 0027

**Date:** 2026-04-11
**Phase:** 4 (Bulk Acts Ingest)
**Batch:** 0027
**Records:** +6 acts (2022 No. 17-22)

## Acts Processed

| Citation | Title | Sections |
|----------|-------|----------|
| Act No. 17 of 2022 | The Zambia Development Agency Act, 2022 | 40 |
| Act No. 18 of 2022 | The Investment, Trade and Business Development Act, 2022 | 77 |
| Act No. 19 of 2022 | Zambia Institute of Secretaries Act, 2022 | 98 |
| Act No. 20 of 2022 | National Pension Scheme (Amendment) Act, 2022 | 4 |
| Act No. 21 of 2022 | The Securities (Amendment) Act, 2022 | 19 |
| Act No. 22 of 2022 | The Criminal Procedure Code (Amendment) Act, 2022 | 8 |

## Budget

- Fetches this batch: 17 (5 index pages + 6 node pages + 6 PDFs)
- Rate limit: 2s between requests (parliament.gov.zm)
- SSL: verify=False (parliament.gov.zm missing intermediate RapidSSL cert)

## Integrity Checks

- No duplicate IDs: PASS (212 total records in SQLite)
- Source hash verification: PASS (all 6 PDFs verified)
- ID format validation: PASS

## Notable

- Zambia Development Agency Act (40 sections) — investment promotion framework
- Investment, Trade and Business Development Act (77 sections) — comprehensive trade regulation
- Zambia Institute of Secretaries Act (98 sections) — professional body regulation
- National Pension Scheme Amendment (4 sections) — brief amendment, low count expected
- Securities Amendment (19 sections) — capital markets regulation
- Criminal Procedure Code Amendment (8 sections) — amendment act, low count expected
- This batch completes all 2022 Acts (No. 1-30)
