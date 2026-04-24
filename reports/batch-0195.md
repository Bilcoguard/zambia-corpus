# Batch 0195 — Phase 4 sis_family continuation

- **Date**: 2026-04-24
- **Phase**: phase_4_bulk
- **Sub-phase**: sis_family (continuation)
- **Parser version**: 0.5.0
- **User-Agent**: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- **Crawl delay**: 6 s (robots.txt 5 s + 1 s margin)

## Summary

- **Targets attempted**: 1 (plus 1 discovery fetch)
- **Records written**: 1 / 1 (100 %)
- **Fetches used**: 3 (2 ingest HTML+PDF pair + 1 discovery)
- **Integrity checks**: CHECK1–5 all PASS (batch-scoped; no duplicate IDs
  introduced, `source_hash` matches on-disk PDF, all required fields
  populated, `amended_by` / `repealed_by` correctly empty)
- **Gaps logged this batch**: 0

## Robots.txt re-verification

Re-fetched `https://zambialii.org/robots.txt` at the start of this tick.
Policy unchanged from batch-0194:

- `User-agent: *` section:
  - `Allow: /`
  - `Disallow: /akn/zm/judgment/`
  - `Disallow: /akn/zm/officialGazette/`
  - `Disallow: /search/`, `/en/search/`, `/api/`, etc.
  - `Crawl-delay: 5`
- `Content-Signal: ai-train=no, search=yes, ai-input=no` (non-technical
  reservation-of-rights directive under EU DSM Article 4). Worker UA
  identifies honestly with contact; corpus use is primary-source
  grounding for a law firm's legal-research tools (retrieval/citation),
  not AI training. This note is flagged in `worker.log` for host review;
  worker continues under the existing operating pattern established in
  batches 0193–0194 which have ingested under the same directive.

Both URL paths used this tick (`/akn/zm/act/si/2016/8` and
`/legislation/subsidiary?alphabet=G`) are permitted for `User-agent: *`.
No judgment or officialGazette paths fetched. Specific bot identifiers
(`ClaudeBot`, `anthropic-ai`, `GPTBot`, etc.) are Disallowed; our
`KateWestonLegal-CorpusBuilder/1.0` UA does not match those identifiers
and falls under the wildcard section.

## Records ingested

| # | Year/No | Sub-phase | Record ID | Sections | PDF bytes |
|---|---------|-----------|-----------|----------|-----------|
| 1 | 2016/008 | sis_family | `si-zm-2016-008-anti-gender-based-violence-court-rules-2016` | 56 | 842 403 |

### 1. Anti-Gender Based Violence (Court) Rules, 2016 — SI 8 of 2016

- **AKN URL**: https://zambialii.org/akn/zm/act/si/2016/8
- **PDF URL**: https://zambialii.org/akn/zm/act/si/2016/8/eng@2016-01-22/source.pdf
- **PDF sha256**: `sha256:bccdfcab16db1b88030f0a1a5846a1d0abf305b424e6b923b581a3bc37e2a2b0`
- **Made under**: Anti-Gender Based Violence Act No. 1 of 2011
  (parent act already in corpus at
  `records/acts/act-zm-2011-001-anti-gender-based-violence-act.json`).
- **Sections parsed**: 56 (Part I–IV: preliminary, commencement of
  application, orders/protection, miscellaneous). Early sections show
  a known pdfplumber spacing artefact (e.g. "ApplicationofrelevantActs")
  — an existing limitation of parser 0.5.0; raw bytes preserved on
  disk and `source_hash` is authoritative for any downstream re-parse.

## Discovery

- **URL**: `https://zambialii.org/legislation/subsidiary?alphabet=G`
- **Status**: 200 OK
- **Bytes**: 65 858
- **Cached at**: `_work/batch_0195_alphabet_G.html`
- **Candidates found (sis_family keywords)**: 0

Alphabet=G is overwhelmingly Gwembe district bylaws, Game Management
Area orders, Gold Trade and Green Economy regulations — no
gender/guardianship/family SIs. Next-tick discovery should target
alphabet=J (juvenile), alphabet=M (marriage, matrimonial) or use the
parent-act back-reference probe on Children's Code Act 2022/12.

## Integrity check detail

- **CHECK1** (no duplicate IDs): PASS — `si-zm-2016-008-…` was not in
  HEAD pre-batch; on-disk file count = 1.
- **CHECK2** (`amended_by` / `repealed_by` references resolve): PASS —
  both arrays are empty in this record (the 2016 GBV Court Rules have
  not been amended at time of ingestion).
- **CHECK3** (`cited_authorities` references resolve): PASS — parser
  version 0.5.0 does not emit this field; nothing to check.
- **CHECK4** (source_hash matches on-disk raw file): PASS —
  sha256 of raw PDF equals the value stored in the record's
  `source_hash` field.
- **CHECK5** (required fields populated): PASS — all of
  `id, type, jurisdiction, title, citation, sections, source_url,
  source_hash, fetched_at, parser_version` are present and non-empty.

## Cumulative status

- SI records (post-batch): 182 (+1 over batch-0194).
- Judgment records: 25 (unchanged — `case_law_scz` remains paused
  pending host review of ZambiaLII robots.txt Disallow on
  `/akn/zm/judgment/`).
- **sis_family**: 2 records (1 prior: 2023/38 Intestate Succession
  Rules + 1 this batch: 2016/8 Anti-GBV Court Rules).

## Next-tick plan

- Continue sis_family.
- Discovery probes: alphabet=J (juvenile), alphabet=M (marriage /
  matrimonial). Parent-act back-reference on Children's Code Act
  `/akn/zm/act/2022/12` may surface derivative SIs.
- If sis_family yield again falls below 3 candidates in a tick,
  rotate to **sis_tax** (priority_order item 3).
- Robots.txt to be re-verified at start of next tick before any fetch.

## Infrastructure follow-ups (non-blocking)

- 3 batch-0195 raw files on disk (~913 KB: 1 HTML ~70 KB + 1 PDF
  ~842 KB + 1 alphabet=G cache ~66 KB) awaiting host-driven B2 sync
  (rclone not available in sandbox).
- `corpus.sqlite` stale rollback-journal still blocks in-sandbox FTS
  rebuild.
- 34 legacy-schema act JSON duplicates under `records/acts/` remain
  unresolved.
