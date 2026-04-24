# Batch 0187 Report

**Phase:** phase_4_bulk  
**Sub-phase:** case_law_scz (priority_order item 5 — rotation from sis_employment per batch 0186 plan)  
**Started:** 2026-04-24T15:33:00Z  
**Completed:** 2026-04-24T15:37:00Z  
**Records written:** 4  
**Fetches used (ingest):** 8 (4 AKN HTML + 4 source.pdf)  
**Discovery fetches (this tick):** 3 (ZMSC index page 1 + 2 low-value probes /judgments/ + /judgments/SCZ/)  
**Cumulative fetches today:** ~192 / 2000 (9.6% of daily budget)

## Targets ingested

| URL | Record | Citation | Paragraphs | PDF bytes |
|-----|--------|----------|-----------:|----------:|
| /akn/zm/judgment/zmsc/2026/10/eng@2026-04-17 | judgment-zm-2026-zmsc-10-first-v-zubao | [2026] ZMSC 10 | 13 | 224,515 |
| /akn/zm/judgment/zmsc/2026/7/eng@2026-03-13 | judgment-zm-2026-zmsc-07-munir-v-attorney | [2026] ZMSC 7 | 11 | 3,195,336 |
| /akn/zm/judgment/zmsc/2026/4/eng@2026-03-10 | judgment-zm-2026-zmsc-04-ventriglia-v-finance | [2026] ZMSC 4 | 39 | 3,028,195 |
| /akn/zm/judgment/zmsc/2026/1/eng@2026-01-29 | judgment-zm-2026-zmsc-01-kapsch-v-intelligent | [2026] ZMSC 1 | 17 | 179,957 |

Targets deliberately skipped in this batch:
- **zmsc/2026/9** — Kapopo Mutele Patel v The People — deferred (criminal; SCZ judgments catalogue priorities are civil / corporate / tax / employment for KWLP retrieval).
- **zmsc/2026/8** — Konkola Copper Mines v AG — duplicates the batch-3 pilot record `judgment-zm-2026-scz-09-konkola-v-ag` under the docket number. The pilot used the appeal number (09/2024) rather than the ZambiaLII neutral citation; reconciliation is a follow-up editorial task, not a batch-0187 ingest.
- **zmsc/2026/6** — Ventriglia (second Ventriglia order on the same day) — mirror of 2026/4; ingest both only after human review to avoid doubling a single controversy.
- **zmsc/2026/3, 2026/2** — Manoj Patel + Standard Chartered — queued for next case_law_scz tick.

## Discovery

- `GET https://zambialii.org/judgments/ZMSC/` → 200, 427 KB, 50 judgment links surfaced (2026–2018 descending).
- `GET https://zambialii.org/judgments/SCZ/` → 404 (legacy alias; not used).
- `GET https://zambialii.org/akn/zm/judgment/` → 404 (no raw akn index).
- Raw index archived to `raw/zambialii/judgments/zmsc/zmsc-index-page-1-20260424.html`.
- 9 entries for 2026 + 12 for 2025 + 29 for earlier years across page 1 — additional pages (2–10) available via `?page=N` parameter observed in the index DOM. Queued for next tick.

## Integrity checks (batch-scoped, all 4 records)

- **CHECK1 unique IDs:** PASS — no intra-batch or HEAD-collision for the four new judgment IDs.
- **CHECK2 amended_by / repealed_by:** PASS — judgments carry no in-force cross-refs (N/A).
- **CHECK3 cited_authorities:** PASS — cited_authorities left empty for this batch (citation extraction deferred; parser does not fabricate).
- **CHECK4 source_hash matches raw:** PASS — sha256 of on-disk `raw/zambialii/judgments/zmsc/2026/*.pdf` verified against `source_hash` for all four records.
- **CHECK5 required fields:** PASS — id / type / jurisdiction / title / citation / court / delivery_date / parties / paragraphs / source_url / source_hash / fetched_at / parser_version all non-empty.

## Provenance

Every record written carries:
- `source_url` — direct ZambiaLII `/source.pdf` URL (primary)
- `source_hash` — `sha256:<hex>` of the fetched PDF bytes
- `fetched_at` — UTC ISO-8601 timestamp at the moment of the HTTP GET
- `parser_version` — 0.5.0
- `alternate_sources[]` — the AKN HTML page (`role: discovery_and_title`) with its own sha256

`costs.log` and `provenance.log` appended with one line per fetch (8 lines each for this batch).

## Gaps

None this batch. No scanned-image PDFs encountered; all four source PDFs carried native text layers and parsed to paragraph structure without OCR.

## Operational notes

- Sandbox bash-tool 45 s hard ceiling confirmed again — batch sliced 2+2 via `--slice=0:2` / `--slice=2:4`. Each slice completed in ~20 s with zambialii 5 s + 1 s margin crawl-delay honoured throughout. No deadline skips.
- Judges-panel extraction from the HTML `CORAM` line proved unreliable for some entries (format variance); `judges: []` retained where parse confidence was low — per non-fabrication policy. Richer judges / cited-authorities enrichment is deferred to a later pass.
- Parties split heuristic (first-word-appellant v first-word-respondent) produces robust record IDs for SCZ civil titles. For consolidated / multi-party appeals the slug truncation may collide with a future target; HEAD/slot collision checks at ingest catch that before write.

## Next-tick plan

Continue case_law_scz with the 2025 corridor — top candidates:
- zmsc/2025/30 (31 Dec 2025) + zmsc/2025/29 (12 Dec 2025) + zmsc/2025/27 + zmsc/2025/25.
- After sub-phase reaches ~10 records, rotate to `sis_data_protection` (priority_order item 6) — a narrower corridor with 2021 DPA + implementing SIs.

## Infrastructure follow-up (non-blocking for next tick)

Stale `corpus.sqlite-journal` (dated 2026-04-15) continues to block in-sandbox FTS rebuild; sandbox filesystem refuses `rm` on the journal. 12 pre-existing acts/chiefs-order records missing the `id` field (legacy schema) detected during this batch's integrity pre-scan — not part of this batch, pre-existing defect. Human-driven corpus rebuild still required for Phase 5 retrieval surface.
