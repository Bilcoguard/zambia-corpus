# Batch 0210 — Phase 4 sis_tax (continuation, Income-Tax foreign-orgs 1985-1986 sweep)

**Started:** 2026-04-25T03:02:29Z  
**Completed:** 2026-04-25T03:06:19Z  
**Phase:** phase_4_bulk  
**Sub-phase:** sis_tax (continuation from batch-0209; alphabet=I/C/W sweep — Income Tax foreign-orgs + Customs + Withholding)  
**Records written:** 8  
**Targets attempted:** 8  
**Fetches used this tick:** 20 (4 discovery [1 robots + 3 alphabet probes] + 16 ingest [8 HTML + 8 PDF])  
**Daily cumulative fetches:** ~142 / 2000 (7.1%)  
**Robots.txt sha256 prefix:** fce67b697ee4ef44 (unchanged from batches 0193-0209)  
**Integrity:** CHECK1-5 all PASS  
**Gaps logged this batch:** 0  
**B2 sync:** deferred to host (rclone unavailable in sandbox)  
**MAX_BATCH_SIZE:** 8 (cap honoured)

## Plan execution

Per batch-0209 next-tick plan, this tick continued sis_tax with alphabet=I (deeper sweep of the 1982-1986 Income Tax Foreign Organisations series still queued), alphabet=C (Customs and Excise with stricter filter to avoid Control of Goods false positives), and alphabet=W (Withholding Tax / Workers' Comp).

All three probes ran. Discovery surfaced 36 novel keyword-matching SI candidates after dedupe against the 259 already-ingested SI slots. Manual curation removed:

- 2 recurring `pdf_parse_empty` image-only PDFs deferred for OCR backfill: SI 2019/25, 2017/43.
- 1 false positive caught by the broad keyword filter: SI 2017/1 (Citizens Economic Empowerment Reservation Scheme — parent statute is Citizens Economic Empowerment Act, not a tax act).
- 9 Control of Goods (Import Licence Fees) (Exemption) Notices (SI 1991/21, 1991/37, 1991/49, 1990/9, 1990/18, 1989/17, 1989/33, 1988/2, 1986/10) — flagged as out-of-scope false positives by the batch-0209 report. Parent is the Control of Goods Act, Cap. 421; not a tax statute. Deferred for a future dedicated Control of Goods probe if sis_tax is redefined to include import-duty adjuncts.

That yielded 24 cleaned candidates. The first 8 were chosen as a contiguous Income Tax (Foreign Organisations) (Exemption Approval) series (1986/4, 1986/27, 1985/16-21) — all parented on the Income Tax Act, Cap. 323, and matching the sis_tax scope squarely.

## Records added (8, all sis_tax)

| Year/No | Title | Sections | PDF bytes |
|---------|-------|----------|-----------|
| 1986/004 | Income Tax (Foreign Organisations) (Exemption Approval) Order, 1986 | 5 | 258,374 |
| 1986/027 | Income Tax (Foreign Organisations) (Exemption Approval) (No. 2) Order, 1986 | 2 | 240,608 |
| 1985/016 | Income Tax (Foreign Organisations) (Exemption Approval) Order, 1985 | 3 | 140,666 |
| 1985/017 | Income Tax (Foreign Organisations) (Exemption Approval) (No. 2) Order, 1985 | 3 | 129,141 |
| 1985/018 | Income Tax (Foreign Organisations) (Exemption Approval) (No. 3) Order, 1985 | 2 | 116,279 |
| 1985/019 | Income Tax (Foreign Organisations) (Exemption Approval) (No. 4) Order, 1985 | 3 | 123,808 |
| 1985/020 | Income Tax (Foreign Organisations) (Exemption Approval) (No. 5) Order, 1985 | 3 | 107,697 |
| 1985/021 | Income Tax (Foreign Organisations) (Exemption Approval) (No. 6) Order, 1985 | 3 | 147,586 |

All 8 are SIs under the **Income Tax Act, Cap. 323** (pre-1995 Act; continued in force under the Income Tax Act, Cap. 323 of the 1995 revised edition).

## Gaps recorded

None this batch. The 2 `pdf_parse_empty` slots (2019/25, 2017/43) and 1 FP slot (2017/1) and 9 Control-of-Goods FP slots were filtered out at discovery curation (not re-attempted) — they remain logged in gaps.md and prior batch reports.

## Discovery snapshot

- alphabet=I → 98 unique SI candidates
- alphabet=C → 245 unique SI candidates
- alphabet=W → 9 unique SI candidates
- Novel pre-keyword-filter: 180
- Kept post-keyword-filter: 36 (then curated to 24 after FP/OCR removal; first 8 ingested)

## Integrity checks (CHECK1-5)

- CHECK1 (no duplicate IDs in `records/sis/`): PASS
- CHECK2 (every `source_hash` matches the on-disk raw PDF byte-for-byte): PASS
- CHECK3 (all required record fields present and non-empty): PASS
- CHECK4 (no unexpected `amended_by` / `repealed_by` cross-refs in fresh batch): PASS
- CHECK5 (every record has at least 1 parsed section): PASS

## Execution notes (non-blocking)

The first ingest sub-call (slice 36-39, targets 1986/4 + 1986/27 + 1985/16) hit the sandbox's 45 s per-command timeout just after its third record was written. Because the ingest pipeline writes records, raw files, costs.log, and provenance.log inline as each target completes, all three records persisted correctly — only the summary slice-file `_work/batch_0210_slice_36_39.json` was missing. That slice file was reconstructed post-hoc from the on-disk records and raw files (the reconstruction is annotated with a `note` field inside the JSON). The remaining 5 records were ingested in two follow-up slice calls (39-42 and 42-44) which completed normally.

## Next tick plan

Yield = 8/8 (full batch ok, ≥3) so next tick continues sis_tax by default. Plan:

- Continue alphabet=I sweep (still ~14 income-tax foreign-orgs exemption SIs queued — 1984/45, 1983/43, 1982/2, 1982/9, 1982/36, 1981/48, plus the pre-1985 tail and the 1985/26, 1985/27, 1985/49, 1985/50 and later 1990s).
- Add alphabet=V (VAT) probe (first time; VAT Act 1995/4 derivatives).
- Add alphabet=T (Tourism Levy, Tax Appeals Tribunal, Tobacco) probe.
- Parent-Act-driven probes: VAT Act Cap. 331 (deeper dive), Mines and Minerals Development Act 2015/11 royalty SIs, Customs and Excise Act Cap. 322 exemption/remission notices.
- Fallback if sis_tax yield <3: rotate to sis_corporate (priority_order item 2) — Companies Act 2017/10 derivatives, BFSA 2017/7, Movable Property Security Interest Act, Insolvency Act 2017/9.
- Re-verify robots.txt at start of next tick.

## Infrastructure notes (non-blocking)

- 16 batch-0210 raw SI files on disk (8 HTML + 8 PDF, ~1.4 MB) plus accumulated batches 0192-0209 raw files awaiting host-driven B2 sync (rclone unavailable in sandbox).
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild (disk I/O error on read).
- Persistent virtiofs unlink-failure warnings (workaround stable across batches 0192-0210 — `.git/objects/maintenance.lock` warning appears on git pull but does not block the pull).
- 34 legacy-schema act JSON dupes + 42 Appropriation-Act `-000-` placeholder dupes + 63 SI flat-layout dupes remain unresolved (pre-existing).
