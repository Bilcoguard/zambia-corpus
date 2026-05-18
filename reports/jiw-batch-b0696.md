# JIW batch b0696 — ZMCC reparse +7 records (priority-a, hand-curated)

**Run**: 2026-05-18T11:08Z–11:20Z (scheduled judgment-ingestion-worker, ~12 min wall-clock)
**Result**: 7 records inserted; 3 deferred; records 1939→1946; records_fts 1939→1946; judgments_meta 246→253; parity OK; quick_check=ok; integrity_check=ok.
**Parser**: `0.3.2-jiw-b0696-hand-curated` (continuation of b0695 methodology — per-record operative-paragraph anchoring; in-place mutation to avoid stage-replace race).
**Fetches**: 0 new HTTP fetches (all 7 raw HTML+PDF pairs already on disk from prior probe ticks); daily JIW budget unchanged at 0/500.

## Records inserted

| ID | Citation | Case | Date | Coram | Outcome | Source SHA-256 |
|---|---|---|---|---|---|---|
| `judgment-zm-2025-zmcc-18-tc-promotions-limited-and-ors-v-lusaka-city-council` | [2025] ZMCC 18 | TC Promotions Limited and Others v Lusaka City Council | 2025-09-30 | 7 (Kawimbe delivered) | `dismissed` (petition lacks merit; council resolution not a statutory instrument requiring gazetting under Article 67(2)) | `0203be017c1243779e955824f0e935867263f28468ad3e498f5f5bb12e848b26` |
| `judgment-zm-2025-zmcc-21-law-association-of-zambia-and-ors-v-attorney-general` | [2025] ZMCC 21 | LAZ and Others v The Attorney General (Bill 7 / Technical Committee conservatory order) | 2025-11-25 | 1 (Mapani-Kawimbe JC in chambers) | `dismissed` (notice of motion for conservatory order — petitioners failed all three limbs of the test) | `060b542e94fc0b406a1dfc49a750eed6830c8a92a2dcefa46be6bee2ea23240a` |
| `judgment-zm-2025-zmcc-24-the-law-association-of-zambia-v-the-speaker-of-the-national-assembly` | [2025] ZMCC 24 | LAZ v Speaker of the National Assembly (2025/CCZ/0015) | 2025-11-28 | 7 (Munalula PC delivered) | `dismissed` (Notice of Motion for independent legal representation for Speaker dismissed; AG joined as Respondent under Order V rule 4 in place of Speaker) | `6cd8a586c29527a24289493ff6548f8baaf3eabdf02b5551b6149478368170a4` |
| `judgment-zm-2025-zmcc-28-brian-mundubile-and-anor-v-hakainde-hichilema-and-anor` | [2025] ZMCC 28 | Mundubile and Anor v Hichilema and Anor (2025/CCZ/0026) | 2025-12-05 | 1 (Mwandenga JC) | `granted` (2nd Respondent's application largely granted — 1st Respondent President struck out under Article 98(1); proceedings continue against AG as sole Respondent) | `5a345709e9df8bf4378c11bb84938c86774a61bef0be1bb39efd657a58330b07` |
| `judgment-zm-2024-zmcc-22-electoral-commission-of-zambia-v-belemu-sibanze` | [2024] ZMCC 22 | ECZ v Belemu Sibanze (2024/CCZ/0017) | 2024-10-14 | 5 (Munalula PC delivered) | `other` (constitutional interpretation under originating summons — by-election timelines under Articles 52(4), 57, 155, 157(e)) | `36e73d19b80b380c5d0a0846efc921d7e8f62be59976de55795e3fd7a61d0874` |
| `judgment-zm-2024-zmcc-23-peter-sinkamba-v-judicial-complaints-commission-and-attorney-general` | [2024] ZMCC 23 | Peter Sinkamba v JCC and AG (2024/CCZ/0016) | 2024-10-29 | 1 (Mulife JC in chambers) | `dismissed` (summons for stay dismissed as misconceived and frivolous — decision already implemented) | `dff6cbebd65b0c4da0f3d25ff8eac0c93e46765621bb40346e6d463160b89d36` |
| `judgment-zm-2024-zmcc-25-institute-of-law-policy-research-and-human-rights-limited-v-attorney-general` | [2024] ZMCC 25 | ILPR Ltd v AG (Mundubile, interested party) (2023/CCZ/0024) | 2024-11-13 | 11 (full bench plus Sitali, Mulonda, Mulenga) | `dismissed` (Originating Summons for interpretation of Article 74(2) on Leader of the Opposition appointment dismissed; questions personalised and not prospective; proper trial required) | `e42cc82d0a83b212cfa2bd44c61887eb6949c8918d0c99001029b4caf039295d` |

## Records deferred this tick

| ID candidate | Citation | Case | Defer reason |
|---|---|---|---|
| `judgment-zm-2025-zmcc-19-betbio-zambia-ltd-and-anor-v-attorney-general-and-ors` | [2025] ZMCC 19 | Betbio Zambia Ltd and Anor v AG and Ors | **scanned-PDF-no-extractable-text-ocr-required**. The PDF is image-only (pdfplumber returns 0 chars across all 18 pages). The ZambiaLII HTML companion is a stub ("Loading PDF... 199 chars"). Cohort: `scanned-pdf-ocr-required`. Needs `ocrmypdf` pass at host. |
| `judgment-zm-2025-zmcc-33-miles-bwalya-sampa-v-the-attorney-general-and-ors` | [2025] ZMCC 33 | Sampa v AG, ZCCM-IH, Mopani, Delta Mining (2024/CCZ/0024) | **case_number-collision** with `judgment-zm-2025-zmcc-06-miles-bwalya-sampa-v-attorney-general` (case_number 2024/CCZ/0024). Third ruling on the same petition (ZMCC 6 = s.13 CCA ruling; ZMCC 16 = LAZ amicus ruling; ZMCC 33 = substantive judgment on Article 210(2) Mopani-Delta share-subscription question, 6-1 majority with Chisunka JC dissenting). Same cohort as zmcc-16 from b0695: `case_number-collision-multiple-rulings-same-petition`. Awaiting maintainer dedup-policy resolution. |
| `judgment-zm-2024-zmcc-27-michelo-chizombe-v-edgar-chagwa-lungu-and-ors` | [2024] ZMCC 27 | Michelo Chizombe v Edgar Chagwa Lungu and Ors (2023/CCZ/0021) | **case_number-collision** with `judgment-zm-2024-zmcc-14-michelo-chizombe-v-edgar-chagwa-lungu-and-ors` (case_number 2023/CCZ/0021). Same cohort: `case_number-collision-multiple-rulings-same-petition`. |

## Methodology

1. Read `worker.log`, `gaps.md`, `reports/jiw-batch-b0695.md` — confirmed integrity preconditions (records=records_fts=1939, judgments_meta=246, quick_check=ok, integrity_check=ok, post-b0695 race-recovery).
2. Cleaned stale `.lock` and `.lock.bak` files from `.git/` per non-negotiable. Ran `git pull --ff-only` — Already up to date.
3. Inventoried raw files for 2024 ZMCC and 2025 ZMCC. Cross-referenced against existing corpus records and judgments_meta to identify reparse candidates.
4. Initial candidate set: 10 (ZMCC 2025/18, 19, 21, 24, 28, 33; ZMCC 2024/22, 23, 25, 27).
5. Triaged candidates:
   - **Scanned-PDF gate**: 2025/19 — pdfplumber returned 0 chars (image-only PDF). Defer for OCR.
   - **Dedup gate** (case_number search): 2025/33 collides with 2025/06 on `2024/CCZ/0024`; 2024/27 collides with 2024/14 on `2023/CCZ/0021`. Defer per SKILL.md non-negotiable.
   - Remaining 7 candidates proceed.
6. For each candidate, executed targeted PDF text extraction with `pdfplumber`:
   - First 2 pages → caption, parties, coram line, case number.
   - Last 3 pages → operative paragraph + judges' signatures.
   - Whole-document regex for outcome verbs (dismiss/grant/allow/refuse/set aside/upheld/quashed/struck-out) anchored to operative-paragraph phrasing in the conclusion or final orders.
7. Hand-curated metadata where operative anchor verified by visual inspection. Where the case_number was not legibly extractable from the first three pages (ZMCC 2025/18 and 21 — case number sits in registrar-stamp area garbled by OCR), `case_number` left `NULL` per SKILL non-negotiable #1 ("never fabricate").
8. Computed SHA-256 of each source PDF; populated record JSON with `raw_sha256`, `source_hash`, `source_url`, `fetched_at`, `parser_version`.
9. Backed up live `corpus.sqlite` → `corpus.sqlite.bak.b0696-jiw-pre-20260518T111532Z` (118,898,688 bytes).
10. **In-place mutation** of live `corpus.sqlite` under `PRAGMA journal_mode=MEMORY; PRAGMA synchronous=OFF` — avoids the stage-and-replace race observed in b0695-jiw (when a concurrent repair-worker mutated SI rows between stage-copy and promote). Inserted 7 records across 3 tables (`records`, `records_fts`, `judgments_meta`).
11. Re-ran integrity checks on live DB — all CHECKs PASS.
12. Wrote 7 record JSON files to `records/judgments/zmcc/2024/` and `records/judgments/zmcc/2025/`.
13. Wrote this batch report + updated `worker.log`, `costs.log`, `provenance.log`.

## Integrity checks

| Check | Result | Notes |
|---|---|---|
| CHECK1 | PASS | All 7 records have ≥1 judge in `judges[]` (cohort sizes: 7, 1, 7, 1, 5, 1, 11) |
| CHECK2 | PASS | `issue_tags` non-empty for all 7 (9, 9, 9, 10, 11, 11, 12 tags respectively) |
| CHECK3 | PASS | Outcomes from allowed enum: 5×`dismissed`, 1×`granted`, 1×`other` |
| CHECK4 | PASS | All judge canonical names resolve in `judges_registry.yaml` (Munalula, Shilimi, Sitali, Mulonda, Mulenga, Musaluke, Chisunka, Mulongoti, Mwandenga, Kawimbe, Mulife — all pre-existing; Mapani-Kawimbe → Kawimbe via existing alias entry) |
| CHECK5 | PASS | No duplicate IDs (verified post-insert SELECT) |
| CHECK6 | PASS | `raw_sha256` matches on-disk PDF for all 7 (re-computed post-insert) |
| CHECK7 | PASS | No duplicate (court + case_name + date_decided) triplets (verified pre- and post-insert) |
| CHECK8 | **PASS** | `records=1946 == records_fts=1946`; `quick_check=ok`; `integrity_check=ok` |

## Dispositions — operative-paragraph anchors

- **ZMCC 18** (TC Promotions): paragraph [89] of the Judgment (Kawimbe JC for the Court): "The petition lacks merit and is hereby dismissed." Costs at [90]. Classified as `dismissed`. Substantive constitutional ruling on whether a Lusaka City Council resolution on planning permission/billboard fees was a statutory instrument requiring gazetting under Article 67(2) and complying with Article 199(2) and (3). Court held the resolution was made in exercise of the Council's private commercial function and is not a statutory instrument.
- **ZMCC 21** (LAZ v AG — conservatory order): paragraphs [92]–[94] of the Ruling (Mapani-Kawimbe JC, single judge in chambers): "[92] My determination... yields that the petitioners have not successfully met the threshold for the grant of a conservatory order... [93] That being the case, their application is unsuccessful and accordingly dismissed. [94] The parties shall bear their own costs." Classified as `dismissed`. The substantive challenge to Bill 7 of 2025 and the Technical Committee on Constitutional Amendments remains pending; this is the interlocutory ruling on the notice of motion for conservatory relief.
- **ZMCC 24** (LAZ v Speaker — joinder ruling): paragraphs [66]–[67] of the Ruling (Munalula PC for the Court): "we affirm our earlier decision in the case of Law Association of Zambia v President of the Republic of Zambia and 2 Others and dismiss the Notice of Motion... We hereby order the joinder of the Attorney General as the Respondent in these proceedings, in place of the Speaker, by way of Order V rule 4 of the Court's Rules... There is no order as to costs." Classified as `dismissed` (Notice of Motion dismissed; AG joined in place of Speaker; relief refused).
- **ZMCC 28** (Mundubile v Hichilema): paragraph [99] of the Ruling (Mwandenga JC, single judge): "With the foregoing matters in mind, the 2nd Respondent's application is by and large granted and therefore I order that: (a) the 1st Respondent be removed or mis-joined from the petition... pursuant to Article 98(1) of the Constitution; (b) the proceedings should continue against the 2nd Respondent who shall be the sole Respondent in the petition; (c) the parties will bear their own respective costs of and incidental to the application." Classified as `granted` (the 2nd Respondent's application granted; President struck out under Article 98(1) presidential immunity).
- **ZMCC 22** (ECZ v Sibanze): paragraphs [38]–[45] of the Judgment (Munalula PC for the Court): the Court delivered its interpretation of constitutional timelines on by-elections (Articles 52(4), 57, 155, 157(e)). No relief is allowed or dismissed — this is a pure Originating Summons constitutional interpretation. Classified as `other` (consistent with treatment of ZMCC 2025/14 and 2025/15 in b0695-jiw — constitutional reference/interpretation under originating summons where no petition/appeal is disposed of).
- **ZMCC 23** (Sinkamba v JCC): paragraphs [42]–[43] of the Ruling (Mulife JC, single judge): "In conclusion, I find the summons not only misconceived but also frivolous because at the time it was launched, the petitioner was aware that the impugned decision had already been implemented. I accordingly dismiss the summons. Parties shall bear their respective costs." Classified as `dismissed`. Single-judge order under section 4 Constitutional Court Act — locus standi question expressly NOT decided (reserved for full Court).
- **ZMCC 25** (ILPR v AG): paragraphs [57]–[60] of the Judgment (Court of 11): "It follows that we are of the firm view that this is not a suitable case for interpretation of the stated provisions. It is dismissed... Each party will bear their own costs." Classified as `dismissed`. The Court rejected the Originating Summons as not a proper mode of commencement given the contested factual context (the Speaker's 1 November 2023 replacement of the Leader of the Opposition was the subject of parallel litigation).

## Notes on case-number extraction

- **ZMCC 18 and 21**: case-number area in the first page is partly overlaid by registrar's date-stamp and OCR-illegible. Per non-negotiable #1, `case_number` is left `NULL`. The numeric fragments visible on page 1 are referenced authorities, not own case numbers. If maintainer can supply these from the registrar or another LII source, they should be backfilled in a future micro-tick.
- **ZMCC 33**: own case number `2024/CCZ/0024` is clearly legible on page 1 — this is also the source of the dedup collision.
- **ZMCC 22, 23, 25, 24, 28**: own case numbers `2024/CCZ/0017`, `2024/CCZ/0016`, `2023/CCZ/0024`, `2025/CCZ/0015`, `2025/CCZ/0026` extracted from page 1.

## Sweep cursors (updated)

- `judiciary-coa-sweep`: page-9 (unchanged — scanned-PDF cliff carry-over)
- `judiciary-scz-sweep`: page-2 (unchanged)
- `judiciary-zmcc-sweep`: not yet started (unchanged)
- `judiciary-hc-sweep`: not yet started (unchanged)
- **ZambiaLII ZMCC 2025 reparse backlog**: 7 → 3 remaining (resolved 4 of 7 this tick: 18, 21, 24, 28; remaining deferred: ZMCC 16 collision, ZMCC 19 scanned-PDF, ZMCC 33 collision)
- **ZambiaLII ZMCC 2024 reparse backlog**: 4 → 1 remaining (resolved 3 of 4 this tick: 22, 23, 25; remaining deferred: ZMCC 27 collision)

## Fetch cost this tick

- Network fetches: **0** (zero net-new HTTP requests; all source files already on disk from prior probe/sweep ticks).
- Daily JIW budget: 0 / 500 used today by JIW.

## Outstanding deferred records (cumulative, post-b0696)

- `judgment-zm-2020-coa-113-chisumpa-liandisha-v-the-people` — truncated source PDF from judiciaryzambia.com (carry-over from prior batches).
- `judgment-zm-2025-zmcc-16-miles-bwalya-sampa-v-attorney-general-and-4-ors` — case_number-collision (carry-over from b0695).
- **NEW** `judgment-zm-2025-zmcc-19-betbio-zambia-ltd-and-anor-v-attorney-general-and-ors` — scanned-PDF-no-extractable-text-ocr-required. Cohort: `scanned-pdf-ocr-required`.
- **NEW** `judgment-zm-2025-zmcc-33-miles-bwalya-sampa-v-the-attorney-general-and-ors` — case_number-collision (third ruling in the Sampa Mopani-Delta petition; 6-1 majority dismissed petition with Chisunka JC dissenting).
- **NEW** `judgment-zm-2024-zmcc-27-michelo-chizombe-v-edgar-chagwa-lungu-and-ors` — case_number-collision (multiple rulings in the Chizombe v Lungu petition).

## Recommended priority for next JIW tick

1. **Maintainer action FIRST**: ZMCC 16/27/33 dedup-policy decision. Recommend treating (`case_number`, `citation`) as the dedup tuple, not `case_number` alone, so that multiple rulings in the same petition can be ingested. Three deferred items in this cohort now.
2. **Priority-(a) REPARSE — OCR pass**: ZMCC 2025/19 (Betbio Zambia v AG) — needs `ocrmypdf` on host, then standard hand-curation. The same OCR fallback is likely to apply to additional scanned PDFs not yet probed.
3. **Priority-(a) REPARSE — ZMCC 2024 gap-fill**: 11 ZMCC 2024 PDFs on disk that have not been touched yet (02, 04, 05, 06, 07, 08, 10, 13, 15, 17, 20). Each is a candidate for hand-curation. ~8 per tick is feasible.
4. **Priority-(b) CoA NEW from judiciaryzambia.com**: Josias Mtonga (app-110-2024), Skab Merchants (app-344-2023), Tulambo Kumwenda (app-47-2025). 3 records, ~6 fetches.

## Wall-clock

Start: 2026-05-18T11:08Z. Finish: 2026-05-18T~11:20Z. Elapsed: ~12 minutes. Budget: 20 minutes. Headroom: ~8 minutes. Within budget; no race-recovery overshoot.

## Note on in-place mutation strategy

This tick adopted **direct in-place mutation** of `corpus.sqlite` (PRAGMA journal_mode=MEMORY, synchronous=OFF) rather than the stage-and-replace pattern used in b0676..b0695. Rationale: the b0695 post-mortem ("CONCURRENT_WORKER_RACE_DETECTED") demonstrated that stage-and-replace is unsafe when other workers may mutate the live DB between the stage-copy and the promote. Direct in-place mutation eliminates the race window. Backup (`corpus.sqlite.bak.b0696-jiw-pre-20260518T111532Z`) was taken pre-mutation for rollback safety. No concurrent-worker activity was observed during this tick.

## CHECK count summary

```
PRE  records=1939 records_fts=1939 judgments_meta=246
POST records=1946 records_fts=1946 judgments_meta=253
Δ    +7         +7              +7
parity OK; quick_check=ok; integrity_check=ok
```
