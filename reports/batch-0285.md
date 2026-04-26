# Batch 0285 Report

**Phase:** 4 — bulk (acts_in_force, chronological-first sweep)
**Tick:** 2026-04-26 (UTC) — scheduled tick, 30-min cadence
**Yield:** 8/8 (100%)
**Wall-clock:** ~7 min
**Parser version:** 0.6.0-act-zambialii-2026-04-26

## Picks (8 chronological from inherited pool)

| Year/Num | Title | Alpha | Status | Sections |
|---|---|---|---|---|
| 2016/36 | Supplementary Appropriation (2016) Act, 2016 | S | ok | 2 |
| 2016/37 | Excess Expenditure Appropriation (2013) Act, 2016 | E | ok | 2 |
| 2016/38 | Supplementary Appropriation (2014) Act, 2016 | S | ok | 3 |
| 2016/39 | Supplementary Appropriation (2016) Act, 2016 | S | ok | 2 |
| 2016/48 | Excess Expenditure Appropriation Act, 2016 | E | ok | 2 |
| 2016/49 | Appropriation Act, 2016 | A | ok | 3 |
| 2017/8  | Supplementary Appropriation (2017) Act, 2017 | S | ok | 2 |
| 2017/21 | Supplementary Appropriation (2017) Act, 2017 | S | ok | 3 |

All 8 picks fell through to the PDF fallback path (HTML akn-section count <2 each); all PDFs were under MAX_PDF_BYTES (4.5 MB).

## Integrity

- CHECK1a: 8/8 batch unique — PASS
- CHECK1b: 8/8 corpus presence — PASS
- CHECK2:  0 amended_by refs — PASS
- CHECK3:  0 repealed_by refs — PASS
- CHECK4:  8/8 source_hash sha256 verified vs raw HTML — PASS
- CHECK5:  128/128 required fields present — PASS
- CHECK6:  0 cited_authorities refs — PASS

## Provenance

Source: zambialii.org (`/akn/zm/act/{yr}/{num}` HTML + `source.pdf` fallback)
User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`
Crawl-delay: 6s (1s margin over robots.txt 5s)
robots.txt sha256: `fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0` (unchanged)

## Pool

- Inherited from batch 0284: 38 items
- Processed this tick: 8
- Remaining for batch 0286: 30 (next: 2017/22 Appropriation Act, 2017)

## Budget

- Today (2026-04-26 UTC) fetches at tick start: 580/2000 (~29%)
- Today (2026-04-26 UTC) fetches at tick end:   ~596/2000 (~29.8%)
- Token budget: within limits

## B2 sync

`rclone` not available in sandbox — B2 sync deferred to host. Peter to run:

```
rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
```

## Next-tick plan

- Refresh inherited pool, sweep next 8 chronological from `2017/22` onwards.
- Window includes 2018/1 Public Finance Management Act and 2018/8 Credit Reporting Act — non-fiscal, expect HTML akn-section path success.
