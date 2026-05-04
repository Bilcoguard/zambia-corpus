# Batch 0516 — judgment-ingestion-worker tick

- **Tick UTC**: 2026-05-04T06:30Z
- **Worker**: judgment-ingestion-worker (separate budget 500/day)
- **Parser**: v0.3.2 (scripts/batch_0506_zmsc_parse.py wrapping batch_0498_parse.py)

## Scope

Continued ZMSC 2024 most-recent-first DESC sweep per b0515 next-tick
recommendation ("continue ZMSC 2024 with nums {26,25,24,23,22,21,20,19}").
Year boundary already established at num=34 in b0515. This tick covers
the next 8 nums down (26..19). Reparse-first inventory remains formally
exhausted under v0.3.2 — the standing 7 outstanding deferrals
(zmsc/2026/{2,3}, zmsc/2025/{1,5}, zmsc/2024/{28,29,31}) are all
`html_no_summary_pdf_no_match` declaratory/leave-to-appeal/interpretive-
ratio framings awaiting a parser_v0.3.3 widening (Peter approval pending).

## HEAD probes (8 — inner-presence check, not boundary)

| num | result |
|----:|--------|
|  26 | 200 → @2024-07-24 |
|  25 | 200 → @2024-07-24 |
|  24 | 200 → @2024-07-23 |
|  23 | 200 → @2024-06-10 |
|  22 | 200 → @2024-03-06 |
|  21 | 200 → @2024-06-06 |
|  20 | 200 → @2024-05-15 |
|  19 | 200 → @2024-06-06 |

All 8 inner nums confirmed present (no inner gaps in this slice). Inventory
boundary at num=34 unchanged from b0515.

## Targets (8) — most-recent-first DESC

| # | court | year | num |   date     | result |
|---|-------|------|----:|------------|--------|
| 1 | zmsc  | 2024 |  26 | 2024-07-24 | DEFERRED (`html_no_summary_pdf_no_match`) |
| 2 | zmsc  | 2024 |  25 | 2024-07-24 | WRITTEN |
| 3 | zmsc  | 2024 |  24 | 2024-07-23 | WRITTEN |
| 4 | zmsc  | 2024 |  23 | 2024-06-10 | WRITTEN |
| 5 | zmsc  | 2024 |  22 | 2024-03-06 | DEFERRED (`html_no_summary_pdf_no_match`) |
| 6 | zmsc  | 2024 |  21 | 2024-06-06 | WRITTEN |
| 7 | zmsc  | 2024 |  20 | 2024-05-15 | WRITTEN |
| 8 | zmsc  | 2024 |  19 | 2024-06-06 | WRITTEN |

## Records written (6)

| id | outcome | source | judges |
|----|---------|--------|--------|
| `judgment-zm-2024-zmsc-25-finsbury-investments-limited-v-murray-and-roberts` | dismissed | pdf-tail-2pages | Malila, Kaoma, Kabuka |
| `judgment-zm-2024-zmsc-24-billis-farm-limited-and-anor-v-molosoni-chipabwamb` | allowed | pdf-tail-2pages | Malila, Hamaundu, Chisanga |
| `judgment-zm-2024-zmsc-23-stephen-mwape-v-the-people` | dismissed | summary | Hamaundu, Kaoma, Chinyama |
| `judgment-zm-2024-zmsc-21-benson-kaunda-v-the-people` | dismissed | pdf-tail-2pages | Hamaundu, Kaoma, Chinyama |
| `judgment-zm-2024-zmsc-20-chanda-mwape-and-anor-v-the-people` | allowed | summary | Hamaundu, Kaoma, Chinyama |
| `judgment-zm-2024-zmsc-19-francis-phiri-v-the-people` | dismissed | pdf-tail-2pages | Hamaundu, Kaoma, Chinyama |

All 6 written records carry full Phase-5 schema fields: id, type,
jurisdiction, title, citation, court, case_name, case_number,
date_decided, judges (with role/dissented), issue_tags, outcome,
outcome_detail, reasoning_tags (empty), key_statutes (empty),
raw_sha256, source_url, source_hash, fetched_at, parser_version.

## Records deferred (2)

