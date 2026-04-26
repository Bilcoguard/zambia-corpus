# Batch 0250 Report — Phase 4 Bulk Ingest

**Date:** 2026-04-26
**Phase:** phase_4_bulk
**Batch:** 0250
**Yield:** 8/8 (100%)
**Records:** +8 SIs (1 reserved residual 1985/14 + 1 alphabet=U novel + 6 alphabet=Z novels)

## Records ingested

| ID | Year/Num | Title | Parent Act | Sub-phase | Pages | Chars |
|----|----------|-------|------------|-----------|-------|-------|
| si-zm-1985-014-equity-levy-exemption-order-1985 | 1985/14 | Equity Levy (Exemption) Order, 1985 | Equity Levy Act | sis_governance | 1 | 808 |
| si-zm-1994-041-university-of-zambia-staff-tribunal-rules-1994 | 1994/41 | University of Zambia (Staff Tribunal) Rules, 1994 | University of Zambia Act | sis_governance | 4 | 6,737 |
| si-zm-1995-002-zambezi-river-authority-terms-and-conditions-of-service-by-laws-1995 | 1995/2 | Zambezi River Authority (Terms and Conditions of Service) By-laws, 1995 | Zambezi River Authority Act | sis_industry | 26 | 48,832 |
| si-zm-2015-086-zambia-institute-of-advanced-legal-education-accreditation-of-legal-education-institutions-regulations-2015 | 2015/86 | Zambia Institute of Advanced Legal Education (Accreditation of Legal Education Institutions) Regulations, 2015 | Zambia Institute of Advanced Legal Education Act | sis_governance | 22 | 31,619 |
| si-zm-2003-049-zambia-national-broadcasting-corporation-amendment-act-commencement-order-2003 | 2003/49 | Zambia National Broadcasting Corporation (Amendment) Act (Commencement) Order, 2003 | Zambia National Broadcasting Corporation Act | sis_governance | 2 | 984 |
| si-zm-2013-018-zambia-national-service-combat-uniform-regulations-2013 | 2013/18 | Zambia National Service (Combat Uniform) Regulations, 2013 | Zambia National Service Act | sis_governance | 2 | 2,016 |
| si-zm-2016-041-zambia-wildlife-game-animals-order-2016 | 2016/41 | Zambia Wildlife (Game Animals) Order, 2016 | Zambia Wildlife Act | sis_governance | 2 | 1,833 |
| si-zm-2016-042-zambia-wildlife-protected-animals-order-2016 | 2016/42 | Zambia Wildlife (Protected Animals) Order, 2016 | Zambia Wildlife Act | sis_governance | 2 | 1,671 |

**Total:** 61 pages / 94,500 chars across 8 records.

## Sub-phase footprint

- **sis_governance +7:** Equity Levy Act 1985/14 + UNZA Act 1994/41 + ZIALE Act 2015/86 + ZNBC Act 2003/49 + Zambia National Service Act 2013/18 + Zambia Wildlife Act 2016/41 + 2016/42. THREE FIRST parent-Act linkages this tick: University of Zambia Act + Zambia Institute of Advanced Legal Education Act + Zambia National Service Act. Equity Levy 1985/14 closes out the 1985 alphabet=E residuals from batch 0247.
- **sis_industry +1:** Zambezi River Authority (Terms and Conditions of Service) By-laws 1995/2 — FIRST sis_industry parent-Act linkage to Zambezi River Authority Act.

## Discovery this tick

Fresh probes of 4 unprobed alphabets (J/K/U/Z): J=1total/0novel, K=0total/0novel, U=20/1novel, Z=23/17novel. **Net 18 novel candidates discovered**, 7 used in this batch + 10 carried as reserved residuals to next tick.

## Costs

- Today's fetches: 111 (pre-tick 107 + 4 discovery this tick) + 16 records this tick = 127 / 2000 (6.4%)
- This batch: 1 robots + 4 alphabet listings + 16 record fetches (8 HTML + 8 PDF) = 21 fetches
- Tokens: within budget

## Reserved residuals (carry to next tick)

10 alphabet=Z novels: 2016/40 + 2016/43 (Wildlife Police Uniforms / Export Prohibition) + 1980/49 + 1990/39 + 1996/44 (ZNPF Statutory Contributions across decades) + 1981/47 (ZNS Obligatory Service Exemption) + 1982/49 (Zambia Airways Dissolution) + 1991/35 (Tender Commencement) + 1998/43 (Tender Amendment) + 2006/10 (Zambia Police Fees). Plus 1 alphabet=Z residual: 1994/49 (ZRA Commencement and Disengagement).

## Integrity

CHECK1a (batch unique 8/8) + CHECK1b (corpus presence 8/8) + CHECK2/3 (0 amended_by/repealed_by refs) + CHECK4 (sha256 verified 8/8 against raw/zambialii/si/(1985,1994,1995,2003,2013,2015,2016)/) + CHECK5 (10 fields x 8 records all present) + CHECK6 (0 cited_authorities refs) — **ALL PASS**.

## Robots compliance

Re-verified at tick start: sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0249. Crawl-delay 5s honoured at 6s margin. Disallow on /akn/zm/judgment/ + /akn/zm/officialGazette/ enforced.

## Cumulative SI count

- Batch 0249: 575
- Batch 0250: 583 (+8)
