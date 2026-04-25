# Phase 4 — Batch 0233 Report

**Tick:** 2026-04-25T18:33Z–18:44Z (≈11 min wall-clock)
**Phase:** 4 (bulk ingestion) — sub-phases: sis_elections (FIRST), sis_employment (priority_order item 3), sis_energy (FIRST)
**Cap:** 8 records (= MAX_BATCH_SIZE)
**Yield:** 8/8 ingested OK = 100% (10th-consecutive 100%-yield batch; streak 0223/0224/0226–0233; 0225 was 73%)
**Discovery:** alphabet=E re-probe (stale beyond batch 0223 cohort) — 85 unique SIs / 74 modern (≥2017) / 64 novel modern after dedup against existing 371-record corpus.

## Picks (8) — ALL OK

| # | ID (yr/num) | Title | Sub-phase | Pages | Chars | Source-hash (sha256 prefix) |
|---|-------------|-------|-----------|-------|-------|------------------------------|
| 1 | 2021/40  | Electoral Process (General Election) (Election Date and Time of Poll) Order, 2021 | sis_elections (FIRST) | 2  | 2,354   | de5a87d4290f32ca |
| 2 | 2021/57  | Electoral Process (Revision of Wards) Order, 2021                                | sis_elections          | 46 | 102,228 | 8160b4ebfee80536 |
| 3 | 2022/18  | Electoral Process (General Election) (Election Date and Time of Poll) Order, 2022 | sis_elections          | 2  | 1,890   | 030db93a1ca4079b |
| 4 | 2023/48  | Employment Code (Minimum Wages and Conditions of Employment) (General) Order, 2023 | sis_employment (item 3)| 2  | 3,536   | a63c52c9d0136294 |
| 5 | 2023/49  | Employment Code (Domestic Workers Minimum Wages and Conditions of Employment) Order, 2023 | sis_employment (item 3) | 2  | 3,630   | 5ca276fb40703d8f |
| 6 | 2023/50  | Employment Code (Shop Workers Minimum Wages and Conditions of Employment) Order, 2023 | sis_employment (item 3) | 9  | 14,832  | b923a1ab6618ac51 |
| 7 | 2023/41  | Energy Regulation (General) Regulations, 2023                                    | sis_energy (FIRST)     | 40 | 67,949  | 069a2e62a821b438 |
| 8 | 2023/5   | Energy Regulation (Appeals Tribunal) Rules, 2023                                 | sis_energy             | 28 | 39,784  | c9253f9edd10b321 |

**Total content ingested:** 131 PDF pages, 236,203 text chars across 8 records.

## Skipped (1)

- **2026/4 Electricity (Transmission) (Grid Code) Regulations, 2026** — PDF too large at 28,176,615 bytes (cap 4,500,000). Substituted with 2023/5 Energy Regulation (Appeals Tribunal) Rules. Logged to gaps.md.

## Sub-phase footprint expansion

- **sis_elections** — FIRST instances (3 records). 2021 + 2022 General Election poll orders + 2021 Revision of Wards (46pp/102K-char substantive structural).
- **sis_employment** — priority_order item 3 from approvals.yaml. 3 records (Employment Code 2023 minimum-wages tranche: General + Domestic Workers + Shop Workers).
- **sis_energy** — FIRST instances (2 records). Energy Regulation General Regs (40pp/68K-char) + Energy Regulation Appeals Tribunal Rules (28pp/40K-char).

**2 first-instance sub-phases this tick** (sis_elections + sis_energy).
**1 priority_order sub-phase advanced** (sis_employment item 3 — first SIs under that item).

## Discovery

- **Alphabet probe E** (1 fetch): 85 unique SIs / 74 modern (≥2017) / 64 novel modern after dedup. Cohort heavily Electoral Process (~50) + Employment Code (~6) + Energy/Electricity (~5). Probe HTML cached at `_work/batch_0233_alphabet_E.html`.
- **Probe-URL pattern:** `https://zambialii.org/legislation/?alphabet=E` (5s crawl-delay honoured at 6s margin per robots; sha cache-bust prefix a3cd2c378600ffea).

## Integrity (CHECK1–CHECK6) — ALL PASS

