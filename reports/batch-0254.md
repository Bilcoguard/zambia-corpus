# Batch 0254 Report — Phase 4 bulk ingest (acts_in_force, alphabet=C drain)

**Date (UTC):** 2026-04-26
**Phase:** 4 (bulk)
**Sub-phase emphasis:** acts_in_force (priority_order item 1)
**Records committed:** 5 / 5 attempted (yield 100%)
**Wall-clock:** ~12 min (incl. one preempted-by-bash-timeout continuation via batch_0254_finish.py)

## Picks

| Idx | yr/num | Title | Sub-phase | Sections | Status |
|-----|--------|-------|-----------|----------|--------|
| 0 | 1926/20 | Clubs Registration Act, 1926 | acts_in_force | 14 | ok |
| 1 | 1963/64 | Central African Power Corporation Act, 1963 | acts_in_force | 4 | ok |
| 2 | 1964/7  | Central African Civil Air Transport Act, 1964 | acts_in_force | 24 | ok |
| 3 | 1968/18 | Calculation of Taxes Act, 1968 | acts_in_force | 3 | ok |
| 4 | 1981/3  | Central Committee Act, 1981 | acts_in_force | 5 | ok |

Drains 5 of the 7 alphabet=C residuals identified at the close of batch
0253. The two remaining residuals — Citizens Economic Empowerment Act
(2006/9) and Constitution of Zambia Act (1996/17) — are deferred to
dedicated batches because of expected size.

## Discovery

No fresh listing probes this tick. All five picks were already on the
batch-0253 alphabet=C residual list, so `/legislation?alphabet=C&nature=act`
was not re-fetched.

## Costs (this tick)

- Fetches: 7 = 1 robots + 5 record HTML + 1 record PDF (1981/3 fell back
  to PDF because HTML had < 2 sections). Each pacing under zambialii.org
  5s crawl-delay using the standard 6s margin.
- Today fetches: ~164 / 2000 (8.2% of daily budget)
- Tokens within budget

## Robots.txt

- sha256 prefix `fce67b697ee4ef44` (unchanged from batches 0193-0253)
- Crawl-delay: 5s (honoured at 6s margin)
- Disallow honoured: `/akn/zm/judgment/`, `/akn/zm/officialGazette/`,
  `/api/`, `/*/search/`

## Integrity (CHECK1a–CHECK6, all PASS)

- CHECK1a (batch unique IDs): 5/5
- CHECK1b (single-file presence per ID across records/): 5/5
- CHECK2 (amended_by resolves): 0 unresolved (all empty)
- CHECK3 (repealed_by resolves): 0 unresolved (all None)
- CHECK4 (source_hash sha256 verified against
  raw/zambialii/act/(1926,1963,1964,1968,1981)/): 5/5
- CHECK5 (10 required fields × 5 records): all present
- CHECK6 (cited_authorities resolves): 0 refs (trivially pass)

`corpus.sqlite` is intentionally not updated by per-batch ticks
(gitignored since commit 4a2544c — rebuild from raw files each session).

## Source-hash audit

| ID | sha256 (prefix) | URL |
|----|-----------------|-----|
| act-zm-1926-020-clubs-registration-act-1926 | 7c00b94fdcae4317… | /akn/zm/act/1926/20/eng@1996-12-31 |
| act-zm-1963-064-central-african-power-corporation-act-1963 | c1edc49291b9f258… | /akn/zm/act/1963/64/eng@1996-12-31 |
| act-zm-1964-007-central-african-civil-air-transport-act-1964 | e4b3d1a3891644e5… | /akn/zm/act/1964/7/eng@1996-12-31 |
| act-zm-1968-018-calculation-of-taxes-act-1968 | 580ab13352f3bf09… | /akn/zm/act/1968/18/eng@1996-12-31 |
| act-zm-1981-003-central-committee-act-1981 | e9b957e527040265… | /akn/zm/act/1981/3/eng@1981-03-06 |

## Cumulative records (post-batch 0254)

- Acts: 910 (+5 over 905); SIs: 593 (unchanged); Judgments: 25 (unchanged,
  paused per robots Disallow)

## Reserved residuals carry to next tick

- 2006/9 Citizens Economic Empowerment Act (alphabet=C, deferred — size)
- 1996/17 Constitution of Zambia Act (alphabet=C, deferred — size)
- 1990/39 ZNPF Statutory Contributions Regs (SI; OCR backlog, > 4.5MB
  cap; no change from prior batches)

## Next-tick plan

- (a) Continue acts_in_force discovery on alphabet=D (next prefix in the
  letter sweep against zambialii.org `/legislation?alphabet=D&nature=act`)
- (b) Either dedicated batch for 2006/9 Citizens Economic Empowerment, or
  defer until alphabet sweep (B–Z) is complete
- (c) Constitution of Zambia (1996/17) likely needs its own multi-batch
  treatment because of size — flag for human review
- (d) OCR retry on backlog (15 items) once tesseract is wired (deferred
  to host)

## MAX_BATCH_SIZE

8 cap honoured. 5 records committed (under 8 cap; conservative residual
drain leaves 3-record headroom for any picks that needed PDF fallback).

## Operational notes

- `batch_0254.py` was preempted by the per-call bash 45s timeout after
  ingesting picks 0–3. The 5th pick was completed by
  `scripts/batch_0254_finish.py`, which re-imports `ingest_one()` from the
  parent module so parser_version, hashing, and provenance writes stay
  byte-identical. No double-fetch occurred — the continuation only ran
  for the unfinished pick.
- 1981/3 Central Committee Act fell back to PDF (HTML returned only
  metadata with < 2 sections); raw_pdf saved alongside the HTML.
