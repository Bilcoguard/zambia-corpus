# Phase 4 Batch 0243

**Date:** 2026-04-25 (UTC start; 2026-04-26 UTC may apply by close-out per env)
**Phase:** phase_4_bulk
**Sub-phase footprint:** FIRST `sis_corporate` cluster (4 records — priority_order item 2 advanced) + `sis_governance` extension (2 records: Citizenship Act parent + Amendment) + `sis_transport` extension (2 records: Civil Aviation Act parent-Act linkage)

## Summary

- **Records committed:** 8 statutory instruments
- **Cumulative SI records:** 530 (+8 over batch 0242's 522)
- **Yield:** 8/8 attempted (100%)
- **First-instance sub-phases:** `sis_corporate` (priority_order item 2 advanced)
- **Discovery cost:** 1 robots reverify + 9 listing probes (G/U/X/Y/Z + year=2024 p1/p2/p3 + year=2023 p1) = 10 fetches
- **Per-record cost:** 16 fetches (8 HTML + 8 PDF for ok records)
- **Tick fetches:** ~26

## Records (8)

| # | yr/num | Title | Sub-phase | Pages | Chars |
|---|--------|-------|-----------|-------|-------|
| 1 | 2019/014 | Companies (General) Regulations, 2019 | sis_corporate | 7 | 9,412 |
| 2 | 2019/015 | Companies (Fees) Regulations, 2019 | sis_corporate | 4 | 6,163 |
| 3 | 2019/021 | Companies (Prescribed Forms) Regulations, 2019 | sis_corporate | 150 | 142,745 |
| 4 | 2019/040 | Corporate Insolvency (Insolvency Practitioner Accreditation) Regulations, 2019 | sis_corporate | 5 | 4,866 |
| 5 | 2017/050 | Citizenship of Zambia Regulations, 2017 | sis_governance | 7 | 16,982 |
| 6 | 2022/027 | Citizenship of Zambia (Amendment) Regulations, 2022 | sis_governance | 2 | 1,573 |
| 7 | 2025/016 | Civil Aviation (Designated Provincial and Strategic Airports) Regulations, 2025 | sis_transport | 2 | 1,518 |
| 8 | 2020/073 | Civil Aviation Authority (Search and Rescue) Regulations, 2020 | sis_transport | 30 | 43,215 |

## Failures (0)

All 8 picks succeeded — no failures, no skips, no in-batch substitutions used.
2 reserved substitutes (1992/9 + 1985/45) were not consumed and remain available
for a future drain tick.

## Discovery probes

| Endpoint | URL | Modern (>=2017) | Novel | Outcome |
|---|---|---|---|---|
| alphabet=G | `?alphabet=G` | 1 | 0 | exhausted (sole modern G already in corpus) |
| alphabet=U | `?alphabet=U` | 19 | 0 | exhausted (all 19 modern U entries already in corpus) |
| alphabet=X | `?alphabet=X` | 0 | 0 | empty |
| alphabet=Y | `?alphabet=Y` | 0 | 0 | empty |
| alphabet=Z | `?alphabet=Z` | 6 | 0 | exhausted |
| year=2024 p1 | `?year=2024` | 12 | 0 | exhausted (first page) |
| year=2024 p2 | `?year=2024&page=2` | 1 | 0 | sparse |
| year=2024 p3 | `?year=2024&page=3` | 18 | 13 | productive — picked 8/13, 5 reserved (see _work/batch_0243_summary.json) |
| year=2023 p1 | `?year=2023` | 12 | 0 | exhausted |

## Integrity (CHECK1a/1b/2/3/4/5/6 — ALL PASS)

- CHECK1a unique ids: 8/8
- CHECK1b on-disk presence: 8/8
- CHECK2 amended_by refs: 0
- CHECK3 repealed_by refs: 0
- CHECK4 source_hash sha256 verified: 8/8 (against `raw/zambialii/si/(2017,2019,2020,2022,2025)/`)
- CHECK5 required fields 10×8: 0 missing
- CHECK6 cited_authorities refs: 0

## Provenance

- All sources fetched from zambialii.org under robots.txt content-signal `search=yes`
- Crawl-delay 5s honoured at 6.0s margin (CRAWL=6.0)
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- Robots.txt sha256 prefix `fce67b697ee4ef44` (unchanged from batches 0193-0242)
- Disallow on `/akn/zm/judgment/` + `/akn/zm/officialGazette/` enforced (judgments paused)

## Infrastructure follow-up

- Raw files (~26 = 8 HTML + 8 PDF + 1 robots + 9 probe HTMLs) await host-driven B2 sync (rclone unavailable in sandbox)
- OCR backlog unchanged at 11 items (no new failures this tick)
- 488+ pre-existing untracked records files unchanged this tick

## Next-tick options

- (a) Drain the 5 reserved year=2024 p3 candidates (2021/35 Citizens Economic Empowerment Transport; 2019/22 Citizens Economic Empowerment Reservation Scheme; 2025/20 Compulsory Standards Declaration; 2020/18 Compulsory Standards Potable Spirits; 2018/64 Constitutional Offices Emoluments) — likely sis_governance/sis_industry/sis_transport mix
- (b) Probe further year listings (e.g., year=2024 page=4, year=2023 page=2/3, year=2022 deep) for more novel modern SIs
- (c) Drain the 2 unused substitutes (1992/9 + 1985/45) as part of a sis_transport extension batch
- (d) Rotate to acts_in_force priority_order item 1 (Acts-listing endpoint discovery)
- (e) OCR retry on backlog (now 11 items) once tesseract is wired
