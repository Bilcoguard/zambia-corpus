# b0704-phase8 — Phase 8 nightly re-verification — COMMIT/PUSH DEFERRED

- **Tick id:** `b0704-phase8`
- **Phase:** `phase_8_nightly_reverify`
- **Detected at:** `2026-05-18T14:12:00Z`
- **Session:** `peaceful-bold-mendel` (model claude-opus-4-7)
- **Outcome:** Phase 8 batch **ran successfully and produced valid work products**, but commit/push is **deferred** pending human reconciliation of a pre-existing upstream block: local HEAD chain contains an unpushable 118MB `corpus.sqlite` blob in commit `0b59638` that exceeds GitHub's per-file size limit.

## Phase 8 work products (on disk, uncommitted)

The Phase 8 batch itself completed cleanly. Every integrity check PASSED. The following files exist on disk and are ready to commit once the upstream block is resolved:

- `scripts/batch_0704_phase8_reverify.py` — clone of frozen baseline with `BATCH = "0704"`
- `reports/batch-0704-reverify.json` — full per-record machine-readable report (1957 pool, 8 sampled, 7 match, 1 drift, 0 fetch_error)
- `reports/batch-0704.md` — narrative report
- Appended audit-only entry to `gaps.md` for the single drift
- Appended fetch + summary lines to `costs.log`
- Appended TICK_START/RESULT/INTEGRITY/END lines to `worker.log`
- Appended REVERIFY summary to `provenance.log`

## Batch result summary

- Pool size: **1957** records
- Sample size: **8** (sample_rate 0.01, capped at MAX_BATCH=8)
- Seed: `phase8-reverify-2026-05-18-b0704`
- Verdicts: **match=7, drift=1, fetch_error=0**
- The one drift: `si-zm-1982-049-zambia-airways-corporation-date-of-dissolution-order-1982` (zambialii.org bare-AKN path; expected `zambialii_akn_html_dynamic_render_drift` cohort behaviour; legal content unchanged).
- All 9 standard Phase 8 integrity checks PASS.
- `corpus.sqlite` live: `records=1954 records_fts=1954 dup_ids=0 quick_check=ok integrity_check=ok` — baseline parity preserved.

## Why commit/push is deferred

When this tick started, the local main branch was **2 commits ahead of origin/main** (`bb09c08`), with the following local-only commits:

1. **`0b59638` — "Repair batch b0703: fixed 8 records (no_body=41 corrupted=0 stubs=0, 33 remaining)"** — created by session `sweet-sleepy-wozniak` at 2026-05-18T14:08:24Z. **This commit accidentally added `corpus.sqlite` (118,898,688 bytes ≈ 113MB) to the tree as a tracked blob, even though `corpus.sqlite` is gitignored.**
2. **`bca06bc` — "Judgment batch b0703-jiw: +3 CoA from judiciary-zm"** — created by the same session at ~14:09Z. This stacks 3 new judgment records on top of 0b59638.

The session `sweet-sleepy-wozniak` already attempted to push 0b59638 at 14:09:19Z and was **rejected by GitHub** with an LFS / file-size error:

```
remote: error: Trace: cf4f84e754d547f7420fd940f4a5b81a2d14559a3559cf224847c03aec4fb69f
remote: error: See https://gh.io/lfs for more information.
remote: error: File corpus.sqlite is 1...
```

(message truncated in worker.log at line 9069 — likely "is 113.4 MB; this exceeds GitHub's file size limit of 100.00 MB").

Because `0b59638` is the parent of `bca06bc`, **any further commit stacked on top of HEAD will also fail to push** for the same reason. Stacking a Phase 8 commit on top would simply add a third unpushable local-only commit to the pile.

## Action taken this tick

Per BRIEF.md non-negotiable #7 ("Integrity checks before every commit. If any check fails, halt, log to `worker.log`, do not commit.") and the brief's "fail loud with a full diagnostic on unexpected errors" rule, this tick:

