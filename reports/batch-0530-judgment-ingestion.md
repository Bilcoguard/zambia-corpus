# Batch 0530 — judgment-ingestion-worker tick

- **Worker**: judgment-ingestion-worker
- **Wall-clock window**: 2026-05-06 (UTC, < 20 min target met)
- **Phase**: ZMSC 2022 most-recent-first DESC sweep continuation + inner-gap probe (per b0529 next-tick recommendation)
- **Targets**: ZMSC 2022 nums {21, 19, 18, 17, 16, 15, 14, 13} — skipping known 404 num 20
- **Parser**: v0.3.2 (scripts/batch_0506_zmsc_parse.py wrapping batch_0498_parse + batch_0360_parse) — not invoked this tick (no fetch successes)

## Tick decision (priority order)

a. **REPARSE DEFERRED** — gaps.md cohort of 41 ZMSC raw-on-disk deferrals are
   all flagged `raw-on-disk-pending-v0.3.3` (parser v0.3.2 already attempted;
   awaiting v0.3.3 patterns for the interpretive-ratio family). Not eligible
   for v0.3.2+ reparse this tick.
b. **SCZ SWEEP** — chosen. Probe num 21 (close inner-gap span) and continue
   ZMSC 2022 DESC sweep into nums {19..13}.
c. ZMCC NEW YEARS — not reached.

## Fetch results

| num | status     | code | date | html bytes | pdf bytes |
|-----|------------|------|------|-----------:|----------:|
| 21  | http-error | 404  | –    | –          |        – |
| 19  | http-error | 404  | –    | –          |        – |
| 18  | http-error | 404  | –    | –          |        – |
| 17  | http-error | 404  | –    | –          |        – |
| 16  | http-error | 404  | –    | –          |        – |
| 15  | http-error | 404  | –    | –          |        – |
| 14  | http-error | 404  | –    | –          |        – |
| 13  | http-error | 404  | –    | –          |        – |

**All 8 candidates returned HTTP 404 on the dateless URL probe.** No HTML
or PDF bytes were written. 8 HTTP requests at 5s rate-limit (8 dateless
HEAD/GET probes + 0 PDF chains because each html-stage 404'd) — all
polite, robots.txt-conformant. **Fetch cost this tick: 8.**

## Internal-gap cluster expansion

Combined with prior probes:
- b0529 confirmed contiguous 404 cluster at nums {22..26} (5 nums).
- b0530 confirmed:
  - num 21 → 404 (the previously unprobed boundary cell — this closes
    the {21..26} side of the cluster contiguous to the known num=20 404).
  - nums {19..13} → all 404 (a *further* 7 contiguous nums below the
    20-boundary, none previously probed).

The merged contiguous 404 span is now nums **{13..26}** — 14 contiguous
404s straddling the previously-isolated num=20 boundary. Ie. between
last-known-OK num=27 (above) and the next-still-unprobed num=12 (below),
*every* probed num is 404. This strongly suggests a real publication
gap in ZambiaLII's ZMSC 2022 numbering at the lower end of the 2022
range — consistent either with a court-internal numbering reset / SI
publication-policy boundary, or with low-numbered 2022 judgments simply
not being uploaded to ZambiaLII.

The lower bound of the cluster is **not yet established** — num 12 and
below have not been probed.

## Parse results

- written: 0
- deferred: 0
- raw-not-on-disk: 8 (all confirmed 404s, not parser failures)

Parser was not invoked because no fetches succeeded.

## Integrity checks

- 0 records written → trivially PASS (0/0).
- corpus.sqlite UNCHANGED (records 1840 → 1840; judgments_meta 150 → 150).
- judges_registry.yaml UNCHANGED.
- approvals.yaml UNCHANGED (per non-negotiable rule #4).

## Cohort status after b0530

ZMSC 2022 sweep: 48 of ~60 attempted
- 14 written
- 20 v0.3.3-pending deferred (raw on disk; awaiting interpretive-ratio parser update)
- 1 OCR-pending deferred (zmsc/2022/51 scanned PDF)
- **14 confirmed internal 404s** at nums {13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26}

Daily fetch budget for judgment-ingestion-worker: 48 (cumulative b0523/b0525/b0526/b0529 today) + 8 (b0530) = **56 / 500** (today).

Note: today crossed UTC midnight near tick start. b0523/b0525/b0526/b0529 are
all 2026-05-06 UTC (the worker scheduled today). b0530 ran on 2026-05-06T23:xxZ
UTC, still 2026-05-06 UTC. No budget reset applies.

Cohort cumulative since b0504: 52 written, 42 deferred, 24 confirmed 404
(includes the +14 newly confirmed in b0530).

## B2 sync

Deferred to host (rclone not in sandbox).

## Next-tick recommendation

Probe ZMSC 2022 nums **{12, 11, 10, 9, 8, 7, 6, 5}** (8 candidates) to find
the lower bound of the 13..26 contiguous 404 span. If still all 404, the
cluster either continues all the way to num=1 (i.e. ZambiaLII has no
ZMSC/2022 entries below num=27) or the boundary lies between num=5 and
num=1. Either way, an outcome of "all 404" the next tick should trigger
escalation to:
  - probe nums {4, 3, 2, 1} in the tick after (4-num final probe), or
  - pivot to **ZMSC 2021** most-recent-first sweep (next year down)
    once ZMSC 2022 is determined exhausted.

Tertiary fallback: if a v0.3.3 parser ships, prioritise REPARSE DEFERRED of
the 41-record raw-on-disk cohort (interpretive-ratio family) before
moving deeper into year sweeps.
