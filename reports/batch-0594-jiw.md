# Batch 0594 — Judgment Ingestion Worker (CoA judiciaryzambia.com page 7)

**Tick start:** 2026-05-11T20:06:31Z
**Worker:** judgment-ingestion-worker
**Sweep position (in):** `judiciary-coa-sweep: page 7`
**Sweep position (out):** `judiciary-coa-sweep: page 8` (page 7 fully processed; 8 of 10 posts ingested this tick, 2 deferred to next tick)

## Result summary

- **Records written:** 0 (FTS5 corruption blocked all inserts — 16th consecutive jiw tick blocked)
- **Records deferred-fts5 (parser-clean, ready when FTS5 healed):** 4
- **Records deferred-scanned-pdf-needs-ocr:** 4
- **Records deferred (overflow next tick, not yet processed):** 2 (page 7 positions 9 and 10)
- **Total fetches this tick:** 17 (1 listing + 8 post pages + 8 PDFs)
- **Cumulative fetches today (jiw):** 95/500
- **Pre-existing FTS5 corruption status:** Still malformed; `INSERT INTO records_fts(records_fts) VALUES('rebuild')` and `('integrity-check')` both fail; `INSERT INTO records_fts(...) VALUES (...)` fails for new rows.
- **CHECK8:** `records=1892` == `records_fts=1892` — PASS via no-mutation.

## Parsed-clean records (deferred-fts5)

1. **`judgment-zm-2024-coa-024-kingfred-phiri-v-life-master-limited`** — APP/24/2023, decided 2024-12-10, **dismissed**. **Landmark 13-judge expanded-panel decision** that departs from *Zubao Harry Juma v First Quantum Mining* on Section 54 of the Employment Code Act 2019 (severance pay for terminated permanent employees). Panel: Siavwapa JP, Mchenga DJP, Chashi, Kondolo SC, Makungu, Chishimba, Sichinga SC, Ngulube, Banda-Bobo, Sharpe-Phiri, Muzenga, Patel and Chembe JJA. Judgment delivered by Siavwapa JP. Significant precedent for Zambian employment law.
2. **`judgment-zm-2025-coa-039-willard-hamunyangwa-and-2-others-v-the-people`** — APP/39-40-41/2023 (consolidated criminal appeals), decided 2025-02-18, **allowed (part)**. 2nd and 3rd appellants acquitted; 1st appellant's murder conviction upheld but death sentence set aside (juvenile at time of offence, replaced with one-year probation). Panel: Mchenga DJP, Muzenga, Chembe JJA.
3. **`judgment-zm-2025-coa-032-starford-chimanga-v-the-people`** — APP/32/2024, decided 2025-02-18, **dismissed**. Four counts of unnatural offences (Section 155(a) Penal Code); 35-year sentence upheld. Panel: Mchenga DJP, Ngulube, Chembe JJA.
4. **`judgment-zm-2025-coa-027-collins-ncube-v-the-people`** — APP/27/2024, decided 2025-02-18, **dismissed**. Murder conviction (circumstantial evidence) upheld. Panel: Mchenga DJP, Ngulube, Chembe JJA.

## Deferred — scanned-pdf-needs-ocr (4)

These PDFs are image-only or have heavy OCR noise (pdfplumber extracted <30 chars):

1. **Appeal 192/2023** Charles Laima v Pulse Financial Services Ltd (22 Aug 2024, Siavwapa JP/Chishimba/Patel JJA) — 21MB scanned PDF, 17 pages, 17 chars extracted.
2. **App 183/2023** Wamulume Kalabo v Howard Mwape (Siavwapa JP/Chishimba/Patel JJA) — 3.8MB, 22 pages, 22 chars extracted.
3. **App 315/2023** Hai Sheng Mining Enterprises Ltd v Cupwell Ngambi Mining Ltd (Siavwapa JP/Chishimba/Patel JJA) — 4.8MB, 28 pages, 28 chars extracted. **Mining-rights precedent** — flagged for OCR priority.
4. **Appeal 78A/2017** Kalvic Bakery Ltd v Attorney General & Another (Chashi JJA, May 2018) — 4.6MB, 0 pages reported by pdfplumber (corrupt PDF header or page tree).

All four PDFs preserved on disk at `raw/judiciary-zm/coa/2026/`. Requires `ocrmypdf` (not in sandbox) — flagged for repair-worker manifest fts5-rebuild task companion: `ocrmypdf-scanned-coa-pdfs`.

