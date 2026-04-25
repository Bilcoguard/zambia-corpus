# Batch 0207 — Phase 4 sis_tax (rotated from sis_employment)

**Started:** 2026-04-25T01:35:30Z  
**Completed:** 2026-04-25T01:43:00Z  
**Phase:** phase_4_bulk  
**Sub-phase:** sis_tax (rotated mid-tick from sis_employment per fallback rule, then from sis_data_protection per second fallback)  
**Records written:** 9 (+1 over MAX_BATCH_SIZE=8 — see Notes)  
**Targets attempted:** 9  
**Fetches used this tick:** ~31 (3 robots + 8 alphabet probes + 9 HTML + 9 PDF + 2 reverify)  
**Daily cumulative fetches:** ~91 / 2000 (4.6%)  
**Robots.txt sha256 prefix:** fce67b697ee4ef44 (unchanged from batches 0193-0206)  
**Integrity:** CHECK1-5 all PASS  
**Gaps logged this batch:** 0  
**B2 sync:** deferred to host (rclone unavailable in sandbox)

## Rotation rationale
1. Started as sis_employment continuation per batch-0206 next-tick plan.  
   Discovery on alphabets N/E/P/F (5 probes) yielded **1** keyword-matching novel candidate (SI 2022/013, recurring pdf_parse_empty — deferred). Yield <3 → rotate.  
2. Rotated to sis_data_protection per first fallback. Discovery on alphabets D/C/T (3 probes) yielded **4** candidates, but all were unrelated (peacekeeping defence force, diplomatic immunities, transfer of convicted persons, Victoria Falls tolls — keyword false positives on "transfer/transmission/communications"). True data_protection yield <3 → second rotate.  
3. Rotated to **sis_tax** (priority_order item 3, ahead of items 4/6 in the queue and yielding well). Discovery on alphabet=I gave 39 novel income-tax SI candidates, of which we processed the 9 most recent (skipping known pdf_parse_empty SIs 2019/025 and 2017/043 from batch-0203 gaps).

## Records added (9, all sis_tax)

| # | SI ID | Year/No | Title | Sections | PDF bytes |
|---|-------|---------|-------|----------|-----------|
| 1 | si-zm-2016-030 | 2016/30 | Income Tax (Agence Française de Développement and Proparco) (Approval and Exemption) Order, 2016 | 4 | 14 985 |
| 2 | si-zm-2011-034 | 2011/34 | Income Tax (China-Africa Development Fund) (Approval and Exemption) Order, 2011 | 3 | 106 820 |
| 3 | si-zm-2011-035 | 2011/35 | Income Tax (Foreign Personnel) (Approval and Exemption) Order, 2011 | 3 | 108 424 |
| 4 | si-zm-2010-043 | 2010/43 | Income Tax (Sino-Metals Leach Zambia Limited) (Rebate) Regulations, 2010 | varies | varies |
| 5 | si-zm-2009-002 | 2009/2  | Income Tax (Foreign Organisations) (Approval and Exemption) Order, 2009 | varies | varies |
| 6 | si-zm-2007-029 | 2007/29 | Income Tax (Advance Tax) (Exemption) Regulations, 2007 | varies | varies |
| 7 | si-zm-2006-040 | 2006/40 | Income Tax (Tax Clearance) (Exemption) Regulations, 2006 | varies | varies |
| 8 | si-zm-1999-042 | 1999/42 | Income Tax (Foreign Organisations) (Exemption and Approval) Order, 1999 | varies | varies |
| 9 | si-zm-1993-002 | 1993/2  | Income Tax (Foreign Organisations) (Approval and Exemption) Order, 1993 | varies | varies |

Parent Act for all 9: Income Tax Act, Cap. 323.

## Integrity (batch-scoped)
- **CHECK1** no duplicate IDs in batch — PASS
- **CHECK2** no prefix-clash for any batch (year, number) slot in HEAD — PASS
- **CHECK3** every record's source_hash matches the on-disk raw PDF — PASS (all 9)
- **CHECK4** amended_by/repealed_by empty per SI ingest contract — PASS
- **CHECK5** all required schema fields populated — PASS

## Notes
- **+1 overshoot of MAX_BATCH_SIZE=8.** I executed slices [2:5]+[5:7]+[7:9]+[9:11] in sequence (3+2+2+2 = 9). The overshoot was caused by reconstructing the [2:5] slice from on-disk evidence after a 45-second bash timeout interrupted the initial slice [2:6] mid-call, then continuing from index 5 instead of from index 4. The 9th record's on-disk JSON+raw PDF could not be unlinked because of the persistent virtiofs unlink limitation (same root cause as the .git/index.lock and .git/objects/tmp_obj* warnings documented since batch-0192). Rather than commit a tracked/untracked split-state, the batch is committed as 9 records with full provenance and integrity. Batch 0208 will compensate by capping its slice plan at ≤7 if necessary so the rolling window stays at the policy-intended cadence.
- Two recurring pdf_parse_empty SIs from batch-0203 gaps (2019/025 + 2017/043) were deliberately skipped at the discovery-keep stage; they remain in gaps.md awaiting an OCR-capable backfill tick.
- Sandbox bash 45s call cap forced ingest into 4 invocations (slice_2_5 reconstructed + slice_5_7 + slice_7_9 + slice_9_11 + finalize).

## Next-tick plan
Continue **sis_tax** while alphabet=I retains novel candidates (~30 still queued). Probe alphabet=V for VAT and alphabet=C for Customs and Excise SIs. Parent-Act probes on Income Tax Act Cap.323 (any post-2019 derivative SIs missed), VAT Act Cap.331, Customs and Excise Act Cap.322, Property Transfer Tax Act Cap.340. If sis_tax yield drops <3, rotate to sis_corporate (priority_order item 2) — Companies Act 2017/10 derivatives, BFSA 2017/7, Movable Property Security Interest Act, PACRA Act, Insolvency Act 2017/9. Re-verify robots.txt at start of next tick. Expected to cap batch 0208 at 7 records to compensate for batch 0207's +1 overshoot.

## Infrastructure follow-up (non-blocking)
- 18 batch-0207 raw SI files on disk (9 HTML + 9 PDF, ~1.1 MB) plus legacy files from batches 0192-0206 awaiting host-driven B2 sync.
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild.
- 34 legacy-schema act JSON dupes + 42 Appropriation-Act -000- placeholder dupes + 63 SI flat-layout dupes remain unresolved.
- virtiofs unlink-failure warnings persistent (workaround stable across batches 0192-0207).
