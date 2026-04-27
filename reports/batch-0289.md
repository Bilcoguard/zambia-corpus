# Batch 0289 Report

**Phase:** 4 — bulk (acts_in_force, chronological-first sweep)
**Tick:** 2026-04-27 (UTC) — scheduled tick, 30-min cadence
**Yield:** 6/6 (100%)
**Wall-clock:** ~7 min
**Parser version:** 0.6.0-act-zambialii-2026-04-26

## Picks (6 from inherited 6-item pool — full sweep)

| Year/Num | Title | Alpha | Status | Sections | Path |
|---|---|---|---|---|---|
| 2024/29 | Appropriation Act, 2024 | A | ok | 3 | PDF fallback (fiscal-series) |
| 2025/3  | Cyber Security Act, 2025 | C | ok | 73 | HTML akn-section parser |
| 2025/4  | Cyber Crimes Act, 2025 | C | ok | 33 | HTML akn-section parser |
| 2025/9  | Supplementary Appropriation (2025) Act, 2025 | S | ok | 3 | PDF fallback (fiscal-series) |
| 2025/14 | Cotton Act, 2025 | C | ok | 52 | HTML akn-section parser |
| 2025/28 | Appropriation Act, 2025 | A | ok | 3 | PDF fallback (fiscal-series) |

All 6 picks ingested cleanly. Three substantive non-fiscal Acts (Cyber Security, Cyber Crimes, Cotton) parsed via HTML akn-section parser; three fiscal-series Acts (two Appropriation, one Supplementary Appropriation) parsed via PDF fallback after HTML akn-section count was <2.

Year-matching content verified by spot-check: 2024/29 sec 2 references "two hundred and seventeen billion … kwacha" (correct FY2024 aggregate); 2025/9 sec 2 references "thirty-three billion, five hundred seventy-seven million … kwacha" (correct supplementary 2025 aggregate); 2025/28 sec 2 references "two hundred and fifty-three billion … kwacha" (correct FY2025 aggregate). 2025/3 Cyber Security Act repeals the Cyber Security and Cyber Crimes Act, 2021 (per its repeal section); 2025/4 Cyber Crimes Act references the Electronic Communications and Transactions Act, 2021 (Act No. 4 of 2021) by citation. 2025/14 Cotton Act repeals the Cotton Act, 2005.

This batch added a new defensive guard relative to batches 0269..0288: for fiscal-series Acts (alpha A or S, slug contains "appropriation"), if the PDF parser returns more than 30 sections, the record is NOT written and the pick is deferred to the **multi-act-gazette retry queue**. None of the three fiscal picks in this batch tripped the guard (all returned 3 sections each, the canonical fiscal pattern).

## Integrity

- CHECK1a: 6/6 batch unique — PASS
- CHECK1b: 6/6 corpus presence — PASS
- CHECK2:  0 amended_by refs — PASS
- CHECK3:  0 repealed_by refs — PASS
- CHECK4:  6/6 source_hash sha256 verified vs raw HTML — PASS
- CHECK5:  96/96 required fields present — PASS
- CHECK6:  0 cited_authorities refs — PASS

## Provenance

Source: zambialii.org (`/akn/zm/act/{yr}/{num}` HTML + `source.pdf` fallback)
User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
Crawl-delay: 6s (1s margin over robots.txt 5s)
robots.txt sha256: `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` (unchanged from b0193..0288, re-verified at tick start)

## Pool

- Inherited from batch 0288: 6 items (2024/29, 2025/3, 2025/4, 2025/9, 2025/14, 2025/28)
- Processed this tick: 6 (all ok; 0 deferred)
- Remaining for batch 0290: 0 in this inherited tail. **Pool refresh required next tick** — sweep `https://zambialii.org/akn/zm/act/?page=N` listing pages for newly published 2025/2026 Acts not yet in corpus, plus revisit any prior-year gaps not yet absorbed via existing `_work/batch_NNNN_pool_refreshed.json` machinery.

## Budget

- Today (2026-04-27 UTC) fetches at tick start: ~16/2000 (~0.8%) — last batch 0288 closed at this level
- Today (2026-04-27 UTC) fetches at tick end:   ~28/2000 (~1.4%) — 6 HTMLs + 3 fiscal PDFs + 1 robots.txt + 2 unsuccessful PDF probes
- Tokens within budget

## Cumulative

- Acts on disk: 1169 records under `records/acts/**/*.json` (+6 over 1163 b0288 baseline)
- Multi-act-gazette retry queue: still 1 item (2024/9 — unchanged)
- Oversize-pdf queue: 6 items (2002/6, 2005/21, 2008/5, 2009/10, 2009/30, 2012/16 — unchanged)
- OCR section-tolerant retry queue: 6 items (1988/32, 1994/40, 1995/33, 2004/6, 2008/9, 2009/7 — unchanged)
- OCR backlog: 18 items (unchanged)

## SQLite

Update of `corpus.sqlite` deferred — same disposition as batches 0240+ (FTS5 vtable in broken state, journal held open). JSON record files, raw HTML/PDF, `provenance.log` and `costs.log` are the authoritative durable artefacts. SQLite index rebuild belongs in Phase 5 (retrieval API) which remains `approved: false`.

## B2 sync

Deferred to host (rclone not available in sandbox).

## Phase 4 status

`approvals.yaml -> phase_4_bulk -> complete` remains `false`. Worker does NOT flip the flag. Sub-phase `acts_in_force` has now exhausted the chronological-first sweep through 2025; a fresh listing-page enumeration is needed to confirm whether any 2025/2026 Acts have been published since the last refresh.
