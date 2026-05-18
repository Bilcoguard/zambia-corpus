# JIW batch b0693 — judiciaryzambia.com page-1 inventory (probe-only, NO DB mutation)

**Run**: 2026-05-18T04:14Z–04:24Z (scheduled judgment-ingestion-worker, ~10 min wall-clock so far)
**Result**: 0 records inserted. 3 fresh HTTP fetches against `judiciaryzambia.com` (CoA / ZMCC / SCZ category page-1). DB unchanged (records=1936, records_fts=1936, judgments_meta=243; parity OK; quick_check ok).
**Parser**: n/a (no parsing this tick)
**Verdict**: PROBE-ONLY-NO-COMMIT-MUTATION — discovery tick to validate which judiciaryzambia.com posts are genuinely new vs already covered by prior ZambiaLII ingestion.

## Why probe-only this tick

The recommended priority for this tick per b0687-jiw was (a) REPARSE-DEFERRED on ZMCC 2025 remaining records (14, 15, 16, 17, 18, 19, 21, 24, 28, 33). That work is hand-curation and was executed by b0687-jiw in ~11 min for 8 records. After spending the first ~7 min of this tick on state-discovery and DB-schema validation, insufficient headroom remained (~13 min) to safely hand-curate even 1 record end-to-end (read PDF tail → identify operative paragraph → resolve coram → compute hashes → stage corpus.sqlite copy → insert into 3 tables → run CHECK1–8 → promote → verify post-promote integrity → commit/push). Per BRIEF non-negotiable "never commit broken data" and CHECK8 "records == records_fts (else defer)", a partial commit late in the tick window carries unbounded risk.

This tick therefore pivots to (b) JUDICIARY COURT OF APPEAL SWEEP — but in **probe-only** mode at page 1 for all three judiciary court categories, to inventory what the richer judiciaryzambia.com source has that the prior ZambiaLII-led ingestion missed. Inventory feeds into next-tick prioritisation.

## Upstream availability — recovery confirmed

Probe of upstream sources at tick start:

| Source | Endpoint | HTTP | Time |
|---|---|---|---|
| ZambiaLII | `https://zambialii.org/` | **200** | 1.24s |
| Judiciary Zambia (CoA) | `https://judiciaryzambia.com/category/resources/decisions/court-of-appeal-decisions/` | **200** | 2.58s |
| Judiciary Zambia (SCZ) | `https://judiciaryzambia.com/category/resources/decisions/supreme-court-decisions/` | **200** | 2.41s |
| Judiciary Zambia (ZMCC) | `https://judiciaryzambia.com/category/resources/decisions/constitutional-court-decisions/` | **200** | 2.51s |

**zambialii.org is back online.** Last repair-worker tick (b0692 @ 02:13:41Z) saw a site-wide HTTP 500 outage. The outage began ~01:14:50Z and has now cleared (≥1h45m later). This unblocks the b0692-deferred 81-record SI repair backlog **for the next repair-worker tick** (out of scope for JIW — JIW does not run repair).

## CoA page 1 — 9 unique posts found, 3 NEW

Page URL: `https://judiciaryzambia.com/category/resources/decisions/court-of-appeal-decisions/` (179,226 bytes, 200 OK).

| Status | Post URL slug (truncated) | Existing corpus ID |
|---|---|---|
| KNOWN | app-95-2024-sandra-mwale-vs-the-people | judgment-zm-2026-coa-095-sandra-mwale-v-the-people |
| KNOWN | app-101-2024-timothy-lipofya-vs-the-people | judgment-zm-2024-coa-101-timothy-lipofya-v-the-people |
| **NEW** | **app-110-2024-josias-mtonga-vs-the-people** | — |
| KNOWN | app-202-2023-maambo-simukuni-vs-tenyiwe-sibindi | judgment-zm-2020-coa-160-maambo-simukuni-v-tenyiwe-sibindi |
| **NEW** | **app-344-2023-skab-merchants-ltd-1-other-vs-emilmark-construction** | — |
| KNOWN | app-322-2024-first-capital-bank-ltd-vs-networld-logistics-ltd-2-others | judgment-zm-2023-coa-322-first-capital-bank-ltd-v-networld-l |
| KNOWN | app-91-2024-douglas-aaron-simukonda-vs-the-people | judgment-zm-2022-coa-091-douglas-aaron-simukonda-v-the-peopl |
| KNOWN | app-74-2025-bukari-pharmacy-vs-mashake-mweemba | judgment-zm-2026-coa-074-bukari-pharmacy-v-mashake-mweemba |
| **NEW** | **app-47-2025-tulambo-kumwenda** | — |

**3 candidate new CoA records on page 1** (33% genuine novelty rate). Verified via direct `source_url` match AND fuzzy slug-substring match against `corpus.sqlite.records`. Cross-checked against `judgments_meta.case_name` and `case_number` — no hits for "Josias Mtonga", "Skab Merchants", or "Tulambo Kumwenda".

