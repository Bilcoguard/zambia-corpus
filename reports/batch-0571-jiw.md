# Judgment batch 0571 — judgment-ingestion-worker tick

**Tick start**: 2026-05-10T18:15Z (session=eloquent-epic-johnson)
**Worker**: judgment-ingestion-worker (separate from main worker; budget 500 fetches/day)
**Pre-tick HEAD**: 56a6ae0 (origin/main, b0570 worker-tick committed; verified via `git pull --ff-only` returning "Already up to date" — full lock cleanup blocked by virtiofs Operation-not-permitted on .git/index.lock, .git/ORIG_HEAD.lock, .git/objects/maintenance.lock; all are 0-byte stale, dated 2026-05-10T18:12-18:13Z, mirrors b016/b017/b0562/b0563/b018/b0565/b0566 FUSE constraint; pull succeeded despite "warning: unable to unlink" message on maintenance.lock)
**Parser**: v0.3.2 baseline (scripts/batch_0498_parse.py) — `build_record_v032` (unchanged; b0571 imports it directly via inline runner; no derivative wrapper script committed per b0548..b0570 sandbox-session safety constraint precedent)

## Tick decision

- **Priority (a) REPARSE DEFERRED — *chosen*.** Per task instruction priority order. v0.3.3-pending cohort stands at 255 records under `html_no_summary_pdf_no_match`; 62 under `pdf_extraction_empty_likely_scanned` (OCR-pending); 3 under `parser_v0.3.2_token_unhandled`; 1 under `raw_bytes_not_on_disk` (404). Total deferred raw-on-disk: 257. Selected 8 ZMCC 2019 v0.3.3-pending candidates not previously retried since their initial deferral in b0561/b0564 (six b0561 deferrals + two b0564 deferrals).
- **Priority (b) SCZ SWEEP — not reached** (deferred records remain).
- **Priority (c) ZMCC NEW YEARS — not reached** (deferred records remain).

## Targets (8)

| court | year | num | initial defer batch | initial defer date |
|-------|------|-----|---------------------|--------------------|
| zmcc  | 2019 | 3   | b0561 | 2026-05-09 |
| zmcc  | 2019 | 4   | b0561 | 2026-05-09 |
| zmcc  | 2019 | 5   | b0561 | 2026-05-09 |
| zmcc  | 2019 | 6   | b0561 | 2026-05-09 |
| zmcc  | 2019 | 17  | b0564 | 2026-05-10 |
| zmcc  | 2019 | 18  | b0564 | 2026-05-10 |
| zmcc  | 2019 | 25  | b0561 | 2026-05-09 |
| zmcc  | 2019 | 26  | b0561 | 2026-05-09 |

All 8 raw HTML+PDF on disk under `raw/zambialii/judgments/zmcc/2019/`. Zero fetch cost (priority (a) reparse).

## Parse outcome (parser v0.3.2)

**0 records written, 8 redeferred — all under same reason code `html_no_summary_pdf_no_match`.**

| num | result    | reason                              | summary head |
|-----|-----------|--------------------------------------|--------------|
| 3   | redeferred | `html_no_summary_pdf_no_match`     | "Suspending a magistrate for a judicial decision violated judicial independence; suspension declared unlawful and damages awarded." |
| 4   | redeferred | `html_no_summary_pdf_no_match`     | "Placing a purported chief on payroll is an administrative act, not constitutional 'recognition', and customary selection disputes are non-constitutional." |
| 5   | redeferred | `html_no_summary_pdf_no_match`     | "The new Local Government Act prescribes two-and-a-half-year deputy terms and allows incumbents to seek re-election." |
| 6   | redeferred | `html_no_summary_pdf_no_match`     | "The Public Protector is an investigatory constitutional office, not a court, and is subject to High Court judicial review." |
| 17  | redeferred | `html_no_summary_pdf_no_match`     | "Sections 3–7 of the Chiefs Act conflict with Article 165 and are void; chieftaincy recognition must follow customary processes." |
| 18  | redeferred | `html_no_summary_pdf_no_match`     | "Whether the Constitutional Court may judicially review a proposed constitutional amendment bill for compliance with national values and principles." |
| 25  | redeferred | `html_no_summary_pdf_no_match`     | "Petition seeking enforcement of Bill of Rights was wrongly brought in Constitutional Court and dismissed as abuse of process." |
| 26  | redeferred | `html_no_summary_pdf_no_match`     | "Summons for judgment on admission dismissed because respondent gave no clear, unequivocal admission; each party bears own costs." |

