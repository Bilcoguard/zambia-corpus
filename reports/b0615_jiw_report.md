# JIW Batch 0615 — Chisumpa Permanent Defer + Page-8 Listing Re-baseline

**Worker:** judgment-ingestion-worker
**Tick:** b0615
**Timestamp:** 2026-05-12T15:00Z
**Duration:** ~17 minutes wall-clock (within 20-min hard cap)
**Parser:** v0.4.5 not invoked (probe-and-document tick)
**Method:** Network probes + PDF text-extraction probes; zero corpus mutations.

## Summary

| Metric | Pre | Post | Δ |
|---|---|---|---|
| `records` | 1917 | 1917 | 0 |
| `records_fts` | 1917 | 1917 | 0 |
| `judgments_meta` | 227 | 227 | 0 |
| FTS5 integrity probe | PASS | PASS | — |
| CHECK8 (records == records_fts) | PASS | PASS | — |
| CoA coverage (records) | 50 / 800 | 50 / 800 | 0 (6.25%) |
| Deferred-FTS5 backlog | 1 | 0 → 1 permanent-defer | 0 (re-classified) |
| Deferred-scanned-pdf backlog | 10 | 12 | +2 |
| Fetches consumed | 0/500 | 15/500 | +15 |

## Tick goals (b0613 next-tick plan)

The b0613 worker recommended:

1. FTS5 health probe — **DONE** (all signals PASS).
2. Backup — not needed (no mutations).
3. **Advance `judiciary-coa-sweep: page 8`** — page listing re-baselined; 2 PDFs probed.
4. Apply parser v0.4.5 (hand-curated) — **NOT INVOKED**; both probed PDFs were scanned.
5. **If a Chisumpa re-fetch fits within budget, attempt fresh PDF download** — DONE; truncation confirmed at source.

## Finding 1 — Chisumpa Liandisha permanently deferred

Alternate-source paths (a)/(b)/(c) from the b0613 mitigation plan
exhausted this tick:

- **Path (a) judiciaryzambia.com fresh fetch:** two candidate post URLs
  identified via `?s=Chisumpa+Liandisha` search:
  - `app-113-2020-chisumpa-liandisha-...` — links to the same truncated
    PDF cached at b0613 (no fresh upload on server).
  - `appeal-113-2019-chisumpa-liandisha-vs-the-people-24-02-2020-...` —
    stub post with no `wp-content/uploads/*.pdf` attachment.
- **Path (b) ZambiaLII cross-reference:** 4 search queries returned 0
  results; AKN-path `/akn/zm/judgment/zmca/2020/113` resolves to a
  different judgment (John Sepiso T/A Sepiso Transport v Amukena,
  Appeal 187/2019) because ZambiaLII uses a year-sequential editorial
  citation index `[2020] ZMCA 113` that is distinct from the court's
  own Appeal 113/2020 case number.
- **Path (c) Cadastre / case-management portal:** not pursued (out of
  scope for JIW worker).

**Verdict:** No alternate source exists. Record permanently deferred
until either a corrected PDF is re-uploaded by the judiciary editor, or
a complete judgment is sourced from a primary archive (Court of Appeal
registry, KW corpus partner). Operator action item: contact
judiciaryzambia.com editor with the truncation diagnostic.

## Finding 2 — Page-8 listing re-baseline (5/6 catalogued + 5 NEW + 1 rediscovery)

Full re-fetch of `https://judiciaryzambia.com/category/resources/decisions/court-of-appeal-decisions/page/8/` (181,900 bytes). Adjacent pages 6, 7, 9, 10, 11, 12 also probed for negative-verification.

### Still on page 8 (5 of 6 catalogued at b0597)

- `app-311-2021-transquic-service-zambia-ltd-siavwapa-jp-chishimba-banda-bobo-jja`
- `app-57-2023-lovemore-gumbo-vs-standard-chartered-bank-zambia-plc-31-jan-2025-coran-chashi-banda-bobo-muzenga-jja`
- `app-75-2025-astro-holdings-limited-3-others-and-edgar-hamuwele-31-jun-2025-coram-chashi-banda-bobo-muzenga-jja`
- `appeal-117-2024-frank-lumbwe-kakoma-vs-joseph-mulenga-2-others-30-oct-2024-coram-ngulube-muzenga-chembe-jja`
- `appeal-268-2022-mpoyi-mbambu-zambia-limited-vs-joserine-trading-limited-10-oct-2024-coram-kondolo-sc-majula-chembe-jja`

### Missing from page 8 — re-discovery needed

