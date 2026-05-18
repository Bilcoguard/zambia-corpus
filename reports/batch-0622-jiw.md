# Batch b0622-jiw — ZMSC 2024 gap-fill (5 records)

- **Tick start**: 2026-05-13T04:02:00Z
- **Tick end**: 2026-05-13T04:02:00Z (within 20-min wall budget)
- **Worker**: judgment-ingestion-worker (JIW)
- **Priority**: (c) SCZ sweep — ZambiaLII gap survey

## Summary

| Metric | Value |
|---|---|
| Pre records / records_fts | 1923 / 1923 |
| Post records / records_fts | 1928 / 1928 |
| Records inserted | 5 |
| Records deferred | 0 |
| Fetches (this tick) | 11 (1 index + 5 HTMLs + 5 PDFs) |
| Budget consumed today | 11 / 500 |
| Bytes downloaded | ~35.5 MB |
| New registry entries | 0 (all judges pre-registered) |
| FTS5 health | PASS (pre + post) |
| CHECK1–CHECK8 | ALL PASS |
| Parser version | 0.3.2 |

## Records inserted

1. **`judgment-zm-2024-zmsc-01-kausa-mwachindalo-and-anor-v-mathews-musona-and-ors`** — [2024] ZMSC 1; APPEAL NO. 1/2021; 2024-03-20; **dismissed** (majority Musonda DCJ + Wood JS); Malila CJ **dissenting**.
   93pp customary-law / chieftaincy succession dispute (Bundabunda Soli Shamifwi chieftaincy). Majority upheld the Court of Appeal's rotation order to the Kashimbi royal family (David Musona); ordered the clan to draw up a documented family tree and rotational succession plan among the Mulonga, Tubi-Kalifu and Kashimbi royal families; each party bears own costs. Malila CJ's dissent: customary practice cannot be changed overnight by agreement among a small number of parties; matrilineal lineage of the Soli people stands.

2. **`judgment-zm-2024-zmsc-02-mabvuto-mwale-and-anor-v-the-people`** — [2024] ZMSC 2; Appeal No. 27, 28/2020; 2024-04-19; **other (mixed)**.
   17pp criminal: appeal against sentence succeeds; appeal against conviction is hereby dismissed (conviction upheld). Coram: Musonda DCJ, Kabuka JJS, Chinyama JJS.

3. **`judgment-zm-2024-zmsc-05-tarick-mwambwa-chanaika-v-zamanita-limited-and-anor`** — [2024] ZMSC 5; APPEAL NO. 018/2013; 2024-05-06; **dismissed**.
   19pp employment (Industrial Relations Court appeal). Acting allowance and salary-increase claims unsubstantiated; e-mail proposals cannot vary fundamental terms of employment; written amendment required. Coram: Malila CJ, Phiri JJS, Hamaundu JJS. Each party to bear own costs.

4. **`judgment-zm-2024-zmsc-06-kelvin-lubona-v-the-people`** — [2024] ZMSC 6; APPEAL NO. 244/2017; 2024-05-14; **allowed**.
   24pp criminal (murder). Appeal allowed; conviction and sentence quashed; appellant acquitted. Three key pieces of evidence failed admissibility — two lacked corroboration and the arresting officer's evidence was wrongly admitted; ballistic examination did not connect the firearm to the gunshot wounds. Coram: Malila CJ, Hamaundu JJS, Kaoma JJS.

5. **`judgment-zm-2024-zmsc-09-frankson-musukwa-and-ors-v-road-transport-and-safety-agency`** — [2024] ZMSC 9; Appeal No. 11 of 2021; 2024-05-16; **dismissed**.
   44pp constitutional / disability rights. No infringement of protection of the law, freedom of movement or non-discrimination established under Articles 11/22/23 of the Constitution; reliance on RTSA Act s 62 and PWD Act ss 43–44 examined and rejected. Coram: Kaoma JJS, Kajimanga JJS, Chisanga JJS. No order as to costs.

## Source

- ZambiaLII `/judgments/ZMSC/2024/` index page (#4 absent on publisher).
- All 5 source PDFs are text-layer PDFs (pdfplumber 0.11.9 extraction succeeded; no OCR required).

## Dedup

- All 5 IDs unique (CHECK5 pass).
- No `case_number` collisions in `judgments_meta`.
- No `case_name` + `date_decided` collisions.

## Judges registry

All coram judges pre-registered (no new entries this tick): Malila, Musonda, Wood, Kabuka, Chinyama, Phiri, Hamaundu, Kaoma, Kajimanga, Chisanga.

## Integrity checks

| Check | Result | Notes |
|---|---|---|
| CHECK1 | PASS | Every judgment has ≥1 judge |
| CHECK2 | PASS | All `issue_tags` non-empty (6–10 tags each) |
| CHECK3 | PASS | Outcomes from allowed enum (dismissed×3, allowed×1, other×1) |
| CHECK4 | PASS | All judges resolve in `judges_registry.yaml` |
| CHECK5 | PASS | No duplicate IDs in corpus |
| CHECK6 | PASS | All `raw_sha256` match on-disk PDFs |
| CHECK7 | PASS | No duplicate (case_name, court, date_decided) |
| CHECK8 | PASS | records=records_fts=1928 |

## Coverage update

| Court / year | Pre | Post | Delta |
|---|---|---|---|
| ZMSC 2024 | 21 | 26 | +5 |
| ZMSC overall | 95 | 100 | +5 |
| ZMCC | 87 | 87 | unchanged |
| CoA | 50 | 50 | unchanged |
| **Pool total** | **1923** | **1928** | **+5** |

ZMSC 2024 remaining corpus gaps: 11, 18, 22, 26, 28, 29, 31, 34 (8 candidates) — see recommendation below.

## Recommendation for next tick (b0623)

1. **Priority (c) ZMSC 2024 continuation**: ingest remaining 8 corpus gaps (11, 18, 22, 26, 28, 29, 31, 34). Each PDF appears to be text-layer based on file-size signature; the publisher serves consistent AKN HTML + source.pdf pairs. Estimated 17 fetches (1 dedup re-check + 8 HTMLs + 8 PDFs). Within budget.
2. **Priority (d) ZMCC 2025 gap survey**: corpus has 15 of N entries; many gaps at 5–12, 14–19, 21, 24, 28.
3. **Priority (e) ZMHC 2025 launch**: zero current coverage. Sample landmark High-Court decisions only (precedential-value gate).
4. **CoA OCR backlog (26 records)** still parked with repair-worker; no JIW action required this tick.

## Non-negotiables

- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` (honoured).
- robots.txt: ZambiaLII permits crawling under polite UA (honoured).
- Daily budget: 11 / 500 used.
- No `approvals.yaml` modification (untouched).
- No new judge registry entries (all pre-existing).
- No `corpus.sqlite` backup created this tick (pool delta +5 is small; b0613 backup remains current).
- Wall clock: ~10 min (within 20-min budget).

## Git commit

Commit pending; if FUSE EPERM on `.git/index.lock` continues (precedent since b0334), this commit will be deferred to host-side parallel-worker file sweep — same transparent commit pattern used since b0608.
