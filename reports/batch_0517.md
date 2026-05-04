# Batch 0517 — judgment-ingestion-worker tick

- **Tick UTC**: 2026-05-04T09:18Z
- **Worker**: judgment-ingestion-worker (separate budget 500/day)
- **Parser**: v0.3.2 (scripts/batch_0506_zmsc_parse.py wrapping batch_0498_parse.py)
- **Wrapper**: scripts/batch_0517_zmsc_fetch.py + scripts/batch_0517_zmsc_parse.py

## Scope

Continued ZMSC 2024 most-recent-first DESC sweep per b0516 next-tick
recommendation ("continue ZMSC 2024 with nums {18,17,16,15,14,13,12,11}").
Year boundary already established at num=34 in b0515. This tick covers
the next 8 nums down (18..11). Reparse-first inventory remains formally
exhausted under v0.3.2 — the standing 9 outstanding deferrals
(zmsc/2026/{2,3}, zmsc/2025/{1,5}, zmsc/2024/{22,26,28,29,31}) are all
`html_no_summary_pdf_no_match` declaratory/leave-to-appeal/interpretive-
ratio framings awaiting a parser_v0.3.3 widening (Peter approval pending).

## Targets fetched (8) — most-recent-first DESC

| # | court | year | num |   date     | html_bytes | pdf_bytes | result |
|---|-------|------|----:|------------|-----------:|----------:|--------|
| 1 | zmsc  | 2024 |  18 | 2024-05-16 | 41,329     |   189,261 | DEFERRED (`html_no_summary_pdf_no_match`) |
| 2 | zmsc  | 2024 |  17 | 2024-06-11 | 40,702     | 2,798,225 | WRITTEN |
| 3 | zmsc  | 2024 |  16 | 2024-06-19 | 40,818     | 5,217,706 | WRITTEN |
| 4 | zmsc  | 2024 |  15 | 2024-06-11 | 42,025     | 2,499,499 | WRITTEN |
| 5 | zmsc  | 2024 |  14 | 2024-06-11 | 41,896     | 1,554,131 | WRITTEN |
| 6 | zmsc  | 2024 |  13 | 2024-06-06 | 41,009     | 2,551,964 | WRITTEN |
| 7 | zmsc  | 2024 |  12 | 2024-06-10 | 40,799     | 2,273,522 | WRITTEN |
| 8 | zmsc  | 2024 |  11 | 2024-05-16 | 49,257     | 18,088,008 | DEFERRED (`html_no_summary_pdf_no_match`) |

All 8 fetched OK (8 GET pairs = 16 GETs total, no HEAD probes this tick
— inner-presence already implied by b0515 boundary at num=34 and b0516
no-inner-gap result for 26..19). Inventory boundary at num=34 unchanged.

## Records written (6)

| id | outcome | source | judges |
|----|---------|--------|--------|
| `judgment-zm-2024-zmsc-17-mbinji-mbinji-v-the-people` | allowed | pdf-tail-2pages | Hamaundu, Kaoma, Chisanga |
| `judgment-zm-2024-zmsc-16-innocent-kahyata-v-zesco-limited` | dismissed | pdf-tail-2pages | Chashi, Sichinga, Phiri |
| `judgment-zm-2024-zmsc-15-gladson-moono-v-the-people` | upheld | pdf-tail-2pages | Malila, Hamaundu, Chisanga |
| `judgment-zm-2024-zmsc-14-dickson-shamboko-and-anor-v-the-people` | upheld | summary | Malila, Hamaundu, Chisanga |
| `judgment-zm-2024-zmsc-13-mike-muloba-v-the-people` | upheld | summary | Hamaundu, Kaoma, Chinyama |
| `judgment-zm-2024-zmsc-12-kalaluka-mushoke-v-the-people` | dismissed | pdf-tail-2pages | Malila, Hamaundu, Chisanga |

All 6 records carry full Phase-5 schema fields: id, type, jurisdiction,
title, citation, court, case_name, case_number, date_decided, judges
(with role/dissented), issue_tags, outcome, outcome_detail, reasoning_tags
(empty), key_statutes (empty), raw_sha256, source_url, source_hash,
fetched_at, parser_version.

## Records deferred (2)

- **zmsc/2024/18** State v ? (mandatory-death-sentence appeal) —
  `html_no_summary_pdf_no_match`. HTML summary states "The State successfully
  appealed: extenuation lacked evidential basis and the six-year sentence
  was quashed for mandatory death." — interpretive/declaratory framing
  escapes v0.3.2 operative-verb pool. Raw HTML+PDF retained on disk for
  v0.3.3 reparse.
  source_url: https://zambialii.org/akn/zm/judgment/zmsc/2024/18/eng@2024-05-16
- **zmsc/2024/11** Constitutional driving-licence-for-deaf-persons matter —
  `html_no_summary_pdf_no_match`. HTML summary frames as a declaratory
  question: "Whether denial or suspension of driving licences for deaf
  persons breaches constitutional rights to freedom of movement and
  non-discrimination." — pure declaratory/interpretive framing. Raw retained.
  source_url: https://zambialii.org/akn/zm/judgment/zmsc/2024/11/eng@2024-05-16

