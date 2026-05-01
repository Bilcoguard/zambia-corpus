# Batch 0378 — Audit-only tick (4th consecutive)

**Timestamp:** 2026-04-30T23:06:35Z
**Phase:** 5 (judgments) — approved+incomplete
**Action:** Inventory audit; no parser run; no fresh fetches; no records written.
**Outcome:** v0.3.1 reparse inventory remains FULLY EXHAUSTED.

## Pre-flight

- `git pull --ff-only` succeeded after repairing zero-byte
  `refs/remotes/origin/main.lock.bak.1777588653` by writing the current
  `origin/main` SHA into it (sandbox cannot unlink permission-bound
  refs; in-place repair is the established workaround). Two related
  stale lock-bak refs (`main.lock.bak.b0293_close`,
  `main.lock.bak_b0365b_2`) carry valid SHAs and pose no fetch
  hazard.
- approvals.yaml unchanged since 2026-04-30 03:23:12Z. parser_v0.3.2
  approval and OCR pipeline approval both still pending.

## Inventory snapshot

| Source | Raw HTML+PDF | Records | Missing |
|--------|--------------|---------|---------|
| ZMCC 2021 | 13 | 8 | 5 |
| ZMCC 2022 | 34 | 5 | 29 |
| ZMCC 2023 | 25 | 8 | 17 |
| ZMCC 2024 | 27 | 12 | 15 |
| ZMCC 2025 | 33 | 11 | 22 |
| ZMCC 2026 | 10 | 9 | 1 |
| ZMCC total | 142 | 53 | 89 |
| ZMSC 2025 | 20 | 20 | 0 |
| ZMSC 2026 | 4 | 4 | 0 |
| ZMSC total | 24 | 24 | 0 |
| Root judgments/ | — | 1 | — |
| **Phase 5 total** | **166** | **78** | **89** |

## Programmatic gaps.md cross-check

- Iterated every `raw/zambialii/judgments/zmcc/{2021..2026}/*.html` slug.
- Extracted canonical `zmcc/YEAR/N` from each slug.
- Confirmed presence in gaps.md via `grep -E "zmcc/Y/N\b|zmcc/Y/0N\b"`.
- Result: **89 / 89 missing ZMCC candidates referenced in gaps.md** under
  v0.3.1 specific reason codes. Zero uncatalogued candidates.

## Reparse decision

Per BRIEF.md "Reparse-first policy" and approvals.yaml `reparse_first: true`:
no v0.3.1-addressable inventory remains. Three prior audit ticks
(b0375, b0376, b0377) reached the same conclusion. Re-running v0.3.1
on any subset of the 89 catalogued candidates would reproduce the same
deferrals (verified empirically by b0375 against zmcc/2025/{22..12}).

## Fresh DESC sweep decision

Continuing to defer per b0376 rationale, now confirmed across four
consecutive ticks: ~85% of the existing ZMCC backlog defers
`html_no_summary_pdf_no_match`, a parser-vocabulary limitation that
older ZMCC/ZMSC years would reproduce while consuming fetch budget that
parser_v0.3.2 will spend far more efficiently once approved. ZMSC raw
inventory is fully parsed; older ZMSC years would require fresh fetches
into 2024 and earlier.

## Recommendation (escalation)

**Four consecutive idle ticks** (b0375 → b0378) confirm that Phase 5
has hit a parser-vocabulary ceiling. Dominant unblocks remain:

1. **parser_v0.3.2 vocabulary widening** — declaratory operative verbs;
   procedural-refusal patterns; `discontinuance allowed`,
   `challenge … dismissed for lack`, `application … dismissed for
   failing`, `declaratory relief was academic`, `single-judge
   declined`, `court refused stay`. Subject to Peter approval per
   BRIEF.md non-negotiable on parser changes.

2. **OCR pipeline approval** — for 4 `pdf_extraction_empty_likely_scanned`
   candidates: zmcc/2021/{14,15}, zmcc/2022/16, zmcc/2025/19.

3. **Older-year ZMSC fresh DESC sweep** (zambialii.org seed page back
   into 2024 / 2023 / 2022 / 2021 / 2020) — would discover new raw
   bytes parser_v0.3.1 may handle better than the ZMCC backlog. Budget
   cost: ~1 seed page fetch + N judgment fetches per tick at the
   configured 5-second rate limit.

## Wall-clock & budget

- Wall-clock: ~6 minutes of the 20-minute ceiling.
- Fetches: 0 (cumulative today ~22/2000, 1.1%).
- Tokens: well under 1,000,000/day cap.
- B2 sync: deferred to host (rclone not in sandbox).
- SQLite ingestion: deferred to host (corpus.sqlite FTS5
  malformed-disk-image carry-forward; canonical source remains
  records/*.json).

## Integrity check

Trivial PASS — no records written; schema/registry/hash clauses not
exercised.
