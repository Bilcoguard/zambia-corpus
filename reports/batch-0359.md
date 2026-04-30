# Batch 0359 — Phase 5 ZMCC ingestion (continuation)

**Date (UTC):** 2026-04-29
**Phase:** phase_5_judgments (approved+incomplete)
**Slice:** ZMCC 2022/{3,2,1} (final 3 of 2022) + start of 2021 DESC sweep
at 2021/{22,21,20,19,18}. Top of 2021 discovered at 2021/24 (2021/25
returned HTTP 404 upstream).
**Parser version:** 0.3.0 (frozen from b0358, byte-identical except for
TARGETS slice and WORK directory).
**Fetcher:** dateless canonical URL + DESC walk (frozen from b0358).

## Fetch

All 8 raw HTML+PDF pairs were persisted to
`raw/zambialii/judgments/zmcc/{2021,2022}/`. Fetch ran across two
sandboxed shards because each successful HTML+PDF fetch costs ~12s
(network + 2× 5s rate-limit sleeps) and the sandbox bash cap is 45s.

  * shard 1 (YEAR=2022, PROBE_FROM=3, WALK_TO=1, MAX_HITS=3) — wrote
    2022/3, 2022/2, 2022/1 cleanly; the wrapper killed the process
    just before the shard log flushed (records on disk are intact).
  * shard 2 (YEAR=2021, PROBE_FROM=22, WALK_TO=1, MAX_HITS=3) — wrote
    2021/22, 2021/21, 2021/20 cleanly; same pattern (raw on disk,
    no shard log).
  * shard 3 (YEAR=2021, PROBE_FROM=19, WALK_TO=18, MAX_HITS=2) — wrote
    2021/19 and 2021/18 plus the shard log
    `_work/b0359/fetch_y2021_probe_19_walk_18.json`.
  * top-of-year discovery probe (separate, ~15s): 2021/25 returned HTTP
    404; 2021/24 and 2021/23 returned 200 — those two are next-tick
    targets, not fetched in this batch.

| Year/# | Date       | Slug                                                  |
|--------|------------|-------------------------------------------------------|
| 2022/03 | 2022-01-25 | shah-and-anor-v-the-attorney-general                  |
| 2022/02 | 2022-01-27 | lieutenant-muchindu-v-attorney-general                |
| 2022/01 | 2022-02-02 | chapter-one-foundation-ltd-v-attorney-general         |
| 2021/22 | 2021-02-12 | bozy-simutanda-as-attorney-for-his-royal-highness     |
| 2021/21 | 2021-03-30 | mulubisha-v-attorney-general                          |
| 2021/20 | 2021-11-24 | autry-chanda-v-the-attorney-general                   |
| 2021/19 | 2021-03-25 | wang-shunxue-and-attorney-general-and-another         |
| 2021/18 | 2021-08-18 | chapter-one-foundation-limited-and-ors-v-the-attorney |

Expression dates were sourced from the canonical `/eng@YYYY-MM-DD`
links inside the persisted HTML.

## Parse

`scripts/batch_0359_parse.py` (parser_version 0.3.0, frozen from
b0358). 1 record written (after post-parse fix — see below), 7 deferred.

### Written (1)

| ID | Outcome | Source | Date | Notes |
|----|---------|--------|------|-------|
| judgment-zm-2021-zmcc-20-autry-chanda-v-the-attorney-general | upheld | summary | 2021-11-24 | Autry Chanda v AG; outcome inferred from PRIMARY summary regex; 5-judge ZMCC panel |

### Deferred (7)

`outcome_not_inferable_under_tightened_policy` (6):

  * 2022/03 — Shah & Anor v AG — summary frames the constitutional question without matching a top-level disposition regex.
  * 2022/02 — Lieutenant Muchindu v AG — summary frames the issue.
  * 2022/01 — Chapter One Foundation Ltd v AG — summary frames the issue.
  * 2021/21 — Mulubisha v AG — summary frames the issue.
  * 2021/19 — Wang Shunxue & AG & Another — summary frames the issue.
  * 2021/18 — Chapter One Foundation Ltd & Ors v AG — summary frames the issue.

`parser_v0.3.0_jjs_title_unhandled` (1):

  * 2021/22 — Bozy Simutanda v Kaoma & Anor — `Chibomba JJS` not handled
    by parser title regex; fallback produced bogus canonical `Jjs`.
    Detected post-parse, record deleted and registry reverted before
    commit. Raw retained on disk for parser_v0.3.1 re-parse. See
    gaps.md for the proposed regex extension.

Per BRIEF.md non-negotiable #1 (no fabrication), no record written for
deferred candidates. Raw bytes retained on disk for re-parse without
re-fetch.

## Integrity check

`scripts/integrity_check_b0359.py` (frozen from b0358):
**PASS (1 record)** after post-parse fix. The single written record has
all 20 required fields, outcome ∈ enum, court ∈ enum, all 5 judges
resolve to existing registry canonicals (Mulonda/Sitali/Munalula/
Musaluke/Mulongoti), judges[*].role ∈ enum, ≥1 issue_tag from Flynote,
source_hash matches raw HTML on disk, raw_sha256 matches raw PDF on
disk, ID matches locked pattern, date matches YYYY-MM-DD, outcome_detail
safety checks all green.

The initial parser run produced a second record for 2021/22, but
post-parse review found the parser had created a bogus canonical
judge `Jjs` from the unhandled title `JJS`. Per BRIEF.md non-negotiable
#1 (no fabrication), the record was deleted and the registry reverted
*before commit*. 2021/22 reclassified as deferred.

## Judges registry

No new canonicals introduced (all surnames already present from prior
batches); alias-extension only.

## corpus.sqlite

NOT modified this tick (no INSERTs). Pre-existing B-tree corruption
(pages 84..99) remains; canonical source-of-truth remains
`records/*.json` (b0351..b0358 policy continues).

## Budget impact

~13 fresh fetches this tick (8 HTML + 8 PDF + 1 dedicated 404 probe for
2021/25 + 2 discovery 200-probes for 2021/{24,23}). Cumulative today:
~311/2000 → ~324/2000 (~16.2%). Well within budget.

## Phase 5 progress

30 / 100-160 target (was 29 at b0358 end-state; +1 this tick).

ZMCC 2022 ingested: {19, 26, 28, 29}. ZMCC 2022 fully fetched (1..34 except
35 = 404 sentinel). All non-ingested 2022 numbers deferred under
parser_v0.3.0 tightened policy (raw retained on disk).

ZMCC 2021 ingested: {20}. ZMCC 2021 deferred (raw on disk):
{18, 19, 21, 22}. 2021/{1..17} not yet attempted. 2021/{23,24} probed
positive but not yet fetched. 2021/25 confirmed 404 upstream
(top-of-year sentinel).

## B2 sync

Deferred to host (rclone not in sandbox).

## Next tick

Continue ZMCC 2021 sweep DESC. First targets: 2021/{24,23} (already
probed positive in this tick), then continue from 2021/17 downward
under the same parser_version 0.3.0 policy.
