# Batch 0208 — Phase 4 sis_tax (continuation, VAT focus)

**Started:** 2026-04-25T01:48:00Z  
**Completed:** 2026-04-25T02:01:30Z  
**Phase:** phase_4_bulk  
**Sub-phase:** sis_tax (continuation from batch-0207; VAT-focused via alphabet=V)  
**Records written:** 5  
**Targets attempted:** 6  
**Fetches used this tick:** 16 (1 robots + 2 alphabet probes + 6 HTML + 7 PDF)*  
**Daily cumulative fetches:** ~107 / 2000 (5.4%)  
**Robots.txt sha256 prefix:** fce67b697ee4ef44 (unchanged from batches 0193-0207)  
**Integrity:** CHECK1-5 all PASS  
**Gaps logged this batch:** 1 (SI 2022/4 pdf_parse_empty)  
**B2 sync:** deferred to host (rclone unavailable in sandbox)  
**MAX_BATCH_SIZE:** 7 (capped per batch-0207 next-tick plan to compensate for prior +1 overshoot)

\* The 6 HTML / 7 PDF asymmetry: SI 2022/4 returned an HTML page that pointed
to a `source.pdf` URL but the PDF parsed empty (no extractable text via
pdfplumber). Both fetches are accounted for; no on-disk artefacts kept for
the failing slot per the gap-record contract.

## Plan execution

Per batch-0207 next-tick plan, this tick was to "Probe alphabet=V for VAT
and alphabet=C for Customs and Excise SIs." Both probes ran. After
filtering against the 243 already-ingested SI slots and applying the
sis_tax keyword filter (income tax / VAT / customs / excise / property
transfer tax / taxation / duty / remission / rebate / exemption / double
taxation), 16 candidate slots emerged. Two false-positive groups were
removed at review:

1. **Citizens Economic Empowerment (Reservation Scheme) Regulations, 2017
   (SI 2017/1)** — keyword match was on "Reservation Scheme" + the policy
   exemption mechanic; parent statute is the Citizens Economic Empowerment
   Act, not a tax statute. Not sis_tax.
2. **Control of Goods (Import Licence Fees) (Exemption) Notices** (1986/10,
   1988/2, 1989/17, 1989/33, 1990/9, 1990/18, 1991/21, 1991/37, 1991/49 —
   9 instruments) — keyword match was on "Import Licence Fees" + "Exemption";
   parent statute is the Control of Goods Act (trade restriction), not the
   Customs and Excise Act. Not sis_tax. They are legitimate sis_corporate /
   sis_trade candidates and will be picked up in a later rotation if a
   sis_trade sub-phase is approved.

That left 6 genuine VAT candidates, all chosen for ingest in this tick.

## Records added (5, all sis_tax / VAT)

| # | SI ID | Year/No | Title | Sections | PDF bytes |
|---|-------|---------|-------|----------|-----------|
| 1 | si-zm-2022-059-value-added-tax-zero-rating-amendment-no-2-order-2022 | 2022/59 | Value Added Tax (Zero Rating) (Amendment) (No. 2) Order, 2022 | 2 | 284 461 |
| 2 | si-zm-2011-049-value-added-tax-exemption-order-2011 | 2011/49 | Value Added Tax (Exemption) Order, 2011 | 3 | 329 676 |
| 3 | si-zm-2004-012-value-added-tax-application-for-registration-order-2004 | 2004/12 | Value Added Tax (Application for Registration) Order, 2004 | 2 | 204 039 |
| 4 | si-zm-1997-011-value-added-tax-rate-of-tax-order-1997 | 1997/11 | Value Added Tax (Rate of Tax) Order, 1997 | 1 | 100 491 |
| 5 | si-zm-1996-023-value-added-tax-supply-regulations-1996 | 1996/23 | Value Added Tax (Supply) Regulations, 1996 | 3 | 142 754 |

Parent Act for all 5: Value Added Tax Act, Cap. 331.

## Gaps recorded

