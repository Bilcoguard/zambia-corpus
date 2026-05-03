# Batch 0495 — parser_v0.3.2 reparse continuation (ZMCC 2025 DESC sweep finisher, num {6, 5, 2})

- **Tick start (UTC):** 2026-05-03T~13:02Z (scheduled tick; resumed after Peter's host-side ref-cleanup intervention at ~13:05Z)
- **Phase:** 5 (judgments) — approved+incomplete
- **Action:** eighth v0.3.2 reparse pass; finishes the ZMCC 2025 DESC sweep recommended by b0494 with the final slice `{6, 5, 2}` (raw on disk, no records yet). Formally exhausts ZMCC 2025 reparse-first inventory under v0.3.2.
- **Records written:** 1 (zmcc/2025/02)
- **Records deferred:** 2 (zmcc/2025/{6, 5} both `html_no_summary_pdf_no_match`)
- **Cumulative today:** 0/2000 fetches; ~6k tokens (parser script copy + report + gaps.md edits)
- **Yield this tick:** 1/3 = 33.3%
- **Five-consecutive-zero-discovery counter:** RESET to 0 (b0494 was 1; b0495 wrote 1)

## Tick prelude — host-side ref-cleanup intervention by Peter

The 12:34Z and 13:02Z scheduled ticks both aborted on `git pull --ff-only` with `fatal: bad object refs/remotes/origin/main.lock.bak.b0494.1.121136` — an empty 0-byte stale ref left over from b0494. The sandbox virtiofs mount blocks `unlink()` on every file under `.git/`, including by `rm`, `git update-ref -d`, and even `find -delete` (touch + write succeed; only deletion fails with EPERM). The b0493 SHA-write workaround was tried but failed because every `git update-ref` operation needs to first acquire a `.lock` file, which then can't be released. After the 13:02Z tick logged the failure and stopped per protocol step 1, Peter intervened on the host with:

```
chflags -R nouchg .git
find .git -name "*.lock.bak*" -print -delete
find .git -name "*.lock" -print -delete
rm -f .git/test_write
git fsck --no-dangling
```

`git fsck --no-dangling` returned clean. The repo unwedged immediately and this tick resumed at 13:14Z. The accumulating `_stale_locks_b04XX_*` files in the working tree (untracked, ~150 of them) are a separate cleanup concern that survives this tick — they are NOT touched by this batch.

## Targets and selection

Per b0494's next-tick recommendation: option (1) — finish the ZMCC 2025 DESC sweep with the three remaining untested-under-v0.3.2 candidates `{6, 5, 2}` (all previously deferred under batch-0364 with `html_no_summary_pdf_no_match`). Short batch (3 < MAX_BATCH_SIZE=8) — formally exhausts ZMCC 2025 reparse-first inventory under v0.3.2. All three HTML+PDF pairs already on disk; 0 fresh fetches consumed.

## Resolutions

- **[2025] ZMCC 2 — Godfrey Shamanena v Anti-Corruption Commission** (2025-02-06)
  - Outcome: `dismissed`
  - Detail: "We dismiss the petition for lack of"
  - Source: `pdf-tail-2pages[v032-tail:\bwe\s+(?:hereby\s+|therefore\s+|accordi]` — the active-voice "we dismiss" operative-verb pattern (one of the 24 v0.3.2 phrase additions Peter listed in the 2026-05-03 widening)
  - Judges (3-judge bench): Munalula (PC), Shilimi (DPC), Chisunka (JC). All three already resolved against canonical entries in `judges_registry.yaml`; no new aliases added.
  - Issue tags: Constitutional jurisdiction; limits of Constitutional Court; national values and principles (Arts. 173, 216) not independently justiciable; interpretation vs. administrative/judicial review; requirement for specific constitutional question to invoke jurisdiction.
  - Record id: `judgment-zm-2025-zmcc-02-godfrey-shamanena-v-anti-corruption-commission`
  - Supersedes b0364 deferral note `html_no_summary_pdf_no_match` (which had itself superseded the original generic `outcome_not_inferable_under_tightened_policy` deferral). RESOLVED line appended beneath the original gaps.md b0364 detailed entry per the reparse-first audit-policy non-negotiable; original entry not deleted.

## Deferrals (specific reason codes only — no generic `outcome_not_inferable_under_tightened_policy`)

- **[2025] ZMCC 6** (Miles Bwalya Sampa v Attorney General, 2024/CCZ/0024, 2025-03-24) — `html_no_summary_pdf_no_match`. Subpoena-disposition style ("Interlocutory subpoenas denied for lack of prior steps, specificity, and demonstrated relevance to Article 210 challenge"); the bare token "denied" applied to "interlocutory subpoenas" still falls outside both v0.3.2 and v0.3.1 SUMMARY/TAIL pattern pools — neither vocabulary covers a subpoena/interlocutory-application disposition.
- **[2025] ZMCC 5** (Miza Phiri Jr v Isaac Mwanza and Ors, 2024/CCZ/0021, 2025-03-24) — `html_no_summary_pdf_no_match`. Procedural-propriety holding ("A petitioner cannot file a new petition to challenge another pending petition; proper remedy is joinder, and such filings may be abuse of process"); no operative disposition verb in either v0.3.2 or v0.3.1 patterns.

Both deferrals received `RECONFIRMED-DEFERRED in batch-0495 (parser_v0.3.2)` notes appended beneath their original `gaps.md` entries (in the batch-0363 detailed section). No `gaps.md` entries were deleted.

## Integrity checks

- IDs unique across `records/judgments/` (93/93 — one new record this tick).
- All 20 required fields present on the new record.
- Both four-field provenance set (source_url, source_hash, fetched_at, parser_version) present and correct.
- `source_hash` matches sha256 of raw HTML on disk (verified by integrity_check_b0495.py).
- `raw_sha256` matches sha256 of raw PDF on disk.
- `outcome` ∈ enum (`dismissed`).
- `court` ∈ enum (Constitutional Court of Zambia).
- All `judges[*].role` ∈ enum (presiding, concurring, concurring).
- All three judges resolve in `judges_registry.yaml` (canonical or bare-surname).
- `issue_tags` non-empty (5 tags).
- `outcome_detail` passes the v0.3.1 `_detail_is_safe` filter (≥12 alphabetic chars, no blacklisted substrings, no leading lowercase mid-word fragment).
- `scripts/integrity_check_b0495.py` returns `INTEGRITY CHECK: PASS (1 record(s))`.

## Cumulative v0.3.2 yield

Across b0488..b0495: **15 records written / 59 attempted = 25.4%**.

| Batch | Cohort | Written | Attempted | Yield | Profile |
|-------|--------|---------|-----------|-------|---------|
| 0488  | ZMCC 2022 (judges_no_comma + html_no_summary, DESC entry) | 2 | 8 | 25.0% | parser-launch + in-batch regression patch |
| 0489  | ZMCC 2022 (judges_no_comma DESC continuation) | 3 | 8 | 37.5% | five-judge benches with v031-tail operative phrases |
| 0490  | ZMCC 2022 (judges_no_comma DESC completion) | 6 | 8 | 75.0% | judges_no_comma backlog cleared |
| 0491  | ZMCC 2022 (html_no_summary untested-under-v0.3.2) | 0 | 8 | 0.0% | declaratory/interpretive — vocabulary-blind |
| 0492  | ZMCC 2024 (num-ASC pivot)                       | 0 | 8 | 0.0% | declaratory/interlocutory — same blind spot |
| 0493  | ZMCC 2025 (DESC pivot, num {33..19})            | 3 | 8 | 37.5% | two SUMMARY hits on Peter-targeted phrases + one PDF-tail hit |
| 0494  | ZMCC 2025 (DESC continuation, num {18..7})      | 0 | 8 | 0.0% | declaratory / ratio-style cohort |
| 0495  | ZMCC 2025 (DESC finisher, num {6, 5, 2})        | 1 | 3 | 33.3% | "we dismiss" v032-tail hit on ZMCC 2 (this batch) |

ZMCC 2025 reparse-first inventory under v0.3.2 is now formally exhausted. ZMCC 2025 DESC totals across b0493/0494/0495: **4 written / 19 attempted = 21.1%**.

## Phase 5 progress

92 → 93 (target 100–160 landmark judgments). 7 short of low end.
Five-consecutive-zero-discovery completion criterion remains UN-FIRED (b0488/0489/0490 wrote, b0491/0492 zero, b0493 wrote 3, b0494 zero, b0495 wrote 1 — counter currently at 0 and resets on every non-zero tick).

## Next-tick recommendation

Per b0494's option (2): **inventory and pivot to ZMCC 2023**. Cohort size unknown to this tick. The next tick should:

1. Inventory `raw/zambialii/judgments/zmcc/2023/` for HTML+PDF pairs without corresponding records under `records/judgments/zmcc/2023/`.
2. Cross-reference against `gaps.md` for any ZMCC 2023 entries with addressable deferral reasons under v0.3.2.
3. Run a v0.3.2 reparse batch over the first 8 (DESC by num) — same `MAX_BATCH_SIZE=8`, same `b0488` frozen baseline pattern.

Option (3) — ZMSC older-year sweep — remains pending Peter's URL pattern confirmation per `approvals.yaml.zmsc_older_year_sweep_approval_note`; not actionable by scheduled tick until that confirmation lands.
