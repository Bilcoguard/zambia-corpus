# Batch 0515 — judgment-ingestion-worker tick

- **Tick UTC**: 2026-05-03T19:17:08Z
- **Worker**: judgment-ingestion-worker (separate budget 500/day)
- **Parser**: v0.3.2 (scripts/batch_0506_zmsc_parse.py wrapping batch_0498_parse.py)

## Scope

Pivoted to ZMSC 2024 sweep per b0511 next-tick recommendation
("ZMSC 2024 sweep recommended next tick (no records on disk; fresh
year highest expected yield)"). Reparse-first inventory remains
formally exhausted under v0.3.2 — the 4 outstanding deferrals
(zmsc/2026/{2,3}, zmsc/2025/{1,5}) are all `html_no_summary_pdf_no_match`
declaratory/leave-to-appeal framings already noted as awaiting parser
v0.3.3 widening (Peter approval pending). Per SKILL most-recent-first
DESC, swept 2024 nums {34,33,32,31,30,29,28,27} after probing the year
boundary at num=35 (404, upper end). Lower nums (1, 10, 30) confirmed
present.

## Year boundary discovery (12 HEAD probes, ~0 KB each)

| num | result |
|----:|--------|
|   1 | 200 → @2024-03-20 |
|  10 | 200 → @2024-04-25 |
|  30 | 200 → @2024-11-08 |
|  32 | 200 → @2024-10-07 |
|  33 | 200 → @2024-07-23 |
|  34 | 200 → @2024-10-04 |
|  35 | **404 — upper boundary confirmed** |
|  40 | 404 |
|  45 | 404 |
|  50 | 404 |
|  70 | 404 |
| 100 | 404 |

Conclusion: ZMSC 2024 inventory ends at num=34 (34 nominal slots,
gaps to be discovered in subsequent ticks).

## Targets (8) — most-recent-first DESC

| # | court | year | num |   date     | result |
|---|-------|------|----:|------------|--------|
| 1 | zmsc  | 2024 |  34 | 2024-10-04 | WRITTEN |
| 2 | zmsc  | 2024 |  33 | 2024-07-23 | WRITTEN |
| 3 | zmsc  | 2024 |  32 | 2024-10-07 | WRITTEN |
| 4 | zmsc  | 2024 |  31 | 2024-10-23 | DEFERRED (`html_no_summary_pdf_no_match`) |
| 5 | zmsc  | 2024 |  30 | 2024-11-08 | WRITTEN |
| 6 | zmsc  | 2024 |  29 | 2024-08-15 | DEFERRED (`html_no_summary_pdf_no_match`) |
| 7 | zmsc  | 2024 |  28 | 2024-08-15 | DEFERRED (`html_no_summary_pdf_no_match`) |
| 8 | zmsc  | 2024 |  27 | 2024-08-07 | WRITTEN |

## Records written (5)

| id | outcome | source | judges |
|----|---------|--------|--------|
| `judgment-zm-2024-zmsc-34-zccm-investments-holdings-plc-v-first-quantum-mine` | dismissed | summary | Mutuna |
| `judgment-zm-2024-zmsc-33-billis-farm-limited-and-anor-v-molosoni-chipabwamb` | allowed | pdf-tail-2pages | Malila, Hamaundu, Chisanga |
| `judgment-zm-2024-zmsc-32-ratoyar-ltd-ors-v-luken-investments-ltd` | allowed | pdf-tail-2pages | Wood, Kabuka, Mutuna |
| `judgment-zm-2024-zmsc-30-finsbury-investments-limited-v-eastern-and-souther` | allowed | pdf-tail-2pages | Mutuna |
| `judgment-zm-2024-zmsc-27-road-development-agency-v-safricas-zambia-limited` | dismissed | pdf-tail-2pages | Malila, Hamaundu, Kaoma, Mutuna, Chisanga |

All 5 written records carry full Phase-5 schema fields: id, type,
jurisdiction, title, citation, court, case_name, case_number,
date_decided, judges (with role/dissented), issue_tags, outcome,
outcome_detail, reasoning_tags (empty), key_statutes (empty),
raw_sha256, source_url, source_hash, fetched_at, parser_version.

## Records deferred (3)