| SI | Status | URL | Note |
|-----|--------|-----|------|
| 2022/4 — Value Added Tax (Zero-Rating) (Amendment) Order, 2022 | pdf_parse_empty | https://zambialii.org/akn/zm/act/si/2022/4 | PDF contains no extractable text via pdfplumber (likely image-only / scanned). Joins the recurring pdf_parse_empty queue (2017/43, 2019/25, 2022/2, 2022/13). Awaits an OCR-capable backfill tick. |

## Integrity (batch-scoped)
- **CHECK1** no duplicate IDs in batch — PASS
- **CHECK2** no prefix-clash for any (year, number) slot in HEAD — PASS
- **CHECK3** every record's source_hash matches the on-disk raw PDF — PASS (all 5)
- **CHECK4** amended_by/repealed_by empty per SI ingest contract — PASS
- **CHECK5** all required schema fields populated — PASS

## Notes
- Discovery probes (robots.txt + alphabet=V + alphabet=C) were executed
  inline in the tick and logged to costs.log fetches 1-3 of batch 0208.
  The discovery-state file (`_work/batch_0208_discovery.json`) was then
  seeded with the post-filter candidate list; the script's own
  `discovery` subcommand was not re-invoked because the data was already
  on disk. This avoids 3 redundant network fetches and respects the
  "minimum bounded unit of work" principle.
- Batch capped at 7 per batch-0207 next-tick plan; only 6 candidates
  were available after sis_tax keyword filtering, so the natural cap was
  6 not 7. 5 ingested cleanly + 1 gap = 6.
- corpus.sqlite remains in stale rollback-journal state (`disk I/O error`
  on read, mtime 2026-04-24T23:38). Not touched this tick. Same workaround
  as batches 0192-0207 (record JSON + raw bytes are the source of truth;
  sqlite rebuild is a host-driven follow-up).

## Next-tick plan
- Continue sis_tax. Probe alphabet=P for **Property Transfer Tax** SIs and
  alphabet=M for **Mineral Royalty / Mining Tax** SIs (any pre-2020 issues
  not yet picked up). Re-probe alphabet=I for any post-2025-Q1 income-tax
  SIs that may have appeared since batch-0207 (39 novel I-list candidates
  remained queued after 0207 took the top 9; 30 still queued).
- Parent-Act probes for: VAT Act Cap. 331 (post-2022), Property Transfer
  Tax Act Cap. 340, Mines and Minerals Development Act 2015/11 royalty
  derivatives, Customs and Excise Act Cap. 322 (deeper alphabet=C dive
  past Control-of-Goods false positives).
- If sis_tax yield drops <3 across two consecutive ticks, rotate to
  sis_corporate (priority_order item 2): Companies Act 2017/10
  derivatives, BFSA 2017/7, Movable Property Security Interest Act,
  PACRA Act, Insolvency Act 2017/9.
- Re-verify robots.txt at start of next tick.
- Expected next-tick batch size: up to 8 (no further compensation needed —
  this batch ingested 5, well under the 7 cap).

## Infrastructure follow-up (non-blocking, carried from prior batches)
- 11 batch-0208 raw SI files on disk (5 HTML + 5 PDF + 1 alphabet
  discovery snapshot, ~1.3 MB) plus accumulated batches 0192-0207 raw
  files awaiting host-driven B2 sync.
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild.
- 34 legacy-schema act JSON dupes + 42 Appropriation-Act -000- placeholder
  dupes + 63 SI flat-layout dupes remain unresolved (from earlier audits).
- Persistent virtiofs unlink-failure warnings (workaround stable across
  batches 0192-0208).

## Phase 4 status
Phase 4 (bulk ingestion) remains **approved: true, complete: false**. Per
non-negotiable #4, this worker MUST NOT flip `complete: true` —
priority-order queues still have unprocessed candidates in sis_tax,
sis_corporate, sis_employment, case_law_scz, sis_data_protection,
sis_mining, sis_family. Awaiting human confirmation before any closure.
