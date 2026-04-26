# Batch 0258 Report — Phase 4 Bulk (acts_in_force, alphabets J + K + L)

**Date:** 2026-04-26
**Phase:** phase_4_bulk (priority_order item 1: acts_in_force)
**Yield:** 8 / 8 (100%)

## Discovery

- Probed `https://zambialii.org/legislation?alphabet=J&nature=act` (single-page listing, 5 unique act hrefs)
- Probed `https://zambialii.org/legislation?alphabet=K&nature=act` (single-page listing, 1 unique act href)
- Probed `https://zambialii.org/legislation?alphabet=L&nature=act` (single-page listing, 24 unique act hrefs)
- Filtered against existing act IDs (930 act records cross-referenced via id-match `act-zm-{yr}-{padded-num}-` plus `Act No. N of YYYY` citation-match) and dropped tokens: amendment / appropriation / supplementary / validation / transitional / repeal / continuation / excess expenditure
- Result: 10 primary candidates (1 from J, 0 from K, 9 from L). Capped at MAX_BATCH_SIZE = 8 — picks fill the cap exactly. Two L-residuals deferred to next tick (1962/22 Local Authorities Superannuation Fund Act + Kazungula Bridge Authority Act 2024/12 was the only K candidate but skipped per cap rule prioritising lowest-disturbance carry order).
- Note: K alphabet listing returned exactly 1 candidate (2024/12 Kazungula Bridge Authority Act) — deferred to next-tick K residual.

## Picks

| Alpha | Yr/Num | Title                                                          | Sections | Source |
|-------|--------|----------------------------------------------------------------|----------|--------|
| J     | 1961/10 | Judgments Act                                                 | 3  | HTML |
| L     | 1973/23 | Law Association of Zambia Act, 1973                           | 25 | HTML |
| L     | 1963/27 | Law Reform (Frustrated Contracts) Act, 1963                   | 4  | HTML |
| L     | 1963/13 | Law Reform (Limitation of Actions, etc.) Act, 1963            | 6  | HTML |
| L     | 1982/27 | Legal Services Corporation Act, 1982                          | 12 | PDF fallback |
| L     | 1992/22 | Legal Services Corporation (Dissolution) Act, 1992            | 35 | PDF fallback |
| L     | 1931/21 | Loan Act, 1931                                                | 5  | HTML |
| L     | 1957/26 | Loans (Authorisation) Act, 1957                               | 7  | HTML |

All 8 are FIRST acts_in_force entries from alphabets J and L.

## Integrity

- CHECK1a (batch unique IDs) — PASS 8/8
- CHECK1b (corpus presence on disk) — PASS 8/8
- CHECK2 (amended_by) — PASS 0 refs
- CHECK3 (repealed_by) — PASS 0 refs
- CHECK4 (source_hash sha256) — PASS 8/8 verified against raw/zambialii/act/(1931,1957,1961,1963,1973,1982,1992)/
- CHECK5 (required fields × records) — PASS 14×8 all present
- CHECK6 (cited_authorities) — PASS 0 refs

## Provenance

- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- Robots.txt re-verified at tick start (sha256 prefix `fce67b697ee4ef44`, unchanged from batches 0193-0257)
- Crawl-delay: 5s declared; honoured at 6s margin per request
- Parser: `0.6.0-act-zambialii-2026-04-26` (HTML akn-section primary; PDF fallback used for 2 acts (1982/27 + 1992/22) where HTML had < 2 sections — both recovered cleanly via pdfplumber)

## Cost (this tick)

- 1 robots reverify + 3 alphabet listing fetches (J, K, L) + 8 record HTML fetches + 2 source.pdf fallback fetches (1982/27 + 1992/22) = 14 fetches on zambialii.org
- Pre-tick today fetches: 193; post-tick: 207 / 2000 (10.35% of daily budget)
- Tokens within budget

## Notes

- All 8 records ingested cleanly; 6 via HTML akn-section, 2 via PDF fallback (1982/27 + 1992/22)
- Smallest record (Judgments Act 1961/10) has 3 sections — short residual statute; matches expected one-shot judgments enforcement pattern
- Largest record (Legal Services Corporation (Dissolution) Act 1992/22) has 35 sections — winding-up statute parsed via PDF fallback
- Continues acts_in_force pivot from batches 0253 (A-C), 0254 (C residual drain), 0255 (D), 0256 (E + F), 0257 (G + H + I)
- Mid-tick: ingestion split across two `batch_0258_one.py` runs (slices 0-4 and 4-8) to fit within host 45s bash timeout; final 1957/26 ingested in a third sub-run after the second slice timed out at the 8th record. All sub-runs reuse the same `ingest_one()` from `batch_0258.py` (identical parser, UA, crawl-delay).
- Alphabet K returned exactly 1 candidate (2024/12 Kazungula Bridge Authority Act) — deferred to next tick to maintain alphabetic-walk continuity
- Reserved residuals carried from prior ticks: 2 alphabet=C deferred (Citizens Economic Empowerment 2006/9, Constitution of Zambia 1996/17 — large, dedicated batches) + 1 SI residual (1990/39 ZNPF >4.5MB OCR backlog at 15 items)
- Fresh residual carried from this tick: 1 alphabet=L candidate (1962/22 Local Authorities Superannuation Fund Act) + 1 alphabet=K candidate (2024/12 Kazungula Bridge Authority Act)

## Next-tick plan

- Continue alphabetic walk to alphabets M-N-O per running plan; sweep remaining K (2024/12) and L (1962/22) residuals first
- OCR backlog (15 items) deferred until tesseract is wired to host
- SQLite rebuild deferred to host: `corpus.sqlite` reflects 543 records (snapshot from earlier rebuild) vs 1502 JSON records on disk after this batch — periodic full rebuild expected from host

## Cumulative footprint

- Acts: 930 (pre-tick) + 8 = 938
- SIs: 593 (unchanged from batch 0252)
- Judgments: 25 (paused per robots Disallow on /akn/zm/judgment/)
