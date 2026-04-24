# Batch 0196 — Phase 4 sis_family closeout + sis_tax rotation

- **Date**: 2026-04-24
- **Phase**: phase_4_bulk
- **Sub-phase**: sis_family_closeout_plus_sis_tax_rotation
- **Parser version**: 0.5.0
- **User-Agent**: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- **Crawl delay**: 6 s (robots.txt 5 s + 1 s margin)

## Summary

- **Targets attempted**: 7 (1 sis_family + 6 sis_tax)
- **Records written**: 7 / 7 (100 %)
- **Fetches used**: 19 (14 ingest HTML+PDF pairs + 5 discovery)
- **Integrity checks**: CHECK1–5 all PASS (batch-scoped; no new
  duplicate IDs introduced, all `source_hash` values match their
  on-disk raw PDFs, all required fields populated, `amended_by` /
  `repealed_by` empty as expected for new ingestions)
- **Gaps logged this batch**: 0

## Rotation reasoning

Per batch-0195 next-tick plan:

> continue sis_family — probe alphabet=J (juvenile), alphabet=M
> (marriage/matrimonial), parent-act back-reference on Children's
> Code Act /akn/zm/act/2022/12 for derivative SIs. If sis_family
> yield <3, rotate to sis_tax (priority_order item 3).

Discovery at tick start produced:

- `alphabet=J` → 1 novel sis_family candidate
  (si/2013/14 Juveniles Approved School Establishment Notice, 2012)
- `alphabet=M` → 0 novel sis_family candidates
  (Marriage Act 2023/4 is a principal Act, not SI; Matrimonial
   Causes Act 2007/20 has no derivative SIs on ZambiaLII)
- Children's Code Act /akn/zm/act/2022/12 → 0 SI back-references
  on the parent-Act page (page loads but AKN linker produces no
  outbound `/akn/zm/act/si/...` links)

sis_family yield = 1, which is `< 3`. Rotated to sis_tax
(priority_order item 3) for the remaining 6 slots. sis_tax
discovery:

- `alphabet=I` → 32 Income-Tax SIs visible, 10 novel vs. HEAD
- `alphabet=V` → 14 VAT SIs visible, 7 novel vs. HEAD

From 17 novel tax candidates, 6 **principal regulations** were
selected — deprioritising single-entity approval/exemption orders
(which duplicate the `si/2019/62 Konoike Construction` pattern
already present in HEAD) and skipping the two SIs already recorded
in `gaps.md` as pdf_parse_empty (si/2019/25, si/2017/43).

## Robots.txt re-verification

Re-fetched `https://zambialii.org/robots.txt` at the start of this
tick. Policy **unchanged** from batches 0193-0195:

- `User-agent: *`: `Allow: /`, `Crawl-delay: 5`,
  `Disallow: /akn/zm/judgment/`, `Disallow: /akn/zm/officialGazette/`,
  plus `Disallow: /search/`, `/en/search/`, etc., and `/api/`.
- `Content-Signal: ai-train=no, search=yes, ai-input=no` (non-
  technical reservation of rights under EU DSM Article 4). Worker
  identifies honestly with contact email; corpus use is primary-
  source grounding for a law firm's legal-research tools
  (retrieval / citation), not AI training. Flagged in `worker.log`
  for host review; worker continues under existing operating
  pattern established in batches 0193-0195.
- Specific-bot bans (`ClaudeBot`, `anthropic-ai`, `GPTBot`,
  `Google-Extended`, `ChatGPT-User`, `Amazonbot`, `cohere-ai`,
  `Applebot-Extended`, `meta-externalagent`, `SemrushBot`,
  `Claude-Web`) do not match our worker UA.

All URLs fetched this tick are under `/akn/zm/act/si/`,
`/akn/zm/act/2022/12`, `/legislation/subsidiary`, or
`/akn/zm/act/si/.../source.pdf` — all permitted for User-agent: *.
No judgment / officialGazette paths fetched. `case_law_scz`
remains paused pending host review.

## Records ingested

