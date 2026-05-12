# Batch 0616 — Judgment Ingestion Worker

**Timestamp:** 2026-05-12T15:30Z
**Worker:** judgment-ingestion-worker (jiw)
**Parser version:** v0.4.5-probe-only (no parse this tick; OCR-required PDFs deferred)
**Phase:** priority_b — judiciary CoA sweep page 8 (continuation of b0615 rebaseline)
**Fetches this tick:** 8
**Cumulative today (jiw budget):** 23/500
**Wall-clock:** ~9 min

## Pre-tick state

- FTS5 integrity_check: **ok**
- records: 1917, records_fts: 1917, judgments_meta: 227 (CHECK8 PASS)
- Court of Appeal coverage: **50 / 800** (6.25 %)

## Plan executed (b0615 hand-off → b0616 advance)

Per b0615 sweep-position note, this tick probed the 5 NEW page-8
candidates discovered at b0615 for text-PDF vs scanned-PDF status:

1. Re-fetched page-8 listing → 10 posts confirmed (cross-checked against b0615 catalogue).
2. Fetched post HTML for 4 candidates (Savenda, Zanaco, Setrec, Peter Mutale). The 5th candidate listed by b0615 (`caz-08-014-2019-maxwell-banda`) was **not present** on the re-fetched page 8 listing — see "Discrepancy" below.
3. Extracted PDF URL from each post and downloaded the PDF.
4. Probed first 3 pages of each PDF with `pdfplumber` 0.11.9 for text content.

## Page-8 candidates — probe results

| Candidate | Post HTML | PDF | First-3-pages text | Verdict |
|-----------|-----------|-----|--------------------|---------|
| `app-165-2024-savenda-management-services-limited-vs-lumwana-mining-company-limited` | OK (167 KB) | OK (3.33 MB / 20 pp) | 0 chars | **scanned — defer to OCR queue** |
| `app-181-2023-zanaco-bank-plc-3-others-vs-allan-kandala` | OK (167 KB) | **WRONG PDF ATTACHED** — post links Astro Holdings PDF (App-75-2025) instead of Zanaco PDF | — | **defer — post-misattachment (source-side data quality issue)** |
| `app-304-2022-setrec-steel-and-wood-processing-limited-vs-zambia-national-commercial-bank` | OK (167 KB) | OK (5.19 MB / 33 pp) | 0 chars | **scanned — defer to OCR queue** |
| `app-24-2024-peter-mutale-vs-davies-mukumbwa` | OK (166 KB) | OK (3.36 MB / 21 pp) | 0 chars | **scanned — defer to OCR queue** |
| `caz-08-014-2019-maxwell-banda` | — | — | — | **not present on page 8 listing — b0615 catalogue error; rediscovery task** |

### Discrepancy with b0615 catalogue

b0615 listed 5 NEW page-8 candidates; in fact only 4 are present
on page 8 (Savenda, Zanaco, Setrec, Peter Mutale). The fifth
b0615-listed candidate `caz-08-014-2019-maxwell-banda` is **not**
on page 8 — either b0615 over-counted, or the post was bumped to
a different page between b0615 (T+13:14Z) and b0616 (T+15:30Z) by
fresh CMS activity (unlikely given low judiciaryzambia.com update
cadence on weekends). Rediscovery task: re-locate Maxwell Banda
via judiciaryzambia.com search next tick.

## Raw files written

```
raw/judiciary-zm/coa/App-24-2024-Peter-Mutale-vs-Davies-Mukumbwa-24-Jan-2025-Coram-Siavwapa-JP-Chishimba-Patel-JJA.pdf
  sha256 = dd4e661bea7fed98ab0fa514c11b13d99be5fae2f42f013d991baafa1666d3c1
  bytes  = 3,356,847
raw/judiciary-zm/coa/App-165-2024-Savenda-Management-Services-Limited-vs-Lumwana-Mining-Company-Limited-31-Dec-2024-Coram-Mchenga-DJP-Muzenga-Chembe-JJA.pdf
  sha256 = 3c2365b0646897fa2131d6e312817a0880865fda701f0cbc30ab72e080281dbe
  bytes  = 3,327,705
raw/judiciary-zm/coa/APP-304-2022-Setrec-Steel-and-Wood-Processing-Limited-vs-Zambia-National-Commercial-Bank-Plc-31-Jan-2025-Coram-Chashi-Makungu-Sichinga-JJA.pdf
  sha256 = 27d9aed19f34fe2ed0d9ee4981829b7a4872c740992ec4f84f02d9897c9361cf
  bytes  = 5,187,516

raw/judiciary-zm/coa/_listings/coa-page-8-fetched-2026-05-12T15-30Z.html
raw/judiciary-zm/coa/post-app-165-2024-savenda-management-services-limited.html
raw/judiciary-zm/coa/post-app-181-2023-zanaco-bank-plc-misattached-astro-pdf.html
raw/judiciary-zm/coa/post-app-304-2022-setrec-steel-and-wood-processing-limited.html
raw/judiciary-zm/coa/post-app-24-2024-peter-mutale-vs-davies-mukumbwa.html
```

## Deferrals issued this tick

- **3× scanned-PDF** (parser v0.4.5 cannot proceed without OCR layer):
  Peter Mutale, Savenda, Setrec — added to repair-worker `ocrmypdf-scanned-coa-pdfs` queue manifest.
