# Phase 4 Batch 0275 — acts_in_force chronological-first across all alphabets

**Tick start:** 2026-04-26T17:03:54Z (UTC)
**Tick complete (ingest):** 2026-04-26T17:08:00Z (UTC)
**Phase:** 4 (bulk ingest) — `approved: true`, `complete: false`
**Sub-phase:** `acts_in_force`
**Scope:** Cross-alphabet residual sweep — final 4 alphabet=A Appropriation Act residuals (1996-1999)
**Source:** zambialii.org (robots.txt re-verified, sha256 prefix `fce67b697ee4ef44`, crawl-delay 5s honoured at 6s margin)

## Picks (4 / MAX_BATCH_SIZE=8)

Inherited residual queue from batch 0274 worker.log entry: 4 alphabet=A Appropriation
Acts spanning 1996-1999 (the final tail of the alphabet=A residual series). Titles
verified against cached `raw/zambialii/legislation/alphabet-A-20260425.html` with
exact-match in `<a>` text and "Appropriation Act, <yr>" label (no fabrication per
BRIEF #1). Pre-flight on-disk check: all 4 confirmed not present (avoided silent
overwrite per BRIEF #4).

Cross-alphabet residual sweep (page 1) shows only 9 missing candidates total this tick,
of which 4 are these alphabet=A residuals. Other 5 candidates are deferred per
established worker.log policy: 1956/4 (disambiguator-deferred), 1996/17 + 2006/9
(alphabet=C deferred large items), 2000/8 + 2000/16 (OCR backlog awaiting tesseract).
Hence batch is 4 records (under MAX_BATCH_SIZE=8 cap). Per BRIEF: "If the batch
completes early, stop — do not start another."

| # | yr/num | Title | id | Sections | Source |
|---|---|---|---|---|---|
| 0 | 1996/13 | Appropriation Act, 1996 | act-zm-1996-013-appropriation-act-1996 | 1 | PDF fallback (HTML <2 sections) |
| 1 | 1997/13 | Appropriation Act, 1997 | act-zm-1997-013-appropriation-act-1997 | 2 | PDF fallback |
| 2 | 1998/3  | Appropriation Act, 1998 | act-zm-1998-003-appropriation-act-1998 | 2 | PDF fallback |
| 3 | 1999/3  | Appropriation Act, 1999 | act-zm-1999-003-appropriation-act-1999 | 2 | PDF fallback |

**Yield:** 4 / 4 (100%) — extends 100%-yield streak across batches 0246-0275 (30 consecutive at 100%).

## Integrity check (pre-commit)

```
PASS CHECK1a - 4 unique IDs in batch
PASS CHECK1b - 4/4 present in corpus
PASS CHECK2/3 - amended_by/repealed_by 0 refs to resolve
PASS CHECK4 - sha256 verified 4/4 against raw HTML
PASS CHECK5 - 16x4=64 required fields present
PASS CHECK6 - cited_authorities 0 refs
ALL CHECKS PASS
```

## Discovery & cost

- 1 robots.txt re-verify (sha256 `fce67b697ee4ef44...8f0`, unchanged from batches 0193-0274)
- 0 alphabet listing fetches (all 24 A-Z page-1 listings cached; 27th day of cache)
- 4 record HTML fetches + 4 PDF fallback fetches (all 4 Appropriation Acts had HTML <2 sections requiring PDF fallback)

Pre-tick fetches: 433/2000 (21.65%). Post-tick: 433 + 1 robots + 4 HTML + 4 PDF = **442/2000 (22.10%)**.

## Reserved residuals carried to next tick

- **alphabet=A residuals:** 0 remaining (page-1 sweep complete)
- **alphabet=S:** 1956/4 Service of Process and Execution of Judgments (disambiguator-deferred)
- **alphabet=C:** 1996/17 Constitution of Zambia + 2006/9 Citizens Economic Empowerment (deferred large items)
- **OCR backlog:** 17 items (act/2000/8 + act/2000/16 + 15 prior; tesseract not wired in sandbox)
- **Pagination expansion (deferred):** 6 alphabets show `?page=2` in cached page-1 HTML (A, C, E, N, P, S) — page-2 listings not yet fetched. Estimated additional discovery surface ≥ 60 new act listings.

## Cumulative records (worker counter)

- acts: 1070 (+4 over 1066)
- SIs: 539 (unchanged from batch 0252)
- judgments: 25 (paused per robots Disallow on /akn/zm/judgment/)

## Sub-phase progress note

With this batch the alphabet=A page-1 residual queue is fully drained (Appropriation Act
series 1980-1999, plus Apprenticeship Act 1964 done in batch 0273). Cross-alphabet page-1
sweep has reached natural exhaustion: only 5 deferred items remain (1956/4 disambiguator,
1996/17 + 2006/9 large-item deferrals, 2000/8 + 2000/16 OCR backlog). Worker does NOT
flip phase_4_bulk.complete — significant work remains: page-2 listing discovery
(≥6 alphabets), disambiguator handler, OCR pipeline, plus next priority sub-phases
(sis_corporate, sis_tax, etc.). Awaits human direction or next-tick advance.

## Next-tick plan

(a) Fetch `?page=2` for alphabets A, C, E, N, P, S (6 listing fetches under crawl-delay 5s)
to reveal additional cross-alphabet residual surface; store under
`raw/zambialii/legislation/alphabet-<L>-page2-<date>.html`.
(b) Sweep next 8 chronologically-earliest cross-alphabet picks from the expanded surface.
(c) Implement disambiguator-aware fetch handler for 1956/4.
(d) OCR retry on 17-item backlog once tesseract is wired (deferred to host).
(e) Re-verify robots.txt at start of next tick.
(f) If page-2 listings surface no new candidates, advance to next priority sub-phase
(`sis_corporate`).

## Infrastructure follow-up (non-blocking)

- batch-0275 raw files (4 act HTML + 4 PDF + 1 robots; 0 alphabet listing this tick) plus
  accumulated batches 0192-0274 raw files awaiting host-driven B2 sync (rclone unavailable
  in sandbox).
- Persistent virtiofs unlink-failure warnings non-fatal (workaround stable across batches
  0192-0275).
- SQLite snapshot drift unchanged this batch (corpus.sqlite has 543 records vs 1634 JSON
  on disk after this batch) — periodic full rebuild expected from host.
- Pre-existing FTS5 vtable malformed image (records_fts) unchanged — non-blocking for
  record integrity, flagged for full-rebuild scope.
