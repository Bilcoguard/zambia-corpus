# Batch Report 0026

**Date:** 2026-04-11
**Phase:** 4 (Bulk Acts Ingest)
**Batch:** 0026
**Records:** +8 acts (2022 No. 9-16)
**Note:** Redo of batch 0025 (push failed in previous tick)

## Acts Processed

| Citation | Title | Sections |
|----------|-------|----------|
| Act No. 9 of 2022 | Public Roads (Amendment) Act, 2022 | 13 |
| Act No. 10 of 2022 | The Tobacco Act, 2022 | 96 |
| Act No. 11 of 2022 | Zambia Institute of Public Relations and Communication Act, 2022 | 89 |
| Act No. 12 of 2022 | The Children's Code Act, 2022 | 456 |
| Act No. 13 of 2022 | Penal Code (Amendment) Act | 3 |
| Act No. 14 of 2022 | Probation of Offenders (Amendment) Act, 2022 | 3 |
| Act No. 15 of 2022 | Public Debt Management Act, 2022 | 83 |
| Act No. 16 of 2022 | The Anti-Human Trafficking Act, 2022 | 14 |

## Budget

- Fetches this batch: 20 (4 index pages + 8 node pages + 8 PDFs)
- Rate limit: 2s between requests (parliament.gov.zm)
- SSL: verify=False (parliament.gov.zm missing intermediate RapidSSL cert)

## Integrity Checks

- No duplicate IDs: PASS (206 total records in SQLite)
- Source hash verification: PASS (all 8 PDFs verified)
- ID format validation: PASS

## Notable

- Children's Code Act, 2022 (456 sections) — major child protection legislation
- Tobacco Act, 2022 (96 sections) — comprehensive regulation
- Public Relations and Communication Act (89 sections) — professional body
- Public Debt Management Act (83 sections) — fiscal governance
- Amendment acts (No. 9, 13, 14) have low section counts as expected
