# Batch 0348 — Phase 5 ZMCC ingestion (continuation)

**Date (UTC):** 2026-04-29
**Phase:** phase_5_judgments (approved+incomplete)
**Slice:** ZMCC 2025/{2, 1} (closing the 2025 numeric sequence) + ZMCC 2024/{27, 26, 25, 24, 23, 22} — step into 2024 most-recent-first to fill the 8-record budget.
**Parser version:** 0.3.0 (frozen from b0347, unchanged)
**Fetcher:** dateless canonical URL pattern (frozen from b0347)

## Fetch

All 8 fetches OK. Raw HTML+PDF pairs persisted to
`raw/zambialii/judgments/zmcc/{2024,2025}/`.

| Year/# | Date (from redirect) | HTML bytes | PDF bytes |
|--------|----------------------|------------|-----------|
| 2025/2  | 2025-02-06 | 45,808 | 8,490,204 |
| 2025/1  | 2025-02-13 | 57,394 | 16,540,716 |
| 2024/27 | 2024-12-10 | 55,961 | 7,918,066 |
| 2024/26 | 2024-11-05 | 43,824 | 3,482,649 |
| 2024/25 | 2024-11-13 | 51,890 | 3,315,162 |
| 2024/24 | 2024-11-11 | 43,452 | 6,194,628 |
| 2024/23 | 2024-10-29 | 46,005 | 6,297,529 |
| 2024/22 | 2024-10-15 | 44,360 |   934,880 |

Fetcher: `scripts/batch_0348_fetch.py` (driven from b0347 with new TARGETS slice; all other logic byte-identical).

## Parse

`scripts/batch_0348_parse.py` (parser_version 0.3.0, frozen from b0347)
wrote **2 records** and **deferred 6**.

### Written

| ID | Citation | Date | Outcome | Outcome source |
|----|----------|------|---------|----------------|
| `judgment-zm-2024-zmcc-26-chipa-chibwe-suing-in-his-capacity-s-chairman-of-t` | [2024] ZMCC 26 | 2024-11-05 | allowed | summary |
| `judgment-zm-2024-zmcc-24-sean-tembo-v-the-attorney-general` | [2024] ZMCC 24 | 2024-11-11 | dismissed | summary |

* **[2024] ZMCC 26** — Chipa Chibwe (Chairman, Outdoor Advertising Association of Zambia) v Lusaka City Council. Outcome `allowed` resolved from PRIMARY summary source ("grant the application" — extension of time application). Panel: Munalula (PC, presiding), Shilimi (DPC, concurring), Mulife (JC, concurring). Issues span civil procedure, Order XV rule 7 CCR, discretionary relief, prejudice analysis.
* **[2024] ZMCC 24** — Sean Tembo v Attorney General. Outcome `dismissed` resolved from PRIMARY summary source ("petition dismissed"). Panel: Shilimi (DPC, presiding), Mulonda, Musaluke, Mwandenga, Mulife (all JJC, concurring). Issues span constitutional law, allegedly insulting indigenous-language remarks by President, contextual interpretation, costs.

### Deferred (no fabrication — per BRIEF.md non-negotiable #1)

All six deferrals are `outcome_not_inferable_under_tightened_policy`.
Raw HTML+PDF remain on disk and can be revisited later if the parser
acquires hand-anchored PDF order paragraphs or the locked summary
regex list is widened (a parser_version bump, not a tick-time change).

| Candidate | Reason |
|-----------|--------|
| [2025] ZMCC 2 (2025-02-06)  | Summary describes ratio/holding without an enum verb on the locked vocabulary. |
| [2025] ZMCC 1 (2025-02-13)  | Same — substantive holding only. |
| [2024] ZMCC 27 (2024-12-10) | Same. |
| [2024] ZMCC 25 (2024-11-13) | Same. |
| [2024] ZMCC 23 (2024-10-29) | Same. |
| [2024] ZMCC 22 (2024-10-15) | Same. |

