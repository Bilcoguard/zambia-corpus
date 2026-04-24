# Batch 0200 — Phase 4 sis_employment rotation opener

- **Tick start:** 2026-04-24T22:02Z
- **Tick complete:** 2026-04-24T22:10Z
- **Phase:** phase_4_bulk
- **Sub-phase rotation:** sis_tax → **sis_employment** (priority_order item 4)
- **Trigger:** per batch-0199 next-tick plan — rotate to sis_employment via alphabet=E (Employment Code Act derivatives) + alphabet=M (Minimum Wages orders) + parent-Act back-reference probe on /akn/zm/act/2019/3

## Targets (4 attempted, 2 written)

| Year/No. | Title | Parent Act | Status |
|---|---|---|---|
| 2022/013 | Minimum Wages and Conditions of Employment (Truck and Bus Drivers) (Amendment) Order, 2022 | Min Wages & Conditions of Employment Act (Cap 276 → 1982/25) | `pdf_parse_empty` (image-only scan; OCR deferred) |
| 2018/035 | Industrial and Labour Relations (Fees) Regulations, 2018 | Industrial and Labour Relations Act 1993/27 | **ok** (11 sections) |
| 2019/029 | Employment Code Act (Commencement) Order, 2019 | Employment Code Act 2019/3 | **ok** (1 section) |
| 2000/105 | Worker's Compensation Act 1999 (Commencement) Order (parent-Act back-ref'd) | Workers' Compensation Act 1999/10 | `http_404` (AKN slug absent; no alternate located) |

## Discovery

Cached from prior batches: alphabet E/I/M. Fresh discovery this tick:
- `robots.txt` re-verification — sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0199
- `alphabet=F` — Factories Act derivatives — 3 hits, all in HEAD
- `alphabet=W` — Workers Compensation — 2 hits, all in HEAD
- `alphabet=L` — Labour / Local Authorities — 1 employment-class hit, in HEAD
- `alphabet=N` — NAPSA / National Pension — 5 hits, all in HEAD
- parent-act `/akn/zm/act/1982/25` (Min Wages & Conditions of Employment Act) — 0 SI links rendered
- parent-act `/akn/zm/act/1993/27` (Industrial and Labour Relations Act) — 0 SI links rendered
- parent-act `/akn/zm/act/1999/10` (Worker's Compensation Act) — 1 NEW: 2000/105 (see above: 404 on ingest)
- parent-act `/akn/zm/act/2019/3` (Employment Code Act) — 1 NEW: 2019/29 (ingested ok)

## Fetch accounting

- Discovery fetches this tick: 9 (robots.txt + 4 alphabet pages + 4 parent-act pages)
- Ingest fetches this tick: 7 (4 HTML GETs — 1 404; 3 PDF GETs of successful HTMLs)
- Total batch fetches: 16
- Cumulative today (2026-04-24 UTC): ~346 + 16 = ~362/2000 (18.1%). Well inside daily budget.

## Integrity

All CHECK1-5 pass on the 2 written records:
- CHECK1 no duplicate IDs in records/sis/ — PASS
- CHECK2 no (year, number) slot collision — PASS
- CHECK3 on-disk raw sha256 matches source_hash — PASS (both)
- CHECK4 amended_by / repealed_by empty — PASS
- CHECK5 required fields present — PASS

## Gaps logged (2)

- `si/2022/013` — pdf_parse_empty (image-only scan; OCR backfill deferred as with 2022/002 in batch-0197)
- `si/2000/105` — http_404 (AKN slug absent; title referenced on parent-act 1999/10 back-ref page but no resolvable URL)

## Rotation decision for next tick

Yield on sis_employment this tick = 2 (<3 threshold per batch-0199 rule). **Rotate to sis_data_protection** (priority_order item 6) next tick via Data Protection Act 2021/3 derivative SIs (Cyber transitional SIs, commencement orders not yet in corpus). If yield remains <3, rotate further to sis_corporate (priority_order item 2) via Companies Act 2017/10 derivatives.

## Policy compliance

- Raw html/pdf (2 HTML + 2 PDF for successful ingests) remain under `raw/zambialii/si/{year}/` on disk, **not** force-added to git (per batch-0190 `.gitignore` policy).
- Robots.txt Disallow on `/akn/zm/judgment/` + `/akn/zm/officialGazette/` still in force; all this tick's URLs under permitted `/akn/zm/act/` + `/legislation/subsidiary`.
- Worker identity: `kwlp-worker <peter@bilcoguard.com>`.
