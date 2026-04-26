# Batch 0249 Report — Phase 4 Bulk Ingest

**Date:** 2026-04-26
**Phase:** phase_4_bulk
**Batch:** 0249
**Yield:** 8/8 (100%)
**Records:** +8 SIs (sis_industry +1 [NCC Exemption Regs 2004/22] + sis_governance +7 [historic 1980s-1990s era])

## Records ingested

| ID | Year/Num | Title | Parent Act | Sub-phase | Pages | Chars |
|----|----------|-------|------------|-----------|-------|-------|
| si-zm-2004-022-national-council-for-construction-exemption-regulations-2004 | 2004/22 | National Council for Construction (Exemption) Regulations, 2004 | National Council for Construction Act | sis_industry | 2 | 1,390 |
| si-zm-1986-032-national-archives-place-of-deposit-declaration-order-1986 | 1986/32 | National Archives (Place of Deposit) (Declaration) Order, 1986 | National Archives Act, 1969 | sis_governance | 1 | 898 |
| si-zm-1987-029-equity-levy-exemption-order-1987 | 1987/29 | Equity Levy (Exemption) Order, 1987 | Equity Levy Act, 1982 | sis_governance | 1 | 721 |
| si-zm-1987-036-national-savings-and-credit-appointment-of-members-of-board-order-1987 | 1987/36 | National Savings and Credit (Appointment of Members of Board) Order, 1987 | National Savings and Credit Act, 1972 | sis_governance | 1 | 1,255 |
| si-zm-1988-038-emergency-essential-supplies-and-services-regulations-1988 | 1988/38 | Emergency (Essential Supplies and Services) Regulations, 1988 | Emergency Powers Act, 1964 | sis_governance | 3 | 4,840 |
| si-zm-1993-037-emergency-regulations-1993 | 1993/37 | Emergency Regulations, 1993 | Emergency Powers Act, 1964 | sis_governance | 2 | 847 |
| si-zm-1995-029-national-archives-fees-regulations-1995 | 1995/29 | National Archives (Fees) Regulations, 1995 | National Archives Act, 1969 | sis_governance | 2 | 1,919 |
| si-zm-1995-030-national-archives-place-of-deposit-revocation-order-1995 | 1995/30 | National Archives (Place of Deposit) (Revocation) Order, 1995 | National Archives Act, 1969 | sis_governance | 2 | 1,033 |

**Total:** 14 pages / 12,903 chars across 8 records.

## Sub-phase footprint

- **sis_industry +1:** Extends NCC Act cluster (2004/22 NCC Exemption — historic 2004 amendment of the NCC framework).
- **sis_governance +7:** FOUR FIRST parent-Act linkages in this single tick — National Archives Act, 1969 (3 records); Equity Levy Act, 1982 (1); National Savings and Credit Act, 1972 (1); Emergency Powers Act, 1964 (2).

## Pure cache-drain tick

Drained 8 of 9 reserved residuals from batch 0248 (alphabet=E + alphabet=N caches). 1 residual reserved for next tick: 1985/14. **Discovery cost: 1 robots reverify only — zero fresh listing probes.**

## Costs

- Today's fetches: 107 / 2000 (5.4%)
- This batch: 1 robots + 16 record fetches (8 HTML + 8 PDF) = 17 fetches
- Tokens: within budget

## Surprise vs. plan

Batch 0248 close-out predicted 60-80% pdf_parse_empty rate for 1980s-1990s residuals (likely scanned-image PDFs). **Reality: 100% text-extractable** — 0% scanned-image rate. All 8 historic SIs (oldest = 1986/32) parsed cleanly with pdfplumber; pdf_text_chars range 721-4,840.

## Integrity

CHECK1a (batch unique 8/8) + CHECK1b (corpus presence 8/8) + CHECK2/3 (0 amended_by/repealed_by refs) + CHECK4 (sha256 verified 8/8 against raw/zambialii/si/(1986,1987,1988,1993,1995,2004)/) + CHECK5 (10 fields x 8 records all present) + CHECK6 (0 cited_authorities refs) — **ALL PASS**.

## Robots compliance

Re-verified at tick start: sha256 prefix `fce67b697ee4ef44` unchanged from batches 0193-0248. Crawl-delay 5s honoured at 6s margin. Disallow on /akn/zm/judgment/ + /akn/zm/officialGazette/ enforced (no fetches under those paths).

## User-Agent

`KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`

## Cumulative

- SI records after batch: 575 (+8 over 567 in batch 0248)
- Judgments: 25 (paused per robots Disallow)

## Next-tick plan

(a) Drain final residual 1985/14 + fresh probes from unprobed alphabets (A/B/C/D/F/H/I/J/L/M/P/S/T/V/W/U/X/Y/Z minus those already probed); (b) rotate to acts_in_force priority_order item 1 (requires Acts-listing endpoint discovery — separate path from SI ingest); (c) OCR retry on backlog (still 14 items unchanged) once tesseract is wired.

## Infrastructure follow-up (non-blocking)

- B2 sync deferred to host (rclone unavailable in sandbox).
- corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild (deferred to host).
- Persistent virtiofs unlink-failure warnings on .git/HEAD.lock + index.lock (Operation not permitted) — workaround stable: GIT_INDEX_FILE bypass via /tmp temp index.
- 488+ pre-existing untracked records files unchanged this tick — long-standing infrastructure backlog.
