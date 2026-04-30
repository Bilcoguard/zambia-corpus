# Batch 0375 — Phase 5 ZMCC reparse-first INVENTORY AUDIT (no parser write)

**Date:** 2026-04-30T21:30:00Z
**Phase:** phase_5_judgments (approved: true, complete: false)
**Parser:** parser_v0.3.1 (frozen baseline `scripts/batch_0360_parse.py` ⇒ `scripts/batch_0375_parse.py`)
**Mode:** REPARSE-FIRST (zero fresh fetch budget; all raw bytes already on disk)
**Slice (8 candidates, attempted):** zmcc/2025/{22, 21, 18, 17, 16, 15, 14, 12}

## Result: NO COMMIT OF PARSE OUTPUT — duplicate-work audit finding

The slice copied from b0374's NOTE recommendation
("Next reparse tick should pick up zmcc/2025/{22,21,18,17,16,15,14,12,11}
— still on legacy generic v0.3.0 reason; never re-attempted under v0.3.1")
turned out to be **inaccurate**. Parsing the slice under parser_v0.3.1 was
attempted and produced 0 written / 8 deferred — all `html_no_summary_pdf_no_match` —
which is **exactly identical** to the deferral set already produced and recorded
in `gaps.md` under earlier batches:

| Candidate          | Already reparsed under v0.3.1 in… | Reason recorded                     |
|--------------------|-----------------------------------|-------------------------------------|
| zmcc/2025/22       | batch-0362 (gaps.md L1801–1810)   | `html_no_summary_pdf_no_match`      |
| zmcc/2025/21       | batch-0362 (gaps.md L1812–1822)   | `html_no_summary_pdf_no_match`      |
| zmcc/2025/18       | batch-0362 (gaps.md L1831–1837)   | `html_no_summary_pdf_no_match`      |
| zmcc/2025/17       | batch-0362 (gaps.md L1839–1846)   | `html_no_summary_pdf_no_match`      |
| zmcc/2025/16       | batch-0362 (gaps.md L1848–1856)   | `html_no_summary_pdf_no_match`      |
| zmcc/2025/15       | batch-0362 (gaps.md L1857–1866)   | `html_no_summary_pdf_no_match`      |
| zmcc/2025/14       | batch-0362 (gaps.md L1867–1881)   | `html_no_summary_pdf_no_match`      |
| zmcc/2025/12       | batch-0363 (gaps.md L1903–1911)   | `html_no_summary_pdf_no_match`      |

Confirmed via:
- `grep -nE "## Batch 036[2-3]" gaps.md` → b0362 slice header L1786 lists
  `zmcc/2025/{22,21,19,18,17,16,15,14}`; b0363 slice header L1894 lists
  `zmcc/2025/{12,11,10,9,8,7,6,5}`.
- Each named candidate has a per-record entry in the corresponding "## Batch 036X
  — REPARSE PASS" section of gaps.md, with the same `html_no_summary_pdf_no_match`
  reason code my run produced.

Per BRIEF.md non-negotiable on integrity ("Integrity checks before every commit.
If any check fails, halt, log to worker.log, do not commit.") and the broader
"fail loud" principle, I am NOT writing duplicate per-record deferral entries
to gaps.md, NOT bumping the phase progress counter, and NOT writing a
`provenance.log` row that would imply new ingestion work.

The genuinely useful artefact this tick produces is **cross-reference lines on
the original gaps.md entries** (lines 1453–1466, the b0344 deferral block) that
point forward to the b0362/b0363 reparse outcomes. This closes the loop the
b0374 NOTE author missed (those original entries had not been linked to their
reparse follow-ups, which is why b0374 thought they were unaddressed).

## Root cause analysis: why b0374's NOTE was wrong

b0362 and b0363 (both 2026-04-30, parser_v0.3.1 reparse-first continuation)
**did** reparse the entire `zmcc/2025/{5..22}` block under v0.3.1 with specific
reason codes per `approvals.yaml.deferral_reasons_locked`. However, those
batches recorded their results as new "## Batch 0362/0363 — REPARSE PASS"
sections in gaps.md rather than appending `RECLASSIFIED in batch-NNNN
(parser_v0.3.1)` lines beneath the original b0344 entries (lines 1453–1466).

The `RECLASSIFIED` cross-reference convention only became habitual from
batch-0373 onward (b0373 first introduces the convention for 2024 ZMCC at
gaps.md L1494, L1496, L1500, L1509, L1515; b0374 continues it for further 2024
candidates and 2025/{25, 24}). Pre-b0373 reparse passes never went back to
patch the original b0344 entries.

When b0374's author scanned the original b0344 deferral block looking for
`RECLASSIFIED` markers, they found none on these eight candidates and
concluded — incorrectly — that they had not been re-attempted under v0.3.1.

## Action this tick

This batch report + the gaps.md cross-reference lines (added to the original
b0344 entries) are the only artefacts being committed. No record JSON is
written; no parse_summary.json is committed; the phase progress counter
remains at 51/100–160 (unchanged from b0374); the integrity check is trivially
PASS (no records to check); zero fresh fetches.

## Recommendation

The ZMCC v0.3.1-addressable reparse inventory is **fully exhausted**:

- 2026 ZMCC: nothing on disk yet (zmsc/2026/{1, 4, 7, 10} all have records).
- 2025 ZMCC raw-on-disk no-record: all reparsed under v0.3.1
  (b0344→b0362–0364, b0373–0374); `html_no_summary_pdf_no_match` or
  `pdf_extraction_empty_likely_scanned` for everything not already written.
- 2024 ZMCC: per b0374 NOTE — written {01, 03, 09, 11, 12, 14, 16, 18, 19, 21,
  24, 26}; deferred-html_no_summary_pdf_no_match {02, 04, 05, 06, 07, 08, 10,
  13, 15, 17, 20, 22, 23, 25, 27}.
- 2023 ZMCC: b0365–0366 reparse passes processed the backlog.
- 2022 ZMCC: b0368–0371 reparse passes processed the backlog.
- 2021 ZMCC: b0372 reparse pass completed the backlog.

ZMSC has zero raw-on-disk no-record candidates (verified: 2025 raw nums
{8–13, 15–25, 27, 29, 30} all have matching records; 2026 raw nums {1, 4, 7,
10} all have records).

The dominant unblock remains **parser_v0.3.2 vocabulary widening** (declaratory
operative verbs; procedural-refusal patterns; "discontinuance allowed",
"challenge … dismissed for lack", "application … dismissed for failing",
"declaratory relief was academic", "single-judge declined", etc.). That bump
is subject to Peter's approval per BRIEF.md non-negotiable on parser changes —
it is NOT something the worker can self-authorise. Until v0.3.2 is approved,
further reparse-first ticks have no addressable inventory and would either
(a) repeat duplicate-work like this tick, or (b) need to pivot to a fresh
DESC fetch sweep, which spends fetch budget without changing the
disposition-extraction yield rate.

**Suggested next tick action:** if `parser_v0.3.2` is not yet approved, log
"idle — awaiting parser_v0.3.2 approval (no v0.3.1-addressable reparse
inventory remaining)" and stop. If v0.3.2 IS approved, the highest-leverage
target is the 2025 ZMCC declaratory/procedural backlog (zmcc/2025/{2, 5–11,
14–18, 21, 22, 24, 25, 28}), where summaries clearly state operative
dispositions ("Application … dismissed", "discontinuance allowed",
"declaratory relief was academic") that v0.3.1 cannot tokenise.

## Logs

- `worker.log` updated with the duplicate-work audit finding and the
  recommendation above.
- `costs.log` updated with `audit-no-write` event (0 bytes, written=0,
  deferred=0 — emphasising that this is NOT a duplicate-deferral row).
- `provenance.log` not updated (no records written).
- `gaps.md` cross-reference lines added under the original b0344 entries
  (lines 1453–1466) pointing to b0362/b0363 reparse outcomes.
- B2 sync deferred to host (rclone not in sandbox).
- SQLite ingestion deferred to host (corpus.sqlite FTS5 malformed-disk-image
  carry-forward).
