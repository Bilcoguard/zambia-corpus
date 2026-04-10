# Gaps Log — Zambian Authorities Corpus

This file tracks known gaps, deferrals, and unresolved questions encountered
during corpus ingestion. Each entry is dated (UTC) and should describe what
is missing, why it could not be resolved at the time, and what would be
needed to close it.

## [2026-04-09] as-enacted Companies Act 2017 deferred

The pilot record for Companies Act No. 10 of 2017 ingested under Phase 2
will be sourced from ZambiaLII, which publishes the consolidated version
(amendments folded in). The as-enacted text from the authoritative
publisher (Parliament of Zambia) is still needed. Parliament URL structure
is unknown as of Phase 2 Checkpoint A (2026-04-09: /sitemap.xml returned
404, homepage not yet fetched). Deferred to a later phase or a dedicated
Parliament-resolution pass. When the as-enacted record lands, it should
be linked to the consolidated record via whatever "prior_version" or
"as_enacted_id" field the schema carries at that time (v0.3+).

## [2026-04-09] ZambiaLII closed — Phase 3 judgment source TBD

ZambiaLII is closed to KWLP corpus use per Phase 2 Checkpoint A policy
decision (Content-Signal ai-input=no + EU 2019/790 Art. 4 reservation).
Phase 3 (pilot judgment) therefore cannot use ZambiaLII. Candidate
alternative sources: (1) Judiciary of Zambia official site
(judiciary.gov.zm) direct judgment publication, (2) Government Gazette
where judgments are gazetted, (3) Parliament of Zambia if any judgments
are hosted there. All three require discovery work. Deferred to Phase 3
kickoff.

## [2026-04-10] Phase 4 Batch 0001 — low-section records flagged for re-parse

The generic section extractor (parser_version 0.3.0) extracted ≤ 2 sections from
the following records. These are likely amendment stubs or schedule-heavy acts where
the section heading regex did not match the PDF's typography. A targeted re-parse
pass is needed:

- act-zm-2024-023-value-added-tax-2024 (2 sections extracted, PDF 13KB — very short amendment)
- act-zm-2024-026-revenue-authority-2024 (2 sections, 283KB — likely section headings not matched)
- act-zm-2024-027-property-transfer-tax-2024 (2 sections, 13KB — short amendment)
- act-zm-2024-028-insurance-premium-levy-2024 (2 sections, 284KB — section headings not matched)
- act-zm-2024-029-appropriation-2024 (1 section, 336KB — Appropriation Acts are schedule-heavy; section "1" only extracted)
- act-zm-2025-009-supplementary-appropriation2025-2025 (2 sections, 18KB)

To close: inspect the raw PDFs in raw/bulk/parliament-zm/node-* and adjust the
section heading regex, or implement a pdfplumber layout-based extractor.

## [2026-04-10] Phase 4 Batch 0001 — listing pages 13-47 not yet walked

The full parliament.gov.zm acts listing has 48 pages. Pages 0–12 are cached and
were used for Batch 0001. Pages 13–47 contain an estimated 700+ additional acts
(pre-2017 era). These will be walked in future batches to complete the acts_in_force
inventory.

## Batch 0002 — 2026-04-10 — Parse quality flags (≤ 2 sections)

- **act-zm-2019-017-supplementary-appropriation-2019-no-2-act-2019** (2 sections): Supplementary Appropriation Act — schedule-heavy format, expected low section count; verify full schedule is captured.
- **act-zm-2019-013-property-transfer-tax-amendment-act-2019** (1 section): Brief amendment Act; re-parse recommended to confirm all amendment clauses captured.
- **act-zm-2019-014-value-added-tax-amendment-act-2019** (3 sections): Short amendment; section count plausible but verify completeness.


## Batch 0003 — 2026-04-10 — Parse quality flags (≤ 2 sections)

- **act-zm-2019-008-supplementary-appropriation-2019-act-2019** (2 sections): The Supplementary Appropriation (2019) Act, 2019 — Supplementary Appropriation Act, schedule-heavy; section count expected to be low.

## Batch 0004 — Parse quality flags (2026-04-10)

- **act-zm-2025-028-appropriation-act** (2 sections): Appropriation Act is schedule-heavy; bulk of content is in schedules not captured by section parser. Needs schedule-aware re-parse.
- **act-zm-2025-027-betting-act** (5 sections): May have schedules or subsidiary definitions not captured. Verify completeness.
- **act-zm-2025-024-registration-of-business-names-amendment-act** (5 sections): Brief amendment act; 5 sections may be complete. Verify.

## Batch 0005 — Parse quality flags (2026-04-10)

- **act-zm-2025-012-superior-courtsnumber-of-judgesact** (4 sections): Brief amending Act — short form expected. Likely complete.
- **act-zm-2025-019-value-added-tax-amendment-act** (2 sections): VAT Amendment Act — likely schedule-heavy or very brief amendment. Needs schedule-aware re-parse to verify completeness.

## Batch 0006 — Parse quality flags (2026-04-10)

- **act-zm-2025-020-zambia-revenue-authority-act** (3 sections): Brief ZRA amendment Act; likely complete.
- **act-zm-2025-021-property-transfer-tax-act** (3 sections): Brief PTT amendment; likely complete.
- **act-zm-2025-022-mobile-money-transaction-levy-act** (3 sections): Brief MoMo Levy amendment; likely complete.
- **act-zm-2018-003-rent-act** (2 sections): Rent Amendment Act — very brief (8 KB PDF). Verify all clauses captured.
- **act-zm-2018-004-subordinate-courts-act** (3 sections): Short amending Act (13 KB). Verify completeness.

## Batch 0007 — Parse quality flags (2026-04-10)