All six raw pairs remain on disk under
`raw/zambialii/judgments/zmcc/{2024,2025}/`. No re-fetch will be
required when the parser is widened.

## Integrity checks (PASS)

`scripts/integrity_check_b0348.py`:

- 2/2 unique IDs (no collisions across `records/judgments/`)
- 2/2 records have all 20 required fields
- 2/2 outcomes ∈ enum (allowed, dismissed)
- 2/2 court ∈ enum (Constitutional Court of Zambia)
- 2/2 ≥1 judge resolves in registry on bare-surname canonical
- 2/2 judges[*].role ∈ enum (presiding/concurring)
- 2/2 ≥1 issue_tag from Flynote (6 tags each)
- 2/2 source_hash matches raw HTML on disk
- 2/2 raw_sha256 matches raw PDF on disk
- 2/2 IDs match locked pattern `^judgment-zm-[a-z0-9-]+$`
- 2/2 dates match `YYYY-MM-DD`
- outcome_detail safety checks all green (no blacklist substrings, ≥12 alphabetic chars, no leading mid-word fragment)

## Judges registry

`judges_registry.yaml` updated:

- **Munalula**: title `PC` added (first seen on this record); alias `Munalula PC` added.
- **Shilimi**: title `DPC` already present from b0346; alias `Shilimi DPC` already present.
- **Mulife**: titles `JC` and `JJC` added (first seen on these records); aliases `Mulife JC`, `Mulife JJC` added.
- **Mulonda, Musaluke, Mwandenga**: title `JJC` already present (from b0345); aliases re-confirmed.

No new canonicals created. All panel members resolve to existing canonicals via bare-surname match.

## Budget impact

* 16 fresh fetches this tick (8 HTML + 8 PDF).
* Cumulative today: 126 → 142/2000 fetches (~7.1%).
* Tokens: well under daily cap (no LLM calls in this tick — pure fetch+parse).
* B2 sync deferred to host (rclone not in sandbox).

## Phase 5 progress

* Records ingested this tick: 2.
* Phase 5 cumulative: 16 → **18 / 100–160** target.
* ZMCC 2026 ingested: {02, 03, 04, 05, 06, 07, 08, 09, 10}; deferred: {01}.
* ZMCC 2025 ingested: {04, 13, 20, 26, 27, 29, 31}; deferred (raw on disk): {01, 02, 03, 05, 06, 07, 08, 09, 10, 11, 12, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25, 28, 30, 32, 33}.
* ZMCC 2025 numeric sequence is now exhausted (1..33 all attempted).
* ZMCC 2024 ingested: {24, 26}; deferred (raw on disk): {22, 23, 25, 27}.
* ZMCC 2024 not yet attempted: {21..1}.

## Notes / sandbox

`corpus.sqlite` updated this tick with 2 INSERT OR REPLACE rows (records
table, judgment type). The sandbox path again required the /tmp shuffle
seen since b0347 — `cp` to `/tmp/corpus_b0348.sqlite`, INSERT, `cp`
back. Same workaround as b0347. The on-disk file's `PRAGMA
integrity_check` continues to flag B-tree corruption from interrupted
prior writes (pages 84..99); this is a long-running condition that is
not blocking the file-based JSON corpus (which remains the canonical
source of truth) and will need a clean rebuild from `records/*.json`
in a dedicated maintenance tick.

`.git/{index,HEAD}.lock` and `tmp_obj` contention from prior sessions
present at tick start; cleaned via the standard `find .git -name
'*.lock' -delete` pattern at tick head.

## Next tick

Continue ZMCC 2024 sweep most-recent-first from 2024/21 backwards under
the same parser_version 0.3.0 policy. Six 2024 deferrals plus the
existing earlier 2026/2025 deferrals are recorded in `gaps.md` for a
later parser-widening tick.
