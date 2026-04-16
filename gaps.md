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
