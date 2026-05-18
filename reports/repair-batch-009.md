# Zambia Corpus Repair — Batch 009 (idle)

**Date:** 2026-05-08 22:11:46 UTC (scheduled run)
**Worker:** repair-corpus (automated tick, scheduled-task SKILL)
**Operator:** automated (Claude scheduled task; session `serene-kind-hopper`)
**Status:** **IDLE — 0 records attempted; queue confirmed empty (42 / 42 fixed); no DB writes; no commit, no push**
**Headline:** Fifth consecutive idle repair tick since `repair-batch-008` cleared the queue at 16:51:38Z 2026-05-08. Renewed recommendation: **disable this scheduled task** and update `SKILL.md` manifest URL for `act-zm-2026-005-national-payment-system-act` to the ZambiaLII canonical (parliament.gov.zm URL is permanently 404 — see batch 008).

## Pre-flight

* Pre-step `find .git -name "*.lock" -delete` and `find .git -name "*.lock.bak" -delete` ran. FUSE mount silently rejected unlink on `.git/objects/maintenance.lock` and `.git/ORIG_HEAD.lock` — same pre-existing constraint as every prior repair batch; non-fatal.
* `git pull --ff-only` returned `Already up to date.`
* Working tree carries pre-existing modifications to `worker.log` and untracked artefacts (`Zambia Corpus Worker/`, `_claude_test_delete.txt`, `_repair_batch_003_result.json`, `_repair_batch_004_result.json`, `_repair_batch_run.py`, `_stale_b0343_bad_records/`, `_stale_b0368_bad_records/`, `.write-test`, `.write_check`, `.write_test`) owned by other workers/sessions. **Left untouched** (outside repair worker's domain — repair-corpus only writes to `worker.log`, `gaps.md`, `costs.log`, `reports/repair-batch-NNN.md`, and UPDATEs `corpus.sqlite` records bodies).

## Step 2 — manifest re-verification

Opened `corpus.sqlite` (live DB at workspace root). Iterated all 42 manifest record IDs (39 Acts + 3 SIs) and applied the corruption test from the spec:

```python
lines = body.strip().split('\n')
num_lines = sum(1 for l in lines if l.strip().isdigit())
is_corrupted = (body is None or body.strip() == "" or
                (num_lines > len(lines) * 0.5 and len(lines) > 10))
```

Result:

| Bucket | Count |
|---|---|
| OK (passes quality gate) | **42** |
| Still corrupted | **0** |
| Not found in DB | **0** |

Sample non-corrupted body length: `act-zm-2026-001-teaching-profession-act` = **67,946 chars**.

→ Per Step 2, when zero remain corrupted: **write the idle line to `worker.log` with timestamp and stop**. Done.

## Records attempted (0 — queue empty, MAX_BATCH_SIZE = 8 unused)

No records attempted. No PDFs downloaded. No bodies updated. No FTS rows rewritten. Zero net fetch budget consumed by this tick.

## Records successfully repaired (0)

n/a — repair queue is empty.

## Records failed (0)

n/a — repair queue is empty.

## Records still remaining (0)

n/a — all 42 repair targets clean and pass the manifest's own corruption test.

## Live-DB integrity snapshot (informational)

* `records` = **1849**
* `records_fts` = **1846**
* Δ = **3 rows** — `records` IDs missing from FTS:
    * `judgment-zm-2020-zmsc-51-richard-h-chama-213-other-v-national-pension-schem`
    * `judgment-zm-2020-zmsc-60-matias-chitigwa-mugogo-v-the-people`
    * `judgment-zm-2020-zmsc-65-jackson-kamanga-others-v-the-people`

These three IDs were inserted by `judgment-ingestion-worker batch-0543` at 21:21:00Z (see worker.log). Their FTS indexing is owned by that worker, **not by repair-corpus** (whose mandate is body-only UPDATE on the 42 manifest targets — never INSERT, never DELETE, and never INSERT into `records_fts` for records this worker did not write). Flagging here for visibility; **not actioning**. Repair worker's own non-negotiable Step 4 integrity check applies "after processing the batch", and this tick processed zero records → no commit gate triggered.

## Step 5–6 — sync / commit

* No body UPDATE → no `costs.log` repair-fetch line written (this tick consumed 0 fetches).
* `worker.log` appended with the Step 2 idle line + timestamp (single-line tab-separated, matching batches 001–008 schema).
* This batch report file (`reports/repair-batch-009.md`) created for audit trail consistency with prior batches.
* `rclone` B2 sync — corpus.sqlite **unchanged** by this tick → nothing to sync; B2 mirror remains at the state set by `repair-batch-008` + `judgment-ingestion-worker batch-0543`.
* **No commit, no push from this idle tick** — there is no body-update payload to commit; the only working-tree change attributable to this tick is the worker.log append + this report file, both of which are scoped, idempotent, and consistent with the four prior idle repair ticks (18:58Z, 19:11Z, 20:11Z, 21:11Z) which similarly logged but did not commit. Following the same pattern.

## Recommendation (renewed, fifth consecutive idle tick)

**Disable the `repair-corpus` scheduled task.** The queue has been empty for 5h 20m wall-clock and there is no upstream source of new corruption — corruption was a one-off artefact of a historical PDF-extraction run, not an ongoing drift. Keeping the task scheduled wastes a tick budget and a `git pull` round-trip every 30 minutes for zero work.

If the host wants to keep a passive guard against future re-corruption, a lighter alternative is a daily (not 30-minute) integrity tick that only runs Step 2 and emails on any non-zero corrupted count.

Secondary action item carried forward from batch 008: **update `SKILL.md` manifest line 3** for `act-zm-2026-005-national-payment-system-act` to point at the ZambiaLII canonical FRBR URL (`https://zambialii.org/akn/zm/act/2026/5/eng@2026-04-08/source.pdf`) so that any future re-run of repair on that record does not fail at Step 3a against the dead parliament.gov.zm URL.

---
*Idle tick. No state change to corpus.sqlite. Stop.*
