# Batch Report 0021

**Date:** 2026-04-11
**Phase:** 4 (Bulk Acts Ingest)
**Batch:** 0021
**Records:** +7 acts (2023 No. 9-11, 13-16; No. 12 skipped — connection error)

## Acts Processed

| Citation | Title | Sections | Source Hash |
|----------|-------|----------|-------------|
| Act No. 9 of 2023 | The Zambia Institute of Valuation Surveyors Act, 2023 | 97 | `sha256:c5f82d9ae105ff06633d2ba...` (verified) |
| Act No. 10 of 2023 | The Supplementary Appropriation Act, 2023 | 2 | `sha256:92390be73b7b510bbccb36c...` (verified) |
| Act No. 11 of 2023 | The Trade Marks Act, 2023 | 247 | `sha256:4abe2d71eabfc1bc349cd84...` (verified) |
| Act No. 13 of 2023 | The Marriage (Amendment) Act, 2023 | 6 | `sha256:83eb7dea1030db63b043d6f...` (verified) |
| Act No. 14 of 2023 | The Judicial Training Institute of Zambia Act, 2023 | 33 | `sha256:c0be76106d01080b9a217f6...` (verified) |
| Act No. 15 of 2023 | The Zambia Institute of Marketing (Amendment) Act, 2023 | 2 | `sha256:9f5550bcc8339e915884082...` (verified) |
| Act No. 16 of 2023 | The Mobile Money Transaction Levy Act, 2023 | 16 | `sha256:c47a0550046390d0b8cbe95...` (verified) |

## Skipped

- **Act No. 12 of 2023** (The Defence (Amendment) Act, 2023): Connection error fetching node page /node/11534. Logged to gaps.md for retry in next batch.

## Parse Quality Notes

- **Act No. 9 of 2023** (97 sections): The Zambia Institute of Valuation Surveyors Act, 2023 — substantial legislation
- **Act No. 10 of 2023** (2 sections): The Supplementary Appropriation Act, 2023 — brief act
- **Act No. 11 of 2023** (247 sections): The Trade Marks Act, 2023 — substantial legislation
- **Act No. 13 of 2023** (6 sections): The Marriage (Amendment) Act, 2023 — moderate amendment/focused act
- **Act No. 14 of 2023** (33 sections): The Judicial Training Institute of Zambia Act, 2023 — substantial legislation
- **Act No. 15 of 2023** (2 sections): The Zambia Institute of Marketing (Amendment) Act, 2023 — brief act
- **Act No. 16 of 2023** (16 sections): The Mobile Money Transaction Levy Act, 2023 — moderate amendment/focused act

## Budget

- Fetches this batch: 14 (7 node pages + 7 PDFs)
- Rate limit: 2s between requests (parliament.gov.zm)
- Total fetches today (2026-04-11): ~50/2000

## Integrity Checks

- No duplicate IDs: ✓ (182 total records in SQLite)
- Source hash verification: ✓ (all 7 PDFs verified)
- Provenance fields complete: ✓
- amended_by/repealed_by references: ✓ (all resolve or empty)
- No fabricated citations: ✓

## Notable Acts

- **The Trade Marks Act, 2023**: 247 sections — substantial new legislation
- **The Zambia Institute of Valuation Surveyors Act, 2023**: 97 sections
- **The Judicial Training Institute of Zambia Act, 2023**: 33 sections
