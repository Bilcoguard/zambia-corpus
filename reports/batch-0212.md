# Batch 0212 — Phase 4 (sis_tax)

- started_at: 2026-04-25T04:01:20Z
- completed_at: 2026-04-25T04:09:00Z
- sub_phase: sis_tax
- discovery_alphabets: ['I', 'V', 'C', 'T']
- robots_sha256: fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0
- novel_pre_keyword: ~414 across alphabets I/V/C/T (98+15+245+56)
- novel_post_keyword: 22
- records_written: 8/8
- discovery_fetches: 5 (1 robots + 4 alphabet pages)
- ingest_fetches: 16 (8 HTML + 8 PDF)
- slices: [[13, 15], [15, 17], [17, 19], [19, 21]]

## Records

- `si-zm-1982-009-income-tax-foreign-organisations-exemption-approval-no-2-order-1982` — Income Tax (Foreign Organisations) (Exemption Approval) (No. 2) Order, 1982 (sis_tax)
- `si-zm-1982-036-income-tax-foreign-organisations-exemption-approval-no-3-order-1982` — Income Tax (Foreign Organisations) (Exemption Approval) (No. 3) Order 1982 (sis_tax)
- `si-zm-1981-048-income-tax-exempt-organisations-approval-order-1981` — Income Tax (Exempt Organisations) (Approval) Order, 1981 (sis_tax)
- `si-zm-1981-049-income-tax-foreign-organisations-exemption-approval-order-1981` — Income Tax (Foreign Organisations) (Exemption Approval) Order, 1981 (sis_tax)
- `si-zm-1980-014-income-tax-foreign-organisations-exemption-approval-order-1980` — Income Tax (Foreign Organisations) (Exemption Approval) Order, 1980 (sis_tax)
- `si-zm-1980-024-income-tax-foreign-organisations-exemption-approval-no-2-order-1980` — Income Tax (Foreign Organisations) (Exemption Approval) (No. 2) Order, 1980 (sis_tax)
- `si-zm-1980-029-income-tax-international-organisations-exemption-approval-order-1980` — Income Tax (International Organisations) (Exemption Approval) Order, 1980 (sis_tax)
- `si-zm-1980-038-income-tax-low-cost-housing-notice-1980` — Income Tax (Low Cost Housing) Notice, 1980 (sis_tax)

## Discovery candidates skipped (curation)

- 2022/004 VAT (Zero-Rating) (Amendment) Order — recurring pdf_parse_empty (image-only PDF, OCR backfill deferred)
- 2019/025 Income Tax (Suspension of Tax on Payment of Interest to Non-Resident) — recurring pdf_parse_empty (image-only PDF)
- 2017/001 Citizens Economic Empowerment (Reservation Scheme) Regulations — keyword-matched on "exemption" earlier; FP per batches 0207–0210, parented on CEE Act not a tax Act
- 2017/043 Income Tax (Suspension of Tax on Payments to Non-Resident Contractors) (Batoka Hydro) — recurring pdf_parse_empty (image-only PDF)
- 9 Control of Goods (Import Licence Fees) (Exemption) Notices spanning 1986–1991 — parent statute is Control of Goods Act, not Customs and Excise Act (FP per batch 0208/0210)
- 1980/051 Income Tax (Foreign Organisations) (Exemption Approval) (No. 3) Order 1980 — deferred to next tick (over MAX_BATCH_SIZE=8)

## Notes

- All 8 records committed under sis_tax. Income Tax (Foreign Organisations) (Exemption Approval) series advanced from 1982 No.2 down through 1980 No.2; plus Income Tax (Exempt Organisations) (Approval) Order 1981/048, Income Tax (International Organisations) (Exemption Approval) 1980/029, Income Tax (Low Cost Housing) Notice 1980/038.
- All records parented on Income Tax Act Cap.323.
- Robots.txt sha256 prefix unchanged (fce67b697ee4ef44, confirmed against batches 0193-0211).
- CHECK1–5 all PASS; no integrity failures.
- B2 sync deferred to host (rclone unavailable in sandbox).
