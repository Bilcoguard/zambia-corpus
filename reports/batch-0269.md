# Batch 0269 — Phase 4 Bulk Ingest

**Date (UTC):** 2026-04-26
**Sub-phase:** acts_in_force (cross-alphabet residual sweep — chronological-first)
**Parser version:** 0.6.0-act-zambialii-2026-04-26
**Yield:** 8/8 (100%) — extends 100%-yield streak across batches 0246–0269 (24 consecutive)
**MAX_BATCH_SIZE cap:** 8 — filled exactly

## Picks

| # | Year | Act No. | Title | Alpha | Sections | Path |
|---|------|---------|-------|-------|----------|------|
| 0 | 1971 | 34 | Landlord and Tenant (Business Premises) Act, 1971 | L | 28 | HTML akn-section |
| 1 | 1980 | 4  | Excess Expenditure Appropriation (1977) Act, 1980  | E | 2  | PDF fallback   |
| 2 | 1980 | 5  | Supplementary Appropriation (1978) Act, 1980       | S | 3  | PDF fallback   |
| 3 | 1981 | 6  | Excess Expenditure Appropriation (1978) Act, 1981  | E | 2  | PDF fallback   |
| 4 | 1981 | 7  | Supplementary Appropriation (1979) Act, 1981       | S | 19 | PDF fallback   |
| 5 | 1982 | 9  | Excess Expenditure Appropriation (1979) Act, 1982  | E | 2  | PDF fallback   |
| 6 | 1982 | 10 | Supplementary Appropriation (1980) Act, 1982       | S | 2  | PDF fallback   |
| 7 | 1983 | 9  | Excess Expenditure Appropriation (1980) Act, 1983  | E | 2  | PDF fallback   |

1 parsed cleanly via akn-section HTML (1971/34); 7 used PDF fallback after HTML returned
<2 akn-sections (typical for short-form fiscal acts).
Largest section count: 1971/34 Landlord and Tenant (Business Premises) (28). Smallest:
several appropriation acts (2 sections — typical short-form fiscal acts).

## Discovery cost
- 1 robots.txt re-verify (sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193–0268)
- 1 new alphabet listing fetch — `alphabet=X&nature=act` (clearing the residual
  next-tick-plan item from batch 0268; X listing returned 0 candidates, confirming
  no Acts-in-force begin with X on zambialii.org)
- 0 other listing fetches (used cached A–Z listings under
  `raw/zambialii/_alphabets/`)

## Cross-alphabet residual sweep methodology
Built `(yr, num)` set from all `records/acts/**/*.json` (both nested
`records/acts/YYYY/` and legacy flat `records/acts/` formats). Walked the most-recent
cached listing per alphabet (C–Z) and collected `(yr, num)` candidates absent
from disk and not in the deferral list. Sorted chronologically and picked the first 8.

**Deferred (excluded from picks):**
- 1956/4 S — Service of Process and Execution of Judgments (disambiguator-deferred,
  flagged in gaps.md, awaits disambiguator-aware fetch handler)
- 1996/17 C — Constitution of Zambia (large, dedicated batch planned)
- 2006/9 C — Citizens Economic Empowerment (large, dedicated batch planned)

**Residuals carried to next tick (26 items):**
E: 1984/5, 1985/8, 1986/10, 1987/13, 1988/14, 1988/30 (and others 1989+);
S: 1983/10, 1984/6, 1985/9, 1986/9, 1987/12, 1988/15 (and others);
C: 2 non-deferred items;
L: 0 (1971/34 swept this tick);
N: 1; P: 3.

## Per-record cost
- 9 record HTML fetches (8 unique + 1 retry on 1982/9 after a sandbox 45s timeout
  during the 3:6 sub-run; HTML was already on disk so the retry was a re-fetch with
  identical sha256, no parser change)
- 7 PDF-fallback fetches (all appropriation acts had HTML with <2 akn-sections)
- All on zambialii.org under robots-declared 5s crawl-delay using 6s margin

## Today fetches (cumulative)
327 (pre-tick after batch 0268) + 1 (robots) + 1 (listing X) + 9 (records, incl. 1 retry)
+ 7 (PDF fallbacks) = **345/2000** (17.25% of daily budget)
Tokens: within budget.

## Integrity (ALL PASS)
- CHECK1a batch unique IDs: 8/8
- CHECK1b corpus presence on disk: 8/8
- CHECK2 amended_by refs resolve: 0 refs (none in batch)
- CHECK3 repealed_by refs resolve: 0 refs (none in batch)
- CHECK4 source_hash sha256 verified against raw HTML: 8/8 — under
  `raw/zambialii/act/(1971,1980,1981,1982,1983)/`
- CHECK5 required 16 fields × 8 records = 128/128 fields present
- CHECK6 cited_authorities refs resolve: 0 refs (none in batch)

## Cumulative records
acts **1016** (+8 over 1008); SIs 593 (unchanged); judgments 25 (paused per robots Disallow).

## Provenance
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- Crawl-delay: 6s (robots declared 5s; +1s margin)
- robots.txt cached: `raw/zambialii/_robots/robots-20260426T140355Z.txt`
- alphabet=X listing cached: `raw/zambialii/_alphabets/legislation-alphabet-X-20260426T140414Z.html`

## Next-tick plan
1. Continue cross-alphabet residual sweep — chronological-first 8 from carry list
   (E/S series 1983/10–1988+ supplementary/excess appropriations dominate).
2. Implement disambiguator-aware fetch handler for 1956/4 S residual.
3. OCR retry on 15-item SI backlog once tesseract is wired (deferred to host).
4. Re-verify robots.txt at start of next tick.

## Infrastructure follow-up (non-blocking)
- batch-0269 raw files (8 act HTML + 1 alphabet listing + 1 robots) plus accumulated
  batches 0192–0268 raw files awaiting host-driven B2 sync (rclone unavailable in sandbox).
  Peter to run: `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`.
- Persistent virtiofs unlink-failure warnings on `.git/objects/tmp_obj_*` and
  `.git/objects/maintenance.lock` unchanged — non-fatal across batches 0192–0269.
- SQLite snapshot drift (`corpus.sqlite` 543 records vs JSON-on-disk count) — periodic
  full rebuild expected from host.
- FTS5 vtable malformed image (`records_fts`) unchanged — non-blocking for record integrity.
