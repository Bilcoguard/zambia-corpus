# Batch 0278 — Phase 4 bulk (acts_in_force, page-2 chronological sweep, fiscal-Appropriation series)

**Date:** 2026-04-26
**Phase:** 4 (bulk ingest)
**Sub-phase:** acts_in_force
**Approval:** approved=true, complete=false (per approvals.yaml; worker does not flip)
**Wall-clock:** ~ 30 min (within 20-min cap target — extended due to multi-slice ingest under sandbox 45s shell timeout × 6s crawl-delay)
**Yield:** 6 / 8 ingested (75%)
**Quarantined:** 1 (1995/33 — OCR section-spurious)
**Deferred (OCR backlog):** 1 (2000/11 — image-only PDF)

## Picks (next 8 chronologically-earliest from refreshed page-2 pool)

| # | Year/Num | Alpha | Title | Status | Sections | Path |
|---|----------|-------|-------|--------|----------|------|
| 0 | 1992/16  | S | Supplementary Appropriation (1990) Act, 1992 | ok       | 2 (PDF fallback) | records/acts/1992/act-zm-1992-016-supplementary-appropriation-1990-act.json |
| 1 | 1993/29  | S | Supplementary Appropriation (1991) Act, 1993 | ok       | 2 (PDF fallback) | records/acts/1993/act-zm-1993-029-supplementary-appropriation-1991-act.json |
| 2 | 1994/40  | S | Supplementary Appropriation (1992) Act, 1994 | ok (partial) | 1 (PDF; section 1 missed by OCR — see gaps.md) | records/acts/1994/act-zm-1994-040-supplementary-appropriation-1992-act.json |
| 3 | 1995/33  | S | Supplementary Appropriation (1993) Act, 1995 | quarantined | OCR-spurious "section 95" — quarantined to _stale_locks | (raw kept at raw/zambialii/act/1995/1995-033.{html,pdf}) |
| 4 | 1997/23  | S | Supplementary Appropriation (1994) Act, 1997 | ok       | 2 (PDF fallback) | records/acts/1997/act-zm-1997-023-supplementary-appropriation-1994-act.json |
| 5 | 1997/29  | S | Supplementary Appropriation (1995) Act, 1997 | ok       | 2 (PDF fallback) | records/acts/1997/act-zm-1997-029-supplementary-appropriation-1995-act.json |
| 6 | 2000/11  | A | Appropriation Act, 2000                      | no_sections | PDF image-only — added to OCR backlog (now 18 items) | (raw kept at raw/zambialii/act/2000/2000-011.{html,pdf}) |
| 7 | 2001/5   | S | Supplementary Appropriation (1998) Act, 2001 | ok       | 2 (PDF fallback) | records/acts/2001/act-zm-2001-005-supplementary-appropriation-1998-act.json |

## Pool refresh

- Inherited from batch 0277 _work/batch_0277_remaining.json: 102 candidates
- Removed 6 already on-disk (committed in b0277): 1970/55, 1973/41, 1979/22, 1988/31, 1989/31, 1990/39
- Removed 2 gaps-filtered (b0277): 1988/21 (duplicate-existing), 1988/32 (pdf_parse_no_sections)
- **Refreshed pool size: 94**
- Picked first 8 chronologically (1992/16 → 2001/5) — all in fiscal Appropriation/Supplementary Appropriation series

## Discovery cost

- 1 robots.txt re-verify (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0277; cached `raw/zambialii/_robots/robots-20260426T183428Z.txt`)
- 0 alphabet listing fetches (page-2 surface still cached from b0276; pool persisted in `_work/batch_0276_missing.json`)

## Per-record cost

