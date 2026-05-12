# Batch 0618 — judgment-ingestion-worker (b0618-jiw)

**Timestamp:** 2026-05-12T16:30Z
**Phase:** priority_b — judiciary CoA sweep page 9 full classification
**Fetches:** 19 (cumulative today 49/500)
**Records inserted:** 0
**Records deferred:** 8 (all scanned-PDF)
**Court of Appeal coverage:** 50 / 800 unchanged (6.25%)
**CHECK8:** PASS (records=1917, records_fts=1917, judgments_meta=227)
**FTS5 integrity-check:** PASS throughout
**Corpus mutations:** none (no records inserted, updated, or deleted)

## Summary

Continuation of the judiciary CoA sweep — page 9. All 8 non-ruling page-9
posts were probed by fetching post HTML + first-attached PDF and running
pdfplumber 0.11.9 on the first three pages. **Every probed PDF returned
zero extractable text — all 8 are scanned-image PDFs.** All 8 are deferred
to the `ocrmypdf-scanned-coa-pdfs` repair-worker queue, taking the
scanned-PDF backlog from 18 → **26 records**.

The two rulings on page 9 (#7 `sp-70-2024-am-media`, #8 `caz-8-298-2024-esther-nyawa-lungu`)
were intentionally skipped per b0617 next-tick guidance (interlocutory, low
precedential value). Page 9 is now **fully classified for judgments**;
sweep advances to **page 10** next tick.

The b0617 scout had imprecise slugs for 4 of the 10 page-9 candidates
(short prefix slugs returned HTTP 404). A page-9 listing re-fetch was used
to obtain canonical full-coram slugs before probing. Two probe-1 candidates
(#2 FAZ, #4 Stone Coat) failed with 404 against the short slug; both
succeeded against the canonical slugs in probe-2.

## Fetches consumed this tick (19 of 500)

| # | URL | bytes | purpose |
|---|-----|-------|---------|
| 1 | `judiciaryzambia.com/.../court-of-appeal-decisions/page/9/` | 182,209 | re-fetch listing for canonical slugs |
| 2 | post: `appeal-42-2024-moffat-fungamwango-...` | 166,715 | post HTML, find PDF URL |
| 3 | PDF: `Appeal-42-2024-Moffat-Fungamwango...pdf` | 2,786,796 | content + classification |
| 4 | post: `appeal-004-2024-faz-vs-augustine-mukoka` (short slug) | — (404) | probe-1 |
| 5 | post: `appeal-309-2022-stone-coat-surfacing-zambia-vs-jmz-properties` (short slug) | — (404) | probe-1 |
| 6 | post: `app-269-2021-sokwani-peter-chilembo-...` | 166,975 | post HTML |
| 7 | PDF: `App-269-2021-Sokwani-Peter-Chilembo...pdf` | 5,214,424 | content + classification |
| 8 | post: `appeal-004-2024-football-association-of-zambiafaz-...` (canonical) | 166,562 | post HTML |
| 9 | PDF: `Appeal-004-2024-Football-Association-of-Zambia...pdf` | 2,247,410 | content + classification |
| 10 | post: `appeal-309-2022-stone-coat-surfacing-zambia-limited-...` (canonical) | 166,656 | post HTML |
| 11 | PDF: `Appeal-309-2022-Stone-Coat-Surfacing...pdf` | 2,242,127 | content + classification |
| 12 | post: `appeal-250-2023-c-and-c-world-trade-limited-...` | 167,439 | post HTML |
| 13 | PDF: `Appeal-250-2023-C-and-C-World-Trade...pdf` | 2,818,538 | content + classification |
| 14 | post: `app-287-2022-nchindika-nankolonga-vs-zambia-national-building-society-...` | 166,779 | post HTML |
| 15 | PDF: `App-287-2022-Nchindika-Nankolonga...pdf` | 7,817,518 | content + classification |
| 16 | post: `app-313-2022-betty-kulofwa-mailosi-makalu-...` | 166,744 | post HTML |
| 17 | PDF: `App-313-2022-Betty-Kulofwa-Mailosi-Makalu...pdf` | 3,454,114 | content + classification |
| 18 | post: `appeal-96-2024-bwalya-lumbwe-vs-ronald-simwinga-dr-...` | 166,108 | post HTML |
| 19 | PDF: `Appeal-96-2024-Bwalya-Lumbwe-vs-Ronald-Simwinga-DR...pdf` | 3,316,171 | content + classification |

Total bytes downloaded this tick: ~30.2 MB (8 PDFs + 1 listing + 8 post HTMLs + 2 404s).
Cumulative fetches today: 30 (prior) + 19 = **49 / 500**.

## Page 9 — full classification (8 judgments + 2 rulings = 10 posts)

| # | Slug (abbrev.) | Date | Verdict | Notes |
|---|---|---|---|---|
| 1 | `appeal-42-2024-moffat-fungamwango-vs-charl-and-basil-farms` | 2024-11-07 | **scanned-PDF** | 16 pp, 2.79 MB |
| 2 | `appeal-004-2024-football-association-of-zambiafaz-vs-augustine-mukoka` | 2024-11-07 | **scanned-PDF** | 14 pp, 2.25 MB |
| 3 | `app-313-2022-betty-kulofwa-mailosi-makalu-vs-edward-mukelabai-mate-paul-mate` | 2024-10-30 | **scanned-PDF** | 23 pp, 3.45 MB |
| 4 | `appeal-309-2022-stone-coat-surfacing-zambia-limited-vs-jmz-properties-limited` | 2024-10-30 | **scanned-PDF** | 16 pp, 2.24 MB |
| 5 | `appeal-96-2024-bwalya-lumbwe-vs-ronald-simwinga-dr` | 2024-10-31 | **scanned-PDF** | 19 pp, 3.32 MB |
| 6 | `appeal-250-2023-c-and-c-world-trade-limited-vs-r-b-technical-services-limited` | 2024-10-31 | **scanned-PDF** | 18 pp, 2.82 MB |
| 7 | `sp-70-2024-am-media-limited-vs-bokani-soko` | 2024-11-01 | ruling — skipped | interlocutory |
| 8 | `caz-8-298-2024-esther-nyawa-lungu-vs-the-director-public-prosecutions` | 2024-11-04 | ruling — skipped | interlocutory |
| 9 | `app-269-2021-sokwani-peter-chilembo-vs-finance-bank-zambia-plc-2-others` | 2024-09-30 | **scanned-PDF** | 27 pp, 5.21 MB |
| 10 | `app-287-2022-nchindika-nankolonga-vs-zambia-national-building-society` | 2024-09-18 | **scanned-PDF** | 43 pp, 7.82 MB |

**Page 9 yield = 0 records ingested, 8 deferred to OCR.**

## New scanned-PDF backlog entries (+8 → 26 total)

All raw PDFs persisted at `raw/judiciary-zm/coa/2026/<filename>.pdf`. Sha256
computed; ready for the repair-worker `ocrmypdf-scanned-coa-pdfs` queue.

| Proposed ID (post-OCR) | sha256 (first 16) | pp | MB |
|---|---|---:|---:|
| `judgment-zm-2024-coa-42-moffat-fungamwango-v-charl-and-basil-farms` | (see manifest) | 16 | 2.79 |
| `judgment-zm-2021-coa-269-sokwani-peter-chilembo-v-finance-bank-zambia` | (see manifest) | 27 | 5.21 |
| `judgment-zm-2024-coa-4-faz-v-augustine-mukoka` | (see manifest) | 14 | 2.25 |
| `judgment-zm-2022-coa-309-stone-coat-surfacing-v-jmz-properties` | (see manifest) | 16 | 2.24 |
| `judgment-zm-2023-coa-250-c-and-c-world-trade-v-r-b-technical-services` | (see manifest) | 18 | 2.82 |
| `judgment-zm-2022-coa-287-nchindika-nankolonga-v-zambia-national-building-society` | (see manifest) | 43 | 7.82 |
| `judgment-zm-2022-coa-313-betty-kulofwa-mailosi-makalu-v-edward-mukelabai-mate` | (see manifest) | 23 | 3.45 |
| `judgment-zm-2024-coa-96-bwalya-lumbwe-v-ronald-simwinga` | (see manifest) | 19 | 3.32 |

Detailed sha256 + raw paths + post URLs are captured in
`_b0618_jiw/scanned_defers.json` (worker scratch dir) and the
`provenance.log` append-only record.

## Trend observation — scanned-PDF prevalence by page

| Page | Total posts | Ingested text-PDF | Scanned (deferred) | Other |
|---:|---:|---:|---:|---:|
| 1–5 | ~50 | ~50 | 0 | 0 |
| 6 | 10 | 7 (b0594) | — | various |
| 7 | 10 | mostly ingested by b0594-b0596 | — | — |
| 8 | 10 | 1 (Rotor-Moulder, b0613) | 8 | 1 misattach |
| 9 | 10 | **0** | **8** | 2 rulings skipped |

**The cliff is real:** pages 1–7 yielded text-PDFs almost exclusively; pages
8–9 are 100% scanned. This is consistent with the judiciary upload pipeline
having shifted from image scans to text-PDFs around mid-2023 / early 2024.
The chronological ordering of the listing (most-recent-first) places older
uploads on higher page numbers, where image-scan format dominates.

**Implication:** continuing the JIW sweep deeper than page 9 (i.e. into
2023 and earlier judgments) will produce **zero JIW ingestions** until OCR
is run. The repair-worker `ocrmypdf-scanned-coa-pdfs` queue is now the
binding constraint on Court of Appeal coverage growth.

**Operator decision suggested:** consider whether the JIW sweep should
continue probing pages 10+ at the cost of bandwidth (~3 MB/PDF × 8/page),
or pause CoA sweep until the OCR backlog (now 26 records) is drained.

## Integrity checks (no records mutated, but verified)

- **CHECK1** (every judgment has ≥1 judge): N/A — no inserts.
- **CHECK2** (issue_tags non-empty): N/A — no inserts.
- **CHECK3** (outcome from enum): N/A — no inserts.
- **CHECK4** (judges resolve in registry): N/A — no inserts.
- **CHECK5** (no duplicate IDs): PASS — no new IDs.
- **CHECK6** (raw_sha256 matches disk): N/A — no records inserted; raw
  PDFs saved with sha256 captured for future OCR ingestion.
- **CHECK7** (no dup case_name+court+date): N/A — no inserts.
- **CHECK8** (records count == records_fts count): **PASS** —
  records=1917, records_fts=1917 (unchanged).
- FTS5 internal integrity-check (`INSERT INTO records_fts(records_fts) VALUES('integrity-check')`):
  **PASS** at start and end of tick.

## Sweep position next tick (b0619)

`judiciary-coa-sweep: page 10` — 0 of N posts classified.

Page 9 is **ARCHIVED** (fully classified). Page 10 has not yet been
scouted at JIW level. Recommended approach:

1. Fetch `https://judiciaryzambia.com/category/resources/decisions/court-of-appeal-decisions/page/10/`
   listing (1 fetch).
2. Extract canonical slugs and titles.
3. **Smart-probe**: given the page 8–9 trend (100% scanned), consider
   probing only 1–2 candidates at most before deciding whether to halt
   the deeper-page sweep entirely and pivot to a different priority
   stream (e.g. ZambiaLII Supreme Court / Constitutional Court, or
   queue-management on the OCR backlog).
4. Alternative pivot streams (operator decision):
   - **Priority (c) — SCZ sweep**: ZambiaLII `/ZMSC/` direct HTML
     ingestion has been productive historically; no text-PDF dependency.
   - **Priority (d) — ZMCC sweep**: same as SCZ but smaller corpus.
   - **Priority (e) — HCJ sweep**: very large corpus; cherry-pick
     landmark decisions only.

## Operator action items (running list)

- (a) FTS5 rebuild action — **COMPLETED** at b0608 host-side sweep.
- (b) `ocrmypdf-scanned-coa-pdfs` repair-worker task — outstanding;
  now **26 records** waiting (was 18). **+8 page-9 records added this tick.**
- (c) Chisumpa Liandisha source-side fix — outstanding; needs editor
  contact at judiciaryzambia.com.
- (d) Zanaco Bank v Allan Kandala post-misattachment — outstanding;
  needs editor contact at judiciaryzambia.com.
- (e) Maxwell Banda post-no-attachment-stub — outstanding; needs editor
  contact or alternate-source retrieval.
- (f) **NEW (recommendation)**: operator decision on whether to continue
  CoA sweep deeper than page 9 given the now-confirmed scanned-PDF cliff,
  or pivot to a non-blocked priority stream (SCZ/ZMCC/HCJ via ZambiaLII).

## B2 sync

`B2 sync deferred to host (rclone not in sandbox)`.

UA: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
