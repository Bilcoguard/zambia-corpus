# Batch 0279 — Phase 4 bulk (acts_in_force, page-2 chronological sweep, fiscal-Appropriation series cont'd)

**Date:** 2026-04-26
**Phase:** 4 (bulk ingest)
**Sub-phase:** acts_in_force
**Approval:** approved=true, complete=false (per approvals.yaml; worker does not flip)
**Wall-clock:** ~ 9 min (well within 20-min cap; 4 sandbox slices × 2 records × 12s + parse + integrity + report)
**Yield:** 7 / 8 ingested (87.5 %); 1 deferred (act/2002/6 — PDF size cap)

## Picks (next 8 chronologically-earliest from refreshed page-2 pool)

| # | Year/Num | Alpha | Title | Status | Sections | Path |
|---|----------|-------|-------|--------|----------|------|
| 0 | 2001/6   | A | Appropriation Act, 2001 | ok       | 2 (PDF fallback) | records/acts/2001/act-zm-2001-006-appropriation-act.json |
| 1 | 2002/6   | A | Appropriation Act, 2002 | deferred | — | PDF 7,227,519 B > MAX_PDF_BYTES 4,500,000 — see gaps.md (raw HTML kept) |
| 2 | 2002/18  | S | Supplementary Appropriation (1999) Act, 2002 | ok | 2 (PDF fallback) | records/acts/2002/act-zm-2002-018-supplementary-appropriation-1999-act.json |
| 3 | 2002/19  | S | Supplementary Appropriation (2000) Act, 2002 | ok | 2 (PDF fallback) | records/acts/2002/act-zm-2002-019-supplementary-appropriation-2000-act.json |
| 4 | 2003/7   | S | Supplementary Appropriation (2001) Act, 2003 | ok | 2 (PDF fallback) | records/acts/2003/act-zm-2003-007-supplementary-appropriation-2001-act.json |
| 5 | 2003/8   | A | Appropriation Act, 2003 | ok | 2 (PDF fallback) | records/acts/2003/act-zm-2003-008-appropriation-act.json |
| 6 | 2004/5   | E | Excess Expenditure Appropriation (2000) Act, 2004 | ok | 3 (PDF fallback) | records/acts/2004/act-zm-2004-005-excess-expenditure-appropriation-2000-act.json |
| 7 | 2004/6   | S | Supplementary Appropriation (2002) Act, 2004 | ok (partial) | 1 (PDF; section 1 missed by OCR — see gaps.md) | records/acts/2004/act-zm-2004-006-supplementary-appropriation-2002-act.json |

## Pool refresh

- Inherited from batch 0278 `_work/batch_0278_remaining.json`: 86 candidates
- Picked first 8 chronologically (2001/6 → 2004/6) — all in fiscal Appropriation/Supplementary Appropriation/Excess Expenditure Appropriation series
- **Refreshed pool size for batch 0280: 78** (persisted to `_work/batch_0279_remaining.json`)

## Discovery cost

- 1 robots.txt re-verify (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0278; cached `raw/zambialii/_robots/robots-20260426T190427Z.txt`)
- 0 alphabet listing fetches (page-2 surface still cached from b0276; pool persisted in `_work/batch_0278_remaining.json`)

## Per-record cost

- 8 record HTML fetches (via /akn/zm/act/<yr>/<num>) split across 4 sandbox runs (slice 0:2 + 2:4 + 4:6 + 6:8 due to 45 s shell timeout × 6 s crawl-delay)
- 8 PDF fallbacks attempted (all 8 picks had HTML <2 akn-sections, consistent with fiscal-series pattern) — 7 succeeded, 1 (2002/6) rejected by MAX_PDF_BYTES guard before save
- Total: 8 HTML + 8 PDF = 16 record fetches; 7 PDFs persisted to disk (2002/6 PDF body fetched-then-discarded in-memory; bytes counted in costs.log per kind=record)

