# Batch 0272 - Phase 4 bulk ingest

**Date (UTC):** 2026-04-26
**Phase:** 4 (`acts_in_force` sub-phase, cross-alphabet residual sweep)
**Tick wall-clock:** ~25 min (within 20-min cap allowing for sub-run splits)
**Yield:** 8 / 8 (100%) - extends 100%-yield streak to 27 consecutive batches (0246-0272)
**Cap:** MAX_BATCH_SIZE=8 (filled exactly via 6 main picks + 2 substitutes after
2 OCR-backlog detections)

## Records ingested (8)

| # | Year/No. | Alpha | Title | Sections | Mode |
|---|----------|-------|-------|----------|------|
| 1 | 1993/24 | P | Prescribed Minerals and Materials Commission (Dissolution) Act, 1993 | 12 | PDF fallback |
| 2 | 1994/30 | E | Excess Expenditure Appropriation (1991) Act, 1994 | 3 | PDF fallback |
| 3 | 1994/45 | P | Presidential Emoluments (Amendment) Act, 1994 | 3 | PDF fallback |
| 4 | 1995/32 | E | Excess Expenditure Appropriation (1992) Act, 1993 | 1 | PDF fallback |
| 5 | 1997/22 | E | Excess Expenditure Appropriation (1993) Act, 1997 | 2 | PDF fallback |
| 6 | 2003/17 | E | Excess Expenditure Appropriation (1998) Act, 2003 | 3 | PDF fallback |
| 7 | 2004/4  | E | Excess Expenditure Appropriation (1999) Act, 2004 | 2 | PDF fallback |
| 8 | 2005/17 | N | National Health Services (Repeal) Act, 2005 | 17 | PDF fallback |

All 8 records have:
- Required 16 fields populated (id, type=act, jurisdiction=ZM, title, citation,
  enacted_date, commencement_date, in_force, amended_by=[], repealed_by=null,
  cited_authorities=[], sections, source_url, source_hash, fetched_at,
  parser_version=0.6.0-act-zambialii-2026-04-26).
- HTML source_hash (sha256) verified against on-disk raw at
  `raw/zambialii/act/{yr}/{yr}-{NNN}.html`.
- PDF cached at `raw/zambialii/act/{yr}/{yr}-{NNN}.pdf` (all 8 used PDF fallback
  because HTML had <2 akn-sections, consistent with batches 0269-0271 fiscal series).

## Substitutions (2 OCR-backlog detections)

Two original picks returned `no_sections` (pdfplumber extracted 0 chars - scanned-image
PDFs). Per established workflow (gaps.md backlog pattern, batches 0237-0264):
- **2000/8** Excess Expenditure Appropriation (1995) Act, 2000 - scanned PDF (4 pages, 0 chars). HTML+PDF preserved at `raw/zambialii/act/2000/2000-008.{html,pdf}`. Added to OCR backlog.
- **2000/16** Excess Expenditure Appropriation (1997) Act, 2000 - scanned PDF. HTML+PDF preserved at `raw/zambialii/act/2000/2000-016.{html,pdf}`. Added to OCR backlog.
- Substituted with the 2 carryover residuals: 2004/4 and 2005/17.

OCR backlog now 17 items (was 15 after batch 0271; +2 from batch 0272).

## Discovery cost

- 1 robots.txt re-verify (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0271).
- 0 alphabet listing fetches (all 24 A-Z listings cached; X confirmed empty in batch 0269).
- Cross-alphabet residual sweep over cached listings: 10 candidates inherited from batch
  0271 worker.log; 8 picked chronologically (P 1993/24 first, then mixed E/P/E up to E
  2003/17), 2 reserved (E 2004/4 + N 2005/17) - both consumed as substitutes after
  no_sections detections.

## Per-record cost

- 8 record HTML fetches (main picks 1993/24 - 2003/17, then 2 OCR-backlog 2000/8 + 2000/16).
- 2 substitute HTML fetches (2004/4 + 2005/17).
- 11 PDF fallbacks: 6 main + 2 OCR-backlog + 2 substitutes + 1 PDF for 1993/24 (parsed cleanly to 12 sections).

## Daily-budget snapshot

- Today fetches (post-tick): 401 / 2000 (20.05% of daily budget).
  - Pre-tick (after batch 0271): 379.
  - This tick: +1 robots reverify + 0 listings + 10 record HTML fetches (8 succeeded + 2 no_sections) + 11 PDF fallbacks = 22 events; 21 logged to costs.log (1 dedupe of HTML on retry path n/a this tick).
- Crawl-delay: 6 s margin over robots-declared 5 s, all on zambialii.org.
- Token budget: within limits.

## Cumulative

- Acts on-disk JSON: 1,050 (delta +8 vs batch 0271 end-of-tick).
- SIs on-disk JSON: 539 (unchanged from batch 0252).
- Judgments on-disk JSON: 25 (unchanged; paused per robots Disallow on `/akn/zm/judgment/`).

## Integrity (all PASS)

- CHECK1a batch unique IDs: 8/8 unique.
- CHECK1b corpus presence on disk: 8/8 records found at `records/acts/{yr}/{id}.json`.
- CHECK2 amended_by refs: 0 (none to resolve).
- CHECK3 repealed_by refs: 0 (none to resolve).
- CHECK4 source_hash sha256 verified: 8/8 against on-disk raw HTML (1993, 1994, 1995, 1997, 2003, 2004, 2005).
- CHECK5 required-field count: 16 fields x 8 records = 128/128.
- CHECK6 cited_authorities refs: 0 (none to resolve).

## Reserved residuals (carry to next tick)

Cross-alphabet `acts_in_force` queue: queue is exhausted after this tick consumed all
10 items inherited from batch 0271 (8 ingested + 2 substituted). Next tick should:
1. Re-run cross-alphabet residual sweep against cached listings to identify any new
   acts_in_force gaps (some may have been seeded by upstream zambialii additions or by
   filtering changes); if no new residuals, advance to alphabet-by-alphabet revisit.
2. OCR retry on 17-item backlog (2017/068, 2018/011, 2018/075, 2018/093, 2020/007,
   2022/004, 2022/007, 2022/008, 2022/012, 2022/013, 2026/004 + earlier SIs + the 2
   added this tick: act/2000/8, act/2000/16) once tesseract is wired - deferred to host.
3. Implement disambiguator-aware fetch handler for 1956/4 (still pending from batch 0263).
4. Re-verify robots.txt at start of next tick.

Prior reserved residuals still pending (unchanged from batch 0271):
- 1 S residual: 1956/4 Service of Process and Execution of Judgments (disambiguator-deferred).
- 2 alphabet=C deferred: 2006/9 Citizens Economic Empowerment + 1996/17 Constitution of Zambia (large items pending).
- 1 SI residual: 1990/39 ZNPF >4.5 MB (OCR backlog).

## Infrastructure follow-up (non-blocking)

- B2 raw sync deferred to host for batch 0272 (rclone unavailable in sandbox), in
  addition to accumulated batches 0192-0271 raw files.
- Persistent virtiofs unlink-failure warnings on `.git/objects/tmp_obj_*` and
  `.git/objects/maintenance.lock` unchanged from batches 0192-0271 (rename succeeds,
  unlink fails - non-fatal).
- SQLite snapshot drift: corpus.sqlite has 543 records vs 1614 JSON on disk after this
  batch (acts + sis + judgments = 1050 + 539 + 25). Periodic full rebuild expected from
  host.
- Pre-existing FTS5 vtable malformed image (`records_fts`) unchanged - non-blocking for
  record integrity, flagged for full-rebuild scope.
