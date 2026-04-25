# Batch 0227 Report

**Phase:** 4 (Bulk ingest)
**Tick window:** 2026-04-25T14:32:00Z – 2026-04-25T14:55:00Z
**Mode:** Fresh L-alphabet probe (4 sis_local_government picks) + drain of batch 0226's 4 unused Forest reserves (sis_environment)
**Outcome:** 8/8 records ingested (100% yield) • integrity PASS

## Records ingested

| # | SI | Sub-phase | Pages | Chars | Effective date |
|---|----|-----------|-------|-------|----------------|
| 1 | 2022/16 Local Authorities Superannuation Fund (Pension Management) Rules | sis_local_government | 26 | 44,717 | 2022-04-08 |
| 2 | 2021/10 Kasama Municipal Council (Vehicle Loading and Parking Levy) By-laws | sis_local_government | 4 | 4,112 | 2021-02-12 |
| 3 | 2020/14 Local Government (Fire Services) Order, 2020 | sis_local_government | 2 | 892 | 2020-02-21 |
| 4 | 2019/44 Local Government (Fire Inspectors and Fire Officers) Order, 2019 | sis_local_government | 6 | 4,495 | 2019-06-21 |
| 5 | 2020/13 National Forest No. F.12 Luano (Alteration of Boundaries) Order | sis_environment | 2 | 3,345 | 2020-02-07 |
| 6 | 2021/3 National Forest No. F31 Kabwe (Alteration of Boundaries) Order | sis_environment | 4 | 5,159 | 2021-01-08 |
| 7 | 2021/2 Kasama National Forest No. P. 47 (Alteration of Boundaries) Order | sis_environment | 2 | 3,463 | 2021-01-08 |
| 8 | 2021/1 Forest Reserve No. 4 Maposa (Cessation) Order | sis_environment | 2 | 1,977 | 2021-01-08 |

(Effective dates derived from `eng@YYYY-MM-DD` in the PDF source URL.)

## Sub-phase footprint expansion

- **sis_local_government** +4 records — most substantive addition is **2022/16 Local Authorities Superannuation Fund (Pension Management) Rules** (26 pp / 44.7K chars), which complements the 3 prior local-government records in the corpus. New parent-Act linkage: **Local Authorities Superannuation Fund Act** (first entry in corpus).
- **sis_environment** +4 records — completes the Forests Act alteration/cessation cluster started in batch 0226. All 4 reserves parsed cleanly (0% scanned-image rate), confirming batch 0226's late-tick observation that modern F-alphabet alteration orders are text-extractable.

## Fetches used

| Component | Count | URLs |
|-----------|-------|------|
| Robots reverify | 1 | zambialii.org/robots.txt |
| Discovery probe | 1 | alphabet=L listing page |
| Record HTML | 8 | /akn/zm/act/si/{yr}/{num} |
| Record PDF | 7* | source.pdf endpoints |
| **Total today** | 17 (this tick) → 465/2000 cumulative | |

\* One PDF (2021/1 Maposa Cessation) was already cached on disk from a prior probe; sha verified, no re-fetch.

Today's fetch count: **465 / 2000** (23.25%) — well within budget. All on zambialii.org, observed 6 s crawl-delay margin against robots-declared 5 s.

## Integrity (CHECK1a–CHECK6)

- CHECK1a — batch unique IDs: PASS (8/8 unique)
- CHECK1b — corpus presence on disk: PASS (8/8 present)
- CHECK2 — amended_by references: PASS (0 refs)
- CHECK3 — repealed_by references: PASS (0 refs)
- CHECK4 — source_hash matches raw file: PASS (8/8 verified)
- CHECK5 — required fields present: PASS (10 fields × 8 records)
- CHECK6 — cited_authorities references: PASS (0 refs)

Overall: **PASS**.

## Robots.txt re-verify

`https://zambialii.org/robots.txt` re-fetched at tick start; sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193–0226. Crawl-delay 5 s honoured at 6 s margin. Disallow on `/akn/zm/judgment/` and `/akn/zm/officialGazette/` enforced (judgments crawl remains paused).

## Cumulative SI records

After this batch: **411** SI records (+8 over batch 0226's 403). Judgments unchanged at 25 (paused per robots Disallow).

## Discovery yield

Single fresh alphabet probe (L) surfaced **11 novel modern (>=2017) candidates** against a 309-pair raw HTML baseline. Picks chosen: 4 substantive (Pension Rules, Vehicle Levy By-laws, two Fire Services Orders). 7 candidates remain unused as next-tick reserves: 2020/34 Laws of Zambia (Specified Date) Notice; 2022/71 Kafue + 2020/95 Kalumbila + 2020/67 Kitwe + 2020/66 Lusaka Local Govt Administrator Appointment Orders; 2019/77 Chembe Town Council Sugar Cane Levy By-laws; 2019/47 Local Government (Fire Services) Order 2019.

## SQLite update

`corpus.sqlite` insert deferred — same stale rollback-journal blocking writes since batches 0192+. JSON record files in `records/sis/` are authoritative; sqlite FTS rebuild remains queued for host-side cleanup.

## B2 raw sync

`rclone` not available in sandbox. B2 sync of `raw/` deferred to host. Peter to run:
```
rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
```
This batch contributes 16 raw files (8 HTML + 7 fresh PDF + 1 reused PDF already on disk) plus 1 robots.txt + 1 alphabet=L listing.

## Phase 4 status

Phase 4 remains incomplete per `approvals.yaml` (worker does not flip the flag). Next-tick options:

1. Drain remaining 7 L-alphabet candidates (mostly Local Government Administrator appointment orders — likely short scanned-image declarations; expected yield 1–3 substantive records).
2. Fresh probe on an unprobed alphabet from {U, X, Y, Z} (or re-probe one of the prior alphabets to surface candidates that didn't make earlier picks).
3. Rotate to `acts_in_force` priority_order item 1 — would require Acts-listing endpoint discovery (the SI ingest path is not directly applicable).
4. OCR backlog from batches 0225/0226 (5 unparseable PDFs awaiting tesseract).

## Tick-time accounting

Started ~14:32 Z (post-tick-init), records 0–7 ingested across ~12 m wall-clock with the per-record 35–40 s subprocess pattern. Robots reverify + discovery + 8 picks completed inside the 20 m cap with margin.
