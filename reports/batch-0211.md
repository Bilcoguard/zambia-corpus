# Batch 0211 — Phase 4 (sis_tax)

- started_at: 2026-04-25T03:33:26Z
- completed_at: 2026-04-25T03:35:48Z
- sub_phase: sis_tax
- discovery_alphabets: ['I', 'V', 'T']
- robots_sha256: fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0
- novel_pre_keyword: 72
- novel_post_keyword: 20
- records_written: 8/8
- discovery_fetches: 4
- ingest_fetches: 16
- slices: [[3, 5], [5, 7], [7, 9], [9, 11]]

## Records

- `si-zm-1985-026-income-tax-foreign-organisations-exemption-approval-no-7-order-1985` — Income Tax (Foreign Organisations) (Exemption Approval) (No. 7) Order, 1985 (sis_tax, 2 sections, 110625 bytes pdf)
- `si-zm-1985-027-income-tax-foreign-organisations-exemption-approval-no-8-order-1985` — Income Tax (Foreign Organisations) (Exemption Approval) (No. 8) Order, 1985 (sis_tax, 3 sections, 131136 bytes pdf)
- `si-zm-1985-049-income-tax-foreign-organisations-exemption-approval-no-9-order-1985` — Income Tax (Foreign Organisations) (Exemption Approval) (No. 9) Order, 1985 (sis_tax, 3 sections, 202709 bytes pdf)
- `si-zm-1985-050-income-tax-foreign-organisations-exemption-approval-no-10-order-1985` — Income Tax (Foreign Organisations) (Exemption Approval) (No. 10) Order, 1985 (sis_tax, 2 sections, 194081 bytes pdf)
- `si-zm-1984-011-customs-and-excise-amendment-bill-provisional-charging-order-1984` — Customs and Excise (Amendment) Bill (Provisional Charging) Order, 1984 (sis_tax, 2 sections, 183688 bytes pdf)
- `si-zm-1984-045-income-tax-foreign-organisations-exemption-approval-order-1984` — Income Tax (Foreign Organisations) (Exemption Approval) Order, 1984 (sis_tax, 6 sections, 353070 bytes pdf)
- `si-zm-1983-043-income-tax-foreign-organisations-exemption-approval-order-1983` — Income Tax (Foreign Organisations) (Exemption Approval) Order, 1983 (sis_tax, 4 sections, 206636 bytes pdf)
- `si-zm-1982-002-income-tax-foreign-organisations-exemption-approval-order-1982` — Income Tax (Foreign Organisations) (Exemption Approval) Order, 1982 (sis_tax, 3 sections, 119619 bytes pdf)

## Discovery candidates skipped (curation)

- 2022/004 VAT (Zero-Rating) (Amendment) Order — recurring pdf_parse_empty (image-only PDF, OCR backfill deferred)
- 2019/025 Income Tax (Suspension of Tax on Payment of Interest to Non-Resident) — recurring pdf_parse_empty (image-only PDF)
- 2017/043 Income Tax (Suspension of Tax on Payments to Non-Resident Contractors) (Batoka Hydro) — recurring pdf_parse_empty (image-only PDF)
- 1982/009 .. 1982/036 .. 1981/048 .. 1981/049 .. 1980/* — queued for batch 0212 (depth limited by MAX_BATCH_SIZE=8)

## Notes

- All 8 records committed under sis_tax. Income Tax (Foreign Organisations) (Exemption Approval) series progressed: 1985 No.7-No.10 (slots 26/27/49/50), 1984 (45), 1983 (43), 1982 No.1 (slot 2). One Customs and Excise (Amendment Bill) (Provisional Charging) Order, 1984 (slot 11) under Customs and Excise Act Cap.322.
- Robots.txt sha256 prefix unchanged (fce67b697ee4ef44, sha256 confirmed against batches 0193-0210).
- CHECK1-5 all PASS; no integrity failures.
- B2 sync deferred to host (rclone unavailable in sandbox).
