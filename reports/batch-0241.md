# Phase 4 Batch 0241 — sis_education FIRST cluster + sis_judicial FIRST single + E-residual final drains

**Date:** 2026-04-25 (UTC)
**Tick window:** 22:35Z—22:5xZ
**Phase:** 4 (bulk ingestion) — approved + incomplete
**Cohort:** sis_education FIRST cluster (4 records via H-probe) + sis_judicial FIRST single (1 record via H-probe) + sis_elections E-residual final drain (2 records) + sis_employment E-residual (1 attempted, 1 failed scanned-image)

## Discovery
- Robots.txt re-verified: sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0240; crawl-delay 5s honoured at 6s margin (CRAWL=6.0); `Disallow` on `/akn/zm/judgment/` + `/akn/zm/officialGazette/` enforced.
- Fresh **alphabet H probe** (`https://zambialii.org/legislation/?alphabet=H`): 15 unique SIs, 8 modern (≥2017), 6 novel after dedup against HEAD. Saved to `_work/batch_0241_alphabet_H.html` and `_work/batch_0241_h_probe.json`.
- Combined with 3 remaining unprocessed novel from batch_0233 E-probe cache (2024/15, 2024/29, 2022/13).

## Picks (8 committed + 1 fail)

| idx | yr/num | title | sub_phase | parent_act | result |
|----:|:-------|:------|:----------|:-----------|:------:|
| 0 | 2024/015 | Electoral Process (LG By-Elections) Order, 2024 | sis_elections | Electoral Process Act | ok |
| 1 | 2024/029 | Electoral Process (LG By-elections) Order, 2024 | sis_elections | Electoral Process Act | ok |
| 2 | 2022/013 | Minimum Wages (Truck and Bus Drivers) (Amendment) Order, 2022 | sis_employment | Min. Wages Act | **fail** (pdf_parse_empty — added to OCR backlog) |
| 3 | 2022/005 | Economic and Financial Crimes (Division of Court) Order, 2022 | **sis_judicial (FIRST)** | Subordinate Courts Act | ok |
| 4 | 2022/039 | Education (Public Higher Education Institution) (Declaration) Order, 2022 | **sis_education (FIRST)** | Higher Education Act | ok |
| 5 | 2019/069 | Palabana University (Declaration) Order, 2019 | sis_education | Higher Education Act | ok |
| 6 | 2018/039 | Levy Mwanawasa Medical University (Declaration) Order, 2018 | sis_education | Higher Education Act | ok |
| 7 | 2018/003 | Zambia Defence University (Declaration) Order, 2018 | sis_education | Higher Education Act | ok |
| 8 | 2018/002 | Education (Military Training Establishment of Zambia Management) (Dissolution) Regulations, 2018 | sis_education | Education Act | ok (in-batch substitute for failed idx 2) |

## Sub-phase footprint
- **sis_education** +4 (FIRST cluster) — Higher Education Act + Education Act
- **sis_judicial** +1 (FIRST cluster) — Subordinate Courts Act / Economic & Financial Crimes Court division
- **sis_elections** +2 (E-residual drain — final novel batch_0233 items)
- **sis_employment** +0 / 1 attempted (2022/13 scanned-image fail; deferred to OCR backlog)
- **2 first-instance sub-phases** this tick (sis_education + sis_judicial).

## Yield
8 ok / 9 attempted = **89%** record yield. 1 in-batch substitute fired (idx 8 stepping in for failed idx 2 substitution within MAX_BATCH_SIZE cap of 8).

## Integrity
ALL CHECKS PASS:
- CHECK1a (batch unique ids): 8/8
- CHECK1b (corpus disk presence): 8/8
- CHECK2/3 (amended_by/repealed_by refs): 0
- CHECK4 (source_hash sha256 verified against raw): 8/8
- CHECK5 (10 required fields × 8 records): all present
- CHECK6 (cited_authorities refs): 0

## Cumulative
- SI records after this batch: **514** (+8 over batch-0240's 506)
- Judgments: 25 (paused per robots Disallow on `/akn/zm/judgment/`)

## Cost & budget
- Today fetches: 708 / 2000 (35.4%) — all on zambialii.org under 5s crawl-delay (6s margin).
- New fetches this tick: 18 (1 robots reverify + 1 alphabet H probe + 16 record fetches × 2 [HTML+PDF])
- Tokens within budget.

## Next-tick plan
- (a) Continue probing fresh alphabets — K, O, Q, R, U, V, W, X, Y, Z still unprobed in 2026-04-25 set; H-probe novel cache now drained (6/6 ok).
- (b) Rotate to `acts_in_force` priority_order item 1 — would require Acts-listing endpoint discovery (separate path from SI alphabet probe).
- (c) OCR retry on backlog (now 10 items: 2017/068, 2018/011, 2018/075, 2018/093, 2022/004, 2022/007, 2022/008, 2022/012, 2022/013, 2026/004) once tesseract is wired.
- Re-verify robots.txt at start of next tick.

## Infrastructure follow-up (non-blocking)
- batch-0241 raw files (~17 = 8 HTML + 8 PDF + 2 fail-preserved files + 1 robots + 1 alphabet probe) plus accumulated batches 0192-0240 raw files awaiting host-driven B2 sync (rclone unavailable in sandbox).
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild (deferred to host).
- persistent virtiofs unlink-failure warnings non-fatal (workaround stable across batches 0192-0241).
- 488+ pre-existing untracked records files unchanged.
- OCR backlog at 10 items (+1 this tick: 2022/013).
