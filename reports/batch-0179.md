# Batch 0179 — Phase 4 sis_corporate

**Started:** 2026-04-24T11:35:04Z
**Completed:** 2026-04-24T11:38:16Z
**Phase / sub-phase:** Phase 4 bulk — `sis_corporate` (priority_order item 2)
**Batch size used:** 4 targets × 2 fetches = 8 fetches (= MAX_BATCH_SIZE)
**Records written:** 3
**Gaps recorded:** 1

## Scope

Batch 0178 exhausted the `/legislation/subsidiary` paginated listing
(pages 1-10 valid; pages 11-12 return HTTP 404). Re-scanning the seven
cached discovery pages on disk (pages 04-10) with an expanded
corporate-keyword filter surfaced 5 novel SIs not in HEAD.

Targets selected (4; the 5th — 2015/033 Road Traffic (Certificates of
Security and Insurance) (Display) Regulations — was deferred in batch
0178 on substance and is deferred again here, because "insurance" in
that title is compulsory-cover terminology for road traffic, not
corporate-sector regulation):

1. **si/2017/042** — Income Tax (Overseas Private Investment Corporation)
   (Approval and Exemption) Order, 2017 (US federal corporate entity,
   income-tax exemption)
2. **si/2017/070** — Income Tax (African Management Services Company)
   (Approval and Exemption) Order, 2017 (SADC-linked corporate entity,
   income-tax exemption)
3. **si/2019/025** — Income Tax Act (Suspension of tax on payment of
   interest to non-resident) (Treasury Bill and Bond) Regulations, 2019
   (non-resident interest suspension on sovereign paper)
4. **si/2020/008** — Diplomatic Immunities and Privileges (Turkish
   Cooperation and Coordination Agency) Order, 2020 (bilateral
   cooperation vehicle, corporate-entity immunities)

## Records committed (+3)

| ID | Sections | Raw PDF bytes | source_hash (first 16) |
|---|---|---|---|
| `si-zm-2017-042-income-tax-overseas-private-investment-corporation-approval-and-exemption-order-` | 22 | 142,912 | (see record) |
| `si-zm-2017-070-income-tax-african-management-services-company-approval-and-exemption-order-2017` | 27 | 147,909 | (see record) |
| `si-zm-2020-008-diplomatic-immunities-and-privileges-turkish-cooperation-and-coordination-agency` | 26 | 27,452 | 5a0e14536293141d |

All three followed the HTML-AKN → PDF-fallback pattern (AKN render
returned sparse HTML for these years; PDF source page extracted cleanly
with pdfplumber).

Titles pulled from og:title meta tag on the AKN page, sanity-checked
against the PDF header-line.

## Gaps (1)

| ID slot | Status | Cause |
|---|---|---|
| si/2019/025 | `pdf_parse_empty` | AKN HTML fetch 200 OK; PDF fetch 200 OK; pdfplumber could not extract text (likely scan-only / image-based PDF). Appended to `gaps.md`. Follow-up: OCR pass is out-of-scope for this tick. |

## Fetches (8 this batch)

| # | URL | Status | Bytes |
|---|---|---|---|
| 1 | `/akn/zm/act/si/2017/42` | 200 | 39,413 |
| 2 | `/akn/zm/act/si/2017/42/eng@2017-06-16/source.pdf` | 200 | 142,912 |
| 3 | `/akn/zm/act/si/2017/70` | 200 | 39,396 |
| 4 | `/akn/zm/act/si/2017/70/eng@2017-09-29/source.pdf` | 200 | 147,909 |
| 5 | `/akn/zm/act/si/2019/25` | 200 | ~39 KB |
| 6 | `/akn/zm/act/si/2019/25/eng@2019-03-22/source.pdf` | 200 | (parse empty) |
| 7 | `/akn/zm/act/si/2020/8` | 200 | ~39 KB |
| 8 | `/akn/zm/act/si/2020/8/eng@2020-01-31/source.pdf` | 200 | 27,452 |

Rate limit: 6 s inter-call (5 s ZambiaLII crawl-delay + 1 s margin) honoured.
robots.txt: `/akn/zm/act/si/` explicitly allowed.

## Integrity checks

All batch-scoped checks PASS for the 3 committed records:

- **CHECK1** unique IDs within batch — ✓ (3/3 distinct)
- **CHECK2** no HEAD prefix collision — ✓ (no existing record starts with
  any of the three slot prefixes)
- **CHECK3** source_hash matches on-disk raw PDF — ✓ (3/3)
- **CHECK4** amended_by / repealed_by / cited_authorities — ✓ (all empty;
  no unresolved cross-refs)
- **CHECK5** required fields present — ✓ (3/3: id, type, jurisdiction,
  title, citation, source_url, source_hash, fetched_at, parser_version,
  sections non-empty)

## Known infrastructure issue (not caused by this batch)

`corpus.sqlite-journal` is a stale (2026-04-15) rollback journal left by
a pre-existing long-dead session. The sandbox filesystem refuses `rm` on
this journal ("Operation not permitted"), so sqlite refuses to open the
database with `disk I/O error` and any in-place INSERTs are discarded on
reopen (the journal rolls them back). This predates batch 0179 — the
records table has been stuck at 535 rows since batch 0146 while on-disk
JSON records now number 1,200+. Recent batch reports silently skipped
the sqlite write; this one documents it openly. See `worker.log`.

**Net effect:** source-of-truth JSON records are authoritative and are
committed to git as normal; `corpus.sqlite` is logically out-of-date but
is not touched by this batch. A human-driven sqlite rebuild from records
is required to recover the full-text search surface.

## B2 raw sync

Deferred to host (rclone not available in sandbox). Peter to run:
```
rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
```

## Next tick plan

- `sis_corporate` discovery channels exhausted at ZambiaLII
  `/legislation/subsidiary` (1-10 valid, 11+ 404) and within the cached
  discovery HTML on disk. Remaining novel corporate candidates surfaced
  by existing discovery: 1 (si/2015/033 — deferred).
- **Pivot:** move to `sis_tax` (next in `priority_order`). ZambiaLII AKN
  tax-namespace SIs are not under `/legislation/subsidiary`; use the
  already-cached discovery pages' tax-keyword filter (income-tax SIs,
  customs/excise SIs) that were recorded as non-corporate candidates in
  batch 0177.
- Alternative pivot if tax discovery is thin: year-listing sweep at
  `/akn/zm/act/si/YYYY/` (different pagination channel from
  `/legislation/subsidiary`).
