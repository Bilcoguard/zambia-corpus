# Batch 0037 Report — Phase 4 (Bulk Ingestion)

**Date:** 2026-04-11T10:38:01Z
**Phase:** 4 — bulk ingestion (acts_in_force)
**Source:** parliament.gov.zm
**Batch size:** 8 records

## Records Ingested

| # | ID | Title | Sections | Citation |
|---|-----|-------|----------|----------|
| 1 | act-zm-2016-034-the-ratification-of-international-agreements | The Ratification of International Agreements | 21 | Act No. 34 of 2016 |
| 2 | act-zm-2016-035-the-electoral-process | The Electoral Process | 202 | Act No. 35 of 2016 |
| 3 | act-zm-2016-036-the-supplementary-appropriation | The Supplementary Appropriation | 2 | Act No. 36 of 2016 |
| 4 | act-zm-2016-037-excess-expenditure-appropriation-2013 | Excess Expenditure Appropriation (2013) | 2 | Act No. 37 of 2016 |
| 5 | act-zm-2016-038-supplementary-appropriation-2014 | Supplementary Appropriation (2014) | 2 | Act No. 38 of 2016 |
| 6 | act-zm-2016-039-the-supplementary-appropriation-2016 | The Supplementary Appropriation (2016) | 2 | Act No. 39 of 2016 |
| 7 | act-zm-2016-040-the-patents-act | The Patents Act | 223 | Act No. 40 of 2016 |
| 8 | act-zm-2016-041-the-securities | The Securities | 358 | Act No. 41 of 2016 |

## Fetch Stats

- Index page fetches: 7 (discovery across pages 14-15 + initial)
- Node page fetches: 8
- PDF fetches: 8
- Total fetches this batch: 16 (+ 7 discovery = 23 total)

## Notable

- **The Electoral Process Act** (202 sections) — comprehensive electoral legislation
- **The Patents Act** (223 sections) — full IP protection framework
- **The Securities Act** (358 sections) — major financial regulation act
- **This batch completes ALL 2016 Acts (No. 1-41)**

## Parse Quality Flags

- act-zm-2016-036-the-supplementary-appropriation: 2 sections (appropriation act, low count expected)
- act-zm-2016-037-excess-expenditure-appropriation-2013: 2 sections (appropriation act, low count expected)
- act-zm-2016-038-supplementary-appropriation-2014: 2 sections (appropriation act, low count expected)
- act-zm-2016-039-the-supplementary-appropriation-2016: 2 sections (appropriation act, low count expected)

## Integrity

All checks PASSED:
- No duplicate IDs (278 unique records total)
- All source hashes verified against raw PDFs
- All amended_by/repealed_by references resolve
- All provenance fields present
