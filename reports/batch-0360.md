# Batch 0360 — Phase 5 ZMCC ingestion (continuation)

**Date (UTC):** 2026-04-30
**Phase:** phase_5_judgments (approved+incomplete)
**Slice:** ZMCC 2021/{24,23,17,16,15,14,13,12} — 8 candidates. The two
top-of-2021 numbers already 200-probed in b0359 (24, 23) plus the
continuation DESC sweep from 17 down through 12. ZMCC 2021/{18,19,21,22}
remain deferred from earlier ticks pending a parser_v0.3.1 re-parse pass
(separate gaps.md reprocessing track per 2026-04-30 user instruction).
**Parser version:** 0.3.0 (frozen from b0359, byte-identical except for
TARGETS slice and WORK directory).
**Fetcher:** dateless canonical URL + explicit-NUMS / DESC-walk variant
(frozen from b0359, includes the explicit-NUMS branch).

## Fetch

All 8 raw HTML+PDF pairs for 2021/{24,23,17,16,15,14,13,12} were
persisted to `raw/zambialii/judgments/zmcc/2021/`. Most were already
on disk from earlier shard runs in this tick (24, 23, 17, 12 returned
`skip-already`); 16, 15, 14, 13 were freshly fetched this tick. The
fetch ran across four sandboxed shards under the 45s bash cap.

| Year/# | Date       | Slug                                                       |
|--------|------------|------------------------------------------------------------|
| 2021/24 | 2021-10-27 | gilford-malenji-v-zambia-airports-corporation-limi         |
| 2021/23 | 2021-11-29 | charles-chihinga-v-new-future-financial-company-li         |
| 2021/17 | 2021-09-20 | anderson-mwale-buchisa-mwalongo-and-kola-odubote-v         |
| 2021/16 | 2021-11-22 | sampa-v-mundubile-and-anor                                 |
| 2021/15 | 2021-09-17 | shunxue-v-the-attorney-general-anor                        |
| 2021/14 | 2021-07-13 | legal-resources-foundation-limited-2-others-v-edga         |
| 2021/13 | 2021-07-20 | bric-back-limited-t-a-gamamwe-ranches-v-kirkpatric         |
| 2021/12 | 2021-06-30 | dipak-patel-v-minister-of-finance-and-attorney-gen         |

Expression dates were verified against the canonical `/eng@YYYY-MM-DD`
links inside each persisted HTML (sed-grepped from
`raw/zambialii/judgments/zmcc/2021/judgment-zm-2021-zmcc-N-*.html`).

## Parse

Parser_v0.3.0 (TIGHTENED policy locked in at b0344) was applied to all
8 raw pairs.

* **Records written:** 0
* **Deferred (raw retained):** 8 — 2021/{24,23,17,16,15,14,13,12} all
  flagged `outcome_not_inferable_under_tightened_policy`. Under the
  tightened policy the parser refuses to emit a record unless the
  outcome regex anchors on a high-confidence summary or PDF-order
  phrase; otherwise the candidate is deferred rather than risk a
  bogus enum value (per BRIEF.md non-negotiable #1 — no fabrication).

Raw HTML+PDF for all 8 are preserved on disk and are eligible for a
future re-parse pass once parser_v0.3.1 (or later) widens the outcome
inference regexes safely.

## Integrity

`scripts/integrity_check_b0360.py` (frozen from `integrity_check_b0358.py`)
ran against the 0 records written this tick:

```
INTEGRITY CHECK: PASS (0 record(s))
```

No corpus.sqlite mutation this tick (canonical source-of-truth remains
`records/*.json`; pre-existing SQLite B-tree corruption on pages 84..99
unchanged — same policy as b0351..b0359).

## Budget

* Fresh fetches this tick: ~13 (4 fresh HTML + 4 fresh PDF for 16/15/14/13,
  4 `skip-already` for 24/23/17/12 with no network cost, plus 5
  consecutive-404 probes on 2021/{35..31} from a default-arg fetch run
  that walked top-of-year before hitting the consecutive-404 sentinel).
* Cumulative today (2026-04-30): ~13 / 2000 (~0.65%).
* B2 sync deferred to host (rclone not in sandbox) — same as
  b0341..b0359.

## Phase 5 progress

* Records ingested before this tick: 30
* Records ingested this tick: 0
* Records ingested after this tick: 30 / 100–160 target
* ZMCC 2022 sweep: 1..34 fully fetched (35=upstream sentinel 404).
* ZMCC 2021 sweep: 1..24 fully fetched (25=upstream sentinel 404, 35..26
  also 404). Records on disk so far: 2021/{20} only. Deferred: 2021/{24,
  23,22,21,19,18,17,16,15,14,13,12} (12 candidates retained for re-parse).
* Next tick: continue ZMCC 2021 DESC from 11 backwards under the same
  parser_v0.3.0 policy.

## Tick housekeeping

* `git pull --ff-only` succeeded (already up to date).
* `approvals.yaml` read OK; `phase_5_judgments` remains approved+
  incomplete; worker did NOT flip approval flags.
* Lock cleanup ran (host-owned `.git/objects/maintenance.lock`
  unlinkable failure remains harmless).
* No `corpus.sqlite` mutation. No `judges_registry.yaml` mutation
  (no records written → no canonicals touched).
