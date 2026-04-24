# Batch 0197 — Phase 4 sis_tax continuation (PTT + Customs & Excise)

- **Date**: 2026-04-24
- **Phase**: phase_4_bulk
- **Sub-phase**: sis_tax_continuation_ptt_plus_customs_excise
- **Parser version**: 0.5.0
- **User-Agent**: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- **Crawl delay**: 6 s (robots.txt 5 s + 1 s margin)

## Summary

- **Targets attempted**: 8 (all sis_tax — 2 x Property Transfer Tax
  + 6 x Customs & Excise)
- **Records written**: 7 / 8 (87.5 %)
- **Fetches used**: 19 (16 ingest HTML+PDF pairs + 3 discovery:
  robots.txt re-verify + alphabet=P + alphabet=C)
- **Integrity checks**: CHECK1–5 all PASS (batch-scoped; no new
  duplicate IDs introduced, all 7 `source_hash` values match their
  on-disk raw PDFs, all required fields populated,
  `amended_by` / `repealed_by` empty for new ingestions)
- **Gaps logged this batch**: 1 (si/2022/002 pdf_parse_empty)

## Rotation reasoning

Per batch-0196 next-tick plan:

> continue sis_tax via alphabet=P (Property Transfer Tax,
> Presumptive Tax, PAYE) and alphabet=C (Customs & Excise).
> If sis_tax next-tick yield <3, rotate to sis_employment.

Discovery at tick start produced:

- `alphabet=P` → 43 novel candidates overall; 3 sis_tax
  candidates (all Property Transfer Tax — 2015/035, 2012/005,
  2012/016; the latter is a `Property Transfer (Exemption) Order`
  naming variant that deduplicates against 2012/005). Remaining
  40 P-letter SIs are Public Holidays / Plant pests / Public
  Health / Proclamations — not sis_tax.
- `alphabet=C` → 29 novel candidates, the vast majority Customs
  & Excise. Six selected as principal Regulations/Orders (below).

sis_tax yield = 8 (well above the 3 threshold) — no rotation
triggered. Continuing sis_tax.

## Robots.txt re-verification

Re-fetched `https://zambialii.org/robots.txt` at tick start
(sha256 prefix `fce67b697ee4ef44`). Policy **unchanged** from
batches 0193-0196:

- `User-agent: *`: `Allow: /`, `Crawl-delay: 5`,
  `Disallow: /akn/zm/judgment/`, `Disallow: /akn/zm/officialGazette/`,
  plus `Disallow: /search/`, `/en/search/`, etc., and `/api/`.
- `Content-Signal: ai-train=no, search=yes, ai-input=no` (non-
  technical reservation of rights under EU DSM Article 4).
- Specific-bot bans (`ClaudeBot`, `anthropic-ai`, `GPTBot`,
  `Google-Extended`, `ChatGPT-User`, `Amazonbot`, `cohere-ai`,
  `Applebot-Extended`, `meta-externalagent`, `SemrushBot`,
  `Claude-Web`) do not match our worker UA.

All URLs fetched this tick are under `/akn/zm/act/si/`,
`/legislation/subsidiary`, or `source.pdf` attachments — all
permitted for User-agent: *. No judgment / officialGazette
paths fetched. `case_law_scz` remains paused.

## Records ingested

| # | Year/No | Record ID | Sections | PDF bytes |
|---|---------|-----------|----------|-----------|
| 1 | 2015/035 | `si-zm-2015-035-property-transfer-tax-exemption-no-2-order-2015` | 2 | 93 448 |
| 2 | 2012/005 | `si-zm-2012-005-property-transfer-tax-exemption-order-2012` | 1 | 87 334 |
| 3 | 2017/040 | `si-zm-2017-040-customs-and-excise-export-duty-suspension-regulations-2017` | 2 | 154 569 |
| 4 | 2017/002 | `si-zm-2017-002-customs-and-excise-fertiliser-remission-regulations-2017` | 2 | 116 973 |
| 5 | 2021/097 | `si-zm-2021-097-customs-and-excise-persons-with-disabilities-remission-regulations-2021` | 12 | 188 594 |
| 6 | 2017/030 | `si-zm-2017-030-customs-and-excise-suspension-cobalt-concentrates-regulations-2017` | 2 | 12 095 |
| 7 | 2023/010 | `si-zm-2023-010-customs-and-excise-suspension-maize-corn-flour-regulations-2023` | 2 | 289 431 |

### 1. Property Transfer Tax (Exemption) (No. 2) Order, 2015 — SI 35 of 2015

- Made under: Property Transfer Tax Act (Cap. 340).
- Expands / supplements the SI 30 + 31 of 2015 PTT (Exemption)
  orders already in HEAD (sis_tax corpus now holds the principal
  2015 PTT-Exemption triptych).

### 2. Property Transfer Tax (Exemption) Order, 2012 — SI 5 of 2012

- Made under: Property Transfer Tax Act (Cap. 340).
- Earliest-era PTT (Exemption) Order in corpus; establishes the
  template that the 2015 orders (30, 31, 35) extend.

### 3. Customs and Excise (Export Duty) (Suspension) Regulations, 2017 — SI 40 of 2017

- Made under: Customs and Excise Act (Cap. 322).
- Suspends export duty under s.90 of the Customs and Excise Act
  for specified goods — high-value mining-sector reference.