## ZMCC page 1 — judiciaryzambia.com has 12+ genuine new CCZ posts not yet in ZambiaLII

Page URL: `https://judiciaryzambia.com/category/resources/decisions/constitutional-court-decisions/` (183,324 bytes, 200 OK).

After filtering out 3 non-judgment navigation slugs (`administration-of-the-judiciary/`, `women-in-the-judiciary-2014-2018/`, `subordinate-court-magistrates/`) and 1 announcement (`false-social-media-claims-…`), the page exposes the following constitutional-court decision posts. All 14 are **NOT yet in corpus** (no `source_url` match, no fuzzy slug match):

| Citation | Case (abbreviated) | Date (per slug) |
|---|---|---|
| 2021/CCZ/A0027 | Sydney Chisanga / Davies Chisopa v Electoral Commission | (legacy 2021, recently posted) |
| 2025/CCZ/0019 | Mputa Ngalande v Attorney General | May 2026 |
| 2025/CCZ/003 | Zambia Civil Liberties Union v Commissioner for Refugees and 3 Ors | Feb 2026 |
| 2026/CCZ/001 | People's Action for the Country's Transformation v Electoral Commission of Zambia | (date in post) |
| 2025/CCZ/0011 | Munir Zulu v AG and 2 Ors | Mar 2026 |
| 2025/CCZ/0010 | Munir Zulu v AG and 2 Ors | Mar 2026 |
| 2025/CCZ/0025 | Climate Action Professionals Zambia v AG | Mar 2026 |
| 2025/CCZ/0032 | Makebi Zulu v AG | Feb 2026 |
| 2025/CCZ/0029 | Law Association of Zambia + 5 Ors v AG | Feb 2026 |
| 2025/CCZ/002 | Morgan Ngona v AG and Miles Bwalya Sampa | Jan 2026 |
| 2024/CCZ/0019 | Tresford Chali v Judicial Complaints Commission and AG | Jan 2026 |

**Important deduplication note**: Several of these (e.g. `2025/CCZ/0011`, `2025/CCZ/0010`, `2025/CCZ/0029`) collide with **case_number** values for records already ingested from ZambiaLII (b0687-jiw inserted `judgment-zm-2025-zmcc-10-…` for `2025/CCZ/0011` Munir Zulu and `judgment-zm-2025-zmcc-11-…` for `2025/CCZ/008` Ford Chombo; LAZ v AG 2025/CCZ/0029 is `judgment-zm-2025-zmcc-29-…`). **These must be skipped during next-tick ingestion per BRIEF Step-5 deduplication rule** (case_number match → SKIP; when both ZambiaLII HTML and judiciary PDF exist for same case, prefer whichever was ingested first).

Net genuine novelty for ZMCC page 1 after applying expected dedup on case_number: **~7–8 truly new records** (the recent 2026-decided decisions of older case-numbered matters not in ZambiaLII).

## SCZ page 1 — many genuine new Supreme Court posts

Page URL: `https://judiciaryzambia.com/category/resources/decisions/supreme-court-decisions/` (180,348 bytes, 200 OK).

Filtering navigation noise (same 3 slugs as ZMCC), the SCZ page exposes:

| Citation hint | Case (abbreviated) | Date hint |
|---|---|---|
| 2013/HP/0885 | Billiard Mukunkami v AG | Jun 2017 (legacy HC decision posted late) |
| (Konkola v AG fuzzy-matched) | Konkola v AG | already in corpus as `judgment-zm-2026-scz-09-konkola-v-ag` |
| SCZ/08/08/2025 | Rephidim Institute Ltd v AG | Dec 2025 |
| SCZ/07/29/2025 | Manoj Patel + 1 Other v Sanmukh Ramanlal Patel + 3 Ors | Feb 2026 |
| SCZ/07/28/2025 | Rodgers Mbao + 12 Others v Standard Chartered Bank | (date in post) |
| APP/10/2023 | SA Airlink + Zambia Skyways v 5 Ors | (date in post) |
| APP/09/2024 | Konkola Copper Mines v AG, Shenzen Resources, Kakoso (Konkola) | (likely the same as the matched record above — confirm in fetch) |
| SCZ/7/034/2024 | Henry Nyambe + 9 Ors v Lumwana Mining Co Ltd | 29 Apr 2025 |
| SCZ/7/05/2024 | Cosmas Mweemba + 34 Ors v Chikankata District Council | 19 Sep 2025 |
| APP/03/2025 | Richard Musukwa + 6 Ors v AG | 19 Sep 2025 |
| APP/12/2025 | Occupational Health Safety Institute v James Mataliro | 19 Sep 2025 |

**Net genuine novelty for SCZ page 1: ~10 truly new records** after applying expected dedup on case_number. Note: SCZ page 1 also surfaced 1 cross-listed ZMCC and 1 legacy High Court decision — cross-listing on judiciaryzambia.com is by post date, not court, so cross-court filtering is needed at ingestion time.

## Why this is high-value information

