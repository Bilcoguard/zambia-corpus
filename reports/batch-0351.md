# Batch 0351 — Phase 5 ZMCC ingestion (continuation)

**Date (UTC):** 2026-04-29
**Phase:** phase_5_judgments (approved+incomplete)
**Slice:** ZMCC 2024/{5, 4, 3, 2, 1} — completes the 2024 most-recent-first sweep started at b0348.
**Parser version:** 0.3.0 (frozen from b0348/b0349/b0350, unchanged)
**Fetcher:** dateless canonical URL pattern (frozen from b0348)

## Fetch

All 5 raw HTML+PDF pairs persisted to `raw/zambialii/judgments/zmcc/2024/`.
The first sandbox run of the fetcher (START=0 END=5) timed out partway
through the 02 record (05/04/03 fully written, 02 HTML written, PDF
not yet, 01 not yet attempted). Continued in a second shard (START=3
END=5); the existence-check skipped 03 cleanly and re-fetched 02's
HTML+PDF + 01's HTML+PDF. Final on-disk pair counts are correct.

| Year/# | Date | HTML bytes | PDF bytes |
|--------|------|------------|-----------|
| 2024/5 | 2024-03-15 | 43,366 |  1,469,606 |
| 2024/4 | 2024-02-23 | 45,170 |    632,958 |
| 2024/3 | 2024-02-09 | 49,531 |  1,428,408 |
| 2024/2 | 2024-01-17 | 44,286 |    508,359 |
| 2024/1 | 2024-01-25 | 48,796 |  3,368,085 |

Dates for 05/04/03 were not captured in a fetch log (the
sandbox-timeout run died before log persistence) and were recovered
post-hoc from the `eng@YYYY-MM-DD` token already embedded in the saved
HTML — no extra HTTP requests, no fabrication.

Fetcher: `scripts/batch_0351_fetch.py` (driven from b0350 with new
TARGETS slice; all other logic byte-identical).

## Parse

`scripts/batch_0351_parse.py` (parser_version 0.3.0, frozen from b0350)
wrote **0 records** and **deferred 5**.

### Written

(none — see deferrals below)

### Deferred (no fabrication — per BRIEF.md non-negotiable #1)

All five deferrals are `outcome_not_inferable_under_tightened_policy`.
Raw HTML+PDF remain on disk and can be revisited later if the parser
acquires hand-anchored PDF order paragraphs or the locked summary
regex list is widened (a parser_version bump, not a tick-time change).

| Candidate | Date | Summary head |
|-----------|------|--------------|
| [2024] ZMCC 5 (Milingo Lungu v AG & Anor) | 2024-03-15 | "The Constitutional Court lacks power to stay subordinate criminal proceedings; the single judge's stay was nullified and discharged." |
| [2024] ZMCC 4 (Moses Sakala v AG & Anor) | 2024-02-23 | "Intended Party joined as 3rd Respondent because the reliefs directly affect him; no costs awarded." |
| [2024] ZMCC 3 (Hastings Mwila v Local Authorities Superannuation Fund) | 2024-02-09 | "Whether the petitioner should have remained on the respondent's payroll pending payment of a commuted LASF lump-sum pension benefit." |
| [2024] ZMCC 2 (Institute of Law, Policy Research & Human Rights) | 2024-01-17 | "An individual directly affected by interpretation of Article 74(2) may be joined as an interested party to adjudicate rights and issues." |
| [2024] ZMCC 1 (Bowman Chilosha Lusambo v Bernard Kanengo & Ors) | 2024-01-25 | "Nomination disputes belong to Article 52(4) proceedings; election petitions require proving substantial non‑compliance affecting results." |

All five raw pairs remain on disk under
`raw/zambialii/judgments/zmcc/2024/`. No re-fetch will be required when
the parser is widened. Raw SHAs:

| Year/# | source_hash (HTML) | raw_sha256 (PDF) |
|--------|--------------------|------------------|
| 2024/5 | sha256:2024812b8a97305d7b79be81b867a97b9652d3ea3cc687a702a0a205499eaf97 | sha256:211290645569b9a99ca945da81c54e80cb414351c177599c2391b9b4cb4f984f |
| 2024/4 | sha256:6833b0a8650df1542964bd022b5de30925b75353dac2e97aa6a287c5a7a729d1 | sha256:954a89ac04785d569d2b9251f7de4e122e19f897a61d07e60c583afd9e428ac8 |
| 2024/3 | sha256:0bd814d62fe13394309f8b2a91a6cb12ebb727b5a13a7773227639b1f63dd48d | sha256:09dccabc6fb7b45aa1c5be2322e3b2c19822700bfc4345c676f4302658e116c7 |
| 2024/2 | sha256:0e77059c3220252bcd2b5e36be325671bd4c4f7b61bd7b0dac6b90b689ae443e | sha256:923910e3043b3c351a4a4832f2b68e9462f786380de5bc0baf44694db36db27e |
| 2024/1 | sha256:3e4825dadc9cae7a22f851e0b2889d2a8380e1d069f8ff606a800012996d55b9 | sha256:b0e311f5c10dad7953fdda7cbe9f3eeddde4ed7e732ce7b8477bee077c3aee85 |

## Integrity checks (PASS — vacuous)

`scripts/integrity_check_b0351.py`:

```
INTEGRITY CHECK: PASS (0 record(s))
```

With no records written this tick, the integrity check is vacuously
true — there are no IDs to dedupe, no judges to resolve, no hashes to
verify. The check still runs end-to-end against the empty written-set
and passes; the report files ten the existing 5 dup-id files in
`records/acts/` from b0128/b0264/b0289 lineage are unchanged.

## Judges registry

No new aliases or canonicals — nothing was written.

## Budget impact

- Effective HTTP fetches this tick: ~9 (5 HTML + 5 PDF, minus the 03
  pair which was correctly skipped on the second shard, plus one
  wasted re-fetch of 02's HTML caused by the sandbox-timeout in the
  first shard). Counted as 9 in `costs.log`.
- Cumulative today: 175 → 184/2000 fetches (~9.2%).
- Tokens: well under daily cap (no LLM calls in this tick — pure
  fetch+parse).
- B2 sync deferred to host (rclone not in sandbox).

## sqlite

`corpus.sqlite` not modified this tick (no new judgment rows). The
pre-existing B-tree corruption flagged on prior `PRAGMA integrity_check`
runs (pages 84..99) remains; the file-based JSON corpus is the
canonical source of truth and will need a dedicated maintenance tick
to rebuild sqlite from `records/*.json`.

## Phase 5 progress

* Records ingested this tick: 0.
* Phase 5 cumulative: still **21 / 100–160** target (no change from
  end-of-b0350 state).
* ZMCC 2025 numeric sequence exhausted (1..33 all attempted).
* ZMCC 2024 numeric sequence now exhausted (1..27 all fetched on
  disk). ZMCC 2024 ingested: {9, 12, 14, 24, 26}. ZMCC 2024 deferred
  (raw on disk): {1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 13, 15, 16, 17, 18,
  19, 20, 21, 22, 23, 25, 27}.
* This is the **first parser-deferred zero-write tick** in the Phase 5
  sweep (it does NOT count as a "zero-discovery tick" under the BRIEF
  completion criterion — the source has plenty of remaining ZMCC 2023+
  candidates, and the deferrals are due to tightened parser policy,
  not source exhaustion).

## Notes / sandbox

`.git/objects/maintenance.lock` was present at tick start (Operation
not permitted to delete via the standard `find .git -name '*.lock'
-delete` step — sandbox can list but not unlink that particular lock).
The pull and subsequent commit succeeded regardless; the lock is
effectively a no-op for the worker's commit path.

The fetcher's sandbox-timeout caused one wasted HTML re-fetch of 02;
no records were corrupted and integrity passed cleanly. Future ticks
should consider sharding the fetch slice into ≤3-record shards if the
PDF sizes look heavy.

## Next tick

ZMCC 2024 numeric sequence is now exhausted. Step into ZMCC 2023
most-recent-first. The 2023 top number is unknown — first sub-shard
should probe the dateless URL for ZMCC 2023/{some plausible top, e.g.
30} to discover the actual top via 302-redirect (or 404). Phase 5
remains approved+incomplete — worker does not flip approval flags.
