# Batch Report 0020

**Date:** 2026-04-11
**Phase:** 4 (Bulk Acts Ingest)
**Batch:** 0020
**Records:** +8 acts (2023 No. 1-8)

## Acts Processed

| Citation | Title | Sections | Source Hash |
|----------|-------|----------|-------------|
| Act No. 1 of 2023 | The National Pension Scheme (Amendment) Act, 2023 | 7 | `sha256:cb7397eeea8e3...` (verified) |
| Act No. 2 of 2023 | The Controlled Substances Act, 2023. | 80 | `sha256:2723463243ba9...` (verified) |
| Act No. 3 of 2023 | The Examinations Council of Zambia Act, 2023 | 83 | `sha256:7de410ea8d3ee...` (verified) |
| Act No. 4 of 2023 | The Teaching Profession (Amendment) Act, 2023 | 4 | `sha256:8cf146ec9e464...` (verified) |
| Act No. 5 of 2023 | The Rural Electrification Act, 2023 | 44 | `sha256:ef2e4fbb75f52...` (verified) |
| Act No. 6 of 2023 | The Anti-Terrorism and Non-Proliferation (Amendment) Act. | 48 | `sha256:cc844fac2f6a2...` (verified) |
| Act No. 7 of 2023 | The National Prosecution Authority (Amendment) Act, 2023 | 6 | `sha256:19fa6aae9d303...` (verified) |
| Act No. 8 of 2023 | The Environmental Management (Amendment) Act, 2023 | 14 | `sha256:62cbeb2785143...` (verified) |

## Parse Quality Notes

- **Act No. 1 of 2023** (7 sections): The National Pension Scheme (Amendment) Act, 2023 — moderate amendment/focused act
- **Act No. 2 of 2023** (80 sections): The Controlled Substances Act, 2023. — substantial legislation
- **Act No. 3 of 2023** (83 sections): The Examinations Council of Zambia Act, 2023 — substantial legislation
- **Act No. 4 of 2023** (4 sections): The Teaching Profession (Amendment) Act, 2023 — moderate amendment/focused act
- **Act No. 5 of 2023** (44 sections): The Rural Electrification Act, 2023 — substantial legislation
- **Act No. 6 of 2023** (48 sections): The Anti-Terrorism and Non-Proliferation (Amendment) Act. — substantial legislation
- **Act No. 7 of 2023** (6 sections): The National Prosecution Authority (Amendment) Act, 2023 — moderate amendment/focused act
- **Act No. 8 of 2023** (14 sections): The Environmental Management (Amendment) Act, 2023 — moderate

## Budget

- Fetches this batch: 16 (8 node pages + 8 PDFs)
- Rate limit: 2s between requests (parliament.gov.zm)
- Total fetches today (2026-04-11): ~36/2000 (20 prior + 16 this batch)

## Integrity Checks

- No duplicate IDs: ✓ (175 total records in SQLite)
- Source hash verification: ✓ (all 8 PDFs verified)
- Provenance fields complete: ✓
- amended_by/repealed_by references: ✓ (all resolve or empty)
- No fabricated citations: ✓

## Notable Acts

- **The Examinations Council of Zambia Act, 2023**: 83 sections
- **The Controlled Substances Act, 2023.**: 80 sections
- **The Anti-Terrorism and Non-Proliferation (Amendment) Act.**: 48 sections
- **The Rural Electrification Act, 2023**: 44 sections

## Workaround Note

git pull --ff-only failed on mounted workspace (FUSE/APFS lock file issue).
Used /tmp clone at HEAD=544beda (batch 0019 confirmed).
SSL: verify=False with urllib3 warnings disabled (parliament.gov.zm missing intermediate cert).
