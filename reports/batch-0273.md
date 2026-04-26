# Batch 0273 - Phase 4 (acts_in_force, cross-alphabet residual sweep)

**Tick start:** 2026-04-26T16:04:10Z
**Tick end:** 2026-04-26T16:25:00Z (approx)
**Batch script:** `scripts/batch_0273.py`
**Integrity script:** `_work/integrity_0273.py`
**Parser version:** `0.6.0-act-zambialii-2026-04-26`
**User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
**Crawl-delay honoured:** 6s margin over robots.txt declared 5s

## Discovery

Re-verified `https://zambialii.org/robots.txt` at tick start.
- sha256: `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0`
- Prefix `fce67b697ee4ef44` unchanged across batches 0193 -> 0273.
- Cached at `raw/zambialii/_robots/robots-20260426T160410Z.txt`.

0 new alphabet listing fetches (all 24 A-Z listings cached;
X confirmed empty in batch 0269; Y absent from sitemap).

Per next-tick plan in batch 0272 worker.log entry, this tick re-ran a
**cross-alphabet residual sweep** against cached listings
(`raw/zambialii/legislation/alphabet-*-2026042{4,5,6}.html`) and diffed against
`records/acts/**/*.json` on disk.

Sweep result: **24 missing (yr,num) entries** found in cached listings but not
on disk.

Excluded 4 known-deferred items:
- `1996/17` Constitution of Zambia Act (alphabet=C deferred per worker.log
  batches 0192-0272)
- `2006/9` Citizens Economic Empowerment Act (alphabet=C deferred per
  worker.log batches 0192-0272)
- `2000/8` Excess Expenditure Appropriation (1995) Act -- OCR backlog
  (scanned-image PDF, 0 chars extracted in batch 0272)
- `2000/16` Excess Expenditure Appropriation (1997) Act -- OCR backlog
  (scanned-image PDF, 0 chars extracted in batch 0272)

Picked 8 chronologically earliest of the 20 remaining. All 8 verified against
cached `alphabet-A-20260425.html` with exact-title and exact-year/number
checks (no fabrication; per BRIEF non-negotiable #1). Filter cross-checked
(yr,num) against `records/acts/**/*.json` -> all 8 confirmed not on disk
(avoided silent overwrite per BRIEF non-negotiable #4).

## Picks (8 / MAX_BATCH_SIZE=8)

| # | yr/num | alpha | Title | Sections | Source |
|---|--------|-------|-------|----------|--------|
| 1 | 1964/36 | A | Apprenticeship Act, 1964 | 28 | HTML primary |
| 2 | 1980/9 | A | Appropriation Act, 1980 | 2 | PDF fallback |
| 3 | 1981/12 | A | Appropriation Act, 1981 | 2 | PDF fallback |
| 4 | 1982/15 | A | Appropriation Act, 1982 | 2 | PDF fallback |
| 5 | 1983/14 | A | Appropriation Act, 1983 | 28 | PDF fallback |
| 6 | 1984/13 | A | Appropriation Act, 1984 | 2 | PDF fallback |
| 7 | 1985/16 | A | Appropriation Act, 1985 | 2 | PDF fallback |
| 8 | 1986/12 | A | Appropriation Act, 1986 | 2 | PDF fallback |

Yield: **8/8 (100%)** -- extends 100%-yield streak across batches 0246-0273
(28 consecutive at 100%).

## Records written

```
records/acts/1964/act-zm-1964-036-apprenticeship-act-1964.json
records/acts/1980/act-zm-1980-009-appropriation-act-1980.json
records/acts/1981/act-zm-1981-012-appropriation-act-1981.json
records/acts/1982/act-zm-1982-015-appropriation-act-1982.json
records/acts/1983/act-zm-1983-014-appropriation-act-1983.json
records/acts/1984/act-zm-1984-013-appropriation-act-1984.json
records/acts/1985/act-zm-1985-016-appropriation-act-1985.json
records/acts/1986/act-zm-1986-012-appropriation-act-1986.json
```

## Raw cache

```
raw/zambialii/act/1964/1964-036.html
raw/zambialii/act/1980/1980-009.{html,pdf}
raw/zambialii/act/1981/1981-012.{html,pdf}
raw/zambialii/act/1982/1982-015.{html,pdf}
raw/zambialii/act/1983/1983-014.{html,pdf}
raw/zambialii/act/1984/1984-013.{html,pdf}
raw/zambialii/act/1985/1985-016.{html,pdf}
raw/zambialii/act/1986/1986-012.{html,pdf}
```
1964/36 produced enough HTML sections so PDF fallback was not needed.
The seven Appropriation Acts triggered the standard `<2 akn-sections` PDF
fallback path. Raw HTML/PDF files retained locally for re-verify; awaits
host-driven B2 sync.

## Integrity (all PASS)

- CHECK1a batch unique IDs: 8/8 unique
- CHECK1b corpus presence on disk: 8/8
- CHECK2 amended_by refs: 0 (none to resolve)
- CHECK3 repealed_by refs: 0 (none to resolve)
- CHECK4 source_hash sha256 verified: 8/8 against
  `raw/zambialii/act/(1964,1980,1981,1982,1983,1984,1985,1986)/`
- CHECK5 required 16 fields x 8 = 128/128
- CHECK6 cited_authorities refs: 0

## Costs (this tick)

- Robots reverify: 1 (~2 KB)
- Record HTML fetches: 8 (~7 KB - 141 KB each)
- PDF fallbacks: 7 (672 KB - 1472 KB each)
- Total tick fetches: 16
- Daily total after tick: **417 / 2000** (20.85% of daily budget)
- Tokens within daily budget.

## Phase 4 status

Phase 4 remains **incomplete** per `approvals.yaml` (worker does not flip the
flag). Residuals carried forward to next tick:

- 12 alphabet=A Appropriation Acts (1987-1999 fiscal series)
- 1 S residual: 1956/4 Service of Process and Execution of Judgments
  (disambiguator-deferred)
- 2 alphabet=C deferred: 1996/17 Constitution of Zambia + 2006/9 Citizens
  Economic Empowerment
- OCR backlog: 17 items (no change from batch 0272; awaits host-side
  tesseract wiring)

## Next-tick plan

(a) Continue alphabet=A Appropriation Act residual sweep -- 8 more chronological
    (1987/15, 1988/19, 1989/34, 1990/44, 1992/17, 1993/22, 1994/5, 1995/1).
(b) Re-verify robots.txt at tick start (sha256 unchanged-prefix expectation
    `fce67b697ee4ef44`).
(c) Implement disambiguator-aware fetch handler for 1956/4 (deferred).
(d) OCR retry on 17-item backlog once tesseract is wired (deferred to host).

## Infrastructure notes (non-blocking)

- `rclone` not available in sandbox -- B2 sync (step 8) deferred to host.
  Peter to run: `rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`.
- `corpus.sqlite` not touched this batch (snapshot drift preserved per
  established workflow).
- Persistent virtiofs unlink-failure warnings on `.git/objects/maintenance.lock`
  and `.git/objects/tmp_obj_*` non-fatal (workaround stable across batches
  0192-0273).
