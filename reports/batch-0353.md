# Batch 0353 Report — Phase 5 (Judgments)
**Tick start (UTC):** 2026-04-29T17:46Z
**Tick end (UTC):**   2026-04-29T18:07:50Z
**Phase:** phase_5_judgments (approved + incomplete)
**Parser version:** 0.3.0 (frozen from b0344, byte-identical to b0352)

## Targets (8)

ZMCC 2023, most-recent-first sweep continuing from b0352 end-state:
`2023/{19, 18, 17, 16, 15, 14, 13, 12}`.

## Outcome

- Records written: **0**
- Records deferred: **8**
  - `2023/17` — PDF returned HTTP 404 (`https://zambialii.org/akn/zm/judgment/zmcc/2023/17/eng/source.pdf`); HTML on disk only. Parser deferred under `raw bytes not on disk` policy. Counted as a hard ZambiaLII gap, not a parser-policy deferral.
  - `2023/19, 18, 16, 15, 14, 13, 12` — all 7 deferred under `outcome_not_inferable_under_tightened_policy`. Summary heads do not match the locked SUMMARY_PATTERNS list and the PDF tail does not produce a sufficient outcome+detail pair under the locked anchor list.

Per BRIEF.md non-negotiable #1, no fabrication; raw bytes preserved on disk for re-parse without re-fetch when SUMMARY_PATTERNS / PDF anchors are next reviewed.

## Phase 5 progress

22/100–160 (unchanged from b0352).

## Deferrals — summary heads

- `zmcc 2023/19` — *outcome_not_inferable_under_tightened_policy*
  - Summary head: "Constitutional Court lacks jurisdiction over redundancy-related salary and damages claims; Industrial Relations Division is competent."
  - URL: https://zambialii.org/akn/zm/judgment/zmcc/2023/19/eng@2023-10-26
- `zmcc 2023/18` — *outcome_not_inferable_under_tightened_policy*
  - Summary head: "A district council election can only be annulled by a petition founded on Section 97 of the Electoral Process Act."
  - URL: https://zambialii.org/akn/zm/judgment/zmcc/2023/18/eng@2023-10-02
- `zmcc 2023/17` — *raw bytes not on disk*
- `zmcc 2023/16` — *outcome_not_inferable_under_tightened_policy*
  - Summary head: "Constitutional Court lacked jurisdiction to entertain a petition challenging nominations and rescinding resignations in parliamentary by-elections."
  - URL: https://zambialii.org/akn/zm/judgment/zmcc/2023/16/eng@2023-07-11
- `zmcc 2023/15` — *outcome_not_inferable_under_tightened_policy*
  - Summary head: "Whether the JCC can investigate pre-appointment misconduct and whether failure to follow Article 144 suspension procedure nullifies removal."
  - URL: https://zambialii.org/akn/zm/judgment/zmcc/2023/15/eng@2023-10-26
- `zmcc 2023/14` — *outcome_not_inferable_under_tightened_policy*
  - Summary head: "Challenge to DC appointments dismissed for lack of evidence and because employment-related claims lie outside Constitutional Court jurisdiction."
  - URL: https://zambialii.org/akn/zm/judgment/zmcc/2023/14/eng@2023-03-10
- `zmcc 2023/13` — *outcome_not_inferable_under_tightened_policy*
  - Summary head: "AG not required to prosecute JCC complaints; JCC procedure and President’s suspension/removal of DPP were lawful."
  - URL: https://zambialii.org/akn/zm/judgment/zmcc/2023/13/eng@2023-09-28
- `zmcc 2023/12` — *outcome_not_inferable_under_tightened_policy*
  - Summary head: "Article 165 is prospective; Constitutional Court lacks jurisdiction to decide ordinary chieftaincy succession disputes."
  - URL: https://zambialii.org/akn/zm/judgment/zmcc/2023/12/eng@2023-09-26

## Integrity

`scripts/integrity_check_b0353.py`: **PASS (0 records)** — vacuously satisfied.

## Notes

- ZMCC 2023/17 is a hard ZambiaLII PDF-404. HTML kept on disk; gap logged.
- Parser policy (v0.3.0) intentionally not loosened this tick.
- corpus.sqlite NOT modified (no INSERTs since 0 records written; b0351/b0352 policy continues).
- B2 sync deferred to host (rclone not in sandbox).
