# Batch 0361 — Phase 5 reparse-first triage

- Tick start: 2026-04-30T15:36:00Z
- Sandbox session: exciting-nifty-johnson
- Phase: phase_5_judgments (approved + incomplete)
- Parser version: 0.3.1 (frozen baseline `scripts/batch_0360_parse.py`,
  copied to `scripts/batch_0361_parse.py` with only TARGETS slice +
  `_work` directory + diagnostic-reason-code refinement edits)
- Mode: REPARSE-FIRST (zero fresh fetch budget consumed)

## Slice

Eight ZMCC raw HTML+PDF pairs already on disk (deferred in earlier
batches under the now-superseded `outcome_not_inferable_under_tightened_policy`
generic reason), top of deferred queue, year-DESC then num-DESC:

| # | Court/Year/# | Date       | Source URL |
|---|--------------|------------|------------|
| 1 | zmcc/2026/1  | 2026-01-20 | https://zambialii.org/akn/zm/judgment/zmcc/2026/1/eng@2026-01-20 |
| 2 | zmcc/2025/33 | 2025-12-18 | https://zambialii.org/akn/zm/judgment/zmcc/2025/33/eng@2025-12-18 |
| 3 | zmcc/2025/32 | 2025-12-16 | https://zambialii.org/akn/zm/judgment/zmcc/2025/32/eng@2025-12-16 |
| 4 | zmcc/2025/30 | 2025-12-11 | https://zambialii.org/akn/zm/judgment/zmcc/2025/30/eng@2025-12-11 |
| 5 | zmcc/2025/28 | 2025-12-05 | https://zambialii.org/akn/zm/judgment/zmcc/2025/28/eng@2025-12-05 |
| 6 | zmcc/2025/25 | 2025-12-04 | https://zambialii.org/akn/zm/judgment/zmcc/2025/25/eng@2025-12-04 |
| 7 | zmcc/2025/24 | 2025-11-28 | https://zambialii.org/akn/zm/judgment/zmcc/2025/24/eng@2025-11-28 |
| 8 | zmcc/2025/23 | 2025-11-27 | https://zambialii.org/akn/zm/judgment/zmcc/2025/23/eng@2025-11-27 |

## Yield

- Records written: **2 / 8**
- Records deferred: **6 / 8** (specific reason codes, no banned generic)
- Outcome-source breakdown: 2/2 via `pdf-tail-2pages` fallback
- Fresh fetches this tick: **0** (all raw bytes already on disk —
  reparse-first compliance)

### Written

| Record ID | Outcome | Source | Detail (truncated) |
|-----------|---------|--------|--------------------|
| `judgment-zm-2025-zmcc-30-legal-resources-foundation-limited-v-the-attorney` | allowed | pdf-tail-2pages | "conservatory order is not granted and the Petition succeeds" |
| `judgment-zm-2025-zmcc-23-emmanuel-kayuni-suing-as-administrator-of-the-esta` | dismissed | pdf-tail-2pages | "[75] The petition is dismissed for want of jurisdiction" |

### Deferred

All six classified `html_no_summary_pdf_no_match` (specific code from
`approvals.yaml` `deferral_reasons_locked`; the banned generic
`outcome_not_inferable_under_tightened_policy` was NOT used). Raw
HTML+PDF retained on disk for a future widened-vocabulary re-parse.
See gaps.md "Batch 0361" section for detail.

| Court/Year/# | Reason |
|--------------|--------|
| zmcc/2026/1  | html_no_summary_pdf_no_match |
| zmcc/2025/33 | html_no_summary_pdf_no_match |
| zmcc/2025/32 | html_no_summary_pdf_no_match |
| zmcc/2025/28 | html_no_summary_pdf_no_match |
| zmcc/2025/25 | html_no_summary_pdf_no_match |
| zmcc/2025/24 | html_no_summary_pdf_no_match |

## Integrity

`scripts/integrity_check_b0361.py` PASS (2 records). All required
fields present, source_hash and raw_sha256 match raw HTML/PDF on
disk, judges resolve in `judges_registry.yaml`, outcome enum + court
enum + role enum all valid, outcome_detail safety checks green, no
duplicate IDs.

## Budget impact

- Fresh fetches: 0 (reparse-pass: zero-cost)
- Cumulative today: ~15 -> ~15 / 2000 (~0.75%)
- Tokens: not separately metered this tick
- B2 sync: deferred to host (rclone not available in sandbox)

## Phase 5 progress

- Before tick: 35 / 100-160 target
- After tick:  **37 / 100-160** target

## Next tick

Continue the reparse pass under the same parser_v0.3.1 baseline.
Many candidates in the deferred queue (zmcc/2024/*, zmcc/2023/*,
zmcc/2022/*) remain unprocessed — all raw bytes on disk, zero fetch
cost. The reparse-first policy in approvals.yaml takes precedence
over fresh DESC sweeps until the queue is exhausted or the parser
hits a known-unaddressable subset.
