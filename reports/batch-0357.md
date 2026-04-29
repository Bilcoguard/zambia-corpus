# Batch 0357 — Phase 5 ZMCC ingestion (continuation)

**Date (UTC):** 2026-04-29
**Phase:** phase_5_judgments (approved+incomplete)
**Slice:** ZMCC 2022/{19..12} — 8 candidates, continuation of 2022 DESC
sweep after b0356 ingested 2022/{27..20}.
**Parser version:** 0.3.0 (frozen from b0356, byte-identical except for
TARGETS slice and WORK directory).
**Fetcher:** dateless canonical URL + DESC walk (frozen from b0356).

## Fetch

All 8 raw HTML+PDF pairs for 2022/{19..12} were persisted to
`raw/zambialii/judgments/zmcc/2022/`. Fetch ran across three sandboxed
shards plus two targeted refetches because each successful HTML+PDF
fetch costs ~10s (network + 2× 5s rate-limit sleeps) and the sandbox
bash cap is 45s:

  * shard 1 (PROBE_FROM=19, WALK_TO=17, MAX_HITS=3) → wrote 19 and
    18 cleanly; HTML for 17 written, PDF for 17 not flushed before
    the 45s kill.
  * targeted refetch for 2022/17 PDF → first attempt at the
    redirect-target date (`@2022-09-21`) returned HTTP 404 upstream;
    second attempt at the in-page canonical date (`@2022-08-31`)
    returned HTTP 200, ~15.9 MB. Hard ZambiaLII quirk: the dateless
    URL 302-redirects to a "latest expression" date for the HTML
    that does not have a `source.pdf` companion; the original
    expression date does. To keep HTML and PDF aligned at the same
    expression, the HTML was re-fetched at `@2022-08-31` (45,097 B,
    sha256 `051e08…`) and the original `@2022-09-21` HTML was
    overwritten in place. Note this for future ticks: a 404 on
    `source.pdf` at a redirected expression date is not a hard gap
    — try the canonical in-page expression first.
  * shard 2 (PROBE_FROM=16, WALK_TO=14, MAX_HITS=3) → wrote 16, 15,
    and the HTML for 14; PDF for 14 not flushed before the 45s kill.
  * targeted refetch for 2022/14 PDF → completed cleanly at the
    in-page canonical date `@2022-08-03` (~41.1 MB).
  * shard 3 (PROBE_FROM=13, WALK_TO=12, MAX_HITS=2) → completed
    cleanly. Both HTML+PDF for 13 and 12 written.

| Year/# | Date       | Slug                                             |
|--------|------------|--------------------------------------------------|
| 2022/19 | 2022-09-20 | tembo-suing-in-his-capacity-as-party-president-of |
| 2022/18 | 2022-09-07 | malanji-and-anor-v-attorney-general-and-anor      |
| 2022/17 | 2022-08-31 | zimba-v-attorney-general                          |
| 2022/16 | 2022-08-25 | malanji-and-anor-v-attorney-general-and-anor      |
| 2022/15 | 2022-07-29 | mutelo-k-v-kang-ombe-and-anor                     |
| 2022/14 | 2022-08-03 | malanji-v-mulenga-and-anor                        |
| 2022/13 | 2022-07-28 | lusambo-v-kanengo-and-anor                        |
| 2022/12 | 2022-06-20 | banda-v-attorney-general                          |

## Parse

`scripts/batch_0357_parse.py` (parser_version 0.3.0, frozen from
b0356). 1 record written, 7 deferred under the same tightened-policy
filter that has governed all parser-only ticks since b0344.

Written:
  * `judgment-zm-2022-zmcc-19-tembo-suing-in-his-capacity-as-party-president-of`
    — outcome `dismissed` (PRIMARY summary regex match). Date
    2022-09-20. Single-judge head (Mulongoti JCC) on the summary;
    `outcome_detail` = "Petition dismissed for failure to plead the
    specific constitutional contravention; Court did not decide
    whether re-payment of nomination fees was permissible".

Deferred under `outcome_not_inferable_under_tightened_policy` (raw
HTML+PDF retained on disk; will be re-considered if the parser policy
is loosened or a higher-version parser is adopted):
  * 2022/18 — Malanji & Anor v AG & Anor — summary frames the
    constitutional question; no single regex pattern matches a
    top-level disposition.
  * 2022/17 — Zimba v AG — summary frames the legal question
    without explicit disposition.
  * 2022/16 — Malanji & Anor v AG & Anor — summary frames the
    constitutional issue.
  * 2022/15 — Mutelo K v Kang'ombe & Anor — summary states findings
    without a top-level disposition match.
  * 2022/14 — Malanji v Mulenga & Anor — summary states findings.
  * 2022/13 — Lusambo v Kanengo & Anor — summary frames the legal
    question.
  * 2022/12 — Banda v AG — summary frames the legal question.

## Integrity check

`scripts/integrity_check_b0357.py` (frozen from b0356):
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

~19 fresh fetches this tick (8 HTML + 8 PDF + 1 dedicated 404 probe
for 2022/17 `@2022-09-21`/source.pdf + 1 HTML refetch for 2022/17
`@2022-08-31` + 1 PDF refetch for 2022/14). Cumulative today:
~276/2000 → ~295/2000 (~14.8%). Well within budget.

## Phase 5 progress

29 / 100-160 target (was 28 at b0356 end-state; +1 this tick).

ZMCC 2022 ingested so far: {19, 26, 28, 29}.
ZMCC 2022 deferred (raw on disk): {12, 13, 14, 15, 16, 17, 18, 20,
21, 22, 23, 24, 25, 27, 30, 31, 32, 33, 34}.
ZMCC 2022/35 confirmed 404 upstream (top-of-year sentinel).
2022/{11..1} not yet attempted.

## B2 sync

Deferred to host (rclone not in sandbox).

## Next tick

Continue ZMCC 2022 sweep DESC from 11 backwards under the same
parser_version 0.3.0 policy. After 2022 is exhausted, move to
ZMCC 2021 top-of-year discovery (no slot count yet).
