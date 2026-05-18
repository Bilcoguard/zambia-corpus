# JIW batch b0687 — ZMCC 2025 reparse +8 records (priority-a, hand-curated)

**Run**: 2026-05-18T00:00Z–00:11Z (scheduled judgment-ingestion-worker, ~11 min wall-clock)
**Result**: 8 records inserted (records: 1928 → 1936; records_fts: 1928 → 1936; judgments_meta: 235 → 243; parity OK; quick_check ok; integrity_check ok)
**Parser**: 0.3.2-jiw-b0687-hand-curated (per-record operative-paragraph anchoring)
**Fetches**: 0 new HTTP fetches against any host (all 16 raw HTML+PDF pairs already on disk from prior probe ticks); daily JIW budget unchanged at 0/500.

## Records inserted

| ID | Citation | Case | Date | Judges | Outcome | Source SHA-256 |
|---|---|---|---|---|---|---|
| `judgment-zm-2025-zmcc-05-miza-phiri-jr-v-isaac-mwanza-and-ors` | [2025] ZMCC 5 | Miza Phiri Jr v Isaac Mwanza and Ors (2024/CCZ/0021) | 2025-03-24 | Munalula PC; Musaluke, Mulife JJC | dismissed (abuse of court process) | `097bdbaeb2584c71df1e0dcc22d3b0fa35e3e47e85c01b9046584e090253587f` |
| `judgment-zm-2025-zmcc-06-miles-bwalya-sampa-v-attorney-general` | [2025] ZMCC 6 | Miles Bwalya Sampa v AG (2024/CCZ/0024) | 2025-03-24 | Mwandenga JC (single) | dismissed (s.13 CCA summons - no relevance) | `97ca345d34fa1ca31d3f30e8eca2b1aaa3d29420fd2100f18afc740f412b451d` |
| `judgment-zm-2025-zmcc-07-munir-zulu-v-the-attorney-general-and-ors` | [2025] ZMCC 7 | Munir Zulu v AG and Ors (2025/CCZ/0010) | 2025-04-07 | Mapani-Kawimbe JC (single) | dismissed (no jurisdiction over Subordinate Court stay) | `17e71ee8958e66814f45ec6ff73fc4aa182164497e9c7895c23262dc1e988237` |
| `judgment-zm-2025-zmcc-08-richard-sakala-v-the-attorney-general` | [2025] ZMCC 8 | Richard Sakala v AG (2024/CCZ/0014) | 2025-04-01 | Shilimi DPC, Chisunka, Mwandenga (dis), Kawimbe, Mulife JJC | dismissed 4:1 (delay - 20+ yrs slept on rights, Art 118(2)(b)) | `c9af58398771aa70795df4e82d2e25b9d5741e7a564718f517adbc4c6d0f0319` |
| `judgment-zm-2025-zmcc-09-the-people-v-attorney-general` | [2025] ZMCC 9 | The People v AG (Ex Parte Nickson Chilangwa) (2024/CCZ/R001) | 2025-02-10 | Munalula PC, Shilimi DPC, Musaluke, Chisunka, Mulongoti, Mwandenga, Kawimbe, Mulife JJC (8) | other (constitutional reference - opinion: Art 72(2)(b)+70(2)(f) automatic vacation) | `9d7f4d2d78ae1516aabe2177ab2f65fb3c2c394a742fe226238bc1512967866c` |
| `judgment-zm-2025-zmcc-10-munir-zulu-v-attorney-general-and-ors` | [2025] ZMCC 10 | Munir Zulu v AG and Ors (2025/CCZ/0011) | 2025-06-04 | Mulife JC (single, in Chambers) | dismissed (misconceived, frivolous; bound by full bench) | `db0018cb3f15e8f5bf53d62b9e9708ae3e7f632d0db33027c3f5f14fa722a56d` |
| `judgment-zm-2025-zmcc-11-ford-chombo-v-the-attorney-general` | [2025] ZMCC 11 | Ford Chombo v AG (2025/CCZ/008) | 2025-06-19 | Munalula JSD/PC, Kawimbe JC | dismissed (Art 189(2) non-retrospective; pre-2016 dispute is labour matter) | `02c3d235b0face947f0f0f9bd332648bba1951e902cd97d2b2808af1136a12ba` |
| `judgment-zm-2025-zmcc-12-munir-zulu-and-anor-v-attorney-general` | [2025] ZMCC 12 | Munir Zulu and Anor v AG (2025/CCZ/009) | 2025-06-27 | Munalula PC, Shilimi DPC, Musaluke, Chisunka, Mulongoti, Mwandenga, Mulife JJC (7) | dismissed (Art 79 governs; consultations not preconditions) | `bb49fa22efad0fb7c8474a90fdec1154a0419e7b9386794e` (sha256 in record) |

