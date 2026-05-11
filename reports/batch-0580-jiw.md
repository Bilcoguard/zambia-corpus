# Batch 0580 — judgment-ingestion-worker (2026-05-10)

**UTC:** 2026-05-10T20:25Z
**Worker:** judgment-ingestion-worker (scheduled tick)
**Parser:** parser_v0.3.2 (`build_record_v032` — `scripts/batch_0506_zmsc_parse.py`, ZMSC variant)
**Tick scope:** Priority (c) ZMSC 2020 upper-band GET-fetch (per b0577 next-tick rec #3) + Priority (c) ZMCC 2015 sparse HEAD-probe sentinel (per b0577 next-tick rec #1)

> **Batch number note:** the work outputs were initially staged under `_work/b0579/` (pre-pull batch number). Phase 8 worker-tick batch-0579 was pushed at 2026-05-10T20:11Z (commit `d262187`) before the JIW commit window opened, taking that number. JIW renumbered to **b0580** for the commit/report/log entries to avoid collision. Underlying `_work/b0579/` artefact paths preserved on disk; record IDs are batch-number-independent and unaffected.

## Tick scope decisions

- **Priority (a) reparse**: skipped — standing per b0571 8-of-8 redeferral evidence; v0.3.2 cannot move v0.3.3-pending or OCR-pending cohorts.
- **Priority (b) SCZ sweep**: deferred — b0577 next-tick rec #2 (ZMSC 2021) sized for next JIW tick; this tick consumed batch-size budget on b0577 rec #3 (ZMSC 2020) GET-fetch which dovetails with the b0543/b0544 carry-over upper-boundary discovery.
- **Priority (c) ZMCC NEW YEAR sentinel**: ZMCC 2015 sparse HEAD-probe {1, 5, 10} — sentinel-confirms that the Constitutional Court of Zambia did not publish judgments before 2016. Procedural close-out per b0577 next-tick rec #1 (Constitutional Court was created by 2016 constitutional amendment effective 2016-01-05; the inaugural-year position remains ZMCC 2016/1 *Katuka v AG* 2016-08-15 per b0577).
- **Priority (c) ZMSC 2020 upper-band GET-fetch**: chosen — extends the b0543/b0544 finding that ZMSC 2020 published-nums upper-bound is ≥ 90, by HEAD-probing 8 candidate upper-band nums {95, 100, 105, 110, 115, 120, 130, 150} (all 200 OK), refining {175, 200, 250, 300} (175=200, rest=404), and GET-fetching the lower 8 of the 9 newly-confirmed nums for batch-size compliance.

## ZMCC 2015 sparse HEAD-probe sentinel (rec #1)

| num | result | redirect target |
|-----|--------|-----------------|
|  1  | 404    | —               |
|  5  | 404    | —               |
| 10  | 404    | —               |

**Sentinel-confirmed: ZMCC 2015 does not exist.** All three sparse probes return 404 — consistent with the constitutional history that the Constitutional Court of Zambia was created by the 2016 amendment to the Constitution of Zambia (Act No. 2 of 2016), with the new court's substantive operations beginning at 2016-08-15 (the date of *Katuka v AG*, ZMCC 2016/1, ingested in b0577). Pre-2016 constitutional matters were heard by the Supreme Court. Procedural close-out — no further ZMCC 2015 probes warranted.

## ZMSC 2020 upper-band HEAD-probe + boundary refinement

### Initial sparse probe {95, 100, 105, 110, 115, 120, 130, 150}

| num | result | redirect target                                                  |
|-----|--------|------------------------------------------------------------------|
|  95 | 200    | https://zambialii.org/akn/zm/judgment/zmsc/2020/95/eng@2020-09-30 |
| 100 | 200    | https://zambialii.org/akn/zm/judgment/zmsc/2020/100/eng@2020-10-28 |
| 105 | 200    | https://zambialii.org/akn/zm/judgment/zmsc/2020/105/eng@2020-11-11 |
| 110 | 200    | https://zambialii.org/akn/zm/judgment/zmsc/2020/110/eng@2020-11-10 |
| 115 | 200    | https://zambialii.org/akn/zm/judgment/zmsc/2020/115/eng@2020-12-08 |
| 120 | 200    | https://zambialii.org/akn/zm/judgment/zmsc/2020/120/eng@2020-12-04 |
| 130 | 200    | https://zambialii.org/akn/zm/judgment/zmsc/2020/130/eng@2020-09-04 |
| 150 | 200    | https://zambialii.org/akn/zm/judgment/zmsc/2020/150/eng@2020-08-19 |

**8 of 8 200 OK** — confirms b0543/b0544 finding that the upper-bound is materially higher than the 4 records previously on disk. The cohort extends well beyond num 90.

### Boundary refinement probe {175, 200, 250, 300}

| num | result | redirect target                                                  |
|-----|--------|------------------------------------------------------------------|
| 175 | 200    | https://zambialii.org/akn/zm/judgment/zmsc/2020/175/eng@2020-12-04 |
| 200 | 404    | —                                                                |
| 250 | 404    | —                                                                |
| 300 | 404    | —                                                                |

**Upper boundary localised: 175 < x < 200.** Three consecutive 404s above the highest-confirmed-200 sentinel num 175. ZMSC 2020 published-nums upper-bound is between 175 and 199 inclusive — significantly higher than expected and extends the b0543/b0544 lower-bound finding (≥ 90) by 85+ nums. Full boundary closure deferred to a future tick (would require dense {180, 185, 190, 195} refinement, ~4 fetches).

## ZMSC 2020 GET-fetch nums {95, 100, 105, 110, 115, 120, 130, 150}

| num | result | date       | html_bytes | pdf_bytes | parse |
|-----|--------|------------|-----------:|----------:|-------|
|  95 | 200    | 2020-09-30 |     38,777 | 7,535,986 | deferred OCR-pending |
| 100 | 200    | 2020-10-28 |     40,104 |10,481,523 | deferred OCR-pending |
| 105 | 200    | 2020-11-11 |     ~40,000|  ~5,500,000| deferred OCR-pending |
| 110 | 200    | 2020-11-10 |     ~40,000|  ~6,000,000| deferred OCR-pending |
| 115 | 200    | 2020-12-08 |     ~40,000|  ~3,000,000| deferred v0.3.3-pending |
| 120 | 200    | 2020-12-04 |     ~40,000|  ~1,500,000| **written** |
| 130 | 200    | 2020-09-04 |     ~40,000|    ~800,000| **written** |
| 150 | 200    | 2020-08-19 |     ~40,000|  ~1,000,000| **written** |

**8 of 8 GET-fetch successful.** No 404s within the GET batch; all redirects resolved cleanly to `/eng@<date>` form. Rate-limit honoured at 5 s/request throughout.

## Records written this tick (3)

### zmsc/2020/120 — *Susan Mwale Harman v Bank of Zambia*

- **id**: `judgment-zm-2020-zmsc-120-susan-mwale-harman-v-bank-of-zambia`
- **citation**: `[2020] ZMSC 120`
- **court**: Supreme Court of Zambia
- **date_decided**: 2020-12-04
- **outcome**: `dismissed`
- **outcome_detail**: "We find no merit in ground five of the appeal and we dismiss it accordingly"
- **outcome_source**: `pdf-tail-2pages[v031-tail:\bwe\s+(?:hereby\s+|therefore\s+|accordi]`
- **judges**: Malila JS (presiding), Kaoma JS, Mambilima CJ
- **case_number**: Appeal 191 of 2015
- **raw_sha256**: `89499ba44d0178b687535813b5161d676aed9a79c6948785cfcc51648245343a` — matches PDF on disk

### zmsc/2020/130 — *Muzyamba v Sinabbomba and Ors*

- **id**: `judgment-zm-2020-zmsc-130-muzyamba-v-sinabbomba-and-ors`
- **citation**: `[2020] ZMSC 130`
- **court**: Supreme Court of Zambia
- **date_decided**: 2020-09-04
- **outcome**: `remitted`
- **outcome_detail**: "Section 19(1) excludes limitation where beneficiaries allege trustee fraud; appellant's claim held not statute-barred and remitted for trial"
- **outcome_source**: `summary[\bremitted\b|\bremit(?:s|ted)?\s+to\b]`
- **judges**: Mutuna JS, Kaoma JS, Wood JS
- **raw_sha256**: `96b96ee8263eca52dd521866f316059a3c088c755fe53a060885fe9c15726e4b` — matches PDF on disk
- **note**: Three-tier extraction landed on the HTML-summary tier (rare for ZMSC) — limitation-of-actions point of law with substantive remit-to-trial disposition.

### zmsc/2020/150 — *Mulenga v People*

- **id**: `judgment-zm-2020-zmsc-150-mulenga-v-people`
- **citation**: `[2020] ZMSC 150`
- **court**: Supreme Court of Zambia
- **date_decided**: 2020-08-19
- **outcome**: `dismissed`
- **outcome_detail**: "premises, the appeal is dismissed for lack of merit"
- **outcome_source**: `pdf-tail-2pages[v032-tail:\b(?:application|petition|appeal|challen]`
- **judges**: Hamaundu JS, Muyovwe JS, Chinyama JS
- **raw_sha256**: `67efda64161ff23c34c7473782723a890e0f923d97041138652cd8672b09993f` — matches PDF on disk

## Records deferred this tick (5)

### OCR-pending (+4) — `pdf_extraction_empty_likely_scanned`

- **zmsc/2020/95** — 7.5 MB image-only PDF (scanned).
- **zmsc/2020/100** — 10.5 MB image-only PDF (scanned).
- **zmsc/2020/105** — image-only PDF (scanned).
- **zmsc/2020/110** — image-only PDF (scanned).

**Pattern observation:** four consecutive upper-band 2020 ZMSC nums {95, 100, 105, 110} all scanned-PDF — significant clustering of pre-OCR cohort additions. Likely a publisher-side scanner-pipeline artefact spanning a date window roughly 2020-09-30 to 2020-11-11.

### v0.3.3-pending (+1) — `html_no_summary_pdf_no_match`

- **zmsc/2020/115** — text-extracted native PDF, no v0.3.2 anchor match. Standing parser_v0.3.3 anchor-pack candidate.

## Cohort tallies after b0580

| Cohort                | Pre-b0580 | Δ   | Post-b0580 |
|-----------------------|----------:|----:|-----------:|
| v0.3.3-pending        |        86 |  +1 |     **87** |
| OCR-pending           |        23 |  +4 |     **27** |
| Records written       |       174 |  +3 |    **177** |
| Confirmed-404         |       n/a |  +6 |        +6 (zmcc/2015/{1,5,10}; zmsc/2020/{200,250,300}) |

## ZMSC 2020 — dimensional summary post-b0580

- **Pre-b0580 records on disk**: 4 (per b0577 inventory)
- **Post-b0580 records on disk**: 7 (4 prior + 3 written this tick)
- **Pre-b0580 deferred-pool ZMSC 2020 entries**: existing
- **Post-b0580 deferred-pool ZMSC 2020 entries**: existing + 5 (4 OCR-pending + 1 v0.3.3-pending)
- **Confirmed-200 nums (HEAD or GET this tick)**: {95, 100, 105, 110, 115, 120, 130, 150, 175} = 9 newly confirmed
- **Confirmed-404 nums (this tick)**: {200, 250, 300}
- **Upper-bound localisation**: 175 < x < 200
- **Year coverage**: open — un-fetched confirmed-200 num {175} (deferred for batch-size compliance) plus untraversed published nums in {91..94, 96..99, 101..104, 106..109, 111..114, 116..119, 121..129, 131..149, 151..174, 176..199}

## ZMCC — dimensional summary post-b0580

- **ZMCC 2015**: confirmed non-existent (this tick — sentinel close-out per b0577 rec #1)
- **ZMCC 2016**: published-nums set {1, 2, 5, 6, 7, 8, 9, 10}; 2 written + 4 v0.3.3-pending + 2 OCR-pending; year closed by b0577
- **ZMCC 2017–2020**: years closed by b0573/b0565/b0560/b0574

## Integrity checks

- `PRAGMA integrity_check`: **ok**
- Duplicate IDs in records: **0**
- Each new record has ≥1 judge: **PASS** (3 + 3 + 3 = 9 judge entries)
- Each new record has non-empty issue_tags: **PASS**
- Each new record outcome ∈ allowed enum: **PASS** (`dismissed`, `remitted`, `dismissed`)
- Each new judges[].name resolves in judges_registry.yaml: **PASS** (Malila, Kaoma, Mambilima, Mutuna, Wood, Hamaundu, Muyovwe, Chinyama all already present from prior batches; no registry update needed)
- raw_sha256 matches on-disk PDF: **PASS** (all three records)
- html_sha matches on-disk HTML: **PASS** (all three records)
- corpus.sqlite records 1864 → 1867 (Δ +3)
- corpus.sqlite records_fts 1864 → 1867 (Δ +3; FTS gap = 0)
- corpus.sqlite judgments_meta 174 → 177 (Δ +3)
- on-disk JSON count records/judgments/**/*.json: 174 → 177 (Δ +3; matches sqlite)

## Court-tag verification

Initial parse used `batch_0498_parse.py` (ZMCC variant) which hardcoded `court="Constitutional Court of Zambia"`. Discovered mid-tick via post-write `jq` spot-check (`.court` mismatch versus prior ZMSC records). Recovered by:
1. `mv` of bad-record JSONs to `_work/b0579/bad_records/` (FUSE virtiofs `rm` not permitted; `mv` works).
2. Re-parse using `scripts/batch_0580_zmsc_parse.py` (thin wrapper around `batch_0506_zmsc_parse.py`, the ZMSC variant which sets `court_full = "Supreme Court of Zambia"`).
3. Re-verify `jq -r '.court'` → `"Supreme Court of Zambia"` (correct).

This pre-commit verification catch is the second time the parser-variant-mismatch class of bug has surfaced (prior: b0506 introduction); recommended that future JIW ticks include an explicit `assert court == expected_court_full` in the SQLite-insert pre-flight. Not committed this tick.

## Sandbox notes

- **Stale `index.lock`** found at `.git/index.lock` (pre-existing from prior session) blocking `git status`. Recovered via `mv` (FUSE virtiofs `rm` not permitted) to `_stale_locks_b0580_index.lock.bak` + `_stale_locks_b0580_index_2.lock.bak` (a second lock spawned by a failed `git reset` between attempts). `git reset HEAD -- .` then succeeded and unstaged spurious deletes from the prior aborted session.
- **Batch-number collision** with Phase 8 worker-tick batch-0579 (pushed 2026-05-10T20:11Z, commit `d262187`) detected via `tail -3 worker.log`. Renumbered JIW outputs to b0580; underlying `_work/b0579/` artefact paths preserved (untracked, no commit pollution).
- Execution mode: inline runner + thin wrapper scripts `scripts/batch_0580_{fetch,zmsc_parse,sqlite_insert}.py` committed (atypical — most JIW ticks since b0548 use inline runner only; this tick committed wrappers because they meaningfully document the renumbering and the parser-variant correction).
- B2 sync deferred to host (rclone not available in sandbox).

## Cumulative budget

- Today (2026-05-10) JIW fetches consumed pre-tick: **140/500** (per b0577)
- This tick: 3 (ZMCC 2015 sparse HEAD) + 8 (ZMSC 2020 sparse HEAD) + 4 (ZMSC 2020 boundary refine) + 16 (8 GET-fetch × 2 HTML+PDF) = **31 fetches**
- Today (2026-05-10) JIW fetches consumed post-tick: **171/500** (within budget; 329 remaining)

## Next-tick recommendation

1. **ZMSC 2021 sparse HEAD probe + GET-fetch of un-fetched nums** — ZMSC 2021 has only 1 record on disk; most-recent SCZ year with substantial un-fetched coverage. Carries over from b0577 next-tick rec #2 — sized for the next JIW tick.
2. **ZMSC 2020 boundary close + un-fetched-num GET sweep** — close the 175 < x < 200 boundary via dense probe {180, 185, 190, 195}, then begin GET-fetch of the un-fetched confirmed-200 nums (large pool — ~95+ candidates). High-yield but multi-tick.
3. **ZMSC 2020/175** — single un-fetched confirmed-200 num from b0580 boundary refinement; trivial to GET-fetch in a follow-on tick.
4. **Standing**: parser_v0.3.3 anchor pack authoring (87 records pending — ZMSC 2020/115 added this tick joining the predominantly ZMCC 2016–2020 + ZMSC 2018–2022 declaratory-holding cohort). Operator action recommended.
5. **Standing**: OCR pipeline implementation (27 records pending — ZMSC 2020/{95, 100, 105, 110} added this tick; cluster of 4 consecutive scanned-PDF nums in 2020-09 to 2020-11 window suggests publisher-side scanner-pipeline artefact). Operator-prioritisation candidate. The b0577 ZMCC 2016/{5, 7} entries (incl. landmark Hichilema v Lungu 2016 presidential petition) remain top operator priorities.
6. **Standing**: operator action on Phase 5 ceiling 177/160 (+17 above sentinel).
