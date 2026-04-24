# Batch 0168 Report

**Date:** 2026-04-24T05:06:00Z
**Phase:** 4 (Bulk Ingestion)
**Records committed:** 0
**Repeal-chain links applied:** 0
**Fetches (script):** 7
**Integrity:** PASS

## Strategy

Probe-only pass. Per batch 0167 next-tick plan (fresh narrower
rotation of the primary-statute sweep). SCOPE REDUCED: the
sandbox per-call bash timeout is 45 s and a full 8-probe +
8-ingest run with 5-second rate limits cannot complete inside
that window, so this batch ran two sub-ticks:

- Sub-tick A (2026-04-24T05:04:00Z–05:04:12Z): probes
  `agriculture`, `public health`. 2 fetches. 102 links
  discovered, 2 novel, 0 survived HEAD + title filters
  (amendment-act variants).
- Sub-tick B (2026-04-24T05:04:56Z–05:05:25Z): probes
  `national assembly`, `parliament`, `cooperatives`,
  `electoral`, `food safety`. 5 fetches. 210 links
  discovered, 6 novel, 0 survived HEAD + title filters
  (all amendment-act variants).

Cumulative: 7 fetches. Probe queries issued: 7 of the 8-query
rotation (`elections` deferred). PDF fallback was DISABLED in
both sub-ticks to keep each sub-tick inside the 45 s bash
window — sparse-HTML candidates are gapped, not PDF-fetched.
Title filter rejects any AKN-page title containing
`amendment` (plus OCR variants `amendrnent`, `amendement`),
`appropriation`, `repeal`, `supplementary`, `validation`, or
`transitional`. No SEED candidates this batch; no
unconditional repeal-chain links are pre-declared.

**Probe yield: 0 new primary parents.** Below the 2-parent
threshold set by the batch-0167 next-tick plan — the next
tick MUST shift to the alphabetical `/akn/zm/act/` listing
traversal fallback for unresolved Cap. parents (Juveniles
Cap. 53, Hire Purchase, Stamp Duty, Sale of Goods, Bills of
Exchange). Patents (Cap. 400 -> Act 2016/40) and Copyright
(Cap. 406 -> Act 1994/44) are already in HEAD per
`existing_acts.txt`.

## Committed records

None — every novel probe hit was an amendment-act variant
rejected by the B-POL-ACT-1 title filter.

**Total sections:** 0

## Repeal-chain links

No repeal-chain links applied this batch — the pre-declared
unconditional link list was empty.

## Seed summary

- Seed candidates queued: 0
- Seed candidates committed: 0
- Seed candidates gapped: 0

## Probe summary

- Probe queries issued: 7 ('agriculture', 'public health',
  'national assembly', 'parliament', 'cooperatives',
  'electoral', 'food safety')
- Probe query deferred: 'elections' (not issued; queue for
  next tick)
- Candidates discovered (total across both sub-ticks): 312
- Candidates novel (post seen-set filter): 8
- Candidates surviving HEAD + title filters: 0
- Candidates processed this batch: 0

## Integrity checks
- CHECK 1 (batch unique IDs): PASS (no records to check)
- CHECK 2 (no HEAD collision): PASS (no records to check)
- CHECK 3 (source_hash matches raw on disk): PASS (no raw
  files written)
- CHECK 4 (amended_by / repealed_by reference resolution):
  PASS (no new cross-refs)
- CHECK 5 (required fields present): PASS (no records to
  check)

## Raw snapshots

No raw record bytes saved this batch (no ingests). Probe JSON
bodies fetched for audit but not retained as raw records. B2
sync deferred to host (rclone not available in sandbox).

## Gaps / skipped targets

Sub-tick A ('agriculture', 'public health'):

- 1995/21 'Agriculture (Seeds) (Amendment) Act, 1995':
  pre-fetch reject — title contains 'amendment' (via query
  'agriculture')
- 1990/2 'National Agricultural Marketing (Amendment) Act,
  1990': pre-fetch reject — title contains 'amendment' (via
  query 'agriculture')

Sub-tick B ('national assembly', 'parliament',
'cooperatives', 'electoral', 'food safety'):

- 2021/36 'Acts of Parliament (Amendment) Act, 2021':
  pre-fetch reject — title contains 'amendment' (via query
  'parliament')
- 1996/23 'Electoral (Amendment) Act, 1996': pre-fetch
  reject — title contains 'amendment' (via query
  'electoral')
- 1986/19 'Electoral (Amendment) Act, 1986': pre-fetch
  reject — title contains 'amendment' (via query
  'electoral')
- 1995/7 'Electoral (Amendment) Act, 1995': pre-fetch
  reject — title contains 'amendment' (via query
  'electoral')
- 1988/20 'Electoral (Amendment) Act, 1988': pre-fetch
  reject — title contains 'amendment' (via query
  'electoral')
- 2001/4 'Electoral (Amendment) Act, 2001': pre-fetch
  reject — title contains 'amendment' (via query
  'electoral')

## Notes

- No SEED stage this batch — no seed candidates were
  deferred into 0168 from batch 0167.
- B-POL-ACT-1 title filter retains the OCR variants
  `amendrnent` and `amendement` added in batch 0157.
- No unconditional repeal-chain link applied this batch —
  the pre-declared list is empty.
- The batch was split across two sub-ticks because the
  sandbox per-call bash timeout (45 s) cannot fit the full
  8-probe rotation plus ingests plus 5-second rate limits.
  PDF fallback was disabled in both sub-ticks for the same
  reason. This is a sandbox-environment adaptation and does
  NOT change the underlying non-negotiables (rate limits,
  provenance, integrity checks all preserved).
- **Next tick: probe yield 0 new primary parents (below the
  2-parent alphabetical-fallback threshold) — SHIFT to the
  alphabetical `/akn/zm/act/` listing traversal fallback**
  for the remaining unresolved Cap. parents (Juveniles
  Cap. 53, Hire Purchase, Stamp Duty, Sale of Goods, Bills
  of Exchange). The listing traversal should be split across
  sub-ticks the same way: a single `/akn/zm/act/` index
  fetch per sub-tick, then sub-ticks for candidate ingests.