- **zmsc/2024/31** Konkola Copper Mines Plc (in liquidation) v Attorney
  General — `html_no_summary_pdf_no_match`. Summary hints at
  "Whether the Director of Mining Cadastre may grant mining access
  over surface rights without notice, and jurisdictional concerns…" —
  characteristic declaratory-question framing that escapes v0.3.2
  operative-verb pool. Raw HTML+PDF retained on disk.
- **zmsc/2024/29** Faustine Kabwe and Bimal Thaker v Ndola Trust School
  — `html_no_summary_pdf_no_match`. Summary "Whether the Supreme
  Court may entertain applications for leave to appeal despite
  Article 131(2) vesting leave in the Court of Appeal…" — leave-to-
  appeal/jurisdictional family. Raw retained.
- **zmsc/2024/28** Lukasu Properties Limited v African Banking
  Corporation — `html_no_summary_pdf_no_match`. Summary "Failure to
  serve a required demand letter on every defendant renders a writ
  incompetent and cannot be cured by registry…" — interpretive ratio
  framing. Raw retained.

All three are candidates for a future parser v0.3.3 widening pass
(pending Peter approval). They join the standing 4 deferrals from
b0506/0511 → cohort total now 7 deferred raw-on-disk pending v0.3.3.

## Integrity (7-check protocol per SKILL)

7/7 PASS for the 5 written records:

1. ✅ Required fields present on every record
2. ✅ Every record has ≥1 judge (range 1–5 in this batch)
3. ✅ `issue_tags` non-empty on every record (range 6–9 tags)
4. ✅ `outcome` ∈ enum (allowed×3, dismissed×2)
5. ✅ All 13 judge name resolutions match `judges_registry.yaml`
   canonical_name or aliases (Mutuna×4 occurrences, Malila×2,
   Hamaundu×2, Chisanga×2, Wood×1, Kabuka×1, Kaoma×1)
6. ✅ `raw_sha256` matches on-disk PDF for all 5 written records
7. ✅ Zero duplicate IDs across the corpus (111 unique judgment ids
   across `records/judgments/**`)

Batch integrity script: `_work/b0515/integrity.py`. PASS.

## Cohort cumulative (judgment-ingestion-worker since b0504)

| tick | written | deferred | 404 |
|:-----|--------:|---------:|----:|
| b0504/0506 | 5 | 3 | 0 |
| b0511      | 4 | 1 | 3 |
| b0515      | 5 | 3 | 0 |
| **total**  | **14** | **7** | **3** |

Phase 5 corpus judgment count: 102 → 106 (b0511) → 111 (b0515).
Still IN BAND for the Phase 5 target (100–160 landmark judgments).

## Fetches & budget

- HTTP requests this tick:
  - 12 HEAD probes for 2024 boundary discovery (~0 KB each)
  - 16 GET requests for the 8 candidates (HTML + PDF pairs, all 200)
  - **Total: 28 fetches**
- Cumulative judgment-worker today: 37 + 28 = **65/500** (well under
  budget; budget remaining 435).

## judges_registry.yaml

13 alias updates across 8 unique canonical names — all matched
existing entries (Mutuna, Malila, Hamaundu, Chisanga, Wood, Kabuka,
Kaoma). No new canonical names introduced.

## corpus.sqlite

Update blocked by FUSE disk I/O error in this sandbox session
(reproduces the b0504 / b0511 mount-blocks symptom). The script
`_work/b0515/sqlite_update.py` is preserved for host-side replay
via the existing `scripts/batch_0504_build_fts5.py` rebuild path.
sqlite is gitignored — JSON records are the source of truth.

## ZMSC 2024 status after this tick

- 5 of 34 nums covered (5 written, 3 deferred = 8 attempted).
- 26 nums still untouched (1–26 except those probed).
- Inner gaps: not yet enumerated (would need probe campaign).
- Recommended next tick: continue ZMSC 2024 with nums {26,25,24,23,22,21,20,19}.

## approvals.yaml

NOT modified — Phase 5 human-only confirmation rule. ZMSC older-year
sweep remains approved per `approvals.yaml.zmsc_older_year_sweep_approved:
true`.

## B2 sync

Deferred to host (rclone not in sandbox).
