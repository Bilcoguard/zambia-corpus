# Batch 0520 — Judgment Ingestion Report

**Date:** 2026-05-04 (UTC)
**Worker:** judgment-ingestion-worker (8th substantive tick)
**Time budget:** within 20-minute tick window
**Fetch budget today:** 85/500 (well within budget)

## Summary

- **Records written:** 2
- **Records deferred:** 5 (4 × `html_no_summary_pdf_no_match` interpretive-ratio family; 1 × `parser_v0.3.2_token_unhandled`)
- **404 confirmed:** 1 (zmsc/2023/13 — internal cadastre gap)
- **Judges added/updated:** 0 new canonical (6 existing re-confirmed: Malila CJ, Kaoma JJS, Kabuka JJS, Hamaundu JJS, Mutuna JJS, Chisanga JJS)
- **Integrity assertions:** 59/59 PASS
- **corpus.sqlite:** records 1818→1820, judgments_meta 128→130

## Work performed

### ZMSC 2023 most-recent-first sweep continuation
Per b0519 next-tick recommendation, fetched nums {17..10} (8 candidates):

| Num | Date | Outcome | Status |
|-----|------|---------|--------|
| 17 | 2023-10-19 | — | deferred (pensions: pre-existing-contract scope of statutory pensionable-age increase) |
| 16 | 2023-09-25 | — | deferred (Mental Health Act §4 capacity / safeguards) |
| 15 | 2023-08-30 | — | deferred (arbitration clause: court-stay obligation under professional rules) |
| 14 | 2023-05-24 | dismissed | **WRITTEN** (K.V. Wheels and Construction Ltd v Investrust Bank Plc) |
| 13 | — | — | 404 (cadastre gap) |
| 12 | 2023-06-22 | — | deferred (Lands Act §13(3): Lands Tribunal exclusivity over re-entry challenges) |
| 11 | 2023-06-08 | dismissed | **WRITTEN** (Kakunda and Ors v The People — aggravated robbery / corroboration / recent possession) |
| 10 | 2023-05-31 | — | deferred (`parser_v0.3.2_token_unhandled` — 6 MB PDF; flag for parser v0.3.3 token-window investigation) |

## Records written

### `judgment-zm-2023-zmsc-14-k-v-wheels-and-construction-ltd-v-investrust-bank`
- Citation: [2023] ZMSC 14
- Case number: SCZ/8/29/2021
- Date: 2023-05-24
- Judges: Malila CJ (presiding), Kaoma JJS, Kabuka JJS
- Outcome: **dismissed** — renewed leave to appeal refused; letter-of-credit disputes were factual/private, not points of law of public importance
- Issues: letters of credit, strict-compliance doctrine, UCP 600 Art. 34, leave-to-appeal threshold

### `judgment-zm-2023-zmsc-11-kakunda-and-ors-v-the-people`
- Citation: [2023] ZMSC 11
- Case number: APPEAL No. 52,53,54/2022
- Date: 2023-06-08
- Judges: Hamaundu JJS (presiding), Mutuna JJS, Chisanga JJS
- Outcome: **dismissed** — pdf-tail v031 match: "and we dismiss it"
- Issues: criminal law, identification evidence, accomplice corroboration, recent-possession doctrine, fingerprint absence

## Deferrals

- 4 records under `html_no_summary_pdf_no_match` (interpretive-ratio family, same v0.3.3-pending cohort as b0506/b0511/b0515/b0516/b0517/b0518/b0519): zmsc/2023/{17, 16, 15, 12}
- 1 record under `parser_v0.3.2_token_unhandled`: zmsc/2023/10 (6 MB PDF; parser exception during pdf-tail extraction — large document possibly with image overlays; defer for v0.3.3 large-doc handling)

## 404 boundary

- zmsc/2023/13 confirmed gap (internal cadastre numbering hole; consistent with prior internal gap at zmsc/2024/4 found in b0518)

## Judges registry

No changes — all 6 panelists already canonical. judges_registry.yaml unchanged.

## Integrity check

`scripts/integrity_check_b0520.py`: **PASSED 59 / FAILED 0** across 2 written records and corpus-wide duplicate-id check. 130 unique judgment IDs on disk.

## corpus.sqlite

In-place insert succeeded; verification reads confirm both new IDs present in `records` and `judgments_meta` with parser_version=0.3.2. records 1818→1820. judgments_meta 128→130. The transient FUSE-symptomatic raise on commit (matching b0504/b0511/b0515/b0516 pattern) did not prevent persistence — verified post-write. records_fts deferred to host-side rebuild.

## Approvals

`approvals.yaml` not modified (judgment-ingestion worker is read-only over approvals per non-negotiables).

## B2 sync

Deferred to host (rclone not in sandbox).

## Cohort cumulative (since b0504)

- 33 written, 26 deferred, 5 confirmed 404
- ZMSC 2024: 22 written / 12 deferred / 1 404 (closed)
- ZMSC 2023: 3 written / 9 deferred / 2 404 (in progress; 14 of ~23 attempted; ~9 remaining)

## Next tick recommendation

Continue ZMSC 2023 most-recent-first DESC sweep with nums {9..3} + close-out probe {2,1} (≈ 8 candidates). Expect mix of writeable and interpretive-ratio deferrals. Once ZMSC 2023 closes, pivot to ZMSC 2022 upper-boundary probe.
