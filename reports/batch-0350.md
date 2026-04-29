# Batch 0350 — Phase 5 ZMCC ingestion (continuation)

**Date (UTC):** 2026-04-29
**Phase:** phase_5_judgments (approved+incomplete)
**Slice:** ZMCC 2024/{13, 12, 11, 10, 9, 8, 7, 6} — continuation of the 2024 most-recent-first sweep started at b0348.
**Parser version:** 0.3.0 (frozen from b0348/b0349, unchanged)
**Fetcher:** dateless canonical URL pattern (frozen from b0348)

## Fetch

All 8 raw HTML+PDF pairs persisted to `raw/zambialii/judgments/zmcc/2024/`.
The first sandbox run of the fetcher (START=0 END=8) timed out partway
through the 09 record (HTML written, PDF not yet attempted). Continued
in two follow-up shards (START=4 END=6 and START=6 END=8); the only
extra cost was one re-fetch of 09's HTML (the script re-fetches when
either side of the HTML+PDF pair is missing on disk). All eight records
ultimately landed cleanly.

| Year/# | Date (from redirect / canonical link) | HTML bytes | PDF bytes |
|--------|---------------------------------------|------------|-----------|
| 2024/13 | 2024-06-28 | 47,012 | 11,560,015 |
| 2024/12 | 2024-06-27 | 53,221 | 14,073,948 |
| 2024/11 | 2024-06-17 | 47,930 |  9,914,512 |
| 2024/10 | 2024-06-25 | 49,408 | 11,378,486 |
| 2024/9  | 2024-04-30 | 44,165 | 11,266,972 |
| 2024/8  | 2024-06-07 | 47,363 |  9,623,279 |
| 2024/7  | 2024-06-06 | 45,261 | 14,675,649 |
| 2024/6  | 2024-04-16 | 49,906 | 15,954,669 |

Dates for 13/12/11/10 were not captured in a fetch log (the
sandbox-timeout run died before log persistence), so they were
recovered post-hoc from the `eng@YYYY-MM-DD` token already embedded in
the saved HTML — no extra HTTP requests, no fabrication. Dates for
9/8/7/6 came from the live 302-redirect during the follow-up shards.

Fetcher: `scripts/batch_0350_fetch.py` (driven from b0349 with new
TARGETS slice; all other logic byte-identical).

## Parse

`scripts/batch_0350_parse.py` (parser_version 0.3.0, frozen from b0349)
wrote **2 records** and **deferred 6**.

### Written

| ID | Citation | Date | Outcome | Outcome source |
|----|----------|------|---------|----------------|
| `judgment-zm-2024-zmcc-12-ronald-kaoma-chitotela-and-ors-v-miles-bwalya-samp` | [2024] ZMCC 12 | 2024-06-27 | dismissed | summary |
| `judgment-zm-2024-zmcc-09-hastie-sibanda-v-attorney-general` | [2024] ZMCC 9 | 2024-04-30 | dismissed | summary |

* **[2024] ZMCC 12** — Ronald Kaoma Chitotela and Ors v Miles Bwalya
  Sampa. Outcome `dismissed` resolved from PRIMARY summary source
  (locked SUMMARY_PATTERNS).
* **[2024] ZMCC 9** — Hastie Sibanda v Attorney General. Outcome
  `dismissed` resolved from PRIMARY summary source.

### Deferred (no fabrication — per BRIEF.md non-negotiable #1)

All six deferrals are `outcome_not_inferable_under_tightened_policy`.
Raw HTML+PDF remain on disk and can be revisited later if the parser
acquires hand-anchored PDF order paragraphs or the locked summary
regex list is widened (a parser_version bump, not a tick-time change).

| Candidate | Reason |
|-----------|--------|
| [2024] ZMCC 13 (2024-06-28) | Summary describes ratio/holding without an enum verb on the locked vocabulary. |
| [2024] ZMCC 11 (2024-06-17) | Same. |
| [2024] ZMCC 10 (2024-06-25) | Same. |
| [2024] ZMCC 8 (2024-06-07) | Same. |
| [2024] ZMCC 7 (2024-06-06) | Same. |
| [2024] ZMCC 6 (2024-04-16) | Same. |

