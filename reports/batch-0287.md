# Batch 0287 Report

**Phase:** 4 — bulk (acts_in_force, chronological-first sweep)
**Tick:** 2026-04-26 (UTC) — scheduled tick, 30-min cadence
**Yield:** 8/8 (100%)
**Wall-clock:** ~6 min
**Parser version:** 0.6.0-act-zambialii-2026-04-26

## Picks (8 chronological from inherited pool)

| Year/Num | Title | Alpha | Status | Sections |
|---|---|---|---|---|
| 2019/18 | Appropriation Act, 2019 | A | ok | 2 |
| 2020/8  | Public Procurement Act, 2020 | P | ok | 114 |
| 2020/9  | Excess Expenditure Appropriation (2020) Act, 2020 | E | ok | 2 |
| 2020/17 | Supplementary Appropriation (2020) Act, 2020 | S | ok | 2 |
| 2020/26 | Appropriation Act, 2020 | A | ok | 2 |
| 2021/2  | Cyber Security and Cyber Crimes Act, 2021 | C | ok | 90 |
| 2021/42 | Excess Expenditure Appropriation (2021) Act, 2021 | E | ok | 2 |
| 2021/52 | Supplementary Appropriation (2021) Act, 2021 | S | ok | 2 |

Of the 8 picks, 6 are fiscal-series (Appropriation/Excess Expenditure/Supplementary) which fell through to the PDF fallback path (HTML akn-section count <2 each). Two substantive non-fiscal acts — Public Procurement Act 2020 (114 sections) and Cyber Security and Cyber Crimes Act 2021 (90 sections) — were ingested via the HTML akn-section parser, not PDF fallback. All PDFs were under MAX_PDF_BYTES (4.5 MB).

## Integrity

- CHECK1a: 8/8 batch unique — PASS
- CHECK1b: 8/8 corpus presence (this batch's IDs unique in corpus) — PASS
- CHECK2:  0 amended_by refs — PASS
- CHECK3:  0 repealed_by refs — PASS
- CHECK4:  8/8 source_hash sha256 verified vs raw HTML — PASS
- CHECK5:  104/104 required fields present — PASS
- CHECK6:  0 cited_authorities refs — PASS

## Provenance

Source: zambialii.org (`/akn/zm/act/{yr}/{num}` HTML + `source.pdf` fallback)
User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
Crawl-delay: 6s (1s margin over robots.txt 5s)
robots.txt sha256: `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` (unchanged)

## Pool

- Inherited from batch 0286: 22 items
- Processed this tick: 8
- Remaining for batch 0288: 14 (next: 2021/53 Appropriation Act, 2021)

## Budget

- Today (2026-04-26 UTC) fetches at tick start: 612/2000 (~30.6%)
- Today (2026-04-26 UTC) fetches at tick end:   624/2000 (~31.2%)

## SQLite

Update of `corpus.sqlite` deferred. The `records_fts` FTS5 vtable is in a broken state ("vtable constructor failed"), and the journal (`corpus.sqlite-journal`) is held open in the sandbox preventing recovery. Recent batches (~0240+) have followed the same deferral pattern. JSON record files, raw HTML/PDF, provenance.log and costs.log are the authoritative durable artefacts. The SQLite index can be rebuilt cleanly under Phase 5 (retrieval API), which remains `approved: false`.

## B2 sync

Deferred to host (rclone not available in sandbox).

## Phase status

Phase 4 remains incomplete per `approvals.yaml`. Worker does not flip the flag.
