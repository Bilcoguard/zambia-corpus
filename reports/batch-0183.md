# Batch 0183 — Phase 4 (sis_tax sub-phase)

**Batch:** 0183
**Phase:** phase_4_bulk
**Sub-phase:** sis_tax (priority_order item 3)
**Started:** 2026-04-24T13:33Z
**Completed:** 2026-04-24T13:38Z (executed as four 2-target slices to fit 45 s bash-tool timeout; six of eight targets succeeded, two logged as PDF parse empty)
**Records written:** 6
**Fetches used:** 16 ingest fetches (8 × AKN HTML + 8 × PDF). Today's running fetch count ~142/2000 (7.1% of daily budget).
**Integrity:** ALL PASS (CHECK1 unique IDs within batch, CHECK2 batch IDs unique in HEAD, CHECK3 source_hash matches on-disk raw for all 6, CHECK4 no unresolved cross-refs, CHECK5 required fields present)

## Records

| ID | Title | Sections | PDF bytes |
|---|---|---:|---:|
| si-zm-2017-074-income-tax-exemption-of-tax-on-interest-payments-to-overseas-lenders-by-maamba-c | Income Tax (Exemption of tax on interest payments to overseas lenders by Maamba Collieries Limited) (Approval and Exemption) Order, 2017 | 2 | 141,724 |
| si-zm-2020-011-income-tax-royal-haskoning-dhv-pty-limited-approval-and-exemption-order-2020 | Income Tax (Royal Haskoning DHV (PTY) Limited) (Approval and Exemption) Order, 2020 | 4 | 10,342 |
| si-zm-2022-032-income-tax-john-snow-health-zambia-limited-approval-and-exemption-order-2022 | Income Tax (John Snow Health Zambia Limited) (Approval and Exemption) Order, 2022 | 6 | 289,731 |
| si-zm-2024-065-income-tax-gopa-infra-gmbh-approval-and-exemption-order-2024 | Income Tax (GOPA Infra GmbH) (Approval and Exemption) Order, 2024 | 12 | 3,776,199 |
| si-zm-2025-089-income-tax-gopa-infra-gmbh-approval-and-exemption-order-2025 | Income Tax (GOPA Infra GmbH) (Approval and Exemption) Order, 2025 | 11 | 325,782 |
| si-zm-2025-092-income-tax-konoike-construction-company-limited-approval-and-exemption-order-202 | Income Tax (Konoike Construction Company Limited) (Approval and Exemption) Order, 2025 | 7 | 373,023 |

## Substance
Donor / DFI / project-specific tax exemption orders — day-to-day utility for structuring incoming grant funding and project-finance transactions:

- **Maamba Collieries 2017** — interest-payment WHT exemption on overseas lender interest for the Maamba IPP (high-value precedent for structuring project-finance WHT carve-outs).
- **Royal Haskoning DHV 2020** — bilateral Dutch-funded infrastructure consultancy exemption (WHT / income tax concession; small but precedent-useful for RVO-backed projects).
- **John Snow Health Zambia 2022** — USAID health delivery NGO tax exemption (precedent for US-funded PEPFAR / global-health NGO structuring).
- **GOPA Infra GmbH 2024** — BMZ / KfW German technical-cooperation infrastructure exemption (12 substantive articles; the larger of the two GOPA orders).
- **GOPA Infra GmbH 2025** — renewed / superseding 2025 order (compare side-by-side to 2024 for scope and duration drafting shifts).
- **Konoike Construction 2025** — Japanese contractor exemption on donor-funded civil-works contract (precedent for JICA-backed project tax carve-outs).

All six are Approval/Exemption Orders under the Income Tax Act — narrow operative instruments useful as drafting precedents for bespoke project tax exemptions, and as compliance references when advising on WHT and corporate tax on NGO / donor-funded operations in Zambia.

## Gaps logged
Two targets failed with `pdf_parse_empty` (likely text-as-image / scanned PDFs — pdfplumber returns no extractable text):

- **si/2017/043** Income Tax (Suspension of Tax on Payments to Non-Resident Contractors) (Batoka Hydro-Electric Scheme and Kariba Dam Rehabilitation Projects) Regulations, 2017
- **si/2019/025** Income Tax Act (Suspension of tax on payment of interest to non-resident) (Treasury Bill and Bond) Regulations, 2019 (already logged twice in batch 0179 — confirmed scanned-image PDF; should be deprioritised until an OCR pass is approved)

Both entries appended to `gaps.md` with status, URL, timestamp, and batch number. Raw PDFs fetched (hashes in provenance.log) but not parsed to records — will require an OCR pre-pass (tesseract or cloud OCR) before re-ingestion.

## Discovery channel
Continued from `_work/batch_0182_candidates.json` (54 modern tax SIs queued after the /legislation/?alphabet=I discovery pass in batch 0182). Five priority items identified in batch 0182's next-tick plan plus three additional modern tax SIs (2017/043 Batoka, 2019/025 Treasury Bill/Bond, 2025/092 Konoike) from the same queue.

## Fetch detail
All 16 fetches honoured ZambiaLII robots.txt `Crawl-delay: 5` (6 s pacing with +1 s margin). User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`. Endpoints used: `/akn/zm/act/si/YYYY/NN` (HTML title/PDF-link discovery) and `/akn/zm/act/si/YYYY/NN/eng@DATE/source.pdf` (operative text).

## Operational note
Script (`_work/batch_0183.py`) sliced into four 2-target invocations (`--slice=0:2`, `2:4`, `4:6`, `6:8`) to fit the sandbox's 45 s bash-tool timeout. Each invocation checkpoints to `_work/batch_0183_summary.json` and `.batch_0183_state.json`. All eight targets attempted; six succeeded first try, two deterministic PDF-empty failures (scanned sources, not worker bugs).

## Next-tick plan
sis_tax sub-phase now has **26 records** in HEAD (8 from batch 0180 + 6 from 0181 + 6 from 0182 + 6 from 0183). The priority_order threshold from batch 0182's plan (~25 records) has been reached — rotate to **sis_employment** (priority_order item 4) for batch 0184.

Suggested batch 0184 discovery: open `/legislation/?alphabet=E` or `/legislation/?alphabet=L` and filter for Employment-Act SIs, minimum-wage / labour regulations, and pension-fund rules. Candidates to probe:

- Employment Code Act SIs (Minimum Wages and Conditions of Employment orders)
- National Pension Scheme Authority (NAPSA) regulations
- Workers Compensation Fund SIs
- National Health Insurance Scheme regulations

Remaining tax-SI candidates from `_work/batch_0182_candidates.json` (48 older pre-2015 entries — mostly repetitive Foreign Organisations exemption orders) should be revisited later as a lower-priority sweep; many are narrow one-off exemptions with limited precedent value outside historical research.

## Infrastructure (non-blocking)
Stale `corpus.sqlite-journal` rollback journal still blocks FTS rebuild — sandbox rm is denied. Human-side: delete journal, rebuild SQLite from `records/` JSON corpus to restore Phase 5 retrieval surface.

Pre-existing duplicate IDs in `records/acts/` (34 acts exist as both `records/acts/{id}.json` AND `records/acts/{year}/{id}.json`) — not introduced by this batch, but should be de-duplicated during Phase 5 index rebuild. All are in `records/acts/` (root-level + year-folder); no SI record duplicates.

B2 raw sync deferred to host — rclone not available in sandbox:
```
rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
```