- **1× post-misattachment** (source-side data quality):
  Zanaco Bank v Allan Kandala — judiciaryzambia.com post page links the Astro Holdings PDF (`App-75-2025`) rather than a Zanaco PDF. Defer with reason `judiciary-zambia-post-misattachment-needs-editor-contact-or-alternate-source`. Operator action item.

## Backlog accounting

**Scanned-PDF backlog: 12 → 15** (+3 this tick).
Running list:
  1.  Mpoyi Mbambu Zambia Limited v Joserine Trading Limited (b0615)
  2.  Lovemore Gumbo v Standard Chartered Bank Zambia plc (b0615)
  3-10. (8 prior scanned-PDF entries listed in gaps.md b0588–b0613)
  11. (b0615 entry 11)
  12. (b0615 entry 12)
  13. **Peter Mutale v Davies Mukumbwa** (b0616 — new)
  14. **Savenda Management Services Ltd v Lumwana Mining Company Ltd** (b0616 — new)
  15. **Setrec Steel and Wood Processing Ltd v Zambia National Commercial Bank plc** (b0616 — new)

**Post-misattachment backlog: 0 → 1** (new category):
  - Zanaco Bank plc & 3 Others v Allan Kandala & 2 Others (b0616).

**Permanent-defer backlog: 1** (Chisumpa Liandisha v The People — b0615, unchanged).

## Sweep position

`judiciary-coa-sweep`: **page 8 — 6 of 10 posts now classified.**

| Post | Status |
|------|--------|
| Savenda (app-165-2024) | scanned-pdf-deferred (b0616) |
| Lovemore Gumbo (app-57-2023) | scanned-pdf-deferred (b0615) |
| Astro Holdings (app-75-2025) | **not yet probed** — next-tick candidate (note: PDF accessible via the misattached Zanaco post link) |
| Zanaco (app-181-2023) | post-misattachment-deferred (b0616) |
| Setrec (app-304-2022) | scanned-pdf-deferred (b0616) |
| Rotor Moulder (app-211-2022) | already ingested (b0613) |
| Peter Mutale (app-24-2024) | scanned-pdf-deferred (b0616) |
| Transquic Service (app-311-2021) | **not yet probed** — next-tick candidate |
| Frank Lumbwe Kakoma (appeal-117-2024) | **not yet probed** — next-tick candidate |
| Mpoyi Mbambu (appeal-268-2022) | scanned-pdf-deferred (b0615) |

**Remaining on page 8 to probe next tick: 3** (Astro Holdings, Transquic, Frank Lumbwe Kakoma).
After page 8 cleared, advance sweep to page 9.

## Corpus mutations

**None.** No records inserted, mutated, or deleted this tick. CHECK8
(records.count == records_fts.count) trivially preserved at 1917
== 1917. No `corpus.sqlite` write occurred.

## Integrity checks (vacuous — no writes)

- CHECK1 (≥1 judge per record): **N/A** (no new records)
- CHECK2 (issue_tags non-empty): **N/A**
- CHECK3 (outcome enum): **N/A**
- CHECK4 (judges resolve in registry): **N/A**
- CHECK5 (no duplicate IDs): **N/A**
- CHECK6 (raw_sha256 match): **PASS** — 3 raw PDFs hashed and recorded above
- CHECK7 (no duplicate case_name/court/date): **N/A**
- CHECK8 (records == records_fts): **PASS** (1917 == 1917, unchanged)

## Budget / cost accounting

| Resource | Used this tick | Cumulative today | Daily cap |
|----------|----------------|------------------|-----------|
| Fetches  | 8              | 23               | 500       |
| Bytes    | ~12.1 MB       | ~19.3 MB         | (untrackd)|
| Wall-clock | ~9 min       | n/a              | 20 min    |

Fetches consumed:
1. `judiciaryzambia.com/.../court-of-appeal-decisions/page/8/` (182 KB)
2. `.../app-165-2024-savenda...` post HTML (167 KB)
3. `.../app-181-2023-zanaco...` post HTML (167 KB)
4. `.../app-304-2022-setrec...` post HTML (167 KB)
5. `.../app-24-2024-peter-mutale...` post HTML (166 KB)
6. `.../wp-content/.../App-24-2024-Peter-Mutale...pdf` (3.36 MB)
7. `.../wp-content/.../App-165-2024-Savenda...pdf` (3.33 MB)
8. `.../wp-content/.../APP-304-2022-Setrec...pdf` (5.19 MB)

User-Agent throughout: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.
`robots.txt` honoured. Rate-limit respected (sequential downloads,
no concurrency, max 60 s per PDF per spec).

## Git / B2

- **Git push**: deferred to host-side sweep. `.git/index.lock` still
  blocked by FUSE EPERM (same pattern documented since b0334+,
  observed across b0608, b0614, b0615). Files-on-disk in workspace
  are authoritative; host-side parallel worker will commit
  transparently once `index.lock` unbinds.
- **B2 sync**: deferred to host (rclone not in sandbox).

## STOP

Verdict: **tick-complete-page-8-probe-3-scanned-PDF-deferrals-1-post-misattachment-deferral-no-corpus-mutation**.
New records: 0. Deferred this tick: 4 (3 scanned + 1 misattachment).
Next tick (b0617): probe Astro Holdings + Transquic + Frank Lumbwe
Kakoma, advance sweep to page 9 if page 8 cleared.
