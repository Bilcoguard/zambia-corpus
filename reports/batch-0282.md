# Phase 4 — Batch 0282 Report

**Date (UTC):** 2026-04-26
**Sub-phase:** acts_in_force (chronological-first, page-2 cross-alphabet residuals)
**Source:** zambialii.org (`/akn/zm/act/<yr>/<num>`)
**Parser:** `0.6.0-act-zambialii-2026-04-26`
**User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
**Crawl-delay:** 6s (margin over robots-declared 5s)
**Robots.txt sha256:** `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` (re-verified at tick start; unchanged from b0193..b0281)
**Inherited pool:** `_work/batch_0281_remaining.json` (62 items)

## Picks

8 chronologically-earliest from inherited pool. Pre-flight slug-glob dedup: all 8 confirmed absent from `records/acts/<yr>/`.

| idx | yr/num | alpha | title | family |
|---|---|---|---|---|
| 0 | 2009/7  | S | Supplementary Appropriation (2007) Act, 2009 | fiscal |
| 1 | 2009/10 | A | Appropriation Act, 2009 | fiscal |
| 2 | 2009/16 | N | Non-Governmental Organisations Act, 2009 | NON-FISCAL |
| 3 | 2009/30 | A | Appropriation (No. 2) Act, 2009 | fiscal |
| 4 | 2010/4  | P | Public Interest Disclosure (Protection of Whistleblowers) Act, 2010 | NON-FISCAL |
| 5 | 2010/11 | S | Supplementary Appropriation (2008) Act, 2010 | fiscal |
| 6 | 2010/23 | E | Excess Expenditure Appropriation (2007) Act, 2010 | fiscal |
| 7 | 2011/25 | S | Supplementary Appropriation (2009) Act, 2011 | fiscal |

## Results

| idx | yr/num | status | sections | notes |
|---|---|---|---|---|
| 0 | 2009/7  | ok               | 1  | OCR-section-tolerant retry candidate (sec 1 missed; sec 2 real Act content) |
| 1 | 2009/10 | pdf_too_large    | -  | PDF 6,920,632 bytes > MAX_PDF_BYTES (4,500,000); deferred — raw HTML kept |
| 2 | 2009/16 | ok               | 37 | NGO Act parsed via HTML akn-section path (no PDF fallback needed) |
| 3 | 2009/30 | pdf_too_large    | -  | PDF 6,007,886 bytes > MAX_PDF_BYTES; deferred — raw HTML kept |
| 4 | 2010/4  | ok               | 84 | Whistleblowers Act parsed via HTML akn-section path; sections 1..59 + sub-clusters |
| 5 | 2010/11 | ok               | 2  | fiscal 2-section pattern via PDF fallback |
| 6 | 2010/23 | ok               | 2  | fiscal 2-section pattern via PDF fallback |
| 7 | 2011/25 | ok               | 2  | fiscal 2-section pattern via PDF fallback |

**Yield: 6/8 (75%).**

## Records committed (6)

- `act-zm-2009-007-supplementary-appropriation-2007-act` — `Act No. 7 of 2009`
- `act-zm-2009-016-non-governmental-organisations-act` — `Act No. 16 of 2009`
- `act-zm-2010-004-public-interest-disclosure-protection-of-whistleblowers-act` — `Act No. 4 of 2010`
- `act-zm-2010-011-supplementary-appropriation-2008-act` — `Act No. 11 of 2010`
- `act-zm-2010-023-excess-expenditure-appropriation-2007-act` — `Act No. 23 of 2010`
- `act-zm-2011-025-supplementary-appropriation-2009-act` — `Act No. 25 of 2011`

## Integrity (`_work/batch_0282_integrity.txt`)

- CHECK1a PASS: 6/6 batch unique
- CHECK1b PASS: 6/6 corpus presence on disk
- CHECK2 PASS: 0 amended_by refs (count=0)
- CHECK3 PASS: 0 repealed_by refs (count=0)
- CHECK4 PASS: 6/6 source_hash sha256 verified against `raw/zambialii/act/<yr>/<num>.html`
- CHECK5 PASS: 16 required fields × 6 = 96/96 present
- CHECK6 PASS: cited_authorities 0 refs all resolve
- **ALL CHECKS PASSED**

## Deferrals (added to gaps.md, raw kept)

- **2009/10** Appropriation Act, 2009 — pdf_too_large (6,920,632 bytes)
- **2009/30** Appropriation (No. 2) Act, 2009 — pdf_too_large (6,007,886 bytes)
- **2009/7** added to OCR section-tolerant retry queue (1 of 2 sections captured; sec 1 missed by OCR — same pattern as 1988/32, 1994/40, 2004/6)

## Costs

- Today (2026-04-26) at tick start: 535 fetches (~27% of 2000/day budget)
- This tick: 1 robots reverify + 8 record HTML + 8 PDF fallbacks = 17 fetches
- Today end: 552/2000 (~27.6%)
- Tokens: within budget

## Next-tick plan (batch 0283)

1. Refresh inherited pool from `_work/batch_0282_remaining.json` (54 items).
2. Pick next 8 chronological from `2011/26` onwards: 2011/26, 2011/32, 2012/4, 2012/5, 2012/16, 2013/7, 2013/8, 2013/19.
3. All 8 fiscal-series — yield expected to revert to ~75% baseline.
4. Re-verify robots.txt at start of next tick.

## Open follow-ups

- **Oversize-PDF queue (4 items):** 2002/6, 2005/21, 2008/5, 2009/10, 2009/30 — host-side handler needed to chunk/extract text from PDFs > 4.5 MB.
- **OCR section-tolerant retry queue (6 items):** 1988/32 (0 sec), 1994/40 (sec 1 missed), 1995/33 (full re-extract — quarantined), 2004/6 (sec 1 missed), 2008/9 (over-match cleanup), 2009/7 (sec 1 missed).
- **OCR backlog (18 items):** image-only PDFs awaiting OCR pipeline.
- **B2 sync deferred to host:** `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4` — rclone unavailable in sandbox.
- **Phase 4 remains incomplete** per approvals.yaml. Worker does not flip.
