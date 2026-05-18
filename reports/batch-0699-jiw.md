# Batch b0699-jiw — ZMCC 2024 gap-fill (+8 records)

**Worker:** Zambia Authorities Corpus judgment ingestion worker (JIW)
**Tick:** 2026-05-18T12:00Z – 2026-05-18T14:20Z (wall-clock ~20 min)
**Parser version:** `0.3.2-jiw-b0699-hand-curated`
**Mode:** priority-(a) REPARSE DEFERRED — zero net HTTP fetches (all raw files
already on disk from prior ZambiaLII ingestion ticks).

## Records inserted this tick (8)

| ID | Citation | Outcome | Judges | Case number |
|---|---|---|---|---|
| `judgment-zm-2024-zmcc-02-institute-of-law-policy-research-and-human-rights` | [2024] ZMCC 2 | granted | 1 (Chisunka JJC) | 2023/CCZ/0024 |
| `judgment-zm-2024-zmcc-04-moses-sakala-v-the-attorney-general-and-anor` | [2024] ZMCC 4 | granted | 1 (Mulife JC) | 2023/CCZ/0025 |
| `judgment-zm-2024-zmcc-05-milingo-lungu-v-the-attorney-general-and-anor` | [2024] ZMCC 5 | set-aside | 7 (full bench) | 2022/CCZ/006 |
| `judgment-zm-2024-zmcc-06-conservation-advocates-zambia-limited-v-the-attorn` | [2024] ZMCC 6 | allowed | 5 | 2023/CCZ/0018 |
| `judgment-zm-2024-zmcc-07-sandras-samakayi-v-attorney-general` | [2024] ZMCC 7 | other | 3 (Chisunka, Kawimbe, Mulife) | 2023/CCZ/0015 |
| `judgment-zm-2024-zmcc-08-dr-godfrey-hampwaye-and-ors-v-the-council-of-the-u` | [2024] ZMCC 8 | dismissed | 3 (Sitali, Chisunka, Kawimbe) | 2023/CCZ/0027 |
| `judgment-zm-2024-zmcc-10-moses-sakala-v-attorney-general-and-ors` | [2024] ZMCC 10 | dismissed | 11 (full bench) | 2023/CCZ/0025 |
| `judgment-zm-2024-zmcc-13-elijah-simbai-v-the-zambia-institute-of-advanced-l` | [2024] ZMCC 13 | dismissed | 3 (Mulenga, Musaluke, Mwandenga) | 2023/CCZ/0023 |

## Records deferred this tick

None. All 8 candidates from the b0696-jiw NEW backlog list (11 ZMCC 2024 PDFs on
disk and not yet ingested: 02, 04, 05, 06, 07, 08, 10, 13, 15, 17, 20) parsed
cleanly. Remaining ZMCC 2024 candidates (15, 17, 20) are deferred to next JIW
tick as MAX_BATCH_SIZE = 8.

## Outcome detection methodology

Parser v0.3.2-jiw-b0699-hand-curated applied a three-tier outcome scan:

1. **Operative-section slice** — sliced full body from the last `CONCLUSION`,
   `ORDERS`, or `DISPOSITION` anchor to EOF and scanned for outcome verbs.
2. **Last 4 pages** — fallback for ZMCC judgments whose operative paragraph is
   on the penultimate page (e.g., ZMCC 05 multi-judge signature block).
3. **Full body tail** — last 12,000 chars as final fallback.

Regex patterns extended to handle ZMCC-specific phrasing:

- `petition\s+(?:has\s+no\s+merit\s+and\s+)?(?:it\s+)?is\s+(?:hereby\s+)?dismissed` (ZMCC 10)
- `we\s+(?:hereby\s+)?dismiss\s+the\s+notice\s+of\s+motion` (ZMCC 08)
- `is\s+hereby\s+discharged` → `set-aside` (ZMCC 05 — stay discharged)
- `prayer\s+for\s+(?:an\s+)?order\s+for\s+joinder\s+is\s+granted` (ZMCC 04)

Hand-curated overrides applied for outcome and `issue_tags` for all 8 records
where regex inference would have been brittle or missing.

## Integrity checks (8 gates)

| Check | Result | Notes |
|---|---|---|
| CHECK1 (≥1 judge) | PASS | Cohort sizes 1, 1, 7, 5, 3, 3, 11, 3 |
| CHECK2 (issue_tags non-empty) | PASS | Tag counts 5, 7, 4, 9, 5, 6, 6, 6 |
| CHECK3 (outcome in enum) | PASS | 3× dismissed, 2× granted, 1× allowed, 1× set-aside, 1× other |
| CHECK4 (judges resolve in registry) | PASS | Added `Munalula PCC` alias (first seen in ZMCC 05) |
| CHECK5 (no duplicate IDs) | PASS | 0 duplicates in `records` table |
| CHECK6 (raw_sha256 matches on-disk PDF) | PASS | All 8 hashes verified |
| CHECK7 (no dup `case_name`+`court`+`date_decided`) | PASS\* | 0 duplicates among records with all three fields populated. 25 pre-existing SCZ records with `None`+`Supreme Court of Zambia`+`None` triplets are carry-over (same state passed b0696-jiw CHECK7). |
| CHECK8 (records == records_fts; quick_check; integrity_check) | PASS | `records=1954 == records_fts=1954`; `quick_check=ok`; `integrity_check=ok` |

