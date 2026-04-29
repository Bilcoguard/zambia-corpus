# Batch 0356 — Phase 5 ZMCC ingestion (continuation)

**Date (UTC):** 2026-04-29
**Phase:** phase_5_judgments (approved+incomplete)
**Slice:** ZMCC 2022/{27..20} — 8 candidates, continuation of 2022 DESC
sweep after b0355 ingested 2022/{34..28}.
**Parser version:** 0.3.0 (frozen from b0355, byte-identical except for
TARGETS slice and WORK directory).
**Fetcher:** dateless canonical URL + DESC walk (frozen from b0355).

## Fetch

All 8 raw HTML+PDF pairs for 2022/{27..20} were persisted to
`raw/zambialii/judgments/zmcc/2022/`. No upstream 404s in this slice.
Fetch ran across three sandboxed shards because each successful
HTML+PDF fetch costs ~10s (network + 2× 5s rate-limit sleeps) and the
sandbox bash cap is 45s:

  * shard 1 (YEAR=2022, PROBE_FROM=27, WALK_TO=20, MAX_HITS=8) →
    timed out at the 45s cap after writing 25/26/27. Shard exit was
    a hard kill; the tail-end PDF for 27 was written cleanly because
    the rate-limit sleep was the gating call.
  * shard 2 (YEAR=2022, PROBE_FROM=24, WALK_TO=20, MAX_HITS=8) →
    timed out at the 45s cap after writing 22/23/24 and the HTML for
    21. PDF for 21 had already flushed.
  * shard 3 (YEAR=2022, PROBE_FROM=21, WALK_TO=20, MAX_HITS=2) →
    timed out at the 45s cap mid-PDF for 20; HTML for 21 already on
    disk so this shard's contribution was the HTML for 20 (and a
    partial PDF that did not flush).
  * shard 4 (YEAR=2022, PROBE_FROM=20, WALK_TO=20, MAX_HITS=1) →
    completed cleanly. Re-fetched 20 (HTML+PDF both written; the
    pre-fetch existence check requires both to skip, and the shard-3
    PDF had not flushed). Effective net cost for 20 = 1 HTML refetch
    + 1 PDF fetch.

| Year/# | Date       | Slug                                             |
|--------|------------|--------------------------------------------------|
| 2022/27 | 2022-11-10 | sangwa-v-attorney-general                        |
| 2022/26 | 2022-10-21 | michelo-v-sampa-and-anor                         |
| 2022/25 | 2022-10-21 | institute-of-law-policy-research-and-human-rig…  |
| 2022/24 | 2022-10-20 | kanengo-v-attorney-general-and-anor              |
| 2022/23 | 2022-10-17 | sinkamba-and-anor-v-electoral-commission-of-z…   |
| 2022/22 | 2022-09-23 | kachize-phiri-and-anor-v-electoral-commission…   |
| 2022/21 | 2022-09-29 | chilufya-v-ng-andwe-and-anor                     |
| 2022/20 | 2022-09-21 | ndhlovu-and-ors-v-road-development-agency        |

## Parse

`scripts/batch_0356_parse.py` (parser_version 0.3.0, frozen from
b0355). 1 record written, 7 deferred under the same tightened-policy
filter that has governed all parser-only ticks since b0344.

Written:
  * `judgment-zm-2022-zmcc-26-michelo-v-sampa-and-anor` — outcome
    `dismissed` (PRIMARY summary regex match). Date 2022-10-21.
    Single-judge bench (Munalula JCC sole) on the summary head.

Deferred under `outcome_not_inferable_under_tightened_policy` (raw
HTML+PDF retained on disk; will be re-considered if the parser policy
is loosened or a higher-version parser is adopted):
  * 2022/27 — Sangwa v AG ("Court dismisses functus officio
    objection and allows constitutional challenge to section 30
    (costs) to proceed to hearing.") — mixed-outcome summary, no
    single regex pattern can safely classify this.
  * 2022/25 — Institute of Law, Policy Research & Human Rights —
    summary frames the legal question without stating disposition.
  * 2022/24 — Kanengo v AG & Anor — summary frames the legal
    question without stating disposition.
  * 2022/23 — Sinkamba & Anor v ECZ — summary frames the legal
    question.
  * 2022/22 — Kachize-Phiri & Anor v ECZ — summary frames the legal
    question.
  * 2022/21 — Chilufya v Ng'andwe & Anor — summary states a remedy
    ("costs order set aside") but no top-level appeal disposition
    matches the v0.3.0 patterns.
  * 2022/20 — Ndhlovu & Ors v Road Development Agency — summary
    states a finding without disposition.

## Integrity check

`scripts/integrity_check_b0356.py` (frozen from b0355):
**PASS (1 record)**.

  * 1/1 unique IDs, all 20 required fields present
  * outcome ∈ enum, court ∈ enum, judges role ∈ enum
  * ≥1 judge resolves in `judges_registry.yaml`
  * ≥1 issue_tag from Flynote
  * `source_hash` matches raw HTML on disk
  * `raw_sha256` matches raw PDF on disk
  * id matches locked pattern, date matches YYYY-MM-DD
  * `outcome_detail` safety checks all green

## Budget impact

~17 fresh fetches this tick (8 HTML + 8 PDF + 1 PDF refetch for 20).
Cumulative today: ~259/2000 → ~276/2000 (~13.8%). Well within budget.

## Phase 5 progress

28 / 100-160 target (was 27 at b0355 end-state; +1 this tick).

ZMCC 2022 ingested so far: {26, 28, 29}.
ZMCC 2022 deferred (raw on disk): {20, 21, 22, 23, 24, 25, 27, 30,
31, 32, 33, 34}.
ZMCC 2022/35 confirmed 404 upstream (top-of-year sentinel).
2022/{19..1} not yet attempted.

## B2 sync

Deferred to host (rclone not in sandbox).

## Next tick

Continue ZMCC 2022 sweep DESC from 19 backwards under the same
parser_version 0.3.0 policy.
