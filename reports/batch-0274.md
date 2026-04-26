# Phase 4 Batch 0274 — acts_in_force chronological-first across all alphabets

**Tick start:** 2026-04-26T16:33:31Z (UTC)  
**Tick complete (ingest):** 2026-04-26T16:42:00Z (UTC)  
**Phase:** 4 (bulk ingest) — `approved: true`, `complete: false`  
**Sub-phase:** `acts_in_force`  
**Scope:** Cross-alphabet residual sweep — alphabet=A Appropriation Act series 1987-1995  
**Source:** zambialii.org (robots.txt re-verified, sha256 prefix `fce67b697ee4ef44`, crawl-delay 5s honoured at 6s margin)

## Picks (8 / MAX_BATCH_SIZE=8)

Inherited residual queue from batch 0273 worker.log entry: 12 alphabet=A Appropriation
Acts spanning 1987-1999. Picked 8 chronologically earliest. Titles verified against cached
`raw/zambialii/legislation/alphabet-A-20260425.html` with exact-match in `<a>` text and
`Act <num> of <yr>` citation cell (no fabrication per BRIEF #1). Pre-flight on-disk check:
all 8 confirmed not present (avoided silent overwrite per BRIEF #4).

| # | yr/num | Title | id | Sections | Source |
|---|---|---|---|---|---|
| 0 | 1987/15 | Appropriation Act, 1987 | act-zm-1987-015-appropriation-act-1987 | 34 | HTML primary (akn-sections >=2) |
| 1 | 1988/19 | Appropriation Act, 1988 | act-zm-1988-019-appropriation-act-1988 |  1 | PDF fallback (HTML <2 sections) |
| 2 | 1989/34 | Appropriation Act, 1989 | act-zm-1989-034-appropriation-act-1989 |  2 | PDF fallback |
| 3 | 1990/44 | Appropriation Act, 1990 | act-zm-1990-044-appropriation-act-1990 |  3 | PDF fallback |
| 4 | 1992/17 | Appropriation Act, 1992 | act-zm-1992-017-appropriation-act-1992 |  2 | PDF fallback |
| 5 | 1993/22 | Appropriation Act, 1993 | act-zm-1993-022-appropriation-act-1993 |  1 | PDF fallback |
| 6 | 1994/5  | Appropriation Act, 1994 | act-zm-1994-005-appropriation-act-1994 |  2 | PDF fallback |
| 7 | 1995/1  | Appropriation Act, 1995 | act-zm-1995-001-appropriation-act-1995 |  3 | PDF fallback |

**Yield:** 8 / 8 (100%) — extends 100%-yield streak across batches 0246-0274 (29 consecutive at 100%).

## Integrity check (pre-commit)

```
PASS CHECK1a - 8 unique IDs in batch
PASS CHECK1b - 8/8 present in corpus
PASS CHECK2/3 - amended_by/repealed_by 0 refs to resolve
PASS CHECK4 - sha256 verified 8/8 against raw HTML
PASS CHECK5 - 16x8=128 required fields present
PASS CHECK6 - cited_authorities 0 refs
ALL CHECKS PASS
```

## Discovery & cost

- 1 robots.txt re-verify (sha256 `fce67b6...8f0`, unchanged from batches 0193-0273)
- 0 alphabet listing fetches (all 24 A-Z listings cached; 26th day of cache)
- 8 record HTML fetches + 7 PDF fallback fetches (1987/15 had >=2 HTML akn-sections so PDF skipped)

Pre-tick fetches: 417/2000 (20.85%). Post-tick: 417 + 1 robots + 8 HTML + 7 PDF = **433/2000 (21.65%)**.

## Reserved residuals carried to next tick

- **alphabet=A residuals:** 4 remaining Appropriation Acts: 1996/13, 1997/13, 1998/3, 1999/3
- **alphabet=S:** 1956/4 Service of Process and Execution of Judgments (disambiguator-deferred)
- **alphabet=C:** 1996/17 Constitution of Zambia + 2006/9 Citizens Economic Empowerment (deferred large items)
- **OCR backlog:** 17 items (act/2000/8 + act/2000/16 + 15 prior; tesseract not wired in sandbox)

## Cumulative records (worker counter)

- acts: 1066 (+8 over 1058)
- SIs: 539 (unchanged from batch 0252)
- judgments: 25 (paused per robots Disallow on /akn/zm/judgment/)

## Infrastructure notes (non-blocking)

- B2 sync deferred to host (rclone unavailable in sandbox); peter to run `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`
- Persistent virtiofs unlink-failure warnings on `.git/objects/tmp_obj_*` non-fatal (workaround stable across batches 0192-0274)
- corpus.sqlite snapshot drift unchanged this batch (periodic full rebuild expected from host)
