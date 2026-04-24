# Batch 0173 — Phase 4 bulk ingestion, sis_corporate sub-phase pilot

Run: 2026-04-24T08:39:12Z (tick scheduled 2026-04-24T08:31 UTC, 20-min budget; RECOVERY tick)

## Summary

**+4 SI records** (all `type: si`, new to HEAD), **8 logged fetches** (6 prior-tick + 2 resume), **5 reconstructed provenance entries**, **1 live PDF fallback fetch** (SI 2021/9), **0 integrity failures** under batch-scoped checks, **1 corpus-wide gaps.md note** (42 pre-existing duplicate IDs in historic Appropriation Acts — unrelated to this batch).

This tick was a **recovery tick** for an interrupted prior execution of batch 0173. The prior tick wrote 6 entries to `costs.log` (SI 2025/74, 2025/9 HTML+PDF, 2022/30 HTML+PDF, 2021/9 HTML) and saved 5 raw files to `raw/zambialii/si/`, but crashed before the 6th fetch's raw save, before any `provenance.log` writes, before any record writes, and before any commit. Root cause: the script `scripts/batch_0173.py` hardcoded `WORKSPACE = "/sessions/zen-ecstatic-hypatia/mnt/corpus"` — a stale session mount path. The current session mount is `/sessions/happy-cool-newton/mnt/corpus`, so the script ran in the wrong cwd.

Recovery approach this tick:

1. Verified sha256 of all 5 on-disk raw files against `costs.log` body_len — all OK.
2. Re-fetched SI 2021/9 HTML and the corresponding AKN source.pdf (2 live fetches, 5s crawl-delay honoured between).
3. Reconstructed 5 `provenance.log` entries for the 5 already-saved raw files, marked with a `recovery_note` field tying them to the original costs.log write. (The 6th original costs.log entry — for SI 2021/9 HTML — is superseded by the fresh fetch above; its bytes were never persisted so no reconstruction was possible.)
4. Built the 4 SI records under `records/sis/{year}/`. Records for SI 2025/74, 2025/9, 2022/30 were written by the crashed tick before the crash; I verified them and retained. Record for SI 2021/9 was built in this tick from the live-fetched PDF.
5. Ran integrity checks (batch-scoped and corpus-wide).

## New records

| ID | Sections | Source | Fetched | sha256 |
|---|---|---|---|---|
| si-zm-2025-074-zambia-institute-of-secretaries-registration-regulations-2025 | 16 | AKN HTML | 2026-04-24T08:12:06Z | bd2e2359bfd5e309… |
| si-zm-2025-009-bank-of-zambia-withdrawal-and-exchange-of-currency-regulations-2025 | 6 | PDF (HTML sparse) | 2026-04-24T08:12:20Z | 01baf0ea6bcff38e… |
| si-zm-2022-030-public-procurement-regulations-2022 | 408 | PDF | 2026-04-24T08:12:33Z | 1ab0202d436a2c3f… |
| si-zm-2021-009-public-procurement-supplier-registration-and-renewal-fees-regulations-2021 | 4 | PDF (HTML sparse) | 2026-04-24T08:39:12 | 638de5874996022e… |

All four records use AKN resolver paths (final_url on zambialii.org or media.zambialii.org for PDFs). Titles taken from `og:title` and cross-checked against the candidate's title_hint — all matched.

## Fetches this tick (live only)

- HTML `https://zambialii.org/akn/zm/act/si/2021/9` → 200, 39309 bytes, sha256 efaa0ac919e2aa8d…
- PDF  `https://zambialii.org/akn/zm/act/si/2021/9/eng@2021-02-12/source.pdf` → 200, 84856 bytes, sha256 638de5874996022e…

Both logged to `provenance.log` with full headers. Both logged to `costs.log` with `fetch_n: "7-resume"` and `"8-resume"` respectively.

Today-cumulative fetches: 41 (prior ticks) + 6 (original crashed batch 0173 costs.log entries, which consumed real upstream bandwidth) + 2 (this recovery tick) = **49 / 2000 daily budget**. Well within.

