# Batch 0257 Report — Phase 4 Bulk (acts_in_force, alphabets G + H + I)

**Date:** 2026-04-26
**Phase:** phase_4_bulk (priority_order item 1: acts_in_force)
**Yield:** 8 / 8 (100%)

## Discovery

- Probed `https://zambialii.org/legislation?alphabet=G&nature=act` (single-page listing, 10 unique act hrefs)
- Probed `https://zambialii.org/legislation?alphabet=H&nature=act` (single-page listing, 11 unique act hrefs)
- Probed `https://zambialii.org/legislation?alphabet=I&nature=act` (single-page listing, 32 unique act hrefs)
- Filtered against existing act IDs (920 act records cross-referenced via both `act-zm-{yr}-{num}-` and slug-match across cap- and loz- naming conventions) and dropped tokens: amendment / appropriation / supplementary / validation / transitional / repeal / continuation / excess expenditure
- Result: 8 primary candidates after combined-alphabet filter (1 from G, 1 from H, 6 from I) — fills the MAX_BATCH_SIZE = 8 cap exactly

## Picks

| Alpha | Yr/Num | Title | Sections |
|-------|--------|-------|----------|
| G | 1912/16 | Gold Trade Act, 1912                                       | 23 |
| H | 1962/47 | Human Tissue Act, 1962                                     | 5  |
| I | 1967/45 | Inquiries Act, 1967                                        | 18 |
| I | 1953/21 | International Bank Loan (Approval) Act, 1953               | 3  |
| I | 1952/39 | International Bank Loan (Rhodesia Railways) Act, 1952      | 9  |
| I | 1965/53 | International Development Association Act, 1965            | 14 |
| I | 1965/52 | International Finance Corporation Act, 1965                | 21 |
| I | 1964/60 | Interpretation and General Provisions Act, 1964            | 53 |

All 8 are FIRST acts_in_force entries from alphabets G, H, and I (no prior primary-act coverage of these letters in the corpus).

## Integrity

- CHECK1a (batch unique IDs) — PASS 8/8
- CHECK1b (corpus presence on disk) — PASS 8/8
- CHECK2 (amended_by) — PASS 0 refs
- CHECK3 (repealed_by) — PASS 0 refs
- CHECK4 (source_hash sha256) — PASS 8/8 verified against raw/zambialii/act/(1912,1952,1953,1962,1964,1965,1967)/
- CHECK5 (required fields × records) — PASS 11×8 all present
- CHECK6 (cited_authorities) — PASS 0 refs

## Provenance

- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- Robots.txt re-verified at tick start (sha256 prefix `fce67b697ee4ef44`, unchanged from batches 0193-0256)
- Crawl-delay: 5s declared; honoured at 6s margin per request
- Parser: `0.6.0-act-zambialii-2026-04-26` (HTML akn-section primary; PDF fallback unused — all records parsed via akn-section HTML)

## Cost (this tick)

- 1 robots reverify + 3 alphabet listing fetches (G, H, I) + 8 record HTML fetches = 12 fetches on zambialii.org
- Pre-tick today fetches: 181; post-tick: 193 / 2000 (9.65% of daily budget)
- Tokens within budget

## Notes

- All 8 records parsed cleanly via HTML akn-section structure; no PDF fallback required
- Smallest record (International Bank Loan (Approval) Act 1953/21) has 3 sections — short statutory instrument; matches expected loan-approval one-shot statute pattern
- Largest record (Interpretation and General Provisions Act 1964/60) has 53 sections — foundational interpretation statute, parsed cleanly
- Continues acts_in_force pivot from batches 0253 (A-C), 0254 (C residual drain), 0255 (D), 0256 (E + F)
- Mid-tick: main `batch_0257.py` was killed by host bash 45s timeout after 5 of 8 records; remaining 3 (1965/53, 1965/52, 1964/60) completed via `batch_0257_finish.py` reusing the same `ingest_one()` function (identical parser, identical UA, identical crawl-delay)
- Reserved residuals carried from prior ticks: 2 alphabet=C deferred (Citizens Economic Empowerment 2006/9, Constitution of Zambia 1996/17 — large, dedicated batches) + 1 SI residual (1990/39 ZNPF >4.5MB OCR backlog at 15 items)
- Pre-tick recovery: working tree had stale staged deletions of batch 0256 records (left over from a partial mid-tick state in another process); resolved with `git reset HEAD` (no `--hard`, no destructive ops on disk records). Pull conflict on worker.log resolved by writing origin/main:worker.log content in-place (virtiofs unlink-failure workaround), then `git update-ref refs/heads/main` to fast-forward c2c4c27..64d3f82.

## Next-tick plan

- Continue alphabetic walk to alphabets J-K-L per running plan (J likely small; L typically dense)
- OCR backlog (15 items) deferred until tesseract is wired to host
- SQLite rebuild deferred to host: `corpus.sqlite` reflects 543 records (snapshot from earlier rebuild) vs 1494 JSON records on disk after this batch — periodic full rebuild expected from host

## Cumulative footprint

- Acts: 922 (pre-tick) + 8 = 930
- SIs: 593 (unchanged from batch 0252)
- Judgments: 25 (paused per robots Disallow on /akn/zm/judgment/)