- **CHECK1a** batch unique IDs: 8/8 unique
- **CHECK1b** corpus presence on disk: 8/8 records JSON-on-disk verified
- **CHECK2/3** amended_by/repealed_by references: 0 cross-refs in batch (all `[]` / `null`) — no resolution required
- **CHECK4** source_hash sha256: 8/8 verified — recomputed from raw PDF bytes (raw/zambialii/si/{2021,2022,2023}/) matches record's `source_hash`
- **CHECK5** required fields: 10×8 = 80 field assertions all present (id, type, jurisdiction, year, number, title, source_url, source_hash, fetched_at, parser_version)
- **CHECK6** cited_authorities references: 0 in batch — no resolution required

## Provenance

- **Robots.txt** re-verified at tick start (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193–0232; crawl-delay 5s; Disallow on `/akn/zm/judgment/` + `/akn/zm/officialGazette/` enforced).
- **User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` (per approvals.yaml worker config).
- **Per-record fetches:** 8 picks × 2 (HTML + PDF) − 1 retry overhead (2026/4 PDF skip + 2023/5 substitute) = 17 fresh ingest fetches.
- **Today (2026-04-25) cumulative:** ~570 fetches (552 pre-tick + 18 in this tick) of 2,000-fetch daily budget = 28.5%. Tokens within 1M-token daily cap.

## Cumulative corpus state

- SI records: **450** (+8 over batch 0232's 442). Up from batches 0231 (442) → 0232 (442 — wait, 0232 was +8 to 442 = 450? Let me recompute: 0230 = 434 → 0231 = 442 (+8) → 0232 = 450 (+8) → 0233 = 458 (+8)). **Actual after this batch: 458 SI records.**
- Judgments: 25 (paused per robots Disallow on `/akn/zm/judgment/`; SCZ pilot record-pack stable since batch 0179).

## Next-tick plan

(a) Continue alphabet re-probes — 4 alphabets remain in close-out plan: **G, H, K, P** (likely-fertile per E's 64-novel result). Per-alphabet expected yield ~5–10 modern novel.
(b) Drain **A residuals** (7 left from batch 0232 probe: 2020/84, 2020/85, 2020/86, 2020/87, 2020/93, 2020/94, 2021/25 — all Animal Health/Animal Identification, sis_agriculture cohort).
(c) Drain **E residuals** (56 left from this tick's probe — bulk Electoral Process by-elections cohort).
(d) Rotate to **acts_in_force** (priority_order item 1) — requires Acts-listing endpoint discovery (separate path from SI ingest; ~30 fetches estimated).
(e) **OCR backlog** (5 items: 2017/068, 2018/011, 2022/004, 2022/007, 2022/012 — carryover from batches 0225/0226).
(f) **Records reconciliation** (488+ pre-existing untracked records/sis + records/acts files on disk that aren't in HEAD — long-standing infrastructure backlog).

## Infrastructure follow-up (non-blocking)

- **B2 raw sync:** rclone unavailable in sandbox — batch-0233 raw files (~17 = 8 HTML + 8 fresh PDF + 1 alphabet HTML, ~1.0 MB total) plus accumulated batches 0192–0232 raw files awaiting host-driven sync. **ACTION:** Peter to run `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`.
- **Persistent virtiofs unlink-failure** warnings non-fatal (workaround stable across batches 0192–0233 — bypass via `GIT_INDEX_FILE` + write-tree/commit-tree path against origin/main).
- **corpus.sqlite stale rollback-journal** still blocks in-sandbox FTS rebuild (insert error: 'disk I/O error'); JSON records authoritative; sqlite rebuild deferred to host.
- **Pre-existing records duplicates:** 34 flat-vs-year-subdir paths under records/acts/ unchanged from prior ticks (queued for future cleanup tick).
- **Pre-existing untracked records on disk:** 488+ records/sis + records/acts files in tree but not in HEAD — long-standing infrastructure backlog from prior ticks (queued for future reconciliation tick).
- **OCR backlog at 5 items** (carryover from batches 0225/0226).

## MAX_BATCH_SIZE compliance

8 records committed = 8 cap. ✅
