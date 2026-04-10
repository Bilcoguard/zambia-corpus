# Phase 4 Batch 0012 Report

**Generated:** 2026-04-10T22:15:00Z
**Batch:** 0012
**Phase:** 4 — bulk ingestion (acts_in_force)
**Source:** parliament.gov.zm
**Tranche:** 2021 Acts No. 1-6, 24-25

## Records ingested (8)

| ID | Title | Citation | Sections | PDF Size |
|----|-------|----------|----------|----------|
| `act-zm-2021-001-legal-aid-act-2021` | The Legal Aid Act, 2021 | Act No. 1 of 2021 | 100 | 131 KB |
| `act-zm-2021-002-cyber-security-and-cyber-crimes-act-2021` | The Cyber Security and Cyber Crimes Act, 2021 | Act No. 2 of 2021 | 138 | 192 KB |
| `act-zm-2021-003-data-protection-act-2021` | The Data Protection Act, 2021 | Act No. 3 of 2021 | 125 | 150 KB |
| `act-zm-2021-004-electronic-communications-and-transactions-act-2021` | The Electronic Communications and Transactions Act, 2021 | Act No. 4 of 2021 | 151 | 155 KB |
| `act-zm-2021-005-citizen-economic-empowerment-amendment-act-2021` | The Citizen Economic Empowerment (Amendment) Act, 2021 | Act No. 5 of 2021 | 2 | 9 KB |
| `act-zm-2021-006-compensation-fund-amendment-act-2021` | The Compensation Fund (Amendment) Act, 2021 | Act No. 6 of 2021 | 3 | 9 KB |
| `act-zm-2021-024-accountants-amendment-act-2021` | The Accountants (Amendment) Act, 2021 | Act No. 24 of 2021 | 3 | 9 KB |
| `act-zm-2021-025-urban-and-regional-planners-amendment-act-2021` | Urban and Regional Planners (Amendment) Act, 2021 | Act No. 25 of 2021 | 4 | 10 KB |

## Source integrity

All 8 new records passed:
- No duplicate IDs (111 total records in corpus)
- All source_hash values verified against on-disk raw PDF files
- JSON schema validation: all required fields present, jurisdiction = ZM

## Parse quality notes

- **act-zm-2021-005-citizen-economic-empowerment-amendment-act-2021** (2 sections): Brief amendment act; verify completeness.
- **act-zm-2021-006-compensation-fund-amendment-act-2021** (3 sections): Brief amendment act; verify completeness.
- **act-zm-2021-024-accountants-amendment-act-2021** (3 sections): Brief amendment act; verify completeness.

## Fetch summary

- Node page fetches: 8
- PDF fetches: 8
- Total fetches this batch: 16
- Total fetches today: 241/2000
- SSL: parliament.gov.zm certificate verification handled via requests library with verify=False; content integrity verified via sha256 hashes.
