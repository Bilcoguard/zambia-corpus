# JIW batch b0695 — ZMCC 2025 reparse +3 records (priority-a, hand-curated)

**Run**: 2026-05-18T10:00Z–10:18Z (scheduled judgment-ingestion-worker, ~18 min wall-clock)
**Result**: 3 records inserted; 1 record deferred (case_number collision); records 1936→1939; records_fts 1936→1939; judgments_meta 243→246; parity OK; quick_check ok; integrity_check ok.
**Parser**: `0.3.2-jiw-b0695-hand-curated` (per-record operative-paragraph anchoring; continuation of b0687-jiw methodology)
**Fetches**: 0 new HTTP fetches (all 4 raw HTML+PDF pairs already on disk from prior probe ticks); daily JIW budget unchanged at 0/500.

## Records inserted

| ID | Citation | Case | Date | Coram size | Outcome | Source SHA-256 |
|---|---|---|---|---|---|---|
| `judgment-zm-2025-zmcc-14-the-people-v-john-sinkamba-and-ors` | [2025] ZMCC 14 | The People v John Sinkamba and Others (2025/CCZ/R001) | 2025-07-25 | 5 (incl. Mwandenga concurring) | `other` (constitutional reference — opinion: definition of "child" under Article 266) | `2d2e99f95bc0a3c81d2a274f3833798996d7d4dc23c567369dee28cf97eb6dbc` |
| `judgment-zm-2025-zmcc-15-tresford-chali-v-judicial-complaints-commission-and-attorney-general` | [2025] ZMCC 15 | Tresford Chali v JCC and AG (case_number not legibly extractable) | 2025-07-23 | 7 | `other` (interlocutory ruling — standing upheld, matter to trial 29 July 2025) | `66d8f5f48be943ffb18c5d51e12607f7a166373e95c90cf40bf5857332aaf13f` |
| `judgment-zm-2025-zmcc-17-isaac-mwanza-v-national-assembly-of-zambia-and-ors` | [2025] ZMCC 17 | Isaac Mwanza v Nat'l Assembly, AG, ECZ (2024/CCZ/0022) | 2025-08-27 | 7 | `dismissed` (petition not properly before Court — Order IV rule 2 non-compliance) | `2759ceeb701621bce2acaede8d33c3acb56722ab8c5ca59bd5c16e432c925b0c` |

## Records deferred this tick

| ID candidate | Citation | Case | Defer reason |
|---|---|---|---|
| `judgment-zm-2025-zmcc-16-miles-bwalya-sampa-v-attorney-general-and-4-ors` | [2025] ZMCC 16 | Miles Bwalya Sampa v AG and 4 Ors (2024/CCZ/0024) | **case_number collision** with `judgment-zm-2025-zmcc-06-miles-bwalya-sampa-v-attorney-general` (already in corpus, inserted b0687-jiw, [2025] ZMCC 6, decided 2025-03-24). Both are legitimate distinct rulings within the same petition (ZMCC 6 = substantive ruling on s.13 CCA summons; ZMCC 16 = interlocutory ruling on amicus curiae application by LAZ before Mwandenga JC). SKILL.md dedup rule (case_number match → SKIP) was honoured. Recommend maintainer relax dedup rule (or supply a per-citation tie-break) so that multiple rulings in the same petition can be ingested. See gaps.md b0695 section. |

## Methodology

1. Read `worker.log`, `gaps.md`, and `reports/jiw-batch-b0693.md` — confirmed integrity preconditions (records=records_fts=1936, quick_check=ok) post b0694-repair.
2. Verified pdfplumber 0.11.9, pypdf 3.17.4, pdfminer available. Stale journals (`_stale_b0521`, `_stale_b0553`, `_stale_b0694`) already renamed by repair worker; no fresh journal blocking access.
3. Selected MAX_BATCH_SIZE=4 candidates from b0693's recommended priority-(a) list (ZMCC 2025/14–17). All 4 raw HTML+PDF pairs present on disk.
4. For each candidate, executed targeted PDF text extraction with `pdfplumber`:
   - First 2 pages → Coram line, case number, parties
   - Last 3 pages → operative paragraph + judges' signatures
   - Whole-document regex search for outcome verbs (dismiss/grant/allow/refuse/set aside/upheld/quashed/struck-out) anchored to operative-paragraph phrasing.
