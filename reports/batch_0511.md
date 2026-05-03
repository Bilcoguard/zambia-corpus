# Batch 0511 — judgment-ingestion-worker tick

- **Tick UTC**: 2026-05-03T18:19:47Z
- **Worker**: judgment-ingestion-worker (separate budget 500/day)
- **Parser**: v0.3.2 (scripts/batch_0506_zmsc_parse.py wrapping batch_0498_parse.py)

## Scope

Continued post-Phase-5 ZMSC inventory completion per b0506 next-tick.
Reparse-first inventory remains formally exhausted under v0.3.2 (per
b0498) — this tick is a fresh-fetch and on-disk-raw-parse pass against
the ZMSC 2026 most-recent-first sweep continued into the 2025 inner
gaps. Most-recent-first DESC priority: probe 2026/{11} for 404 sentinel,
fill 2026/{05}, then 2025/{28, 26, 14, 07, 06, 05} inner gaps.

## Targets (8)

| # | court | year | num | result |
|---|-------|------|-----|--------|
| 1 | zmsc  | 2026 |  11 | 404 — boundary confirmed (ZMSC 2026 ends at /10 as of 2026-05-03) |
| 2 | zmsc  | 2026 |   5 | 404 — gap genuinely not present on ZambiaLII |
| 3 | zmsc  | 2025 |  28 | parse-only (raw on disk); WRITTEN |
| 4 | zmsc  | 2025 |  26 | parse-only (raw on disk); WRITTEN |
| 5 | zmsc  | 2025 |  14 | 404 — gap genuinely not present |
| 6 | zmsc  | 2025 |   7 | parse-only (raw on disk); WRITTEN |
| 7 | zmsc  | 2025 |   6 | fetched fresh; WRITTEN |
| 8 | zmsc  | 2025 |   5 | fetched fresh; DEFERRED (html_no_summary_pdf_no_match) |

## Records written (4)

- `judgment-zm-2025-zmsc-06-zambia-telecommunication-company-v-felix-musonda-a` — outcome=allowed, via=pdf-tail-2pages
- `judgment-zm-2025-zmsc-07-star-drilling-and-exploration-limited-v-national-t` — outcome=upheld, via=pdf-tail-2pages
- `judgment-zm-2025-zmsc-26-richard-musukwa-and-ors-v-the-attorney-general` — outcome=remitted, via=summary
- `judgment-zm-2025-zmsc-28-konkola-copper-mines-plc-v-the-attorney-general-an` — outcome=dismissed, via=pdf-tail-2pages

## Records deferred (1)

- `zmsc/2025/05` — `html_no_summary_pdf_no_match` (William Saunders v Pemba Lapidaries — declaratory framing on procedural objection; raw HTML+PDF retained on disk for future v0.3.3 reparse).

## 404 sentinels (3)

- `zmsc/2026/11` — confirms 2026 inventory ends at num=10 (10 records on disk)
- `zmsc/2026/05` — gap; not allocated by ZambiaLII
- `zmsc/2025/14` — gap; not allocated by ZambiaLII

## Fetches & budget

- HTTP requests this tick: 7 (3 × 404 HTML probes + 2 × ok = 4 HTML+PDF pairs).
- Cumulative judgment-worker today: 30 + 7 = ~37/500 (well under budget).

## Integrity

- 4/4 records pass schema (id, type=judgment, court, citation, case_name,
  case_number, date_decided, judges≥1, issue_tags non-empty, outcome ∈ enum,
  outcome_detail present, raw_sha256 64 hex chars matching on-disk PDF, source_url).
- 4/4 raw_sha256 verified against on-disk PDF bytes.
- All judges resolve in `judges_registry.yaml` after parser-side
  `update_judges_registry` pass (12 alias-resolution updates against
  existing canonical entries; no new canonical names).
- 0 duplicate judgment IDs (corpus now has 106 unique judgment records).

## corpus.sqlite (gitignored)

- `records` count: 1791 → 1795 ✓ (incremental insert OK)
- `judgments_meta` count: 102 → 106 ✓
- `records_fts` count: 1791 → 1791 (FTS5 inserts blocked by FUSE
  disk I/O error on this session — behaviour matches the b0504
  `mount-blocks-unlink-on-stale-refs` symptom). Source-of-truth
  remains the JSON files; next host-side rebuild via canonical
  `scripts/batch_0504_build_fts5.py` will repopulate FTS deterministically.
  Not a blocker — corpus.sqlite is gitignored and rebuildable.

## Phase 5 progress

- Court breakdown: 25 SCZ/ZMSC + 5 ZMSC (b0506) + 4 ZMSC (b0511) + 72 ZMCC = 106 judgments.
  (Note SCZ/ZMSC pre-b0506 count was 25; b0506 added 5 new ZMSC = 30; this tick adds 4 more = 34.)
- Phase 5 target band: 100–160 judgments. **106/100–160** — IN BAND.

## Next-tick recommendation

ZMSC 2025 inventory now has records at nums {02, 03, 06, 07, 08, 09,
10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
28, 29, 30} = 26 of 30 numbered slots, with confirmed 404s at {04, 05, 14}
and a deferred at {05}. Wait — {05} both 404 and deferred? No — 2025/05 was
fetched OK then deferred at parser; my 404 result was for 2025/14. So:

- 26 ZMSC 2025 records written (02, 03, 06–13, 15–30, except 14)
- 1 ZMSC 2025 deferred (05)
- Confirmed 404 gaps in 2025: {04, 14}
- Untouched 2025 nums: only 01 (raw on disk; previously deferred under b0506
  as html_no_summary_pdf_no_match — leave-to-appeal/declaratory family
  not amenable to v0.3.2)

ZMSC 2026 fully exhausted at v0.3.2: 7 written (01, 04, 06, 07, 08,
09, 10) + 2 deferred at parser (02, 03) + 1 deferred this tick (none —
the 2 ZMSC 2026 nums attempted both 404'd) + 2 confirmed 404 (05, 11+).

Next tick should pivot to **ZMSC 2024 sweep** (no records on disk —
fresh year, highest expected yield) or **ZMSC older years** (2023..)
per the SKILL most-recent-first DESC pattern. ZMSC older-year sweep
remains approved per `approvals.yaml.zmsc_older_year_sweep_approved:
true` (b0498). The canonical URL pattern is now empirically confirmed
this tick: `/akn/zm/judgment/zmsc/{year}/{num}/eng` 302→`@YYYY-MM-DD/`.

## approvals.yaml

NOT modified — Phase 5 human-only confirmation rule.

## B2 sync

Deferred to host (rclone not in sandbox).
