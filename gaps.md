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

