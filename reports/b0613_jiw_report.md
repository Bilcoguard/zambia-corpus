# JIW Batch 0613 — Drain b0593 v0.4-Pending Dirty Cohort + b0597 Rotor Moulder

**Worker:** judgment-ingestion-worker
**Tick:** b0613
**Timestamp:** 2026-05-12T12:12Z
**Duration:** ~5 minutes wall-clock
**Parser:** v0.4.5-b0613-inline
**Method:** Direct corpus.sqlite write (records + judgments_meta + records_fts), no /tmp staging.

## Summary

| Metric | Pre | Post | Δ |
|---|---|---|---|
| `records` | 1911 | 1917 | +6 |
| `records_fts` | 1911 | 1917 | +6 |
| `judgments_meta` | 221 | 227 | +6 |
| FTS5 integrity probe | PASS | PASS | — |
| CHECK8 (records == records_fts) | PASS | PASS | — |
| CoA coverage (records) | 44 / 800 | 50 / 800 | +6 (5.5% → 6.25%) |
| Deferred-FTS5 backlog | 7 | 1 | −6 |
| Fetches consumed (network) | 0 | 0 | 0 (re-parse only) |

## Records Inserted

1. **`judgment-zm-2025-coa-095-lamasat-international-v-african-banking-corporation-zambia`** — APPEAL/095/2024, 2025-12-31, *granted* — Chashi JJA in chambers; administrative recusal granted while explicitly noting application would otherwise have been refused on merit. 5,780-char body, 124 paragraphs.
2. **`judgment-zm-2025-coa-331-jennifer-tembo-njovu-v-administrator-general`** — CAZ/08/331/2024, 2025-12-31, *dismissed* — Kondolo SC JJA in chambers; appeal dismissed for filing outside Order 10 Rule 3(5) time-frame. 9,013-char body, 197 paragraphs.
3. **`judgment-zm-2025-coa-170-mukamunya-homeowners-association-v-leslie-szeftel-and-anor`** — APP/170/2025, 2025-12-04, *remitted* — Chashi/Ngulube/Banda-Bobo JJA; property held to be business premises within Cap. 193; remitted for rehearing before same Judge. 20,492-char body, 421 paragraphs.
4. **`judgment-zm-2025-coa-127-philemon-dyamini-v-the-people`** — CAZ/09/127/2025, 2025-12-05, *granted* — Mchenga DJP; bail pending appeal granted (K15,000 own recognisance + 2 sureties). 4,859-char body, 113 paragraphs.
5. **`judgment-zm-2025-coa-071-charles-mpundu-v-food-reserve-agency`** — SP/71/2024, 2025-12-05, *dismissed* — Kondolo SC/Majula/Muzenga JJA; leave to appeal to Supreme Court (s.13(1) & (3) CoA Act) dismissed. 13,914-char body, 275 paragraphs.
6. **`judgment-zm-2024-coa-211-rotor-moulder-enterprises-v-stanley-jordan-and-others`** — APP/211/2022, 2024-12-31, *allowed* — Makungu/Muzenga/Chembe JJA; writ of possession set aside for breach of natural justice (intervenors not served). 23,019-char body.

## Records Deferred (1)

- **`judgment-zm-2020-coa-113-chisumpa-liandisha-v-the-people`** — APP/113/2020. **`truncated-source-pdf-missing-operative-paragraphs`**: pdfplumber reports 8 pages but pages 6–8 are byte-identical duplicates of pages 1–3, and the judgment body ends mid-sentence on page 5. No operative paragraph, no "Dated at…" stamp, no decision date. Mitigation: re-fetch from judiciaryzambia.com next tick (URL preserved); cross-check ZambiaLII for the same appeal; if neither yields, escalate to alternate-source retrieval.

## Integrity Checks (all PASS)

- CHECK1: Every record has ≥1 judge (verified — single-judge rulings explicitly cited; three-judge panels expanded).
- CHECK2: `issue_tags` non-empty for all 6 records (4–6 tags each, hand-curated).
- CHECK3: All outcomes drawn from allowed enum (`granted`, `dismissed`, `remitted`, `allowed`).
- CHECK4: All judges resolve in `judges_registry.yaml` (Chashi, Banda-Bobo, Ngulube, Mchenga, Kondolo SC, Majula, Muzenga, Makungu, Chembe — all pre-existing canonical entries with correct CoA `JJA`/`DJP`/`SC` post-nominals).
- CHECK5: No duplicate IDs in `records` (verified pre-INSERT).
- CHECK6: `raw_sha256` matches on-disk file for every record (recomputed via `hashlib.sha256` of full bytes).
- CHECK7: No duplicate `case_number` + `court` combinations (dup-check on `judgments_meta` pre-INSERT).
- CHECK8: `records (1917) == records_fts (1917)` (PASS).

## Coram Bleed-Through Cleanup (v0.4.5 lessons)

The 5 b0593 records each had distinct Coram-line bleed-through patterns that defeated v0.3.x and v0.4.x parsers:

- **Lamasat:** "RESPONDENT LIMITED T/A ATLAS MARA…" line continuation across line-break into Coram address; v0.3.x parser captured "RESPONDENT" as part of case_name.
- **Jennifer:** "APPELLANT" terminator-token followed by date stamp "31 DEC 2025" inserted before "AND <party> RESPONDENT"; date stamp polluted case_name field.
- **Mukamunya:** Coram line "Chashi, Ngulube and Banda-Bobo, JJA" cleanly delineated, but judge-extractor was over-greedy and pulled "On 15th, October, 2025 and 4th December, 2025" hearing-date line into judges_json as a fourth "judge".
- **Dyamini:** PDF stamp bleed-through ("i IC OF iRT OF APP", "ri ''•) L.L.", "CRIMINAL REGISTRY 2") injected into BETWEEN block — required ground-truth re-derivation of case_name from the URL slug + careful inspection of the Coram line.
- **Mpundu:** Stamp bleed "/ C6URTO'J1 r" and "05 OE 2O5" replaced "CHARLES MPUNDU" with "C6URTO'J1 r CHARLES MP ND" and dropped final "U" — required manual reconstruction.

All 5 records were re-derived from first principles by reading the cover page and Coram line directly, not relying on the b0593 parser output. This is sustainable for per-record curation up to ~10 records per tick; for batch sizes >10, recommend v0.5 auto-Coram-stripping with a regex that anchors on BETWEEN…AND…RESPONDENT and an explicit Coram-line state machine.

## Next-Tick Plan (b0614)

1. FTS5 health probe (5 signals).
2. `corpus.sqlite.bak.b0614-pre-…` backup.
3. **Advance `judiciary-coa-sweep: page 8`** (6 unprocessed CoA candidates) — fetch posts + PDFs, hand-curate or apply v0.4.5 inline parser depending on Coram-line cleanliness. Within 500/day budget (today 0/500 used).
4. If page-8 sweep yields any "scanned-PDF" candidates, defer to repair-worker `ocrmypdf` queue (currently 10 records backlog).
5. Optionally attempt fresh `judiciaryzambia.com` re-fetch of Chisumpa Liandisha PDF to test for source-side truncation fix; cheap probe (~1 fetch).

## Budget

- Today's JIW fetches: **0 / 500** (re-parse from on-disk raw PDFs only — no network calls this tick).
- Wall-clock: ~5 minutes (well under 20-min hard cap).
- Records inserted: 6 / 8 MAX_BATCH_SIZE.

## B2 Sync

`rclone` not available in sandbox — deferred to host (per established b0548..b0612 precedent).
