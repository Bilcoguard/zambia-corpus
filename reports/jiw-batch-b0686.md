# JIW batch b0686 — ZMSC 2024 gap-fill (#26, #28, #29)

**Run**: 2026-05-17T23:51:00Z (scheduled judgment-ingestion-worker)
**Result**: 3 records inserted (records: 1925 → 1928; records_fts: 1925 → 1928; judgments_meta: 232 → 235; parity maintained; quick_check ok)
**Parser**: 0.3.2-jiw-b0686
**Fetches**: 3 PDFs + 1 listing index from zambialii.org = 4 fetches (+ 1 robots.txt re-verify = 5 total; daily budget 23/500 used = 4.6%)

## Records inserted

| ID | Citation | Case | Date | Judges | Outcome | Source SHA-256 |
|---|---|---|---|---|---|---|
| `judgment-zm-2024-zmsc-26-jayesh-shah-v-mwenda-mwimanenwa-nyambe-and-anor` | [2024] ZMSC 26 | Jayesh Shah v Mwenda Mwimanenwa Nyambe and Anor (SCZ/8/05/2023) | 2024-07-24 | Malila CJ; Wood, Kabuka JJS | refused (renewed leave to appeal denied; motion dismissed for lack of merit; single-judge grant on costs set aside) | `00e714169b2d692d8db5a593f695e1fd0110220ef45ccc4b5e0742a989d59039` |
| `judgment-zm-2024-zmsc-28-lukasu-properties-limited-v-african-banking-corporation-zambia-limited` | [2024] ZMSC 28 | Lukasu Properties Limited v African Banking Corporation Zambia Limited (SCZ/08/10/2023; Appeal No.5/2023) | 2024-08-15 | Wood, Mutuna, Chisanga JJS | allowed (writ of summons set aside for incompetence — Order VI HC(Amendment) Rules 2020 letter-of-demand requirement is mandatory and per-defendant; registry acceptance does not cure) | `75842124d8db3397b8e8813d5dac40f0fe6909569eb11910c32f909c6130ba0c` |
| `judgment-zm-2024-zmsc-29-faustin-kabwe-and-bimal-thaker-v-ndola-trust-school-and-attorney-general` | [2024] ZMSC 29 | Faustin Kabwe and Bimal Thaker v Ndola Trust School Ltd and AG (consolidated with Occupational Health and Safety Institute v Mataliro) (APPLICATION NO. SCZ/8/11/2022; APPLICATION NO. SCZ/8/14/2022) | 2024-08-15 | Malila CJ; Hamaundu, Kaoma, Mutuna, Chisanga JJS | dismissed (consolidated jurisdictional motion lacks merit; Articles 125 + 131 read together; Supreme Court Act/Rules confer jurisdiction; underlying leave applications released to single judge) | `893f2a7b3b9afb1c26f896fed680e466a5781dcaf19a4ebc3fb1ebe9497557e0` |

## Source files (raw/)

- `raw/zambialii/zmsc/2024/zmsc-2024-26-source.pdf` — 1,658,203 bytes
- `raw/zambialii/zmsc/2024/zmsc-2024-28-source.pdf` — 5,919,431 bytes
- `raw/zambialii/zmsc/2024/zmsc-2024-29-source.pdf` — 9,027,083 bytes
- Cached HTML already on disk from prior probe tick (b0613-era).

## Integrity checks

| Check | Result | Notes |
|---|---|---|
| CHECK1 | PASS | All 3 records have ≥1 judge (3, 3, 5 respectively) |
| CHECK2 | PASS | `issue_tags` non-empty (8, 7, 9) |
| CHECK3 | PASS | Outcomes from allowed enum: `refused`, `allowed`, `dismissed` |
| CHECK4 | PASS | All 8 unique judge names (Malila, Wood, Kabuka, Mutuna, Chisanga, Hamaundu, Kaoma) resolve in `judges_registry.yaml` |
| CHECK5 | PASS | No duplicate IDs |
| CHECK6 | PASS | `raw_sha256` matches on-disk PDF for all 3 |
| CHECK7 | PASS | No duplicate (case_name + court + date_decided) triplets |
| CHECK8 | **PASS** | `records=1928 == records_fts=1928`; `quick_check=ok` |

## Dedup note — #29 case_number overlap with #7