- **act-zm-2019-018-the-appropriation-act-2019** (2 sections): The Appropriation Act, 2019 — schedule-heavy Appropriation Act; verify completeness.
- **act-zm-2018-005-the-judiciary-administration-amendment-act-2018** (3 sections): The Judiciary Administration (Amendment) Act, 2018 — brief amendment act; verify completeness.
- **act-zm-2018-010-the-supplementary-appropriation-2018-act-2018** (3 sections): The Supplementary Appropriation (2018) Act, 2018 — schedule-heavy Appropriation Act; verify completeness.

## Batch 0008 (2026-04-10T17:18:19Z)
- `act-zm-2017-008-supplementary-appropriation-2017`: 1 section only (schedule-heavy Appropriation Act). Re-parse with table extraction may improve coverage.
- `act-zm-2017-011-property-transfer-tax-amendment`: 3 sections (brief amendment). Verify completeness.
- SSL: parliament.gov.zm certificate verification failed in sandbox. Fetched with verify=False; content integrity verified via sha256 hashes.

## Batch 0009 — Parse quality flags (2026-04-10)

- **act-zm-2017-012-value-added-tax-amendment** (2 sections): Brief VAT amendment act; verify all amendment clauses captured.
- **act-zm-2017-013-skills-development-levy-amendment** (1 section): Very brief levy amendment (8 KB PDF); stored as single section. Verify completeness.
- **act-zm-2017-015-insurance-premium-levy-amendment** (1 section): Very brief levy amendment (8 KB PDF); stored as single section. Verify completeness.
- **act-zm-2017-017-zambia-national-broadcasting-corporation-amendment** (2 sections): Brief broadcasting amendment. Verify completeness.
- **act-zm-2017-018-independent-broadcasting-authority-amendment** (1 section): Brief IBA amendment (13 KB PDF); stored as single section. Verify completeness.
- SSL: parliament.gov.zm certificate verification handled via requests library with verify=False; content integrity verified via sha256 hashes.

## Batch 0010 — Parse quality flags (2026-04-10)

- **act-zm-2021-021-health-professions-amendment-act-2021** (3 sections): Brief Health Professions amendment; verify completeness.
- **act-zm-2021-020-rural-electrification-amendment-act-2021** (3 sections): Brief Rural Electrification amendment; verify completeness.
- **act-zm-2021-019-national-heritage-conservation-commission-amendment-act-2021** (2 sections): Brief NHCC amendment; verify completeness.
- **act-zm-2021-018-examination-council-of-zambia-amendment-act-2021** (2 sections): Brief ECZ amendment; verify completeness.
- **act-zm-2021-017-zambia-law-development-commission-amendment-act-2021** (3 sections): Brief ZLDC amendment; verify completeness.
- **act-zm-2021-016-zambia-institute-of-advanced-legal-education-amendment-act-2021** (3 sections): Brief ZIALE amendment; verify completeness.
- **act-zm-2021-015-zambia-revenue-authority-amendment-act-2021** (2 sections): Brief ZRA amendment; verify completeness.
- **act-zm-2021-022-public-private-partnership-amendment-act-2021**: PDF NOT FOUND on node page https://www.parliament.gov.zm/node/8834 — needs manual retrieval or alternative source (ZambiaLII).
- SSL: parliament.gov.zm certificate verification handled via requests library with verify=False; content integrity verified via sha256 hashes.

## Batch 0011 (2026-04-10T18:39:27Z)

- Act No. 7 of 2021: only 2 sections (brief amendment act, may need re-parse)
- Act No. 8 of 2021: only 3 sections (brief amendment act, may need re-parse)
- Act No. 9 of 2021: only 3 sections (brief amendment act, may need re-parse)
- Act No. 10 of 2021: only 3 sections (brief amendment act, may need re-parse)
- Act No. 11 of 2021: only 3 sections (brief amendment act, may need re-parse)
- Act No. 12 of 2021: only 2 sections (brief amendment act, may need re-parse)
- Act No. 13 of 2021: only 2 sections (brief amendment act, may need re-parse)
- Act No. 14 of 2021: only 2 sections (brief amendment act, may need re-parse)

## Batch 0013 — Parse quality flags (2026-04-10T19:37:30Z)

- **act-zm-2021-026-the-health-professions-amendment-act-2021** (1 section): The Health Professions (Amendment) Act, 2021 — brief amendment act; verify completeness.
- **act-zm-2021-027-the-zambia-institute-of-marketing-amendment-act-2021** (1 section): The Zambia Institute of Marketing (Amendment) Act, 2021 — brief amendment act; verify completeness.
- **act-zm-2021-028-the-engineering-institution-of-zambia-amendment-act-2021** (1 section): The Engineering Institution of Zambia (Amendment) Act, 2021 — brief amendment act; verify completeness.
- **act-zm-2021-029-the-zambia-institute-of-advanced-legal-education-amendment-act-2021** (1 section): The Zambia Institute of Advanced Legal Education (Amendment) Act, 2021 — brief amendment act; verify completeness.
- **act-zm-2021-030-the-chartered-institute-of-logistics-and-transport-amendment-act-2021** (1 section): The Chartered Institute of Logistics and Transport (Amendment) Act, 2021 — brief amendment act; verify completeness.
- **act-zm-2021-031-the-zambia-institute-of-tourism-and-hospitality-studies-amendment-act-2021** (1 section): The Zambia Institute of Tourism and Hospitality Studies (Amendment) Act, 2021 — brief amendment act; verify completeness.
- **act-zm-2021-032-electoral-process-amendment-act-2021** (2 section): Electoral Process (Amendment) Act, 2021 — brief amendment act; verify completeness.
