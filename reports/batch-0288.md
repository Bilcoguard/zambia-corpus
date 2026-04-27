# Batch 0288 Report

**Phase:** 4 — bulk (acts_in_force, chronological-first sweep)
**Tick:** 2026-04-27 (UTC) — scheduled tick, 30-min cadence
**Yield:** 7/8 (87.5%)
**Wall-clock:** ~5 min
**Parser version:** 0.6.0-act-zambialii-2026-04-26

## Picks (8 chronological from inherited pool)

| Year/Num | Title | Alpha | Status | Sections |
|---|---|---|---|---|
| 2021/53 | Appropriation Act, 2021 | A | ok | 3 |
| 2022/7  | Supplementary Appropriation (2022) Act, 2022 | S | ok | 3 |
| 2022/30 | Appropriation Act, 2022 | A | ok | 2 |
| 2023/10 | Supplementary Appropriation (2023) Act, 2023 | S | ok | 2 |
| 2023/18 | Public-Private Partnership Act, 2023 | P | ok | 162 |
| 2023/29 | Appropriation Act, 2023 | A | ok | 2 |
| 2024/9  | Supplementary Appropriation Act, 2024 | S | deferred_multi_act_gazette | — |
| 2024/20 | Supplementary Appropriation (2024) (No. 2) Act, 2024 | S | ok | 3 |

Of the 7 successful picks, 6 are fiscal-series (Appropriation/Supplementary) that fell through to the PDF fallback path (HTML akn-section count <2 each). One substantive non-fiscal Act — Public-Private Partnership Act, 2023 (162 sections) — was ingested via the HTML akn-section parser, not PDF fallback.

The 8th pick (Act No. 9 of 2024 — Supplementary Appropriation Act, 2024) was DEFERRED. The PDF fetched from zambialii.org is a multi-Act Government Gazette bundle (Vol. LX, No. 7,631, 16th August 2024) containing Acts 4–12 of 2024 in sequence; the naive top-level PDF section regex pulled 237 sections that overwhelmingly belong to OTHER Acts in that bundle (Human Rights Commission Act, ZIALE Amendment, Matrimonial Causes Amendment, etc.) rather than to the Supplementary Appropriation Act itself. The misfired record was REMOVED before commit (no fabrication committed); the corresponding `provenance.log` line was rolled back; raw HTML and raw PDF are retained for traceability and re-ingestion under a future Act-boundary-aware parser. Logged in `gaps.md` and added to a NEW **multi-act-gazette retry queue** (1 item).

## Integrity

- CHECK1a: 7/7 batch unique — PASS
- CHECK1b: 7/7 corpus presence — PASS
- CHECK2:  0 amended_by refs — PASS
- CHECK3:  0 repealed_by refs — PASS
- CHECK4:  7/7 source_hash sha256 verified vs raw HTML — PASS
- CHECK5:  112/112 required fields present — PASS
- CHECK6:  0 cited_authorities refs — PASS

## Provenance

Source: zambialii.org (`/akn/zm/act/{yr}/{num}` HTML + `source.pdf` fallback)
User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
Crawl-delay: 6s (1s margin over robots.txt 5s)
robots.txt sha256: `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` (unchanged from b0193..0287)

## Pool

- Inherited from batch 0287: 14 items
- Processed this tick: 8 (7 ok + 1 deferred to multi-act-gazette retry queue)
- Remaining for batch 0289: 6 (next: 2025/3 Cyber Security Act, 2025)

## Budget

- Today (2026-04-27 UTC) fetches at tick start: 0/2000 (fresh day)
- Today (2026-04-27 UTC) fetches at tick end:   ~16/2000 (~0.8%)

## SQLite

Update of `corpus.sqlite` deferred — same disposition as batches 0240+ (FTS5 vtable in broken state, journal held open). JSON record files, raw HTML/PDF, `provenance.log` and `costs.log` are the authoritative durable artefacts. SQLite index rebuild belongs in Phase 5 (retrieval API) which remains `approved: false`.

## B2 sync

Deferred to host (rclone not available in sandbox).

## Phase status

Phase 4 remains incomplete per `approvals.yaml`. Worker does not flip the flag.