The summary heads confirm the v0.3.3-pending pattern: each is a *declaratory* or *jurisdictional* holding ("declared unlawful", "void", "wrongly brought", "dismissed as abuse of process") which v0.3.2's outcome anchors do not reach. The pattern matches b0552's "8/8 redeferred" finding from 2026-05-09 — the v0.3.2 outcome vocabulary is genuinely insufficient for this cohort. Resolution path: parser_v0.3.3 anchor pack authoring (operator task, out-of-tick).

## Cohort movement

- **v0.3.3-pending** (`html_no_summary_pdf_no_match`): 255 → 255 (no change; the 8 records were already in this cohort and re-enter under same reason)
- **OCR-pending** (`pdf_extraction_empty_likely_scanned`): 62 → 62 (untouched this tick)
- **parser_v0.3.2_token_unhandled**: 3 → 3 (untouched this tick)

## Judges registry

`judges_registry.yaml` **NOT modified**. The parser short-circuits before judges parsing when `infer_outcome_v032` returns no outcome — this is by design in `build_record_v032` (returns deferral debug *before* `parse_judges_v032` is called when outcome is None). No new aliases observed.

## corpus.sqlite update

**No change.** No records written → no DB writes. The journal mode untouched. Pre-tick verification:

| metric | value |
|--------|-------|
| `records` | 1861 |
| `records_fts` | 1861 |
| `records − records_fts` gap | 0 |
| `judgments_meta` | 171 |
| `PRAGMA integrity_check` | `ok` |
| on-disk JSON count under records/judgments/ | 171 |

Post-tick: identical (no DB writes).

## Integrity checks (all pass)

- ✓ `records` = `records_fts` = 1861 (b0557 strict assertion)
- ✓ `judgments_meta` = 171 = on-disk JSON count
- ✓ No duplicate ids in DB or on disk (no records added)
- ✓ All 8 reparse targets have raw HTML+PDF on disk under `raw/zambialii/judgments/zmcc/2019/` (verified by `parse_summary.json` showing reason codes other than `raw_bytes_not_on_disk`)
- ✓ Parser exited cleanly on all 8 (no `parser_exception` deferrals)

## Approvals.yaml

NOT modified. Phase 5 ceiling 171/160 → 171/160 unchanged (still +11 above sentinel). Recommend operator extend or close per b0553/b0557/b0558/b0560/b0561/b0564/b0565/b0566 standing.

## Costs

- Pre-tick cumulative_today: 74/500 (set by b0568 at 10:14:25Z)
- Fetches this tick: **0** (priority (a) reparse uses raw bytes already on disk)
- Post-tick cumulative_today: **74/500**
- Daily budget: 500 (separate from main worker's 2000/day)

## Next-tick recommendations

1. **Standing**: parser_v0.3.3 anchor pack authoring — *cohort grew implicitly today via b0568 (+8 ZMCC 2018) and is now 255 across all years; this batch confirms the v0.3.2 ceiling for ZMCC 2019 (8/8 redeferral)*. Recommended scope: declaratory-holding patterns ("declared unlawful", "is void", "wrongly brought", "abuse of process"), academic-relief patterns, and constitutional-amendment-review patterns drawn from the 8 summary heads sampled here.
2. **Standing**: OCR pipeline implementation (62 records pending — predominantly ZMCC 2018 + ZMCC 2020 scanned PDFs).
3. **Standing**: operator action on Phase 5 ceiling 171/160 (+11 above sentinel).
4. **Optional next-tick**: priority (c) ZMCC NEW YEARS — ZMCC 2017 is unswept (0 records, 0 raws on disk). Sparse HEAD probe `{1, 5, 10, 15, 20, 25}` would be the first step. Per task instruction this is gated on "no deferred records remain", which is not yet satisfied; but the v0.3.3-pending and OCR-pending cohorts are blocked on operator/parser-author work, not fetches — so practically a future tick may proceed to (c) once both cohorts are recognised as ineligible for inline reparse.
5. **Optional next-tick**: priority (a) on a different sub-cohort (e.g. ZMSC 2020 v0.3.3-pending records, of which there are ~19 raw on disk vs. 4 written) to extend the ceiling-confirmation evidence.

## Notes

- B2 sync deferred to host (rclone not in sandbox).
- Execution mode: **inline runner**; no derivative script committed (`_work/b0571/targets.json` written; `_work/b0571/parse_summary.json` produced by `scripts/batch_0498_parse.py` via `import` + path overrides; no `scripts/batch_0571_*.py` files created). Mirrors b0548..b0570 sandbox-session safety constraint precedent.
- Lock cleanup attempted at tick start: `find .git -name "*.lock" -delete` blocked by virtiofs Operation-not-permitted on three 0-byte locks (`.git/index.lock`, `.git/ORIG_HEAD.lock`, `.git/objects/maintenance.lock`, all 18:12-18:13Z). `git pull --ff-only` succeeded despite locks ("Already up to date") with a single warning on maintenance.lock unlink.
