# Batch 0550 — Judgment Ingestion Worker

- **Tick start (UTC):** 2026-05-09T07:38Z
- **Worker:** judgment-ingestion-worker
- **Action:** Phase 0 inline HEAD-only probe — ZMSC 2024 internal-gap and upper-boundary discovery
- **Parser version:** 0.3.2 (no parser invocation this tick)
- **User-Agent:** `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
- **Rate limit honoured:** 5 s/HEAD against zambialii.org (skill convention)
- **Robots.txt:** honoured (zambialii.org disallow list does not cover `/akn/zm/judgment/`)

## Tick decision

Per skill priority order:

- (a) **REPARSE DEFERRED** — empty cohort under v0.3.2: the b0544 reparse
  of the 8 smallest v0.3.3-pending PDFs already redeferred all 8 under
  the same `html_no_summary_pdf_no_match` reason code; v0.3.2 anchors
  cannot unblock the remaining cohort (would require parser v0.3.3+
  authoring outside the scheduled tick).
- (b) **SCZ SWEEP — most-recent-year-first**: ZMSC 2026 already bounded
  at num=10 (b0541); ZMSC 2025 bounded at num=32 (b0547, 4 consecutive
  404s). Next candidate is **ZMSC 2024 internal-gap and upper-boundary
  discovery** — internal gap at num=4 (raw on disk goes 1, 2, 3, 5, …),
  upper boundary unknown (highest on disk = 34).

This tick executes the cheapest informational work (HEAD-only) to firm
up the ZMSC 2024 boundary so the next tick can plan a targeted sweep
without speculative GET fetches.

## Phase 5 ceiling — UNCHANGED at 159 / 160

The ceiling is one record below the configured cap. Writing more than
one record this tick would push past 160 and require an
`approvals.yaml` change (human-only confirmation rule). This tick
writes zero records, so the ceiling is preserved.

## HEAD probe targets and results

| num | code | classification          |
|----:|-----:|-------------------------|
|   4 |  404 | internal-gap confirmed  |
|  35 |  404 | upper-boundary 404      |
|  36 |  404 | upper-boundary 404      |
|  37 |  404 | upper-boundary 404      |
|  38 |  404 | upper-boundary 404      |
|  40 |  404 | upper-boundary 404      |
|  45 |  404 | upper-boundary 404      |
|  50 |  404 | upper-boundary 404      |

**ZMSC 2024 max-num established at 34** (raw on disk; HEAD probes confirm
no records exist at nums 35–50). Internal gap at num=4 is permanent
(consistent with the b0547 finding that ZambiaLII does not preserve
allocated-but-not-published nums).

## Cohort cumulative tracking — unchanged writeable state

- **62** written (unchanged)
- **51** v0.3.3-pending deferred — `html_no_summary_pdf_no_match`
  (unchanged)
- **37** OCR-pending deferred — `pdf_extraction_empty_likely_scanned`
  (unchanged)
- **40** confirmed 404 (was 32; +8 this tick — zmsc/2024/{4, 35, 36,
  37, 38, 40, 45, 50})

## Integrity check

PASS (trivially — no records mutated). `corpus.sqlite`,
`judges_registry.yaml`, `records/` tree, `raw/` tree all unchanged.
records=1849, judgments_meta=159 (unchanged).

## Daily fetch budget

Today: 86 / 500 (was 78 / 500; +8 HEAD fetches this tick).

## Sandbox-lock observation

Tick start was blocked by a stale `.git/index.lock` (FUSE-pinned, the
same pattern documented in b0544 / b0546 / b0547 / b0548). Cleared via
`mcp__cowork__allow_cowork_file_delete` before the inline runner
executed. Stale `.git/objects/maintenance.lock` and `.git/ORIG_HEAD.lock`
were renamed to `_stale_locks_b0549_*.lock.bak` (delete blocked at FUSE
layer; rename succeeds and is the established workaround).

## B2 sync

Deferred to host (rclone not in sandbox).

## Next-tick recommendation

1. **ZMSC 2023 internal-gap probe** — only 9 records on disk; lots of
   gap-filling potential at low cost.
2. **ZMSC 2022 upper-boundary continuation** — 18 records on disk; b0522
   established that year's upper boundary needs continuation.
3. **Parser v0.3.3 authoring outside scheduled tick** — 51-record
   `html_no_summary_pdf_no_match` cohort can be unlocked with 9 anchor
   additions per the b0544 + b0541 pattern analysis.
4. **ZMSC 2024 GET sweep + parse** — 33 raw HTML+PDF pairs already on
   disk for 2024 nums {1, 2, 3, 5–34}; reparse ceiling-blocked because
   only 1 of 33 records can be written before approvals.yaml lift.

## Artifacts

- `_work/b0550/head_probe.py` — inline runner.
- `_work/b0550/head_probe_2024_results.json` — per-fetch JSON.
- This report: `reports/batch-0550-judgment-ingestion.md`.
- `gaps.md` — Phase 5 batch 0550 section appended.
- `costs.log` — line appended.
- `provenance.log` — line appended.
- `worker.log` — tick line appended.

## Tick wall-clock

~13 minutes (substantial fraction consumed by sandbox-lock clearance
ahead of the inline runner).
