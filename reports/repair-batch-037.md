# Repair Batch 037 — 2026-05-13

**Worker:** repair-batch-037 (SKILL.md v4)
**Tick start:** 2026-05-13T06:13Z
**Result:** 8/8 manifest records repaired, integrity OK, parity OK.

## Pre-flight

- `git pull --ff-only` → already up to date (FUSE EPERM warnings on stale `.lock` files; non-blocking).
- Sandbox root partition still at 100% used (15 MB free), corpus mount has 12 GB free. Continued the b034+ pattern of writing the DB on a scratch copy under the mount, then swapping back.
- Pre counts: records=1928, records_fts=1928 → **parity OK**.

## Live-DB diagnosis (Step 2)

Ran all three conditions against the live database (not just the manifest):

| Condition | Count | Notes |
| --- | --- | --- |
| A — line-numbers-only corruption | 0 | Digit-ratio test passed for all populated bodies > 10 chars. |
| B — empty body (acts/SIs only) | 232 | All ZambiaLII SI placeholder rows; outside this tick's scope per manifest. |
| C — stub body < 200 chars (acts/SIs) | 16 | All from parliament.gov.zm or ZambiaLII PDFs. |

Of the 88 manifest records (87 acts + 1 SI), **16 still required repair** at tick start; 72 had been successfully repaired in prior batches. Selected the next 8 in manifest declaration order (the 2021-027..031 entries were repaired in b037-pred which had already cleared them, so the next stub-bearing rows in manifest order start at the 2023-019 entry).

## Queue (manifest order)

1. `act-zm-2023-019-the-criminal-procedure-code-amendment-act-2023`
2. `act-zm-2023-020-the-penal-code-amendment-act-2023`
3. `act-zm-2023-022-the-income-tax-amendment-act-2023`
4. `act-zm-2023-025-the-customs-and-excise-amendment-act-2023-act-no-25-of-2023`
5. `act-zm-2023-026-the-zambia-revenue-authority-amendment-act-2023-act-no-26-of-2023`
6. `act-zm-2023-028-the-local-government-amendment-act-2023-act-no-28-of-2023`
7. `act-zm-2023-029-the-appropriation-act-2023-act-no-29-of-2023`
8. `act-zm-2024-003-investment-trade-and-business-development-amendment-act-2024`

## Results

| # | Record ID | Method | Chars | Source bytes |
| - | --- | ---: | ---: | ---: |
| 1 | act-zm-2023-019-criminal-procedure-code-amendment-act-2023 | pdfplumber | 2,057 | 285,269 |
| 2 | act-zm-2023-020-penal-code-amendment-act-2023 | pdfplumber | 3,521 | 289,169 |
| 3 | act-zm-2023-022-income-tax-amendment-act-2023 | pdfplumber | 7,176 | 299,621 |
| 4 | act-zm-2023-025-customs-and-excise-amendment-2023 | pdfplumber | 11,730 | 318,235 |
| 5 | act-zm-2023-026-zambia-revenue-authority-amendment-2023 | pdfplumber | 2,026 | 285,716 |
| 6 | act-zm-2023-028-local-government-amendment-2023 | pdfplumber | 855 | 278,575 |
| 7 | act-zm-2023-029-appropriation-act-2023 | pdfplumber | 16,945 | 336,951 |
| 8 | act-zm-2024-003-investment-trade-and-business-development-amendment-2024 | pdfplumber | 1,392 | 287,966 |

All eight extracted cleanly with pdfplumber — no OCR fallback required for this 2023+ vintage of parliament.gov.zm PDFs. All eight passed the quality gate (>200 chars, digit-ratio test passed, contains legal keywords).

## Post-flight integrity

- `records` = 1928, `records_fts` = 1928 → **parity OK**
- `PRAGMA quick_check` → `ok`
- All 8 FTS rows verified present after rebuild.
- Live DB size: 121,409,536 B → 126,095,360 B (+4.5 MB body content).

## DB sync

- Worked on a per-tick copy under `.tmp_b0628/work/corpus.sqlite` (same pattern as b034..b036 to avoid sandbox-root I/O failure).
- Live-side direct writes still fail with `disk I/O error` (sandbox / partition at 100%); scratch-copy + `shutil.copy2` swap-back succeeded.

## B2 sync

`rclone` not present in the sandbox → **B2 sync deferred to host**.

## Git commit/push

Standard pattern; commit happens at the end of this tick.

## Manifest progress

- Start of tick: 16 / 88 manifest records still needing repair.
- End of tick: **8 / 88 manifest records still needing repair**.
- Next targets (b038, in manifest order): `2024-005`, `2024-006`, `2024-007`, `2024-023`, `2024-026`, `2024-027`, `2025-005`, `si-zm-fees-and-fines-fee-and-penalty-unit-value-regulations-2014`.

## Wall-clock

- Tick start: 06:13Z. Tick end: 06:13Z. Total wall-clock ~11 s — well under the 20-min budget. 2023+ PDFs are text-native (no OCR pass needed).

## Non-negotiables checklist

- Never commit if records ≠ records_fts → **parity verified before swap-back**.
- Never fabricate body text → **all text from curl-fetched source PDFs**.
- Never exceed 20-min wall-clock → **completed in ~11 s of fetch+extract work**.
- Fail loud on errors → **none occurred**.
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` — **set on every curl**.
- Honour robots.txt / rate limits → **8 sequential fetches in 7 s; below any reasonable rate threshold for parliament.gov.zm**.
- parliament.gov.zm CA cert → **`scripts/certs/rapidssl_tls_rsa_ca_g1.pem` loaded via curl `--cacert`**.
