# Batch 0188 — Phase 4, case_law_scz sub-phase

**Phase:** phase_4_bulk  
**Sub-phase:** case_law_scz  
**Batch:** 0188  
**Started:** 2026-04-24T16:03:52Z  
**Completed:** 2026-04-24T16:04:56Z  
**Fetches used:** 8 (4 AKN HTML + 4 PDF fallback)  
**Records written:** 4 / 4  
**Integrity:** CHECK1 unique IDs · CHECK2 no HEAD slot collision · CHECK3 source_hash matches on-disk raw · CHECK4 no unresolved cross-refs · CHECK5 required fields — **ALL PASS**  
**Gaps logged:** 0

## Records

- **[2025] ZMSC 30** — SA Airlink (PTY) Limited v Zambia Skyways Limited and Ors (APPEAL NO. 10/2023) [2025] ZMSC 30 (31 December 2025) (18 paragraphs; PDF 11310547 bytes; sha256=59914f96416fd627…) → `records/judgments/zmsc/2025/judgment-zm-2025-zmsc-30-sa-v-zambia.json`
- **[2025] ZMSC 29** — Rephidim Institute Limited v Attorney General (SCZ/08/08/2025) [2025] ZMSC 29 (12 December 2025) (26 paragraphs; PDF 5729905 bytes; sha256=cea3ff3c6dccd506…) → `records/judgments/zmsc/2025/judgment-zm-2025-zmsc-29-rephidim-v-attorney.json`
- **[2025] ZMSC 27** — Jonathan Van Blerk v The Attorney General and Ors (SCZ NO. SCZ/07/27/2024) [2025] ZMSC 27 (2 October 2025) (13 paragraphs; PDF 3443440 bytes; sha256=8b6bf246c9172e40…) → `records/judgments/zmsc/2025/judgment-zm-2025-zmsc-27-jonathan-v-the.json`
- **[2025] ZMSC 25** — Cosmas Mweemba and Ors v Chikankata District Council and Anor (SCZ/07/05/2024) [2025] ZMSC 25 (19 September 2025) (6 paragraphs; PDF 1496376 bytes; sha256=94dfffe61aa2fd35…) → `records/judgments/zmsc/2025/judgment-zm-2025-zmsc-25-cosmas-v-chikankata.json`

## Discovery channel

ZambiaLII neutral-citation AKN pattern (`/akn/zm/judgment/zmsc/{year}/{num}/eng@{date}`), 
with date slugs resolved from the cached index page 
`raw/zambialii/judgments/zmsc/zmsc-index-page-1-20260424.html` (no new discovery 
fetch needed this tick).

## Ingestion notes

Sliced into two sub-ticks (0:2 then 2:4) to fit the 45 s sandbox bash ceiling
with a 6 s zambialii crawl delay per request. Rate limit honoured (5 s per
robots + 1 s margin). Parser version 0.5.0. User-Agent 
`KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.

## Sub-phase status after this batch

case_law_scz: 9 records (5 prior + 4 this batch)  
- 2026: 5 (batch-3 pilot + 4 from batch 0187)
- 2025: 4 (this batch: ZMSC 30, 29, 27, 25)

## Next tick plan

Continue case_law_scz with 2025 mid-corridor (zmsc/2025/24, 23, 22, 21 per
cached index). After case_law_scz reaches ~13 records, rotate to 
sis_data_protection (priority_order item 6).

B2 sync deferred to host — rclone not available in sandbox.
