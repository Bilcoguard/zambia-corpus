# Phase 8 nightly re-verification — batch 0554

- Started: 2026-05-09T08:29:14Z
- Completed: 2026-05-09T08:29:51Z
- Seed: `phase8-reverify-2026-05-09-b0554` (tick-suffixed; 5th worker-tick of 2026-05-09; 9th Phase 8 tick overall)
- Pool size: 1855
- Sample size: 8
- Sample rate: 1% (cap MAX_BATCH=8)

## Result counts

- match: 1
- drift: 7
- fetch_error: 0
- fetches: 8  (cumulative_today after this tick = 48/2000)

## Per-record verdicts

| verdict | id | host | bytes |
| --- | --- | --- | --- |
| drift | judgment-zm-2022-zmsc-57-zesco-limited-v-isaac-mbewe-25-ors | zambialii.org | 41797 |
| drift | si-zm-2016-062-electoral-process-code-of-conduct-enforcement-regulations-2016 | zambialii.org | 40402 |
| match | si-zm-2019-062-income-tax-konoike-construction-company-limited-approval-and-exemption-order-2019 | media.zambialii.org | 16605 |
| drift | act-zm-1991-021-local-government-elections-act-1991 | zambialii.org | 319165 |
| drift | act-zm-2017-004-standards-act-2017 | zambialii.org | 41613 |
| drift | act-zm-1993-019-mutual-legal-assistance-in-criminal-matters-act-1993 | zambialii.org | 195991 |
| drift | act-zm-1972-021-national-college-management-development-studies-act-1972 | www.zambialii.org | 121222 |
| drift | judgment-zm-2023-zmcc-22-charles-mwelwa-v-stephen-chikota-and-anor | zambialii.org | 44780 |

## Cross-tick observations (cumulative across 9 Phase 8 ticks)

- zambialii.org `/akn/` act-or-SI HTML URL drifts: 30/30 (b0554 added 6: act-zm-1991-021, act-zm-2017-004, act-zm-1993-019, act-zm-1972-021, si-zm-2016-062 — and judgment zmcc/2023/22, zmsc/2022/57 noted separately).
- media.zambialii.org PDF stable matches: 25/25 (b0554 added 1: si-zm-2019-062 income-tax-konoike PDF).
- judgment `/akn/` HTML URL outcomes: 1 match (b0551 zmsc/2020/51 chama) + 2 drifts (b0554 zmsc/2022/57 zesco-mbewe + zmcc/2023/22 mwelwa-chikota). Counter-evidence to the b0551 N=1 judgment-stability working hypothesis. Working revision: judgment `/akn/` HTML URLs also drift (likely same backend rendering layer); the b0551 single match was sample noise. Future ticks should continue tracking judgment-/akn/ verdicts separately to accumulate evidence.

## Integrity check

- No records mutated (Phase 8 is a read-only verification phase).
- All 8 sampled record JSON files remain on disk: PASS.
- corpus.sqlite not touched: confirmed (script writes only `reports/batch-0554-reverify.json`).
- approvals.yaml not modified.

## Notes

- Phase 8 is open-ended (sample_rate: 0.01); approvals.yaml `approved` and `complete` flags untouched.
- Execution mode: inline runner (per b0548/b0549/b0551 sandbox-session safety precedent); no `scripts/batch_0554_phase8_reverify.py` derivative committed. Functionality matches the b0546 baseline including `scripts/certs/*.pem` PKI loader.
- B2 sync deferred to host (rclone not available in sandbox).
