# Batch 0498 — Phase 5 ZMCC reparse, parser_v0.3.2

**Tick:** 2026-05-03T14:08Z (eleventh substantive v0.3.2 reparse tick; 18th substantive tick of UTC date 2026-05-03)
**Parser:** v0.3.2 (baseline `scripts/batch_0488_parse.py`; v0.3.1 baseline `scripts/batch_0360_parse.py` imported)
**Targets file:** `_work/b0498/targets.json`
**Mode:** REPARSE-FIRST per approvals.yaml.phase_5_judgments.reparse_first
**Fetches:** 0 (raw HTML+PDF already on disk for every target)
**Cumulative fetches today:** 0/2000
**Cumulative tokens today:** within budget (1,000,000)

## Targets (4 candidates — combined ZMCC 2026 + ZMCC 2021 untested-under-v0.3.2)

Per b0497 next-tick recommendation (option 1 + option 2): both the
ZMCC 2026 cohort (1 raw-on-disk no-record candidate, num 01) and
the ZMCC 2021 v0.3.2-amenable cohort (3 candidates: nums 21, 18,
12 — excluding 14, 15 which are `pdf_extraction_empty_likely_scanned`
and need OCR not parser widening) are addressed in a single tick.
Combined slice size 4, intentionally below MAX_BATCH_SIZE=8 because
the combined v0.3.2-amenable inventory is exhausted at 4 candidates.

| court | year | num | prior status under v0.3.1 |
|:------|:-----|:----|:--------------------------|
| zmcc  | 2026 |  01 | never written |
| zmcc  | 2021 |  21 | html_no_summary_pdf_no_match (b0371) |
| zmcc  | 2021 |  18 | html_no_summary_pdf_no_match (b0372) |
| zmcc  | 2021 |  12 | html_no_summary_pdf_no_match (b0372) |

## Outcome

| Metric             | Value |
|:-------------------|:------|
| Targets attempted  | 4 |
| Records written    | 1 |
| Records deferred   | 3 |
| Yield              | 25.0% |
| Cumulative v0.3.2 yield (b0488..b0498) | 19/79 = 24.1% |
| Phase 5 progress   | 96 → 97 (target 100–160) |
| Records short of low end | 3 |
| Five-consecutive-zero-discovery counter | 0 (substantive write this tick) |

## Resolved (1)

- **`judgment-zm-2021-zmcc-21-mulubisha-v-attorney-general`**
  ([2021] ZMCC 21, 30 March 2021).
  Outcome `dismissed`, detail "The respondent's application to
  correct an alleged accidental omission was dismissed for failure
  to show a prima facie slip; procedural irregularity deemed
  curable" via the v0.3.2 SUMMARY pattern
  `(?:application|petition|appeal|challenge) is dismissed/refused`
  family — specifically the "is dismissed" form widened on
  2026-05-03. Three-judge bench: Mulonda JJC (presiding), Mulenga
  JJC, Munalula JJC. All three resolve in `judges_registry.yaml`
  as existing canonical entries.
  Source URL: https://zambialii.org/akn/zm/judgment/zmcc/2021/21/eng@2021-03-30
  source_hash sha256:f327a3a7a6f6b17809e066b847f45cf2cfc7f1659c7afd3d25cc70d43f0705db
  raw_sha256 0b28f1f0175a62bbb8fabb6f8ec1322eadc1df101e8edb25d0d24022f64033c7

## Deferred (3)

All three `html_no_summary_pdf_no_match` re-tested under v0.3.2's
widened SUMMARY_PATTERNS_V032, PDF_TAIL_PATTERNS_V032 and
ORDER_INTRO window-scan resolver:

- **zmcc/2026/1** (Tresford Chali v The JCC, 2026-01-20) — pure
  procedural-routing declaratory holding ("must proceed by judicial
  review … not by original petition"); no operative dispositive
  verb in either pool.
- **zmcc/2021/18** (Chapter One Foundation v AG, 2021-08-18) —
  declaratory/interpretive question framing on constitutional
  gender-parity nominations; no operative-verb match.
- **zmcc/2021/12** (Dipak Patel v Minister of Finance, 2021-06-30)
  — interpretive question framing on Article 63(2)(d) public
  borrowing approval; no operative-verb match. Previously moved
  through `multi_judge_separate_opinions_no_clear_majority_disposition`
  (v0.3.0) → `html_no_summary_pdf_no_match` (v0.3.1) →
  `html_no_summary_pdf_no_match` (v0.3.2).

## Integrity

- `scripts/integrity_check_b0498.py`: PASS (1/1 new records)
- New-record judges resolution: 3/3 PASS against `judges_registry.yaml` (existing canonical entries, no new aliases)
- Source-hash spot recompute: PASS (sha256 of raw HTML matches `source_hash`; sha256 of raw PDF matches `raw_sha256`)
- Corpus-wide xref resolution: 0 unresolved
- Corpus-wide source_hash resolution: 97/97 records' source_hash present in raw/ sha256 index (3203 raw files / 2926 unique sha256)
- judges_registry.yaml: unchanged this tick (3 new alias-resolutions all matched existing canonical entries)
- Outcome detail-safety filter: PASS (no blacklisted substrings, ≥12 alphabetic chars, no leading lowercase mid-word fragment)

## v0.3.2 cohort exhaustion summary (post-tick)

After b0498, the complete ZMCC raw-on-disk no-record reparse-first
inventory under parser_v0.3.2 is **FORMALLY EXHAUSTED** across
all years. Only `pdf_extraction_empty_likely_scanned` candidates
remain (zmcc/2021/14, zmcc/2021/15, zmcc/2022/16, zmcc/2025/19);
those need OCR not parser widening.

## Files changed

- new: `_work/b0498/targets.json`
- new: `_work/b0498/parse_summary.json`
- new: `scripts/batch_0498_parse.py` (copy of `batch_0497_parse.py` with WORK directory pointer updated to `_work/b0498`)
- new: `scripts/integrity_check_b0498.py` (copy of `integrity_check_b0497.py` with WORK directory pointer updated)
- new: `records/judgments/zmcc/2021/judgment-zm-2021-zmcc-21-mulubisha-v-attorney-general.json`
- modified: `gaps.md` (RECONFIRMED-DEFERRED notes for 3 deferrals + new ## Batch 0498 section)
- modified: `provenance.log` (1 entry for the new record)
- modified: `costs.log` (batch-0498 line)
- modified: `worker.log` (tick start/end markers)

## Next-tick recommendation

The v0.3.2 reparse-first inventory is now empty across all ZMCC
years. Subsequent scheduled ticks will be audit-only zero-yield
ticks (returning to the b0375..b0487 idle pattern) until one of
the following human-approved unblocks lands:

1. **ZMSC older-year sweep** — approved by Peter 2026-05-03 per
   `approvals.yaml.zmsc_older_year_sweep_approved: true` but gated
   on Peter confirming the canonical source URL pattern. Not
   actionable by scheduled tick until that confirmation lands.
2. **OCR pass** for the 4 `pdf_extraction_empty_likely_scanned`
   candidates. Requires OCR pipeline approval.
3. **Parser_v0.3.3 widening** for the recurring deferral families
   (declaratory/interpretive ratios, jurisdictional-routing,
   joinder-as-disposition, subordinate-clause dismissed,
   nullified-and-discharged). Requires Peter approval per BRIEF.md
   non-negotiable on parser vocabulary changes.

Five-consecutive-zero-discovery completion criterion will fire
after 5 consecutive audit-only ticks. approvals.yaml NOT modified
per Phase 5 human-only confirmation rule.
