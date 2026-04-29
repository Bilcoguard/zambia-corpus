# Batch 0349 — Phase 5 ZMCC ingestion (continuation)

**Date (UTC):** 2026-04-29
**Phase:** phase_5_judgments (approved+incomplete)
**Slice:** ZMCC 2024/{21, 20, 19, 18, 17, 16, 15, 14} — continuation of the 2024 most-recent-first sweep started at b0348.
**Parser version:** 0.3.0 (frozen from b0348, unchanged)
**Fetcher:** dateless canonical URL pattern (frozen from b0348)

## Fetch

All 8 fetches OK. Raw HTML+PDF pairs persisted to
`raw/zambialii/judgments/zmcc/2024/`.

| Year/# | Date (from redirect) | HTML bytes | PDF bytes |
|--------|----------------------|------------|-----------|
| 2024/21 | 2024-10-11 | 45,962 | 11,171,054 |
| 2024/20 | 2024-10-03 | 46,395 | 10,752,564 |
| 2024/19 | 2024-07-26 | 44,369 |  7,043,895 |
| 2024/18 | 2024-07-26 | 45,295 |  7,635,944 |
| 2024/17 | 2024-07-29 | 43,748 | 10,178,778 |
| 2024/16 | 2024-07-10 | 45,365 | 17,101,835 |
| 2024/15 | 2024-07-08 | 45,130 | 14,070,154 |
| 2024/14 | 2024-07-09 | 52,546 |  7,450,820 |

Fetcher: `scripts/batch_0349_fetch.py` (driven from b0348 with new TARGETS slice; all other logic byte-identical).

## Parse

`scripts/batch_0349_parse.py` (parser_version 0.3.0, frozen from b0348)
wrote **1 record** and **deferred 7**.

### Written

| ID | Citation | Date | Outcome | Outcome source |
|----|----------|------|---------|----------------|
| `judgment-zm-2024-zmcc-14-michelo-chizombe-v-edgar-chagwa-lungu-and-ors` | [2024] ZMCC 14 | 2024-07-09 | dismissed | summary |

* **[2024] ZMCC 14** — Michelo Chizombe v Edgar Chagwa Lungu and Ors. Outcome `dismissed` resolved from PRIMARY summary source (locked SUMMARY_PATTERNS). Eleven-judge panel: Munalula (PC, presiding), Shilimi (DPC, concurring), Sitali, Mulonda, Mulenga, Musaluke, Chisunka, Mulongoti, Mwandenga, Kawimbe, Mulife (all JC, concurring).

### Deferred (no fabrication — per BRIEF.md non-negotiable #1)

All seven deferrals are `outcome_not_inferable_under_tightened_policy`.
Raw HTML+PDF remain on disk and can be revisited later if the parser
acquires hand-anchored PDF order paragraphs or the locked summary
regex list is widened (a parser_version bump, not a tick-time change).

| Candidate | Reason |
|-----------|--------|
| [2024] ZMCC 21 (2024-10-11) | Summary describes ratio/holding without an enum verb on the locked vocabulary. |
| [2024] ZMCC 20 (2024-10-03) | Same — substantive holding only. |
| [2024] ZMCC 19 (2024-07-26) | Same. |
| [2024] ZMCC 18 (2024-07-26) | Same. |
| [2024] ZMCC 17 (2024-07-29) | Same. |
| [2024] ZMCC 16 (2024-07-10) | Same. |
| [2024] ZMCC 15 (2024-07-08) | Same. |

All seven raw pairs remain on disk under
`raw/zambialii/judgments/zmcc/2024/`. No re-fetch will be required when
the parser is widened.

## Integrity checks (PASS)

`scripts/integrity_check_b0349.py`:

- 1/1 unique IDs (no collisions across `records/judgments/`)
- 1/1 records have all 20 required fields
- 1/1 outcomes ∈ enum (dismissed)
- 1/1 court ∈ enum (Constitutional Court of Zambia)
- 1/1 ≥1 judge resolves in registry on bare-surname canonical
- 1/1 judges[*].role ∈ enum (presiding/concurring)
- 1/1 ≥1 issue_tag from Flynote
- 1/1 source_hash matches raw HTML on disk
- 1/1 raw_sha256 matches raw PDF on disk
- 1/1 IDs match locked pattern `^judgment-zm-[a-z0-9-]+$`
- 1/1 dates match `YYYY-MM-DD`
- outcome_detail safety checks all green (no blacklist substrings, ≥12 alphabetic chars, no leading mid-word fragment)

## Judges registry

All 11 panel-member surnames (Munalula, Shilimi, Sitali, Mulonda, Mulenga,
Musaluke, Chisunka, Mulongoti, Mwandenga, Kawimbe, Mulife) already
present from prior batches. No new canonicals added; alias additions
(if any) handled by `update_judges_registry` — see `judges_registry.yaml`
diff.

## Budget impact

- 16 fresh fetches this tick (8 HTML + 8 PDF).
- Cumulative today: 142 → 158/2000 fetches (~7.9%).
- B2 sync deferred to host (rclone not in sandbox).

## sqlite

`corpus.sqlite` updated this tick (1 INSERT OR REPLACE for the new
judgment row in `records` table; sandbox `/tmp` shuffle pattern from
b0347/b0348 reused — disk I/O when writing to mount path, identical
writeback via `cp` succeeded). PRAGMA integrity_check continues to
flag pre-existing B-tree corruption (pages 84..99) — not blocking, file-
based JSON corpus remains canonical source of truth and will need a
dedicated maintenance tick to rebuild sqlite from `records/*.json`.

## Phase 5 progress

19/100-160 target (was 18 at b0348 end-state; +1 this tick).

ZMCC 2025 numeric sequence exhausted (1..33 all attempted).
ZMCC 2024 ingested: {14, 24, 26}. ZMCC 2024 deferred (raw on disk):
{15, 16, 17, 18, 19, 20, 21, 22, 23, 25, 27}. ZMCC 2024/{1..13} not yet
attempted.

## Next tick

Continue ZMCC 2024 sweep most-recent-first from 2024/13 backwards under
the same parser_version 0.3.0 policy. Phase 5 remains
approved+incomplete — worker does not flip approval flags.