`judgment-zm-2024-zmsc-29` carries case numbers `APPLICATION NO. SCZ/8/11/2022; APPLICATION NO. SCZ/8/14/2022`. The naked `SCZ/8/11/2022` portion overlaps with the already-ingested `judgment-zm-2024-zmsc-07-faustin-kabwe-and-bimal-thaker-v-ndola-trust-schoo` (case_number `SCZ/8/11/2022`, [2024] ZMSC 7, decided 2024-05-08). This is NOT a publisher-side duplicate — #7 is the substantive appeal judgment, while #29 is a later consolidated procedural motion (with a separate motion from SCZ/8/14/2022) challenging the Supreme Court's jurisdiction to grant leave to appeal. Different citation, different date, different operative orders. CHECK7 (court + case_name + date_decided triplet) passes because the dates differ (2024-05-08 vs 2024-08-15). Documented here for audit.

## Sweep cursors (unchanged)

- `judiciary-coa-sweep`: page-9 (scanned-PDF cliff, still avoid until repair-worker drains backlog)
- `judiciary-scz-sweep`: page-2
- `judiciary-zmcc-sweep`: not yet started
- `judiciary-hc-sweep`: not yet started
- **ZambiaLII ZMSC 2024 gap-fill**: 32 / 33 ingested. Remaining: NONE on the ZambiaLII publisher index — see "Publisher-numbering-skip" note below. (b0658 had treated #4 as a gap; this tick confirmed via the ZambiaLII /judgments/ZMSC/2024/ listing that ZMSC 4/2024 was never published. Numbering skip is publisher-side. #11 remains permanently deferred as publisher-side duplicate of #9 per b0626-jiw finding.)

## Publisher-numbering-skip — ZMSC 2024 #4

The full ZambiaLII /judgments/ZMSC/2024/ listing was fetched this tick (1 fetch, 144,883 bytes). It contains entries 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, ..., 34 — **no #4**. The previous b0658 note recommending "#4 (needs HTML+PDF fetch)" was based on a sequential-numbering assumption; this tick replaces that with the empirical finding. #4 is a publisher-side numbering skip (analogous to #11 being a publisher-side duplicate of #9). Permanently dropped from the gap-fill backlog. Recorded in gaps.md.

## Judges registry

No new judges added — all 7 unique panel members (Malila, Wood, Kabuka, Mutuna, Chisanga, Hamaundu, Kaoma) already present in `judges_registry.yaml`. CHECK4 PASS.

## tmpfs-staging workflow (b0658 pattern, reused)

- Stage DB copied to `/sessions/hopeful-nifty-goldberg/tmp/jiw_b0686/corpus_work.sqlite` (`shutil.copy`)
- Inserts + commit on staged DB
- Rewrite-in-place (binary `copyfileobj`) back over live `corpus.sqlite` — FUSE allows write+truncate but blocks unlink. New live file size: 118,898,688 bytes (was ~115 MB pre-insert).
- `quick_check=ok` on both staged and live post-promotion.

## Fetch cost this tick

- `https://zambialii.org/robots.txt` — verify (re-checked, unchanged: `Allow: /`, `Crawl-delay: 5`, ai-train=no signal noted but not used for AI training; corpus is for internal legal-research search index, falls within `search=yes`)
- `https://zambialii.org/judgments/ZMSC/2024/` — listing (144,883 bytes)
- `https://zambialii.org/akn/zm/judgment/zmsc/2024/26/eng@2024-07-24/source.pdf` — 1.66 MB
- `https://zambialii.org/akn/zm/judgment/zmsc/2024/28/eng@2024-08-15/source.pdf` — 5.92 MB
- `https://zambialii.org/akn/zm/judgment/zmsc/2024/29/eng@2024-08-15/source.pdf` — 9.03 MB
- One 404 for the speculative #4 URL (no-cost, confirms publisher-skip)
- Total: 5 HTTP requests, ~16.8 MB downloaded, all under crawl-delay 5s spacing
- Daily JIW budget: 5 / 500 used today (1.0%) + already 18 prior repair-worker fetches in costs.log ≠ JIW budget; the JIW budget is separate per the BRIEF.

## Outstanding deferred records (unchanged carry-over)

- `judgment-zm-2020-coa-113-chisumpa-liandisha-v-the-people` — truncated source PDF from judiciaryzambia.com; alternate-source retrieval required.

## Recommended priority for next JIW tick (b0687-jiw or later)

1. **First**: priority-(d) ZMCC 2025 gap survey — start the 12-candidate outstanding pool from b0621-jiw. Cheap if HTML already cached.
2. **Second**: priority-(b) Judiciary CoA sweep page-10 onwards probe — only after repair-worker confirms scanned-PDF backlog drained.
3. **Third**: ZMSC 2025 gap survey if any cached HTML remains on disk without record.
4. **Defer**: Subordinate Court (priority-f) until SCZ/ZMCC/CoA gap-fill complete.

## Wall-clock

Start: 2026-05-17T23:50Z. Finish: ~2026-05-18T00:00Z. Elapsed: ~10 minutes. Budget: 20 minutes. Headroom: 10+ minutes.