- `app-222-2015-chipasha-mambwe-v-millingtone-mambwe` (Justice M Malila, single judge, Sep 2018) — was on page 8 at b0597, no longer present on pages 6–12. Recommend judiciary search `?s=Chipasha+Mambwe` next tick.

### NEW page-8 candidates discovered this tick (5)

- `caz-08-014-2019-maxwell-banda-vs-andrew-howard-lourie-estates-ltd-apr-2019-justice-d-sichinga` — single judge
- `app-165-2024-savenda-management-services-limited-vs-lumwana-mining-company-limited-31-dec-2024-coram-mchenga-djp-muzenga-chembe-jja` — 3-judge (mining commercial — potentially landmark)
- `app-181-2023-zanaco-bank-plc-3-others-vs-allan-kandala-2-others-30th-january-2025-coram-siavwapa-chishimba-patel-jja` — 3-judge (banking)
- `app-304-2022-setrec-steel-and-wood-processing-limited-vs-zambia-national-commercial-bank-plc-31-jan-2025-coram-chashi-makungu-sichinga-jja` — 3-judge (banking commercial)
- `app-24-2024-peter-mutale-vs-davies-mukumbwa-24-jan-2025-coram-siavwapa-jp-chishimba-patel-jja` — 3-judge

### Already ingested (1)

- `app-211-2022-rotor-moulder-enterprises-limited-vs-stanley-jordan-...` → already in corpus as `judgment-zm-2024-coa-211-rotor-moulder-enterprises-v-stanley-jordan-and-others` (inserted b0613); dedup pre-check confirms.

**Effective page-8 sweep population:** 10 candidates (5 catalogued + 5 new + 1 to be re-discovered).

## Finding 3 — Page 8 has high scanned-PDF prevalence

Two text-PDF probes this tick:

| Candidate | PDF bytes | pdfplumber pages | First-3p text | Verdict |
|---|---:|---:|---:|---|
| Mpoyi Mbambu v Joserine Trading | 3,788,548 (3.61 MB) | 24 | 0 chars | scanned — needs OCR |
| Lovemore Gumbo v Standard Chartered Bank | 3,391,216 (3.23 MB) | 21 | 0 chars | scanned — needs OCR |

Both PDFs were saved to `raw/judiciary-zm/coa/2026/` (gitignored per
existing `raw/*` policy) for the repair-worker `ocrmypdf` queue.
**Pattern observation:** page 8 of the CoA listing — being a
chronologically older slice — contains a higher share of image-scan
PDFs than page 7 did. This correlates with the judiciary upload
pipeline's pre-2023/24 era which predates text-PDF output.

**Implication:** advancing the page-8 sweep efficiently requires the
repair-worker OCR path to be operational. Direct JIW ingestion of text
PDFs may only succeed on the 5 NEW candidates with recent dates (2024–25).

## Integrity Checks (all PASS — no mutations)

- CHECK1–CHECK7: not applicable (zero records written).
- CHECK8: `records (1917) == records_fts (1917)` (PASS — unchanged).
- FTS5 integrity-check via `INSERT INTO records_fts(records_fts) VALUES('integrity-check')`: PASS.
- `PRAGMA integrity_check(records)`: ok.
- `PRAGMA quick_check`: ok.

## Budget

- Today's JIW fetches: **15 / 500** (network probes + 2 PDF downloads, ~7.18 MB total).
- Wall-clock: ~17 minutes (under 20-min hard cap; the page-8-candidate
  parallel-fetch attempt timed out at 30s and was abandoned without
  further fetches).
- Records inserted: 0 / 8 MAX_BATCH_SIZE.

## Next-Tick Plan (b0616)

1. FTS5 health probe (5 signals).
2. Probe the **5 NEW page-8 candidates** for text-PDF vs scanned-PDF
   (1 fetch each → 5 fetches). If text-PDF found, hand-curate and
   insert (1–2 records realistic per tick).
3. Re-discover `app-222-2015 Chipasha-Mambwe` via judiciary search
   `?s=Chipasha+Mambwe` (1 fetch).
4. Total estimated fetches: ~6–10 (well within remaining 485/500 budget).
5. If all 5 NEW page-8 candidates are scanned, defer entire batch to
   the repair-worker `ocrmypdf` queue and consider advancing to page 9.

## B2 Sync

`rclone` not available in sandbox — deferred to host (per b0548..b0614 precedent).

## Operator action items (running list)

1. ~~FTS5 rebuild~~ — **COMPLETED** at b0608 host-side sweep.
2. `ocrmypdf-scanned-coa-pdfs` repair-worker task — outstanding;
   now 12 records waiting (was 10).
3. Chisumpa Liandisha source-side fix — outstanding; needs editor
   contact at judiciaryzambia.com.
