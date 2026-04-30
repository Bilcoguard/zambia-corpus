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

## Batch 0014 — Parse quality flags (2026-04-10T20:05:49Z)

- **act-zm-2020-005-the-landlord-and-tenant-business-premises-amendment-act-2020** (2 sections): The Landlord and Tenant (Business Premises) (Amendment Act), 2020 — brief act or parse issue; verify completeness.

## Batch 0017 — Parse quality flags (2026-04-10T22:32:15Z)

- **act-zm-2022-026-the-value-added-tax-amendment-act-2022** (4 sections): Brief act; verify completeness.
- **act-zm-2022-027-the-property-transfer-tax-amendment-act-2022** (2 sections): Brief act; verify completeness.
- **act-zm-2022-028-the-pension-scheme-regulation-amendment-act-2022** (2 sections): Brief act; verify completeness.
- **act-zm-2022-029-the-mines-and-minerals-development-amendment-act-2022** (2 sections): Brief act; verify completeness.
- **act-zm-2022-030-the-appropriation-act-2022** (2 sections): Brief act; verify completeness.
- 2022 Acts No. 1-22 still to ingest in future batches.

## Batch 0018 — 2026-04-10T22:43:52Z — Parse quality flags (≤ 5 sections)

- **act-zm-2026-004-criminal-procedure-code-amendment-act** (4 sections): Criminal Procedure Code (Amendment) Act 2026 — low section count; brief amendment act. Verify all amendment clauses captured.

### Batch 0019 — Low section count records (2026-04-11)
- **Act No. 26 of 2023** (Zambia Revenue Authority Amendment) — 3 sections. Amendment act, low count expected. Verify completeness on re-parse.
- **Act No. 27 of 2023** (Value Added Tax Amendment) — 2 sections. Amendment act, low count expected.
- **Act No. 28 of 2023** (Local Government Amendment) — 2 sections. Amendment act, low count expected.
- **Act No. 29 of 2023** (Appropriation Act) — 2 sections. Appropriation act, low count expected.

## Batch 0021 — Act No. 12 of 2023 connection error (2026-04-11)

- **Act No. 12 of 2023** (The Defence (Amendment) Act, 2023): Node page /node/11534 returned connection error (RemoteDisconnected). Retry in next batch.

### Batch 0021 — Low section count records (2026-04-11)
- **Act No. 10 of 2023** (Supplementary Appropriation) — 2 sections. Appropriation act, low count expected.
- **Act No. 15 of 2023** (Zambia Institute of Marketing Amendment) — 2 sections. Amendment act, low count expected.

### Batch 0022 — Low section count records (2026-04-11T01:07:47Z)
- **Act No. 19 of 2023** (4 sections): The Criminal Procedure Code (Amendment) Act, 2023. Amendment act, low count expected.
- **Act No. 20 of 2023** (3 sections): The Penal Code (Amendment) Act, 2023. Amendment act, low count expected.
- **Act No. 23 of 2023** (2 sections): The Subordinate Courts (Amendment) Act, 2023. Amendment act, low count expected.

## Batch 0024 — 2026-04-11

- **Act No. 6 of 2022** (The Judges (Conditions of Service) Act, 2022.): 5 sections — brief act, may need re-parse
- **Act No. 7 of 2022** (The Supplementary Appropriation (2022) Act, 2022.): 2 sections — brief act, may need re-parse

### Batch 0027 — Low section count records (2026-04-11T03:35:52Z)
- **Act No. 20 of 2022** (4 sections): National Pension Scheme (Amendment) Act. Amendment act, low count expected.
- **Act No. 22 of 2022** (8 sections): Criminal Procedure Code (Amendment) Act. Amendment act, low count expected.

### Batch 0030 — Low section count records (2026-04-11T05:38:28Z)
- **Act No. 9 of 2024** (Supplementary Appropriation) — 2 sections. Appropriation act, low count expected.
- **Act No. 15 of 2024** (ZNPHI Amendment) — 3 sections. Amendment act, low count expected.
- **Act No. 16 of 2024** (Judiciary Administration Amendment) — 2 sections. Amendment act, low count expected.

### Batch 0034 — Low section count records (2026-04-11T09:06:47Z)
- **The Income Tax (Amendment)** (3 sections): Amendment act, low count expected.
- **The Mines and Minerals Development (Amendment)** (3 sections): Amendment act, low count expected.
- **The Local Government (Amendment)** (3 sections): Amendment act, low count expected.

### Batch 0035 — 2016 Acts gap (2026-04-11)
- Could not find 2016 Acts No. 18+ on parliament.gov.zm listing pages 15-19
- May need to check different page range or alternative URL pattern

### Batch 0040 — 2015 Act No. 2 no PDF
- **Act No. 2 of 2015** (Anti-Terrorism (Amendment) Act, 2015): No PDF on https://www.parliament.gov.zm/node/4542

### Batch 0042 — 2015 Acts gaps
- **Act No. 10 of 2015** (The Zambia Wildlife Act): No PDF found on parliament.gov.zm
- **Act No. 14 of 2015** (The Appropriation Act): No PDF found on parliament.gov.zm
- **Act No. 15 of 2015** (The Zambia Institute of Chartered Accountants Act): No PDF found on parliament.gov.zm
- **Act No. 16 of 2015** (The National Health Insurance Act): No PDF found on parliament.gov.zm
- **Act No. 17 of 2015** (The Cyber Security and Cyber Crimes Act): No PDF found on parliament.gov.zm
- **Act No. 18 of 2015** (The Electronic Communications and Transactions Act): No PDF found on parliament.gov.zm
- **Act No. 19 of 2015** (The Public-Private Partnership Act): No PDF found on parliament.gov.zm
- **Act No. 20 of 2015** (The Planning and Budgeting Act): No PDF found on parliament.gov.zm

## Batch 0043 — 2026-04-11 — 2014 Acts missing PDFs

The following 2014 Acts have node pages on parliament.gov.zm but no PDF attachments.
These need to be sourced from an alternative location (ZambiaLII TDM reservation applies;
consider Government Gazette or direct MMMD/MoJ request).

- **Act No. 6 of 2014** — The Excess Expenditure Appropriation (2011) Act (node/2826)
- **Act No. 7 of 2014** — The Income Tax (Amendment) Act 2014 (node/2938)
- **Act No. 8 of 2014** — The Customs and Excise (Amendment) Act 2014 (node/2920)
- **Act No. 9 of 2014** — The Property Transfer Tax (Amendment) Act 2014 (node/2884)
- **Act No. 10 of 2014** — The Zambia Revenue Authority (Amendment) / Value Added Tax (Amendment) Act 2014 (node/2907, node/2941)
- **Act No. 11 of 2014** — The Mines and Minerals Development (Amendment) Act 2014 (node/2925)
- **Act No. 12 of 2014** — The Local Government (Amendment) Act 2014 (node/2911)

## Batch 0043 — 2026-04-11 — Parse quality flags

- **act-zm-2014-002** (1 section): Service Commissions Amendment — short amendment, may be complete; verify.
- **act-zm-2014-003** (1 section): Business Regulatory Act — 8.6MB PDF (likely scanned). Only 1 section extracted. Needs OCR re-parse.
- **act-zm-2015-023** (2 sections): Appropriation Act — schedule-heavy, expected low count.
- **act-zm-2014-005** (2 sections): Supplementary Appropriation Act — schedule-heavy, expected low count.

## Batch 0045 (2026-04-11)
- Act No. 8 of 2013: not found on parliament.gov.zm index (may not exist or not uploaded)
- Act No. 9 of 2013: not found on parliament.gov.zm index (may not exist or not uploaded)
- Act No. 10 of 2013: not found on parliament.gov.zm index (may not exist or not uploaded)
- Act No. 11 of 2013: not found on parliament.gov.zm index (may not exist or not uploaded)
- Act No. 17 of 2013: not found on parliament.gov.zm index (may not exist or not uploaded)
- Act No. 18 of 2013: not found on parliament.gov.zm index (may not exist or not uploaded)

### Batch 0046 — 2012 Acts gaps (2026-04-11 15:37 UTC)
- Act No. 9 of 2012 (Customs and Excise Amendment): No PDF on node page /node/3178
- Acts No. 6, 7, 8, 10, 11 of 2012: Scanned PDFs, OCR re-parse needed

