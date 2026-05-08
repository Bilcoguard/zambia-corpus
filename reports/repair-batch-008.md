# Zambia Corpus Repair — Batch 008

**Date:** 2026-05-08 UTC (scheduled run)
**Worker:** repair-corpus (automated tick, scheduled-task SKILL)
**Operator:** automated (Claude scheduled task; session `hopeful-friendly-lamport`)
**Status:** **COMPLETE — 1 successful repair; integrity OK; live DB updated; queue fully cleared (42 / 42)**
**Headline:** Resolved the only remaining manifest target — `act-zm-2026-005-national-payment-system-act` — by falling back to the ZambiaLII canonical expression URL after seven consecutive batches of HTTP 404 on the manifest's parliament.gov.zm URL. **All 42 repair targets are now repaired.** Recommend disabling this scheduled task and updating the manifest URL in `SKILL.md`.

## Pre-flight

* Scheduled-task pre-step `find .git -name "*.lock" -delete` and `find .git -name "*.lock.bak" -delete` ran. The FUSE mount blocked unlink on `.git/ORIG_HEAD.lock` (same constraint as previous batches). `git pull --ff-only` returned `Already up to date.`
* Live `corpus.sqlite` (~109 MB) carried **1846 records / 1846 FTS rows** pre-batch — matched (FTS orphan from batch 007 closed the previous gap).
* Identified 1 still-corrupted record on entry, exactly the recurring failure from batches 001, 003, 004, 005, 006 and 007: `act-zm-2026-005-national-payment-system-act` (`body` was 503 bytes, 153 of 153 lines pure digits).

## Method — manifest-URL fallback to ZambiaLII canonical FRBR

Per batch 007's action item, the manifest URL `https://www.parliament.gov.zm/sites/default/files/documents/acts/National%20Payment%20System%20Act%20No.%205%20of%202026.pdf` is permanently HTTP 404 (also fails with relaxed SSL). This tick treated the queue-end recurrence as a manifest defect and resolved it via the ZambiaLII canonical FRBR landing page rather than abandoning the record.

1. **Probed candidate URLs** (one batch of HEAD/GETs, all rate-limited 2 s, single User-Agent `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`):
    * Six parliament.gov.zm filename variants — all `SSL: CERTIFICATE_VERIFY_FAILED` (sandbox CA bundle does not trust parliament.gov.zm chain), and prior worker has confirmed under relaxed SSL that they are HTTP 404.
    * `https://zambialii.org/akn/zm/act/2026/5` → HTTP 200, HTML 38 858 bytes — canonical FRBR landing page exists.
    * `https://zambialii.org/akn/zm/act/2026/5/source.pdf` → HTTP 404 (no expression-less alias).
    * `https://zambialii.org/akn/zm/act/2026/5/eng@2026-04-10/source.pdf` and `eng@2026-04-09/source.pdf` → HTTP 404 (wrong dates).
2. **Parsed the FRBR landing page** for the canonical expression date and source URL: `eng@2026-04-08`, source link `/akn/zm/act/2026/5/eng@2026-04-08/source.pdf`.
3. **Fetched** `https://zambialii.org/akn/zm/act/2026/5/eng@2026-04-08/source.pdf` → HTTP 200, `application/pdf`, 910 732 bytes, starts with `%PDF-`.
4. **Extracted text** with pdfplumber 0.11.9: 155 266 chars across 3 260 lines.
5. **Section-normalised** per the manifest recipe (no concatenated section pairs needed splitting in this body).
6. **Quality gate** passed: 155 266 chars > 500; 9 / 3 260 digit-only lines (well under the 50 % cut-off); contains many ≥ 6-letter words.

## Records attempted (1 — within MAX_BATCH_SIZE = 8)

| # | Record ID | Status | Body chars | URL used |
|---|---|---:|---:|---|
| 1 | `act-zm-2026-005-national-payment-system-act` | **ok** | 155 266 | `https://zambialii.org/akn/zm/act/2026/5/eng@2026-04-08/source.pdf` (ZambiaLII fallback; manifest's parliament.gov.zm URL still HTTP 404) |

Total body characters added this tick: **155 266**.

## Records that failed this tick

None.

## Records still remaining after this tick

**Zero.** All 42 manifest targets are now repaired.

```
records.body length for act-zm-2026-005-national-payment-system-act: 155 266 chars
records count: 1 846
records_fts count: 1 846
PRAGMA integrity_check: ok
FTS MATCH 'national payment system': 185 hits, includes target
```

## Diagnostics

* `worker.log` updated with `START`, pre/post counts, fallback-probe trace, per-record outcome, and `END`.
* `gaps.md` appended with one resolution row pointing to the working ZambiaLII URL and noting the manifest URL is still dead and should be updated.
* `costs.log` appended with `repair-batch-008 records_repaired=1 fetches=2 confirmed_404=0`.
* B2 sync: **deferred to host** — `rclone` not available in this sandbox (logged to `worker.log`).
* Per-record fetch obeys 2 s rate-limit; UA `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.

## SQLite commit pattern (FUSE-safe atomic copy)

The FUSE mount on this sandbox host (`/sessions/hopeful-friendly-lamport/mnt/corpus`) disallows file unlink, which prevents SQLite from cleaning up its rollback journal at commit time on the live DB. The pattern used here, consistent with prior repair batches (001, 003, 004):

1. `cp corpus.sqlite /tmp/corpus.sqlite.work` (working copy in unmounted /tmp).
2. `cp corpus.sqlite corpus.sqlite.bak.repair-batch-008-pre-<UTC>` (in-place backup on the FUSE mount).
3. Open `/tmp/corpus.sqlite.work`, run UPDATE + DELETE/INSERT FTS on the working copy, `COMMIT`, run `PRAGMA integrity_check`.
4. `cp /tmp/corpus.sqlite.work corpus.sqlite` (atomic-by-rename-equivalent overwrite).
5. Re-open the live DB and verify counts + record body length + FTS hit + `PRAGMA integrity_check`.

This sidesteps the FUSE unlink restriction without needing `journal_mode=TRUNCATE`.

## Integrity

* Pre-batch: records = 1846, fts = 1846 — **matched**.
* Post-batch: records = 1846, fts = 1846 — **matched**.
* No INSERT or DELETE of `records` was performed. One UPDATE on `records.body` (rowcount = 1); one matched DELETE+INSERT pair on `records_fts`. `approvals.yaml` was not touched.

## Action items for the human operator

1. **Update manifest URL** in `SKILL.md` (this very file) for `act-zm-2026-005-national-payment-system-act`. Replace
   `https://www.parliament.gov.zm/sites/default/files/documents/acts/National%20Payment%20System%20Act%20No.%205%20of%202026.pdf`
   with the working ZambiaLII URL
   `https://zambialii.org/akn/zm/act/2026/5/eng@2026-04-08/source.pdf`
   so future correctness checks against the manifest URL pass without the parliament.gov.zm dead-link detour.
2. **Disable this scheduled task** — the queue is fully clear (42 / 42 repaired). The next tick would no-op and write an idle entry; cleaner to disable.
3. **B2 sync** — run `rclone copyto corpus.sqlite b2raw:kwlp-corpus-raw/corpus.sqlite` from the host once the commit lands.
4. The `judgment-zm-2020-zmsc-01-hiteshbhai-partel-v-kofi-another` body remains `NULL` (per batch 007's note). Outside this worker's scope; tracked by the judgment-ingestion-worker.