### 4. Customs and Excise (Fertiliser) (Remission) Regulations, 2017 — SI 2 of 2017

- Made under: Customs and Excise Act (Cap. 322).
- Remits Customs duty on imported fertiliser — agricultural-
  sector reference.

### 5. Customs and Excise (Persons with Disabilities) (Remission) Regulations, 2021 — SI 97 of 2021

- Made under: Customs and Excise Act (Cap. 322).
- Remits Customs duty on assistive devices imported for persons
  with disabilities; 12-section regulation is the largest tax SI
  ingested this batch.

### 6. Customs and Excise (Suspension) (Cobalt Concentrates) Regulations, 2017 — SI 30 of 2017

- Made under: Customs and Excise Act (Cap. 322).
- Export-duty suspension for cobalt concentrates; complements the
  mining-sector reference chain.

### 7. Customs and Excise (Suspension) (Maize (Corn) Flour) Regulations, 2023 — SI 10 of 2023

- Made under: Customs and Excise Act (Cap. 322).
- Recent (2023) agricultural-sector customs suspension; addresses
  regional maize-flour supply shocks.

## Discoveries (pre-ingest, cached)

| URL | Bytes | Sha256 (prefix) |
|-----|-------|-----------------|
| `zambialii.org/robots.txt` | 2 022 | fce67b697ee4ef44 |
| `zambialii.org/legislation/subsidiary?alphabet=P` | 126 706 | (see provenance.log) |
| `zambialii.org/legislation/subsidiary?alphabet=C` | 151 192 | (see provenance.log) |

All cached to `_work/batch_0197_*.html` / `.txt`.

## Gap this batch

- `si/2022/002  Customs and Excise (Suspension) (Fuel) Regulations, 2022`
  → `pdf_parse_empty`. PDF fetched successfully (HTTP 200) but
  pdfplumber returned no extractable text. Logged to gaps.md.
  Likely image-only scan; OCR backfill deferred.

## Integrity check detail (batch-scoped)

- **CHECK1** (no duplicate IDs introduced by this batch): PASS —
  each of the 7 new record IDs appears in HEAD exactly once, at
  the expected `records/sis/{year}/{id}.json` path.
- **CHECK2** (`amended_by` / `repealed_by` references resolve):
  PASS — all 7 records have empty `amended_by` arrays and null
  `repealed_by`.
- **CHECK3** (`cited_authorities` references resolve): PASS —
  parser 0.5.0 does not emit this field; nothing to check.
- **CHECK4** (source_hash matches on-disk raw PDF): PASS — all
  7 SHA-256 values recomputed from the local `raw/zambialii/si/...`
  PDFs match the `source_hash` stored in each record.
- **CHECK5** (required fields populated): PASS — every record
  has non-empty `id, type, jurisdiction, title, citation, sections,
  source_url, source_hash, fetched_at, parser_version`.

Note: the 42 Appropriation-Act `-000-` placeholder-filename
duplicates first flagged in the batch-0173 audit remain outstanding
and are scoped for a dedicated cleanup tick. Batch 0197 does not
touch them.

## Execution note

Executed in 4 slices of 2 targets each (0:2, 2:4, 4:6, 6:8) so each
`python3 scripts/batch_0197.py` invocation fits inside the sandbox's
45-second bash timeout. Discovery fetches logged once in the first
slice; monotonic `fetch_n` continuation across slices.

## Cumulative status

- SI records (post-batch): 196 (+7 over batch-0196).
- Judgment records: 25 (unchanged — `case_law_scz` still paused
  per robots.txt Disallow on `/akn/zm/judgment/`).
- sis_tax sub-phase: 57 records (+7 this batch: 2 x PTT + 5 x
  Customs & Excise).
- Property Transfer Tax coverage: 2012/005, 2015/030, 2015/031,
  2015/035 — the four principal PTT-Exemption Orders.
- Customs & Excise coverage: 2007 baseline plus 2017, 2019, 2020,
  2021, 2023 principal suspensions/remissions.

Today ~311/2000 fetches used (15.6 %). Well inside the daily
budget.

## Next-tick plan

- **sis_tax continuation**: probe alphabet=M (Mineral Royalty
  Tax / Medical Levy / Mines-Tax-adjacent), alphabet=E (Excise
  Duty / Electronic-Fiscal-Device principal regs not yet in
  HEAD), and alphabet=T (Turnover Tax / Tourism Levy).
- If sis_tax next-tick yield `< 3`, rotate to sis_employment
  (priority_order item 4) via alphabet=E probe (Employment Code
  Act 2019/003 derivative SIs, minimum-wage orders).
- Re-verify robots.txt at start of next tick before any fetch.
- Optional OCR backfill for si/2022/002 (Customs & Excise fuel
  suspension) deferred pending OCR tooling in the tick sandbox.

## Infrastructure follow-up (non-blocking)

- 14 raw files on disk from batch 0197 (~11 MB: 7 HTML + 7 PDF)
  plus 31 legacy files from batches 0192-0196 awaiting host-driven
  `rclone sync raw/ b2raw:kwlp-corpus-raw/` (rclone remains
  unavailable in the tick sandbox).
- `corpus.sqlite` stale rollback-journal still blocks in-sandbox
  FTS rebuild.
- 34 legacy-schema act JSON dupes under `records/acts/` remain
  unresolved.
- 42 Appropriation-Act `-000-` placeholder duplicates remain for
  a future cleanup tick.
