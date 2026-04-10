# Batch Report 0019

**Date:** 2026-04-11
**Phase:** 4 (Bulk Acts Ingest)
**Batch:** 0019
**Records:** +8 acts (2026 No. 10-11, 2023 No. 24-29)

## Acts Processed

| Citation | Title | Sections | Source Hash |
|----------|-------|----------|-------------|
| Act No. 10 of 2026 | The State-Owned Enterprise Act, 2026 | 78 | `sha256:...` (verified) |
| Act No. 11 of 2026 | The Zambia Deposit Insurance Corporation Act, 2026 | 87 | `sha256:...` (verified) |
| Act No. 24 of 2023 | The Access to Information Act, 2023 | 63 | `sha256:...` (verified) |
| Act No. 25 of 2023 | The Customs and Excise (Amendment) Act, 2023 | 8 | `sha256:...` (verified) |
| Act No. 26 of 2023 | The Zambia Revenue Authority (Amendment) Act, 2023 | 3 | `sha256:...` (verified) |
| Act No. 27 of 2023 | The Value Added Tax (Amendment) Act, 2023 | 2 | `sha256:...` (verified) |
| Act No. 28 of 2023 | The Local Government (Amendment) Act, 2023 | 2 | `sha256:...` (verified) |
| Act No. 29 of 2023 | The Appropriation Act, 2023 | 2 | `sha256:...` (verified) |

## Parse Quality Notes

- **Act No. 26 of 2023** (3 sections), **No. 27** (2 sections), **No. 28** (2 sections), **No. 29** (2 sections): Brief amendment/appropriation acts — low section count expected. Flagged in gaps.md for re-parse verification.
- **Act No. 25 of 2023** (8 sections): Customs amendment — moderate section count, expected for amendment act.
- **Act No. 10 of 2026** (78 sections): Substantial new legislation — State-Owned Enterprise Act.
- **Act No. 11 of 2026** (87 sections): Substantial new legislation — Deposit Insurance Corporation Act.
- **Act No. 24 of 2023** (63 sections): Substantial new legislation — Access to Information Act.

## Budget

- Fetches this batch: 20 (4 index pages + 8 node pages + 8 PDFs)
- Rate limit: 2s between requests (parliament.gov.zm)
- Total fetches today (2026-04-11): 20/2000

## Integrity Checks

- No duplicate IDs: ✓ (166 total records)
- Source hash verification: ✓ (all 8 PDFs verified)
- Provenance fields complete: ✓
- amended_by/repealed_by references: ✓ (all resolve or empty)
- No fabricated citations: ✓

## Notable Acts

- **The State-Owned Enterprise Act, 2026 (Act No. 10 of 2026)**: 78 sections — comprehensive SOE governance framework
- **The Zambia Deposit Insurance Corporation Act, 2026 (Act No. 11 of 2026)**: 87 sections — new deposit insurance regime
- **The Access to Information Act, 2023 (Act No. 24 of 2023)**: 63 sections — FOI legislation

## Workaround Note

SSL certificate chain on parliament.gov.zm is missing the intermediate RapidSSL TLS RSA CA G1 cert.
Resolved by downloading the intermediate from DigiCert and creating a combined CA bundle.
git pull --ff-only failed on mounted workspace (FUSE/APFS lock file issue — same as all prior ticks).
Used /tmp clone at HEAD=3f7bbf1 (batch 0018 confirmed).
