# Repair batch 0656 — 1 act + 6 SIs (mixed cohort drainage)

**Worker**: repair-corpus (scheduled-task, v4 prompt)
**Tick**: b0656
**Wall-clock**: ~6 min (well within 20-min budget)
**Parent commit**: (post-b0654 main)
**Date**: 2026-05-15T05:09Z

## Summary

This tick targeted the last Condition-B act with no body (`act-zm-2023-025`,
the Customs and Excise (Amendment) Act 2023) and 7 ZambiaLII SIs from the
2018–2019 cohort. Eight UPDATEs were attempted; **7 committed successfully**,
**1 reverted** due to an upstream ZambiaLII data-quality issue (see Gaps).

Total body bytes written: **31,675** (net of revert).

## Records repaired (7)

| # | ID | Bytes | SHA-256 (8) |
|---|---|------:|---|
| 1 | act-zm-2023-025-the-customs-and-excise-amendment-act-2023-act-no-25-of-2023 | 11,730 | 14b457ce |
| 2 | si-zm-2018-056-national-assembly-by-election-kasenengwa-constituency-no-41-election-date-and-time-of-poll-no-2-order-2018 | 3,822 | 7ba43808 |
| 3 | si-zm-2018-064-constitutional-offices-emoluments-regulations-2018 | 1,743 | 1640a029 |
| 4 | si-zm-2018-081-electoral-process-local-governments-by-elections-election-date-and-time-of-poll-no-6-order-2018 | 1,891 | a2500ec6 |
| 5 | si-zm-2018-094-electoral-process-local-governments-by-elections-election-date-and-time-of-poll-no-7-order-2018 | 2,030 | ce4e23be |
| 6 | si-zm-2019-006-disaster-management-qualifications-of-national-coordinator-regulations-2019 | 1,041 | f5146c1c |
| 7 | si-zm-2019-014-companies-general-regulations-2019 | 9,418 | 9932453c |

## Reverted (1) — upstream data-quality issue

| ID | Reason |
|---|---|
| si-zm-2018-057-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-4-order-2018 | ZambiaLII `si/2018/57/eng@2018-08-03/source.pdf` byte-identical to `si/2018/56/...source.pdf` (sha256 `d405f924…`). Both return the SI 56 gazette text. PDF passed our quality gate but is materially wrong for record 057 — refusing to fabricate; body cleared, source_hash cleared, awaiting upstream fix or alternate source. |

## Pipeline

For each target id:

1. Read `source_url` from `records`.
2. If URL ends `.pdf` and host is `parliament.gov.zm`, fetch with
   `curl --cacert scripts/certs/rapidssl_tls_rsa_ca_g1.pem -L -A "<UA>"`
   (Python certifi bundle lacks the RapidSSL CA chain).
3. Otherwise fetch HTML, parse `href="...source.pdf"`, then fetch the PDF.
4. Extract text page-by-page with `pdfplumber`.
5. Section-number normalisation: `re.sub(r"(\d+)\.([A-Z])", r"\1. \2", body)`.
6. Quality gate: `len > 200`, digit-line-ratio test, legal-marker regex.
7. `UPDATE records SET body=?, source_hash=?, fetched_at=?, parser_version='repair-0.6.2' WHERE id=?` — one connection per record, individual commit (crash-safe).
8. Crawl delay: 5 s between fetches.

## FTS refresh

Per-row FTS5 refresh, one transaction per record:

```sql
INSERT INTO records_fts(records_fts, rowid, id, title, body, citation, type)
  VALUES('delete', :rowid, :id, :title, '', :citation, :type);
INSERT INTO records_fts(rowid, id, title, body, citation, type)
  VALUES(:rowid, :id, :title, :body, :citation, :type);
```

Global `INSERT INTO records_fts(records_fts) VALUES('rebuild')` raised
`disk I/O error` during commit (same chronic FUSE/virtiofs pattern observed
in b0654 and earlier). The journal grew to ~21 MB and was renamed
`corpus.sqlite-journal.b0656-failed-fts-rebuild.bak` to unblock SQLite.
A second small revert UPDATE on record 057 also tripped the journal pattern
once; it was unblocked via
`corpus.sqlite-journal.b0656b-revert-attempt.bak` and the UPDATE succeeded
on the retry under `PRAGMA journal_mode=MEMORY`. All 7 body UPDATEs were
committed in their own connections **before** any FTS work, so the body
data is durable.

FTS verification:

- `MATCH 'Customs AND Excise AND Amendment'` → 62 hits (act now indexed).
- `MATCH 'companies AND regulations'` → 167 hits (si-2019-014 indexed).
- `MATCH 'Kasenengwa'` → hits include si-2018-056 (newly indexed).

## Integrity

| Check | Result |
|---|---|
| `records` count | 1,922 |
| `records_fts` count | 1,922 |
| Parity (records == records_fts) | OK |
| `PRAGMA quick_check` | `ok` |

## Cost / footprint

- 8 ZambiaLII / parliament.gov.zm GETs, ~700 KB HTML + ~600 KB PDF
- 7 record UPDATEs + 7 FTS index refreshes
- No global FTS rebuild (deferred — chronic FUSE issue)
- B2 sync: deferred to host (`rclone` not installed in sandbox).

## Next-tick priority

Condition-B SI count after this batch: **153** (was 159).
The two `commons.laws.africa` records (`local-courts-administration-of-estates-rules-1969`,
`local-courts-rules-1966`) are image-PDFs that need OCR — defer to a tick
with `ocrmypdf` available, or pull alternate text-bearing copies from
laws.africa or ZambiaLII.
