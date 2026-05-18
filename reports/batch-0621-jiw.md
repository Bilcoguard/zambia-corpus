# Judgment ingestion batch 0621-jiw

| | |
|---|---|
| Tick start | 2026-05-12T18:18:00Z |
| Tick end   | 2026-05-12T18:30:00Z |
| Wall clock | ~12 min |
| Worker     | judgment-ingestion-worker |
| Phase      | priority-c ZambiaLII sweep continuation |
| Parser     | v0.3.2 |
| UA         | KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com) |

## Summary

Continuation of b0620 ZambiaLII pivot. CoA scanned-PDF cliff
(pages 8–9 of the judiciary CoA decisions category) remains a
blocker for priority-b — pivot to ZambiaLII SCZ + ZMCC gap-fill
sustained for a second tick. **Ingested +4 records** (2 Supreme
Court, 2 Constitutional Court). **Deferred 2** with specific
reasons.

## Source listings probed

| Source | Listed | In corpus pre | Ingested | Deferred | Result |
|---|---|---|---|---|---|
| `https://zambialii.org/judgments/ZMSC/2025/` | 31 (1–13, 15–32) | 28 | 2 | 1 | SCZ-2025 effectively complete |
| `https://zambialii.org/judgments/ZMCC/2026/` | 12 (1–12) | 9 | 2 | 1 | ZMCC-2026 effectively complete |

## Ingested records

| ID | Citation | Case # | Date | Court | Outcome |
|---|---|---|---|---|---|
| `judgment-zm-2025-zmsc-01-occupational-health-and-safety-institute-v-james-mataliro` | [2025] ZMSC 1 | SCZ No.8/14/2022 | 2025-01-15 | Supreme Court | granted |
| `judgment-zm-2025-zmsc-31-hambani-ngwenya-and-anor-v-lubambe-copper-mine-limited` | [2025] ZMSC 31 | SCZ/7/15/2025 | 2025-10-28 | Supreme Court | granted |
| `judgment-zm-2026-zmcc-01-tresford-chali-v-the-judicial-complaints-commission-and-ors` | [2026] ZMCC 1 | 2024/CCZ/0019 | 2026-01-20 | Constitutional Court | dismissed |
| `judgment-zm-2026-zmcc-11-zambia-civil-liberties-union-v-commissioner-for-refugees` | [2026] ZMCC 11 | 2025/CCZ/003 | 2026-04-27 | Constitutional Court | granted |

Outcome detection: all four outcomes extracted via the parser-v0.3.2
PDF order-anchor / operative-paragraph pattern (strategy 2 + 3),
with HTML metadata cross-validation. No falls-through; no defer
on operative-paragraph grounds for the 4 ingested records.

Judge registry: all 14 distinct judges resolve under existing
canonical surnames — no new registry entries required.

## Deferred records

### ZMSC 5/2025 — `William Saunders v Pemba Lapidaries Limted and Anor`

- Case_number `SCZ/8/28/2023` — collides with existing
  `judgment-zm-2025-zmsc-12-pemba-v-william` (citation [2025] ZMSC
  12; date 2025-03-21).
- Both legitimate distinct judgments (preliminary leave/stay order
  by Hamaundu JS on 15 January 2025 vs substantive ZMSC 12 order
  21 March 2025).
- Strict reading of dedup rule step-3 ("If a match exists: SKIP")
  triggers a skip on case_number alone.
- **Action**: operator review of dedup rule interpretation.
- Raw files saved: `_b0621_jiw/html/zmsc-2025-5.html` (42 KB),
  `_b0621_jiw/pdf/zmsc-2025-5.pdf` (366 KB, 7 pages, text-layer).

### ZMCC 12/2026 — `Mputa Ngalande v The Attorney General`

- Case_number `2025/CCZ/0019`; date 2026-05-11.
- PDF (1.30 MB, 29 pages, text-layer) ends mid-discussion at
  paragraph 87 with only one signature block
  (`CONSTITUTIONAL COURT JUDGE`) and **no** operative paragraph or
  "It is hereby Ordered" block.
- Three outcome-extraction strategies (HTML summary, PDF order
  anchors, last-two-pages operative-paragraph scan) all fail.
- Hypothesis (a): ZambiaLII publishes each judge's opinion as a
  separate AKN URL — this is one judge's separate concurring or
  dissenting opinion, and the "lead" judgment is at a different
  URL.