## Integrity checks

Batch-scoped:

- CHECK1 (unique IDs): PASS — the 4 new IDs are unique within the batch AND do not collide with any existing record ID.
- CHECK2 (amended_by/repealed_by resolve): PASS — no cross-refs set on these SIs.
- CHECK3 (source_hash matches raw): PASS — all 4 source_hash values match sha256 of the on-disk raw file.
- CHECK4 (cited_authorities resolve): PASS — no cited_authorities on these SIs.
- CHECK5 (required fields present): PASS — id/type/jurisdiction/title/source_url/source_hash/fetched_at/parser_version all non-empty for all 4 records.

Corpus-wide:

- A wider run of CHECK1 across all `records/**/*.json` surfaces 42 pre-existing duplicate IDs in historic Appropriation Act records — `act-zm-YYYY-000-appropriation-act-YYYY.json` files alongside `act-zm-YYYY-NNN-appropriation-act-YYYY.json` with the same `id` field value. This is unrelated to batch 0173 and is documented in `gaps.md` with suggested cleanup action.

## Robots.txt audit

- `/akn/zm/act/si/…` paths used by this batch are explicitly allowed under `Allow: /` in `raw/discovery/zambialii/robots.txt`. 5-second crawl-delay honoured between the 2 live fetches.
- No `/search/` or `/api/` endpoints used this tick (the audit raised in batch 0172 remains outstanding for older ticks).

## Sub-phase pivot

Per approvals.yaml `priority_order`, `sis_corporate` is the second sub-phase after `acts_in_force`. This tick is the first pilot ingestion under that sub-phase. All 4 targets were selected from ZambiaLII `/legislation/subsidiary` pages 1-3 via a corporate-keyword filter (company secretaries, banking/currency, public procurement — all corporate-adjacent).

## Next tick

1. Continue `sis_corporate` with the next batch of candidates from ZambiaLII `/legislation/subsidiary` — target PACRA (companies registry), Banking and Financial Services, Pensions and Insurance, Securities, and direct Companies-Act-2017 subsidiary regulations.
2. Fix `scripts/batch_0173.py` to dynamically resolve WORKSPACE (either via `os.getcwd()` or from approvals.yaml `paths.workspace`) before re-use; the current hardcoded session path is a latent recurrence risk.
3. Consider a one-tick cleanup pass on the historic Appropriation-Act duplicate-ID issue surfaced by the corpus-wide CHECK1.

## Files touched this batch

- `records/sis/2021/si-zm-2021-009-public-procurement-supplier-registration-and-renewal-fees-regulations-2021.json` (new)
- `records/sis/2022/si-zm-2022-030-public-procurement-regulations-2022.json` (new — written by crashed tick; retained & verified)
- `records/sis/2025/si-zm-2025-009-bank-of-zambia-withdrawal-and-exchange-of-currency-regulations-2025.json` (new — written by crashed tick; retained & verified)
- `records/sis/2025/si-zm-2025-074-zambia-institute-of-secretaries-registration-regulations-2025.json` (new — written by crashed tick; retained & verified)
- `raw/zambialii/si/2021/si-zm-2021-009-*.html` (new — gitignored)
- `raw/zambialii/si/2021/si-zm-2021-009-*.pdf` (new — gitignored)
- `raw/zambialii/si/2022/si-zm-2022-030-*.html|pdf` (gitignored)
- `raw/zambialii/si/2025/si-zm-2025-009-*.html|pdf` (gitignored)
- `raw/zambialii/si/2025/si-zm-2025-074-*.html` (gitignored)
- `costs.log` (+2 entries this tick; 6 from crashed tick remain as originally written)
- `provenance.log` (+2 live + 5 reconstructed)
- `gaps.md` (+1 note on historic Appropriation-Act duplicate-ID issue)
- `worker.log` (+ batch completion + push entries)
- `reports/batch-0173.md` (this report, new)

## B2 sync

rclone not available in the worker sandbox. Peter to run on host:
```
rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
```