## Methodology

1. Read `gaps.md` and prior batch reports — confirmed integrity preconditions (records=records_fts=1928, quick_check=ok) post b0686-jiw.
2. Enumerated raw HTML+PDF on disk under `raw/zambialii/judgments/zmcc/2025/` — 33 pairs.
3. Cross-referenced existing records → identified 18 deferred candidates with raw on disk and no inserted record.
4. Selected MAX_BATCH_SIZE=8 — first 8 (ZMCC 5–12) in numeric order. Skipped 13 (already-resolved).
5. For each candidate, executed targeted PDF text extraction:
   - First 2 pages → `Coram` line, case number, parties
   - Final 2 pages → operative paragraph (the "we dismiss / it is hereby dismissed" line)
   - Whole-document search for `we (dismiss|allow|grant|refuse|set aside|uphold) / petition is ... / accordingly / we therefore / for the foregoing reasons` patterns
6. Hand-curated metadata where operative anchor verified by visual inspection (no fabrication — every disposition is anchored to a specific paragraph quoted in the gaps.md entry).
7. Computed SHA-256 of source PDF; populated record JSON with `raw_sha256`, `source_hash`, `source_url`, `fetched_at`, `parser_version`.
8. Staged corpus.sqlite copy to `/sessions/wizardly-ecstatic-noether/jiw_b0687_stage/corpus_work.sqlite` (114 MB). Inserted into 3 tables (records, records_fts, judgments_meta). Verified `quick_check=ok` and `integrity_check=ok` on staged DB. Promoted to live via binary `copyfileobj` (FUSE-safe; new live size 118,898,688 bytes; backup at `corpus.sqlite.bak.b0687-pre-20260518T001058Z`).
9. Re-ran integrity checks on live DB — all 8 CHECKs PASS.

## Integrity checks

| Check | Result | Notes |
|---|---|---|
| CHECK1 | PASS | All 8 records have ≥1 judge in `judges[]` (min 1, max 8) |
| CHECK2 | PASS | `issue_tags` non-empty for all 8 (6–7 tags each) |
| CHECK3 | PASS | Outcomes from allowed enum: 7×`dismissed`, 1×`other` |
| CHECK4 | PASS | All judge canonical names resolve in `judges_registry.yaml` (no new judges added; 8 canonical names used: Munalula, Musaluke, Mulife, Mwandenga, Kawimbe, Shilimi, Chisunka, Mulongoti) |
| CHECK5 | PASS | No duplicate IDs |
| CHECK6 | PASS | `raw_sha256` matches on-disk PDF for all 8 (re-verified post-insert) |
| CHECK7 | PASS | No duplicate (court + case_name + date_decided) triplets |
| CHECK8 | **PASS** | `records=1936 == records_fts=1936`; `quick_check=ok`; `integrity_check=ok` |

## Dispositions — operative-paragraph anchors

All 8 dispositions are anchored on explicit operative-paragraph verbs found in the PDF body (not summary patterns, which failed in v0.3.1 / v0.3.2 automated runs). Specific anchors:

- ZMCC 5: "we order that this petition be dismissed forthwith" — Conclusion §8.1, page R22
- ZMCC 6: "the Application for a summons under section 13 of the CCA has no merit and is therefore dismissed" — Conclusion §2.0, page R36
- ZMCC 7: "I find the application to be misconceived and dismiss it for want of jurisdiction" — §25, page R12
- ZMCC 8: "For the foregoing reasons, the petition is dismissed" — Conclusion §62, page R22 (majority)
- ZMCC 9: "the answer to the referred constitutional question is that ... imprisonment ... triggers the automatic vacation" — §30, page CR12 (outcome `other`: opinion, not disposition)
- ZMCC 10: "I accordingly dismiss the summons" — Conclusion §85, page R33
- ZMCC 11: "It is dismissed and each party will bear their own costs" — §17, page R10
- ZMCC 12: "Accordingly, we would dismiss the petition and make no order as to costs" — §107

## Notes on ZMCC 9 outcome classification

ZMCC 9 (The People v AG, Ex Parte Nickson Chilangwa) is a constitutional reference under Article 128(2) — an OPINION answering a referred question from the Chinsali High Court, not a disposition of an underlying appeal/petition. The 12 enumerated outcomes in the schema do not include "opinion" or "reference-answered". Classified as `other` with the full referred-question answer in `outcome_detail`. This is consistent with the BRIEF's enum, which permits `other` for non-standard dispositions.

## Notes on ZMCC 11 coram

ZMCC 11's coram line in the source PDF is heavily OCR-damaged ("Coram Munalula , · · JC on 4th April..."). Only Munalula PC (signature visible at end as "M M Munalula (JSD), Constitutional Court President") and Kawimbe (signature visible as "MM Ka imbe") were legibly identified. The closing block shows "Constitutional Court Judge Constitutional Court Judge" indicating a 3-judge panel, but the third name is unrecoverable from this PDF rendering. Per non-negotiable #1 (no fabrication), only the 2 legibly-identified judges are listed. CHECK1 (≥1 judge) is satisfied. Held as low-priority enhancement for future hand-curation pass with higher-quality source.

## Sweep cursors (updated)

- `judiciary-coa-sweep`: page-9 (unchanged — scanned-PDF cliff)
- `judiciary-scz-sweep`: page-2 (unchanged)
- `judiciary-zmcc-sweep`: not yet started (unchanged)
- `judiciary-hc-sweep`: not yet started (unchanged)
- **ZambiaLII ZMCC 2025 reparse backlog**: 18 → 10 remaining (resolved 8 of 18; remaining: ZMCC 14, 15, 16, 17, 18, 19, 21, 24, 28, 33)

## Fetch cost this tick

- Network fetches: **0** (zero net-new HTTP requests; all source files already on disk from prior probe/sweep ticks)
- Daily JIW budget: 0 / 500 used today; full headroom preserved for subsequent ticks

## Outstanding deferred records (unchanged carry-over)

- `judgment-zm-2020-coa-113-chisumpa-liandisha-v-the-people` — truncated source PDF from judiciaryzambia.com; alternate-source retrieval required.

## Recommended priority for next JIW tick (b0689-jiw or later — b0688 taken by concurrent repair worker)

1. **First**: priority-(a) REPARSE — continue ZMCC 2025 reparse on the remaining 10 deferred records (14, 15, 16, 17, 18, 19, 21, 24, 28, 33). Same zero-net-fetch hand-curation pathway as this tick.
2. **Second**: priority-(d) ZMCC 2024 reparse — 4 remaining deferrals (2024/22, /23, /25, /27).
3. **Third**: priority-(b) Judiciary CoA sweep page-10 onwards probe — only after repair-worker confirms scanned-PDF backlog drained.
4. **Defer**: Subordinate Court (priority-f) until SCZ/ZMCC/CoA gap-fill complete.

## Wall-clock

Start: 2026-05-18T00:00Z. Finish: 2026-05-18T00:11Z. Elapsed: ~11 minutes. Budget: 20 minutes. Headroom: 9 minutes.