All six raw pairs remain on disk under
`raw/zambialii/judgments/zmcc/2024/`. No re-fetch will be required when
the parser is widened.

## Integrity checks (PASS)

`scripts/integrity_check_b0350.py`:

- 2/2 unique IDs (no collisions across `records/judgments/`)
- 2/2 records have all 20 required fields
- 2/2 outcomes ∈ enum (dismissed)
- 2/2 court ∈ enum (Constitutional Court of Zambia)
- 2/2 ≥1 judge resolves in registry on bare-surname canonical
- 2/2 judges[*].role ∈ enum (presiding/concurring)
- 2/2 ≥1 issue_tag from Flynote
- 2/2 source_hash matches raw HTML on disk
- 2/2 raw_sha256 matches raw PDF on disk
- 2/2 IDs match locked pattern `^judgment-zm-[a-z0-9-]+$`
- 2/2 dates match `YYYY-MM-DD`
- outcome_detail safety checks all green (no blacklist substrings, ≥12 alphabetic chars, no leading mid-word fragment)

## Judges registry

All panel-member surnames already present from prior batches; aliases
re-confirmed where new title strings were observed. No new canonicals
created. Alias additions (if any) handled by `update_judges_registry`
— see `judges_registry.yaml` diff.

## Budget impact

- Effective HTTP fetches this tick: ~17 (8 HTML + 8 PDF, plus one
  wasted re-fetch of 09's HTML caused by the sandbox-timeout in the
  first shard). Counted as 17 in `costs.log` to be honest.
- Cumulative today: 158 → 175/2000 fetches (~8.8%).
- Tokens: well under daily cap (no LLM calls in this tick — pure
  fetch+parse).
- B2 sync deferred to host (rclone not in sandbox).

## sqlite

`corpus.sqlite` updated this tick (2 INSERT OR REPLACE for the new
judgment rows in `records` table; sandbox `/tmp` shuffle pattern from
b0347/b0348/b0349 reused — `cp` to `/tmp/corpus_b0350.sqlite`, INSERT,
`cp` back; verified post-write that both rows are queryable from a
fresh copy of the on-disk file). The pre-existing B-tree corruption
flagged on prior `PRAGMA integrity_check` runs (pages 84..99) is not
blocking — file-based JSON corpus remains canonical source of truth
and will need a dedicated maintenance tick to rebuild sqlite from
`records/*.json`.

## Phase 5 progress

* Records ingested this tick: 2.
* Phase 5 cumulative: 19 → **21 / 100–160** target (was 19 at end of
  b0349; +2 this tick).
* ZMCC 2025 numeric sequence exhausted (1..33 all attempted).
* ZMCC 2024 ingested: {9, 12, 14, 24, 26}. ZMCC 2024 deferred (raw on
  disk): {6, 7, 8, 10, 11, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 25,
  27}. ZMCC 2024/{1..5} not yet attempted.

## Notes / sandbox

`.git/objects/maintenance.lock` was present at tick start (Operation
not permitted to delete via the standard `find .git -name '*.lock'
-delete` step — sandbox can list but not unlink that particular lock).
The pull and subsequent commit succeeded regardless; the lock is
effectively a no-op for the worker's commit path.

The fetcher's sandbox-timeout caused one wasted HTML re-fetch of 09;
no records were corrupted and integrity passed cleanly. Future ticks
should consider sharding the fetch slice into ≤3-record shards if the
PDF sizes look heavy (some of these ConCourt PDFs run 10–17 MB).

## Next tick

Continue ZMCC 2024 sweep most-recent-first from 2024/5 backwards under
the same parser_version 0.3.0 policy (5 records left in the 2024
sequence: 5, 4, 3, 2, 1). After 2024 exhausts, move to ZMCC 2023.
Phase 5 remains approved+incomplete — worker does not flip approval
flags.