## Today fetches

Pre-tick: 488 / 2000 (24.40 %).
This tick: 1 robots + 8 record HTML + 8 PDF = 17 fetches.
Post-tick: **505 / 2000 (25.25 %)**. Tokens within budget.

## Rate-limit discipline

All fetches on zambialii.org under robots-declared 5 s crawl-delay (we use 6 s margin). UA = `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.

## Integrity check (committed records only — 7)

| Check | Result |
|-------|--------|
| CHECK1a (batch-unique IDs) | 7/7 PASS |
| CHECK1b (corpus presence on disk) | 7/7 PASS |
| CHECK2 (amended_by refs resolve) | 0 refs — PASS vacuously |
| CHECK3 (repealed_by refs resolve) | 0 refs — PASS vacuously |
| CHECK4 (source_hash sha256 verified) | 7/7 PASS — verified against raw/zambialii/act/(2001,2002,2002,2003,2003,2004,2004)/*.html |
| CHECK5 (16 required fields) | 112/112 PASS |
| CHECK6 (cited_authorities refs resolve) | 0 refs — PASS vacuously |

**ALL INTEGRITY CHECKS PASS** for 7 committed records. 2002/6 deferred PRE-commit (oversized PDF; not subject to integrity rules).

## Cumulative records

- acts: 1097 (+7 over 1090 worker-counter from batch 0278)
- SIs: 539 (unchanged from batch 0252)
- judgments: 25 (paused per robots Disallow on `/akn/zm/judgment/`)

## Reserved residuals carried to next tick

- **78 page-2 missing** across A/C/E/N/P/S (next 8 chronological from page-2 pool for batch 0280)
- 1 S residual (1956/4 Service of Process and Execution of Judgments — disambiguator-deferred)
- 2 alphabet=C deferred (Citizens Economic Empowerment 2006/9 + Constitution of Zambia 1996/17)
- OCR backlog 18 items (unchanged from b0278)
- OCR section-tolerant retry queue: 4 items (1988/32, 1994/40 [section 1 missed], 1995/33 [full re-extract], 2004/6 [section 1 missed]) — 1 added this batch
- **NEW: oversized-pdf queue** — 1 item (2002/6 — 7.2 MB > 4.5 MB cap). Recommend MAX_PDF_BYTES bump to 8 MB or streaming parser.

## Next-tick plan (batch 0280)

(a) refresh pool from cached page-2 HTML AND glob-dedup against records/acts (slug-suffix-agnostic);
(b) sweep next 8 chronologically-earliest from refreshed pool avoiding gaps.md-listed items;
(c) the 1990s/2000s Appropriation series remains unstable (PDFs are scanned-OCR'd with variable noise) — yield will fluctuate; keep parser strict (refuse fabrication);
(d) implement disambiguator-aware fetch handler for 1956/4 (still deferred);
(e) re-verify robots.txt at start of next tick;
(f) batch 0280 picks 2004/7, 2005/5, 2005/6, 2005/7, 2005/8, 2005/21 (Cotton Act 2005 — first non-fiscal!), 2006/1, 2006/2 — diversification of yield risk profile;
(g) once page-2 pool drains (~10 ticks at current yield), advance to next priority sub-phase (sis_corporate).

## Infrastructure follow-up (non-blocking)

- B2 sync deferred to host (rclone unavailable in sandbox). Peter to run: `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`
- Persistent virtiofs unlink-failure warnings on `.git/objects/tmp_obj_*` and `.git/objects/maintenance.lock` unchanged from batches 0192-0278 (rename succeeds, unlink fails — non-fatal).
- corpus.sqlite NOT touched this batch (snapshot drift preserved per established workflow). Now 543 records vs 1655 JSON on disk (1648 + 7).
- Pre-existing FTS5 vtable malformed image (records_fts) unchanged — non-blocking, flagged for full-rebuild scope.
