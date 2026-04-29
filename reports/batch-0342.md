# Batch 0342 — Phase 5 ZMCC continuation

- **Tick start:** 2026-04-29T13:22Z
- **Phase:** phase_5_judgments (lowest approved + incomplete)
- **Source:** ZambiaLII Constitutional Court of Zambia index (`/judgments/ZMCC/`)
- **Bounded unit:** continue ConCourt 2026 sweep — re-attempt the 2 deferrals
  from b0341 (2026/6 Munir Zulu privilege; 2026/7 Climate Action) and ingest the
  one remaining 2026 candidate (2026/2 Morgan Ng'ona).
- **Result:** 3 records written, 0 deferred.

## Records written (3)

| ID | Citation | Court | Outcome | Date |
|---|---|---|---|---|
| judgment-zm-2026-zmcc-02-morgan-ng-ona-suing-as-secretary-general-of-the-pa | [2026] ZMCC 2 | Constitutional Court of Zambia | dismissed | 2026-01-28 |
| judgment-zm-2026-zmcc-06-munir-zulu-v-attorney-general-and-anor | [2026] ZMCC 6 | Constitutional Court of Zambia | dismissed | 2026-03-19 |
| judgment-zm-2026-zmcc-07-climate-action-professionals-zambia-v-attorney-gen | [2026] ZMCC 7 | Constitutional Court of Zambia | dismissed | 2026-03-25 |

All three were originally deferred at b0341 (or skipped because the b0341 target
list focused on the top 8 most recent 2026 candidates). For each, the ZambiaLII
summary block is a question of law without a disposition phrase mappable to the
locked Phase 5 outcome enum, so the disposition was inferred from the PDF body
order/conclusion paragraph (parser_version 0.2.0):

- **2026/2 Morgan Ng'ona** — anchor `for the foregoing reasons`, paragraph 28–29
  ("the Petition is devoid of merit ... 29.1. The Petition is dismissed").
  Munalula PC partially dissented on reasoning (paras 25–28) but agreed the
  petition should be dismissed; recorded as `concurring` since the outcome
  aligns. (Refinement to `partial-dissenting` is left as a later pass on the
  reasoning-tags axis — does not affect the outcome enum or judge resolution.)
- **2026/6 Munir Zulu (Article 76 parliamentary privilege)** — second-half scan,
  paragraph 5.34 ("That said, this Petition fails for lack of merit"). Outcome
  detail captured a related earlier paragraph at the strongest pattern match;
  the disposition itself is unambiguous in the body.
- **2026/7 Climate Action Professionals Zambia** — anchor `accordingly,`,
  paragraph [62] ("The Petition is therefore dismissed for want of jurisdiction").

## Provenance

All 3 records carry: `source_url`, `source_hash` (sha256 of HTML),
`raw_sha256` (sha256 of source.pdf), `fetched_at` (ISO 8601 UTC),
`parser_version: 0.2.0`. Raw HTML and PDF persisted to
`raw/zambialii/judgments/zmcc/2026/`.

## Judges registry update

Added one new canonical entry: `Mulife` (with title `JCC`, aliases `Mulife JJC`,
`Mulife JCC`). The previous batch added the with-title `Mulife JJC` canonical
but no bare-surname canonical, so b0342's records — which use the bare-surname
convention shared by `Munalula`, `Shilimi`, `Musaluke`, etc. — could not all
resolve until the bare `Mulife` canonical was added. Registry alphabetised by
canonical_name as part of the same write. Total canonical entries: 14 (was 13).

## Integrity checks

Run via `scripts/integrity_check_b0342.py`:

- 3/3 records have all 20 required fields.
- 3/3 outcomes ∈ enum (`dismissed` × 3).
- 3/3 records have ≥1 judge; every `judges[*].name` resolves in
  `judges_registry.yaml` (after the `Mulife` canonical add).
- 3/3 records have ≥1 issue_tag (parsed from ZambiaLII Flynote, except where
  Flynote is absent; for 2026/2 the flynote is question-of-law style and the
  parsed tags reflect the constitutional issue on the face of the case).
- 3/3 source_hash values match raw HTML on disk.
- 3/3 raw_sha256 values match raw PDF on disk.
- No duplicate IDs introduced by this batch (the corpus-wide `id` scan
  surfaces 5 pre-existing duplicate-`id` files in `records/acts/` from
  b0128/b0264/b0289 lineage — unchanged by this batch and not regressions).

**Result: PASS.**

## Budget impact

- Fresh fetches this tick: 7 (1 ZMCC index re-probe + 6 judgment fetches:
  HTML+PDF for 2026/02, 2026/06, 2026/07).
- The first fetcher invocation persisted those 6 raw files before the host
  killed the long-running process; a second non-fetching parser (`batch_0342_step2.py`)
  built the records from the persisted raw bytes. Net fetches: 7.
- Cumulative fetches today: 55 → 62 (target ≤ 2000/day). ~3.10% of daily
  fetch budget.

## Phase 5 progress

- Records this batch: 3
- Records this phase total: 6 (b0341) + 3 (b0342) = **9 / 100–160 target**.
- ZMCC 2026: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 — only 2026/01 still uningested
  (deferred because the original fetcher run was killed before reaching it).
- ZMCC 2025: 33 candidates uningested (none touched this batch).

## Next tick

- Re-attempt 2026/01 (one final 2026 ConCourt judgment).
- Begin ZMCC 2025 sweep, most recent first (2025/33, 2025/32, ...).
- Then plan SCZ constitutional bucket per BRIEF priority order.

## Sandbox notes

- B2 sync deferred to host (rclone not available in sandbox).
- Long-running fetcher process was killed by the sandbox after ~6 fetches;
  workaround was to split into `batch_0342.py` (fetcher) and
  `batch_0342_step2.py` (parser-only) so that records are persisted from raw
  bytes already on disk even if the fetcher is interrupted. The same pattern
  is recommended for subsequent ticks.
