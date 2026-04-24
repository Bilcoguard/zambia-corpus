# Batch 0186 — Phase 4 sis_employment (continuation)

**Batch:** 0186
**Phase:** phase_4_bulk — sub-phase sis_employment (priority_order item 4)
**Started:** 2026-04-24T15:04:58Z
**Completed:** 2026-04-24T15:06:01Z
**Worker:** kwlp-worker (peter@bilcoguard.com)

## Summary

5 residual sis_employment candidates from `_work/batch_0185_candidates.json`
(the 13-item discovery set produced by batch 0185 from the
`/legislation/?alphabet=N,P,W,F,O` listings) — specifically the pre-2003
NAPSA / pension / workmen's-compensation regulatory substrate that was
queued when batch 0185 reached its 8-record MAX_BATCH_SIZE ceiling.

All five records fetched, parsed, integrity-checked, and written.

## Records written

| SI | Title | Sections | PDF bytes | Sha256 (prefix) |
|----|-------|---------:|----------:|-----------------|
| si/2002/39 | Pension Scheme (Offshore Investments) Regulations, 2002 | 1 | 287,100 | `d44d83f1…` |
| si/2000/37 | Pension Scheme Regulation (Investment) (Exemption) Order, 2000 | 1 | 656,054 | `a1b94078…` |
| si/2000/34 | National Pension Scheme (Transfer of Employees) Order, 2000 | 4 | 650,439 | `82ca4da2…` |
| si/2000/22 | National Pension Scheme (Pensionable Earnings) Regulations, 2000 | 4 | 3,591,930 | `0b0d85a1…` |
| si/1994/39 | Workmen's Compensation (Assessment or Earnings) Regulations, 1994 | 4 | 188,197 | `c03bdf01…` |

Section counts of 1 for 2002/39 and 2000/37 are genuine — both are short
statutory orders whose operative clauses begin at numbered item 2
(item 1 being the citation / short-title paragraph that our section-regex
treats as a preamble). Re-inspection of the stored PDFs confirms the
text is real (not scan-only) and survives pdfplumber extraction cleanly
(~280–660 KB of vectorised text).

## Fetches

- 10 fetches total this tick (5 AKN HTML + 5 PDF fallback)
- All GETs respected ZambiaLII `Crawl-delay: 5` with +1s margin (6s between
  requests); User-Agent `KateWestonLegal-CorpusBuilder/1.0 (contact:
  peter@bilcoguard.com)` per approvals.yaml.
- Today cumulative: 181 / 2,000 fetches (9.05 %); tokens ~0 / 1,000,000.
- Sliced into two sub-ticks (`--slice=0:3` then `--slice=3:5`) to respect
  the sandbox 45 s bash-tool ceiling; resume via
  `_work/batch_0186_summary.json` checkpoint per the batch 0182 pattern.

## Integrity (batch-scoped)

- **CHECK1** unique IDs — PASS (5 novel IDs, no HEAD collision across
  1,239 records)
- **CHECK2** `amended_by` / `repealed_by` refs resolve — PASS (no
  cross-references; primary SIs)
- **CHECK3** `cited_authorities` refs resolve — PASS (none present)
- **CHECK4** `source_hash` matches on-disk raw — PASS (5/5 sha256
  verified against `raw/zambialii/si/YYYY/*.pdf`)
- **CHECK5** required fields present — PASS

## Gaps

None this batch.

## Sub-phase status after batch 0186

- `sis_corporate` — ~14 records (effectively exhausted on
  `/legislation/subsidiary`)
- `sis_tax` — 26 records
- `sis_employment` — **23 records** (+5 this batch); pre-2003 pension
  / workmen's-compensation pocket now filled. All 13 candidates from the
  batch 0185 discovery set are now ingested except si/2012/??? Truck-and-Bus
  base order (reference-only; no candidate row in the discovery set).

Cumulative SI records in HEAD after this batch: **161** (156 + 5).
Cumulative records overall: 1,244 (1,239 HEAD + 5 new).

## B2 raw sync

rclone not available in sandbox — B2 sync deferred to host:
`rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`

## Next-tick plan

sis_employment is now substantially covered across the NAPSA / pension /
workmen's-compensation / minimum-wages / factories corridor. Per
approvals.yaml `priority_order`, rotate to **case_law_scz** (item 5) next
tick. Candidate discovery channel: ZambiaLII judgment index
`https://zambialii.org/judgments/SCZ/` paginated by year.

Infrastructure follow-up (non-blocking): `corpus.sqlite` stale
rollback-journal still blocks in-sandbox FTS rebuild (JSON records remain
source of truth — sqlite rebuild is a host-side task for Phase 5).
