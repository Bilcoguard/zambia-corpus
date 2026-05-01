# batch-0397

- Tick start: 2026-05-01T09:04:15Z
- Phase: phase_5_judgments (approved+incomplete)
- Mode: substantive audit-only idle tick (22nd consecutive — b0375..b0383, b0385..b0397)
- Yield: 0 records written / 0 deferred / 0 fresh fetches
- Cumulative today: 0 / 2000 fetches; 0 / 1,000,000 tokens (UTC date 2026-05-01, 16th substantive tick of new day)
- Wall-clock: well under 20-min budget

## Pre-flight

- `find .git -name "*.lock" -delete` and `*.lock.bak -delete` clean (no in-`.git` matches; pre-existing
  `_stale_locks_b03**_*.lock.bak` quarantine residue at repo root persists ~30+ files — harmless).
- `git pull --ff-only` → "Already up to date." Carry-forward
  `.git/objects/maintenance.lock` "Operation not permitted" warning persists; non-blocking.
- `approvals.yaml` unchanged since 2026-04-30T15:36:40Z (commit b24a938) — phase_5_judgments still approved+incomplete;
  parser_v0.3.2 / OCR / ZMSC fresh-DESC-sweep approvals still pending (~17h 30m since approvals last touched).

## Reparse-first inventory audit

- ZMCC: 142 HTML / 141 PDF / 53 records (89 missing → all already in gaps.md as v0.3.1 deferrals)
- ZMSC: 26 HTML / 24 PDF / 24 records (2 HTML stems outside canonical pattern, non-blocking)
- SCZ:  1 record
- Total records: 78 (unchanged from b0378 through b0396)
- v0.3.1 reparse inventory remains FULLY EXHAUSTED — no addressable deferred candidates remain at v0.3.1 vocabulary level.

## gaps.md cross-check

(line-frequency, `grep -c`; identical to b0386–b0396)

| count | reason |
| ----- | ------ |
| 114   | html_no_summary_pdf_no_match |
|  14   | parser_v0.3.1_judges_no_comma_unhandled |
|  10   | pdf_extraction_empty_likely_scanned |
|   2   | multi_judge_separate_opinions_no_clear_majority_disposition |
|  49   | outcome_not_inferable_under_tightened_policy (v0.3.0 generic, retained historical; banned for new deferrals per approvals.yaml) |
|   0   | parser_v0.3.1_token_unhandled |
|   0   | outcome_inferred_but_detail_unsafe |
|  21   | RESOLVED in batch (resolved-line tally, unchanged since v0.3.1 inventory exhausted) |

`gaps.md` last commit 2026-04-30T21:40:59+00:00 — unchanged since b0379.

## Integrity spot-check (no records written, trivial PASS)

- 6-record provenance spot-check (3 latest ZMCC + 3 latest ZMSC):
  - 3/3 ZMCC (parser 0.3.1) carry the canonical schema (id/court/case_name/date_decided/outcome + provenance) — all OK.
  - 3/3 ZMSC (parser 0.5.0) carry the v0.5.0 schema (uses `parties` instead of `case_name`, `delivery_date` instead of `date_decided`, no `outcome` enum). All required-by-its-own-schema provenance fields (source_url, source_hash, fetched_at, parser_version, id) present and JSON parses clean. Schema-mixing hazard documented in worker.log b0394; will be reconciled when parser_v0.3.2 / migration is approved.
- 3/3 ZMCC source_hash recompute spot-check (judgment-zm-2024-zmcc-01, -03, -09) → all match the on-disk raw HTML byte-for-byte.

## Fresh DESC sweep — continuing to defer

Per b0376–b0396 rationale:

1. ~85% of existing ZMCC backlog defers `html_no_summary_pdf_no_match` (parser-vocabulary limitation a fresh
   sweep would reproduce while consuming fetch budget v0.3.2 will be far more efficient with).
2. ZMSC schema-mixing hazard — existing 24 ZMSC records use parser_v0.5.0 schema; v0.3.1 sweep would mix two
   schemas and integrity checks do not catch schema-mixing.

## Escalation (22nd consecutive substantive idle tick)

Three non-overlapping unblocks ranked by yield, all subject to Peter approval per BRIEF.md non-negotiable on parser changes:

1. **parser_v0.3.2 vocabulary widening** — highest yield against existing ZMCC backlog (~70/89 deferred candidates).
2. **OCR pipeline** for 4 scanned-PDF candidates (zmcc/2021/{14,15}, zmcc/2022/16, zmcc/2025/19).
3. **ZMSC fresh DESC sweep** into 2024/2023 (schema-mixing hazard — needs explicit approval).

Recommended ordering: (1) → (2) → (3).

## Outcome

- Phase 5 progress: 78 / 100–160 target (unchanged from b0378).
- Phase 5 completion criterion (five consecutive zero-discovery ticks) remains fired since b0379; `approvals.yaml` NOT modified per the Phase 5 human-only confirmation rule.
- B2 sync deferred to host (rclone not in sandbox).
- SQLite ingestion deferred (corpus.sqlite FTS5 malformed-disk-image carry-forward; canonical source remains `records/*.json`).

