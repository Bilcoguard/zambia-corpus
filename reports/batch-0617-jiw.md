# Batch 0617 — judgment-ingestion-worker (b0617-jiw)

**Timestamp:** 2026-05-12T17:11Z
**Phase:** priority_b — judiciary CoA sweep page 8 completion + page 9 scout
**Fetches:** 7 (cumulative today 30/500)
**Records inserted:** 0
**Records deferred:** 4 (3 scanned-PDF + 1 post-no-attachment stub)
**Court of Appeal coverage:** 50 / 800 unchanged (6.25%)
**CHECK8:** PASS (records=1917, records_fts=1917)
**FTS5 integrity-check:** PASS throughout

## Summary

This was the page-8 completion tick. The three remaining unclassified
posts (Astro Holdings v Edgar Hamuwele, App-311-2021 Transquic, and
Appeal-117-2024 Frank Lumbwe Kakoma) were probed; all three are
scanned-image PDFs with zero extractable text and are deferred to the
`ocrmypdf-scanned-coa-pdfs` repair-worker queue. A rediscovery probe
for the b0615-catalogued Maxwell Banda (`caz-08-014-2019`) confirmed
the post exists at judiciaryzambia.com but is a STUB — no PDF
attachment of any kind. The judiciary CoA category page 9 listing was
fetched as a scout for the next tick.

**Page 8 is now FULLY CLASSIFIED.** Next-tick sweep advances to page 9.

## Fetches consumed this tick (7 of 500)

| # | URL | bytes | purpose |
|---|-----|-------|---------|
| 1 | `judiciaryzambia.com/app-75-2025-astro-holdings…/` | 166,474 | post HTML, find PDF URL |
| 2 | `judiciaryzambia.com/app-311-2021-transquic-service…/` | 166,516 | post HTML, find PDF URL |
| 3 | `judiciaryzambia.com/appeal-117-2024-frank-lumbwe-kakoma…/` | 166,352 | post HTML, find PDF URL |
| 4 | `wp-content/.../App-311-2021-Transquic-Service…JJA.pdf` | 5,572,012 | PDF download — newly fetched |
| 5 | `judiciaryzambia.com/?s=Maxwell+Banda` | 160,312 | search rediscovery probe |
| 6 | `judiciaryzambia.com/caz-08-014-2019-maxwell-banda…/` | 166,982 | post HTML — STUB (no PDF) |
| 7 | `judiciaryzambia.com/category/.../court-of-appeal-decisions/page/9/` | 182,247 | page-9 listing scout |

Total bytes downloaded: ~6.58 MB.

**Note:** Astro Holdings APP-75-2025 PDF and Frank Lumbwe Kakoma
Appeal-117-2024 PDF were already on disk from prior fetches (Astro
via b0616's Zanaco-misattachment side-effect; Frank via an earlier
unattributed fetch). Zero net PDF bytes downloaded for those two.

## New scanned-PDF backlog entries (+3 → 18 total)

| Slug | Pages | sha256 (first 16) | Raw path |
|------|-------|-------------------|----------|
| `judgment-zm-2025-coa-app-75-astro-holdings-v-edgar-hamuwele` | 20 | `92d7372ee5ac2782` | `raw/judiciary-zm/coa/2026/APP-75-2025-Astro-Holdings-Limited-3-Others-and-Edgar-Hamuwele-31-Jun-2025-Coram-Chashi-Banda-Bobo-Muzenga-JJA.pdf` |
| `judgment-zm-2024-coa-appeal-117-frank-lumbwe-kakoma-v-joseph-mulenga` | 15 | `cebeb26a3d721aa0` | `raw/judiciary-zm/coa/2026/Appeal-117-2024-Frank-Lumbwe-Kakoma-vs-Joseph-Mulenga-2-Others-30-Oct-2024-Coram-Ngulube-Muzenga-Chembe-JJA.pdf` |
| `judgment-zm-2021-coa-app-311-transquic-v-african-banking-corporation-zambia` | 37 | `fbc309f43dbd7995` | `raw/judiciary-zm/coa/2026/App-311-2021-Transquic-Service-Zambia-Ltd-3-Others-vs-African-Banking-Corporation-Zambia-LTD-Coram-Siavwapa-JP-Chishimba-Banda-Bobo-JJA.pdf` |