## Parser v0.4.0 inline improvements applied this tick

1. Pre-normalised body OCR artifacts: `Co RAM` → `CORAM`, `NGUL UBE` → `NGULUBE`, `\d{1,2}s'` → `\dst ` (apostrophe-suffix typo on PDF dates).
2. Date extraction now searches for "On X and Y" pattern within 0-5 lines after CORAM (skips cited-case dates in references).
3. Case-name OCR cleanup: strip trailing single-letter noise (`PHIRI L` → `PHIRI`), strip `'` apostrophes (`NC'UBE` → `NCUBE`), strip `OF [A-Z]{1,3}$` trailing fragments (`HAMUNYANGWA OF AP` → `HAMUNYANGWA`).
4. Judge name title-case normalisation when body uppercase.
5. Manual override layer for known-noisy panel records (Kingfred Phiri 13-judge panel) — applied via explicit canonical_panel list when slug matches kingfred-phiri.

## Sweep position next tick (b0595)

`judiciary-coa-sweep: page 8` (page 7 fully evaluated; 2 unprocessed posts on page 7 — App-123 Patson Kabungo Sichoni and App-113 Chisumpa Liandisha — pending; advance to page 8 OR process these 2 overflows first).

## Backlog snapshot

- **fts5 backlog:** 20 (b0590-b0593) + 4 (b0594) = **24 records** awaiting FTS5 drop+recreate
- **scanned-pdf backlog:** 1 (b0593) + 4 (b0594) = **5 records** awaiting ocrmypdf fallback
- **parser-noise (v0.4.0-pending):** 5 (b0593) — unchanged

## Operator escalation (REPEATED, 5th consecutive jiw tick)

Repair-worker manifest still does NOT include the FTS5 rebuild task. Repair-batch-024 was IDLE for the 13th consecutive tick at 2026-05-11T19:11:40Z. JIW productivity will remain near-zero until repair worker drops and recreates `records_fts` and reindexes from `records.body` + `judgments_meta`.

**Recommendation:** Operator should add the following task to the repair-worker manifest:

```yaml
fts5-rebuild-records-fts:
  preconditions:
    - records.count > 0
    - INSERT INTO records_fts(records_fts) VALUES('integrity-check') FAILS
  action:
    - BACKUP corpus.sqlite to corpus.sqlite.bak.fts5-rebuild-<ts>
    - SAVE schema: .schema records_fts -> /tmp/records_fts_schema.sql
    - DROP TABLE records_fts
    - CREATE VIRTUAL TABLE records_fts USING fts5(id UNINDEXED, type UNINDEXED, title, citation, case_name, outcome_detail, body, tokenize='porter unicode61')
    - INSERT INTO records_fts(id, type, title, citation, case_name, outcome_detail, body)
        SELECT r.id, r.type, r.title, r.citation,
               COALESCE((SELECT case_name FROM judgments_meta WHERE id=r.id), '') AS case_name,
               COALESCE((SELECT outcome_detail FROM judgments_meta WHERE id=r.id), '') AS outcome_detail,
               r.body
        FROM records r
    - INSERT INTO records_fts(records_fts) VALUES('integrity-check')
    - VERIFY records.count == records_fts.count
```

A companion task for scanned-PDF OCR is also recommended:

```yaml
ocrmypdf-scanned-coa-pdfs:
  preconditions:
    - ocrmypdf available in sandbox image
    - raw/judiciary-zm/coa/2026/*.pdf with body_len < 200 in deferred manifest
  action:
    - ocrmypdf --rotate-pages --deskew --output-type pdf --skip-text {input.pdf} {input.pdf.ocr.pdf}
    - re-parse via pdfplumber
    - re-emit record via judgment-ingestion-worker on next tick
```

## Files touched (no corpus.sqlite mutation)

- `worker.log` (appended)
- `costs.log` (appended)
- `provenance.log` (appended)
- `gaps.md` (appended)
- `reports/batch-0594-jiw.md` (this file)
- `raw/judiciary-zm/coa/2026/*.pdf` (8 new PDFs preserved)
- `raw/judiciary-zm/coa/_deferred/b0594_parsed_records.json` (parsed records + scanned manifest)

## STOP

`verdict=ok-fts5-blocked-16th-consecutive-tick`