1. ✅ Pulled `--ff-only` (succeeded — "Already up to date.")
2. ✅ Read `BRIEF.md` and `approvals.yaml`. Active phase: `phase_8_nightly_reverify` (approved: true, complete: false, sample_rate: 0.01).
3. ✅ Confirmed daily budget (~145/2000 fetches before this tick; well under the 2000 limit).
4. ✅ Ran the Phase 8 batch (`scripts/batch_0704_phase8_reverify.py`). 8 fetches, all HTTP 200. Wall-clock 21s of 20min budget.
5. ✅ All standard Phase 8 integrity checks PASSED.
6. ✅ Wrote the JSON + MD batch reports; appended audit entries to `gaps.md`, `costs.log`, `worker.log`, `provenance.log`.
7. ❌ **Did NOT commit** — stacking on top of HEAD would just create a third unpushable local-only commit.
8. ❌ **Did NOT push** — push would fail at origin due to the 118MB `corpus.sqlite` blob in `0b59638`.
9. ❌ **Did NOT reset/rebase/force-push** — the brief forbids destructive git operations, and resolving this requires human judgment about whether to (a) `git filter-repo --invert-paths --path corpus.sqlite` to strip the blob from 0b59638 then force-push the cleaned history, or (b) drop both 0b59638 and bca06bc and re-apply the underlying repair / jiw work as fresh commits without `corpus.sqlite`.

## Human action requested

Peter, please resolve the upstream block before the next tick. Suggested options:

### Option A — strip the blob from history (preserves the existing 2 commits' content)

```bash
cd ~/KateWestonCorpus/corpus
git fetch origin
git status                       # confirm 0b59638 and bca06bc are local-only
# Use git-filter-repo (preferred) to drop corpus.sqlite from the two local commits:
pip install git-filter-repo
git filter-repo --invert-paths --path corpus.sqlite --refs origin/main..HEAD --force
# Verify:
git log --stat origin/main..HEAD | grep -c corpus.sqlite   # should print 0
git push origin main             # should now succeed
```

### Option B — reset and re-apply

If the b0703 repair and b0703-jiw work products can be re-derived from `records/` and `reports/` (which they should be, since the corpus.sqlite is rebuilt deterministically from on-disk JSON), then the cleanest action is:

```bash
git reset --hard origin/main     # destroys 0b59638 and bca06bc — only safe if work products are also on disk
# Re-add the b0703 repair + b0703-jiw record JSONs + reports + scripts (without corpus.sqlite)
git add records/judgments/2026/judgment-zm-2026-coa-{110,344,047}-*.json
git add reports/repair-batch-b0703.md reports/repair-batch-b0703-summary.json
git add scripts/  # whatever scripts those batches used
git add worker.log costs.log provenance.log gaps.md
git status        # double-check corpus.sqlite is NOT staged
git commit -m "Recompose b0703 repair + b0703-jiw on top of bb09c08 (drop corpus.sqlite blob)"
git push origin main
```

### Option C — defer indefinitely

Leave the local-only commits alone. Ticks continue to run Phase 8 (which only reads from disk and writes to gitignored or non-sqlite files), but their outputs accumulate on disk uncommitted. This is the option this tick effectively defaulted to.

## After Peter resolves the upstream block

The next tick should:
1. `git pull --ff-only` (will succeed once origin/main has been updated to whichever resolution Peter chose).
2. Detect the stranded Phase 8 work products on disk:
   - `scripts/batch_0704_phase8_reverify.py`
   - `reports/batch-0704.md`
   - `reports/batch-0704-reverify.json`
   - the b0704 entries already appended to `worker.log`, `costs.log`, `provenance.log`, `gaps.md`
3. Decide whether to commit them as-is (preferred, since they are already finalised and integrity-checked) or to re-run the Phase 8 batch with a fresh batch number.

If the next tick chooses to commit them as-is, the message should be:
`worker: phase_8 batch 0704 — nightly re-verification (sample 8/1957, match=7 drift=1 fetch_error=0, all 9 integrity checks PASS)` — same convention as `a383e19` / `651c883`.

## References

- BRIEF.md §"Non-negotiables" #4 (Versioning — never silently overwrite) and #7 (Integrity checks before every commit).
- approvals.yaml `phase_8_nightly_reverify` (approved: true, complete: false, sample_rate: 0.01).
- worker.log lines 9020-9072 (the b0703 + b0703-jiw history that produced 0b59638 and bca06bc).
- reports/batch-0704.md — narrative Phase 8 report for this tick.
- reports/batch-0704-reverify.json — machine-readable per-record results.
