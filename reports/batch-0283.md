# Phase 4 — Batch 0283 Report

**Date (UTC):** 2026-04-26
**Sub-phase:** acts_in_force (chronological-first, fiscal-series sweep 2011→2013)
**Source:** zambialii.org (`/akn/zm/act/<yr>/<num>`)
**Parser:** `0.6.0-act-zambialii-2026-04-26`
**User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
**Crawl-delay:** 6s (margin over robots-declared 5s)
**Robots.txt sha256:** `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` (re-verified at tick start; unchanged from b0193..b0282)
**Inherited pool:** `_work/batch_0282_remaining.json` (54 items)

## Picks

8 chronologically-earliest from inherited pool. Pre-flight slug-glob dedup: all 8 confirmed absent from `records/acts/<yr>/`.

| idx | yr/num | alpha | title | family |
|---|---|---|---|---|
| 0 | 2011/26 | E | Excess Expenditure Appropriation (2008) Act, 2011 | fiscal |
| 1 | 2011/32 | A | Appropriation Act, 2011                           | fiscal |
| 2 | 2012/4  | E | Excess Expenditure Appropriation (2009) Act, 2012 | fiscal |
| 3 | 2012/5  | S | Supplementary Appropriation (2010) Act, 2012      | fiscal |
| 4 | 2012/16 | A | Appropriation Act, 2012                           | fiscal |
| 5 | 2013/7  | E | Excess Expenditure Appropriation (2010) Act, 2013 | fiscal |
| 6 | 2013/8  | S | Supplementary Appropriation (2011) Act, 2013      | fiscal |
| 7 | 2013/19 | A | Appropriation Act, 2013                           | fiscal |

## Results

| idx | yr/num | status | sections | notes |
|---|---|---|---|---|
| 0 | 2011/26 | ok            | 2 | fiscal 2-section pattern via PDF fallback |
| 1 | 2011/32 | ok            | 2 | fiscal 2-section pattern via PDF fallback |
| 2 | 2012/4  | ok            | 2 | fiscal 2-section pattern via PDF fallback |
| 3 | 2012/5  | ok            | 2 | fiscal 2-section pattern via PDF fallback |
| 4 | 2012/16 | pdf_too_large | - | PDF 5,553,668 bytes > MAX_PDF_BYTES (4,500,000); deferred — raw HTML kept |
| 5 | 2013/7  | ok            | 2 | fiscal 2-section pattern via PDF fallback |
| 6 | 2013/8  | ok            | 2 | fiscal 2-section pattern via PDF fallback |
| 7 | 2013/19 | ok            | 1 | OCR-section-tolerant retry candidate (sec 1 missed; sec 2 real Act content) |

**Yield: 7/8 (87.5%).** Above 75% baseline.

## Records committed (7)

- `act-zm-2011-026-excess-expenditure-appropriation-2008-act` — `Act No. 26 of 2011`
- `act-zm-2011-032-appropriation-act` — `Act No. 32 of 2011`
- `act-zm-2012-004-excess-expenditure-appropriation-2009-act` — `Act No. 4 of 2012`
- `act-zm-2012-005-supplementary-appropriation-2010-act` — `Act No. 5 of 2012`
- `act-zm-2013-007-excess-expenditure-appropriation-2010-act` — `Act No. 7 of 2013`
- `act-zm-2013-008-supplementary-appropriation-2011-act` — `Act No. 8 of 2013`
- `act-zm-2013-019-appropriation-act` — `Act No. 19 of 2013`

## Integrity (`_work/batch_0283_integrity.txt`)

- CHECK1a PASS: 7/7 batch unique
- CHECK1b PASS: 7/7 corpus presence on disk
- CHECK2 PASS: 0 amended_by refs (count=0 in batch; 0 across corpus)
- CHECK3 PASS: 7 repealed_by refs (legacy corpus refs all resolve)
- CHECK4 PASS: 7/7 source_hash sha256 verified against `raw/zambialii/act/<yr>/<num>.html`
- CHECK5 PASS: 16 required fields × 7 = 112/112 present
- CHECK6 PASS: cited_authorities 0 refs all resolve
- **ALL CHECKS PASSED**

Note: pre-existing tombstone files (`records/acts/act-zm-<yr>-chiefs-order.json`) lack the standard `id` field — these are reclassification forwarding stubs, not real records, and are unaffected by this batch.

## Deferrals (added to gaps.md, raw kept)

- **2012/16** Appropriation Act, 2012 — pdf_too_large (5,553,668 bytes); raw HTML retained at `raw/zambialii/act/2012/2012-016.html`
- **2013/19** added to OCR section-tolerant retry queue (1 of 2 sections captured; sec 1 missed by OCR — same pattern as 1988/32, 1994/40, 2004/6, 2009/7)

## Costs

- Today (2026-04-26) at tick start: 550 fetches (~27.5% of 2000/day budget)
- This tick: 8 record HTML + 8 PDF fallback attempts (1 pre-fail oversize) = 16 fetches
- Today end: 566/2000 (~28.3%)
- Tokens: within budget

## Next-tick plan (batch 0284)

1. Refresh inherited pool from `_work/batch_0283_remaining.json` (46 items).
2. Pick next 8 chronological from `2014/5` onwards: 2014/5, 2014/6, 2014/14, 2015/9, 2015/10, 2015/23, 2016/7, 2016/15.
3. Mix of fiscal-series (5) and non-fiscal (Court of Appeal Act 2016/7, Public Protector Act 2016/15) — yield expected ≥75%.
4. Re-verify robots.txt at start of next tick.

## Open follow-ups

- **Oversize-PDF queue (5 items):** 2002/6, 2005/21, 2008/5, 2009/10, 2009/30, 2012/16 — host-side handler needed to chunk/extract text from PDFs > 4.5 MB.
- **OCR section-tolerant retry queue (7 items):** 1988/32 (0 sec), 1994/40 (sec 1 missed), 1995/33 (full re-extract — quarantined), 2004/6 (sec 1 missed), 2008/9 (over-match cleanup), 2009/7 (sec 1 missed), 2013/19 (sec 1 missed).
- **OCR backlog (18 items):** image-only PDFs awaiting OCR pipeline.
- **B2 sync deferred to host:** `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4` — rclone unavailable in sandbox.
- **Phase 4 remains incomplete** per approvals.yaml. Worker does not flip.
