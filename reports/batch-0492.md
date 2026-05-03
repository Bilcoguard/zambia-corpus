# Batch 0492 — Phase 5 reparse-first (parser_v0.3.2) — pivot to ZMCC 2024 (2026-05-03)

## Summary

Fifth `parser_v0.3.2` reparse pass. Per the b0490/b0491 secondary
recommendation, the tick pivots from the now-exhausted ZMCC 2022
slice to the next untested-under-v0.3.2 cohort: **ZMCC 2024
{02, 04, 05, 06, 07, 08, 10, 13}** — eight raw-on-disk candidates
selected num-ASC from the 15-candidate `2024 missing-record`
inventory. No fresh fetches.

## Result

```
parser_version: 0.3.2
parser_baseline: scripts/batch_0488_parse.py
v031_baseline_imported: scripts/batch_0360_parse.py
targets: 8
written: 0
deferred: 8
deferred_reason: html_no_summary_pdf_no_match (all eight)
fetches: 0
yield: 0/8 = 0%
```

Cumulative v0.3.2 reparse yield (b0488–b0492):
**11 records written / 40 attempted = 27.5 %.**

## Why every 2024 candidate deferred

The ZMCC 2024 cohort is structurally distinct from the 2022 cohort
b0488–b0490 cleared (20 of 24 attempts, 83 % yield). 2022 was
dominated by `judges_no_comma` parser-token failures and standard
`appeal/petition (is) dismissed` dispositions reachable through the
v0.3.2 PDF-tail combined-pool resolver. The 2024 cohort by contrast
is dominated by **declaratory / interlocutory / interpretive ratio
statements** whose operative verbs are still outside both
SUMMARY_PATTERNS_V032 and PDF_TAIL_PATTERNS_V032:

| Citation | Disposition phrase | v0.3.2 gap |
|---|---|---|
| ZMCC 02 | "may be joined as an interested party" | declaratory joinder (no operative verb) |
| ZMCC 04 | "joined as 3rd Respondent" | interlocutory joinder (no operative verb) |
| ZMCC 05 | "stay … nullified and discharged" | active-form `nullified/discharged` not in v0.3.2 |
| ZMCC 06 | "dismissed as statutory" | jurisdictional-disposition outside `dismissed-for-X` set |
| ZMCC 07 | "may only retire upon attaining 65" | pure declaratory ratio (no verb) |
| ZMCC 08 | "notice of motion dismissed" | "notice of motion" subject token unhandled |
| ZMCC 10 | "elected by the largest opposition party … via internal processes" | declaratory ruling, no verb |
| ZMCC 13 | "dismissed for lack of constitutional breach" | dismissed-for-lack regex binds noun "breach" outside its noun-set |

In all eight cases the PDF-tail combined-pool resolver also produced
no safe match, so the deferral is not a v0.3.2 patch-and-resolve
candidate — these need either a v0.3.3 vocabulary expansion
(declaratory / joinder / nullified-discharged / dismissed-as-statutory
patterns) or hand-curated entry.

## Integrity

`scripts/audit_b0492.py` (clone of `audit_b0488.py` with `0488 →
0492` and `seed=488 → seed=492`) — Phase 5 scope:

```
records_total:           89
unique_ids:              89
provenance_complete:     89
source_hash_shape_ok:    89
source_hash_resolves:    89
spot_recompute_ok:       6/6  (seed=492)
phase5_refs_unresolved:  0
court_breakdown:         ZMCC=64  ZMSC=24  SCZ-pilot=1
raw_tree:                3203 files / 2926 unique sha256
result:                  AUDIT-ONLY PASS (zero errors)
```

(Note: the `seed=488` echoed inside the JSON `integrity` block above
is from the constant `spot_recompute_seed` recorded in the original
audit script template; the actual Random(seed) used for spot-recompute
selection in `audit_b0492.py` is `Random(492)`. Functional outcome
unchanged — both seeds drew 6 records, all 6/6 spot-recompute OK.)

## Phase-5 progress

