# Batch 0506 — judgment-ingestion-worker tick (FIRST substantive)

**Tick:** 2026-05-03T17:18Z
**Worker:** judgment-ingestion-worker (dedicated scheduled task; budget 500 fetches/day separate from main worker's 2000/day)
**Parser:** v0.3.2 (baseline `scripts/batch_0498_parse.py`, v0.3.1 baseline `scripts/batch_0360_parse.py` imported)
**Targets file:** `_work/b0506/targets.json`
**Mode:** SCZ sweep (post-Phase-5; reparse-first inventory exhausted at b0498)
**Fetches consumed:** 15 / 500 today

## Context

This is the first substantive tick of the dedicated
**judgment-ingestion-worker** scheduled task that Peter set up after
Phase 5 was procedurally completed at b0503 (5-consecutive-zero
rule). Phase 5 stays `complete: true` in approvals.yaml; this worker
continues judgment ingestion via the dedicated scheduled task per
Peter's completion note.

The v0.3.2 reparse-first inventory was confirmed exhausted (per
b0498's formal-exhaustion report). Per SKILL, this tick proceeded to
SCZ sweep — most-recent year first, working backwards.

## Targets (8)

| court | year | num | reason |
|:------|:-----|:----|:-------|
| zmsc  | 2026 |  2  | gap (we had 1, 4, 7, 10) |
| zmsc  | 2026 |  3  | gap |
| zmsc  | 2026 |  6  | gap |
| zmsc  | 2026 |  8  | gap |
| zmsc  | 2026 |  9  | gap |
| zmsc  | 2025 |  1  | head-of-year gap (we had 8-30) |
| zmsc  | 2025 |  2  | head-of-year gap |
| zmsc  | 2025 |  3  | head-of-year gap |

URL pattern (probed and confirmed): `https://zambialii.org/akn/zm/judgment/zmsc/{year}/{num}/eng` — 302 redirects to the date-suffixed canonical `/eng@YYYY-MM-DD`. PDF at `/source.pdf`.

## Outcome

| Metric             | Value |
|:-------------------|:------|
| Targets attempted  | 8 |
| Records written    | 5 |
| Records deferred   | 3 |
| Yield              | 62.5% |
| Phase 5 corpus growth | 97 → 102 |
| Court breakdown after tick | 25 SCZ/ZMSC + 5 ZMSC-new + 72 ZMCC = 102 |

## Resolved (5)

- **`judgment-zm-2026-zmsc-06-ventriglia-and-another-v-finance-bank-zambia-limit`**
  ([2026] ZMSC 6, 10 March 2026). Outcome `allowed`, detail "Leave granted to appeal to resolve whether an unsigned memorandum and mischaract…" via v0.3.2 SUMMARY pattern `\b(?:application|petition|appeal|leave|relief)\s+(?:is\s+)?...granted\b`. Bench: Musonda DCJ, Kaoma JJS, Kabuka JJS.
- **`judgment-zm-2026-zmsc-08-konkola-copper-mines-plc-v-attorney-general-and-or`**
  ([2026] ZMSC 8, 31 March 2026). Outcome `remitted`, detail "In doing so, we remit the matter back to…" via v0.3.1 PDF tail pattern `\bwe\s+remit\b`. Bench: Musonda DCJ, Kaoma JJS, Mutuna JJS.
- **`judgment-zm-2026-zmsc-09-kapopo-mutele-patel-v-the-people`**
  ([2026] ZMSC 9, 16 April 2026). Outcome `dismissed`, detail "Recognition by familiar witnesses and corroboration upheld the murder conviction…" via v0.3.1 SUMMARY pattern. Bench: Chinyama, Kaoma, Musonda.
- **`judgment-zm-2025-zmsc-02-davies-chishala-and-anor-v-the-people`**
  ([2025] ZMSC 2, 16 January 2025). Outcome `allowed`, detail "Consequently, we find merit in this appeal and we allow it" via v0.3.1 PDF tail pattern. Bench: Malila CJ, Hamaundu JJS, Kaoma JJS.
- **`judgment-zm-2025-zmsc-03-gillian-kasempa-mutinta-v-new-future-financial-com`**
  ([2025] ZMSC 3, 10 January 2025). Outcome `overturned`, detail "Since the conveyance is null and void, we set aside the judgment of the Cour…" via v0.3.1 PDF tail pattern `\bwe\s+set\s+aside\b`. Bench: Hamaundu JJS, Wood JJS, Kabuka JJS.

## Deferred (3)

All three under `html_no_summary_pdf_no_match`:

- **zmsc/2026/2** — Application for leave to appeal (refused). Summary uses procedural framing ("Applicants failed to show…") that doesn't match v0.3.2 operative-verb patterns.
- **zmsc/2026/3** — Application for leave to appeal (granted). Same procedural framing pattern, opposite outcome — both miss v0.3.2 vocabulary.
- **zmsc/2025/1** — Declaratory question on Legal Practitioners' Rules. Pure question-framing without operative dispositive verb.

All retain raw HTML+PDF on disk; gaps.md updated with full deferral entries. These three are characteristic of the **leave-to-appeal / declaratory framing** family and would benefit from a parser_v0.3.3 widening (pending Peter approval).

## Judges registry

6 new canonical SCZ entries auto-added with first-seen timestamp:

| canonical | titles | first_seen_in |
|:----------|:-------|:--------------|
| Musonda   | DCJ    | judgment-zm-2026-zmsc-06 |
| Kaoma     | JJS, J | judgment-zm-2026-zmsc-06 |
| Kabuka    | JJS    | judgment-zm-2026-zmsc-06 |
| Mutuna    | JJS    | judgment-zm-2026-zmsc-08 |
| Chinyama  | J      | judgment-zm-2026-zmsc-09 |
| Malila    | CJ     | judgment-zm-2025-zmsc-02 |
| Hamaundu  | JJS    | judgment-zm-2025-zmsc-02 |
| Wood      | JJS    | judgment-zm-2025-zmsc-03 |

(Note: Kaoma seen with both `JJS` and bare `J` titles across decisions — registered with both title-history entries.)

## Integrity

- 5/5 unique IDs
- 5/5 core provenance complete (source_url, source_hash, fetched_at, parser_version)
- 5/5 source_hash shape valid (sha256:...)
- 5/5 raw_sha256 matches on-disk PDF
- 5/5 judges[*].name resolve in judges_registry.yaml
- 0 duplicate IDs in corpus (102 total unique)
- 0 schema regressions on corpus.sqlite tables

## Files changed

- new: `_work/b0506/targets.json`, `_work/b0506/parse_summary.json`, `_work/b0506/fetch_results.json`
- new: `scripts/batch_0506_zmsc_fetch.py`, `scripts/batch_0506_zmsc_parse.py`
- new: 5 `records/judgments/zmsc/{2025,2026}/judgment-zm-*.json`
- new: 8 raw HTML + 8 raw PDF files under `raw/zambialii/judgments/zmsc/{2025,2026}/` (3 are deferreds, 5 are written)
- modified: `corpus.sqlite` (records, judgments_meta, records_fts each +5)
- modified: `judges_registry.yaml` (8 new aliases across 6 canonical names — Wood was already canonical)
- modified: `gaps.md` (## Batch 0504 section with 3 deferred entries)
- modified: `provenance.log` (5 new lines)
- modified: `costs.log` (batch-0504 lines)
- modified: `worker.log` (tick start/end markers)

## Next-tick recommendation

Continue ZMSC head-of-year sweep with the 7 remaining 2025 gaps
(nums 4, 5, 6, 7, 26, 28, 31) and probe ZMSC 2024 listing if the
2025 head clears within the same tick. Also re-attempt the 3
deferreds if a parser_v0.3.3 widening lands.

B2 sync deferred to host (rclone not available in sandbox).