- Hypothesis (b): upload is genuinely truncated (same vendor-issue
  pattern as Chisumpa Liandisha b0615 and Zanaco b0616).
- **Action**: source verification (editor contact, or alternate
  retrieval; also worth checking whether judiciaryzambia.com has a
  fuller PDF).
- Raw files saved: `_b0621_jiw/html/zmcc-2026-12.html` (47 KB),
  `_b0621_jiw/pdf/zmcc-2026-12.pdf` (1.30 MB).

## Integrity checks

| Check | Verdict | Detail |
|---|---|---|
| CHECK1 (judges per record ≥ 1) | PASS | min=1 (SCZ-1, SCZ-31 single-judge orders), max=7 (ZMCC bench) |
| CHECK2 (issue_tags non-empty) | PASS | min=6, max=8 |
| CHECK3 (outcome ∈ enum) | PASS | granted×3, dismissed×1 |
| CHECK4 (judges in registry) | PASS | all 14 distinct judges resolve |
| CHECK5 (no dup IDs) | PASS | 4/4 unique |
| CHECK6 (raw_sha256 matches on-disk PDF) | PASS | all 4 hashes verified post-insert |
| CHECK7 (no dup case_name+court+date) | PASS | 4/4 unique triples |
| CHECK8 (records == records_fts) | PASS | 1923 == 1923 |

## Budget

| | |
|---|---|
| Fetches this tick | 14 |
| Bytes downloaded | ~10.83 MB |
| Cumulative today | 68 / 500 |
| Wall clock | ~12 min |
| Wall budget | 20 min |

Fetch breakdown:
1. `https://zambialii.org/judgments/ZMSC/2025/` — 141.3 KB
2. `https://zambialii.org/judgments/ZMCC/2026/` — 96.1 KB
3-8. Six judgment HTML pages (~40-58 KB each)
9-14. Six judgment source.pdf files (200 KB – 6.26 MB)

## Coverage delta

| Court | Pre | Post | Delta |
|---|---|---|---|
| Supreme Court of Zambia | 92 | 94 | +2 |
| Constitutional Court of Zambia | 85 | 87 | +2 |
| Court of Appeal | 50 | 50 | 0 |
| **Total pool** | **1919** | **1923** | **+4** |

Toward 800-judgment target: **216 / 800** (27.0 %) — judgment-type
records only; the 1923 total includes Acts, SIs, and other corpus
records. Approximate; the 800 target is cumulative across all
courts.

## Recommended priorities for b0622

1. ZambiaLII `/judgments/ZMSC/2024/` — gap survey (corpus has 21
   of unknown total). Priority c (Supreme Court).
2. ZambiaLII `/judgments/ZMCC/2025/` — many gaps (5–12, 14–19, 21,
   24, 28). Priority d (Constitutional Court).
3. ZambiaLII `/judgments/ZMHC/` — High Court (priority e); no
   current coverage on that index — investigate.
4. **Decision required**: ZMSC 5/2025 dedup-rule override (operator).
5. **Decision required**: ZMCC 12/2026 source verification (operator).

## File manifest

- `_b0621_jiw/scz-2025-index.html`
- `_b0621_jiw/zmcc-2026-index.html`
- `_b0621_jiw/html/{zmsc-2025-1,zmsc-2025-5,zmsc-2025-31,zmcc-2026-1,zmcc-2026-11,zmcc-2026-12}.html`
- `_b0621_jiw/pdf/{zmsc-2025-1,zmsc-2025-5,zmsc-2025-31,zmcc-2026-1,zmcc-2026-11,zmcc-2026-12}.pdf`
- `_b0621_jiw/insert_b0621.py`
- `_b0621_jiw/parsed.json`
- `records/judgments/zmsc/2025/judgment-zm-2025-zmsc-01-….json`
- `records/judgments/zmsc/2025/judgment-zm-2025-zmsc-31-….json`
- `records/judgments/zmcc/2026/judgment-zm-2026-zmcc-01-….json`
- `records/judgments/zmcc/2026/judgment-zm-2026-zmcc-11-….json`
- `raw/zambialii/{zmsc,zmcc}/{2025,2026}/{key}-source.pdf`
- `raw/zambialii/{zmsc,zmcc}/{2025,2026}/{key}-eng.html`
- `reports/batch-0621-jiw.md` (this file)
- Logs: `worker.log`, `costs.log`, `provenance.log`, `gaps.md`
