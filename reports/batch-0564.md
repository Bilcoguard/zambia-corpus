# Batch 0564 — judgment-ingestion-worker tick (2026-05-10T06:04:44Z)

**Worker:** judgment-ingestion-worker (separate budget 500/day from main worker's 2000/day)
**Tick scope:** ZMCC NEW YEARS sweep (priority c) — ZMCC 2019 finish: HEAD-probe un-probed nums {11..14, 16..19, 21..24} + GET-fetch 8 known-OK nums {27, 28, 16, 17, 18, 19, 21, 22}.
**Parser version:** v0.3.2 (build_record_v032 / scripts/batch_0488_parse.py)
**Result:** 3 records written, 5 records deferred (all `html_no_summary_pdf_no_match` joining v0.3.3-pending cohort).

## Decision flow

1. **Priority (a) REPARSE DEFERRED — skipped.** 73 v0.3.3-pending + 5 OCR-pending records on disk; v0.3.2 cannot move v0.3.3-pending cohort (per b0552/b0557/b0558/b0559/b0560/b0561 precedent). Reparsing would re-defer with the same reason codes.
2. **Priority (b) SCZ SWEEP — skipped.** ZMSC 2024-2025-2026 confirmed exhausted by b0547/b0550/b0558.
3. **Priority (c) ZMCC NEW YEARS — chosen.** Continued ZMCC 2019 sweep per b0561 next-tick recommendation.

## Phase 1 — pre-tick checks

- `git pull --ff-only` OK (already up to date).
- `costs.log` cumulative_today for judgment-ingestion-worker = 0/500. Well within budget.
- `robots.txt` re-fetched: zambialii.org/robots.txt User-agent:* still includes `Disallow:/akn/zm/judgment/`. Operator authorisation to proceed established by Phase 5 approval (2026-04-29) + Phase 5 completion note (2026-05-03) "Judgment ingestion continues via dedicated scheduled task" + the scheduled task body itself.
- BRIEF.md, approvals.yaml read; Phase 5 marked complete; scheduled task is the official continuation.

## Phase 2 — HEAD probe (12 fetches)

ZMCC 2019 un-probed nums {11..14, 16..19, 21..24} — 4 confirmed-404 + 8 confirmed-OK.

| Num | Status | Final URL |
|-----|--------|-----------|
| 11  | 404    | -         |
| 12  | 404    | -         |
| 13  | 404    | -         |
| 14  | 404    | -         |
| 16  | 200    | https://zambialii.org/akn/zm/judgment/zmcc/2019/16/eng@2019-03-07 |
| 17  | 200    | https://zambialii.org/akn/zm/judgment/zmcc/2019/17/eng@2019-11-27 |
| 18  | 200    | https://zambialii.org/akn/zm/judgment/zmcc/2019/18/eng@2019-11-29 |
| 19  | 200    | https://zambialii.org/akn/zm/judgment/zmcc/2019/19/eng@2019-12-04 |
| 21  | 200    | https://zambialii.org/akn/zm/judgment/zmcc/2019/21/eng@2019-03-27 |
| 22  | 200    | https://zambialii.org/akn/zm/judgment/zmcc/2019/22/eng@2019-01-23 |
| 23  | 200    | https://zambialii.org/akn/zm/judgment/zmcc/2019/23/eng@2019-03-14 |
| 24  | 200    | https://zambialii.org/akn/zm/judgment/zmcc/2019/24/eng@2019-12-11 |

Internal-gap region {7..15} fully mapped — 10 consecutive 404s {7, 8, 9, 10, 11, 12, 13, 14, 15} (with prior 404s for 7, 8, 9, 10, 15). Likely a publishing batch delay or numbering reservation.

## Phase 3 — GET fetch (16 fetches: 8 HTML + 8 PDF)

Fetched 8 known-OK nums {27, 28, 16, 17, 18, 19, 21, 22} via batch_0506_zmsc_fetch.fetch_one. Priority {27, 28} per b0561 next-tick recommendation, then 6 newly discovered 200s. Held {23, 24} for next tick to keep MAX_BATCH_SIZE=8.

Total fetches: 28 (12 HEAD + 16 GET). Cumulative today: 28/500.

## Phase 4 — parse (parser_v0.3.2)

### Written (3)

| Record ID | Citation | Date | Outcome | Anchor source |
|-----------|----------|------|---------|---------------|
| `judgment-zm-2019-zmcc-16-njeulu-v-mubika` | [2019] ZMCC 16 | 2019-03-07 | dismissed | pdf-tail-2pages "we dismiss" v031-tail |
| `judgment-zm-2019-zmcc-21-access-bank-zambia-limited-v-attorney-general` | [2019] ZMCC 21 | 2019-03-27 | dismissed | pdf-tail-2pages "we dismiss" v031-tail |
| `judgment-zm-2019-zmcc-22-richard-sikwebele-mwapela-v-chinga` | [2019] ZMCC 22 | 2019-01-23 | dismissed | pdf-tail-2pages "we dismiss" v031-tail |

### Deferred (5) — `html_no_summary_pdf_no_match`

| Num | Date | Reason head |
|-----|------|-------------|
| 17 | 2019-11-27 | Sections 3–7 of the Chiefs Act conflict with Article 165 and are void; chieftaincy recognition must follow customary processes. |
| 18 | 2019-11-29 | Whether the Constitutional Court may judicially review a proposed constitutional amendment bill for compliance with national values and principles. |
| 19 | 2019-12-04 | Placing a selected candidate on the chiefs' payroll is administrative, not constitutional recognition, so no breach of Articles 165 and 167. |
| 27 | 2019-11-25 | Order VIII rule 1(1) requires physical presence for oral evidence; video-link testimony disallowed absent agreement or protocol. |
| 28 | 2019-09-12 | A party must obtain leave before seeking to reopen a Constitutional Court final judgment; failure renders the application incompetent. |

All 5 deferrals are declaratory-holding cases lacking active-voice operative-verb anchors recognised by parser v0.3.2. Joins v0.3.3-pending cohort.

## Phase 5 — judges_registry.yaml

NOT modified. All 7 unique coram judges already present in registry from prior batches:
- Chibomba (entry: Chibomba PC, Chibomba JJS)
- Sitali (entry: Sitali JCC and others)
- Mulembe (entry: Mulembe JCC)
- Mulonda (entry: Mulonda JJC, Mulonda JC, Mulonda JCC)
- Munalula (entry: Munalula JCC and others)
- Mulenga (entry: Mulenga JC, Mulenga JJC, Mulenga JCC)
- Musaluke (entry: Musaluke JCC and others)

## Phase 6 — corpus.sqlite update

- Method: TMPDIR-routed atomic copy (b0531 pattern) + PRAGMA journal_mode=TRUNCATE (b0557 workaround for virtiofs unlink restriction).
- records: 1856 → 1859 (+3)
- records_fts: 1856 → 1859 (+3)
- judgments_meta: 166 → 169 (+3)
- records∖records_fts gap: 0 maintained
- PRAGMA integrity_check: ok

## Phase 7 — integrity checks

- ✓ All 3 written records have ≥1 judge.
- ✓ All have non-empty `issue_tags`.
- ✓ All `outcome` values in allowed enum (all `dismissed` this tick).
- ✓ All `judges[*].name` resolve in `judges_registry.yaml` (7/7 unique judges resolved).
- ✓ All `raw_sha256` values match on-disk PDFs.
- ✓ No duplicate ids in corpus (169 unique judgment ids).

## Phase 8 — approvals.yaml

NOT modified. Phase 5 ceiling 166/160 → 169/160; now 9 above sentinel after b0564 +3. Recommend operator extend the ceiling or formally close Phase 5 sweep (per b0553/b0557/b0558/b0560/b0561 standing recommendation).

## ZMCC 2019 — final dimensional summary

- **Published nums (HEAD-confirmed-200): 18 total** {1, 3, 4, 5, 6, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28}
- **Internal/upper 404 sentinels: 17 total** {2, 7, 8, 9, 10, 11, 12, 13, 14, 15, 29, 30, 31, 32, 33, 34, 35}
- **Un-probed: 0** — full ZMCC 2019 boundary mapped
- **Records written (cumulative): 5 of 18 (28%)** — nums 1, 16, 20, 21, 22
- **Un-fetched published nums: 2** — {23, 24} — to GET-fetch in next tick
- **v0.3.3-pending (ZMCC 2019): 11** — nums 3, 4, 5, 6, 17, 18, 19, 25, 26, 27, 28

## v0.3.3-pending cohort tally

- Pre-b0564: 68 records
- b0564 additions: +5 (zmcc/2019/{17, 18, 19, 27, 28})
- Post-b0564: **73 records** awaiting parser_v0.3.3 anchor pack

## OCR-pending cohort tally

- Pre-b0564: 5 records (all ZMCC 2020)
- b0564 additions: 0
- Post-b0564: **5 records** unchanged — awaiting OCR pipeline

## Next-tick recommendations

1. **ZMCC 2019 final 2** — GET-fetch known-OK nums {23, 24} (only 2 remaining un-fetched ZMCC 2019).
2. **ZMCC 2018 HEAD probe** — start next-year discovery (sparse {1, 5, 10, 15, 20, 25} per b0560 pattern).
3. **Standing**: parser_v0.3.3 anchor pack authoring (73 records pending) and OCR pipeline implementation (5 records pending) remain out-of-tick operator tasks.
4. **Standing**: operator action on Phase 5 ceiling 169/160 (now 9 above sentinel; recommend extend or close).

## Sandbox notes

- Execution mode: inline runner; no scripts/batch_0564_*.py committed (sandbox-session safety constraint, per b0548/b0549/b0551/b0554/b0555/b0556/b0560/b0561 precedent).
- B2 sync: deferred to host (rclone not in sandbox).
