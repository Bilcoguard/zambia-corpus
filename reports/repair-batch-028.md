# Repair batch 028 — IDLE (17th consecutive idle tick)

**Timestamp (UTC):** 2026-05-12T07:14:33Z
**Worker:** repair-corpus (scheduled task v3)
**Verdict:** No work required — all 48 manifest records pass the v3 corruption test.

## Step 1 — git pull

Stale-lock cleanup ran first (`find .git -name "*.lock" -delete` and the
`.lock.bak` variant). One residual file remained: `.git/objects/maintenance.lock`,
which the FUSE-backed sandbox refuses to delete (`Operation not permitted`),
but it does not block pull/push as confirmed below.

```
$ git pull --ff-only
Already up to date.
```

HEAD: `1117ee8 batch-0607-jiw: post-tick discovery — FTS5 corruption resolved by host-side rebuild`

## Step 2 — Identify remaining corrupted records

Ran the v3 corruption test against all 48 manifest IDs:

```python
lines = body.strip().split('\n')
num_lines = sum(1 for l in lines if l.strip().isdigit())
is_corrupted = (num_lines > len(lines) * 0.5 and len(lines) > 10)
```

| Bucket | Count |
|---|---:|
| OK (passes corruption test) | **48** |
| Still corrupted (line-numbers) | **0** |
| Empty / NULL body | **0** |
| Not found in DB | **0** |

Spot-checked three bodies — real legislative text confirmed:

- `act-zm-2010-027-the-animal-health` (89,852 chars) — opens with
  "Animal Health [No. 27 of 2010 385 / THE ANIMAL HEALTH ACT, 2010 /
  ARRANGEMENT OF SECTIONS ..."
- `act-zm-2026-005-national-payment-system-act` (155,266 chars) — opens with
  "National Payment System [No. 5 of 2026 107 / THE NATIONAL PAYMENT
  SYSTEM ACT, 2026 ..."
- `si-zm-financial-intelligence-centre-prescribed-threshold-regulations-2022`
  (26,018 chars) — opens with "19th August, 2022 Statutory Instruments 839
  ... The Financial Intelligence Centre (Prescribed Threshold) Regulations,
  2022 ..."

Verdict: **No work required.** All 48 manifest records carry valid body
text; none regress against the v3 rule.

## Steps 3 / 3a–3f — Repair batch

Skipped. No corrupted records to repair.

## Step 4 — Integrity check

```
records      = 1,892
records_fts  = 1,892
records == records_fts → OK
```

Note: per the JIW POST_TICK_DISCOVERY entry at 07:11:30Z, the
host-side rebuild of `records_fts` was applied between batch-0607-jiw's
probe and re-probe. The repair worker's records-table is unaffected by
that rebuild; this idle tick simply confirms the 48-record backlog
remains cleared.

## Step 5 — B2 sync

No corpus.sqlite mutation this tick. rclone is not installed in the
sandbox — B2 sync deferred to host. The sqlite file md5 prior to this
tick is `a9af40f02b8cb82a20eb49a5f893d820` (per b0607 re-probe); this
tick performs only read-only queries, so the file is byte-identical.

## Step 6 — Commit / push

Only this report + the worker.log entry are committed. corpus.sqlite,
approvals.yaml, judges_registry.yaml, costs.log, gaps.md, provenance.log
are all unchanged this tick.

## Step 7 — Summary

- Records attempted: **0**
- Records successfully repaired: **0**
- Records failed: **0**
- Records still remaining (corrupted across the 48-record manifest): **0**
- Wall-clock used: well under the 20-minute budget
- Fetch count: 0 (no PDFs downloaded)

Repair worker idle for the 17th consecutive tick. The 48-record repair
backlog remains fully cleared. Next tick runs on schedule.