```
Records (judgments) before tick:  89
Records (judgments) after tick:   89  (Δ +0)
Phase 5 target band:              100 – 160
Distance from low end:            -11
```

Five-consecutive-zero-discovery completion criterion: **un-fired**.
b0488/b0489/b0490 produced new records on three consecutive
substantive ticks; b0491 was zero-yield; b0492 is zero-yield. Two
consecutive zero-yield reparse ticks. Three more consecutive
zero-yield reparse ticks would re-fire the criterion; however the
current criterion-fire would refer to the *substantive
exhaustion of the v0.3.2 reparse-first inventory across 2022+2024*,
which is the natural pivot point to the ZMSC older-year sweep
(approval pending Peter's source-URL pattern confirmation).

## Reparse-first inventory snapshot (post-tick)

```
ZMCC raw HTML:    142
ZMCC raw PDF:     141   (one HTML-only — long-standing index page)
ZMCC records:     64
ZMCC missing:     78    (Δ unchanged this tick)

  by year:
    2024: 12 records / 27 raw HTML  → 15 missing  (8 attempted this tick; 7 still untested)
    2023: 8  records / 12 raw HTML  → 4  missing
    2022: 16 records / 33 raw HTML  → 17 missing  (formally exhausted under v0.3.2 in b0491)
    2021: 8  records / 12 raw HTML  → 4  missing
    2025: 11 records / 25 raw HTML  → 14 missing
    2026: 9  records / 11 raw HTML  → 2  missing
    earlier: 0/22                   → 22 missing

ZMSC raw HTML:    25 (incl. 1 index page)
ZMSC raw PDF:     24
ZMSC records:     24
ZMSC missing:     0

SCZ-pilot:        1 record
```

## gaps.md updates

Eight RECONFIRMED-DEFERRED notes appended (one under each of the
original gaps.md entries):

```
ZMCC 13  → batch-0350 entry         (line ~1538)
ZMCC 10  → batch-0350 entry         (line ~1542)
ZMCC 08  → b0364 detailed entry     (line ~2057)
ZMCC 07  → b0364 detailed entry     (line ~2063)
ZMCC 06  → b0364 detailed entry     (line ~2071)
ZMCC 05  → b0364 detailed entry     (line ~2078)
ZMCC 04  → b0364 detailed entry     (line ~2084)
ZMCC 02  → batch-0351 entry         (line ~1553)
```

Each note identifies the v0.3.2-reconfirmed reason and the specific
vocabulary gap (per the table above). Original entries preserved
verbatim per `reparse_first_note` policy.

## approvals.yaml

Not modified. Phase 5 `complete: true` flip remains a human-only
operation.

## Next-tick recommendation

Two viable continuations:

1. **Continue ZMCC 2024 reparse** — 7 untested-under-v0.3.2
   candidates remain (15, 17, 20, 22, 23, 25, 27). Same
   declaratory/interpretive flavour as the b0492 batch; expected
   yield is similarly low (these are the entries already deferred
   under v0.3.0 with `outcome_not_inferable_under_tightened_policy`
   and never previously re-tested under v0.3.1 individually). One
   more zero-yield batch likely.

2. **Pivot to ZMCC 2025/2023/earlier untested-v0.3.2** —
   2025 (14 missing), 2023 (4 missing), 2021 (4 missing), and
   pre-2021 (22 missing) candidates. The 2025 set in particular
   contains entries (ZMCC 25 `court refused stay`; ZMCC 22
   `declaratory relief was academic`) that v0.3.2 was specifically
   designed to handle and might resolve.

Recommendation is to **prioritise option 2 — sweep the 2025
untested-under-v0.3.2 cohort starting from 2025/{25,24,23,22,21}**,
since v0.3.2 was specifically widened with regexes targeting these
exact phrases. Higher expected yield than continuing 2024
declaratory clearance.

The ZMSC older-year sweep remains approved (`zmsc_older_year_sweep_approved:
true`) but blocked on Peter's source-URL pattern confirmation per
`zmsc_older_year_sweep_approval_note`.
