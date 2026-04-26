# Batch 0260 Report

- **Date (UTC):** 2026-04-26
- **Phase:** 4 (bulk)
- **Sub-phase:** acts_in_force
- **Source:** zambialii.org (alphabetic walk; N residuals + O + P)
- **Records added:** 8
- **Cap:** MAX_BATCH_SIZE = 8 (filled exactly)

## Picks

| Alpha | Year/Num | Title | Sections | ID |
|---|---|---|---|---|
| N | 1995/35 | National Road Safety Council Act, 1995 | 21 | act-zm-1995-035-national-road-safety-council-act-1995 |
| N | 1986/7 | National Youth Development Council Act, 1986 | 30 | act-zm-1986-007-national-youth-development-council-act-1986 |
| O | 1963/33 | Occupiers' Liability Act, 1963 | 7 | act-zm-1963-033-occupiers-liability-act-1963 |
| O | 1966/11 | Organisations (Control of Assistance) Act, 1966 | 11 | act-zm-1966-011-organisations-control-of-assistance-act-1966 |
| P | 1963/72 | Personal Levy Act, 1963 | 25 | act-zm-1963-072-personal-levy-act-1963 |
| P | 1967/14 | Plant Variety and Seeds Act, 1967 | 85 | act-zm-1967-014-plant-variety-and-seeds-act-1967 |
| P | 1959/33 | Pools Act, 1959 | 7 | act-zm-1959-033-pools-act-1959 |
| P | 1995/9 | Preferential Claims in Bankruptcy Act, 1995 | 5 | act-zm-1995-009-preferential-claims-in-bankruptcy-act-1995 |

## Discovery

- alphabet=O: 1 listing fetch (single-page, 4 unique act hrefs). 2 candidates remained after filtering against existing 944 act IDs and dropping amendment/repeal/transitional/dissolution tokens (1990/4 Official Oaths Act + 2025/16 Occupational Health and Safety Act already in corpus).
- alphabet=P: 1 listing fetch (single-page, 48 unique act hrefs). 12+ primary candidates after the same filter; first 4 selected to fill the cap.
- N residuals: 1995/35 NRSC + 1986/7 NYDC carried forward from batch 0259.
- Total candidates filling cap: 8. Deferred to next tick: 8+ P residuals (Plant Pests and Diseases Act 1958/11, Plumage Birds Protection Act 1915/23, Probates (Resealing) Act 1936/22, Probation of Offenders Act 1953/15, Professional Boxing and Wrestling Control Act 1961/37, Prohibition of Anti-Personnel Mines Act 2003/16, Prohibition (Chemical Weapons) Act 2007/2, Protected Places and Areas Act 1960/6, Protection of Names, Uniforms and Badges Act 1957/38, Provincial and District Boundaries Act 1965/8, Public Audit Act 1980/8, etc.).

## Provenance

- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- Crawl-delay: 6s margin over robots.txt-declared 5s
- Robots.txt re-verified at tick start (sha256 `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` unchanged from batches 0193-0259)
- Parser version: `0.6.0-act-zambialii-2026-04-26`
- All 8 records parsed cleanly via akn-section HTML — no PDF fallback required
- Smallest: 1995/9 Preferential Claims in Bankruptcy Act, 5 sections
- Largest: 1967/14 Plant Variety and Seeds Act, 85 sections

## Integrity

- CHECK1a (batch unique IDs): PASS — 8/8
- CHECK1b (corpus presence on disk): PASS — 8/8
- CHECK2 (amended_by refs resolve): PASS — 0 refs
- CHECK3 (repealed_by refs resolve): PASS — 0 refs
- CHECK4 (source_hash matches on-disk raw HTML): PASS — 8/8 sha256 verified against raw/zambialii/act/(1959,1963,1966,1967,1986,1995)/
- CHECK5 (required 16 fields present): PASS — 16x8
- CHECK6 (cited_authorities refs resolve): PASS — 0 refs

## Costs

- Pre-tick fetches today: 218
- This tick: 1 robots + 2 alphabet listings (O, P) + 8 record HTML = 11 fetches
- Post-tick: 229/2000 (11.45% of daily budget)
- All fetches on zambialii.org under robots-declared 5s crawl-delay using 6s margin

## Cumulative

- Acts: 952 (+8 over 944)
- SIs: 593 (unchanged)
- Judgments: 25 (paused per robots Disallow on /akn/zm/judgment/)

## Residuals carried to next tick

- 8+ P residuals (deferred for cap; full alphabet=P walk continues next tick)
- Prior reserved residuals still pending: 2 alphabet=C (Citizens Economic Empowerment 2006/9 + Constitution of Zambia 1996/17 — large, dedicated batches), 1 SI residual (1990/39 ZNPF >4.5MB OCR backlog at 15 items)

## Next-tick plan

- (a) Continue P sweep (Plant Pests and Diseases / Probation / Public Audit / Public Finance / Public Procurement / Public Service Pensions / Privatisation / etc. — first 8 clean candidates)
- (b) Probe alphabet=Q–R nature=act and continue alphabetic walk
- (c) OCR retry on 15-item backlog once tesseract is wired (deferred to host)
- Re-verify robots.txt at start of next tick.

## B2 sync

- WARN: rclone unavailable in sandbox. Raw files (8 HTML + 2 alphabet listings + 1 robots) cached locally to `raw/zambialii/...`; awaits host-driven `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`.
