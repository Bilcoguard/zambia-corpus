# Batch 0043 Report

**Date:** 2026-04-11T13:44:40Z
**Phase:** 4 (Bulk Ingestion)
**Records added:** 7
**Source:** parliament.gov.zm

## Records

| # | ID | Title | Sections | PDF Size |
|---|---|---|---|---|
| 23 | `act-zm-2015-023` | Appropriation Act, 2015 | 2 | 214,835 bytes |
| 22 | `act-zm-2015-022` | Gender Equity and Equality Act, 2015 | 89 | 98,709 bytes |
| 2 | `act-zm-2014-002` | Service Commissions (Amendment) Act, 2014 | 1 | 158,307 bytes |
| 3 | `act-zm-2014-003` | Business Regulatory Act, 2014 | 1 | 8,644,803 bytes |
| 4 | `act-zm-2014-004` | Zambia Chartered Institute of Logistics and Transport Act, 2014 | 88 | 7,287,148 bytes |
| 5 | `act-zm-2014-005` | Supplementary Appropriation (2012) Act, 2014 | 2 | 753,657 bytes |
| 14 | `act-zm-2014-014` | Appropriation Act, 2014 | 3 | 52,796 bytes |

## Notes

- 2015 Acts now COMPLETE (all 23 ingested, minus No. 2 and 10 — no PDFs on parliament.gov.zm).
- 2014 Acts progress: 5/~14+ ingested (No. 2-5, 14). Acts No. 6-12 have no PDF attached on parliament.gov.zm — logged to gaps.md.
- Gender Equity and Equality Act (89 sections) is a substantial piece of legislation.
- Business Regulatory Act and ZCILT Act are very large PDFs (~8.6MB and ~7.3MB respectively) — may be scanned images. Section extraction yielded only 1 and 88 sections respectively; re-parse recommended for No. 3.
- Appropriation/Supplementary Appropriation acts have expected low section counts (schedule-heavy).

## Fetches

- Discovery pages: ~30+
- Node pages: 7
- PDFs: 7
- Total fetch count this batch: 69

## Gaps logged

- 2014 No. 6 (Excess Expenditure Appropriation 2011) — no PDF on node page
- 2014 No. 7 (Income Tax Amendment) — no PDF on node page
- 2014 No. 8 (Customs and Excise Amendment) — no PDF on node page
- 2014 No. 9 (Property Transfer Tax Amendment) — no PDF on node page
- 2014 No. 10 (ZRA Amendment / VAT Amendment) — no PDF on node page
- 2014 No. 11 (Mines and Minerals Development Amendment) — no PDF on node page
- 2014 No. 12 (Local Government Amendment) — no PDF on node page