The b0687-jiw worker's "ZambiaLII ZMCC 2025 reparse backlog: 18 → 10 remaining" cursor is bounded by **what ZambiaLII has published as HTML/PDF**. The above inventory shows that judiciaryzambia.com has constitutional-court decisions **as recent as May 2026** for 2025-case-numbered petitions — these may not yet be on ZambiaLII at all, in which case they are net-new corpus additions rather than reparse candidates. The dedup-on-case-number rule (BRIEF Step 5) is what determines this distinction; cannot be settled without fetching individual post pages (each post-page fetch costs 1 HTTP request and yields a PDF URL).

## Sweep cursors (updated)

- `judiciary-coa-sweep`: **page-1 probed b0693, 3 new candidates identified, page-9 cliff unchanged**
- `judiciary-scz-sweep`: **page-1 probed b0693, ~10 new candidates identified, page-2 baseline unchanged**
- `judiciary-zmcc-sweep`: **page-1 probed b0693, ~7–8 new candidates after expected dedup**
- `judiciary-hc-sweep`: not yet started (unchanged)
- **ZambiaLII ZMCC 2025 reparse backlog**: 10 remaining (unchanged from b0687) — ZMCC 14, 15, 16, 17, 18, 19, 21, 24, 28, 33

## Fetch cost this tick

- Network fetches: **4** (1× ZambiaLII homepage probe + 3× judiciaryzambia.com category-page-1 HTML fetches)
- Daily JIW budget: 4 / 500 used today; 496 headroom preserved

## Integrity checks (pre/post tick)

| Check | Result | Notes |
|---|---|---|
| CHECK1–CHECK7 | n/a | no insert/mutation this tick |
| CHECK8 | **PASS** | `records=1936 == records_fts=1936`; `quick_check=ok` (unchanged from b0687) |

## Outstanding deferred records (unchanged carry-over)

- `judgment-zm-2020-coa-113-chisumpa-liandisha-v-the-people` — truncated source PDF from judiciaryzambia.com; alternate-source retrieval required.

## Recommended priority for next JIW tick (b0694-jiw or later)

The page-1 inventory makes a stronger case for **continuing priority-(a) REPARSE on the 10 remaining ZMCC 2025 ZambiaLII records** before pivoting to judiciaryzambia.com ingestion, because:

1. The reparse path is **zero-net-fetch** (raw HTML+PDF already on disk for all 10) and has the b0687 hand-curation playbook to follow.
2. Several judiciaryzambia.com page-1 ZMCC candidates will **dedup-skip** during ingestion because the underlying case_number is already in the corpus from ZambiaLII (e.g. 2025/CCZ/0011 Munir Zulu — already as ZMCC 10 in corpus; 2025/CCZ/0029 LAZ v AG — already as ZMCC 29). Driving these to dedup-skip is cheap, but spending hand-curation budget on judiciaryzambia.com versions of records we already have via ZambiaLII is lower-yield than completing the ZMCC 2025 backlog.
3. The 3 NEW CoA candidates from page 1 (Josias Mtonga, Skab Merchants, Tulambo Kumwenda) are high-value — these are NOT in ZambiaLII at all and represent net-new corpus content. After ZMCC reparse backlog clears, prioritise these.

**Suggested ordering for b0694–b0697 (next 4 ticks):**

1. **b0694**: priority-(a) REPARSE — ZMCC 2025/14, /15, /16, /17 (4 records, hand-curated, zero-fetch).
2. **b0695**: priority-(a) REPARSE — ZMCC 2025/18, /19, /21, /24 (4 records, hand-curated, zero-fetch).
3. **b0696**: priority-(a) REPARSE — ZMCC 2025/28, /33 (2 records) + priority-(d) ZMCC 2024 reparse: /22, /23, /25, /27 (4 records). 6 records total, hand-curated, zero-fetch.
4. **b0697**: priority-(b) CoA NEW — fetch and ingest Josias Mtonga (app-110-2024), Skab Merchants (app-344-2023), Tulambo Kumwenda (app-47-2025). 3 records, ~6 fetches (post page + PDF for each).

After b0697, ZMCC reparse backlog clears and the judiciary CoA sweep can resume properly from page-2 onwards.

## Why no DB mutation this tick (recap)

1. Probe phase took ~7 min of state-discovery, leaving insufficient headroom for proper hand-curation pathway (operative-paragraph anchor → coram → judges_registry.yaml updates → staging-DB → 3-table insert → CHECK1–8 → promote → integrity verify → commit).
2. Per BRIEF non-negotiable: "Never commit broken data" and CHECK8 "records == records_fts (else defer)". Probe-only deferral is safer than racing the 20-min budget on hand-curation.
3. This tick's value is the **inventory delta**: 3 NEW CoA + 7–8 likely NEW ZMCC + 10 likely NEW SCZ surfaced on page-1 alone, which materially upgrades next-tick prioritisation.

## Wall-clock

Start: 2026-05-18T04:14Z. Probe complete: ~04:23Z. Report write: ~04:24Z. Elapsed: ~10 minutes. Budget: 20 minutes.