5. Hand-curated metadata where operative anchor verified by visual inspection (no fabrication — every disposition is anchored to a specific paragraph). Where text was illegible/OCR-damaged (ZMCC 14 coram garbled with "K~;N~ ~ KA~EBA"; ZMCC 15 case number area only showed a registrar's stamp), the SKILL non-negotiable #1 ("never fabricate") was honoured by leaving uncertain fields out / null.
6. Computed SHA-256 of source PDF; populated record JSON with `raw_sha256`, `source_hash`, `source_url`, `fetched_at`, `parser_version`.
7. Staged corpus.sqlite copy to `/sessions/zen-quirky-brown/jiw_b0695/corpus_work.sqlite` (118,898,688 bytes). Opened with `PRAGMA journal_mode=MEMORY; synchronous=OFF` (per b0694 disk-I/O workaround). Inserted into 3 tables (records, records_fts, judgments_meta). Verified `quick_check=ok` and `integrity_check=ok` on staged DB. Promoted to live via binary `copyfileobj` (FUSE-safe; new live size unchanged at 118,898,688 bytes; backup at `corpus.sqlite.bak.b0695-jiw-pre-20260518T101303Z`).
8. Wrote 3 record JSON files to `records/judgments/zmcc/2025/`.
9. Re-ran integrity checks on live DB — all CHECKs PASS.

## Integrity checks

| Check | Result | Notes |
|---|---|---|
| CHECK1 | PASS | All 3 records have ≥1 judge in `judges[]` (5, 7, 7) |
| CHECK2 | PASS | `issue_tags` non-empty for all 3 (6, 7, 10 tags respectively) |
| CHECK3 | PASS | Outcomes from allowed enum: 2×`other`, 1×`dismissed` |
| CHECK4 | PASS | All judge canonical names resolve in `judges_registry.yaml` (Munalula, Shilimi, Musaluke, Chisunka, Mulongoti, Mwandenga, Kawimbe, Mulife — all pre-existing) |
| CHECK5 | PASS | No duplicate IDs (verified post-insert SELECT) |
| CHECK6 | PASS | `raw_sha256` matches on-disk PDF for all 3 (re-computed post-insert) |
| CHECK7 | PASS | No duplicate (court + case_name + date_decided) triplets (verified pre-insert) |
| CHECK8 | **PASS** | `records=1939 == records_fts=1939`; `quick_check=ok`; `integrity_check=ok` |

## Dispositions — operative-paragraph anchors

- **ZMCC 14**: paragraph [46] of opinion of the Court (Musaluke JC): "the combined effect of the definition of a 'child' and a 'person' under Article 266 of the Constitution is that a 'child' under the Constitution means an individual who has reached the age of 18 or is below the age of 18." Classified as `other` because this is a constitutional reference under Article 128(1)(b) — the Court rendered an OPINION answering the referred question rather than disposing of an appeal or petition. Same treatment as ZMCC 9 in b0687 (`other` + descriptive `outcome_detail`). Mwandenga JC issued a separate concurring opinion (final page signature "M.Z. MWANDENGA / CONSTITUTIONAL COURT JUDGE").
- **ZMCC 15**: paragraph [49] of the Ruling: "We therefore, order that this matter will proceed to trial to be held in open Court on 29th July, 2025 at 09.00 hours." This is an interlocutory ruling rejecting the Respondents' preliminary objection on locus standi. Classified as `other` because no listed outcome enum cleanly matches "interlocutory order directing matter to proceed to trial" — the dispositive action is upholding the Petitioner's standing under Articles 1(5), 2, 43(2)(a), 128 and s.11 CCA, but no petition or appeal is disposed of by this ruling.
- **ZMCC 17**: paragraph [161] (Conclusion): "the Petition is not properly before the Court and is therefore dismissed." Classified as `dismissed`. The dismissal is on procedural grounds (Order IV rule 2 of the CCR — paragraphs 15–33 of the petition were surplusage), not on the merits. Costs not awarded (paragraph [162]).

## Notes on ZMCC 14 coram

The coram line of ZMCC 14 is partly OCR-damaged. The legible text reads "Coram: Munalula PC, Shilimi DPC, Musaluke, … and Mulife JJC on 25th July, 2025." A garbled fragment in the surrounding text contains "...awimbe" which suggests Kawimbe was part of the panel, but the fragment sits in the case-caption area rather than the coram itself, so Kawimbe is NOT listed in the inserted record per non-negotiable #1 ("never fabricate"). The conservative coram is: Munalula PC, Shilimi DPC, Musaluke JC (opinion of the Court), Mulife JC + Mwandenga JC (concurring; legible signature on last page). If a higher-quality source becomes available, the coram should be revisited.

## Notes on ZMCC 15 case number

The first page of the ZMCC 15 PDF shows a registrar's date-stamp "13 JUL 2~ /0019" but does NOT show an unambiguous case_number in the standard `YYYY/CCZ/####` format. The fragment "/0019" could be a file index or part of a year-2024 stamp; both are speculative. Per non-negotiable #1, `case_number` is left `NULL` in `judgments_meta`. If the maintainer can supply the case number from the registrar or zambialii ZSC index, it should be backfilled in a future micro-tick.

## Sweep cursors (updated)

- `judiciary-coa-sweep`: page-9 (unchanged — scanned-PDF cliff)
- `judiciary-scz-sweep`: page-2 (unchanged)
- `judiciary-zmcc-sweep`: not yet started (unchanged)
- `judiciary-hc-sweep`: not yet started (unchanged)
- **ZambiaLII ZMCC 2025 reparse backlog**: 10 → 7 remaining (resolved 3 of 10; remaining: ZMCC 16, 18, 19, 21, 24, 28, 33 — note ZMCC 16 deferred this tick on case_number collision)
- **ZambiaLII ZMCC 2024 reparse backlog**: 4 remaining unchanged (2024/22, /23, /25, /27)

## Fetch cost this tick

- Network fetches: **0** (zero net-new HTTP requests; all source files already on disk from prior probe/sweep ticks)
- Daily JIW budget: 0 / 500 used today by JIW; 42+ used by main worker repair/phase8 (separate 2000/day budget)

## Outstanding deferred records

- `judgment-zm-2020-coa-113-chisumpa-liandisha-v-the-people` — truncated source PDF from judiciaryzambia.com (carry-over from prior batches).
- **NEW** `judgment-zm-2025-zmcc-16-miles-bwalya-sampa-v-attorney-general-and-4-ors` — case_number 2024/CCZ/0024 collides with existing ZMCC 6 (different ruling, same petition). Cohort: `case_number-collision-multiple-rulings-same-petition`. Resolution pending maintainer policy decision.

## Recommended priority for next JIW tick (b0697-jiw or later)

1. **First**: priority-(a) REPARSE — continue ZMCC 2025 on ZMCC 18, 19, 21, 24 (4 records). Same zero-net-fetch hand-curation pathway.
2. **Second**: priority-(a) REPARSE — ZMCC 2025/28, /33 + ZMCC 2024 deferrals 2024/22, /23, /25, /27 (6 records).
3. **Third**: priority-(b) CoA NEW from judiciaryzambia.com — Josias Mtonga (app-110-2024), Skab Merchants (app-344-2023), Tulambo Kumwenda (app-47-2025). 3 records, ~6 fetches.
4. **Backlog**: ZMCC 16 case_number-collision resolution — needs maintainer guidance on dedup policy when multiple rulings share a case number.

## Wall-clock

Start: 2026-05-18T10:00Z (this tick). Finish: 2026-05-18T~10:18Z. Elapsed: ~18 minutes. Budget: 20 minutes. Headroom: ~2 minutes.
