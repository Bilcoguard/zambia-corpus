# Batch 0209 — Phase 4 sis_tax (continuation, PTT + Income-Tax foreign-orgs sweep)

**Started:** 2026-04-25T02:33:55Z  
**Completed:** 2026-04-25T02:36:37Z  
**Phase:** phase_4_bulk  
**Sub-phase:** sis_tax (continuation from batch-0208; alphabet=P/M/I sweep — Property Transfer Tax + Income Tax)  
**Records written:** 8  
**Targets attempted:** 8  
**Fetches used this tick:** 21 (1 robots + 3 alphabet probes + 16 ingest [HTML+PDF])  
**Daily cumulative fetches:** ~128 / 2000 (6.4%)  
**Robots.txt sha256 prefix:** fce67b697ee4ef44 (unchanged from batches 0193-0208)  
**Integrity:** CHECK1-5 all PASS (batch-scoped + corpus-wide id-uniqueness)  
**Gaps logged this batch:** 0  
**B2 sync:** deferred to host (rclone unavailable in sandbox)  
**MAX_BATCH_SIZE:** 8 (cap honoured)

## Plan execution

Per batch-0208 next-tick plan, this tick was to continue sis_tax with alphabet=P (Property Transfer Tax), alphabet=M (Mineral Royalty / Mining Tax), and a deeper alphabet=I pass for the ~30 income-tax slots still queued. All three probes ran. Discovery surfaced 39 novel keyword-matching SI candidates after dedupe against the 248 already-ingested SI slots. The candidate list was curated to remove:

- 4 recurring `pdf_parse_empty` image-only PDFs deferred for OCR backfill: SI 2019/25, 2017/43, 2022/4, 2022/13.
- 5 false positives caught by the broad `exemption`/`remission` keyword: SI 2017/55 (Preservation of Public Security Regulations — parent statute is PSA, not a tax act), SI 1994/6 + 1993/40 + 1993/41 (3 Privatisation SIs — parent is Privatisation Act), SI 1991/30 (Medical Aid Societies — parent is Medical Aid Societies Act).

That yielded 32 cleaned candidates. The first 8 were chosen with a deliberate decade-spread: 3 Property Transfer Tax exemption orders (2012/16, 1997/50, 1985/28) + 4 Income Tax foreign-orgs / body-corporate orders (1993/11, 1993/12, 1987/9, 1983/6) + 1 Preservation of Public Security (Income Tax Act) (Suspension) Regulations 1991/42 (which invokes the Income Tax Act through PSA emergency mechanism, so retained for sis_tax).

## Records added (8, all sis_tax)

| # | SI ID | Year/No | Title | Sections | PDF bytes | Parent Act |
|---|-------|---------|-------|----------|-----------|------------|
| 1 | si-zm-2012-016-property-transfer-exemption-order-2012 | 2012/16 | Property Transfer (Exemption) Order, 2012 | 4 | 152,634 | Property Transfer Tax Act, Cap. 340 |
| 2 | si-zm-1997-050-property-transfer-tax-exemption-order-1997 | 1997/50 | Property Transfer Tax (Exemption) Order, 1997 | 1 | 117,466 | Property Transfer Tax Act, Cap. 340 |
| 3 | si-zm-1985-028-property-transfer-tax-exemption-order-1985 | 1985/28 | Property Transfer Tax (Exemption) Order, 1985 | 2 | 161,952 | Property Transfer Tax Act, Cap. 340 |
| 4 | si-zm-1993-011-income-tax-body-corporate-approval-and-exemption-order-1993 | 1993/11 | Income Tax (Body Corporate) (Approval and Exemption) Order, 1993 | 2 | 98,469 | Income Tax Act, Cap. 323 |
| 5 | si-zm-1993-012-income-tax-foreign-organisations-approval-and-exemption-no-2-order-1993 | 1993/12 | Income Tax (Foreign Organisations) (Approval and Exemption) (No. 2) Order, 1993 | 2 | 152,533 | Income Tax Act, Cap. 323 |
| 6 | si-zm-1991-042-preservation-of-public-security-income-tax-act-suspension-regulations-1991 | 1991/42 | Preservation of Public Security (Income Tax Act) (Suspension) Regulations, 1991 | 2 | 156,398 | Preservation of Public Security Act, Cap. 112 (suspending Income Tax Act, Cap. 323) |
| 7 | si-zm-1987-009-income-tax-foreign-organisations-exemption-approval-order-1987 | 1987/9 | Income Tax (Foreign Organisations) (Exemption Approval) Order, 1987 | 5 | 329,464 | Income Tax Act, Cap. 323 |
| 8 | si-zm-1983-006-income-tax-intersomer-spa-exemption-order-1983 | 1983/6 | Income Tax (Intersomer S.P.A.) (Exemption) Order, 1983 | 2 | 109,532 | Income Tax Act, Cap. 323 |

## Gaps recorded

None this batch. The 4 recurring `pdf_parse_empty` slots were deliberately filtered out at discovery curation (not re-attempted) — they remain logged in gaps.md and `existing_acts.txt` from prior batches, awaiting an OCR-capable parser pass.

## Discovery snapshot

- alphabet=P → 33 unique SI candidates
- alphabet=M → 24 unique SI candidates
- alphabet=I → 98 unique SI candidates
- Novel pre-keyword-filter: 39
- Kept post-keyword-filter: 39 (then curated to 32 after FP removal; first 8 ingested)

## Integrity checks (CHECK1-5)

- CHECK1 (no duplicate IDs in `records/sis/`): PASS
- CHECK2 (every `source_hash` matches the on-disk raw PDF byte-for-byte): PASS
- CHECK3 (all required record fields present and non-empty): PASS
- CHECK4 (no unexpected `amended_by` / `repealed_by` cross-refs in fresh batch): PASS
- CHECK5 (every record has at least 1 parsed section): PASS

## Next tick plan

Yield = 8/8 (full batch ok, ≥3) so next tick continues sis_tax by default. Plan:

- Continue alphabet=I sweep (still ~24 income-tax foreign-orgs/exemption SIs queued — the long 1985-1986 series + 1982 + 1984 + 1986 + later 1990s).
- Add alphabet=C (Customs and Excise) probe with stricter keyword filter (avoid Control of Goods false positives explicitly excluded in 0208).
- Add alphabet=W (Withholding Tax / Workers' Comp tax interface) probe.
- Parent-Act-driven probes: Customs and Excise Act Cap. 322 (deeper dive), Property Transfer Tax Act Cap. 340 (post-2012), Mines and Minerals Development Act 2015/11 royalty SIs.
- Fallback if sis_tax yield <3: rotate to sis_corporate (priority_order item 2) — Companies Act 2017/10 derivatives, BFSA 2017/7, Movable Property Security Interest Act, Insolvency Act 2017/9.
- Re-verify robots.txt at start of next tick.

## Infrastructure notes (non-blocking)

- 16 batch-0209 raw SI files on disk (8 HTML + 8 PDF, ~1 MB) plus accumulated batches 0192-0208 raw files awaiting host-driven B2 sync (rclone unavailable in sandbox).
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild (disk I/O error on read).
- Persistent virtiofs unlink-failure warnings (workaround stable across batches 0192-0209 — rename `.git/index.lock` and `.git/refs/remotes/origin/main.lock.*` to `.dN_PID` siblings, write valid sha into stale-ref files when git refuses to ignore them).
- 34 legacy-schema act JSON dupes + 42 Appropriation-Act `-000-` placeholder dupes + 63 SI flat-layout dupes remain unresolved (pre-existing).