### Batch 0047 — 2012/2011 Acts gaps (2026-04-11T16:08:46Z)
- No PDF on node page for 2012 Act No. 14 (https://www.parliament.gov.zm/node/3191)
- No PDF on node page for 2011 Act No. 24 (https://www.parliament.gov.zm/node/3368)
- No PDF on node page for 2011 Act No. 25 (https://www.parliament.gov.zm/node/3371)
- No PDF on node page for 2011 Act No. 26 (https://www.parliament.gov.zm/node/3414)
- No PDF on node page for 2011 Act No. 28 (https://www.parliament.gov.zm/node/3424)

### Batch 0048 — 2011/2010/2009 Acts gaps (2026-04-11T16:36:29Z)
- No PDF on node page for 2011 Excess Expenditure Appropriation Act
- No PDF on node page for 2011 Mines and Minerals Development (Amendment) Act
- 4 duplicate IDs detected and cleaned (slug variation with/without 'the-' prefix)

## Batch 0050 (2026-04-11T17:39:55Z)
- act-zm-2011-008-the-supreme-court-amendment-act-2011: 0 sections parsed — likely scanned PDF, needs OCR re-parse
- act-zm-2011-009-the-zambia-institute-of-advanced-legal-education-amendment-act-2011: 0 sections parsed — scanned PDF (1.2MB), needs OCR re-parse

### Batch 0051 — 2011/2010 Acts gaps (2026-04-11T18:08:21Z)
- act-zm-2010-050-property-transfer-tax-amendment: 0 sections parsed — scanned/image PDF, needs OCR re-parse
- act-zm-2010-049-income-tax-amendment: 0 sections parsed — scanned/image PDF, needs OCR re-parse
- act-zm-2010-048-value-added-tax-amendment: 0 sections parsed — scanned/image PDF, needs OCR re-parse
- act-zm-2010-047-customs-and-excise-amendment: 0 sections parsed — scanned/image PDF, needs OCR re-parse
- act-zm-2010-046-financial-intelligence-centre-2010: 0 sections parsed — scanned/image PDF, needs OCR re-parse

### Batch 0052 — gaps (2026-04-12T11:42:11.107764+00:00)
- act-zm-2010-045-veterinary-and-veterinary-para-professions-2010: 0 sections — scanned PDF, needs OCR
- act-zm-2010-044-prohibition-and-prevention-of-money-laundering-amendment: 0 sections — scanned PDF, needs OCR
- act-zm-2010-043-citizens-economic-empowerement-amendment: 0 sections — scanned PDF, needs OCR
- act-zm-2010-041-lands-amendment: 0 sections — scanned PDF, needs OCR
- act-zm-2010-040-lands-and-deeds-registry-amendment: 0 sections — scanned PDF, needs OCR
- act-zm-2010-039-lands-tribunal-2010: 0 sections — scanned PDF, needs OCR

- 2010 Act No. 26: No PDF on node page (https://www.parliament.gov.zm/node/3365)
- 2010 Act No. 23: No PDF on node page (https://www.parliament.gov.zm/node/3356)
### Batch 0055 — Gaps (2026-04-12T14:45:12Z)
- Act No. 1 of 2010 (The Zambia Development Agency): Scanned PDF, needs OCR re-parse. 0 chars extracted.

### Batch 0056 — Gaps (2026-04-12T16:50:00Z)
- Act No. 26 of 2010 (Independent Broadcasting Authority Amendment): No PDF on node page (https://www.parliament.gov.zm/node/3365) — confirmed again
- act-zm-2009-030-appropriation: 0 sections — scanned PDF, needs OCR re-parse

## [2026-04-12] Phase 4 Batch 0057 — 2009 Acts gaps

- **Act No. 21 of 2009** (Electronic Communications and Transactions Act): No PDF link on parliament.gov.zm node /node/3581. May need alternative source.
- **Act No. 13 of 2009** (Ministerial and Parliamentary Offices (Emoluments) (Amendment)): No PDF link on parliament.gov.zm node /node/3637. May need alternative source.
- **act-zm-2009-020-constitution-of-zambia-amendment**: 1 section extracted — scanned PDF, needs OCR re-parse.
- **act-zm-2009-018-zambia-law-development-commission-amendment-act-2009**: 1 section extracted — scanned PDF, needs OCR re-parse.
- **act-zm-2009-012-presidential-emoluments-amendment**: 1 section extracted — scanned PDF, needs OCR re-parse.

### Batch 0060 — Gaps (2026-04-13T04:31:34Z)
- act-zm-2007-024-zambia-tourism-board: scanned PDF, needs OCR
- 2008 Acts: No. 1-5, 8, 11, 13+ not discoverable on parliament.gov.zm. Need ZambiaLII or Gazette sources.

### Batch 0061 — Gaps (2026-04-13T06:45:00Z)
- act-zm-2001-009-the-customs-and-excise-amendment-act-no-9-of-2001: 0 sections — scanned PDF, needs OCR
- act-zm-2001-008-the-income-tax-amendment-act-no-8-of-2001: 0 sections — scanned PDF, needs OCR
- act-zm-2000-020-the-penal-code-amendment-act-no-20-of-2000: 0 sections — scanned PDF, needs OCR
- act-zm-2000-007-excess-expenditure-appropriation-1994-act-no-7-of-2000: 0 sections — scanned PDF, needs OCR
- act-zm-2000-006-the-value-added-tax-amendment-act-no-6-of-2000: 0 sections — scanned PDF, needs OCR
- Discovery pages 27-34 contain many navigation links mixed with act links; actual act yield ~8 per 8 pages

## Batch 0062 — Strategy note (2026-04-13T05:40:40Z)
- Pages 35+ of parliament.gov.zm listing contain Laws of Zambia (Chapter Acts) without year/number in titles
- Successfully extracting Cap. numbers from PDF first pages
- Remaining Cap. Acts from pages 35-36 for next tick: Tourism Act, Water Act, National Heritage Conservation Commission Act, Rating Act, National Housing Authority Act, Agricultural Lands Act, ZNBC Act, Landlord and Tenant Act, Housing (Statutory) Act, and more

## [2026-04-13] Phase 4 Batch 0064 — Gaps

- Constitution Amendment Act 2016: duplicate of act-zm-2016-002, removed
- Lands Act: duplicate of act-zm-cap-184-lands-act (same hash), removed
- 5 Laws of Zambia chapter acts have no extractable Cap. number (tagged loz-*): need manual Cap. assignment from Laws of Zambia index

## Batch 0065 (2026-04-13T07:12:12Z)

- Anti-Terrorism (Amendment) Act, 2015: no PDF link on node page (https://www.parliament.gov.zm/node/4542)
- The Zambia Revenue Authority (Amendment): no PDF link on node page (https://www.parliament.gov.zm/node/2907)
- The Companies (Amendment) Act (2011): no PDF link on node page (https://www.parliament.gov.zm/node/3368)

### Batch 0066 — Laws of Zambia Cap. gaps (2026-04-13T08:09:53Z)
- **About Parliament**: No PDF on https://www.parliament.gov.zm/node/108
- **Parliament Buildings History**: No PDF on https://www.parliament.gov.zm/node/111
- **Departments**: No PDF on https://www.parliament.gov.zm/node/159
- **Visiting parliament**: No PDF on https://www.parliament.gov.zm/node/110
- **Committee System**: No PDF on https://www.parliament.gov.zm/node/109
- **Attendance Guidlines**: No PDF on https://www.parliament.gov.zm/node/91
- **Submission Procedure**: No PDF on https://www.parliament.gov.zm/node/444
- **Committee Submission**: No PDF on https://www.parliament.gov.zm/node/210
- **Up Coming Events**: No PDF on https://www.parliament.gov.zm/node/12899

## Batch 73 — Workers' Compensation Act, 1999
- act-zm-cap-271-workers-compensation-act: 404 at https://zambialii.org/akn/zm/act/1999/10/eng@2005-12-31 — may need alternative AKN path

## Batch 73 — Factories Act, 1966
- act-zm-cap-441-factories-act: 404 at https://zambialii.org/akn/zm/act/1966/17/eng@1996-12-31 — may need alternative AKN path

## Batch 73 — Public Holidays Act, 1965
- act-zm-cap-272-public-holidays-act: 404 at https://zambialii.org/akn/zm/act/1965/3/eng@1996-12-31 — may need alternative AKN path

## Batch 73 — Transferred Federal Officers (Pensions) Act, 1964
- act-zm-cap-266-transferred-federal-officers-pensions-act: 404 at https://zambialii.org/akn/zm/act/1964/62/eng@1996-12-31 — may need alternative AKN path

## Batch 73 — European Officers (Pensions) Act, 1964
- act-zm-cap-267-european-officers-pensions-act: 404 at https://zambialii.org/akn/zm/act/1964/63/eng@1996-12-31 — may need alternative AKN path

## Batch 73 — Public Officers (Change of Titles) Act, 1964
- act-zm-cap-265-public-officers-change-of-titles-act: 404 at https://zambialii.org/akn/zm/act/1964/5/eng@1996-12-31 — may need alternative AKN path

## Batch 73 — Employment (Exchange) Act, 1970
- act-zm-cap-273-employment-exchange-act: 404 at https://zambialii.org/akn/zm/act/1970/20/eng@1996-12-31 — may need alternative AKN path

## Batch 74 — Arbitration Act, 2000
- act-zm-2000-019-arbitration-act-2000: PDF is scanned images (no extractable text). Needs OCR or alternative source.

## Batch 0075 — Notes (2026-04-15T07:43:47Z)
- Access to Information Act 2023, Agricultural Credits Act 2010, Agricultural Institute of Zambia Act 2017, Animal Health Act 2010: HTML pages had 0 AKN sections; fell back to PDF source successfully.

## act-zm-2006-009-citizens-economic-empowerment-act (Batch 0080)
- Source: https://zambialii.org/akn/zm/act/2006/9/eng@2006-05-19/source.pdf
- Issue: Scanned PDF — 0 extractable text sections. Needs OCR or alternative source.
- Logged: 2026-04-15T00:00:00Z

## Batch 0082 — ZambiaLII Connectivity Failure (2026-04-15T14:30:00Z)
- All 8 targets failed due to SSL errors (UNEXPECTED_EOF_WHILE_READING) — zambialii.org appears to be experiencing infrastructure issues.
- Council of Law Reporting Act, 1967 returned HTTP 500.
- Targets deferred to next tick: Constitution of Zambia Act 1991, Constitution of Zambia Act 1996, Consular Conventions Act 1951, Control of Goods Act 1954, Copperbelt University Act 1987, Council of Law Reporting Act 1967, Dangerous Drugs Act 1967, Debtors Act 1938.

## Batch 0083 — Issues (2026-04-15T12:37:07Z)
- act-zm-1951-026-consular-conventions-act-1951: HTTP unknown
  URL: https://zambialii.org/akn/zm/act/1951/26/eng@1996-12-31
- act-zm-1954-015-control-of-goods-act-1954: HTTP unknown
  URL: https://zambialii.org/akn/zm/act/1954/15/eng@1996-12-31
- act-zm-1987-019-copperbelt-university-act-1987: HTTP unknown
  URL: https://zambialii.org/akn/zm/act/1987/19/eng@1996-12-31
- act-zm-1967-007-council-of-law-reporting-act-1967: HTTP unknown
  URL: https://zambialii.org/akn/zm/act/1967/7/eng@1996-12-31
- act-zm-1938-001-debtors-act-1938: HTTP unknown
  URL: https://zambialii.org/akn/zm/act/1938/1/eng@1996-12-31
## act-zm-2017-013 — Compulsory Standards Act, 2017 (Batch 0084)
- HTML: https://zambialii.org/akn/zm/act/2017/13/eng@2017-07-07 → status 404
- PDF: https://zambialii.org/akn/zm/act/2017/13/eng@2017-07-07/source.pdf → status 404
- Issue: Both HTML and PDF fetch failed.
- Logged: 2026-04-15T13:04:59Z

## act-zm-2018-011 — Constituency Development Fund Act, 2018 (Batch 0084)
- HTML: https://zambialii.org/akn/zm/act/2018/11/eng@2018-08-17 → status 404
- PDF: https://zambialii.org/akn/zm/act/2018/11/eng@2018-08-17/source.pdf → status 404
- Issue: Both HTML and PDF fetch failed.
- Logged: 2026-04-15T13:05:10Z

## act-zm-2023-029 — Consumer Credit Act, 2023 (Batch 0084)
- HTML: https://zambialii.org/akn/zm/act/2023/29/eng@2023-08-28 → status 404
- PDF: https://zambialii.org/akn/zm/act/2023/29/eng@2023-08-28/source.pdf → status 404
- Issue: Both HTML and PDF fetch failed.
- Logged: 2026-04-15T13:05:21Z

## act-zm-1964-047 — Control of Dogs Act, 1964 (Batch 0084)
- HTML: https://zambialii.org/akn/zm/act/1964/47/eng@1996-12-31 → status 404
- PDF: https://zambialii.org/akn/zm/act/1964/47/eng@1996-12-31/source.pdf → status 404
- Issue: Both HTML and PDF fetch failed.
- Logged: 2026-04-15T13:05:32Z

## act-zm-2017-009 — Corporate Insolvency Act, 2017 (Batch 0084)
- HTML: https://zambialii.org/akn/zm/act/2017/9/eng@2017-07-07 → status 404
- PDF: https://zambialii.org/akn/zm/act/2017/9/eng@2017-07-07/source.pdf → status 404
- Issue: Both HTML and PDF fetch failed.
- Logged: 2026-04-15T13:05:43Z

## act-zm-2021-037 — Correctional Service Act, 2021 (Batch 0084)
- HTML: https://zambialii.org/akn/zm/act/2021/37/eng@2021-12-31 → status 404
- PDF: https://zambialii.org/akn/zm/act/2021/37/eng@2021-12-31/source.pdf → status 404
- Issue: Both HTML and PDF fetch failed.
- Logged: 2026-04-15T13:05:54Z

## act-zm-2005-021 — Cotton Act, 2005 (Batch 0084)
- HTML: https://zambialii.org/akn/zm/act/2005/21/eng@2005-12-31 → status 404
- PDF: https://zambialii.org/akn/zm/act/2005/21/eng@2005-12-31/source.pdf → status 404
- Issue: Both HTML and PDF fetch failed.
- Logged: 2026-04-15T13:06:04Z


## Batch 0085 — Listing fetch failed
- URL: https://zambialii.org/legislation/act
- Error: Acts listing returned 404
- Logged: 2026-04-15T13:35:38Z


## Batch 0085 — Integrity check failures
- HASH MISMATCH: act-zm-1995-005-affiliation-and-maintenance-of-children-act-1995
- HASH MISMATCH: act-zm-1980-009-appropriation-act-1980
- HASH MISMATCH: act-zm-1981-012-appropriation-act-1981
- HASH MISMATCH: act-zm-1982-015-appropriation-act-1982
- HASH MISMATCH: act-zm-1983-014-appropriation-act-1983
- HASH MISMATCH: act-zm-1984-013-appropriation-act-1984
- HASH MISMATCH: act-zm-1985-016-appropriation-act-1985
- Logged: 2026-04-15T13:40:50Z


## 2026-04-15 Batch 0094 — PDF-only acts (0 sections from HTML)

- **High Court Act (Cap. 27)** — Act No. 41 of 1960: ZambiaLII HTML page is a landing stub. Full text in PDF (307.5 KB). URL: https://zambialii.org/akn/zm/act/1960/41/eng@1996-12-31. Record created with 0 sections. Needs PDF re-parse.
- **Judgments Act (Cap. 81)** — Act No. 10 of 1961: ZambiaLII HTML page is a landing stub. Full text in PDF (146.7 KB). URL: https://zambialii.org/akn/zm/act/1961/10/eng@1996-12-31. Record created with 0 sections. Needs PDF re-parse.

## Batch 0102 — 2026-04-16
- `act-zm-2025-2025-access-to-information-guidelines-2025`: Access to Information Guidelines, 2025 (GN 1624 of 2025) — 0 sections parsed from PDF. PDF may be scanned image or non-standard layout. Needs manual review or OCR re-parse.

## 2026-04-17 Batch 0117

- **Arbitration Act, 2000** (Act No. 19 of 2000): ZambiaLII source PDF is a scanned image (35 pages, 35 chars extracted). Cannot parse sections with pdfplumber. Requires OCR processing. Raw file saved at raw/zambialii/act-zm-2000-019-arbitration-act-2000.pdf. Record created with 0 sections — needs manual OCR or alternative source.
- **Cheques Act, 1959**: Already exists at records/acts/1959/act-zm-1959-005-cheques-act-1959.json (16 sections). New fetch has fewer sections (3). Duplicate flat file created but NOT committed.
- **Chiefs Act, 1965**: Already exists at records/acts/1965/act-zm-1965-067-chiefs-act-1965.json (37 sections). New fetch has fewer sections (9). Duplicate flat file created but NOT committed.

## Batch 0122 — Scanned PDFs (2026-04-17)
- **Local Courts Rules, 1966** (SI 293/1966): PDF is scanned image, no extractable text. Source: https://zambialii.org/akn/zm/act/si/1966/293/eng@1995-04-14. Needs OCR.
- **Local Courts (Administration of Estates) Rules, 1969** (SI 297/1969): PDF is scanned image, no extractable text. Source: https://zambialii.org/akn/zm/act/si/1969/297/eng@1969-06-06. Needs OCR.

- [2026-04-17T14:36:34.940563+00:00] Batch 130: 0-section result for 'Citizens Economic Empowerment Act, 2006' @ https://www.zambialii.org/akn/zm/act/2006/9/eng@2006-05-19

## Batch 0130 gaps (2026-04-17T14:43:48Z)
- Citizens Economic Empowerment Act, 2006 (Act No. 9 of 2006) — fetched HTML and PDF but both produced 0 parseable sections. Source: https://www.zambialii.org/akn/zm/act/2006/9/eng@2006-05-19
- 6 duplicate-content files remain as untracked orphans in the working tree (see reports/batch-0130.md for paths). Sandbox cannot delete; host must remove manually.
- Dedup strategy is URL-keyed; needs (year, act_num) tuple keying to catch cross-source re-ingestion from ZambiaLII vs Parliament.

## 2026-04-18 (Batch 0132)

- **National Water Supply and Sanitation Act** — not located on ZambiaLII via
  `/legislation/?q=` under any of: "Water Supply", "Water and Sanitation",
  "Zambian Water". Usually cited as Act No. 28 of 1997. Next tick: try
  ZambiaLII subject-browse index (ministry-of-water-development subject) or a
  Gazette search. Alternative source: parliament.gov.zm Acts archive.
- **National Tourism Board Act** — phantom target. ZambiaLII returns only
  "Zambia Tourism Board Act, 2007" (Act No. 24 of 2007), already ingested as
  `act-zm-2007-024-zambia-tourism-board`. No separate National Tourism Board
  Act exists; remove from future target lists.

## Batch 0134 integrity failures (2026-04-18T08:09:17Z)

- HASH MISMATCH: act-zm-2016-042-zambia-institute-for-tourism-and-hospitality-studies-act-2016 (raw=d828ca46d1ff... vs src=8b32657a319d...)

## Batch 0134 phantom targets (2026-04-18T08:18:28Z)

Targets from batch 0133's next-tick list not found on ZambiaLII via either `/search/api/documents/` or `/legislation/?page=` alphabetical index. Need alternative source (parliament.gov.zm, Gazette, Cap-numbered archive):

- Optometry Act
- Open University Act
- Organs of Government (Dispersal) Act
- National Water Supply and Sanitation Act
- Protected Disclosures Act
- Private Security Services Act
- Personal Property Security Interests Act

Note: the `/legislation/?q=` URL used in earlier batch notes is misleading — the `q` parameter is silently ignored and the page always returns the unfiltered listing. The real full-text search endpoint is `/search/api/documents/?search=<term>&nature=Act`, which returns a JSON envelope (`count`, `results_html`) but searches document full text — matches may not be title matches.

## Batch 0144 per-target notes (2026-04-20T12:03:35Z)

- registered-designs-1987 (Act 25/1987): title rejected (contains 'amendment'): 'Registered Designs (Amendment) Act, 1987'
- industrial-relations-act-1983 (Act 13/1983): title rejected (contains 'amendment'): 'Industrial Relations (Amendment) Act, 1983'
- candidate-2008-008 (Act 8/2008): title rejected (contains 'amendment'): 'Industrial and Labour Relations (Amendment) Act, 2008'

## Batch 0145 per-target notes (2026-04-20T12:12:50Z)

- banking-2000-018 (Act 18/2000): no parseable sections in HTML or PDF
- banking-2005-025 (Act 25/2005): title rejected (contains 'amendment'): 'Banking and Financial Services (Amendment) Act, 2005'
- lands-1985-015 (Act 15/1985): title rejected (contains 'amendment'): 'Land (Conversion of Titles) (Amendment) (No. 2) Act, 1985'

## Batch 0146 per-target notes (2026-04-20T12:37:42Z)

- citizens-economic-empowerment-2006 (Act 9/2006): no parseable sections in HTML or PDF
- children-candidate-1989 (Act 14/1989): title rejected (contains 'amendment'): 'Employment of Women, Young Persons and Children (Amendment) Act, 1989'
- bank-of-zambia-2001 (2001/11): batch cap reached (MAX_RECORDS=8) — deferred
- mines-minerals-2011 (2011/28): batch cap reached (MAX_RECORDS=8) — deferred

## Batch 0147 per-target notes (2026-04-20T13:39:24Z)

- bank-of-zambia-2001 (Act 11/2001): title rejected (contains 'amendment'): 'Development Bank of Zambia (Amendment) Act, 2001'
- mines-minerals-2011 (Act 28/2011): title rejected (contains 'amendment'): 'Mines and Minerals Development (Amendment) Act, 2011'
- pensions-and-insurance-2005 (Act 26/2005): title rejected (contains 'amendment'): 'Insurance (Amendment) Act, 2005'
- local-government-1993 (Act 30/1993): title rejected (contains 'amendment'): 'Local Government (Amendment) Act, 1993'
- immigration-1997 (Act 25/1997): title rejected (contains 'amendment'): 'Immigration and Deportation (Amendment) Bill, I997'

## Batch 0149 per-target notes (2026-04-20T18:40:29Z)

- citizens-economic-empowerment-2006 (Act 9/2006): no parseable sections in HTML or PDF
- local-government-elections-2004 (Act 9/2004): title rejected (contains 'amendment'): 'Local Government (Amendment) Act, 2004'
- patents-1987 (Act 26/1987): title rejected (contains 'amendment'): 'Patents (Amendment) Act, 1987'
- zambia-tourism-board-1985 (Act 22/1985): title rejected (contains 'amendment'): 'Tourism (Amendment) Act, 1985'

## Batch 0150 per-target notes (2026-04-20T19:08:19Z)

- 1995/10 'Tanzania-Zambia Railway Act, 1995': batch cap reached (MAX_RECORDS=8) — deferred
- 1971/34 'Landlord and Tenant (Business Premises) Act, 1971': batch cap reached (MAX_RECORDS=8) — deferred
- 1968/25 'Misrepresentation Act, 1968': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2019/3 'Employment Code Act, 2019': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2017/9 'Corporate Insolvency Act, 2017': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2010/38 'Anti-Corruption Act, 2010': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2012/3 'Anti-Corruption Act, 2012': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2002/11 'Road Traffic Act, 2002': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2010/24 'Competition and Consumer Protection Act, 2010': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2009/15 'Information and Communication Technologies Act, 2009': pre-fetch reject — already in HEAD (via query 'sale of goods')
- 2015/15 'Employment (Amendment) Act, 2015': pre-fetch reject — already in HEAD (via query 'employers and workers')
- 2010/18 'Immigration and Deportation Act, 2010': pre-fetch reject — already in HEAD (via query 'employers and workers')
- 1999/10 "Workers ' Compensation Act, 1999": pre-fetch reject — already in HEAD (via query 'employers and workers')
- 1973/20 'Medical Examination of Young Persons (Underground Work) Act, 1973': pre-fetch reject — already in HEAD (via query 'employers and workers')
- 1993/27 'Industrial and Labour Relations Act, 1993': pre-fetch reject — already in HEAD (via query 'employers and workers')
- 2008/11 'Anti-Human Trafficking Act, 2008': pre-fetch reject — already in HEAD (via query 'employers and workers')
- 1982/25 'Minimum Wages and Conditions of Employment , 1982': pre-fetch reject — already in HEAD (via query 'employers and workers')
- 1989/6 'Wills and Administration of Testate Estates Act, 1989': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1960/41 'High Court Act': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1925/20 "Administrator -General's Act, 1925": pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 2021/1 'Legal Aid Act, 2021': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1949/21 'Mental Disorders Act, 1949': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1936/22 'Probates (Resealing) Act, 1936': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1951/2 'Consular Conventions Act, 1951': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1973/22 'Legal Practitioners Act, 1973': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1967/27 'Bankruptcy Act, 1967': pre-fetch reject — already in HEAD (via query 'probate administration estates')
- 1998/12 'Zambia Wildlife Act, 1998': pre-fetch reject — already in HEAD (via query 'hire purchase')
- 2011/12 'Environmental Management Act, 2011': pre-fetch reject — already in HEAD (via query 'hire purchase')
- 2008/12 'Public Procurement Act, 2008': pre-fetch reject — already in HEAD (via query 'hire purchase')
- 2010/27 'Animal Health Act, 2010': pre-fetch reject — already in HEAD (via query 'hire purchase')
- 2015/14 'Zambia Wildlife Act, 2015': pre-fetch reject — already in HEAD (via query 'hire purchase')
- 1999/12 'Environment Protection and Pollution Control (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'hire purchase')
- 2018/8 'Credit Reporting Act, 2018': pre-fetch reject — already in HEAD (via query 'hire purchase')
- 2017/10 'Companies Act, 2017': pre-fetch reject — already in HEAD (via query 'bills of exchange')
- 1996/43 'Bank of Zambia Act, 1996': pre-fetch reject — already in HEAD (via query 'bills of exchange')
- 1972/21 'National College for Management and Development Studies Act, 1972': pre-fetch reject — already in HEAD (via query 'bills of exchange')
- 1990/32 'Stamp Duty (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'bills of exchange')

## Batch 0151 per-target notes (2026-04-20T19:37:29Z)

- 1996/28 'Pension Scheme Regulation Act , 1996': batch cap reached (MAX_RECORDS=8) — deferred
- 1961/27 'Dairy Produce Marketing and Levy Act, 1961': batch cap reached (MAX_RECORDS=8) — deferred
- 1967/64 'Tobacco Act, 1967': batch cap reached (MAX_RECORDS=8) — deferred
- 1967/65 'Tobacco Levy Act, 1967': batch cap reached (MAX_RECORDS=8) — deferred
- 1969/28 'Loans and Guarantees (Authorisation) Act, 1969': batch cap reached (MAX_RECORDS=8) — deferred
- 1970/63 'Co - operative Societies Act, 1970': batch cap reached (MAX_RECORDS=8) — deferred
- 1971/30 'Registration and Development of Villages Act, 1971': batch cap reached (MAX_RECORDS=8) — deferred
- 1984/12 'Property Transfer Tax Act, 1984': batch cap reached (MAX_RECORDS=8) — deferred
- 1968/59 'Carriage by Air Act, 1968': batch cap reached (MAX_RECORDS=8) — deferred
- 1989/6 'Wills and Administration of Testate Estates Act, 1989': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 2022/12 'Children’s Code Act, 2022': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 1989/5 'Intestate Succession Act, 1989': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 1996/40 'National Pension Scheme Act, 1996': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 2021/1 'Legal Aid Act, 2021': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 1994/26 'Companies Act, 1994': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 1967/27 'Bankruptcy Act, 1967': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 1960/57 'Agricultural Lands Act, 1960': pre-fetch reject — already in HEAD (via query 'wills administration estates')
- 2019/3 'Employment Code Act, 2019': pre-fetch reject — already in HEAD (via query 'intestate succession')
- 1996/35 'Public Service Pensions Act, 1996': pre-fetch reject — already in HEAD (via query 'intestate succession')
- 1966/20 'Local Courts Act, 1966': pre-fetch reject — already in HEAD (via query 'intestate succession')
- 1989/4 'Interpretation and General Provisions (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'intestate succession')
- 1991/8 'Local Courts (Amendment) Act, 1991': pre-fetch reject — title contains 'amendment' (via query 'intestate succession')
- 2018/2 'National Health Insurance Act , 2018': pre-fetch reject — already in HEAD (via query 'insurance act')
- 2005/26 'Insurance (Amendment) Act , 2005': pre-fetch reject — title contains 'amendment' (via query 'insurance act')
- 2015/21 'Insurance Premium Levy Act': pre-fetch reject — already in HEAD (via query 'insurance act')
- 1989/28 'Insurance (Amendment) Act , 1989': pre-fetch reject — title contains 'amendment' (via query 'insurance act')
- 1992/2 'Insurance (Amendment) Act , 1992': pre-fetch reject — title contains 'amendment' (via query 'insurance act')
- 2021/47 'Insurance Premium Levy (Amendment) Act , 2021': pre-fetch reject — title contains 'amendment' (via query 'insurance act')
- 2024/28 'Insurance Premium Levy (Amendment) Act , 2024': pre-fetch reject — already in HEAD (via query 'insurance act')
- 2018/16 'Insurance Premium Levy (Amendment) Act , 2018': pre-fetch reject — already in HEAD (via query 'insurance act')
- 1991/17 'Insurance Brokers (Cessation and Transfer) (Repeal) Act , 1991': pre-fetch reject — title contains 'repeal' (via query 'insurance act')
- 1990/13 'Civil Service (Local Condition) (Amendment) Pensions Act , 1990': pre-fetch reject — title contains 'amendment' (via query 'pensions act')
- 2021/11 'Public Service Pensions (Amendment) Act , 2021': pre-fetch reject — already in HEAD (via query 'pensions act')
- 2015/7 'National Pension Scheme (Amendment) Act , 2015': pre-fetch reject — already in HEAD (via query 'pensions act')
- 1989/24 'Coffee Act, 1989': pre-fetch reject — already in HEAD (via query 'co-operative societies')
- 1993/27 'Industrial and Labour Relations Act, 1993': pre-fetch reject — already in HEAD (via query 'co-operative societies')
- 1995/29 'Lands Act': pre-fetch reject — already in HEAD (via query 'co-operative societies')
- 1923/9 'British Acts Extension Act, 1923': pre-fetch reject — already in HEAD (via query 'friendly societies')
- 1968/46 'Building Societies Act, 1968': pre-fetch reject — already in HEAD (via query 'friendly societies')
- 1956/5 'Adoption Act, 1956': pre-fetch reject — already in HEAD (via query 'friendly societies')

## Batch 0152 per-target notes (2026-04-20T20:07:59Z)

- 1968/59 'Carriage by Air Act, 1968': batch cap reached (MAX_RECORDS=8) — deferred
- 1950/18 'Rhodesia Railways Loans Guarantee Act, 1950': batch cap reached (MAX_RECORDS=8) — deferred
- 1964/51 'General Loans ( Guarantee ) Act, 1964': batch cap reached (MAX_RECORDS=8) — deferred
- 1972/24 'National Savings and Credit Act, 1972': batch cap reached (MAX_RECORDS=8) — deferred
- 1980/14 'Corrupt Practice Act, 1980': batch cap reached (MAX_RECORDS=8) — deferred
- 2016/40 'Patents Act , 2016': pre-fetch reject — already in HEAD (via query 'patents act')
- 1987/26 'Patents (Amendment) Act , 1987': pre-fetch reject — title contains 'amendment' (via query 'patents act')
- 2010/14 'Patents (Amendment) Act , 2010': pre-fetch reject — already in HEAD (via query 'patents act')
- 2010/15 'Patents and Companies Registration Agency Act , 2010': pre-fetch reject — already in HEAD (via query 'patents act')
- 2020/4 'Patents and Companies Registration Agency Act , 2020': pre-fetch reject — already in HEAD (via query 'patents act')
- 1980/18 'Patents (Amendment) Act , 1980': pre-fetch reject — title contains 'amendment' (via query 'patents act')
- 2013/12 'Patents and Companies Registration Agency (Amendment) Act , 2013': pre-fetch reject — already in HEAD (via query 'patents act')
- 2016/41 'Securities Act , 2016': pre-fetch reject — already in HEAD (via query 'patents act')
- 2017/10 'Companies Act , 2017': pre-fetch reject — already in HEAD (via query 'patents act')
- 2017/9 'Corporate Insolvency Act , 2017': pre-fetch reject — already in HEAD (via query 'patents act')
- 1994/44 'Copyright and Performance Rights Act, 1994': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 2010/25 'Copyright and Performance Rights (Amendment) Act, 2010': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 2010/24 'Competition and Consumer Protection Act, 2010': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 2024/27 'Property Transfer Tax (Amendment) Act, 2024': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 1987/16 'Zambia National Broadcasting Corporation Act, 1987': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 1994/26 'Companies Act, 1994': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 2013/6 'Millennium Challenge Compact Act, 2013': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 1967/27 'Bankruptcy Act, 1967': pre-fetch reject — already in HEAD (via query 'copyright performance rights')
- 2019/12 'Energy Regulation Act, 2019': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2010/18 'Immigration and Deportation Act, 2010': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2002/12 'Public Roads Act, 2002': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2023/18 'Public -Private Partnership Act, 2023': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2008/13 'Accountants Act, 2008': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2018/13 'Statistics Act, 2018': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2014/4 'Zambia Chartered Institute of Logistics and Transport Act, 2014': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2022/5 'Bank of Zambia Act, 2022': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2015/13 'Tourism and Hospitality Act, 2015': pre-fetch reject — already in HEAD (via query 'chartered institute public relations')
- 2022/10 'Tobacco Act , 2022': pre-fetch reject — already in HEAD (via query 'tobacco act')
- 2022/12 'Children’s Code Act , 2022': pre-fetch reject — already in HEAD (via query 'tobacco act')
- 2023/25 'Customs and Excise (Amendment) Act , 2023': pre-fetch reject — already in HEAD (via query 'tobacco act')
- 2011/20 'Liquor Licensing Act , 2011': pre-fetch reject — already in HEAD (via query 'tobacco act')
- 2023/2 'Controlled Substances Act , 2023': pre-fetch reject — already in HEAD (via query 'tobacco act')
- 1965/56 'Prisons Act , 1965': pre-fetch reject — already in HEAD (via query 'tobacco act')
- 1999/4 'Customs and Excise (Amendment) Act , 1999': pre-fetch reject — title contains 'amendment' (via query 'tobacco act')
- 2020/3 'Food and Nutrition Act , 2020': pre-fetch reject — already in HEAD (via query 'tobacco act')
- 1989/24 'Coffee Act, 1989': pre-fetch reject — already in HEAD (via query 'co-operative societies')
- 1993/27 'Industrial and Labour Relations Act, 1993': pre-fetch reject — already in HEAD (via query 'co-operative societies')
- 1995/29 'Lands Act': pre-fetch reject — already in HEAD (via query 'co-operative societies')
- 2025/21 'Property Transfer Tax (Amendment) Act, 2025': pre-fetch reject — already in HEAD (via query 'property transfer tax')
- 2003/4 'Property Transfer Tax (Amendment) Act, 2003': pre-fetch reject — title contains 'amendment' (via query 'property transfer tax')

## Batch 0153 per-target notes (2026-04-20T20:37:34Z)

- 1963/65 "Workers' Compensation Act, 1963": batch cap reached (MAX_RECORDS=8) — deferred
- 2003/13 'National Council for Construction Act, 2003': batch cap reached (MAX_RECORDS=8) — deferred
- 1954/12 'Control of Goods Act , 1954': batch cap reached (MAX_RECORDS=8) — deferred
- 1995/4 'Value Added Tax Act , 1995': batch cap reached (MAX_RECORDS=8) — deferred
- 1995/31 'Mines and Minerals Act , 1995': batch cap reached (MAX_RECORDS=8) — deferred
- 1996/28 'Pension Scheme Regulation Act , 1996': batch cap reached (MAX_RECORDS=8) — deferred
- 1990/32 'Stamp Duty (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'bills of exchange')
- 2011/3 'Juveniles (Amendment) Act , 2011': pre-fetch reject — title contains 'amendment' (via query 'juveniles act')
- 1999/12 'Environment Protection and Pollution Control (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'hire purchase')
- 1994/17 'Stamp Duty (Repeal) Act, 1994': pre-fetch reject — title contains 'repeal' (via query 'stamp duty')
- 1992/8 'Stamp Duty (Amendment) Act, 1992': pre-fetch reject — title contains 'amendment' (via query 'stamp duty')
- 1984/3 'Stamp Duty (Amendment) Act, 1984': pre-fetch reject — title contains 'amendment' (via query 'stamp duty')
- 2005/26 'Insurance (Amendment) Act , 2005': pre-fetch reject — title contains 'amendment' (via query 'insurance act 1997')
- 1997/7 'Control of Goods (Amendment) Act , 1997': pre-fetch reject — title contains 'amendment' (via query 'insurance act 1997')

## Batch 0154 per-target notes (2026-04-20T21:06:40Z)

- 2008/8 'Industrial and Labour Relations (Amendment) Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'arbitration')
- 2021/53 'Appropriation Act, 2021': pre-fetch reject — title contains 'appropriation' (via query 'adult literacy')
- 2020/26 'Appropriation Act, 2020': pre-fetch reject — title contains 'appropriation' (via query 'adult literacy')
- 2008/2 'Customs and Excise (Amendment) Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'cotton')
- 2001/2 'Customs and Excise (Amendment) Act, 2001': pre-fetch reject — title contains 'amendment' (via query 'cotton')
- 1984/2 'Sales Tax (Amendment) Act, 1984': pre-fetch reject — title contains 'amendment' (via query 'cotton')
- 2005/26 'Insurance (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'insurance')
- 2021/47 'Insurance Premium Levy (Amendment) Act, 2021': pre-fetch reject — title contains 'amendment' (via query 'insurance')
- 1992/2 'Insurance (Amendment) Act, 1992': pre-fetch reject — title contains 'amendment' (via query 'insurance')
- 1991/17 'Insurance Brokers (Cessation and Transfer) (Repeal) Act, 1991': pre-fetch reject — title contains 'repeal' (via query 'insurance')
- 1989/28 'Insurance (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'insurance')

## Batch 0155 per-target notes (2026-04-20T21:36:07Z)

- 2011/3 'Juveniles (Amendment) Act, 2011': pre-fetch reject — title contains 'amendment' (via query 'juveniles')
- 1999/12 'Environment Protection and Pollution Control (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'hire purchase')
- 1990/32 'Stamp Duty (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'bills of exchange')
- 1997/4 'Roads and Road Traffic (Amendment) Act, 1997': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1996/4 'Roads and Road Traffic (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1989/29 'Roads and Road Traffic (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1994/12 'Roads and Road Traffic (Amendment) Act, 1994': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 2006/6 'Road Traffic (Amendment) Act, 2006': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1992/7 'Roads and Road Traffic (Amendment) Act, 1992': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 2008/4 'Road Traffic (Amendment)Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1985/4 'Roads and Road Traffic (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1986/16 'Firearms (Amendment) Act, 1986': pre-fetch reject — title contains 'amendment' (via query 'firearms')
- 1985/29 'Firearm (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'firearms')
- 1993/30 'Local Government (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 2014/12 'Local Government (Amendment) Act, 2014': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 2004/9 'Local Government (Amendment) Act, 2004': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 1995/30 'Local Government (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 1993/31 'Local Government Elections (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'local government')

## Batch 0156 per-target notes (2026-04-20T22:06:28Z)

- 2000/18 'Banking and Financial Services (Amendrnent) Act, 2000': no parseable sections in HTML or PDF
- 1995/28 'Banking and Financial Services (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'banking and financial services')
- 2005/25 'Banking and Financial Services (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'banking and financial services')
- 2007/22 'Fisheries Act (Amendment) Act, 2007': pre-fetch reject — title contains 'amendment' (via query 'fisheries')
- 1981/15 'Forest (Amendment) Act, 1981': pre-fetch reject — title contains 'amendment' (via query 'forests')
- 1985/27 'State Security (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'securities')
- 1987/26 'Patents (Amendment) Act , 1987': pre-fetch reject — title contains 'amendment' (via query 'patents act')
- 1980/18 'Patents (Amendment) Act , 1980': pre-fetch reject — title contains 'amendment' (via query 'patents act')
- 1989/29 'Roads and Road Traffic (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1997/4 'Roads and Road Traffic (Amendment) Act, 1997': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1996/4 'Roads and Road Traffic (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1994/12 'Roads and Road Traffic (Amendment) Act, 1994': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1985/4 'Roads and Road Traffic (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1990/30 'Roads and Road Traffic (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1993/14 'Roads and Road Traffic (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1992/7 'Roads and Road Traffic (Amendment) Act, 1992': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')
- 1991/14 'Roads and Road Traffic (Amendment) Act, 1991': pre-fetch reject — title contains 'amendment' (via query 'roads and road traffic')

## Batch 0157 per-target notes (2026-04-22T10:52:26Z)

- 2008/8 'Industrial and Labour Relations (Amendment) Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'arbitration')
- 1999/4 'Customs and Excise (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'copyright')
- 2020/27 'Zambia Institute of Marketing (Amendment) Act, 2020': pre-fetch reject — title contains 'amendment' (via query 'higher education')
- 1996/23 'Electoral (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'electoral')
- 1986/19 'Electoral (Amendment) Act, 1986': pre-fetch reject — title contains 'amendment' (via query 'electoral')
- 1995/7 'Electoral (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'electoral')
- 1988/20 'Electoral (Amendment) Act, 1988': pre-fetch reject — title contains 'amendment' (via query 'electoral')
- 2001/4 'Electoral (Amendment) Act, 2001': pre-fetch reject — title contains 'amendment' (via query 'electoral')
- 2014/10 'Zambia Revenue Authority (Amendment) Act, 2014': pre-fetch reject — title contains 'amendment' (via query 'zambia revenue authority')
- 1996/32 'Zambia Revenue Authority (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'zambia revenue authority')
- 2010/42 'Housing (Statutory andImprovement Areas) (Amendment) Act, 2010': pre-fetch reject — title contains 'amendment' (via query 'lands tribunal')

## Batch 0158 per-target notes (2026-04-22T11:01:10Z)

- 1993/35 'Criminal Procedure Code (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'treason')
- 1997/25 'Immigration and Deportation (Amendment) Bill, I997': pre-fetch reject — title contains 'amendment' (via query 'immigration')
- 2012/16 'Appropriation Act, 2012': pre-fetch reject — title contains 'appropriation' (via query 'immigration')
- 1989/16 'Aviation (Amendment) Act) 1989': pre-fetch reject — title contains 'amendment' (via query 'aviation')
- 2007/17 'Penal Code (Amendment) Act, 2007': pre-fetch reject — title contains 'amendment' (via query 'aviation')
- 1983/13 'Industrial Relations (Amendment) Act, 1983': pre-fetch reject — title contains 'amendment' (via query 'industrial relations')
- 2008/8 'Industrial and Labour Relations (Amendment) Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'industrial relations')
- 1996/18 'Constitution of Zambia (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'industrial relations')
- 1990/32 'Stamp Duty (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'bills of exchange')

## Batch 0159 per-target notes (2026-04-22T11:09:01Z)

- 1999/12 'Environment Protection and Pollution Control (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'hire purchase')
- 1994/17 'Stamp Duty (Repeal) Act, 1994': pre-fetch reject — title contains 'repeal' (via query 'stamp duty')
- 1992/8 'Stamp Duty (Amendment) Act, 1992': pre-fetch reject — title contains 'amendment' (via query 'stamp duty')
- 1990/32 'Stamp Duty (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'stamp duty')
- 1984/3 'Stamp Duty (Amendment) Act, 1984': pre-fetch reject — title contains 'amendment' (via query 'stamp duty')
- 2011/3 'Juveniles (Amendment) Act, 2011': pre-fetch reject — title contains 'amendment' (via query 'juveniles')
- 1987/26 'Patents (Amendment) Act, 1987': pre-fetch reject — title contains 'amendment' (via query 'patents')
- 1980/18 'Patents (Amendment) Act, 1980': pre-fetch reject — title contains 'amendment' (via query 'patents')
- 1997/4 'Roads and Road Traffic (Amendment) Act, 1997': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1996/4 'Roads and Road Traffic (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1989/29 'Roads and Road Traffic (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1994/12 'Roads and Road Traffic (Amendment) Act, 1994': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 2006/6 'Road Traffic (Amendment) Act, 2006': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1992/7 'Roads and Road Traffic (Amendment) Act, 1992': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 2008/4 'Road Traffic (Amendment)Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1985/4 'Roads and Road Traffic (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'road traffic')
- 1997/25 'Immigration and Deportation (Amendment) Bill, I997': pre-fetch reject — title contains 'amendment' (via query 'immigration')
- 2012/16 'Appropriation Act, 2012': pre-fetch reject — title contains 'appropriation' (via query 'immigration')

## Batch 0160 per-target notes (2026-04-22T11:36:22Z)

- 1993/6 'Trades Licensing (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'trade')
- 2007/15 'Trades Licensing (Amendment) Act, 2007': pre-fetch reject — title contains 'amendment' (via query 'trade')
- 1994/10 'Trades Licensing (Amendment) Act, 1994': pre-fetch reject — title contains 'amendment' (via query 'trade')
- 1990/26 'Trades Licensing (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'trade')
- 1984/10 'Gold Trade (Amendment) Act, 1984': pre-fetch reject — title contains 'amendment' (via query 'trade')
- 2001/2 'Customs and Excise (Amendment) Act, 2001': pre-fetch reject — title contains 'amendment' (via query 'customs')
- 1985/1 'Customs and Excise (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'customs')
- 2008/2 'Customs and Excise (Amendment) Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'customs')
- 1989/25 'Customs and Excise (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'customs')
- 2005/4 'Customs and Excise (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'customs')
- 2004/11 'Customs and Excise (Amendment) (No. 2) Act, 2004': pre-fetch reject — title contains 'amendment' (via query 'customs')
- 1982/8 'Exchange Control (Amendment) Act, 1982': pre-fetch reject — title contains 'amendment' (via query 'exchange control')
- 1988/27 'Exchange Control (Amendment) (No. 2) Act, 1988': pre-fetch reject — title contains 'amendment' (via query 'exchange control')
- 1988/11 'Exchange Control (Amendment) Act, 1988': pre-fetch reject — title contains 'amendment' (via query 'exchange control')
- 1993/30 'Local Government (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 2014/12 'Local Government (Amendment) Act, 2014': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 2004/9 'Local Government (Amendment) Act, 2004': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 1995/30 'Local Government (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 1993/31 'Local Government Elections (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 2006/6 'Road Traffic (Amendment) Act, 2006': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 1997/4 'Roads and Road Traffic (Amendment) Act, 1997': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 1996/4 'Roads and Road Traffic (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 1994/12 'Roads and Road Traffic (Amendment) Act, 1994': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 1989/29 'Roads and Road Traffic (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 2008/4 'Road Traffic (Amendment)Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 2021/49 'Road Traffic (Amendment) Act, 2021': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 1990/10 'Citizenship of Zambia (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'citizenship')
- 1988/24 'Citizenship of Zambia (Amendment) Act, 1988': pre-fetch reject — title contains 'amendment' (via query 'citizenship')
- 1994/34 "President's Citizenship College (Amendment) Act, 1994": pre-fetch reject — title contains 'amendment' (via query 'citizenship')
- 1996/18 'Constitution of Zambia (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'citizenship')

## Batch 0161 per-target notes (2026-04-22T12:06:51Z)

- 2020/25 'Mines and Minerals Development (Amendment) Act , 2020': pre-fetch reject — title contains 'amendment' (via query 'mining act')
- 2002/5 'Mines and Minerals (Amendment) Act , 2002': pre-fetch reject — title contains 'amendment' (via query 'mining act')
- 1998/8 'Mines and Minerals (Amendment) Act , 1998': pre-fetch reject — title contains 'amendment' (via query 'mining act')
- 1985/18 'Mines and Minerals (Amendment) Act , 1985': pre-fetch reject — title contains 'amendment' (via query 'mining act')
- 2007/22 'Fisheries Act (Amendment) Act, 2007': pre-fetch reject — title contains 'amendment' (via query 'fisheries')
- 1995/21 'Agriculture (Seeds) (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'agriculture')
- 1990/2 'National Agricultural Marketing (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'agriculture')
- 2020/27 'Zambia Institute of Marketing (Amendment) Act, 2020': pre-fetch reject — title contains 'amendment' (via query 'marketing')
- 1988/7 'Markets (Amendment) Act, 1988': pre-fetch reject — title contains 'amendment' (via query 'marketing')
- 1995/6 'Companies (Amendment) Act , 1995': pre-fetch reject — title contains 'amendment' (via query 'companies act')
- 1986/2 'Companies (Amendment) Act , 1986': pre-fetch reject — title contains 'amendment' (via query 'companies act')
- 1983/7 'Companies (Amendment) Act , 1983': pre-fetch reject — title contains 'amendment' (via query 'companies act')
- 1990/27 'Companies (Amendment) Act , 1990': pre-fetch reject — title contains 'amendment' (via query 'companies act')
- 1993/16 'Companies (Amendment) Act , 1993': pre-fetch reject — title contains 'amendment' (via query 'companies act')
- 2011/24 'Companies (Amendment) Act , 2011': pre-fetch reject — title contains 'amendment' (via query 'companies act')
- 1994/3 'Companies (Amendment) Act , 1994': pre-fetch reject — title contains 'amendment' (via query 'companies act')
- 1995/26 'Investment (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'investment')
- 1998/10 'Investment (Amendment) Act, 1998': pre-fetch reject — title contains 'amendment' (via query 'investment')
- 1996/5 'Investment (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'investment')
- 2001/4 'Electoral (Amendment) Act, 2001': pre-fetch reject — title contains 'amendment' (via query 'referendum')
- 2015/10 'Excess Expenditure Appropriation (2012) Act, 2015': pre-fetch reject — title contains 'appropriation' (via query 'referendum')

## Batch 0162 per-target notes (2026-04-22T12:36:19Z)

- 1994/20 'Standards Act, 1994': batch cap reached (MAX_RECORDS=8) — deferred
- 1985/16 'Appropriation Act, 1985': pre-fetch reject — title contains 'appropriation' (via query 'forestry')
- 1999/12 'Environment Protection and Pollution Control (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'animal health')
- 1993/2 'Education Levy (Repeal) Act, 1993': pre-fetch reject — title contains 'repeal' (via query 'education')
- 1981/11 'Education Levy (Amendment) Act, 1981': pre-fetch reject — title contains 'amendment' (via query 'education')
- 1986/6 'Education Levy (Amendment) Act, 1986': pre-fetch reject — title contains 'amendment' (via query 'education')
- 2006/14 'Legal Practitioners (Amendment) Act, 2006': pre-fetch reject — title contains 'amendment' (via query 'legal practitioners')
- 1981/21 'Legal Practitioners (Amendment) Act, 1981': pre-fetch reject — title contains 'amendment' (via query 'legal practitioners')
- 2021/40 'Land Survey (Amendment) Act, 2021': pre-fetch reject — title contains 'amendment' (via query 'land survey')

## Batch 0163 per-target notes (2026-04-22T14:43:28Z)

- 2005/10 'Water Supply and Sanitation (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'water resources')
- 2021/53 'Appropriation Act, 2021': pre-fetch reject — title contains 'appropriation' (via query 'water resources')
- 1982/33 'National Parks and Wildlife (Amendment) Act, 1982': pre-fetch reject — title contains 'amendment' (via query 'wildlife')
- 2005/26 'Insurance (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'insurance')
- 2021/47 'Insurance Premium Levy (Amendment) Act, 2021': pre-fetch reject — title contains 'amendment' (via query 'insurance')
- 1992/2 'Insurance (Amendment) Act, 1992': pre-fetch reject — title contains 'amendment' (via query 'insurance')
- 1991/17 'Insurance Brokers (Cessation and Transfer) (Repeal) Act, 1991': pre-fetch reject — title contains 'repeal' (via query 'insurance')
- 1989/28 'Insurance (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'insurance')
- 2005/27 'Pension Scheme Regulation (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'pensions')
- 1985/27 'State Security (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'securities')
- 1999/8 'Telecommunications (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'telecommunications')
- 2007/17 'Penal Code (Amendment) Act, 2007': pre-fetch reject — title contains 'amendment' (via query 'telecommunications')
- 2003/23 'Energy Regulation (Amendment) Act, 2003': pre-fetch reject — title contains 'amendment' (via query 'energy regulation')

## Batch 0164 per-target notes (2026-04-22T15:06:07Z)

- 2009/21 'Electronic Communications and Transactions Act, 2009': no parseable sections in HTML or PDF
- 2005/10 'Water Supply and Sanitation (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'water')
- 1999/12 'Environment Protection and Pollution Control (Amendment) Act, 1999': pre-fetch reject — title contains 'amendment' (via query 'environment')
- 2005/15 'Penal Code (Amendment) Act, 2005': pre-fetch reject — title contains 'amendment' (via query 'environment')
- 1996/19 'Zambia Institute of Mass Communications (Repeal) Act, 1996': pre-fetch reject — title contains 'repeal' (via query 'communications')
- 2010/3 'Information and Communication Technologies Amendment) Act, 2010': pre-fetch reject — title contains 'amendment' (via query 'communications')
- 1994/12 'Roads and Road Traffic (Amendment) Act, 1994': pre-fetch reject — title contains 'amendment' (via query 'roads')
- 1997/4 'Roads and Road Traffic (Amendment) Act, 1997': pre-fetch reject — title contains 'amendment' (via query 'roads')
- 1993/14 'Roads and Road Traffic (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'roads')
- 1990/30 'Roads and Road Traffic (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'roads')
- 1985/4 'Roads and Road Traffic (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'roads')
- 1989/29 'Roads and Road Traffic (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'roads')
- 2006/6 'Road Traffic (Amendment) Act, 2006': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 1996/4 'Roads and Road Traffic (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 2008/4 'Road Traffic (Amendment)Act, 2008': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 2021/49 'Road Traffic (Amendment) Act, 2021': pre-fetch reject — title contains 'amendment' (via query 'traffic')
- 1985/15 'Land (Conversion of Titles) (Amendment) (No. 2) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'lands')
- 1996/20 'Lands (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'lands')
- 1995/8 'Petroleum (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'petroleum')
- 1996/2 'Bank of Zambia (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'banking')
- 2001/11 'Development Bank of Zambia (Amendment) Act, 2001': pre-fetch reject — title contains 'amendment' (via query 'banking')

## Batch 0165 per-target notes (2026-04-22T15:36:34Z)

- 2020/25 'Mines and Minerals Development (Amendment) Act, 2020': pre-fetch reject — title contains 'amendment' (via query 'mines and minerals')
- 2002/5 'Mines and Minerals (Amendment) Act, 2002': pre-fetch reject — title contains 'amendment' (via query 'mines and minerals')
- 1998/8 'Mines and Minerals (Amendment) Act, 1998': pre-fetch reject — title contains 'amendment' (via query 'mines and minerals')
- 1996/41 'Mines and Minerals (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'mines and minerals')
- 2011/28 'Mines and Minerals Development (Amendment) Act, 2011': pre-fetch reject — title contains 'amendment' (via query 'mines and minerals')
- 1985/18 'Mines and Minerals (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'mines and minerals')
- 2013/10 'Environmental Management (Amendment) Act, 2013': pre-fetch reject — title contains 'amendment' (via query 'environmental management')
- 2010/42 'Housing (Statutory andImprovement Areas) (Amendment) Act, 2010': pre-fetch reject — title contains 'amendment' (via query 'housing')
- 1998/5 'Zambia Publishing House (Amendment) Act, 1998': pre-fetch reject — title contains 'amendment' (via query 'housing')
- 2004/16 'Prisons (Amendment) Act, 2004': pre-fetch reject — title contains 'amendment' (via query 'prisons')
- 2000/14 'Prisons (Amendment) Act, 2000': pre-fetch reject — title contains 'amendment' (via query 'prisons')
- 1996/18 'Constitution of Zambia (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'prisons')

## Batch 0166 per-target notes (2026-04-22T16:06:04Z)

- 1985/22 'Tourism (Amendment) Act, 1985': pre-fetch reject — title contains 'amendment' (via query 'tourism')
- 1989/25 'Customs and Excise (Amendment) Act, 1989': pre-fetch reject — title contains 'amendment' (via query 'fertiliser')
- 1981/5 'Customs and Excise (Amendment) Act, 1981': pre-fetch reject — title contains 'amendment' (via query 'fertiliser')
- 1982/4 'Customs and Excise (Amendment) Act, 1982': pre-fetch reject — title contains 'amendment' (via query 'tobacco')
- 2021/45 'Customs and Excise (Amendment) Act, 2021': pre-fetch reject — title contains 'amendment' (via query 'tobacco')
- 1981/10 'Income Tax (Amendment) Act, 1981': pre-fetch reject — title contains 'amendment' (via query 'dairy')
- 2006/10 'Public Roads (Amendment) Act, 2006': pre-fetch reject — title contains 'amendment' (via query 'public roads')
- 1993/30 'Local Government (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 2014/12 'Local Government (Amendment) Act, 2014': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 2004/9 'Local Government (Amendment) Act, 2004': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 1995/30 'Local Government (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 1993/31 'Local Government Elections (Amendment) Act, 1993': pre-fetch reject — title contains 'amendment' (via query 'local government')
- 1996/18 'Constitution of Zambia (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'chieftaincy')

## Batch 0167 per-target notes (2026-04-22T16:34:44Z)

- 2007/22 'Fisheries Act (Amendment) Act, 2007': pre-fetch reject — title contains 'amendment' (via query 'fisheries')
- 1981/15 'Forest (Amendment) Act, 1981': pre-fetch reject — title contains 'amendment' (via query 'forests')
- 1982/33 'National Parks and Wildlife (Amendment) Act, 1982': pre-fetch reject — title contains 'amendment' (via query 'wildlife')
- 2020/26 'Appropriation Act, 2020': pre-fetch reject — title contains 'appropriation' (via query 'traditional leadership')

## Batch 0168 per-target notes (2026-04-24T05:04:12Z)

- 1995/21 'Agriculture (Seeds) (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'agriculture')
- 1990/2 'National Agricultural Marketing (Amendment) Act, 1990': pre-fetch reject — title contains 'amendment' (via query 'agriculture')

## Batch 0168 per-target notes (2026-04-24T05:05:25Z)

- 2021/36 'Acts of Parliament (Amendment) Act, 2021': pre-fetch reject — title contains 'amendment' (via query 'parliament')
- 1996/23 'Electoral (Amendment) Act, 1996': pre-fetch reject — title contains 'amendment' (via query 'electoral')
- 1986/19 'Electoral (Amendment) Act, 1986': pre-fetch reject — title contains 'amendment' (via query 'electoral')
- 1995/7 'Electoral (Amendment) Act, 1995': pre-fetch reject — title contains 'amendment' (via query 'electoral')
- 1988/20 'Electoral (Amendment) Act, 1988': pre-fetch reject — title contains 'amendment' (via query 'electoral')
- 2001/4 'Electoral (Amendment) Act, 2001': pre-fetch reject — title contains 'amendment' (via query 'electoral')

## Batch 0169 per-target notes (2026-04-24T05:16:34Z)

- 2011/3 'Juveniles (Amendment) Act , 2011': alphabetical-fallback pre-fetch reject — title contains 'amendment' (via query 'juveniles act')
- 1994/17 'Stamp Duty (Repeal) Act , 1994': alphabetical-fallback pre-fetch reject — title contains 'repeal' (via query 'stamp duties act')
- 1990/32 'Stamp Duty (Amendment) Act , 1990': alphabetical-fallback pre-fetch reject — title contains 'amendment' (via query 'stamp duties act')
- 1992/8 'Stamp Duty (Amendment) Act , 1992': alphabetical-fallback pre-fetch reject — title contains 'amendment' (via query 'stamp duties act')
- 1984/3 'Stamp Duty (Amendment) Act , 1984': alphabetical-fallback pre-fetch reject — title contains 'amendment' (via query 'stamp duties act')
- UNRESOLVED CAP. PARENT ('juveniles act'): no-nature-filter probe returned ZambiaLII count=163, page-1 /akn/zm/act/ links=3. No primary parent surfaced. Pivot next tick to parliament.gov.zm listing.
- UNRESOLVED CAP. PARENT ('hire purchase act'): no-nature-filter probe returned ZambiaLII count=79, page-1 /akn/zm/act/ links=17. No primary parent surfaced. Pivot next tick to parliament.gov.zm listing.
- UNRESOLVED CAP. PARENT ('stamp duties act'): no-nature-filter probe returned ZambiaLII count=130, page-1 /akn/zm/act/ links=32. No primary parent surfaced. Pivot next tick to parliament.gov.zm listing.
- UNRESOLVED CAP. PARENT ('sale of goods act'): no-nature-filter probe returned ZambiaLII count=663, page-1 /akn/zm/act/ links=0. No primary parent surfaced. Pivot next tick to parliament.gov.zm listing.
- UNRESOLVED CAP. PARENT ('bills of exchange act'): no-nature-filter probe returned ZambiaLII count=79, page-1 /akn/zm/act/ links=19. No primary parent surfaced. Pivot next tick to parliament.gov.zm listing.

## Batch 0170 per-target notes (2026-04-24T05:39:03Z)

- 2021/38 'insurance-act-2021': HTML fetch failed: status=404 len=17595
- 2021/37 'zambia-correctional-service-act-2021': pre-queue reject — already in HEAD (parliament.gov.zm /node/9008 — primary Act, absent from HEAD)
- 2021/35 'narcotic-drugs-and-psychotropic-substances-act-2021': pre-queue reject — already in HEAD (parliament.gov.zm /node/9005 — primary Act, absent from HEAD)
- 2021/34 'industrial-hemp-act-2021': pre-queue reject — already in HEAD (parliament.gov.zm /node/9004 — primary Act, absent from HEAD)
- [2026-04-24T07:38:20Z] 2026/001 listing_title='The Teaching Profession Act, 2026' status=skip_slot_in_head node=https://www.parliament.gov.zm/node/12917 batch=0172
- [2026-04-24T07:38:20Z] 2025/029 listing_title='The Zambia Institute of Procurement and Supply Act, 2025' status=skip_slot_in_head node=https://www.parliament.gov.zm/node/12779 batch=0172
- [2026-04-24T07:38:20Z] 2025/027 listing_title='The Betting Act, 2025' status=skip_slot_in_head node=https://www.parliament.gov.zm/node/12777 batch=0172
- [2026-04-24T07:38:20Z] 2025/026 listing_title='The Zambia National Broadcasting Corporation Act, 2025' status=skip_slot_in_head node=https://www.parliament.gov.zm/node/12775 batch=0172
- [2026-04-24T07:38:20Z] 2025/025 listing_title='The Independent Broadcasting Authority Act, 2025' status=skip_slot_in_head node=https://www.parliament.gov.zm/node/12774 batch=0172
- [2026-04-24T07:41:28Z] 2015/002 AKN probe status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/2015/2 batch=0172
- [2026-04-24T07:41:42Z] 2015/010 AKN probe status=reject_title:appropriation:Excess Expenditure Appropriation (2012) Act, 2015 url=https://zambialii.org/akn/zm/act/2015/10 batch=0172
- [2026-04-24T07:41:55Z] 2021/022 AKN probe status=reject_title:amendment:Public-Private Partnership (Amendment) Act, 2021 url=https://zambialii.org/akn/zm/act/2021/22 batch=0172
- [2026-04-24T07:44:37Z] 2015/002 AKN exists at https://zambialii.org/akn/zm/act/2015/2/eng@2015-08-14 but title 'Anti-Terrorism (Amendment) Act, 2015' rejected by B-POL-ACT-1 (token='amendment'); slot intentionally absent from HEAD. batch=0172
- [2026-04-24T07:44:37Z] 2015/010 AKN exists at https://zambialii.org/akn/zm/act/2015/10/eng@2015-08-14 but title 'Excess Expenditure Appropriation (2012) Act, 2015' rejected by B-POL-ACT-1 (token='excess expenditure'); slot intentionally absent from HEAD. batch=0172
- [2026-04-24T07:44:37Z] 2021/022 AKN exists at https://zambialii.org/akn/zm/act/2021/22/eng@2021-03-24 but title 'Public-Private Partnership (Amendment) Act, 2021' rejected by B-POL-ACT-1 (token='amendment'); slot intentionally absent from HEAD. batch=0172
- [2026-04-24T07:44:37Z] 2021/036 AKN exists at https://zambialii.org/akn/zm/act/2021/36/eng@2021-05-20 but title 'Acts of Parliament (Amendment) Act, 2021' rejected by B-POL-ACT-1 (token='amendment'); slot intentionally absent from HEAD. batch=0172
- [2026-04-24T07:44:37Z] 2021/039 AKN exists at https://zambialii.org/akn/zm/act/2021/39/eng@2021-05-20 but title 'Lands and Deeds Registry (Amendment) Act, 2021' rejected by B-POL-ACT-1 (token='amendment'); slot intentionally absent from HEAD. batch=0172
- [2026-04-24T07:44:37Z] 2021/040 AKN exists at https://zambialii.org/akn/zm/act/2021/40/eng@2021-05-20 but title 'Land Survey (Amendment) Act, 2021' rejected by B-POL-ACT-1 (token='amendment'); slot intentionally absent from HEAD. batch=0172

## 2026-04-24T08:39:12Z — batch 0173 audit: pre-existing duplicate IDs (not introduced by this batch)

Corpus-wide CHECK1 (unique IDs) surfaces 42 duplicates between older Appropriation-Act record files using the "-000-" placeholder-number pattern (e.g., `act-zm-1994-000-appropriation-act-1994.json`) and the correctly-numbered variants (e.g., `act-zm-1994-005-appropriation-act-1994.json`). Both files share the same `id` field value (the correctly-numbered ID), which means the `-000-` filename variant is orphaned data with a duplicate ID. This is a historical data-quality issue predating batch 0173. Batch-scoped CHECK1 for batch 0173 passes — none of the 4 new SI records introduce new duplicate IDs. Flagged for a future cleanup tick to de-duplicate the historic Appropriation Acts.

Affected IDs (pairs where -000- variant exists alongside canonical-numbered variant):
- act-zm-1990-044-appropriation-act-1990
- act-zm-1991-* … act-zm-2013-* (appropriation acts with `-000-` placeholder file + correct-numbered file)
- full list on demand via: `python3 -c "import json,glob; ids=[(p,json.load(open(p))['id']) for p in glob.glob('records/acts/*.json')]; from collections import defaultdict; d=defaultdict(list); [d[i].append(p) for p,i in ids]; [print(i, paths) for i,paths in d.items() if len(paths)>1]"`

Sev: low (historic). Action: queue for next clean-up batch.

## Batch 0175 — sis_corporate filter refinement note (2026-04-24T09:37:22Z)

The substring-based CORPORATE_KEYWORDS filter in scripts/batch_0174.py and
batch_0175.py produces false positives for the token "pension" because it
matches as a substring of "suspension". Batch 0175 discovery surfaced 4
such false-positive SIs (2019/25 Income Tax Suspension Treasury Bill;
2019/11, 2018/61 Customs Excise Suspension Fuel; 2018/36 Customs Excise
Cut-rag Suspension). These are tax/customs suspension orders, not pension
SIs. Genuine corporate candidates from pages 5+6: 2019/62 Konoike
Construction Income Tax Exemption, 2019/59 Insurance Fidelity Fund
Regulations. Action item: change the filter to use a word-boundary regex
(e.g. r"\bpension") or a token-list approach before the next discovery
sweep. Not fixing this tick — flagged for human review.

## Batch 0176 — pension/suspension filter bug FIXED (2026-04-24T10:07:30Z)

Confirmed fixed in `scripts/batch_0176.py`: `CORPORATE_KEYWORDS` is now a
word-boundary regex `\b(?:compan(?:y|ies)|...|pension|...)\b`. Pages 7 & 8
discovery surfaced 6 corporate candidates with zero "suspension→pension"
false positives (verified: 2017/70, 2017/42, 2017/19, 2016/95, 2016/9,
2016/52 — all genuine corporate regulation). The older scripts
(`batch_0174.py`, `batch_0175.py`) still contain the substring filter but
are not re-invoked; future sis_corporate batches should inherit the
regex form from `batch_0176.py`.
- [2026-04-24T11:36:15Z] si/2019/025 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2019/25 batch=0179
- [2026-04-24T11:38:03Z] si/2019/025 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2019/25 batch=0179
- [2026-04-24T13:34:47Z] si/2017/043 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2017/43 batch=0183
- [2026-04-24T13:35:14Z] si/2019/025 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2019/25 batch=0183
- [2026-04-24T14:05:36Z] si/2022/013 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2022/13 batch=0184

## 2026-04-24 batch 0193 (sis_mining)

- ZambiaLII robots.txt now includes `Disallow: /akn/zm/judgment/` and `Disallow: /akn/zm/officialGazette/` under `User-agent: *`. Worker UA `KateWestonLegal-CorpusBuilder/1.0` matches the wildcard rule. Ongoing case_law_scz ingestion (priority_order item 5) is blocked by robots compliance from this tick onward. Crawl-delay: 5s for legislation paths still allowed under /akn/zm/act/. Action: pause case_law_scz; continue legislation sub-phases. Reverify robots.txt next tick before any judgment fetch.
- si/1995/166 (Mines and Minerals Act 1995 cited subsidiary) returns HTTP 404 at https://zambialii.org/akn/zm/act/si/1995/166 — referenced as the only SI from /akn/zm/act/1995/31 page. No alternate AKN slug found. Title not derivable from 404 — not invented. Mark as missing source.
- [2026-04-24T20:37:38Z] si/2022/002 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2022/2 batch=0197 sub_phase=sis_tax
- [2026-04-24T22:09:28Z] si/2022/013 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2022/13 batch=0200 sub_phase=sis_employment
- [2026-04-24T22:10:02Z] si/2000/105 status=http_404 url=https://zambialii.org/akn/zm/act/si/2000/105 batch=0200 sub_phase=sis_employment
- [2026-04-24T23:34:55Z] si/2019/025 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2019/25 batch=0203 sub_phase=sis_corporate
- [2026-04-24T23:35:08Z] si/2017/043 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2017/43 batch=0203 sub_phase=sis_corporate
- [2026-04-25T00:38:54Z] si/2022/013 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2022/13 batch=0205 sub_phase=sis_employment
- [2026-04-25T02:05:42Z] si/2022/004 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2022/4 batch=0208 sub_phase=sis_tax
- [2026-04-25T04:40:43Z] si/2022/012 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2022/12 batch=0213 sub_phase=sis_corporate
- [2026-04-25T09:07:15Z] si/2022/013 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2022/13 batch=0221 sub_phase=sis_employment
- [2026-04-25T11:38:07Z] si/2017/043 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2017/43 batch=0222 sub_phase=sis_tax
- [2026-04-25T11:38:22Z] si/2019/025 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2019/25 batch=0222 sub_phase=sis_tax
- [2026-04-25T11:39:12Z] si/2017/043 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2017/43 batch=0222 sub_phase=sis_tax note=image-only/scanned PDF (pdfplumber+pdfminer both 0 chars; same pattern as 2022/004, 2022/012, 2022/013)
- [2026-04-25T11:39:12Z] si/2019/025 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2019/25 batch=0222 sub_phase=sis_tax note=image-only/scanned PDF (pdfplumber+pdfminer both 0 chars; same pattern as 2022/004, 2022/012, 2022/013)
- [2026-04-25T11:41:15Z] si/2011/129 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2011/129 batch=0222 sub_phase=sis_immigration
- [2026-04-25T11:41:55Z] si/2011/129 status=pdf_parse_empty url=https://commons.laws.africa/akn/zm/act/si/2011/129/media/publication/zm-act-si-2011-129-publication-document.pdf batch=0222 sub_phase=sis_immigration note=image-only/scanned PDF (Immigration and Deportation General Regs 2011)

## Batch 0233 (2026-04-25T18:43Z)

- **2026/4 Electricity (Transmission) (Grid Code) Regulations, 2026** — `https://zambialii.org/akn/zm/act/si/2026/4` — PDF size 28,176,615 bytes exceeds MAX_PDF_BYTES cap of 4,500,000. Skipped; substituted within batch with 2023/5 Energy Regulation (Appeals Tribunal) Rules. **Future-tick action:** raise cap for this one-off (substantive grid code likely worth retaining) or chunk-fetch + reassemble. Raw HTML+PDF cached on disk at raw/zambialii/si/2026/si-zm-2026-004-electricity-transmission-grid-code-regulations-2026.{html,pdf} for reuse.

## [2026-04-25T19:41:35Z] Batch 0235 — pdf_parse_empty: 2022/8 National Assembly By-Election (Kabwata Constituency No. 77) (Election Date and Time of Poll) Order, 2022
- URL: https://zambialii.org/akn/zm/act/si/2022/8
- Error: pdf_parse_empty
- html_sha: 1be74b42c0f53bdb
- pdf_sha: aa39ab49caa6f499
- Disposition: raw HTML+PDF preserved on disk for OCR retry. Likely scanned-image PDF. Added to OCR backlog (now 6 items: 2017/068, 2018/011, 2022/004, 2022/007, 2022/012, 2022/008).
- Substituted in-batch with 2021/88 Local Government By-Elections No.4 Order, 2021 (parsed cleanly).

## 2026-04-25T22:40:37Z batch 0241 — pdf_parse_empty / OCR backlog

- **2022/13** Minimum Wages and Conditions of Employment (Truck and Bus Drivers) (Amendment) Order, 2022 — `https://zambialii.org/akn/zm/act/si/2022/13` — PDF appears scanned-image only (pdfplumber returned 0 chars). Raw HTML+PDF preserved at `raw/zambialii/si/2022/`. Added to OCR backlog (now 10 items: 2017/068, 2018/011, 2018/075, 2018/093, 2022/004, 2022/007, 2022/008, 2022/012, 2022/013, 2026/004).

## Batch 0242 (2026-04-25)
- 2020/007 Road Traffic (Speed Limits) Regulations, 2019 — pdf_parse_empty (scanned image). Raw HTML+PDF preserved at raw/zambialii/si/2020/. Added to OCR backlog (now 11 items: 2017/068 + 2018/011 + 2018/075 + 2018/093 + 2020/007 + 2022/004 + 2022/007 + 2022/008 + 2022/012 + 2022/013 + 2026/004).
- Alphabet probes K/O/Q each yielded 0 SI links. These letters appear to have minimal SI activity on zambialii.org's alphabetical listing (mostly Acts only).
- year=2025 listing partially returned older SIs (1985-2014 mix); 3 unprocessed novel remain in cache (1985/45 Air Services Aerial App; 1992/9 Air Passenger Charging; possibly more) — deferred to next tick.

## Batch 0263 (2026-04-26) — 1956/4 URL disambiguator deferral

- **1956/4** Service of Process and Execution of Judgments Act, 1956 — zambialii lists this at `/akn/zm/act/1956/4-x/eng@1996-12-31` (note the `-x` disambiguator suffix in the path). The standard fetch pattern `/akn/zm/act/{yr}/{num}` would resolve to `/1956/4` which may not redirect. Skipped from this batch to avoid 404; needs special-case handler that probes `-x` and other disambiguators (e.g. `-y`, `-z`) before falling through. Substituted in-batch with 1989/9 Specified Offices (Terminal Gratuities) Act to fill MAX_BATCH_SIZE=8 cap. Reserved for follow-up batch with disambiguator-aware fetch.

## 2026-04-26 batch 0264 — Pre-existing IDs filtered from S residuals

The S residual list inherited from batch 0263 included two acts already
present in the corpus:

- **1933/36 Subordinate Courts Act** (in corpus from batch 0143, commit
  bf470ae). My batch 0264 ingestion silently overwrote it with a fresh
  fetch (parser_version 0.6.0-act-zambialii-2026-04-26 vs original 0.5.0)
  and regressed  from 1933-01-01 to null. Per BRIEF
  non-negotiable #4, the record was reverted via git cat-file -p HEAD.
- **1967/1 Suicide Act** (already in corpus). Skipped from this batch.

Substituted with 2025/12 Superior Courts (Number of Judges) Act, 2025
to fill the MAX_BATCH_SIZE=8 cap.

**Action item for future batches:** discovery filter must use
 (or equivalent
on-disk slug-aware check) before adding a candidate to picks. Year/num
existence check alone is insufficient because slug variants can mask
duplicates.

## Batch 0272 (2026-04-26) — pdf_parse_empty / OCR backlog

Two original picks for batch 0272 (acts_in_force chronological residual sweep) returned
`no_sections` because the source PDF was a scanned image (pdfplumber extracted 0 chars
across all pages). HTML and PDF preserved on disk for OCR retry.

- **2000/8** Excess Expenditure Appropriation (1995) Act, 2000 — `https://zambialii.org/akn/zm/act/2000/8` — PDF appears scanned-image only (4 pages, 0 chars extractable). Raw HTML+PDF preserved at `raw/zambialii/act/2000/2000-008.{html,pdf}`. Substituted in-batch with 2004/4 (Excess Expenditure Appropriation (1999) Act, 2004) which parsed cleanly.
- **2000/16** Excess Expenditure Appropriation (1997) Act, 2000 — `https://zambialii.org/akn/zm/act/2000/16` — PDF appears scanned-image only. Raw HTML+PDF preserved at `raw/zambialii/act/2000/2000-016.{html,pdf}`. Substituted in-batch with 2005/17 (National Health Services (Repeal) Act, 2005) which parsed cleanly.

OCR backlog now 17 items (act/2000/8, act/2000/16 added; previously 15: si 2017/068, 2018/011, 2018/075, 2018/093, 2020/007, 2022/004, 2022/007, 2022/008, 2022/012, 2022/013, 2026/004 + earlier SIs).

## Batch 0277 (2026-04-26) — duplicate-existing + pdf_parse_no_sections

Of 8 chronological picks from the inherited 102-item page-2 missing pool, 6/8 were
ingested cleanly. Two are deferred:

- **1988/21** Supreme Court and High Court (Number of Judges) Act, 1988 — `https://zambialii.org/akn/zm/act/1988/21` — DUPLICATE-EXISTING. Pre-flight dedup against on-disk records used the `/akn/zm/act/<yr>/<num>` source_url pattern, but the existing record (`act-zm-1988-021-supreme-court-and-high-court-number-of-judges-act-1988`, fetched 2026-04-20T18:40:15Z, 4 sections) was ingested via the `media.zambialii.org/media/legislation/...` PDF source URL pattern (likely an earlier batch using a different parser path), so it slipped past the dedup. New record (slug missing trailing -1988) was created and then quarantined to `_stale_locks/act-zm-1988-021-...act.json.b0277-dup` (virtiofs unlink restriction prevented direct removal). No new record committed for this pick. Action item: extend dedup pre-flight to also check `media.zambialii.org/media/legislation/.../zm-act-<yr>-<num>-publication-document.pdf` source_url shape AND glob `act-zm-<yr>-<num:03d>-*.json` regardless of slug suffix.
- **1988/32** Appropriation (No. 2) Act, 1988 — `https://zambialii.org/akn/zm/act/1988/32` — `no_sections`. HTML returned <2 akn-sections so PDF fallback engaged. PDF (5 pages, 12,570 chars extracted) is OCR'd legibly but section "1." was misread as "i." (lowercase i with period), causing the section regex `^(\d+)\.\s+...` to match zero sections. Parser refused to fabricate. Raw HTML+PDF preserved at `raw/zambialii/act/1988/1988-032.{html,pdf}`. Action item: add OCR-tolerant regex variant for Appropriation Act fiscal series (e.g. allow `^[1iIl]\.` for the canonical section "1") - deferred to future parser revision.

OCR backlog unchanged at 17 items (no new OCR-only PDFs this batch). Duplicate-existing
sweep candidate for one-shot audit: enumerate all `act-zm-<yr>-<num:03d>-*.json` glob
collisions across `records/acts/`.

## Batch 0278 (2026-04-26) — OCR section-spurious + image-only PDF

Of 8 chronological picks from the inherited 102-item page-2 missing pool (refreshed
to 94 candidates after glob-dedup of 6 batch-0277-committed and gaps-filter of
1988/21 + 1988/32), 6/8 ingested cleanly. Two are deferred:

- **1995/33** Supplementary Appropriation (1993) Act, 1995 — `https://zambialii.org/akn/zm/act/1995/33` — OCR_SECTION_SPURIOUS. PDF (2.5 MB, 18,234 chars OCR'd legibly enough for the regex to match patterns) was severely OCR-degraded: the section regex `^(\d+)\.\s+...` matched a single "section 95." which is not actually a section but a fragment of "No. 33 of 1995" whose OCR broke across lines as `(1 9 11 9 9b 5 12`. The captured "section 95" heading is OCR noise (`P J;i JO ... ? i - , • t £ • ? e B l ? 11`). Parser refused to fabricate clean section structure; record was written then quarantined to `_stale_locks/act-zm-1995-033-supplementary-appropriation-1993-act.json.b0278-ocr-quarantine` (virtiofs unlink restriction prevented direct rm). Raw HTML+PDF preserved at `raw/zambialii/act/1995/1995-033.{html,pdf}`. Action item: re-extract via dedicated OCR pipeline (tesseract/abbyy) before regex section-detection. Title says "1993" Act but PDF is from 1995 publication; cross-reference Cap discrepancy noted.

- **2000/11** Appropriation Act, 2000 — `https://zambialii.org/akn/zm/act/2000/11` — `no_sections`. HTML returned 0 akn-sections so PDF fallback engaged. PDF (816 KB) is purely scanned-image with NO embedded text layer (15 chars extractable across all pages). Parser refused to fabricate. Raw HTML+PDF preserved at `raw/zambialii/act/2000/2000-011.{html,pdf}`. Added to OCR backlog. OCR backlog now 18 items (act/2000/8, act/2000/16, act/2000/11 added; previously: si 2017/068, 2018/011, 2018/075, 2018/093, 2020/007, 2022/004, 2022/007, 2022/008, 2022/012, 2022/013, 2026/004 + earlier SIs).

**Note on 1994/40** Supplementary Appropriation (1992) Act, 1994 — committed with only
1 captured section (section 2 — "The expenditure on the services of the Republic
during the Supplementary financial year which ended on 31st December, 1992..."),
genuine Act content but with OCR noise. Section 1 (short title) was not detected
because OCR mis-rendered "1." as a non-digit token (similar to b0277 1988/32 case
which returned 0 sections). Committed because section 2 is real Act content;
flagged here for OCR-tolerant section regex follow-up to recover section 1.

OCR backlog now 18 items. All quarantined PDFs preserved on disk for re-extraction.

## Batch 0279 (2026-04-26) — Phase 4 acts_in_force fiscal-series follow-ups

- **act/2002/6 — Appropriation Act, 2002** — STATUS: deferred. HTML had <2 akn-sections (fiscal-series pattern); PDF fallback fetched **7,227,519 bytes > MAX_PDF_BYTES (4,500,000)**. Raw HTML kept at `raw/zambialii/act/2002/2002-006.html` (sha256 logged in costs.log, no PDF saved). Action: add to `oversized-pdf` queue alongside any prior >4.5 MB rejections; require either MAX_PDF_BYTES bump (eg 8 MB) or streaming/chunked PDF parser before re-attempt. No record JSON written; parser refused fabrication.
- **act/2004/6 — Supplementary Appropriation (2002) Act, 2004** — STATUS: ok (partial). Only **1 of expected 2 sections** parsed from PDF; section 1 missed by OCR (text begins mid-sentence "hereby confirmed that there was expended..."), section header heading shows hyphenated wrap "On the authority of a warrant issued by the President, it is Supplemen­..." indicating mid-line break. Same pattern as `act-zm-1994-040-supplementary-appropriation-1992-act` (b0278). Action: add to OCR section-tolerant retry queue (now 4 items: 1988/32, 1994/40, 1995/33, 2004/6).


## Batch 0280 (2026-04-26) — Phase 4 acts_in_force fiscal-series follow-ups

- **act/2005/21 — Cotton Act, 2005** — STATUS: deferred. HTML had <2 akn-sections so PDF fallback engaged; PDF fetched **6,931,314 bytes > MAX_PDF_BYTES (4,500,000)**. Raw HTML kept at `raw/zambialii/act/2005/2005-021.html` (sha256 logged in costs.log, no PDF saved). Same disposition as `act/2002/6` (b0279 - 7,227,519 bytes). Action: add to `oversized-pdf` queue (now 2 items: 2002/6, 2005/21); require either MAX_PDF_BYTES bump (eg 8 MB) or streaming/chunked PDF parser before re-attempt. No record JSON written; parser refused fabrication. NOTE: 2005/21 is the Cotton Act (non-fiscal), not an Appropriation; the oversize PDF root cause is large scanned image content, not fiscal-series formatting.

7 of 8 picks committed cleanly with 2-3 sections each (acts 2004/7, 2005/5, 2005/6, 2005/7, 2005/8, 2006/1, 2006/2 — all Appropriation/Supplementary/Excess Expenditure Appropriation series). Yield 7/8 (87.5%) — same as b0279, slightly above b0278 (75%). OCR backlog unchanged at 18 items. Section-tolerant retry queue unchanged at 4 items (1988/32, 1994/40, 1995/33, 2004/6).

## Batch 0281 (2026-04-26)
- **act/2008/5 Appropriation Act, 2008**: PDF size 5,181,722 bytes > MAX_PDF_BYTES (4,500,000). Deferred to oversize-pdf queue. Raw HTML kept.
- **act/2008/9 Supplementary Appropriation (2006) Act, 2008**: PDF parse yielded 105 sections (OCR over-match — many short-text/empty-text sections, headings include OCR fragments). Logged for section-tolerant retry queue (next backlog growth from 4 -> 5).
- Oversize-pdf queue now: 2002/6 (b0279), 2005/21 (b0280), 2008/5 (b0281). Three items.
- OCR backlog unchanged at 18 items.
- Section-tolerant retry queue: now 5 items (added 2008/9).

## Batch 0282 (2026-04-26)

- **act/2009/10 Appropriation Act, 2009**: PDF size 6,920,632 bytes > MAX_PDF_BYTES (4,500,000). Deferred to oversize-pdf queue. Raw HTML kept at `raw/zambialii/act/2009/2009-010.html`.
- **act/2009/30 Appropriation (No. 2) Act, 2009**: PDF size 6,007,886 bytes > MAX_PDF_BYTES. Deferred to oversize-pdf queue. Raw HTML kept at `raw/zambialii/act/2009/2009-030.html`.
- **act/2009/7 Supplementary Appropriation (2007) Act, 2009**: PDF parse captured only 1 section (section 2 — real Act content; section 1 missed by OCR). Same OCR-section pattern as 1988/32, 1994/40, 2004/6. Committed (content verifiably real Act language, not fabrication). Added to section-tolerant retry queue.
- Oversize-pdf queue now: 2002/6 (b0279), 2005/21 (b0280), 2008/5 (b0281), 2009/10 (b0282), 2009/30 (b0282). Five items.
- OCR backlog unchanged at 18 items.
- Section-tolerant retry queue: now 6 items (added 2009/7). Items: 1988/32, 1994/40, 1995/33, 2004/6, 2008/9, 2009/7.

## Batch 0283 (2026-04-26)

- **2012/16 Appropriation Act, 2012** — `pdf_too_large` (5,553,668 bytes > MAX_PDF_BYTES 4,500,000). Raw HTML retained at `raw/zambialii/act/2012/2012-016.html`. Added to oversize-PDF queue for host-side chunked extraction.
- **2013/19 Appropriation Act, 2013** — committed but with 1 section only (sec 1 missed by PDF text extraction; sec 2 captured). Added to OCR section-tolerant retry queue. Source HTML+PDF retained.

## Batch 0288 (2026-04-27)

- **act/2024/9 Supplementary Appropriation Act, 2024** — STATUS: deferred. HTML had <2 akn-sections (fiscal-series pattern); PDF fallback fetched 3,224,064 bytes (under MAX_PDF_BYTES 4,500,000). However, the source PDF is a multi-Act Government Gazette bundle (Vol. LX, No. 7,631, 16th August 2024) containing Acts 4-12 of 2024 in sequence. Page 1 is the Gazette Notice; pages 2 onwards are the Human Rights Commission Act (No. 4/2024). The naive top-level PDF section parser pulled 237 sections that overwhelmingly belong to OTHER Acts (Human Rights Commission, ZIALE Amendment, Matrimonial Causes Amendment, Lands Tribunal Amendment, Zambia Qualifications Authority, Civil Aviation Amendments, Kazungula Bridge Authority) rather than to Supplementary Appropriation No. 9/2024. Record was REMOVED before commit (no fabrication). Provenance entry rolled back. Raw HTML at `raw/zambialii/act/2024/2024-009.html` and raw PDF at `raw/zambialii/act/2024/2024-009.pdf` retained for traceability. Action: add to **multi-act-gazette retry queue** (NEW queue) — requires Act-boundary detection in PDF (anchor on "GOVERNMENT OF ZAMBIA" / "ACT No. X of YYYY" headers and slice sections per Act) before re-ingestion.

7 of 8 picks committed cleanly: 2021/53, 2022/7, 2022/30, 2023/10, 2023/18 (PPP Act, 162 sections via HTML), 2023/29, 2024/20. Yield 7/8 (87.5%). PPP Act 2023 is a substantive non-fiscal Act parsed via HTML akn-section parser (162 sections). All 6 fiscal-series acts have correct year-matching content (sections 1-3 referencing the correct Act citation in-text).

Multi-act-gazette retry queue: 1 item (2024/9). NEW queue introduced this tick.
Oversize-pdf queue unchanged: 5 items as of b0283 (2002/6, 2005/21, 2008/5, 2009/10, 2009/30, 2012/16 — six items, see prior batches).
OCR section-tolerant retry queue unchanged.

## Batch 0291 (2026-04-27)

- **sis/2017/43 Income Tax (Suspension of Tax on Payments to Non-Resident Contractors)(Batoka Hydro-Electric Scheme) Regulations, 2017** — STATUS: deferred (OCR backlog). Both base HTML and source.pdf fetched cleanly (HTML sha256 verified, PDF 475,677 bytes). pdfplumber returned 0 text characters across all pages — scanned-image PDF. No record JSON written; parser refused fabrication. Raw kept at `raw/zambialii/si/2017/si-zm-2017-043-...html` and `raw/zambialii/si/2017/si-zm-2017-043-...pdf`.
- **sis/2019/25 Income Tax Act (Suspension of tax on payment of interest to non-resident)(Treasury Bill and Bond) Regulations, 2019** — STATUS: deferred (OCR backlog). PDF 303,419 bytes, pdfplumber returned 0 text chars (scanned image). Raw kept at `raw/zambialii/si/2019/si-zm-2019-025-...{html,pdf}`. No record written.
- **sis/2022/4 Value Added Tax (Zero-Rating)(Amendment) Order, 2022** — STATUS: deferred (OCR backlog). PDF 343,193 bytes, pdfplumber returned 0 text chars (scanned image). Raw kept at `raw/zambialii/si/2022/si-zm-2022-004-...{html,pdf}`. No record written.

All three are the only modern (>=2017) novel sis_tax candidates upstream on zambialii (per 9-alphabet probe sweep this tick); all three require an OCR pipeline (out of toolset scope per BRIEF) before ingestion. Add to OCR backlog (was 18 items, now 21).

Other novel modern SIs discovered this tick but **out of priority_order**:
- 2025/20 Compulsory Standards (Declaration) Order, 2025 — sis_industry
- 2017/68 Standards (Compulsory Standards)(Declaration) Order, 2017 — sis_industry
- 2022/12 Societies (Amendment) Rules, 2021 — sis_governance
Reserved for future tick if these sub-phases are added to approvals.yaml priority_order.

sis_corporate (priority_order item 2) modern-era novel pool is **empty** across all 9 corporate-relevant alphabets probed (A, B, C, I, M, P, S, T, V).

## Batch 0292 — sis_employment / sis_mining / sis_family probe (2026-04-27)

Probed alphabets E, F, J, L, N, W (the highest-yield letters for the three
remaining priority sub-phases not covered in b0291's A,B,C,I,M,P,S,T,V
sweep). Robots.txt re-verified (sha256 unchanged: `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0`).

Novel modern (>=2017) results: 7 SIs, all already on disk in HTML form
from prior probe ticks; 6 of the 7 also have cached PDFs.

In-priority sub-phases:

- [2026-04-27T14:43:34Z] si/2022/013 status=pdf_parse_empty url=https://zambialii.org/akn/zm/act/si/2022/13 batch=0292 sub_phase=sis_employment note=re-attempt; same pdfplumber 0-char result as b0184/b0200/b0205/b0221; remains in OCR backlog
- sis_mining (alphabet=M probed b0291): 0 novel modern
- sis_family (alphabets F, J, L, M, W): 0 novel modern matching Marriage / Matrimonial / Children / Juvenile / Maintenance / Adoption / Affiliation patterns

Off-priority novel modern SIs encountered (reserved — not in
approvals.yaml priority_order; not picked):

| Year/Num | Title (truncated)                                                | Sub-phase     | OCR status |
|----------|------------------------------------------------------------------|---------------|------------|
| 2026/4   | Electricity (Transmission) (Grid Code) Regulations, 2026         | sis_energy    | OCR-backlog (b0245) |
| 2022/7   | National Archives (Fees) Regulations, 2021                       | sis_archives  | OCR-backlog (b0184) |
| 2022/8   | National Assembly By-Election (Kabwata) Order, 2022              | sis_elections | OCR-backlog (b0200) |
| 2018/11  | Forests (Community Forest Management) Regulations, 2018          | sis_forests   | HTML cached only — PDF fetch deferred (off-priority) |
| 2018/75  | National Assembly By-Election (Mangango) Order, 2018             | sis_elections | OCR-backlog (b0184) |
| 2018/93  | National Assembly By-Election (Sesheke) Order, 2018              | sis_elections | OCR-backlog (b0184) |

Conclusion: sis_employment-modern (priority_order item 4),
sis_mining-modern (item 7), sis_family-modern (item 8) are all at
upstream steady state for the worker's current toolset (requests +
beautifulsoup4 + pdfplumber). The single text-extractable candidate
(2022/13 sis_employment) returns 0 chars from pdfplumber and remains in
the OCR backlog (no change to its status this tick).

## Batch 0293 — alphabet exhaust closure (2026-04-27)

This tick swept the 7 remaining uncovered zambialii alphabet listings
(D, G, H, K, O, R, U) for novel modern (>=2017) SIs. Combined with
b0291 (A,B,C,I,M,P,S,T,V) and b0292 (E,F,J,L,N,W), all 22 active
letters have now been exhaustively probed (Q, X, Y, Z omitted by
design — empty/near-empty for Zambian SI listings).

**0 in-priority candidates** (sis_corporate, sis_tax, sis_employment,
sis_mining, sis_family, sis_data_protection — all empty across the 7
new letters).

**1 off-priority reserve** (2020/7 Road Traffic (Speed Limits)
Regulations, 2019 — already in OCR backlog from b0276).

37 raw "novel" hits from the discover script were re-classified as
already-in-corpus under non-standard filenames (Urban and Regional
Planning, Diplomatic Immunities, Higher Education, Defence Force,
Disaster Management, etc.) by reading citation/id JSON fields from
each on-disk record. Discover script's filename-only existing-set
extraction missed these; integrity check uses comprehensive
content-fall-through to verify.

**Refresh probes (steady-state confirmation):**
- zambialii /legislation/recent: 13 acts, ALL 13 in corpus.
- parliament /acts-of-parliament page 0: 20 acts (2026/1..11 +
  2025/21..29), ALL 20 in corpus.

Phase 4 / acts_in_force chronological-first sweep confirmed complete
through 2026/11. Every priority_order sub-phase confirmed at upstream
steady state for the requests + beautifulsoup4 + pdfplumber toolset.

No new gaps introduced. No records written.

## 2026-04-29 — batch 0341 — Phase 5 kickoff (ZMCC judgments)

The following ConCourt 2026 judgments were fetched but deferred from this batch
because the ZambiaLII summary text alone does not contain a disposition phrase
mappable to the locked Phase 5 outcome enum (`allowed | dismissed | upheld |
overturned | remitted | struck-out | withdrawn`). No fabrication: the records
are not written. Re-attempt next tick by reading the order paragraph from the
PDF body (pdfplumber).

- [2026] ZMCC 7 — Climate Action Professionals Zambia v Attorney General (2025/CCZ/0025)
  — https://zambialii.org/akn/zm/judgment/zmcc/2026/7/eng@2026-03-25
  — summary is a question of law, no disposition phrase: "Whether non-implementation of statutory climate mechanisms constitutes a justiciable constitutional violation."

- [2026] ZMCC 6 — Munir Zulu v Attorney General and Anor (2025/CCZ/0010)
  — https://zambialii.org/akn/zm/judgment/zmcc/2026/6/eng@2026-03-19
  — summary is a question of law, no disposition phrase: "Whether Article 76 parliamentary privilege protects media statements made within National Assembly precincts."

## 2026-04-29 — batch 0342 — Phase 5 ZMCC continuation

Resolved both b0341 deferrals plus ingested ZMCC 2026/02:

- **[2026] ZMCC 7** (Climate Action Professionals Zambia v Attorney General,
  2025/CCZ/0025) — RESOLVED. Disposition inferred from PDF body paragraph [62]
  ("The Petition is therefore dismissed for want of jurisdiction"). Outcome:
  `dismissed`. Record written:
  judgment-zm-2026-zmcc-07-climate-action-professionals-zambia-v-attorney-gen.

- **[2026] ZMCC 6** (Munir Zulu v Attorney General and Anor, 2025/CCZ/0010) —
  RESOLVED. Disposition inferred from PDF body paragraph 5.34 ("That said, this
  Petition fails for lack of merit"). Outcome: `dismissed`. Record written:
  judgment-zm-2026-zmcc-06-munir-zulu-v-attorney-general-and-anor.

- **[2026] ZMCC 2** (Morgan Ng'ona v Attorney General and Anor, 2025/CCZ/0029)
  — INGESTED. Disposition inferred from PDF body paragraph 28–29 ("the Petition
  is devoid of merit ... 29.1. The Petition is dismissed"). Outcome:
  `dismissed`. Munalula PC partial-dissented on reasoning (paras 25–28) but
  agreed petition should be dismissed; recorded as `concurring` since outcome
  aligns. Refinement to `partial-dissenting` with reasoning_tags is left to a
  later pass. Record written:
  judgment-zm-2026-zmcc-02-morgan-ng-ona-suing-as-secretary-general-of-the-pa.

ZMCC 2026/01 was on the b0342 target list but the long-running fetcher process
was killed by the sandbox before reaching it. Will retry in next tick.

## 2026-04-29  Phase 5 ZMCC sweep — batch 0343 (continuation of b0341/b0342)

Targets (8 candidates, ZMCC 2026/01 + 7 most-recent ZMCC 2025) all DEFERRED to a
later tick after a parser-safety review. Raw HTML+PDF persisted on disk for all
8 and the parser ran cleanly, but four of the disposition inferences came from
unsafe sources (regex over the PDF tail / full body matching disposition words
in citations to OTHER cases). Per non-negotiable #1 (no fabrication) the
parser-version-0.2.0 inference policy is being tightened to require an explicit
order-paragraph anchor (one of: "It is ordered", "It is hereby ordered",
"We accordingly", "We therefore", "For the foregoing reasons", "Accordingly,"
within ~1500 chars of an enum-mappable disposition phrase). Records that cannot
be matched to such an anchor will be deferred rather than written. The four
unsafe inferences from this batch:

- **[2026] ZMCC 1** (Tresford Chali v The Judicial Complaints Commission, 2026-01-20):
  parser inferred `overturned` from a `set aside` match in the PDF body — most
  likely a quote from a cited authority, not the disposition of THIS case.
  outcome_detail produced: "d by Judge Mulonda." (clearly a mid-word fragment).
  DEFER until the order paragraph is hand-anchored or the parser is tightened.

- **[2025] ZMCC 32** (The Law Association of Zambia and Ors v The Attorney
  General, 2025-12-16): parser inferred `overturned` from a `set aside` match
  in the PDF tail. outcome_detail produced "another v Attorney Generall4l." —
  almost certainly a cross-reference to another case in the index, not this
  case's disposition. DEFER.

- **[2025] ZMCC 28** (Brian Mundubile and Anor v Hakainde Hichilema and Anor,
  2025-12-05): parser inferred `allowed` from "declared ... violated" pattern
  in the PDF body. outcome_detail produced "the Godfrey Miyanda v Attorney
  General case supra." — a citation reference, not the disposition. DEFER.
  Also only 1 judge resolved (Mwandenga); the panel for ConCourt judgments is
  typically 3–7, so the Judges metadata field on the HTML page may be malformed
  on this entry. Re-parse needed.

- **[2025] ZMCC 27** (Munir Zulu and Anor v Attorney General and Ors,
  2025-12-05): parser inferred `allowed` from a similar weak pattern; only 1
  judge (Mulongoti) resolved — same panel-size red flag as ZMCC 28. DEFER.

The other four candidates were correctly identified as outcome-not-inferable
from the summary alone:

- **[2025] ZMCC 33** (Miles Bwalya Sampa v The Attorney General and Ors,
  2025-12-18): summary describes ratio (subscription vs. State equity disposal
  under Article 210) but no disposition phrase. DEFER.

- **[2025] ZMCC 31** (Munir Zulu and Anor v Attorney General and Ors,
  2025-12-10): summary contains "Application for contempt dismissed for being
  procedurally misconceived..." which DOES describe the disposition (`dismissed`),
  but the phrase "Application for contempt dismissed" is not matched by the
  current `(?:application|...) (?:is )?(?:hereby )?dismissed` regex because the
  noun phrase has the qualifier "for contempt" before the verb. Easy parser
  improvement next tick. DEFER.

- **[2025] ZMCC 30** (Legal Resources Foundation Limited v The Attorney General,
  2025-12-11): summary describes the prima facie / irreparable harm test for
  staying judicial appointments — no disposition phrase. DEFER.

- **[2025] ZMCC 29** (Law Association of Zambia and Ors v Attorney General,
  2025-12-08): summary says "Court granted joinder to two intended interested
  parties" — likely `allowed` but the joinder language isn't in the current
  outcome enum mapping. DEFER until a joinder→`allowed` rule is added or the
  PDF order paragraph is anchored.

Raw HTML+PDF for all 8 are persisted on disk under
`raw/zambialii/judgments/zmcc/{2025,2026}/` — no re-fetch needed next tick;
the next tick can rerun the parser-only step against the persisted bytes once
the inference policy is tightened. The buggy first-pass record JSONs were
moved to `_stale_b0343_bad_records/` (untracked) before this commit so the
corpus does not contain any of the unsafe inferences.

## 2026-04-29 — batch 0344 — Phase 5 ZMCC re-parse (tightened policy)

Re-parsed the 8 ZMCC raw HTML+PDF pairs persisted at b0343 using a tightened
disposition policy (`scripts/batch_0344_parse.py`, `parser_version: 0.3.0`).
3 ingested from summary text alone; 5 deferred because the summary describes
a holding/issue without an enum-mappable disposition phrase AND no eligible
PDF order anchor match was found within the strict 800-char window.

**Ingested (3) — moves Phase 5 from 9 → 12 / 100–160 target:**

- **[2025] ZMCC 27** (Munir Zuu and Anor v Attorney General and Ors,
  2025/CCZ/009, 2025-12-05) — `dismissed` from summary "Court dismissed
  application to disqualify petitioners' counsel for alleged conflict
  absent evidence of confidential information or real prejudice." Single
  judge: Mulongoti.

- **[2025] ZMCC 29** (Law Association of Zambia and Ors v Attorney General,
  2025/CCZ/0029, 2025-12-08) — `allowed` from summary "Court granted
  joinder to two intended interested parties, holding standing rules broad
  and persons may appear in person." Single judge: Kawimbe (alias added:
  HON. LADY JUSTICE MARIA MAPANI - KAWIMBE).

- **[2025] ZMCC 31** (Munir Zulu and Anor v Attorney General and Ors,
  2025/CCZ/009, 2025-12-10) — `dismissed` from summary "Application for
  contempt dismissed for being procedurally misconceived for failing to
  invoke a proper rule or authority." Single judge: Mulongoti (alias added:
  Lady Justice J.Z Mulongoti).

**Deferred (5) — raw on disk, awaiting either hand-anchored PDF order
paragraph or further summary-pattern extension:**

- **[2026] ZMCC 1** (Tresford Chali v Judicial Complaints Commission,
  2024/CCZ/0019, 2026-01-20): summary describes the holding only — "A
  challenge to the JCC's report and removals must proceed by judicial
  review in the High Court, not by original petition here." No disposition
  phrase. PDF lacks an order-anchor match within window. DEFER.

- **[2025] ZMCC 33** (Miles Bwalya Sampa v Attorney General, 2024/CCZ/0024,
  2025-12-18): summary describes ratio (subscription vs. State equity
  disposal under Article 210); no disposition phrase. DEFER.

- **[2025] ZMCC 32** (Law Association of Zambia v Attorney General,
  2025/CCZ/0029, 2025-12-16): summary describes the procedural holding
  ("Renewal before the full Court is the proper route to challenge a
  single judge's interlocutory ruling; late conservatory relief denied").
  Phrase "conservatory relief denied" reads as a disposition but is not
  in the current enum mapping; rather than fabricate, DEFER.

- **[2025] ZMCC 30** (Legal Resources Foundation v Attorney General,
  2025/CCZ/0021, 2025-12-11): summary is a question of law ("Whether the
  applicant proved a prima facie constitutional breach and irreparable
  harm to justify staying judicial appointments"). DEFER.

- **[2025] ZMCC 28** (Brian Mundubile v Hakainde Hichilema, 2025/CCZ/0026,
  2025-12-05): summary describes the holding ("constitutional challenges
  implicating the President must proceed against the Attorney-General;
  the President has immunity from personal civil suits"). No disposition
  phrase. DEFER.

The four buggy first-pass record JSONs from b0343 remain in
`_stale_b0343_bad_records/` (untracked, not in the corpus). They will not
be re-introduced; b0344 records are written fresh from raw bytes.

Parser-tightening summary (locked at parser_version 0.3.0):
- PRIMARY source for outcome: ZambiaLII summary `<dd>` block, with
  patterns extended to include `Court dismissed`, `Court (allowed|
  granted|upheld|overturned)`, `Application for <X> dismissed`,
  `joinder granted` / `Court granted joinder`.
- SECONDARY source: PDF order-anchor matches only (anchor list locked,
  800-char window).
- pdf-tail and pdf-full sweeps removed.
- Soft anchors ("for the foregoing", "in conclusion", "we conclude",
  "accordingly,") rejected outright.
- outcome_detail safety guards: word-boundary start, ≥12 chars alphabetic
  content, no cross-reference markers (`case supra`, ` supra`, `another v
  `, `Generall4l`, `Mulonda`).

## batch-0345 deferrals (Phase 5 ZMCC 2025 sweep slice 19–26) — 2026-04-29T14:27:57Z

Per BRIEF.md non-negotiable #1, the following 6 candidates could not safely be parsed under tightened parser_version 0.3.0 (no enum-mappable disposition phrase in summary AND no qualifying PDF order-anchor match within 800 chars). Raw HTML+PDF remain on disk under raw/zambialii/judgments/zmcc/2025/.

- **[2025] ZMCC 25** (zmcc 2025/25, deferred 2026-04-29): outcome_not_inferable_under_tightened_policy. URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/25/eng@2025-12-04. Summary: "Court refused stay of Speaker's vacancy ruling absent special and convincing grounds; merits not to be decided interlocutorily."

- **[2025] ZMCC 24** (zmcc 2025/24, deferred 2026-04-29): outcome_not_inferable_under_tightened_policy. URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/24/eng@2025-11-28. Summary: "The Constitutional Court held the Attorney General may represent the Speaker as the legal representative of 'Government' and ordered joinder of the Attorney General."

- **[2025] ZMCC 23** (zmcc 2025/23, deferred 2026-04-29): outcome_not_inferable_under_tightened_policy. URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/23/eng@2025-11-27. Summary: "A pension-quantum and payroll dispute is a labour matter for the Industrial Relations Division, not the Constitutional Court."

- **[2025] ZMCC 22** (zmcc 2025/22, deferred 2026-04-29): outcome_not_inferable_under_tightened_policy. URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/22/eng@2025-11-27. Summary: "Declaratory relief was academic; transitional Act provisions governed eligibility, and Article 267(3)(b)(c) did not affect the Court’s decision."

- **[2025] ZMCC 21** (zmcc 2025/21, deferred 2026-04-29): outcome_not_inferable_under_tightened_policy. URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/21/eng@2025-11-25. Summary: "Application to suspend a presidentially appointed constitutional Technical Committee dismissed for failing to show irreparable harm."

- **[2025] ZMCC 19** (zmcc 2025/19, deferred 2026-04-29): outcome_not_inferable_under_tightened_policy. URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/19/eng@2025-09-30. Summary: ""

## Batch 0346 deferrals (2026-04-29)
- **[2025] ZMCC 18** (zmcc 2025/18, deferred 2026-04-29): outcome_not_inferable_under_tightened_policy. URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/18/eng@2025-09-30. Summary: "Whether a local authority resolution increasing advertising fees is a statutory instrument requiring gazetting and reporting under Articles 67 and 199."
- **[2025] ZMCC 17** (zmcc 2025/17, deferred 2026-04-29): outcome_not_inferable_under_tightened_policy. URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/17/eng@2025-08-27. Summary: "Petitioner had standing but challenge to parliamentary vacancy improperly filed in Constitutional Court; vacancy questions fall to High Court/tribunal under section 96 EPA."
- **[2025] ZMCC 16** (zmcc 2025/16, deferred 2026-04-29): outcome_not_inferable_under_tightened_policy. URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/16/eng@2025-08-25. Summary: "A single judge may grant an extension to file amicus materials; delay condoned in the interests of justice, but costs awarded."
- **[2025] ZMCC 15** (zmcc 2025/15, deferred 2026-04-29): outcome_not_inferable_under_tightened_policy. URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/15/eng@2025-07-23. Summary: "A citizen acting in the public interest has standing to challenge alleged constitutional contraventions before the Constitutional Court."
- **[2025] ZMCC 14** (zmcc 2025/14, deferred 2026-04-29): outcome_not_inferable_under_tightened_policy. URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/14/eng@2025-07-28. Summary: "Article 266 defines a child as any person below eighteen; attaining eighteen confers adult status under the Constitution."
- **[2025] ZMCC 12** (zmcc 2025/12, deferred 2026-04-29): outcome_not_inferable_under_tightened_policy. URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/12/eng@2025-06-27. Summary: "Court holds it can review pre‑Bill executive initiation of constitutional amendments and requires people‑driven wide consultations."
- **[2025] ZMCC 11** (zmcc 2025/11, deferred 2026-04-29): outcome_not_inferable_under_tightened_policy. URL: https://zambialii.org/akn/zm/judgment/zmcc/2025/11/eng@2025-06-19. Summary: "A pre-2016 pension dispute is a labour matter and outside the Constitutional Court’s jurisdiction."

## Batch 0347 — ZMCC 2025/{10,9,8,7,6,5,4,3} deferrals (parser_version 0.3.0)

All raw HTML+PDF persisted under `raw/zambialii/judgments/zmcc/2025/`. Deferrals are 'outcome_not_inferable_under_tightened_policy' — to be revisited once the parser supports hand-anchored PDF order paragraphs or the locked SUMMARY_PATTERNS subject vocabulary is widened (parser_version bump).

- [2025] ZMCC 10 — Munir Zulu v AG and Ors (2025-06-04) — substantive ratio, no enum verb in summary
- [2025] ZMCC 9 — The People v AG (2025-02-10) — same ratio family as 2025/10
- [2025] ZMCC 8 — Richard Sakala v AG (2025-04-01) — conditional verb (delay 'may justify dismissal')
- [2025] ZMCC 7 — Munir Zulu v AG and Ors (2025-04-07) — jurisdictional ratio, no disposition verb
- [2025] ZMCC 6 — Miles Bwalya Sampa v AG (2025-03-24) — 'denied' not on enum
- [2025] ZMCC 5 — Miza Phiri Jr v Mwanza & Ors (2025-03-24) — procedural ratio, no enum verb
- [2025] ZMCC 3 — Petrushika Trading v AG (2025-03-06) — verb 'dismissed' present but subject 'Challenge' is not in locked SUMMARY_PATTERNS subject vocabulary; not loosened mid-tick

## 2026-04-29 batch-0348 deferrals (parser_version 0.3.0)

Targeted ZMCC 2025/{2,1} + ZMCC 2024/{27,26,25,24,23,22}.
Records written: 2 (judgment-zm-2024-zmcc-26-chipa-chibwe-suing-in-his-capacity-s-chairman-of-t, judgment-zm-2024-zmcc-24-sean-tembo-v-the-attorney-general).
Deferred: 6 (all 'outcome_not_inferable_under_tightened_policy').

All raw HTML+PDF persisted under `raw/zambialii/judgments/zmcc/{2024,2025}/`.
Deferrals to be revisited once the parser supports hand-anchored PDF order paragraphs or the locked SUMMARY_PATTERNS subject vocabulary is widened (parser_version bump).

- [2025] ZMCC 2 — https://zambialii.org/akn/zm/judgment/zmcc/2025/2/eng@2025-02-06 — outcome_not_inferable_under_tightened_policy; summary head: Constitutional values alone do not found Constitutional Court jurisdiction; a specific constitutional question is required.
- [2025] ZMCC 1 — https://zambialii.org/akn/zm/judgment/zmcc/2025/1/eng@2025-02-13 — outcome_not_inferable_under_tightened_policy; summary head: Applicants who retired before 2016 cannot rely on Article 189; their pension disputes against respondent are private law matters.
- [2024] ZMCC 27 — https://zambialii.org/akn/zm/judgment/zmcc/2024/27/eng@2024-12-10 — outcome_not_inferable_under_tightened_policy; summary head: Whether transitional savings preserved the repealed term‑limit regime, rendering the former president ineligible for future presidential elections.
- [2024] ZMCC 25 — https://zambialii.org/akn/zm/judgment/zmcc/2024/25/eng@2024-11-13 — outcome_not_inferable_under_tightened_policy; summary head: Originating summons for abstract interpretation of Article 74(2) dismissed as the dispute is personalized, contentious and requires trial.
- [2024] ZMCC 23 — https://zambialii.org/akn/zm/judgment/zmcc/2024/23/eng@2024-10-29 — outcome_not_inferable_under_tightened_policy; summary head: An interim stay cannot be granted where the presidential suspension has already been implemented; single judge declined to decide standing.
- [2024] ZMCC 22 — https://zambialii.org/akn/zm/judgment/zmcc/2024/22/eng@2024-10-15 — outcome_not_inferable_under_tightened_policy; summary head: Constitutional electoral timelines (90‑day by‑election; 7/21‑day nomination challenge) are mandatory and cannot be extended by court proceedings.

## batch-0349 deferred (2026-04-29)

Reason: outcome_not_inferable_under_tightened_policy (parser_version 0.3.0). Raw HTML+PDF on disk; can be revisited when parser is widened (parser_version bump, not a tick-time change).

- [2024] ZMZMCC 21 (2024-10-11) — https://zambialii.org/akn/zm/judgment/zmcc/2024/21/eng@2024-10-11
- [2024] ZMZMCC 20 (2024-10-03) — https://zambialii.org/akn/zm/judgment/zmcc/2024/20/eng@2024-10-03
- [2024] ZMZMCC 19 (2024-07-26) — https://zambialii.org/akn/zm/judgment/zmcc/2024/19/eng@2024-07-26
- [2024] ZMZMCC 18 (2024-07-26) — https://zambialii.org/akn/zm/judgment/zmcc/2024/18/eng@2024-07-26
- [2024] ZMZMCC 17 (2024-07-29) — https://zambialii.org/akn/zm/judgment/zmcc/2024/17/eng@2024-07-29
- [2024] ZMZMCC 16 (2024-07-10) — https://zambialii.org/akn/zm/judgment/zmcc/2024/16/eng@2024-07-10
- [2024] ZMZMCC 15 (2024-07-08) — https://zambialii.org/akn/zm/judgment/zmcc/2024/15/eng@2024-07-08

## batch-0350 deferred (2026-04-29)

Reason: outcome_not_inferable_under_tightened_policy (parser_version 0.3.0). Raw HTML+PDF on disk; can be revisited when parser is widened (parser_version bump, not a tick-time change).

- [2024] ZMCC 13 (2024-06-28) — https://zambialii.org/akn/zm/judgment/zmcc/2024/13/eng@2024-06-28
- [2024] ZMCC 11 (2024-06-17) — https://zambialii.org/akn/zm/judgment/zmcc/2024/11/eng@2024-06-17
- [2024] ZMCC 10 (2024-06-25) — https://zambialii.org/akn/zm/judgment/zmcc/2024/10/eng@2024-06-25
- [2024] ZMCC 8 (2024-06-07) — https://zambialii.org/akn/zm/judgment/zmcc/2024/8/eng@2024-06-07
- [2024] ZMCC 7 (2024-06-06) — https://zambialii.org/akn/zm/judgment/zmcc/2024/7/eng@2024-06-06
- [2024] ZMCC 6 (2024-04-16) — https://zambialii.org/akn/zm/judgment/zmcc/2024/6/eng@2024-04-16


## Batch 0351 — ZMCC 2024/{5,4,3,2,1} parser-deferred (2026-04-29)

All five raw HTML+PDF pairs persisted under `raw/zambialii/judgments/zmcc/2024/`. Outcome could not be inferred under parser_version 0.3.0's tightened SUMMARY_PATTERNS + locked PDF_ORDER_ANCHORS. Re-parse without re-fetch when parser is widened.

- **[2024] ZMCC 5** — Milingo Lungu v The Attorney General and Another (2024-03-15). Summary: "The Constitutional Court lacks power to stay subordinate criminal proceedings; the single judge's stay was nullified and discharged."
- **[2024] ZMCC 4** — Moses Sakala v The Attorney General and Another (2024-02-23). Summary: "Intended Party joined as 3rd Respondent because the reliefs directly affect him; no costs awarded."
- **[2024] ZMCC 3** — Hastings Mwila v Local Authorities Superannuation Fund (2024-02-09). Summary: "Whether the petitioner should have remained on the respondent's payroll pending payment of a commuted LASF lump-sum pension benefit."
- **[2024] ZMCC 2** — Institute of Law, Policy Research and Human Rights (2024-01-17). Summary: "An individual directly affected by interpretation of Article 74(2) may be joined as an interested party to adjudicate rights and issues."
- **[2024] ZMCC 1** — Bowman Chilosha Lusambo v Bernard Kanengo and Others (2024-01-25). Summary: "Nomination disputes belong to Article 52(4) proceedings; election petitions require proving substantial non‑compliance affecting results."

## 2026-04-29 — batch-0352 deferrals (Phase 5, ZMCC 2023)

Seven ZMCC 2023 candidates deferred under
`outcome_not_inferable_under_tightened_policy` (parser_version 0.3.0).
Raw HTML+PDF on disk under `raw/zambialii/judgments/zmcc/2023/`. No
re-fetch needed when the parser is widened (a `parser_version` bump).

| Year/# | Date       | Case (case_name preview) | source_hash (HTML) | raw_sha256 (PDF) |
|--------|------------|--------------------------|--------------------|------------------|
| 2023/27 | 2023-08-03 | Zambia Community Development Initiative Programme | (see raw dir)      | (see raw dir)    |
| 2023/26 | 2023-12-16 | Milingo Lungu v The Attorney General and Anor      | (see raw dir)      | (see raw dir)    |
| 2023/25 | 2023-12-08 | Sean Tembo v The Attorney General                  | (see raw dir)      | (see raw dir)    |
| 2023/24 | 2023-12-01 | Fredson Kango Yamba v The Principal Resident Magis | (see raw dir)      | (see raw dir)    |
| 2023/23 | 2023-11-07 | Milingo Lungu v The Attorney General and Anor      | (see raw dir)      | (see raw dir)    |
| 2023/21 | 2023-10-27 | (companion to 2023/22)                             | (see raw dir)      | (see raw dir)    |
| 2023/20 | 2023-10-26 | (case_name from H1)                                | (see raw dir)      | (see raw dir)    |

Reason: neither the locked `SUMMARY_PATTERNS` nor any locked
`PDF_ORDER_ANCHORS` matched in a 800-char window in the relevant raw
bytes. Per BRIEF.md non-negotiable #1 (no fabrication), no record was
written. Re-parse on next parser_version bump.

## batch-0353 (Phase 5 ZMCC 2023 sweep, 2026-04-29T18:07:50Z)

- `judgment-zm-2023-zmcc-17` — **PDF 404 at source**. URL: https://zambialii.org/akn/zm/judgment/zmcc/2023/17/eng/source.pdf — HTML on disk; PDF unavailable from ZambiaLII. Hard upstream gap.
- `zmcc 2023/19` — outcome not inferable under v0.3.0; raw on disk; summary head: "Constitutional Court lacks jurisdiction over redundancy-related salary and damages claims; Industrial Relations Division is competent."
- `zmcc 2023/18` — outcome not inferable under v0.3.0; raw on disk; summary head: "A district council election can only be annulled by a petition founded on Section 97 of the Electoral Process Act."
- `zmcc 2023/16` — outcome not inferable under v0.3.0; raw on disk; summary head: "Constitutional Court lacked jurisdiction to entertain a petition challenging nominations and rescinding resignations in parliamentary by-elections."
- `zmcc 2023/15` — outcome not inferable under v0.3.0; raw on disk; summary head: "Whether the JCC can investigate pre-appointment misconduct and whether failure to follow Article 144 suspension procedure nullifies removal."
- `zmcc 2023/14` — outcome not inferable under v0.3.0; raw on disk; summary head: "Challenge to DC appointments dismissed for lack of evidence and because employment-related claims lie outside Constitutional Court jurisdiction."
- `zmcc 2023/13` — outcome not inferable under v0.3.0; raw on disk; summary head: "AG not required to prosecute JCC complaints; JCC procedure and President’s suspension/removal of DPP were lawful."
- `zmcc 2023/12` — outcome not inferable under v0.3.0; raw on disk; summary head: "Article 165 is prospective; Constitutional Court lacks jurisdiction to decide ordinary chieftaincy succession disputes."

## batch-0354 (Phase 5 ZMCC 2023 sweep continuation, 2026-04-29)

ZMCC 2023 numbering gaps confirmed via dedicated 404 probes:

- `zmcc 2023/11` — **HTTP 404 at source** (number not assigned upstream). Hard gap, not retried.
- `zmcc 2023/9`  — **HTTP 404 at source** (number not assigned upstream). Hard gap, not retried.

Six ZMCC 2023 candidates deferred under `outcome_not_inferable_under_tightened_policy` (parser_version 0.3.0). Raw HTML+PDF on disk under `raw/zambialii/judgments/zmcc/2023/`. No re-fetch needed when the parser is widened (a `parser_version` bump).

- `zmcc 2023/10` — outcome not inferable under v0.3.0; raw on disk; summary head: "Court held no mandatory advertising of judicial vacancies but requires human rights or constitutional law training/experience for Constitutional Court judges."
- `zmcc 2023/8` — outcome not inferable under v0.3.0; raw on disk; summary head: "Retirement in national interest triggers Article 189 protections; payroll-based allowances payable, but NAPSA eligibility rules remain valid."
- `zmcc 2023/6` — outcome not inferable under v0.3.0; raw on disk; summary head: "Court finds State has not fully implemented judicial financial autonomy but declines to void transitional emoluments provisions."
- `zmcc 2023/5` — outcome not inferable under v0.3.0; raw on disk; summary head: "Article 52(6) does not permit independent candidates to withdraw after nominations; ECZ cancels only for party candidate resignation, death or disqualification."
- `zmcc 2023/4` — outcome not inferable under v0.3.0; raw on disk; summary head: "Local authorities qualify as "persons" under Article 266; Article 160 mandates one‑year immunity against enforcement; other issues non‑constitutional."
- `zmcc 2023/3` — outcome not inferable under v0.3.0; raw on disk; summary head: "Whether vacancies caused by nullification of an election fall within Article 72(4)'s ban on re-contesting during that Parliament."
- `zmcc 2022/34` — outcome not inferable under v0.3.0; raw on disk; summary head: "An election may only be annulled where widespread malpractice by the candidate or agents is proved to a high degree of convincing clarity."
- `zmcc 2022/33` — outcome not inferable under v0.3.0; raw on disk; summary head: "Appellate court reversed nullification: petitioners failed to prove widespread, high-standard electoral malpractice and some agent-attributions were unsupported."
- `zmcc 2022/32` — outcome not inferable under v0.3.0; raw on disk; summary head: "A renewed application from a single-judge ruling must be by summons; improperly commenced motion dismissed, corrected record ordered."
- `zmcc 2022/31` — outcome not inferable under v0.3.0; raw on disk; summary head: "Court refused to interpret Article 52(6) because the applicant’s challenge was speculative, academic and lacked a factual cause of action."
- `zmcc 2022/30` — outcome not inferable under v0.3.0; raw on disk; summary head: "Joinder refused where applicant failed to show the proposed party had sufficient interest or nexus to the constitutional petition."

## Batch 0358 deferrals (2026-04-29)

Slice: ZMCC 2022/{11..4} — 8 candidates, all DEFERRED under
`outcome_not_inferable_under_tightened_policy` (parser_version 0.3.0).
Raw HTML+PDF retained on disk in raw/zambialii/judgments/zmcc/2022/.

  * 2022/11 — Chisanga & Anor v Electoral Commission of Zambia (2022-05-16)
  * 2022/10 — Lungu v Attorney General & Ors (2022-05-19)
  * 2022/09 — Tembo (party president) (2022-03-14)
  * 2022/08 — Kafwaya v Katonga & Ors (2022-04-13)
  * 2022/07 — Law Association of Zambia v Attorney General (2022-03-22)
  * 2022/06 — Malanji v Mulenga & Anor (2022-02-24)
  * 2022/05 — Moyo v Attorney General (2022-02-28)
  * 2022/04 — Chapter One Foundation Ltd v Attorney General (2022-02-25)

Reason: each summary frames the constitutional / legal question without
matching a top-level disposition regex. Per BRIEF.md non-negotiable #1
(no fabrication), no record written. Will be re-considered if the
parser policy is loosened or a higher-version parser is adopted.

## batch-0359 deferrals (parser_v0.3.0 tightened policy)

Six of eight ZMCC candidates fetched in b0359 deferred under
`outcome_not_inferable_under_tightened_policy`. Raw HTML+PDF retained on
disk for re-parse without re-fetch when (or if) the parser policy is
loosened or a higher-version parser is adopted. None of these are
*hard* gaps — the upstream sources are healthy.

| Court | Year/# | Slug | Notes |
|-------|--------|------|-------|
| ZMCC | 2022/03 | shah-and-anor-v-the-attorney-general | summary frames issue, no top-level disposition regex match |
| ZMCC | 2022/02 | lieutenant-muchindu-v-attorney-general | summary frames issue |
| ZMCC | 2022/01 | chapter-one-foundation-ltd-v-attorney-general | summary frames issue |
| ZMCC | 2021/21 | mulubisha-v-attorney-general | summary frames issue |
| ZMCC | 2021/19 | wang-shunxue-and-attorney-general-and-another | summary frames issue |
| ZMCC | 2021/18 | chapter-one-foundation-limited-and-ors-v-the-attorney-general | summary frames issue |

Top of ZMCC 2021 confirmed at 2021/24 (2021/25 returns HTTP 404 upstream).
2021/{24,23} not yet fetched — first targets of the next tick.

### batch-0359 parser bug (JJS title) — 2021/22 recovered, defer until parser fix

Parser v0.3.0 mishandled `Chibomba JJS` (Hilda Chibomba was previously JS — Supreme Court — and had used the JJS title before becoming PC of the Constitutional Court). The parser's title regex
`PC|DPC|CJ|DCJ|JCC|JJC|JC|JS|JA|J|JJ|JJA` does NOT include `JJS`, so the
last-token fallback produced canonical `Jjs` from the title fragment.

Action this tick: deleted the bad record `judgment-zm-2021-zmcc-22-bozy-simutanda-as-attorney-for-his-royal-highness.json` and reverted the spurious `Jjs` registry entry. 2021/22 deferred under
`parser_v0.3.0_jjs_title_unhandled`. Raw HTML+PDF retained on disk
(html sha256:9837e53618ae5525..., pdf sha256:d2fc958426afa436...).

Suggested fix for next parser version (0.3.1):
- Add `JJS` to `parse_one_judge`'s title regex (Constitutional Court
  alternative spelling for retired/older Supreme Court justices).
- Re-run on this raw on disk to recover Chibomba's record without
  re-fetch.

## Batch 0360 — 2026-04-30 — ZMCC 2021/{24,23,17,16,15,14,13,12} deferred under parser_v0.3.0 tightened policy

| Court/Year/# | Date | Slug | Reason |
|--------------|------|------|--------|
| zmcc/2021/24 | 2021-10-27 | gilford-malenji-v-zambia-airports-corporation-limi | outcome_not_inferable_under_tightened_policy |
| zmcc/2021/23 | 2021-11-29 | charles-chihinga-v-new-future-financial-company-li | outcome_not_inferable_under_tightened_policy |
| zmcc/2021/17 | 2021-09-20 | anderson-mwale-buchisa-mwalongo-and-kola-odubote-v | outcome_not_inferable_under_tightened_policy |
| zmcc/2021/16 | 2021-11-22 | sampa-v-mundubile-and-anor | outcome_not_inferable_under_tightened_policy |
| zmcc/2021/15 | 2021-09-17 | shunxue-v-the-attorney-general-anor | outcome_not_inferable_under_tightened_policy |
| zmcc/2021/14 | 2021-07-13 | legal-resources-foundation-limited-2-others-v-edga | outcome_not_inferable_under_tightened_policy |
| zmcc/2021/13 | 2021-07-20 | bric-back-limited-t-a-gamamwe-ranches-v-kirkpatric | outcome_not_inferable_under_tightened_policy |
| zmcc/2021/12 | 2021-06-30 | dipak-patel-v-minister-of-finance-and-attorney-gen | outcome_not_inferable_under_tightened_policy |

Raw HTML+PDF retained on disk for re-parse under parser_v0.3.1+.