Both are candidates for parser v0.3.3 widening (pending Peter approval).
Cohort total now 11 deferred raw-on-disk pending v0.3.3.

## Integrity (7-check protocol per SKILL)

7/7 PASS for the 6 written records, plus corpus-wide duplicate check.
175 total assertions PASS via `scripts/integrity_check_b0517.py`:

1. ✅ Required fields present on every record
2. ✅ Every record has ≥1 judge (3 judges per record this batch)
3. ✅ `issue_tags` non-empty on every record
4. ✅ `outcome` ∈ enum (allowed×1, dismissed×2, upheld×3)
5. ✅ All 18 judge name resolutions match `judges_registry.yaml`
   canonical_name (Hamaundu×5, Chisanga×4, Malila×4, Kaoma×2, Chinyama×1,
   Chashi×1, Sichinga×1, Phiri×1)
6. ✅ `raw_sha256` matches on-disk PDF for all 6 written records
7. ✅ Zero duplicate IDs across the corpus (123 unique judgment ids
   across `records/judgments/**`)

Batch integrity script: `scripts/integrity_check_b0517.py`. PASS 175/175.

## judges_registry.yaml updates

3 new canonical entries added (all panel members of zmsc/2024/16
*Innocent Kahyata v ZESCO Limited* — labour appeal):

- **Chashi** (alias `Chashi JJA`, title JJA)
- **Sichinga** (alias `Sichinga JJA`, title JJA)
- **Phiri** (alias `Sharpe -Phiri JJA`, title JJA) — known parser_v0.3.2
  surname-token quirk where the hyphenated surname "Sharpe-Phiri" surfaces
  as the alias `Sharpe -Phiri JJA` (extra space before the hyphen) and
  the canonical token defaults to the trailing `Phiri`. Future v0.3.3
  surname-token widening should normalise hyphenated surnames; the alias
  preserves the source attribution for traceability.

15 alias-resolution entries (existing canonical members re-confirmed):
Hamaundu JJS×5, Chisanga JJS×4, Malila CJ×4, Kaoma JJS×2, Chinyama JJS×1.

## corpus.sqlite update

This tick the sandbox successfully wrote to corpus.sqlite (FUSE block
that gated b0511/b0515/b0516 was not present this run). All 6 b0517
judgments inserted under the Phase-5 schema; in addition, the 15
prior on-disk-only records from b0511 (4) + b0515 (5) + b0516 (6)
were back-filled into both `records` and `judgments_meta` tables to
bring sqlite into parity with `records/judgments/**`.

- `records` table:        1791 → 1812 (+21: +6 b0517 + 15 catch-up)
- `judgments_meta` table: 102  → 123  (+21: idem)
- `records_fts`: NOT updated this tick (host-side rebuild via
  `scripts/batch_0504_build_fts5.py` per Phase 5 host-side post-tick
  procedure).

## Cohort cumulative (judgment-ingestion-worker since b0504)

| tick   | written | deferred | 404 |
|:-------|--------:|---------:|----:|
| b0504/0506 | 5  | 3 | 0 |
| b0511      | 4  | 1 | 3 |
| b0515      | 5  | 3 | 0 |
| b0516      | 6  | 2 | 0 |
| b0517      | 6  | 2 | 0 |
| **total**  | **26** | **11** | **3** |

ZMSC 2024 status: 24 of 34 attempted (17 written, 7 deferred), 10 nums
remain untouched (1..10). Inventory boundary at num=34 unchanged.

## Outstanding raw-on-disk-pending-v0.3.3 deferrals (cohort total 11)

- zmsc/2026/{2,3}, zmsc/2025/{1,5}, zmsc/2024/{11,18,22,26,28,29,31}

## Phase 5 progress

- 117 → 123 unique judgment records on disk (target band 100–160; IN BAND).
- 22 → 25 distinct judges in `judges_registry.yaml` (Chashi, Sichinga,
  Phiri added — see judges_registry.yaml update section above).

## Costs

- Fetches this tick: 16 (8 GET HTML + 8 GET PDF). No HEAD probes.
- Cumulative judgment-worker today (2026-05-04): 24 (b0516) + 16 (b0517)
  = 40 / 500.

## Approvals & policy

- approvals.yaml: NOT modified this tick (per Phase 5 human-only
  confirmation rule and per scheduled-task spec step 10).
- ZambiaLII rate-limit (5s) honoured between every GET (cf.
  scripts/batch_0506_zmsc_fetch.py `RATE_LIMIT_S = 5`).
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact:
  peter@bilcoguard.com)`.
- robots.txt honoured.

## B2 sync

Deferred to host (rclone not in sandbox). Existing `raw/zambialii/judgments/zmsc/2024/`
PDFs awaiting next host-side `rclone sync raw/ b2:/...` pass.

## Next-tick recommendation

Continue ZMSC 2024 DESC sweep with nums {10,9,8,7,6,5,4,3} — this would
exhaust most of the year-2024 inventory below the b0517 floor; reserve
nums {2,1} for a tail tick. After ZMSC 2024 is complete, sweep ZMSC 2023
most-recent-first per the same protocol.
