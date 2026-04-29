# Batch 0358 — Phase 5 ZMCC ingestion (continuation)

**Date (UTC):** 2026-04-29
**Phase:** phase_5_judgments (approved+incomplete)
**Slice:** ZMCC 2022/{11..4} — 8 candidates, continuation of 2022 DESC
sweep after b0357 ingested 2022/19 (1 written, 7 deferred).
**Parser version:** 0.3.0 (frozen from b0357, byte-identical except for
TARGETS slice and WORK directory).
**Fetcher:** dateless canonical URL + DESC walk (frozen from b0357).

## Fetch

All 8 raw HTML+PDF pairs for 2022/{11..4} were persisted to
`raw/zambialii/judgments/zmcc/2022/`. Fetch ran across three sandboxed
shards because each successful HTML+PDF fetch costs ~10s (network +
2× 5s rate-limit sleeps) and the sandbox bash cap is 45s:

  * shard 1 (PROBE_FROM=11, WALK_TO=8, MAX_HITS=4) — wrote 11, 10, 09
    cleanly; the 4th candidate (08) HTML may have been mid-fetch when
    the 42s wrapper timeout fired (no shard log written, but 08 was
    ultimately fetched cleanly in shard 2).
  * shard 2 (PROBE_FROM=8, WALK_TO=5, MAX_HITS=4) — wrote 08, 07, 06
    cleanly; same 42s wrapper kill before flushing 05.
  * shard 3 (PROBE_FROM=5, WALK_TO=4, MAX_HITS=2) — completed cleanly,
    wrote 05 and 04 plus the shard log
    `_work/b0358/fetch_y2022_probe_5_walk_4.json`.

| Year/# | Date       | Slug                                                  |
|--------|------------|-------------------------------------------------------|
| 2022/11 | 2022-05-16 | chisanga-and-anor-v-electoral-commission-of-zambia    |
| 2022/10 | 2022-05-19 | lungu-v-attorney-general-and-ors                      |
| 2022/09 | 2022-03-14 | tembo-suing-in-his-capacity-as-party-president-of     |
| 2022/08 | 2022-04-13 | kafwaya-v-katonga-and-ors                             |
| 2022/07 | 2022-03-22 | law-association-of-zambia-v-attorney-general          |
| 2022/06 | 2022-02-24 | malanji-v-mulenga-and-anor                            |
| 2022/05 | 2022-02-28 | moyo-v-attorney-general                               |
| 2022/04 | 2022-02-25 | chapter-one-foundation-ltd-v-attorney-general         |

Expression dates 2022/{11..6} were sourced from the canonical
`/eng@YYYY-MM-DD` links inside the persisted HTML (verified against the
in-page `Judgment date` field — they agree on every record). 2022/{5,4}
dates came from the live shard 3 redirect.

## Parse

`scripts/batch_0358_parse.py` (parser_version 0.3.0, frozen from
b0357). 0 records written, 8 deferred under the same tightened-policy
filter that has governed all parser-only ticks since b0344.

Deferred under `outcome_not_inferable_under_tightened_policy` (raw
HTML+PDF retained on disk; will be re-considered if the parser policy
is loosened or a higher-version parser is adopted):
  * 2022/11 — Chisanga & Anor v ECZ — summary frames the constitutional
    question without matching a top-level disposition regex.
  * 2022/10 — Lungu v AG & Ors — summary frames the issue.
  * 2022/09 — Tembo (party president) — summary frames the issue.
  * 2022/08 — Kafwaya v Katonga & Ors — summary frames the issue.
  * 2022/07 — Law Association of Zambia v AG — summary frames the issue.
  * 2022/06 — Malanji v Mulenga & Anor — summary frames the issue.
  * 2022/05 — Moyo v AG — summary frames the issue.
  * 2022/04 — Chapter One Foundation Ltd v AG — summary frames the issue.

Per BRIEF.md non-negotiable #1 (no fabrication), no record written.

## Integrity check

`scripts/integrity_check_b0358.py` (frozen from b0357):
**PASS (0 record(s))** — vacuously, no written records to validate.

## Budget impact

~16 fresh fetches this tick (8 HTML + 8 PDF). Cumulative today:
~295/2000 → ~311/2000 (~15.6%). Well within budget.

## Phase 5 progress

29 / 100-160 target (was 29 at b0357 end-state; +0 this tick).

ZMCC 2022 ingested so far: {19, 26, 28, 29}.
ZMCC 2022 deferred (raw on disk): {4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 27, 30, 31, 32, 33, 34}.
ZMCC 2022/35 confirmed 404 upstream (top-of-year sentinel).
2022/{3..1} not yet attempted.

## B2 sync

Deferred to host (rclone not in sandbox).

## Next tick

Continue ZMCC 2022 sweep DESC from 3 to 1 (last 3 candidates of 2022).
After 2022 is exhausted, move to ZMCC 2021 top-of-year discovery
(no slot count yet).