All three need OCR via the repair-worker `ocrmypdf-scanned-coa-pdfs`
queue. Raw PDFs saved on disk; sha256 computed and recorded in
`provenance.log`.

## New post-no-attachment-stub backlog entry (+1, new sub-category)

- `caz-08-014-2019-maxwell-banda-vs-andrew-howard-lourie-estates-ltd-apr-2019-justice-d-sichinga`
  - Post URL: `https://judiciaryzambia.com/caz-08-014-2019-maxwell-banda-vs-andrew-howard-lourie-estates-ltd-apr-2019-justice-d-sichinga/`
  - HTTP 200, 166,982 bytes returned, but the post body contains
    **zero PDF attachments**, zero file links of any kind, and the
    `entry-content` div is empty/title-only.
  - The post is **NOT** present on judiciary CoA page 8 (this tick's
    re-fetch confirms 10 posts, all accounted for; Maxwell Banda is
    not among them). It also is not on any of pages 6, 7, 9, 10, 11,
    or 12 (verified at b0615). The post exists as an orphan reachable
    only via search.
  - This resolves the b0615 catalogue discrepancy: the "5 NEW
    candidates" list at b0615 over-counted by 1 — Maxwell Banda was
    likely included from a prior listing-pagination snapshot that
    has since shifted.
  - Deferral category: `post-no-attachment-stub` (new — distinct from
    `post-misattachment` because there is no PDF at all, not a wrong
    PDF). Resolution requires editor contact at judiciaryzambia.com,
    or alternate-source retrieval (ZambiaLII or Court of Appeal
    registry direct).

## Page 8 final classification (10 posts)

| # | Post slug | Status | Batch |
|---|-----------|--------|-------|
| 1 | `app-165-2024-savenda-management-services-vs-lumwana-mining` | scanned-PDF deferral | b0616 |
| 2 | `app-57-2023-lovemore-gumbo-vs-standard-chartered-bank` | scanned-PDF deferral | b0615 |
| 3 | `app-75-2025-astro-holdings-limited-3-others-vs-edgar-hamuwele` | scanned-PDF deferral | **b0617** |
| 4 | `app-181-2023-zanaco-bank-plc-vs-allan-kandala` | post-misattachment | b0616 |
| 5 | `app-304-2022-setrec-steel-and-wood-processing-vs-zanaco` | scanned-PDF deferral | b0616 |
| 6 | `app-211-2022-rotor-moulder-enterprises-vs-stanley-jordan` | INGESTED | b0613 |
| 7 | `app-24-2024-peter-mutale-vs-davies-mukumbwa` | scanned-PDF deferral | b0616 |
| 8 | `app-311-2021-transquic-service-zambia-vs-african-banking-corp` | scanned-PDF deferral | **b0617** |
| 9 | `appeal-117-2024-frank-lumbwe-kakoma-vs-joseph-mulenga` | scanned-PDF deferral | **b0617** |
| 10 | `appeal-268-2022-mpoyi-mbambu-zambia-vs-joserine-trading` | scanned-PDF deferral | b0615 |

Net result for page 8: 8 scanned-PDF deferrals + 1 post-misattachment
+ 1 already-ingested = 10 posts.

Maxwell Banda is an **orphan stub** outside page 8 and is not part of
this tally.

## Page 9 scout (next-tick candidates)

Page 9 listing fetched (`/court-of-appeal-decisions/page/9/`, 182,247
bytes). 10 posts identified (all 2024 decisions, no prior-batch
overlap by slug):

