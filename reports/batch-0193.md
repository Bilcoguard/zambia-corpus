# Batch 0193 — Phase 4 sis_mining

- Started: 2026-04-24T18:35:00Z
- Completed: 2026-04-24T18:38:00Z
- Phase: phase_4_bulk
- Sub-phase: sis_mining (priority_order item 7)
- Records written: 5/5
- Fetches used: 10 (5 AKN HTML + 5 PDF)

## Records

- `si-zm-2016-007-mines-and-minerals-development-general-regulations-2016` — Mines and Minerals Development (General) Regulations, 2016 (240 sections; sha256 16ab08de891df2fa…; 842,403 bytes)
- `si-zm-2010-026-mines-and-minerals-development-mining-rights-and-non-mining-rights-order-2010` — Mines and Minerals Development (Mining Rights and Non-Mining Rights) Order, 2010 (2 sections; sha256 ba0383ef504a76cf…; 82,849 bytes)
- `si-zm-2009-027-mines-and-minerals-development-mining-rights-and-non-mining-rights-order-2009` — Mines and Minerals Development (Mining Rights and Non-Mining Rights) Order, 2009 (1 section; sha256 0f90069df34a0b83…; 153,225 bytes)
- `si-zm-2000-019-mines-and-minerals-environmental-exemption-order-2000` — Mines and Minerals (Environmental) (Exemption) Order, 2000 (1 section; sha256 fc5a4ddea09c9a91…; 332,051 bytes)
- `si-zm-2000-018-mines-and-minerals-royalty-remission-order-2000` — Mines and Minerals (Royalty) (Remission) Order, 2000 (1 section; sha256 a3991319980d50c5…; 893,894 bytes)

## Integrity

- CHECK1 unique IDs within batch: PASS
- CHECK2 no HEAD collision: PASS
- CHECK3 source_hash matches on-disk raw (5/5 sha256 verified): PASS
- CHECK4 no unresolved amended_by/repealed_by cross-refs: PASS
- CHECK5 required fields present: PASS

## Sub-phase notes

- First non-trivial expansion of sis_mining since corpus inception. Prior HEAD count: 1 record (si-zm-2020-028 Ndola Lime Remission). After this batch: 6 records.
- Discovery via `https://zambialii.org/legislation/subsidiary?alphabet=M` (4 mining-substance hits) plus parent-act back-references in `/akn/zm/act/2008/7` page (2 additional Mining Rights Orders). One historical SI ref — si/1995/166 — returned 404 on direct AKN probe; logged below.
- The 2016/7 General Regulations (240 parsed sections, 842 KB PDF) is the substantive regulatory backbone for the Mines and Minerals Development Act 2015 (Act 11 of 2015). The 2009/27 and 2010/26 Orders are the historical Mining Rights orders made under the predecessor Act 7 of 2008. The 2000/18 and 2000/19 Orders sit under the older Mines and Minerals Act 1995 (Act 31 of 1995).
- Cumulative SI records after this batch: 179 (+5). Cumulative judgment records: unchanged at 25. Sub-phase status: sis_mining 6 records.

## Robots / source-policy note

- ZambiaLII robots.txt observed this tick now contains `Disallow: /akn/zm/judgment/` for `User-agent: *`. Worker UA `KateWestonLegal-CorpusBuilder/1.0` falls under the wildcard rule, so further /akn/zm/judgment/ ingestion (case_law_scz, priority_order item 5) is now blocked by robots compliance. Logged to `gaps.md`. /akn/zm/act/ legislation paths remain allowed (only judgment + officialGazette are disallowed). This validates the rotation away from case_law_scz to sis_mining.

## Gaps

- si/1995/166 — referenced from /akn/zm/act/1995/31 (Mines and Minerals Act 1995) but returned HTTP 404 on direct AKN probe. Logged to gaps.md. Title not derivable from a 404 page; not invented.

## Next tick plan

- Continue sis_mining with second-tier extraction: probe /akn/zm/act/si/ slots for any MMDA 2015 derivative SIs not yet surfaced (Royalty regulations, Cadastre regulations, Mineral Rights Regulations 2018-2024 era). If yield thins below 3 candidates, rotate to sis_family (priority_order item 8).
- Infrastructure follow-up (non-blocking): rclone unavailable in sandbox — B2 sync deferred to host (`rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`). Stale corpus.sqlite rollback-journal still blocks in-sandbox FTS rebuild. 34 legacy-schema act JSON dupes under records/acts/ remain unresolved.