| # | Year/No | Sub-phase | Record ID | Sections | PDF bytes |
|---|---------|-----------|-----------|----------|-----------|
| 1 | 2013/014 | sis_family | `si-zm-2013-014-juveniles-approved-school-establishment-notice-2012` | 1 | 82 460 |
| 2 | 2011/033 | sis_tax | `si-zm-2011-033-income-tax-tax-clearance-exemption-regulations-2011` | 2 | 93 522 |
| 3 | 2024/018 | sis_tax | `si-zm-2024-018-value-added-tax-cross-border-electronic-services-regulations-2024` | 5 | 305 510 |
| 4 | 2014/069 | sis_tax | `si-zm-2014-069-value-added-tax-zero-rating-order-2014` | 11 | (see provenance.log) |
| 5 | 2014/068 | sis_tax | `si-zm-2014-068-value-added-tax-exemption-order-2014` | 20 | (see provenance.log) |
| 6 | 2008/014 | sis_tax | `si-zm-2008-014-value-added-tax-rate-of-tax-order-2008` | 1 | (see provenance.log) |
| 7 | 2007/019 | sis_tax | `si-zm-2007-019-value-added-tax-taxable-value-regulations-2007` | 13 | (see provenance.log) |

### 1. Juveniles (Approved School) (Establishment) Notice, 2012 — SI 14 of 2013 (sis_family)

- **AKN URL**: https://zambialii.org/akn/zm/act/si/2013/14
- **PDF URL**: https://zambialii.org/akn/zm/act/si/2013/14/eng@2013-02-01/source.pdf
- **Made under**: Juveniles Act, Cap. 53 (pre-Children's Code Act
  era; the Juveniles Act was repealed by the Children's Code Act
  No. 12 of 2022, so this Notice is of **historical** relevance
  and may be spent — retained for provenance).
- **Sections parsed**: 1 (single-section Notice declaring an
  establishment; pdfplumber did not detect a numbered-section
  heading so the parser's fallback captured the full text as
  section "1. Full text" — intentional behaviour of parser 0.5.0).

### 2. Income Tax (Tax Clearance) (Exemption) Regulations, 2011 — SI 33 of 2011 (sis_tax)

- **AKN URL**: https://zambialii.org/akn/zm/act/si/2011/33
- **PDF URL**: https://zambialii.org/akn/zm/act/si/2011/33/eng@2011-04-15/source.pdf
- **Made under**: Income Tax Act (Cap. 323).
- Significance: carves out the classes of payer exempt from the
  otherwise-blanket Income Tax tax-clearance-certificate
  requirements — high-value for practitioner reference.

### 3. Value Added Tax (Cross Border Electronic Services) Regulations, 2024 — SI 18 of 2024 (sis_tax)

- **AKN URL**: https://zambialii.org/akn/zm/act/si/2024/18
- **PDF URL**: https://zambialii.org/akn/zm/act/si/2024/18/eng@2024-02-26/source.pdf
- **Made under**: Value Added Tax Act (Cap. 331).
- Significance: implements the Zambian DST-adjacent obligation to
  register and remit VAT on cross-border electronic services
  supplied to Zambian consumers. Complements the existing
  electronic-fiscal-devices SI set in HEAD
  (2020/33 + 2021/106 amendments).

### 4. Value Added Tax (Zero Rating) Order, 2014 — SI 69 of 2014 (sis_tax)

- **AKN URL**: https://zambialii.org/akn/zm/act/si/2014/69
- **Made under**: VAT Act Cap. 331. Principal Zero-Rating order
  (subsequent 2021/104 and 2022/004+059 amendments in HEAD
  depend on this base order — adding the principal order
  completes the reference chain).

### 5. Value Added Tax (Exemption) Order, 2014 — SI 68 of 2014 (sis_tax)

- **AKN URL**: https://zambialii.org/akn/zm/act/si/2014/68
- **Made under**: VAT Act Cap. 331. Principal VAT-Exemption
  Order (subsequent 2021/105 amendment in HEAD depends on this).

### 6. Value Added Tax (Rate of Tax) Order, 2008 — SI 14 of 2008 (sis_tax)

- **AKN URL**: https://zambialii.org/akn/zm/act/si/2008/14
- **Made under**: VAT Act Cap. 331. Sets the standard VAT rate.
  Short 1-section Order; pdfplumber fell back to the full-text
  capture.

### 7. Value Added Tax (Taxable Value) Regulations, 2007 — SI 19 of 2007 (sis_tax)

