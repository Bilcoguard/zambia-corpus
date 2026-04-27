# Batch 0290 Report

**Phase:** 4 — bulk (acts_in_force, pool-refresh probe)
**Tick:** 2026-04-27 (UTC) — scheduled tick, 30-min cadence
**Yield:** 0 picks (probe-only)
**Wall-clock:** ~10 min
**Parser version:** 0.6.0-act-zambialii-2026-04-26 (carried over from b0289; not exercised this tick)

## Summary

Inherited zambialii chronological-first acts pool was exhausted at the close of batch 0289. Per the b0289 closing note, this tick performs the deferred **pool-refresh probe** across both upstream act sources to determine whether any newly published 2025/2026 Acts exist that are not yet in the corpus.

**Result:** zero new picks. acts_in_force chronological-first sweep is at steady state with respect to current Parliament of Zambia publication.

## Probes

### Probe 1 — zambialii.org

| Action | URL | Bytes | Result |
|---|---|---|---|
| robots re-verify | `/robots.txt` | 1,818 | sha256 unchanged: `fce67b6…dcd8f0` |
| listing | `/legislation/recent` | 94,772 | 13 acts enumerated |
| listing diag | `/legislation/` | 231,880 | filter form static — no recent-year drilldown via URL params |
| listing diag | `/legislation/?year=2025` | 232,020 | identical to /legislation/ (HTMX-driven filter) |
| listing diag | `/legislation/?year=2026` | 232,020 | identical to /legislation/ (HTMX-driven filter) |

`/legislation/recent` returned: 2025/5, 2025/6, 2025/7, 2025/8, 2025/9, 2025/22, 2025/23, 2025/24, 2025/25, 2025/26, 2025/27, 2025/28, 2025/29. **All 13 already in corpus.**

### Probe 2 — www.parliament.gov.zm

| Action | URL | Bytes | Result |
|---|---|---|---|
| robots check | `/robots.txt` | 2,003 | sha256: `278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762` (Drupal default; Crawl-delay 10s) |
| listing p0 | `/acts-of-parliament` | 38,208 | 20 acts (2026/1..11 + 2025/21..29) |
| listing p1 | `/acts-of-parliament?page=1` | 38,164 | 20 acts (2025/1..20) |
| listing p2 | `/acts-of-parliament?page=2` | 38,291 | 19 acts (2024/12..30) |

Total enumerated: 59 distinct `(year, num)` tuples spanning 2024/12..2026/11. **All 59 already in corpus.**

## Pool

- Inherited from batch 0289: 0 items
- Discovered this tick: 0 new items (full upstream-listing diff against `records/acts/**/*.json` returned empty set)
- Remaining for batch 0291 (acts_in_force chronological-first): 0

## Integrity

This tick performed no record writes; the standard CHECK1..CHECK6 do not apply. A diff verification was performed instead (see `Probes` above): both listings 100% covered by the on-disk corpus.

## Provenance

User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
Crawl-delay: 6 s on zambialii (robots 5 s + 1 s margin); 11 s on parliament (robots 10 s + 1 s margin).
robots.txt sha256 (zambialii): `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` (unchanged from b0193..0289)
robots.txt sha256 (parliament): `278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762`

## Budget

- Today (2026-04-27 UTC) fetches at tick start: ~28/2,000 (~1.4%) — last batch 0289 closed at this level
- Today (2026-04-27 UTC) fetches at tick end: ~37/2,000 (~1.85%) — 9 listing/robots fetches this tick
- Tokens within budget

## Cumulative

- Acts on disk: 1,169 records under `records/acts/**/*.json` (unchanged from b0289)
- Multi-act-gazette retry queue: 1 item (2024/9 — unchanged)
- Oversize-pdf queue: 6 items (2002/6, 2005/21, 2008/5, 2009/10, 2009/30, 2012/16 — unchanged)
- OCR section-tolerant retry queue: 6 items (1988/32, 1994/40, 1995/33, 2004/6, 2008/9, 2009/7 — unchanged)
- OCR backlog: 18 items (unchanged)
- SI records on disk: 539 (sis_corporate sub-phase shows 6 records; sis_tax 8; others sparse)

## SQLite

`corpus.sqlite` not modified (no record writes; established disposition: FTS5 vtable broken, journal held open — JSON records authoritative).

## B2 sync

Deferred to host (rclone not available in sandbox).

## Phase 4 status

`approvals.yaml -> phase_4_bulk -> complete` remains `false`. Worker does NOT flip the flag. The **acts_in_force chronological-first sub-phase** has now reached upstream steady state at 2026/11 (verified by independent probes of two upstream sources).

## Recommended next move (for human reviewer)

Per `approvals.yaml.phases.phase_4_bulk.priority_order`, the sub-phase that follows `acts_in_force` is `sis_corporate`. The corpus currently holds 6 records tagged `sis_corporate`. To proceed productively, one of the following human-controlled decisions is needed:

1. **Define sis_corporate scope.** Identify the upstream listing endpoint (zambialii has `/legislation/?nature=si` segment — would need to be enumerated against existing on-disk SIs for diff) and whether the topic taxonomy is keyword-based (regulations citing the Companies Act, Securities Act, Banking & Financial Services Act) or list-based.
2. **Approve a retry-queue tick.** Authorise targeted work on the multi-act-gazette retry queue (1 item — would unblock 2024/9 if a Government Gazette PDF splitter is added) or the oversize-pdf queue (6 items — chunked PDF fetching).
3. **Accept current acts_in_force coverage and move forward.** If the residual queues (1 multi-act + 6 oversize + 6 OCR retry + 18 OCR backlog = 31 deferred Acts) are deemed acceptable gaps, list them in `gaps.md` and consider phase_4_bulk acts_in_force sub-phase complete.

Worker will continue to idle on `phase_4_bulk` ticks until pool refresh detects new upstream Acts (cadence: roughly weekly Parliament publication during sitting season) or human reviewer changes scope.
