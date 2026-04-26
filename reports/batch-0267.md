# Batch 0267 — Phase 4 Bulk Ingest

**Date (UTC):** 2026-04-26
**Sub-phase:** acts_in_force (Z residuals sweep, chronological-first 8 of 16)
**Parser version:** 0.6.0-act-zambialii-2026-04-26
**Yield:** 8/8 (100%) — extends 100%-yield streak across batches 0246–0267 (22 consecutive)
**MAX_BATCH_SIZE cap:** 8 — filled exactly

## Picks

| # | Year | Act No. | Title | Sections |
|---|------|---------|-------|----------|
| 0 | 1964 | 39 | Zambia Youth Service Act, 1964 | 23 |
| 1 | 1966 | 1  | Zambia National Provident Fund Act, 1966 | 60 |
| 2 | 1966 | 9  | Zambia Red Cross Society Act, 1966 | 8 |
| 3 | 1966 | 32 | Zambia National Commission for UNESCO Act, 1966 | 10 |
| 4 | 1966 | 50 | Zambian Mines Local Pension Fund (Dissolution) Act, 1966 | 6 |
| 5 | 1967 | 18 | Zambia Tanzania Pipeline Act, 1967 | 12 |
| 6 | 1973 | 43 | Zambia Security Intelligence Service Act, 1973 | 10 |
| 7 | 1982 | 30 | Zambia National Tender Board Act, 1982 | 45 |

All 8 parsed cleanly via akn-section HTML; no PDF fallback required this batch.
Largest section count: 1966/1 ZNPF Act (60). Smallest: 1966/50 Mines Local Pension Fund (Dissolution) (6).

## Discovery cost
- 1 robots.txt re-verify (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193–0266)
- 0 alphabet listing fetches this tick (alphabet=Z listing reused from batch 0266 cache at
  `raw/zambialii/_alphabets/legislation-alphabet-Z-20260426T123515Z.html`)

## Per-record cost
- 8 record HTML fetches; 0 PDF fallbacks
- All on zambialii.org under robots-declared 5s crawl-delay using 6s margin

## Today fetches (cumulative)
306 (pre-tick after batch 0266) + 1 (robots) + 0 (listings) + 8 (records) = **315/2000** (15.75% of daily budget)
Tokens: within budget.

## Integrity (ALL PASS)
- CHECK1a batch unique IDs: 8/8
- CHECK1b corpus presence on disk: 8/8
- CHECK2 amended_by refs: 0
- CHECK3 repealed_by refs: 0
- CHECK4 source_hash sha256 verified against raw/zambialii/act/(1964,1966,1967,1973,1982)/: 8/8
- CHECK5 required 16 fields × 8 records: 128/128 present
- CHECK6 cited_authorities refs: 0

## Cumulative records
- Acts: 1000 (+8 over 992) — **milestone: 1000 acts on disk**
- SIs: 593 (unchanged from batch 0252; large-PDF SI ingestion paused awaiting OCR)
- Judgments: 25 (unchanged; paused per robots Disallow on /akn/zm/judgment/)

## Reserved residuals carried forward
- **8 Z residuals (chronological tail):** 1989/1, 1993/25, 1995/{24,36}, 1996/{10,11,19}, 1997/11
- 1 S residual: 1956/4 Service of Process & Execution of Judgments (disambiguator-deferred, gaps.md)
- 2 alphabet=C deferred: Citizens Economic Empowerment 2006/9 + Constitution of Zambia 1996/17 (large, dedicated batches)
- 1 SI residual: 1990/39 ZNPF >4.5MB OCR backlog (15 items; tesseract not wired)

## Next-tick plan
1. Sweep remaining 8 Z residuals (chronological tail — fills MAX_BATCH_SIZE=8 exactly)
2. Probe alphabet=X (skipped this tick to consume Z first)
3. Implement disambiguator-aware fetch handler for 1956/4 (S residual)
4. OCR retry on 15-item SI backlog once tesseract wired (deferred to host)
5. Re-verify robots.txt at start of next tick

## Infrastructure notes (non-blocking)
- B2 sync deferred to host (rclone unavailable in sandbox)
- Persistent virtiofs unlink-failure warnings on `.git/objects/tmp_obj_*` and
  `.git/objects/maintenance.lock` unchanged from batches 0192–0266 (rename succeeds, unlink fails — non-fatal)
- corpus.sqlite snapshot drift (543 records vs 1574 JSON on disk after this batch) — periodic full rebuild expected from host
- FTS5 vtable malformed image (records_fts) unchanged — non-blocking for record integrity
