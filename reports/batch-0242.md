# Phase 4 Batch 0242

**Date:** 2026-04-25 (UTC)
**Phase:** phase_4_bulk
**Sub-phase footprint:** FIRST sis_transport cluster (5 records) + FIRST sis_agriculture cluster (3 records)

## Summary

- **Records committed:** 8 statutory instruments
- **Cumulative SI records:** 522 (+8 over batch 0241's 514)
- **Yield:** 8/9 attempted (89%)
- **First-instance sub-phases:** sis_transport, sis_agriculture
- **Discovery cost:** 1 robots reverify + 4 listing probes (K, R, O, Q + year=2025) = 5 fetches
- **Per-record cost:** 16 fetches (8 HTML + 8 PDF for ok records) + 2 (1 HTML + 1 PDF for fail preserved)
- **Tick fetches:** ~23 (1 robots + 4 probes + 16 ok + 2 fail-preserved)

## Records (8)

| # | yr/num | Title | Sub-phase | Pages | Chars |
|---|--------|-------|-----------|-------|-------|
| 1 | 2018/007 | Railways (Transportation of Heavy Goods) Regulations, 2018 | sis_transport | 4 | 4,316 |
| 2 | 2020/050 | Road Traffic (Driving Licence) Regulations, 2020 | sis_transport | 26 | 42,935 |
| 3 | 2021/112 | Road Traffic (Fees) Regulations, 2021 | sis_transport | 4 | 4,698 |
| 4 | 2014/016 | Animal Health (Livestock Cleansing) Order, 2014 | sis_agriculture | 2 | 1,918 |
| 5 | 2014/024 | Animal Health (Control and Prevention of Animal Disease) Order, 2014 | sis_agriculture | 4 | 2,852 |
| 6 | 2014/059 | Agricultural Credits (Appointment of Authorised Agency) Order, 2014 | sis_agriculture | 2 | 852 |
| 7 | 2001/032 | Air Services (Permit Fees) Regulations, 2001 | sis_transport | 2 | 2,705 |
| 8 | 1985/024 | Air Passenger Service Charge (Appointment of Collection Agents) (No. 2) Order, 1985 | sis_transport | 1 | 1,049 |

## Failures (1)

- **2020/007** Road Traffic (Speed Limits) Regulations, 2019 — `pdf_parse_empty` (scanned image, raw HTML+PDF preserved at `raw/zambialii/si/2020/` for OCR retry; added to OCR backlog)

## Discovery probes

| Alphabet/Year | URL | Modern SIs | Novel | Outcome |
|---|---|---|---|---|
| K | `?alphabet=K` | 0 | 0 | empty |
| R | `?alphabet=R` | 4 | 4 | drained 4/4 → 4 ok records |
| O | `?alphabet=O` | 0 | 0 | empty |
| Q | `?alphabet=Q` | 0 | 0 | empty |
| year=2025 | `?year=2025` | 7 | 7 | drained 4/7 (3 picks + sub) — 3 unprocessed novel remain in cache (1985/45 Air Services Aerial App; 1992/9 Air Passenger Charging; 2001/32 was picked) |

## Integrity (CHECK1a/1b/2/3/4/5/6 — ALL PASS)

- CHECK1a unique ids: 8/8
- CHECK1b on-disk presence: 8/8
- CHECK2 amended_by refs: 0
- CHECK3 repealed_by refs: 0
- CHECK4 source_hash sha256 verified: 8/8 (against `raw/zambialii/si/(1985,2001,2014,2018,2020,2021)/`)
- CHECK5 required fields 10×8: 0 missing
- CHECK6 cited_authorities refs: 0

## Provenance

- All sources fetched from zambialii.org under robots.txt content-signal `search=yes`
- Crawl-delay 5s honoured at 6.0s margin (CRAWL=6.0)
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- Robots.txt sha256 prefix `fce67b697ee4ef44` (unchanged from batches 0193-0241)
- Disallow on `/akn/zm/judgment/` + `/akn/zm/officialGazette/` enforced (judgments paused)

## Infrastructure follow-up

- Raw files (~17 = 8 HTML + 8 PDF + 1 robots + 4 probe HTMLs + 2 fail-preserved) await host-driven B2 sync (rclone unavailable in sandbox)
- OCR backlog now 11 items (+1 this tick: 2020/007)
- 488+ pre-existing untracked records files unchanged this tick

## Next-tick options

- (a) Drain 3 unprocessed novel from year=2025 probe (1985/45 + 1992/9 + others)
- (b) Probe further year listings (1980-2010 backfill, or 2024/2025 fresh)
- (c) Rotate to acts_in_force priority_order item 1 (Acts-listing endpoint discovery)
- (d) OCR retry on backlog (now 11 items) once tesseract is wired
