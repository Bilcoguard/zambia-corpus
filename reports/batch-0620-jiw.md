# Judgment Ingestion Worker — batch 0620-jiw

- **Date (UTC):** 2026-05-12T17:06:36Z start / 2026-05-12T~17:25Z end
- **Worker:** judgment-ingestion-worker
- **Parser version:** 0.3.2 (outcome_detail-as-body convention, matching neighbouring zmsc-08/09)
- **Pool size:** 1917 → 1919 (+2)
- **Fetches today (this worker):** 49 → 54 of 500 daily budget
- **CHECK8:** records=1919 == records_fts=1919 PASS

## Summary

Pivoted from CoA sweep (scanned-PDF cliff on pages 8–9 confirmed in
b0617 + b0618) to ZambiaLII Supreme Court 2026 sweep. Identified two
missing 2026 SCZ judgments on the publisher's page-1 listing and
ingested both. CoA page 10 catalogued only (no PDF probes); 10 posts
dated September 2024 noted for later evaluation.

## Records inserted

### judgment-zm-2026-zmsc-02-rodgers-mbao-and-ors-v-standard-chartered-bank-zambia-plc

- **Citation:** [2026] ZMSC 2
- **Case number:** SCZ/07/28/2025
- **Court:** Supreme Court of Zambia
- **Date decided:** 2026-02-11
- **Coram:** Malila CJ; Kaoma JJS; Chisanga JJS
- **Outcome:** dismissed — motion for leave to appeal fails; applicants
  did not satisfy s 13(3) Court of Appeal Act (no point of public
  importance, no compelling reasons) in their Employment Code Act
  redundancy-pay claim concerning the meaning of "other benefits"
  (car allowances, talk-time and bonuses).
- **Source:** https://zambialii.org/akn/zm/judgment/zmsc/2026/2/eng@2026-02-11
- **HTML sha256:** 516b57ffe8aaf8e8aa56bc2a509a917a68a832e1bc486d45639dccf31275915f
- **PDF sha256 (raw_sha256):** 5334f74f0b9e17249ac12c9a734fa71773287dc505507798e86eb9604b3fecfd
- **PDF pages:** 14 (text-layer; pdfplumber 0.11.9 clean)

### judgment-zm-2026-zmsc-03-manoj-patel-and-anor-v-sanmukh-ramanlal-patel-and-ors

- **Citation:** [2026] ZMSC 3
- **Case number:** SCZ/7/29/2025
- **Court:** Supreme Court of Zambia
- **Date decided:** 2026-02-11
- **Coram:** Malila CJ; Kaoma JJS; Chisanga JJS
- **Outcome:** granted — leave to appeal granted; the appeal raises a
  point of law of public importance (directors' fiduciary duties,
  PACRA records / shareholding) and other compelling reasons; costs
  abide the appeal.
- **Source:** https://zambialii.org/akn/zm/judgment/zmsc/2026/3/eng@2026-02-11
- **HTML sha256:** 79cec44ff370d4a10f8ecb9f2f0e79ccb72ef243dcfc5679dec0caffaeb432d3
- **PDF sha256 (raw_sha256):** 25b6e843dbb1186e973d0a520b0a7083d4ae18507a22f20d0a79701e408cedb9
- **PDF pages:** 36 (text-layer; pdfplumber 0.11.9 clean)

## SCZ 2026 page-1 listing coverage

| ZMSC # | Status                                      |
|:------:|:--------------------------------------------|
| 1      | already in corpus (zmsc-01-kapsch)          |
| 2      | **INSERTED THIS TICK**                      |
| 3      | **INSERTED THIS TICK**                      |
| 4      | already in corpus (zmsc-04-ventriglia)      |
| 5      | absent from publisher's index               |
| 6      | already in corpus (zmsc-06-ventriglia)      |
| 7      | already in corpus (zmsc-07-munir)           |
| 8      | already in corpus (zmsc-08-konkola)         |
| 9      | already in corpus (zmsc-09-kapopo-patel)    |
| 10     | already in corpus (zmsc-10-first-quantum)   |

Coverage after this tick: 9/9 of what's published; 10/11 if ZMSC 5
returns to the index later.

## CoA page 10 probe (catalogue only — no PDF fetches)

Fetched listing: https://judiciaryzambia.com/category/resources/decisions/court-of-appeal-decisions/page/10/
181,531 bytes, sha256 fbc105f4eddcae5f5cc6778debe720ff171f4b01f986749af8b5a6d3b1826162.
10 articles parsed (post-thumbnail href extraction):

