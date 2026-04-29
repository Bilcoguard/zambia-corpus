# Batch 0354 — Phase 5 ZMCC ingestion (continuation)

**Date (UTC):** 2026-04-29
**Phase:** phase_5_judgments (approved+incomplete)
**Slice:** ZMCC 2023 most-recent-first sweep — continuing after b0353; targeted 2023/{11..4} (8 candidates from the prompt-imposed MAX_BATCH_SIZE).
**Parser version:** 0.3.0 (frozen from b0351/b0352/b0353, byte-identical except for TARGETS slice)
**Fetcher:** dateless canonical URL pattern + DESC walk (frozen from b0353).

## Fetch

Slice 11 → 4 (8 numbers). Two of the eight target slots were empty
gaps in the upstream numbering and resolved as HTTP 404:

  * `2023/11` → 404 (gap; numbering is non-contiguous like 2023/17 and
    the 28/29/30 probes from b0352).
  * `2023/9` → 404 (gap).

The remaining 6 successful items were 2023/{10, 8, 7, 6, 5, 4}. To
stay at the MAX_BATCH_SIZE of 8 written-or-attempted records, the
fetcher continued past the WALK_TO=4 boundary into 2023/{3, 2}, both
of which were also valid and on disk pulled cleanly. Final on-disk
hits this tick: 2023/{10, 8, 7, 6, 5, 4, 3, 2} (8 successful HTML+PDF
pairs — exactly MAX_BATCH_SIZE).

The fetch ran in four sandboxed shards because each bash call is
capped at 45s wall-clock and each successful HTML+PDF fetch costs
~10s (network + 2× 5s rate-limit sleeps):

  * shard 1 (PROBE_FROM=11, MAX_HITS=4): fetched 11 (404), 10 (ok
    pair), 9 (404), 8 (ok pair) — terminated by 45s bash cap before
    log flush. Raw HTML+PDF for 10 and 8 persisted; 11 and 9 404s not
    yet logged.
  * shards 2 & 3 (re-probes of 11 and 9): 1× 404 each, confirming the
    gaps and writing the JSON probe logs.
  * shard 4 (PROBE_FROM=7, MAX_HITS=3): 3× ok (7/6/5).
  * shard 5 (PROBE_FROM=4, MAX_HITS=3): 3× ok (4/3/2).

| Year/# | Date       | HTML bytes | PDF bytes |
|--------|------------|------------|-----------|
| 2023/10 | 2023-09-19 |     54,822 |  1,502,855 |
| 2023/8  | 2023-01-31 |     46,051 |  1,501,914 |
| 2023/7  | 2023-08-03 |     44,507 |    663,432 |
| 2023/6  | 2023-07-31 |     77,057 |  6,468,907 |
| 2023/5  | 2023-06-15 |     48,414 |    473,317 |
| 2023/4  | 2023-03-30 |     47,715 |  4,105,534 |
| 2023/3  | 2023-03-10 |     49,292 |  6,247,863 |
| 2023/2  | 2023-03-02 |     45,305 |    564,874 |

Effective HTTP cost ~20: 8 HTML + 8 PDF + 2 dedicated 404 probes
(11, 9) + 2 shard1-killed pre-timeout 404 probes for the same two
numbers (re-counted because they generated outbound HTTPs even though
the JSON log was lost). All exact byte-counts and SHAs are in
`_work/b0354/fetch_probe_*.json` and the new entries appended to
`provenance.log` and `costs.log`.

Fetcher: `scripts/batch_0354_fetch.py` (byte-identical to b0353 except
for `PROBE_FROM=11`).

## Parse

`scripts/batch_0354_parse.py` (parser_version 0.3.0, frozen from b0353)
wrote **2 records** and **deferred 6**.

### Written

  * `judgment-zm-2023-zmcc-07-zulu-v-chilufya-and-ors`
    — *Zulu v Chilufya and Others* — [2023] ZMCC 7 — decided
    2023-08-03 — outcome `dismissed` (resolved from PRIMARY summary
    regex; pdf-anchor not used) — 3-judge panel (Shilimi DPC presiding,
    Mulonda JJC, Chisunka JJC).
  * `judgment-zm-2023-zmcc-02-mwanza-v-attorney-general`
    — *Mwanza v Attorney General* — [2023] ZMCC 2 — decided
    2023-03-02 — outcome `dismissed` — 5-judge panel (Munalula JCC
    presiding, Sitali JCC, Mulonda JCC, Chisunka JCC, Mulongoti JCC).

### Deferred (no fabrication — per BRIEF.md non-negotiable #1)

All six deferrals are `outcome_not_inferable_under_tightened_policy`.
Raw HTML+PDF remain on disk and can be revisited later if the parser
acquires hand-anchored PDF order paragraphs or the locked summary
regex list is widened (a parser_version bump, not a tick-time change).

  * 2023/10 — *Mwanza and Anor v The Attorney General* — 2023-09-19
  * 2023/8  — *Mwiinde v Attorney General and National Pensions Scheme* — 2023-01-31
  * 2023/6  — 2023-07-31
  * 2023/5  — 2023-06-15
  * 2023/4  — 2023-03-30
  * 2023/3  — 2023-03-10

All six raw pairs remain on disk under
`raw/zambialii/judgments/zmcc/2023/`. No re-fetch will be required when
the parser is widened.

### Hard upstream gaps

  * `2023/11` — HTTP 404 from ZambiaLII (number not assigned upstream).
  * `2023/9`  — HTTP 404 from ZambiaLII (number not assigned upstream).

These are not pending parses; they are confirmed source-side gaps and
will not be retried. Logged in `costs.log` as `kind=probe-404`.

## Integrity (PASS)

`scripts/integrity_check_b0354.py`: **PASS (2 records)** — all 20
required fields present on both records; ID pattern OK; date format OK;
outcome ∈ enum (`dismissed`); court ∈ enum (`Constitutional Court of
Zambia`); judges resolve in `judges_registry.yaml` (Shilimi, Mulonda,
Chisunka, Munalula, Sitali, Mulongoti — all present from prior
batches); ≥1 issue_tag; source_hash and raw_sha256 match raw bytes on
disk; outcome_detail safety checks all green. ID uniqueness check
across `records/judgments/`: no new collisions introduced this tick.

## Notes

- `judges_registry.yaml`: no new canonicals introduced. The aliases
  list for some judges may have been extended by the batch but no
  unseen names appeared.
- corpus.sqlite NOT modified (canonical source-of-truth remains
  `records/*.json`; b0351/b0352/b0353 policy continues; B-tree
  corruption pages 84..99 unchanged).
- B2 sync deferred to host (rclone not in sandbox).
- Phase 5 progress: was 22 before this tick → **24** after this tick
  (target 100–160). Phase remains `approved: true, complete: false`;
  worker does not flip approval flags.
- Next tick: ZMCC 2023 sweep is now functionally complete (all 1..27
  reachable numbers fetched; 9, 11, 17 are PDF-404/HTML-404 hard gaps;
  2023/1 still untouched). Plan: probe 2023/1 then move to ZMCC 2022
  top via dateless URL discovery, continuing under the same
  parser_version 0.3.0 policy.
