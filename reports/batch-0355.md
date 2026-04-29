# Batch 0355 — Phase 5 ZMCC ingestion (continuation)

**Date (UTC):** 2026-04-29
**Phase:** phase_5_judgments (approved+incomplete)
**Slice:** ZMCC 2023/1 (closing the 2023 sweep) + ZMCC 2022 top-down
discovery from confirmed top n=34 down to n=28 (8 candidates total —
MAX_BATCH_SIZE).
**Parser version:** 0.3.0 (frozen from b0354, byte-identical except for
TARGETS slice and WORK directory).
**Fetcher:** dateless canonical URL pattern + DESC walk (frozen from
b0354), now parameterised by YEAR.

## Fetch

ZMCC 2023/1 was the only 2023 number not yet attempted. It returned a
clean HTML+PDF pair (date 2023-03-02, same date as 2023/2 — the two
appear to share a release day). After that, the fetcher moved to
ZMCC 2022 starting from a probe-from of 35 walking DESC.

  * `2022/35` → 404 (confirms 2022 top is n=34).
  * `2022/{34, 33, 32, 31, 30, 29, 28}` → all clean HTML+PDF pairs.

Fetch ran across four sandboxed shards because each bash call is
capped at 45s wall-clock and each successful HTML+PDF fetch costs
~10s (network + 2× 5s rate-limit sleeps):

  * shard 1 (YEAR=2023, PROBE_FROM=1, MAX_HITS=1): fetched 2023/1.
  * shard 2 (YEAR=2022, PROBE_FROM=35, MAX_HITS=4): hit 35 (404)
    then 34 (ok pair), terminated by 45s bash cap before 33.
  * shard 3 (YEAR=2022, PROBE_FROM=33, MAX_HITS=3): 33/32/31 (ok pairs).
  * shard 4 (YEAR=2022, PROBE_FROM=30, MAX_HITS=3): 30/29/28 (ok pairs).
  * shard 5 (YEAR=2022, PROBE_FROM=35, WALK_TO=35, MAX_HITS=1): one
    dedicated 404 confirmation for 2022/35 (the shard-2 404 was logged
    in JSON but not flushed to costs.log because shard-2 timed out
    before its tail; this shard re-confirms it cleanly).

| Year/# | Date       | HTML bytes | PDF bytes |
|--------|------------|------------|-----------|
| 2023/1  | 2023-03-02 |     43,570 |  1,212,961 |
| 2022/34 | 2022-02-15 |     45,315 |  1,285,745 |
| 2022/33 | 2022-05-05 |     45,804 |  2,775,345 |
| 2022/32 | 2022-07-15 |     46,149 |    596,297 |
| 2022/31 | 2022-01-19 |     44,300 |  1,121,725 |
| 2022/30 | 2022-11-11 |     42,665 |    514,102 |
| 2022/29 | 2022-05-16 |     45,762 |    585,922 |
| 2022/28 | 2022-01-26 |     48,455 |    815,725 |

Effective HTTP cost: 8 HTML + 7 PDF + 2× 404 probes for 2022/35
(one shard-2 probe + one dedicated re-confirmation in shard-5) +
1× 404 probe attempted by shard-2 before shard-3 took over (no
duplicate to costs.log because shard-2 tail was lost) = 17 successful
fetches on disk, ~15 fresh fetches recorded in costs.log this tick.
All exact byte-counts and SHAs are in `_work/b0355/fetch_y*_probe_*.json`
and the new entries appended to `provenance.log` and `costs.log`.

Fetcher: `scripts/batch_0355_fetch.py` (parameterised; same fetch_one
core as b0354).

## Parse

Records written: **3** (well above the b0353/b0354 zero-yield ticks).

| ID | Citation | Outcome | Date | Source |
|----|----------|---------|------|--------|
| `judgment-zm-2023-zmcc-01-yamba-v-principal-resident-magistrate` | [2023] ZMCC 1 | dismissed | 2023-03-02 | summary |
| `judgment-zm-2022-zmcc-29-chisanga-v-chisopa-and-anor` | [2022] ZMCC 29 | dismissed | 2022-05-16 | summary |
| `judgment-zm-2022-zmcc-28-kolala-v-zambia-postal-services-corporation` | [2022] ZMCC 28 | dismissed | 2022-01-26 | pdf-anchor:"the following orders" |

Records deferred (5): 2022/{34, 33, 32, 31, 30} — all
`outcome_not_inferable_under_tightened_policy`. Summary heads logged
to `gaps.md` for re-parse without re-fetch.

## Integrity

`scripts/integrity_check_b0355.py` PASS:
  * 3/3 unique IDs (globally checked across `records/judgments/**`).
  * 3/3 records have all 20 required fields.
  * 3/3 outcome ∈ enum; 3/3 court ∈ enum.
  * 3/3 ≥1 judge resolves in `judges_registry.yaml`; 3/3 judges[*].role
    ∈ enum.
  * 3/3 ≥1 issue_tag (from Flynote where present, else case-name fallback).
  * 3/3 source_hash matches raw HTML on disk; 3/3 raw_sha256 matches
    raw PDF on disk.
  * 3/3 ID matches locked pattern; 3/3 date_decided matches YYYY-MM-DD.
  * 3/3 outcome_detail safety green (no blacklist substrings, ≥12
    alphabetic chars, no leading lowercase fragment).

## Judges registry

No new canonicals added. All judges identified in this batch
(Munalula, Sitali, Musaluke, Chisunka, Mulonda, Chitabo, Mulongoti)
already present from prior batches; alias-extension only as needed.

## SQLite

`corpus.sqlite` not modified this tick. Pre-existing B-tree corruption
(pages 84..99) remains; canonical source-of-truth remains
`records/*.json` (b0351..b0354 policy continues).

## Budget

Cumulative today: 244 → ~259/2000 fetches (~13.0%). Tokens within
budget. B2 sync deferred to host (rclone not in sandbox).

## Phase 5 progress

24 + 3 = **27 / 100–160** ZMCC judgments ingested this phase.

  * ZMCC 2026 ingested: per prior batches (count maintained in
    Phase 5 ledger).
  * ZMCC 2025 ingested: per prior batches.
  * ZMCC 2024 ingested: per prior batches.
  * ZMCC 2023 ingested: {1, 2, 7, 22} (+1 this tick).
  * ZMCC 2022 ingested: {28, 29} (+2 this tick — first 2022 records).
  * ZMCC 2023 deferred (raw on disk): {3, 4, 5, 6, 8, 10, 12, 13, 14,
    15, 16, 18, 19, 20, 21, 23, 24, 25, 26, 27}.
  * ZMCC 2022 deferred (raw on disk): {30, 31, 32, 33, 34}.
  * ZMCC 2023/17 = HTML on disk only (PDF-404 hard gap).
  * ZMCC 2023/{9, 11} = HTTP 404 upstream (hard gaps).
  * ZMCC 2022/35 = HTTP 404 upstream (top-of-year sentinel).

## Next tick

Continue ZMCC 2022 sweep DESC from 27 backwards under the same
parser_version 0.3.0 policy. ZMCC 2022/35 confirmed 404 (do not
re-attempt). Same MAX_BATCH_SIZE=8 cap.