1. APP/102/2022 — Zubao Harry Juma vs First Quantum Mining & Operations Ltd, Road Division — 18 Sept 2024 — Kondolo SC, Majula, Patel JJA
2. APP/192/2022 — Standard Chartered Bank Zambia Plc vs Rodgers Mbao + 12 others — 18 Sept 2024 — Kondolo SC, Majula, Patel SC JJA
   (note: this is the Court of Appeal predecessor of ZMSC 2 ingested this tick)
3. APPEAL/204/2022 — Richard Ndonji vs Lafarge Zambia Plc — 18 Sept 2024 — Kondolo SC, Majula, Patel JJA
4. APP/257/2022 — Katongo Chilufya Elliot vs Jonathan Hugh Elliot — 04 Sept 2024 — Makungu, Sichinga, Sharpe-Phiri JJA
5. APP/248/2022 — David Mufwaya vs Dora Shilute — 04 Sept 2024 — Makungu, Sichinga, Sharpe-Phiri JJA
6. APP/138/2022 — Attorney General vs David Mumba + 1 other — Kondolo SC, Majula, Banda-Bobo JJA
7. APP/254/2022 — Amelia Bembe Toco Batista vs Zambia National Commercial Bank Plc — Kondolo SC (variant 1)
8. APP/254/2022 — Amelia Bembe Toco Batista vs Zambia National Commercial Bank Plc — Kondolo SC (variant 2; possible duplicate post)
9. (post-19864 — slug "19864-2" — likely an orphan/draft post; skipped)
10. APP/98/2023 — Zifa Chirwa vs The People — Ngulube, Muzenga, Chembe JJA

These are decisions delivered Sept 2024 — older than the page 8–9
cliff. Probe of one or two PDFs next tick would test whether the
cliff is a date threshold (text-PDFs for Sept 2024 era and earlier).
If text-layer, page 10 yields up to 8 net ingestions after dedup of
APP/192/2022 (parent of ZMSC 2 — separate court, separate record),
exclusion of the duplicate APP/254/2022 post variant, and exclusion
of the orphan post-19864.

## Integrity checks

| Check  | Status | Notes                                                          |
|:-------|:------:|:---------------------------------------------------------------|
| CHECK1 | PASS   | Both records have judges[] populated (3 judges each)           |
| CHECK2 | PASS   | issue_tags non-empty (5 tags each)                             |
| CHECK3 | PASS   | outcome ∈ enum (dismissed, granted)                            |
| CHECK4 | PASS   | All 3 judges resolve in registry (Malila, Kaoma, Chisanga)     |
| CHECK5 | PASS   | No duplicate IDs                                               |
| CHECK6 | PASS   | raw_sha256 matches on-disk PDF for both records                |
| CHECK7 | PASS   | No duplicate case_name + court + date_decided combinations     |
| CHECK8 | PASS   | records=1919 == records_fts=1919                               |
| FTS5   | PASS   | integrity-check pre-insert and post-insert; FTS search returns |
|        |        | both new records for "Mbao" and "Sanmukh" tokens               |

## Cost ledger

5 fetches consumed (well within 500/day):

| URL                                                                      | Bytes   | SHA prefix |
|:-------------------------------------------------------------------------|--------:|:-----------|
| zambialii.org/.../zmsc/2026/2/eng@2026-02-11 (html)                      |  44,504 | 516b57ff…  |
| zambialii.org/.../zmsc/2026/2/eng@2026-02-11/source.pdf                  | 188,804 | 5334f74f…  |
| zambialii.org/.../zmsc/2026/3/eng@2026-02-11 (html)                      |  46,169 | 79cec44f…  |
| zambialii.org/.../zmsc/2026/3/eng@2026-02-11/source.pdf                  | 381,963 | 25b6e843…  |
| judiciaryzambia.com/.../coa/page/10/ (listing only)                      | 181,531 | fbc105f4…  |

**Total this tick:** 842,971 bytes; **cumulative today:** 54/500.

## Operator notes

- The CoA scanned-PDF cliff appears date-correlated: pages 8–9
  (decisions delivered late 2024 / early 2025) are 100% scanned;
  page 10 (decisions delivered Sept 2024) is unprobed but likely
  contains text-PDFs given the older upload era. Suggest one
  next-tick PDF probe to test the cliff date threshold.
- ZMSC 5/2026 is absent from the publisher's index — not a corpus
  gap, a source-side gap. Will be picked up automatically if added.
- Konkola Copper Mines duplicate (`scz-09-konkola-v-ag` pilot record
  vs `zmsc-08-konkola` ZambiaLII record) remains as previously
  documented — not touched this tick per "prefer whichever was
  ingested first" rule.

## Targets

- Court of Appeal: 50/800 unchanged (sweep blocked by cliff)
- Supreme Court of Zambia: 92 → 94
- Constitutional Court: 85 unchanged
- High Court: unchanged

## B2 sync

`rclone` not available in sandbox; B2 sync deferred to host as per
batch convention since b0608.

User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
