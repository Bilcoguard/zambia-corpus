# Batch 0256 Report — Phase 4 Bulk (acts_in_force, alphabets E + F)

**Date:** 2026-04-26
**Phase:** phase_4_bulk (priority_order item 1: acts_in_force)
**Yield:** 7 / 7 (100%)

## Discovery

- Probed `https://zambialii.org/legislation?alphabet=E&nature=act` (single-page listing, 45 unique act hrefs)
- Probed `https://zambialii.org/legislation?alphabet=F&nature=act` (single-page listing, 15 unique act hrefs)
- Filtered against existing act IDs and dropped tokens: amendment / appropriation / supplementary / validation / transitional / repeal / continuation / excess expenditure
- Result: 7 primary candidates (4 from E, 3 from F)

## Picks

| Alpha | Yr/Num | Title | Sections |
|-------|--------|-------|----------|
| E | 1933/10 | Employment of Young Persons and Children Act, 1933 | 21 |
| E | 1963/4  | English Law (Extent of Application) Act, 1963       | 2  |
| E | 1964/31 | Evidence (Bankers' Books) Act, 1964                 | 9  |
| E | 1964/43 | Emergency Powers Act, 1964                          | 6  |
| F | 1937/5  | Foreign Judgments (Reciprocal Enforcement) Act, 1937 | 13 |
| F | 1949/19 | Fencing Act, 1949                                   | 25 |
| F | 1966/2  | Factories Act, 1966                                 | 105|

All 7 are FIRST acts_in_force entries from their respective alphabets (no prior coverage of E or F primary acts in the corpus).

## Integrity

- CHECK1a (batch unique IDs) — PASS 7/7
- CHECK1b (corpus presence) — PASS 7/7
- CHECK2 (amended_by) — PASS 0 refs
- CHECK3 (repealed_by) — PASS 0 refs
- CHECK4 (source_hash sha256) — PASS 7/7 verified against raw/zambialii/act/(1933,1937,1949,1963,1964,1966)/
- CHECK5 (required fields × records) — PASS 10×7 all present
- CHECK6 (cited_authorities) — PASS 0 refs

## Provenance

- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- Robots.txt re-verified at tick start (sha256 prefix `fce67b697ee4ef44`, unchanged from batches 0193-0255)
- Crawl-delay: 5s declared; honoured at 6s margin per request
- Parser: `0.6.0-act-zambialii-2026-04-26` (HTML akn-section primary; PDF fallback unused)

## Cost (this tick)

- 1 robots reverify + 2 alphabet listing fetches + 7 record HTML fetches = 10 fetches on zambialii.org
- Pre-tick today fetches: 171; post-tick: 181 / 2000 (9.05% of daily budget)
- Tokens within budget

## Notes

- All 7 records parsed cleanly via HTML akn-section structure; no PDF fallback required
- Largest record (Factories Act 1966) has 105 sections — long-tick parser handled cleanly
- Continues acts_in_force pivot from batches 0253 (A-C), 0254 (C residual drain), 0255 (D)
- Reserved residuals carried from batch 0255: 2 alphabet=C deferred (Citizens Economic Empowerment 2006/9, Constitution of Zambia 1996/17 — large, dedicated batches) + 1 SI residual (1990/39 ZNPF >4.5MB OCR backlog at 15 items)

## Next-tick plan

- Probe alphabet=G (likely small primary count given prior alphabets pattern)
- Continue alphabetic walk through G-K per running plan
- OCR backlog (15 items) deferred until tesseract is wired to host
