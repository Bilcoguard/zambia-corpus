# Batch 0259 Report

- **Date (UTC):** 2026-04-26
- **Phase:** 4 (bulk)
- **Sub-phase:** acts_in_force
- **Source:** zambialii.org (alphabetic walk; L residual + M + N)
- **Records added:** 8
- **Cap:** MAX_BATCH_SIZE = 8 (filled exactly)

## Picks

| Alpha | Year/Num | Title | Sections | ID |
|---|---|---|---|---|
| L | 1962/22 | Local Authorities Superannuation Fund Act, 1962 | 48 | act-zm-1962-022-local-authorities-superannuation-fund-act-1962 |
| M | 1921/20 | Maintenance Orders (Enforcement) Act, 1921 | 11 | act-zm-1921-020-maintenance-orders-enforcement-act-1921 |
| M | 1929/24 | Mufulira-Mokambo Railway Act, 1929 | 8 | act-zm-1929-024-mufulira-mokambo-railway-act-1929 |
| M | 1957/17 | Merchandise Marks Act, 1957 | 24 | act-zm-1957-017-merchandise-marks-act-1957 |
| M | 1970/29 | Mines Acquisition (Special Provisions) (No. 2) Act, 1970 | 5 | act-zm-1970-029-mines-acquisition-special-provisions-no-2-act-1970 |
| N | 1965/23 | National Flag and Armorial Ensigns, 1965 | 6 | act-zm-1965-023-national-flag-and-armorial-ensigns-act-1965 |
| N | 1965/75 | Non-Designated Expatriate Officers (Retiring Benefits) Act, 1965 | 14 | act-zm-1965-075-non-designated-expatriate-officers-retiring-benefits-act-1965 |
| N | 1966/10 | National Museums Act, 1966 | 12 | act-zm-1966-010-national-museums-act-1966 |

## Discovery

- alphabet=M: 1 listing fetch (single-page, 34 unique act hrefs). 4 candidates remained after filtering against existing 936 act IDs and dropping amendment/repeal/transitional/etc. tokens.
- alphabet=N: 1 listing fetch (single-page, 45 unique act hrefs). 5 candidates remained after the same filter.
- L residual: 1962/22 carried forward from batch 0258.
- Total candidates: 10. Capped at 8. Deferred to next tick: 2 N residuals (1986/7 NYDC + 1995/35 NRSC).

## Provenance

- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- Crawl-delay: 6s margin over robots.txt-declared 5s
- Robots.txt re-verified at tick start (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0258)
- Parser version: `0.6.0-act-zambialii-2026-04-26`
- All 8 records parsed cleanly via akn-section HTML — no PDF fallback required
- Smallest: 1970/29 Mines Acquisition (No. 2) Act, 5 sections
- Largest: 1962/22 Local Authorities Superannuation Fund Act, 48 sections

## Integrity

- CHECK1a (batch unique IDs): PASS — 8/8
- CHECK1b (corpus presence on disk): PASS — 8/8
- CHECK2 (amended_by refs resolve): PASS — 0 refs
- CHECK3 (repealed_by refs resolve): PASS — 0 refs
- CHECK4 (source_hash matches on-disk raw HTML): PASS — 8/8 sha256 verified against raw/zambialii/act/(1921,1929,1957,1962,1965,1966,1970)/
- CHECK5 (required 16 fields present): PASS — 16x8
- CHECK6 (cited_authorities refs resolve): PASS — 0 refs

## Costs

- Pre-tick fetches today: 207
- This tick: 1 robots + 2 alphabet listings (M, N) + 8 record HTML = 11 fetches
- Post-tick: 218/2000 (10.9% of daily budget)
- All fetches on zambialii.org under robots-declared 5s crawl-delay using 6s margin

## Cumulative

- Acts: 944 (+8 over 936)
- SIs: 593 (unchanged)
- Judgments: 25 (paused per robots Disallow on /akn/zm/judgment/)

## Next-tick plan

1. Sweep remaining N residuals: 1986/7 NYDC + 1995/35 NRSC
2. Probe alphabet=O nature=act (and continue alphabetic walk through P-Q)
3. Re-verify robots.txt at start of tick
4. Reserved residuals still pending: 2 alphabet=C deferred (Citizens Economic Empowerment 2006/9 + Constitution of Zambia 1996/17 — large, dedicated batches), 1 SI residual (1990/39 ZNPF >4.5MB OCR backlog at 15 items, awaiting tesseract on host)

## Infrastructure follow-up (non-blocking)

- B2 raw sync deferred to host (rclone unavailable in sandbox); batch-0259 raw files (8 HTML + 2 alphabet listings + 1 robots) plus accumulated batches 0192-0258 raws still pending.
- Persistent virtiofs unlink-failure warnings remain non-fatal (workaround stable across batches 0192-0259).
- SQLite snapshot drift: corpus.sqlite has 543 records vs ~1510 JSON on disk after this batch — periodic full rebuild expected from host.
