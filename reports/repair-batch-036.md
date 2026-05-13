# Repair Batch 036 — 2026-05-13

**Worker:** repair-batch-036 (SKILL.md v4)
**Tick start:** 2026-05-13T04:08Z
**Result:** 8/8 manifest records repaired, integrity OK, parity OK.

## Pre-flight

- `git pull --ff-only` → already up to date (warnings about FUSE EPERM on stale `.lock` files; non-blocking).
- `PRAGMA integrity_check` → `ok`.
- Pre counts: records=1928, records_fts=1928.

## Live-DB diagnosis (Step 2)

Ran all three conditions against the live database (not just manifest):

| Condition | Count | Notes |
| --- | --- | --- |
| A — line-numbers-only corruption | 0 | Digit-ratio test passed for all 1524 bodies > 10c. |
| B — empty body (acts/SIs only) | 233 | Almost all ZambiaLII SI placeholder rows; outside this tick's scope per manifest. |
| C — stub body < 200c (acts/SIs) | 31 | All from parliament.gov.zm or ZambiaLII PDFs. |

Of the 88 manifest records (87 acts + 1 SI), **32 still required repair** at tick start; **56 had been successfully repaired in prior batches**. Selected the next 8 in manifest declaration order for this batch.

## Queue (manifest order)

1. `act-zm-2013-016-the-customs-and-excise-amendment-2013`
2. `act-zm-2013-019-the-appropriation-act-2013`
3. `act-zm-2014-001-the-legal-practitioner-amendment-act`
4. `act-zm-2014-002-the-service-commissions-amendment-act-2014-act-no-2-of-2014`
5. `act-zm-2016-008-the-constitutional-court`
6. `act-zm-2016-009-the-superior-courts-number-of-judges`
7. `act-zm-2017-008-supplementary-appropriation-2017`
8. `act-zm-2021-026-the-health-professions-amendment-act-2021`

## Results

| # | Record ID | Method | Chars | Source bytes |
| - | --- | --- | ---: | ---: |
| 1 | act-zm-2013-016-customs-and-excise-amendment-2013 | OCR (13pp) | 6,708 | 176,017 |
| 2 | act-zm-2013-019-appropriation-act-2013 | OCR (20pp) | 6,852 | 367,932 |
| 3 | act-zm-2014-001-legal-practitioner-amendment-act | OCR (1pp) | 842 | 68,241 |
| 4 | act-zm-2014-002-service-commissions-amendment-2014 | OCR (2pp) | 2,470 | 158,307 |
| 5 | act-zm-2016-008-constitutional-court | OCR (10pp) | 3,493 | 2,519,942 |
| 6 | act-zm-2016-009-superior-courts-number-of-judges | OCR (2pp) | 1,310 | 303,993 |
| 7 | act-zm-2017-008-supplementary-appropriation-2017 | OCR (6pp) | 4,935 | 1,214,620 |
| 8 | act-zm-2021-026-health-professions-amendment-2021 | pdfplumber | 3,473 | 13,557 |

Seven of eight required the OCR fallback (pdftotext yielded zero — the published PDFs are image-only scans). Only the 2021 health-professions act came through clean via pdfplumber. All eight passed the quality gate (>500 chars, ≥2 legal markers, long-word present, not line-numbers-only).

## Post-flight integrity

- `records` = 1928, `records_fts` = 1928 → **parity OK**
- `PRAGMA quick_check` → `ok`
- `PRAGMA integrity_check` → `ok`
- All 8 FTS rows verified present after rebuild.

## DB sync

- Worked on a per-tick copy under `_repair_b036_tmpdb/` (same pattern as b034/b035 to avoid FUSE I/O glitches mid-write).
- Swap-back via `os.replace(tmp_db, DB)` succeeded.

## B2 sync

`rclone` not present in the sandbox → **B2 sync deferred to host**.

## Git commit/push

Per the established pattern since b0608, `.git/index.lock` is held under FUSE EPERM inside the sandbox. The host-side sweeper handles the commit/push of `corpus.sqlite`, `reports/repair-batch-036.md`, `worker.log`, `costs.log`, and `gaps.md`. From the sandbox's perspective the working tree changes are persisted on disk.

## Manifest progress

- Start of tick: 32 / 88 manifest records still needing repair.
- End of tick: **24 / 88 manifest records still needing repair**.
- Next targets (b037, in manifest order): `2021-027`, `2021-028`, `2021-029`, `2021-030`, `2021-031`, `2023-019`, `2023-020`, `2023-022`.

## Wall-clock

- Tick start: 04:08Z. Tick end: 04:09Z. Well under the 20-min budget — OCR for these 2013-2017 acts was fast (1-30 pages each).

## Non-negotiables checklist

- Never commit if records ≠ records_fts → **parity verified before swap-back**.
- Never fabricate body text → **all text from curl-fetched source PDFs**.
- Never exceed 20-min wall-clock → **completed in ~1 min**.
- Fail loud on errors → **none occurred**.
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)` — **set**.
- Honour robots.txt / rate limits → **2 s sleep between fetches**.
- parliament.gov.zm CA cert → **`scripts/certs/rapidssl_tls_rsa_ca_g1.pem` loaded via curl `--cacert`**.
