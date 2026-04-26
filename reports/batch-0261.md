# Batch 0261 Report

- **Date (UTC):** 2026-04-26
- **Phase:** 4 (bulk)
- **Sub-phase:** acts_in_force
- **Source:** zambialii.org (alphabetic walk; P residuals + Q + R)
- **Records added:** 8
- **Cap:** MAX_BATCH_SIZE = 8 (filled exactly)

## Picks

| Alpha | Year/Num | Title | Sections | ID |
|---|---|---|---|---|
| P | 1981/2 | Presidential Emoluments Act, 1981 | 3 | act-zm-1981-002-presidential-emoluments-act-1981 |
| P | 1947/31 | Printed Publications Act, 1947 | 6 | act-zm-1947-031-printed-publications-act-1947 |
| P | 1992/21 | Privatisation Act, 1992 | 51 | act-zm-1992-021-privatisation-act-1992 |
| P | 1961/37 | Professional Boxing and Wrestling Control Act, 1961 | 16 | act-zm-1961-037-professional-boxing-and-wrestling-control-act-1961 |
| P | 1960/6 | Protected Places and Areas Act, 1960 | 13 | act-zm-1960-006-protected-places-and-areas-act-1960 |
| P | 1965/8 | Provincial and District Boundaries Act, 1965 | 2 | act-zm-1965-008-provincial-and-district-boundaries-act-1965 |
| Q | 1995/37 | Quantity Surveyors Act, 1995 | 30 | act-zm-1995-037-quantity-surveyors-act-1995 |
| R | 1994/25 | Radiocommunications Act, 1994 | 21 | act-zm-1994-025-radiocommunications-act-1994 |

## Discovery

- alphabet=P: 1 listing fetch (single-page, 48 unique act hrefs). 12 candidates remained after filtering against existing 952 act IDs and dropping amendment/repeal/transitional/dissolution/rectification tokens — 9 primary picks identified; first 6 selected.
- alphabet=Q: 1 listing fetch (single-page, 1 unique act href). 1 primary candidate (1995/37 Quantity Surveyors Act) — selected.
- alphabet=R: 1 listing fetch (single-page, 21 unique act hrefs). 3 primary candidates after the same filter — first 1 (1994/25 Radiocommunications Act) selected to fill the cap.
- Total candidates filling cap: 8. Deferred to next tick: 3 P primary residuals (Prohibition (Chemical Weapons) Act 2007/2, Protection of Names, Uniforms and Badges Act 1957/38, Public Audit Act 1980/8) + 2 R residuals (Revenue Appeals Tribunal Act 1998/11, Rural Councils (Beer Surtax) Fund Act 1968/45).

## Provenance

- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- Crawl-delay: 6s margin over robots.txt-declared 5s
- Robots.txt re-verified at tick start (sha256 `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` unchanged from batches 0193-0260)
- Parser version: `0.6.0-act-zambialii-2026-04-26`
- All 8 records parsed cleanly via akn-section HTML — no PDF fallback required
- Smallest: 1965/8 Provincial and District Boundaries Act, 2 sections
- Largest: 1992/21 Privatisation Act, 51 sections

## Integrity

- CHECK1a (batch unique IDs): PASS — 8/8
- CHECK1b (corpus presence on disk): PASS — 8/8
- CHECK2 (amended_by refs resolve): PASS — 0 refs
- CHECK3 (repealed_by refs resolve): PASS — 0 refs
- CHECK4 (source_hash matches on-disk raw HTML): PASS — 8/8 sha256 verified against raw/zambialii/act/(1947,1960,1961,1965,1981,1992,1994,1995)/
- CHECK5 (required 16 fields present): PASS — 16x8
- CHECK6 (cited_authorities refs resolve): PASS — 0 refs

## Costs

- Pre-tick fetches today: 229
- This tick: 1 robots + 3 alphabet listings (P, Q, R) + 8 record HTML = 12 fetches
- Post-tick: 241/2000 (12.05% of daily budget)
- All fetches on zambialii.org under robots-declared 5s crawl-delay using 6s margin

## Cumulative

- Acts: 960 (+8 over 952)
- SIs: 593 (unchanged)
- Judgments: 25 (paused per robots Disallow on /akn/zm/judgment/)

## Residuals carried to next tick

- 3 P primary residuals (Prohibition (Chemical Weapons) Act 2007/2 + Protection of Names, Uniforms and Badges Act 1957/38 + Public Audit Act 1980/8)
- 2 R residuals (Revenue Appeals Tribunal Act 1998/11 + Rural Councils (Beer Surtax) Fund Act 1968/45)
- Prior reserved residuals still pending: 2 alphabet=C (Citizens Economic Empowerment 2006/9 + Constitution of Zambia 1996/17 — large, dedicated batches), 1 SI residual (1990/39 ZNPF >4.5MB OCR backlog at 15 items)

## Next-tick plan

- (a) Sweep P + R residuals first (5 candidates)
- (b) Probe alphabet=S nature=act and continue alphabetic walk
- (c) OCR retry on 15-item backlog once tesseract is wired (deferred to host)
- Re-verify robots.txt at start of next tick.

## B2 sync

- WARN: rclone unavailable in sandbox. Raw files (8 HTML + 3 alphabet listings + 1 robots) cached locally to `raw/zambialii/...`; awaits host-driven `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`.

## Infrastructure notes

- Mid-tick: ingestion split across two `batch_0261.py` sub-runs (slices 0:4 + 4:8) to fit within host 45s bash timeout; both sub-runs reuse `ingest_one()` (identical parser, UA, crawl-delay).
- Lock-recovery applied mid-tick: stale `.git/index.lock` detected (likely from prior sqlite3 attempt) — moved to `_stale_locks/index.lock.b0261-20260426T101149Z`. Persistent virtiofs unlink-failure restriction unchanged from batches 0192-0260 (rename succeeds, unlink fails).
- corpus.sqlite NOT updated this batch (per established workflow — periodic full rebuild expected from host; SQLite snapshot drift remains at 543 records vs 1526 JSON on disk).
- corpus.sqlite-journal stale 29 KB journal observed at tick start (truncated to 0 bytes — virtiofs unlink restricted, truncate succeeds; pre-existing FTS5 vtable issue noted as gap, non-blocking for record integrity).
