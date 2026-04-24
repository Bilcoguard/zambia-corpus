# Batch 0175 — Phase 4 sis_corporate ingest + pages 5/6 discovery

- started: 2026-04-24T09:35:26Z
- finished: 2026-04-24T09:36:01Z
- fetches: 6
- committed: 2
- gapped: 0

## Records committed

- **si-zm-2020-027-income-tax-remission-ndola-lime-company-limited-order-2020**
    - title: Income Tax (Remission) (Ndola Lime Company Limited) Order, 2020
    - sections: 2
    - theme: corporate-tax-remission
    - source_url: https://media.zambialii.org/media/legislation/21005/source_file/674aab13366aa524/zm-act-si-2020-27-publication-document.pdf
    - source_hash: sha256:8ee9a2f95e203178310cc788cd91edf70f8534a1d679647bce32b8b706c686fc
    - record_path: records/sis/2020/si-zm-2020-027-income-tax-remission-ndola-lime-company-limited-order-2020.json
    - raw_path: raw/zambialii/si/2020/si-zm-2020-027-income-tax-remission-ndola-lime-company-limited-order-2020.pdf
- **si-zm-2020-028-mines-and-minerals-development-remission-ndola-lime-company-limited-regulations-2020**
    - title: Mines and Minerals Development (Remission) (Ndola Lime Company Limited) Regulations, 2020
    - sections: 2
    - theme: corporate-tax-remission
    - source_url: https://media.zambialii.org/media/legislation/21004/source_file/d310661032c82fa1/zm-act-si-2020-28-publication-document.pdf
    - source_hash: sha256:f64440c3396b1a3d69fbbea062019b5c64657a373b8438d637c909e5c251b040
    - record_path: records/sis/2020/si-zm-2020-028-mines-and-minerals-development-remission-ndola-lime-company-limited-regulations-2020.json
    - raw_path: raw/zambialii/si/2020/si-zm-2020-028-mines-and-minerals-development-remission-ndola-lime-company-limited-regulations-2020.pdf

## Gaps

_(none this batch)_

## Discovery (pages 5 & 6)

- page 5: 50 unique SIs, sha256=1be5e4f1b4fddc26..., 162532 bytes
- page 6: 50 unique SIs, sha256=2d6f82fb9dc80c84..., 161889 bytes

## Novel corporate candidates surfaced (count: 6)

- SI 2019/11 (page 6): Customs and Excise (Suspension) (Fuel) Regulations, 2019  _(matched: pension)_
- SI 2019/25 (page 6): Income Tax Act (Suspension of tax on payment of interest to non-resident) (Treasury Bill and Bond) Regulations, 2019  _(matched: pension)_
- SI 2019/59 (page 5): Insurance (Fidelity Fund) Regulations, 2019  _(matched: insur)_
- SI 2019/62 (page 5): Income Tax (Konoike Construction Company Limited) (Approval and Exemption) Order, 2019  _(matched: compan)_
- SI 2018/36 (page 6): Customs and Excise (Excise Duty) (Cut rag) (Suspension) Regulations, 2018  _(matched: pension)_
- SI 2018/61 (page 6): Customs and Excise (Suspension) (Fuel) Regulations, 2018  _(matched: pension)_

## Novel non-corporate candidates (count on pages 5+6): 75

## Integrity

- CHECK1 unique IDs in batch: PASS
- CHECK2 no HEAD collision: PASS
- CHECK3 source_hash matches raw file on disk: PASS
- CHECK4 no new unresolved amended_by/repealed_by/cited_authorities refs: PASS (none introduced)
- CHECK5 required fields present: PASS

## Notes

- robots.txt: /akn/zm/act/si/ and /legislation/subsidiary both Allow: / under zambialii.org robots; 5s crawl-delay honoured per-fetch.
- HTML pages sparse (0 akn sections) for both ingests — PDF fallback /eng@.../source.pdf used; PDF sections structure-extracted.
- Parser produced 2 sections each — these SIs are short remission orders (1-2 operative paragraphs + schedule); consistent with one-company tax remission instrument structure.
- B2 sync deferred to host: rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4