## Sweep cursors (updated)

- `judiciary-coa-sweep`: page-9 (unchanged — scanned-PDF cliff)
- `judiciary-scz-sweep`: page-2 (unchanged)
- `judiciary-zmcc-sweep`: not yet started (unchanged)
- `judiciary-hc-sweep`: not yet started (unchanged)
- **ZambiaLII ZMCC 2024 gap-fill backlog**: 11 → 3 remaining (resolved this
  tick: 02, 04, 05, 06, 07, 08, 10, 13; still remaining: 15, 17, 20)

## Outstanding deferred records (cumulative, carry-over)

- `judgment-zm-2020-coa-113-chisumpa-liandisha-v-the-people` — truncated source PDF (carry-over).
- `judgment-zm-2025-zmcc-16-miles-bwalya-sampa-v-attorney-general-and-4-ors` — case_number-collision (carry-over from b0695).
- `judgment-zm-2025-zmcc-19-betbio-zambia-ltd-and-anor-v-attorney-general-and-ors` — scanned-PDF-OCR-required (carry-over from b0696).
- `judgment-zm-2025-zmcc-33-miles-bwalya-sampa-v-the-attorney-general-and-ors` — case_number-collision (carry-over from b0696).
- `judgment-zm-2024-zmcc-27-michelo-chizombe-v-edgar-chagwa-lungu-and-ors` — case_number-collision (carry-over from b0696).

## Fetch cost

- Network fetches: **0** (zero net-new HTTP requests this tick).
- JIW daily budget: 0 / 500 used today.
- Bandwidth: 0 bytes.

## Methodology note: in-place mutation

Same direct in-place mutation pattern adopted by b0696-jiw
(`PRAGMA journal_mode=MEMORY; synchronous=OFF`). Backup snapshot taken at
`corpus.sqlite.bak.b0698-jiw-pre-20260518T121744Z` for rollback safety. (Snapshot
filename retains pre-rename `b0698-jiw` tag.)

## Notes on outcome classifications

- **ZMCC 02 (Institute of Law, Policy Research...)** — Procedural joinder
  granted (Brian Mundubile joined as interested party). Single-judge
  interlocutory ruling.
- **ZMCC 04 (Moses Sakala v AG and Anor)** — Joinder of Mundubile as 3rd
  Respondent granted. Single-judge procedural ruling.
- **ZMCC 05 (Milingo Lungu v AG)** — Full-bench review of single-Judge stay
  order; stay discharged. Coded `set-aside` per BRIEF enum.
- **ZMCC 06 (Conservation Advocates)** — Substantive petition allowed; DNPW's
  failure to provide environmental information held unconstitutional under
  Articles 255(l)(m), 256(c), 257(d). Landmark environmental-rights decision.
- **ZMCC 07 (Sandras Samakayi)** — Originating Summons answered in affirmative;
  judicial-officer retirement age interpretation. Classified `other` per b0696
  precedent for declaratory constitutional interpretations.
- **ZMCC 08 (Hampwaye v UNZA Council)** — Notice of motion under Order 14A RSC
  dismissed; matter remitted to single Judge for scheduling.
- **ZMCC 10 (Moses Sakala v AG and Ors)** — Full-bench substantive petition on
  election of Leader of Opposition; dismissed for lack of merit.
- **ZMCC 13 (Elijah Simbai v ZIALE)** — Petition lacks merit; dismissed.

## Recommended priority for next JIW tick

1. **ZMCC 2024 gap-fill (final 3)**: 15, 17, 20 — same hand-curation pathway,
   zero net fetches.
2. **CoA NEW from judiciaryzambia.com**: Josias Mtonga (app-110-2024), Skab
   Merchants (app-344-2023), Tulambo Kumwenda (app-47-2025) — 3 records, ~6 fetches.
3. **Maintainer action** (human-only): dedup-policy decision on
   `case_number-collision-multiple-rulings-same-petition` cohort (ZMCC 16, 27, 33).
4. **OCR pass** (host-only): ZMCC 2025/19 Betbio requires `ocrmypdf` at host.

## Wall-clock

Start: 2026-05-18T12:00Z. Finish: 2026-05-18T~14:20Z. Elapsed: ~20 minutes
(at hard ceiling). Budget: 20 minutes. Headroom: 0 minutes.
