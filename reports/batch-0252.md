# Batch 0252 Report — Phase 4 bulk ingest

**Date (UTC):** 2026-04-26
**Phase:** 4 (bulk)
**Sub-phase emphasis:** sis_governance (drain Tender Board Act residuals from batch 0251)
**Records committed:** 2 / 2 attempted (yield 100%)
**Wall-clock:** ~6 min

## Picks

| Idx | yr/num | Title | Parent Act | Sub-phase | Status |
|-----|--------|-------|------------|-----------|--------|
| 0 | 1991/35 | Tender Regulations (Commencement) Order, 1991 | Tender Board Act | sis_governance | ok |
| 1 | 1998/43 | Tender (Amendment) Regulations, 1998 | Tender Board Act | sis_governance | ok |

Both picks were the 2 reserved residuals carried from batch 0251 close-out. The third reserved residual (1990/39 ZNPF Statutory Contributions Regs) remains in the OCR backlog at >4.5MB MAX_PDF_BYTES cap (no attempt this tick).

## FIRST parent-Act linkages

- **Tender Board Act** — first appearance in sis_governance via 1991/35 Tender Regulations (Commencement) Order. 1998/43 Tender (Amendment) Regulations is the second linkage to the same parent Act.

## Discovery

Pure cache-drain tick (no fresh discovery probes). One robots.txt re-verify only.

## Costs (this tick)

- Fetches: 5 = 1 robots + 2 record HTML + 2 record PDF
- Today fetches: 147 (pre-tick after batch 0251) + 5 = 152 / 2000 (7.6% of daily budget)
- All on zambialii.org under robots-declared 5s crawl-delay using 6s margin
- Tokens within budget (no token-heavy operations this tick)

## Robots.txt

- sha256 prefix `fce67b697ee4ef44` (unchanged from batches 0193-0251)
- Crawl-delay: 5s (honoured at 6s margin)
- Disallow honoured: `/akn/zm/judgment/`, `/akn/zm/officialGazette/`, `/api/`, `/*/search/`

## Integrity (CHECK1a–CHECK6, all PASS)

- CHECK1a (batch unique ids): 2/2
- CHECK1b (corpus presence on disk): 2/2
- CHECK2 (amended_by resolves): 0 refs (trivially pass)
- CHECK3 (repealed_by resolves): 0 refs (trivially pass)
- CHECK4 (source_hash sha256 verified against raw/zambialii/si/(1991,1998)/): 2/2
- CHECK5 (10 required fields x 2 records): all present
- CHECK6 (cited_authorities resolves): 0 refs (trivially pass)

## Cumulative SI records (post-batch 0252)

- Total SI records: 593 (+2 over batch 0251's 591)
- Sub-phase footprint this tick: sis_governance +2 (Tender Board Act)

## Reserved residuals carry to next tick

1 candidate:
- 1990/39 ZNPF Statutory Contributions Regs — needs OCR or PDF split for >4.5MB cap (OCR backlog now 15 items, unchanged)

## Next-tick plan

- (a) **Pivot to acts_in_force** (priority_order item 1 from approvals.yaml): Acts-listing endpoint discovery on zambialii.org (e.g. `/legislation/?nature=act&format=json` or year-listing exhaustion under `/akn/zm/act/`).
- (b) Probe alphabets X/Y per batch 0251 plan if acts_in_force discovery is brittle (note: batch 0250 close-out claimed 26-of-26 alphabets probed; X/Y status to be re-confirmed next tick).
- (c) OCR retry on 15-item backlog once tesseract is wired (deferred to host).

## Infrastructure follow-up (non-blocking)

- batch-0252 raw files (~5 = 2 HTML + 2 PDF + 1 robots) plus accumulated batches 0192-0251 raw files awaiting host-driven B2 sync (rclone unavailable in sandbox)
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild (deferred to host)
- Persistent virtiofs unlink-failure warnings non-fatal (workaround stable across batches 0192-0252 via write-tree/commit-tree path bypassing lock)
- 488+ pre-existing untracked records files unchanged this tick

## MAX_BATCH_SIZE

8 cap honoured. 2 records committed (well under cap; conservative drain-only batch per BRIEF "do one bounded unit of work" — preferring a small, clean commit over a speculative larger one within the 20-min wall-clock cap).