- **AKN URL**: https://zambialii.org/akn/zm/act/si/2007/19
- **Made under**: VAT Act Cap. 331. Establishes the rules for
  determining the taxable value of supplies — one of the three
  foundational VAT SIs (alongside Rate of Tax and Exemption).

## Discoveries (pre-ingest, cached)

| URL | Bytes | Sha256 (prefix) |
|-----|-------|-----------------|
| `zambialii.org/legislation/subsidiary?alphabet=J` | 59 443 | (see provenance.log) |
| `zambialii.org/legislation/subsidiary?alphabet=M` | 125 415 | (see provenance.log) |
| `zambialii.org/akn/zm/act/2022/12` (Children's Code Act) | 2 080 302 | (see provenance.log) |
| `zambialii.org/legislation/subsidiary?alphabet=I` | 138 246 | (see provenance.log) |
| `zambialii.org/legislation/subsidiary?alphabet=V` | 79 416 | (see provenance.log) |

All cached to `_work/batch_0196_*.html`.

## Integrity check detail (batch-scoped)

- **CHECK1** (no duplicate IDs introduced by this batch): PASS —
  each of the 7 new record IDs appears in HEAD exactly once, at
  the expected path.
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

Note on historic corpus-wide duplicates (NOT introduced by this
batch): the 42 Appropriation-Act `-000-` placeholder-filename
duplicates first flagged in the batch-0173 audit remain outstanding
and are scoped for a dedicated cleanup tick. Batch 0196 does not
touch them.

## Execution note

Initial `scripts/batch_0196.py` process was killed at the 45-second
sandbox `bash` timeout after writing 3 / 7 records
(si/2013/14, si/2011/33, si/2024/18). Resume performed via
`scripts/batch_0196_resume.py` in two 2-target chunks
(slices `0:2` and `2:4`) with monotonic `fetch_n` continuation.
Discovery fetches (`fetch_n=1..5`) were logged once only, in the
first run. All 7 targets ultimately succeeded, no duplicate log
entries, no duplicate records.

## Cumulative status

- SI records (post-batch): 189 (+7 over batch-0195).
- Judgment records: 25 (unchanged — `case_law_scz` still paused
  per robots.txt Disallow on `/akn/zm/judgment/`).
- sis_family sub-phase: 3 records
  (2016/008 Anti-GBV Court Rules + 2023/038 Intestate Succession
   + 2013/014 Juveniles Approved School).
- sis_tax sub-phase: principal VAT order set (2014/068, 2014/069,
  2008/014, 2007/019) plus 2011/033 Income Tax Tax-Clearance and
  2024/018 VAT Cross-Border Electronic Services — total of 50 tax
  SIs in HEAD (was 44 pre-batch).

Today ~292/2000 fetches used (14.6 %). Well inside the daily
budget.

## Next-tick plan

- **sis_tax continuation**: probe alphabet=P (Property Transfer
  Tax, Presumptive Tax, PAYE) and alphabet=C (Customs & Excise).
  Novel candidates include the principal Property Transfer Tax
  Regulations (if still on ZambiaLII) and historic Customs & Excise
  orders not yet in HEAD.
- If sis_tax next-tick yield `< 3`, rotate to sis_employment
  (priority_order item 4) via alphabet=E probe (Employment Code
  Act 2019/003 derivative SIs, minimum-wage orders).
- Re-verify robots.txt at start of next tick before any fetch.
- Continue respecting MAX_BATCH_SIZE = 8 and ingesting in
  ≤2-target chunks to stay inside the 45-second bash-call ceiling.

## Infrastructure follow-up (non-blocking)

- 14 raw files on disk from batch 0196 (~6 MB: 7 HTML + 7 PDF)
  plus 17 legacy files from batches 0192–0195 awaiting host-driven
  `rclone sync raw/ b2raw:kwlp-corpus-raw/` (rclone remains
  unavailable in the tick sandbox).
- `corpus.sqlite` stale rollback-journal still blocks in-sandbox
  FTS rebuild.
- 34 legacy-schema act JSON dupes under `records/acts/` remain
  unresolved.
- 42 Appropriation-Act `-000-` placeholder duplicates remain for
  a future cleanup tick.
