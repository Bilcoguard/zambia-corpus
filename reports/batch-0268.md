# Batch 0268 — Phase 4 Bulk Ingest

**Date (UTC):** 2026-04-26
**Sub-phase:** acts_in_force (Z residuals chronological tail — final 8 of 16)
**Parser version:** 0.6.0-act-zambialii-2026-04-26
**Yield:** 8/8 (100%) — extends 100%-yield streak across batches 0246–0268 (23 consecutive)
**MAX_BATCH_SIZE cap:** 8 — filled exactly

## Picks

| # | Year | Act No. | Title | Sections | Path |
|---|------|---------|-------|----------|------|
| 0 | 1989 | 1  | Zambia Centre for Accountancy Studies Act, 1989 | 6  | PDF fallback |
| 1 | 1993 | 25 | Zambia Iron and Steel Authority (Dissolution) Act, 1993 | 5  | PDF fallback |
| 2 | 1995 | 24 | Zambia Institute of Diplomacy and International Studies Act, 1995 | 21 | HTML akn-section |
| 3 | 1995 | 36 | Zambia Institute of Architects Act, 1995 | 54 | HTML akn-section |
| 4 | 1996 | 10 | Zambia Institute of Advanced Legal Education Act, 1996 | 24 | HTML akn-section |
| 5 | 1996 | 11 | Zambia Law Development Commission Act, 1996 | 22 | HTML akn-section |
| 6 | 1996 | 19 | Zambia Institute of Mass Communications (Repeal) Act, 1996 | 8  | HTML akn-section |
| 7 | 1997 | 11 | Zambia Institute of Human Resources Management Act, 1997 | 44 | HTML akn-section |

6 parsed cleanly via akn-section HTML; 2 used PDF fallback after HTML returned <2 akn-sections.
Largest section count: 1995/36 Zambia Institute of Architects (54). Smallest: 1993/25 Zambia Iron and Steel Authority Dissolution (5).

## Discovery cost
- 1 robots.txt re-verify (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193–0267)
- 0 alphabet listing fetches this tick (alphabet=Z listing reused from batch 0266 cache at
  `raw/zambialii/_alphabets/legislation-alphabet-Z-20260426T123515Z.html`)

## Per-record cost
- 8 record HTML fetches + 2 PDF fallbacks
- All on zambialii.org under robots-declared 5s crawl-delay using 6s margin

## Today fetches (cumulative)
315 (pre-tick after batch 0267) + 1 (robots) + 0 (listings) + 8 (records) + 2 (PDF fallbacks) = **326/2000** (16.3% of daily budget)
Tokens: within budget.

## Integrity (ALL PASS)
- CHECK1a batch unique IDs: 8/8
- CHECK1b corpus presence on disk: 8/8
- CHECK2 amended_by refs: 0
- CHECK3 repealed_by refs: 0
- CHECK4 source_hash sha256 verified against raw/zambialii/act/(1989,1993,1995,1996,1997)/: 8/8
- CHECK5 required 16 fields × 8 records: 128/128 present
- CHECK6 cited_authorities refs: 0

## Cumulative records
- Acts: 1008 (+8 over 1000)
- SIs: 593 (unchanged from batch 0252; large-PDF SI ingestion paused awaiting OCR)
- Judgments: 25 (unchanged; paused per robots Disallow on /akn/zm/judgment/)

## Reserved residuals carried forward
- **0 Z residuals remaining** — alphabet=Z fully swept (batches 0266+0267+0268)
- 1 S residual: 1956/4 Service of Process & Execution of Judgments (disambiguator-deferred, gaps.md)
- 2 alphabet=C deferred: Citizens Economic Empowerment 2006/9 + Constitution of Zambia 1996/17 (large, dedicated batches)
- 1 SI residual: 1990/39 ZNPF >4.5MB OCR backlog (15 items; tesseract not wired)

## Next-tick plan
1. Probe alphabet=X nature=act (skipped previous tick to consume Z first)
2. Continue alphabetic walk where still under-explored (revisit C, D, E etc. as backlog grows)
3. Implement disambiguator-aware fetch handler for 1956/4 Service of Process
4. OCR retry on 15-item SI backlog once tesseract is wired (deferred to host)
5. Re-verify robots.txt at start of next tick

## Infrastructure notes
- Persistent virtiofs unlink-failure warnings non-fatal (workaround stable across batches 0192–0268)
- Raw HTML/PDF files NOT committed (gitignore policy followed; raw cached locally for re-verify; awaits host-driven B2 sync — rclone unavailable in sandbox)
- corpus.sqlite NOT touched this batch (snapshot drift preserved; periodic full rebuild expected from host)
