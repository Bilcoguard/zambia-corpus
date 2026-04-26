# Batch 0253 Report — Phase 4 bulk ingest (PIVOT to acts_in_force)

**Date (UTC):** 2026-04-26
**Phase:** 4 (bulk)
**Sub-phase emphasis:** acts_in_force (priority_order item 1)
**Records committed:** 6 / 6 attempted (yield 100%)
**Wall-clock:** ~10 min (incl. lock-recovery + discovery)

## Picks

| Idx | yr/num | Title | Sub-phase | Sections | Status |
|-----|--------|-------|-----------|----------|--------|
| 0 | 1931/3 | Boy Scouts and Girl Guides Associations Act, 1931 | acts_in_force | 6 | ok |
| 1 | 1965/51 | Bretton Woods Agreement Act, 1965 | acts_in_force | 40 | ok |
| 2 | 1929/17 | Control of Dogs Act, 1929 | acts_in_force | 4 | ok |
| 3 | 1940/12 | Civil Courts (Attachment of Debts) Act, 1940 | acts_in_force | 12 | ok |
| 4 | 1954/12 | Control of Goods Act, 1954 | acts_in_force | (parsed) | ok |
| 5 | 1994/39 | Common Leasehold Schemes Act, 1994 | acts_in_force | (parsed) | ok |

## Pivot rationale

After 252 SI-focused batches, this batch executes the previously
documented pivot to acts_in_force (priority_order item 1 in approvals.yaml).
Discovery: zambialii.org `/legislation?alphabet={A,B,C}&nature=act` listings
cross-referenced against existing 768-id corpus by (year/num) tuple. Filter
applied: skip appropriation/amendment/supplementary/validation/transitional
boilerplate. Alphabet=A yielded 0 primary picks (all 32 were Appropriation
Acts already filtered); B/C yielded 13 candidates, of which 6 were selected
for this batch (deferring Constitution of Zambia Act 1996/17 and Citizens
Economic Empowerment Act 2006/9 to dedicated batches given expected size).

## Discovery

- alphabet=A nature=act (page 1 + 2): 74 acts listed, 34 missing, all 32 primary candidates were Appropriation Acts (filtered out)
- alphabet=B nature=act (page 1 + 2): 16 acts listed, 2 primary missing
- alphabet=C nature=act (page 1 + 2): 55 acts listed, 11 primary missing

## Costs (this tick)

- Fetches: 14 = 1 robots + 6 record HTML + 1 listing probe (initial /legislation?nature=act) + 4 listing probes (alphabet=A,B,C with B/C page=2) + 2 unsuccessful page=3 probes (alpha=A — 404 expected) — all under zambialii.org 5s crawl-delay using 6s margin
- Today fetches: ~166 / 2000 (8.3% of daily budget)
- Tokens within budget

## Robots.txt

- sha256 prefix `fce67b697ee4ef44` (unchanged from batches 0193-0252)
- Crawl-delay: 5s (honoured at 6s margin)
- Disallow honoured: `/akn/zm/judgment/`, `/akn/zm/officialGazette/`, `/api/`, `/*/search/`

## Integrity (CHECK1a–CHECK6, all PASS)

- CHECK1a (batch unique IDs): 6/6
- CHECK1b (corpus presence): 0 dups
- CHECK2 (amended_by resolves): 0 unresolved
- CHECK3 (repealed_by resolves): 0 unresolved
- CHECK4 (source_hash sha256 verified against raw/zambialii/act/(1929,1931,1940,1954,1965,1994)/): 6/6
- CHECK5 (10 required fields x 6 records): all present
- CHECK6 (cited_authorities resolves): 0 refs (trivially pass)

## Cumulative records (post-batch 0253)

- Acts: 905 (+6 over 899); SIs: 593 (unchanged); Judgments: 25 (unchanged, paused per robots Disallow)

## Reserved residuals carry to next tick

- 1990/39 ZNPF Statutory Contributions Regs (SI; OCR backlog, >4.5MB cap; no change from batch 0252)
- alphabet=B: Boy Scouts Act DONE this batch; remaining alphabet=B residual: 0 primary
- alphabet=C: 7 primary acts not yet ingested (Calculation of Taxes 1968/18, Central African Civil Air Transport 1964/7, Central African Power Corp 1963/64, Central Committee 1981/3, Citizens Economic Empowerment 2006/9, Clubs Registration 1926/20, Constitution of Zambia 1996/17)

## Next-tick plan

- (a) Continue acts_in_force discovery on remaining alphabets D-Z (excluding the 26 SI alphabets already probed, since act listings are independent paths from SI listings — all 26 letter prefixes need re-probing under nature=act filter)
- (b) Drain the 7 alphabet=C primary residuals identified above (Citizens Economic Empowerment Act and Constitution of Zambia Act flagged as larger — may need split batches)
- (c) OCR retry on backlog (15 items) once tesseract is wired (deferred to host)

## MAX_BATCH_SIZE

8 cap honoured. 6 records committed (under 8 cap; conservative pivot batch, leaving 2-record headroom for any picks that needed PDF fallback).