- **zmsc/2024/26** Sun International v Standard Chartered (renewed leave
  application) — `html_no_summary_pdf_no_match`. Summary: "Applicant's
  renewed leave to appeal denied; no novel point of law and factual
  findings on title and fraud upheld." — leave-to-appeal/interpretive
  ratio framing escapes v0.3.2 operative-verb pool. Raw HTML+PDF
  retained on disk for v0.3.3 reparse.
- **zmsc/2024/22** Kapanji-style court-martial appeal —
  `html_no_summary_pdf_no_match`. Summary: "Evidence of telephone
  confirmations and corroborating call-back stamps upheld a court-martial
  conviction despite a harmless misdirection about producing signature
  comparisons." — interpretive-ratio framing (substantive holding stated
  declaratively without "appeal is X" disposition verb). Raw retained.

Both are candidates for parser v0.3.3 widening (pending Peter approval).
Cohort total now 9 deferred raw-on-disk pending v0.3.3.

## Integrity (7-check protocol per SKILL)

7/7 PASS for the 6 written records, plus corpus-wide duplicate check.
175 total assertions PASS via `scripts/integrity_check_b0516.py`:

1. ✅ Required fields present on every record
2. ✅ Every record has ≥1 judge (range 3 in this batch)
3. ✅ `issue_tags` non-empty on every record (range 2–7 tags)
4. ✅ `outcome` ∈ enum (allowed×2, dismissed×4)
5. ✅ All 18 judge name resolutions match `judges_registry.yaml`
   canonical_name (Hamaundu×4, Kaoma×4, Chinyama×4, Malila×2,
   Kabuka×1, Chisanga×1, all existing)
6. ✅ `raw_sha256` matches on-disk PDF for all 6 written records
7. ✅ Zero duplicate IDs across the corpus (117 unique judgment ids
   across `records/judgments/**`)

Batch integrity script: `scripts/integrity_check_b0516.py`. PASS 175/175.

## Cohort cumulative (judgment-ingestion-worker since b0504)

| tick | written | deferred | 404 |
|:-----|--------:|---------:|----:|
| b0504/0506 | 5 | 3 | 0 |
| b0511      | 4 | 1 | 3 |
| b0515      | 5 | 3 | 0 |
| b0516      | 6 | 2 | 0 |
| **total**  | **20** | **9** | **3** |

Phase 5 corpus judgment count: 102 → 106 (b0511) → 111 (b0515) → 117 (b0516).
Still IN BAND for the Phase 5 target (100–160 landmark judgments).

## Fetches & budget

- HTTP requests this tick:
  - 8 HEAD probes for 26..19 inner-presence check (~0 KB each)
  - 16 GET requests for the 8 candidates (HTML + PDF pairs, all 200)
  - **Total: 24 fetches**
- Cumulative judgment-worker today (2026-05-04): **24/500** (well under
  budget; budget remaining 476).

## judges_registry.yaml

18 alias updates across 6 unique canonical names (Malila, Kaoma, Kabuka,
Hamaundu, Chisanga, Chinyama). All matched existing canonical entries —
no new canonical names introduced. `Chinyama` gained a JJS title-history
entry (previously seen only as J in b0506 zmsc/2026/9). `Kabuka` gained
a JJS title-history entry (previously JS in b0515 zmsc/2024/32).

## corpus.sqlite

Update blocked by FUSE disk I/O error in this sandbox session
(reproduces the b0504 / b0511 / b0515 mount-blocks symptom). Will
rebuild host-side via `scripts/batch_0504_build_fts5.py`. corpus.sqlite
is gitignored — JSON records are the source of truth.

## ZMSC 2024 status after this tick

- 11 of 34 nums covered (11 written, 5 deferred = 16 attempted).
- 18 nums still untouched (1–18).
- All probed inner nums 19–26 present (no gaps); inventory upper
  boundary remains at 34.
- Recommended next tick: continue ZMSC 2024 with nums {18,17,16,15,14,13,12,11}.

## approvals.yaml

NOT modified — Phase 5 human-only confirmation rule. ZMSC older-year
sweep remains approved per `approvals.yaml.zmsc_older_year_sweep_approved:
true` (already in scope for current ZMSC 2024 work).

## B2 sync

Deferred to host (rclone not in sandbox).