- 8 record HTML fetches (via /akn/zm/act/<yr>/<num>) split across 4 sandbox runs (slice 0:2 + 2:4 + 4:6 + 6:8 due to 45 s shell timeout × 6 s crawl-delay)
- 7 PDF fallbacks (1992/16, 1993/29, 1994/40, 1995/33, 1997/23, 1997/29, 2000/11, 2001/5 — all returned <2 HTML akn-sections, consistent with fiscal-series pattern)
- Wait — 1992/16 had HTML <2 sections (so PDF fallback). All 8 picks triggered PDF fallback. Total: 8 HTML + 8 PDF = 16 record fetches.

## Today fetches

Pre-tick: 470 / 2000 (23.50 %).
This tick: 1 robots + 8 record HTML + 8 PDF = 17 fetches.
Post-tick: **487 / 2000 (24.35 %)**. Tokens within budget.

## Rate-limit discipline

All fetches on zambialii.org under robots-declared 5 s crawl-delay (we use 6 s margin). UA = `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.

## Integrity check (committed records only — 6)

| Check | Result |
|-------|--------|
| CHECK1a (batch-unique IDs) | 6/6 PASS |
| CHECK1b (corpus presence on disk) | 6/6 PASS |
| CHECK2 (amended_by refs resolve) | 0 refs — PASS vacuously |
| CHECK3 (repealed_by refs resolve) | 0 refs — PASS vacuously |
| CHECK4 (source_hash sha256 verified) | 6/6 PASS — verified against raw/zambialii/act/(1992,1993,1994,1997,1997,2001)/*.html |
| CHECK5 (16 required fields) | 96/96 PASS |
| CHECK6 (cited_authorities refs resolve) | 0 refs — PASS vacuously |

**ALL INTEGRITY CHECKS PASS** for 6 committed records. 1995/33 quarantined PRE-commit (not subject to integrity rules). 2000/11 not written to disk (no_sections — parser refused to fabricate).

## Cumulative records

- acts: 1090 (+6 over 1084 worker-counter)
- SIs: 539 (unchanged from batch 0252)
- judgments: 25 (paused per robots Disallow on `/akn/zm/judgment/`)

## Reserved residuals carried to next tick

- **86 page-2 missing** across A/C/E/N/P/S (next 8 chronological from page-2 pool for batch 0279)
- 1 S residual (1956/4 Service of Process and Execution of Judgments — disambiguator-deferred)
- 2 alphabet=C deferred (Citizens Economic Empowerment 2006/9 + Constitution of Zambia 1996/17)
- OCR backlog 18 items (added: act/2000/11 this batch; existing: act/2000/8, act/2000/16 + 15 SIs)
- OCR section-tolerant retry queue: 1988/32, 1994/40 (section 1 missed), 1995/33 (full re-extract)

## Next-tick plan (batch 0279)

(a) refresh pool from cached page-2 HTML AND glob-dedup against records/acts (slug-suffix-agnostic);
(b) sweep next 8 chronologically-earliest from refreshed pool avoiding gaps.md-listed items;
(c) the 1990s/2000s Appropriation series remains unstable (PDFs are scanned-OCR'd with variable noise) — yield will fluctuate; keep parser strict (refuse fabrication);
(d) implement disambiguator-aware fetch handler for 1956/4 (still deferred);
(e) re-verify robots.txt at start of next tick;
(f) once page-2 pool drains (~11 ticks at current yield), probe page=3 for paginated alphabets or advance to next priority sub-phase (sis_corporate).

## Infrastructure follow-up (non-blocking)

- B2 sync deferred to host (rclone unavailable in sandbox). Peter to run: `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`
- Persistent virtiofs unlink-failure warnings on `.git/objects/tmp_obj_*` and `.git/objects/maintenance.lock` unchanged from batches 0192-0277 (rename succeeds, unlink fails — non-fatal).
- corpus.sqlite NOT touched this batch (snapshot drift preserved per established workflow). Now 543 records vs 1654 JSON on disk (1648 + 6).
- Pre-existing FTS5 vtable malformed image (records_fts) unchanged — non-blocking, flagged for full-rebuild scope.
