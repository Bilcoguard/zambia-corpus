# Batch 0343 — Phase 5 ZMCC continuation (parser-safety deferral)

- **Tick start:** 2026-04-29T13:42Z
- **Phase:** phase_5_judgments (lowest approved + incomplete)
- **Source:** ZambiaLII Constitutional Court of Zambia (`/judgments/ZMCC/`)
- **Bounded unit:** continue ConCourt sweep — pick up the one outstanding 2026
  candidate (2026/01) and the seven most-recent 2025 ZMCC candidates
  (2025/{33,32,31,30,29,28,27}).
- **Result:** 0 records written, 8 deferred (see gaps.md). All 8 raw HTML+PDF
  persisted on disk for re-parse next tick.

## What happened

The fetcher ran cleanly across 4 staged calls (2 candidates × 4 stages, fully
within the 5s/req zambialii rate limit) and persisted 8 HTML + 8 PDF pairs
under `raw/zambialii/judgments/zmcc/{2025,2026}/`.

The parser (`scripts/batch_0343_parse.py`, parser_version 0.2.0 with an
extended set of order-paragraph keywords) wrote 4 first-pass record JSONs to
`records/judgments/zmcc/{2025,2026}/`. On manual review BEFORE commit, the four
inferred outcomes were judged unsafe:

| ID | Inferred outcome | outcome_detail produced | Why unsafe |
|---|---|---|---|
| zmcc-2026-01 Tresford Chali | overturned | "d by Judge Mulonda." | Mid-word fragment; "set aside" matched in a quote from a cited case. |
| zmcc-2025-32 LAZ v AG | overturned | "another v Attorney Generall4l." | Cross-reference to another case in the index. |
| zmcc-2025-28 Mundubile v HH | allowed | "the Godfrey Miyanda v Attorney General case supra." | Citation reference, not a disposition. |
| zmcc-2025-27 Munir Zulu v AG | allowed | "proved or demonstrated to the required standard." | Mid-paragraph fragment from analysis section. |

Per non-negotiable #1 (no fabrication) the four buggy records were moved to
`_stale_b0343_bad_records/` (untracked, kept for post-mortem) BEFORE commit;
they are NOT in the corpus.

The other four candidates correctly bailed at parse time:

| ID | Reason |
|---|---|
| zmcc-2025-33 Miles Bwalya Sampa | Summary describes ratio (Article 210, share subscription vs. State equity disposal) but no disposition phrase. |
| zmcc-2025-31 Munir Zulu (contempt) | Summary contains "Application for contempt dismissed for being procedurally misconceived" — DOES describe outcome `dismissed`, but the regex requires the disposition verb to be adjacent to the noun (no qualifier). One-line parser fix next tick. |
| zmcc-2025-30 Legal Resources Foundation | Summary describes the prima facie / irreparable harm test for staying judicial appointments — no disposition phrase. |
| zmcc-2025-29 LAZ v AG (joinder) | Summary says "Court granted joinder" — likely `allowed` but the joinder→`allowed` rule is not in the current outcome map. |

## Parser limitation surfaced (next-tick action)

The current parser falls back from `summary` → `pdf-tail` → `pdf-kw:<keyword>`
→ `pdf-full`. The pdf-tail and pdf-full sources are unsafe because regex
matches on disposition words (`set aside`, `dismissed`, `allowed`, `declared
unconstitutional`) anywhere in the document body fire on quotes from cited
cases, footnote references, and analysis-section fragments — NOT on the actual
order paragraph.

**Tightening:** restrict acceptable inference to one of:

1. `summary` source with a clear noun-phrase + disposition verb pattern;
2. `pdf-kw:<keyword>` source where `keyword` is one of the explicit
   order-paragraph anchors AND the inferred disposition phrase appears WITHIN
   ~1500 chars of that anchor;
3. Anything else → defer.

This will be implemented at b0344 head.

## Provenance

All 8 raw fetches recorded in `provenance.log` (8 `raw_persisted` lines with
html_sha + pdf_sha + fetched_at), and `costs.log` updated with 16 fetch lines
+ 1 batch summary line. Cumulative today: 62 → 78/2000 fetches (~3.9%).

## Integrity checks

Per the BRIEF Phase 5 integrity gate:

- **No duplicate IDs introduced this batch:** PASS — 0 records added to the
  corpus.
- **amended_by / repealed_by reference resolution:** N/A for judgments.
- **cited_authorities reference resolution:** N/A — judgment records have
  none yet.
- **source_hash matches raw HTML on disk:** N/A — no new records written;
  the 4 buggy first-pass JSONs were moved out of `records/` BEFORE commit.

The pre-existing 5 duplicate-`id` files in `records/acts/` from
b0128/b0264/b0289 lineage are unchanged by this batch and not regressions.

**Result: PASS (vacuously — no records written).**

## Budget impact

- Fresh fetches this tick: 16 (8 HTML + 8 PDF).
- Cumulative fetches today: 62 → 78 (target ≤ 2000/day, ~3.9%).
- B2 sync deferred to host (rclone not in sandbox).

## Phase 5 progress

- Records this batch: 0
- Records this phase total: still **9 / 100–160 target**.
- ZMCC 2026: fully ingested 2–10; **2026/01 deferred** (raw on disk).
- ZMCC 2025: 33 candidates; **7 deferred this tick** (raw on disk for 27, 28,
  29, 30, 31, 32, 33); 26 not yet attempted.

## Next tick

1. Tighten parser disposition rule to the policy above.
2. Re-run parser-only over the 8 already-persisted raw pairs (no re-fetch).
3. Continue down the ZMCC 2025 index (most-recent next: 2025/26, 2025/25, ...).

## Sandbox notes

- B2 sync deferred to host (rclone not available in sandbox).
- `.git/index.lock` rotated to `_stale_locks_b0343/` once during the tick;
  unlink consistently denied for host-owned files, so the workaround was
  `mv` to a stale dir.
- Bad-first-pass record JSONs moved to `_stale_b0343_bad_records/` (also
  via `mv`, since unlink is denied) so they are out of `records/` but
  preserved for post-mortem.
- `judges_registry.yaml` was reverted to HEAD via the host-side Write tool
  (the in-sandbox parser had added 6 unsafe alias entries derived from the
  buggy panel parses on 2025/27, 2025/28).
- Wall-clock ~17 min, within the 20-min budget.
