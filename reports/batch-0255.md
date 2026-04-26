# Batch 0255 Report — Phase 4 bulk ingest (acts_in_force, alphabet=D)

**Date (UTC):** 2026-04-26
**Phase:** 4 (bulk)
**Sub-phase emphasis:** acts_in_force (priority_order item 1)
**Records committed:** 5 / 5 attempted (yield 100%)
**Wall-clock:** ~3 min (5 record fetches at 6s pacing + 2 listing fetches)

## Picks

| Idx | yr/num | Title | Sub-phase | Sections | Status |
|-----|--------|-------|-----------|----------|--------|
| 0 | 1938/12 | Debtors Act, 1938 | acts_in_force | 12 | ok |
| 1 | 1953/46 | Defamation Act, 1953 | acts_in_force | 19 | ok |
| 2 | 1960/24 | Development (United Kingdom Government) Loan Act, 1960 | acts_in_force | 6 | ok |
| 3 | 1960/48 | District Messengers Act, 1960 | acts_in_force | 10 | ok |
| 4 | 1965/30 | Diplomatic Immunities and Privileges Act, 1965 | acts_in_force | 19 | ok |

This is the next-tick plan from batch 0254 close-out: pivot acts_in_force
discovery to alphabet=D after fully draining the small alphabet=C primary
residuals in batches 0253/0254. All five picks parsed cleanly via the
`akn-section` HTML extractor — no PDF fallback was required for this
batch. Continues the alphabetic walk down the acts_in_force backlog.

## Discovery

Probed `https://zambialii.org/legislation?alphabet=D&nature=act` once —
single-page listing, 16 unique `/akn/zm/act/{yr}/{num}` hrefs returned.
Cross-referenced against 910 existing act IDs and dropped amendment /
appropriation / supplementary / validation / transitional / repeal-style
tokens, leaving 5 primary candidates — every one of which is ingested
here. Raw listing cached to
`raw/zambialii/_alphabets/legislation-alphabet-D-<ts>.html`.

Discovery deltas to be aware of: alphabet=D listing surfaces no further
non-amendment primaries. Next acts_in_force expansion should advance to
alphabets E–K per batch 0254 close-out plan; alphabet=C still has the two
deliberately-deferred large records (Citizens Economic Empowerment 2006/9;
Constitution of Zambia 1996/17) plus the SI OCR-backlog item 1990/39
(ZNPF Statutory Contributions Regs > 4.5MB cap).

## Costs (this tick)

- Fetches: 7 = 1 robots + 1 alphabet=D listing + 5 record HTML. No PDF
  fallback needed; all sections came from the akn-section HTML
  extractor (each act had ≥ 6 sections).
- Today fetches (cumulative across the day): ~171 / 2000 (8.55% of daily
  budget).
- Tokens within budget.

All zambialii.org fetches paced under the robots-declared 5s crawl-delay
using the standard 6s margin.

## Robots.txt

- sha256 prefix `fce67b697ee4ef44` (unchanged from batches 0193-0254)
- Crawl-delay: 5s (honoured at 6s margin)
- Disallow honoured: `/akn/zm/judgment/`, `/akn/zm/officialGazette/`,
  `/api/`, `/*/search/`

## Integrity (CHECK1a–CHECK6, all PASS)

- CHECK1a (batch unique IDs): 5/5 unique
- CHECK1b (single-file presence per ID across records/): 5/5
- CHECK2 (amended_by resolves): 0 unresolved (all empty)
- CHECK3 (repealed_by resolves): 0 unresolved (all None)
- CHECK4 (source_hash sha256 verified against
  `raw/zambialii/act/(1938,1953,1960,1965)/`): 5/5
- CHECK5 (10 required fields × 5 records): all present
- CHECK6 (cited_authorities resolves): 0 refs (trivially pass)

`corpus.sqlite` is intentionally not updated by per-batch ticks
(gitignored since commit 4a2544c — rebuild from raw files each session).

## Source-hash audit

| ID | sha256 (prefix) | URL |
|----|-----------------|-----|
| act-zm-1938-012-debtors-act-1938 | 78e7a0297f30db7b… | /akn/zm/act/1938/12/eng@1996-12-31 |
| act-zm-1953-046-defamation-act-1953 | 21bc5e1f6a8c12fa… | /akn/zm/act/1953/46/eng@1996-12-31 |
| act-zm-1960-024-development-united-kingdom-government-loan-act-1960 | ed8c97c7da2a73b3… | /akn/zm/act/1960/24/eng@1996-12-31 |
| act-zm-1960-048-district-messengers-act-1960 | 39184e919c8aed42… | /akn/zm/act/1960/48/eng@1996-12-31 |
| act-zm-1965-030-diplomatic-immunities-and-privileges-act-1965 | ee47b0d3d7a2bff6… | /akn/zm/act/1965/30/eng@1996-12-31 |

## Cumulative records (post-batch 0255)

- Acts: 915 (+5 over 910); SIs: 593 (unchanged); Judgments: 25
  (unchanged, paused per robots Disallow on `/akn/zm/judgment/`)

## Reserved residuals carry to next tick

- 2006/9 Citizens Economic Empowerment Act (alphabet=C, deferred — size)
- 1996/17 Constitution of Zambia Act (alphabet=C, deferred — size)
- 1990/39 ZNPF Statutory Contributions Regs (SI; OCR backlog, > 4.5MB
  cap; no change from prior batches)

## Next-tick plan

- Probe alphabet=E acts listing under `/legislation?alphabet=E&nature=act`
  and continue the walk through alphabets F–K per the batch 0254
  close-out plan.
- Re-verify robots.txt at start of next tick.
- B2 raw sync of accumulated batches 0192-0255 still awaiting host
  (rclone unavailable in sandbox).
- OCR backlog at 15 items unchanged (deferred to host).

## Yield streak

100% record yield extends across batches 0246/0247/0248/0249/0250/0251/
0252/0253/0254/0255 — 9 consecutive batches at 100%.