1. `appeal-42-2024-moffat-fungamwango-vs-charl-and-basil-farms` (07-Nov-2024)
2. `appeal-004-2024-football-association-of-zambia-vs-augustine-mukoka` (07-Nov-2024)
3. `app-313-2022-betty-kulofwa-mailosi-vs-edward-mukelabai-mate` (30-Oct-2024)
4. `appeal-309-2022-stone-coat-surfacing-zambia-vs-jmz-properties` (30-Oct-2024)
5. `appeal-96-2024-bwalya-lumbwe-vs-ronald-simwinga-dr` (31-Oct-2024)
6. `appeal-250-2023-c-and-c-world-trade-vs-r-b-technical-services-indo-zambia-bank` (31-Oct-2024)
7. `sp-70-2024-am-media-vs-bokani-soko` (01-Nov-2024) — ruling
8. `caz-8-298-2024-esther-nyawa-lungu-vs-the-dpp` (04-Nov-2024) — ruling
9. `app-269-2021-sokwani-peter-chilembo-vs-finance-bank-zambia` (30-Sept-2024)
10. `app-287-2022-nchindika-nankolonga-vs-zambia-national-building-society` (18-Sept-2024)

Recommended next-tick approach: probe 4-6 of these in priority order
(non-criminal, non-ruling commercial / land / pension judgments
typically yield text-PDFs more often than the scanned-image-pipeline
era cluster on pages 8). Two are explicitly labelled "ruling" rather
than judgment (#7 and #8) — these are typically interlocutory and
short.

## Integrity checks

| Check | Verdict |
|-------|---------|
| CHECK1 judges per record | N/A — zero writes this tick |
| CHECK2 issue_tags non-empty | N/A |
| CHECK3 outcome enum | N/A |
| CHECK4 judges resolved in registry | N/A |
| CHECK5 no duplicate IDs | N/A |
| CHECK6 raw_sha256 matches on-disk | PASS — 3 PDFs hashed and recorded |
| CHECK7 no duplicate case_name + court + date | N/A |
| CHECK8 records == records_fts | PASS (1917 == 1917) |
| FTS5 integrity-check | PASS |

## Backlog state

- Deferred-fts5: 1 (Chisumpa Liandisha — permanently deferred at b0615).
- Deferred-scanned-pdf: **18** (was 15; added Astro + Frank Lumbwe + Transquic).
- Deferred-post-misattachment: 1 (Zanaco Bank v Allan Kandala — b0616).
- Deferred-post-no-attachment-stub: 1 (Maxwell Banda — **b0617**, new sub-category).
- Court of Appeal coverage: 50 / 800 (6.25%) unchanged.

## Sweep position next tick (b0618)

`judiciary-coa-sweep`: **page 9, 0 of 10 posts classified.**

Page-8 archived as fully-classified.

Recommended next-tick approach:
1. Probe 4-6 of the 10 page-9 candidates listed above; prefer
   non-criminal commercial/land/pension judgments to maximise
   text-PDF yield.
2. Skip explicit "ruling" labels (interlocutory, often short and not
   precedential).
3. If text-PDF, hand-curated v0.4.5-inline parse and insert.
4. If scanned-PDF, append to repair-worker `ocrmypdf-scanned-coa-pdfs`
   queue manifest.

## Operator action items (running list)

- (a) FTS5 rebuild action — **COMPLETED** at b0608 host-side sweep.
- (b) `ocrmypdf-scanned-coa-pdfs` repair-worker task — outstanding;
  now **18 records** waiting (was 15).
- (c) Chisumpa Liandisha source-side fix — outstanding; needs editor
  contact at judiciaryzambia.com.
- (d) Zanaco Bank v Allan Kandala post-misattachment — outstanding;
  needs editor contact at judiciaryzambia.com to fix wrong PDF
  attachment, or alternate-source retrieval.
- (e) **NEW**: Maxwell Banda post-no-attachment-stub — outstanding;
  needs editor contact at judiciaryzambia.com to upload PDF, or
  alternate-source retrieval (ZambiaLII / Court of Appeal registry).
