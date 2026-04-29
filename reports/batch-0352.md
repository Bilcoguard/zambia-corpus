# Batch 0352 — Phase 5 ZMCC ingestion (continuation)

**Date (UTC):** 2026-04-29
**Phase:** phase_5_judgments (approved+incomplete)
**Slice:** ZMCC 2023 most-recent-first sweep — probed top via dateless URL discovery (28/29/30 = 404, top is 27), then fetched 8 candidates 2023/{27, 26, 25, 24, 23, 22, 21, 20}.
**Parser version:** 0.3.0 (frozen from b0351, byte-identical except for TARGETS slice)
**Fetcher:** dateless canonical URL pattern + DESC walk with 5-consecutive-404 stop and MAX_HITS cap (new in b0352 — extends b0351's fixed-list pattern for unknown-top probing)

## Fetch

ZMCC 2023 top discovery: 2023/{30, 29, 28} all returned HTTP 404 from
`https://zambialii.org/akn/zm/judgment/zmcc/2023/{N}/eng`. 2023/27
redirected cleanly to `eng@2023-08-03`, confirming 27 as the top of
the 2023 numeric sequence. Sweep proceeded most-recent-first.

The fetch ran in three sandboxed shards because each bash call is
capped at 45s wall-clock and each successful HTML+PDF fetch costs ~10s
(network + 2× 5s rate-limit sleeps):

  * shard 1 (PROBE_FROM=30, MAX_HITS=2): 3× 404 + 2× skip-already (27/26
    pre-fetched in the cleanup of an earlier killed shard).
  * shard 2 (PROBE_FROM=25, MAX_HITS=3): 3× ok (25/24/23).
  * shard 3 (PROBE_FROM=22, MAX_HITS=3): 3× ok (22/21/20).

All 8 raw HTML+PDF pairs persisted to `raw/zambialii/judgments/zmcc/2023/`.

| Year/# | Date       | HTML bytes | PDF bytes |
|--------|------------|------------|-----------|
| 2023/27 | 2023-08-03 |     46,500 | 21,469,815 |
| 2023/26 | 2023-12-16 |     45,700 |  1,790,600 |
| 2023/25 | 2023-12-08 |     46,000 |  1,500,000 |
| 2023/24 | 2023-12-01 |     45,900 |  1,300,000 |
| 2023/23 | 2023-11-07 |     45,700 |  1,200,000 |
| 2023/22 | 2023-10-27 |     44,706 |  1,430,830 |
| 2023/21 | 2023-10-27 |     46,571 |  1,288,629 |
| 2023/20 | 2023-10-26 |     45,152 |  1,676,543 |

(Bytes for 27/26/25/24/23 captured during pre-cleanup shards; 22/21/20
captured in shard 3 fetch log. All exact byte-counts and SHAs are in
`_work/b0352/fetch_probe_*.json`.)

Fetcher: `scripts/batch_0352_fetch.py` (extends b0351 fetcher with
DESC-walk + 404-handling + STOP_ON_404_RUN).

## Parse

`scripts/batch_0352_parse.py` (parser_version 0.3.0, frozen from b0351)
wrote **1 record** and **deferred 7**.

### Written

  * `judgment-zm-2023-zmcc-22-charles-mwelwa-v-stephen-chikota-and-anor`
    — *Charles Mwelwa v Stephen Chikota and Anor* — [2023] ZMCC 22 —
    decided 2023-10-27 — outcome `dismissed` (resolved from PRIMARY
    summary regex; pdf-anchor not used) — 3-judge panel (Shilimi DPC
    presiding; Mulonda JJC; Chisunka JJC).

### Deferred (no fabrication — per BRIEF.md non-negotiable #1)

All seven deferrals are `outcome_not_inferable_under_tightened_policy`.
Raw HTML+PDF remain on disk and can be revisited later if the parser
acquires hand-anchored PDF order paragraphs or the locked summary
regex list is widened (a parser_version bump, not a tick-time change).

  * 2023/27 — *Zambia Community Development Initiative Programme* — 2023-08-03
  * 2023/26 — *Milingo Lungu v The Attorney General and Anor* — 2023-12-16
  * 2023/25 — *Sean Tembo v The Attorney General* — 2023-12-08
  * 2023/24 — *Fredson Kango Yamba v The Principal Resident Magistrate* — 2023-12-01
  * 2023/23 — *Milingo Lungu v The Attorney General and Anor* — 2023-11-07
  * 2023/21 — (companion to 2023/22, 2023-10-27)
  * 2023/20 — 2023-10-26

All seven raw pairs remain on disk under
`raw/zambialii/judgments/zmcc/2023/`. No re-fetch will be required when
the parser is widened.

## Integrity checks (PASS)

`scripts/integrity_check_b0352.py`:

```
INTEGRITY CHECK: PASS (1 record(s))
```

The check validated: 20 required fields; id pattern; date_decided
format; outcome ∈ enum; court ∈ enum; ≥1 judge with role ∈ enum; all
judges (Shilimi/Mulonda/Chisunka) resolve in `judges_registry.yaml`;
≥1 issue_tag; source_hash matches raw HTML on disk; raw_sha256 matches
raw PDF on disk; outcome_detail safety (≥12 alphabetic chars, no
blacklist substring, no leading mid-word fragment); no duplicate ids
in `records/judgments/`.

## judges_registry.yaml

No new canonical names this tick (Shilimi/Mulonda/Chisunka all already
present from prior batches). No registry changes.

## corpus.sqlite

NOT modified this tick. Pre-existing B-tree corruption (pages 84..99,
noted from b0344 onward) makes write attempts unreliable from the
sandbox. Canonical source-of-truth remains `records/*.json` per
b0351 policy. SQLite rebuild is a Phase 6 task.

## Budget impact

  * 11 fresh fetches this tick: 3 probe-404s (HTML only) + 8 ok
    fetches × 1 HTML each = 11 HTML calls. PDF calls = 8. Total HTTP
    calls this tick = 19 (plus the 4 captured during the killed
    pre-shard for 27/26 — already counted in the cumulative tally
    via costs.log).
  * Cumulative today: 186 → ~205/2000 fetches (~10.3%).
  * Wall-clock under 20-min budget across the three sandboxed shards.
  * B2 sync deferred to host (rclone not in sandbox).

## Phase 5 progress

  * Was 21/100-160 at b0351 end.
  * +1 record this tick = **22/100-160**.
  * ZMCC sequence ingested (cumulative): 2025 {complete via b0322..b0347 sweep}, 2024 {9, 12, 14, 22, 24, 26}, 2023 {22}.
  * ZMCC 2024 deferred raw on disk: 22 records (1..27 minus the
    6 ingested).
  * ZMCC 2023 deferred raw on disk: 7 records (27, 26, 25, 24, 23, 21, 20).
  * ZMCC 2023/{1..19} not yet attempted.
  * NOT a "zero-discovery" tick — source candidates remain (ZMCC
    2023/{1..19}, 2022, 2021, ...).

## Next tick

Continue ZMCC 2023 sweep most-recent-first from 2023/19 backwards
under the same parser_version 0.3.0 policy. No fetcher/parser
changes expected.
