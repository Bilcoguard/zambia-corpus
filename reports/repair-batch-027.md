# Repair batch 027 — IDLE (16th consecutive idle tick)

**Timestamp (UTC):** 2026-05-12T05:12:35Z
**Worker:** repair-corpus (scheduled task v3)
**Verdict:** No work required — all 48 manifest records pass the v3 corruption test.

## Step 1 — git pull

Stale lock cleanup was run first (broadened to match `*.lock*` since the
v3 hard-coded `*.lock` / `*.lock.bak` patterns do not catch files whose
suffix is *after* `.lock` such as `index.lock.b0602-...` or
`HEAD.lock.atomic`). The sandbox FUSE mount still rejects `rm` on most of
these (`Operation not permitted`), but they no longer block git
operations now that the previously-named lock-files under
`refs/remotes/origin/` have been cleared.

```
$ git pull --ff-only origin main
From https://github.com/Bilcoguard/zambia-corpus
 * branch            main       -> FETCH_HEAD
Already up to date.
```

Two consecutive blocked ticks (2026-05-12T01:32 and 2026-05-12T05:07)
that halted on `fatal: bad object refs/remotes/origin/main.lock.*` are
now unblocked — `.git/refs/remotes/origin/` is clean of named-lock
files. The `.git/objects/maintenance.lock.*` residue remains
unlinkable from the sandbox, but does not block pull/push.

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

Spot-checked three bodies confirm real legislative text, not line numbers:

- `act-zm-2010-027-the-animal-health` (89,852 chars) — opens with
  "Animal Health [No. 27 of 2010 385 / THE ANIMAL HEALTH ACT, 2010 /
  ARRANGEMENT OF SECTIONS ..."
- `act-zm-2026-005-national-payment-system-act` (real body) — opens with
  "National Payment System [No. 5 of 2026 107 / THE NATIONAL PAYMENT
  SYSTEM ACT, 2026 ..."
- `si-zm-financial-intelligence-centre-prescribed-threshold-regulations-2022`
  — opens with "19th August, 2022 Statutory Instruments 839 ... The
  Financial Intelligence Centre (Prescribed Threshold) Regulations,
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

## Step 5 — B2 sync

No corpus.sqlite mutation this tick, so no B2 push attempted. The sqlite
file is byte-identical to the last good push; rclone copyto would be a
no-op. (rclone is also not installed in the sandbox, per prior ticks.)

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

Repair worker idle for the 16th consecutive tick. The 48-record repair
backlog remains fully cleared. Next tick runs on schedule.
