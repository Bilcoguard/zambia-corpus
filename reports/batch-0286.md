# Batch 0286 Report

**Phase:** 4 — bulk (acts_in_force, chronological-first sweep)
**Tick:** 2026-04-26 (UTC) — scheduled tick, 30-min cadence
**Yield:** 8/8 (100%)
**Wall-clock:** ~6 min
**Parser version:** 0.6.0-act-zambialii-2026-04-26

## Picks (8 chronological from inherited pool)

| Year/Num | Title | Alpha | Status | Sections |
|---|---|---|---|---|
| 2017/22 | Appropriation Act, 2017 | A | ok | 2 |
| 2018/1  | Public Finance Management Act, 2018 | P | ok | 152 |
| 2018/8  | Credit Reporting Act, 2018 | C | ok | 99 |
| 2018/10 | Supplementary Appropriation (2018) Act, 2018 | S | ok | 3 |
| 2018/22 | Appropriation Act, 2018 | A | ok | 2 |
| 2018/23 | Supplementary Appropriation (2018) (No. 2) Act, 2018 | S | ok | 2 |
| 2019/8  | Supplementary Appropriation (2019) Act, 2019 | S | ok | 2 |
| 2019/17 | Supplementary Appropriation (2019) (No. 2) Act, 2019 | S | ok | 2 |

Of the 8 picks, 6 are fiscal-series (Appropriation/Supplementary) which fell through to the PDF fallback path (HTML akn-section count <2 each). Two substantive non-fiscal acts — Public Finance Management Act 2018 (152 sections) and Credit Reporting Act 2018 (99 sections) — were ingested via the HTML akn-section parser, not PDF fallback. All PDFs were under MAX_PDF_BYTES (4.5 MB).

## Integrity

- CHECK1a: 8/8 batch unique — PASS
- CHECK1b: 8/8 corpus presence — PASS
- CHECK2:  0 amended_by refs — PASS
- CHECK3:  0 repealed_by refs — PASS
- CHECK4:  8/8 source_hash sha256 verified vs raw HTML — PASS
- CHECK5:  128/128 required fields present — PASS
- CHECK6:  0 cited_authorities refs — PASS

## Provenance

Source: zambialii.org (`/akn/zm/act/{yr}/{num}` HTML + `source.pdf` fallback)
User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
Crawl-delay: 6s (1s margin over robots.txt 5s)
robots.txt sha256: `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` (unchanged)

## Pool

- Inherited from batch 0285: 30 items
- Processed this tick: 8
- Remaining for batch 0287: 22 (next: 2019/18 Appropriation Act, 2019)

## Budget

- Today (2026-04-26 UTC) fetches at tick start: 596/2000 (~29.8%)
- Today (2026-04-26 UTC) fetches at tick end:   ~612/2000 (~30.6%)

## B2 sync

Deferred to host (rclone not available in sandbox).

## Phase status

Phase 4 remains incomplete per `approvals.yaml`. Worker does not flip the flag.
