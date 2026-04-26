# Batch 0248 Report — Phase 4 Bulk Ingest

**Date:** 2026-04-26T02:09:18Z
**Phase:** phase_4_bulk
**Strategy:** Pure cache-drain — drain 8 of 17 reserved residuals carried from batch 0247 (alphabet=E + alphabet=N novels). 9 residuals reserved for next-tick drain (1980s/1990s era + 2004/22 NCC Exemption).

## Yield
- Attempted: 8 records
- OK: 8 records (yield 100%)
- Skip: 0
- Fail: 0

## Records ingested

| # | Year/Num | Pages | Chars | Sub-phase | Title |
|---|---|---|---|---|---|
| 0 | 2016/3 | 26 | 30777 | sis_corporate | si-zm-2016-003-estate-agents-general-regulations-2016 |
| 1 | 2015/39 | 14 | 17182 | sis_industry | si-zm-2015-039-national-council-for-construction-registration-of-projects-regulations-2015 |
| 2 | 2015/89 | 2 | 826 | sis_governance | si-zm-2015-089-national-museums-declaration-order-2015 |
| 3 | 2016/59 | 2 | 1267 | sis_governance | si-zm-2016-059-national-museums-entry-fees-regulations-2016 |
| 4 | 2009/37 | 26 | 41457 | sis_industry | si-zm-2009-037-national-council-for-construction-forms-and-fees-regulations-2009 |
| 5 | 2008/24 | 18 | 30989 | sis_governance | si-zm-2008-024-national-constitutional-conference-committees-regulations-2008 |
| 6 | 2008/16 | 2 | 1737 | sis_transport | si-zm-2008-016-national-road-fund-charges-and-fees-apportionment-regulations-2008 |
| 7 | 2005/19 | 2 | 831 | sis_transport | si-zm-2005-019-national-road-fund-act-commencement-order-2005 |


## Sub-phase footprint
- sis_corporate +1 (Estate Agents Act: 2016/003 General Regs — extends priority_order item 2 sis_corporate cluster from batch 0243)
- sis_industry +2 (National Council for Construction Act: 2015/039 Registration of Projects + 2009/037 Forms and Fees — extends priority_order outside-named-items sis_industry cluster from batch 0244)
- sis_governance +3 (National Museums Act: 2015/089 Declaration + 2016/059 Entry Fees + National Constitutional Conference Act: 2008/024 Committees — broadens sis_governance footprint)
- sis_transport +2 (National Road Fund Act: 2008/016 Charges and Fees Apportionment + 2005/019 Commencement Order)

## Discovery cost
- 1 robots.txt re-verification (sha256 prefix fce67b697ee4ef44 unchanged from batches 0193-0247)
- 0 listing probes (pure cache-drain from batch 0247 reserved residuals — zero fresh discovery this tick)
- Total discovery fetches: 1

## Per-record cost
- 16 fetches (8 HTML + 8 PDF for ok records)

## Integrity check
- CHECK1a (batch unique): 8/8 PASS
- CHECK1b (corpus presence on disk): 8/8 PASS
- CHECK2 (amended_by resolves): 0 refs PASS
- CHECK3 (repealed_by resolves): 0 refs PASS
- CHECK4 (sha256 verified against raw files): 8/8 PASS
- CHECK5 (10 required fields): 8/8 PASS
- CHECK6 (cited_authorities resolves): 0 refs PASS
- **ALL PASS**

## Cumulative
- SI records after this batch: 567 (+8 over batch 0247's 559)
- Judgments: 25 (paused per robots Disallow on /akn/zm/judgment/)
- Acts: unchanged (Phase 4 priority_order item 1 acts_in_force pending Acts-listing endpoint discovery)

## Reserved residuals carry to next tick
9 candidates from batch 0247 alphabet=E + alphabet=N novels:
- 1985/14 Equity Levy (Exemption) Order
- 1986/32 National Archives (Place of Deposit) (Declaration) Order
- 1987/29 Equity Levy (Exemption) Order
- 1987/36 National Savings and Credit (Appointment of Members of Board) Order
- 1988/38 Emergency (Essential Supplies and Services) Regulations
- 1993/37 Emergency Regulations
- 1995/29 National Archives (Fees) Regulations
- 1995/30 National Archives (Place of Deposit) (Revocation) Order
- 2004/22 National Council for Construction (Exemption) Regulations

Note: These 8 of 9 are 1980s-1990s era; expect higher pdf_parse_empty rate due to scanned-image PDFs.
2004/22 is text-era and likely text-extractable.

## Notes
- Robots.txt re-verified: sha256 prefix fce67b697ee4ef44 unchanged across batches 0193-0247
- All fetches honoured 5s crawl-delay using 6s margin
- B2 raw sync: rclone unavailable in sandbox — deferred to host
- OCR backlog unchanged at 14 items (no new fails this tick)
