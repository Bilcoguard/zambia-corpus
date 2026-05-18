# Batch b0709-jiw — multi-source judgment sweep

- Started: 2026-05-18T16:13:49Z
- Worker: judgment-ingestion-worker
- Mode: priority-(c,d,e) SCZ+ZMCC+HC sweeps from judiciaryzambia.com
- Parser: 0.4.2-jiw-b0709
- Fetches: 112 (cumulative today: ~176/500)
- Bandwidth: 550203933 bytes
- Records inserted: 0
- Records deferred: 59
- DB pre/post: records=1961->1961, fts=1961->1961
- Integrity (CHECK8): True

## Sweep results

- SCZ page-2: cands=16, inserted=0
- ZMCC page-1: cands=15, inserted=0
- SCZ page-3: cands=16, inserted=0
- HC page-2: cands=12, inserted=0

## Inserted


## Deferred

- https://judiciaryzambia.com/the-child-justice-forum/: no-pdf-url-found
- https://judiciaryzambia.com/2023-hpf-d237-bridget-chitambala-banda-vs-billy-banda-2024-matandala-j/: pdf-fetch-fail:UnicodeEncodeError
- https://judiciaryzambia.com/scz-7-32-2024-kapsch-trafficcom-south-africa-holding-pty-ltd-vs-intelligent-mobility-solutions-lt-sep-2025-justice-malila-kaoma-chisanga-jjs/: pdf-fetch-fail:UnicodeEncodeError
- https://judiciaryzambia.com/scz-7-25-2024-emmanuel-tumba-and-6-others-vs-zambia-bata-shoe-company-aug-2025-malila-mtuna-chisanga-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/appeal-no-10-of-2025-ronald-kaoma-chitotela-vs-anti-corruption-commission-and-3-others-aug-2025-malila-kaaoma-chisanga-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/scz-8-01-2021-attorney-general-and-commission-of-lands-vs-metro-investments-ltd-and-centina-transport-ltd-and-lusaka-city-council-july-2025-justice-musonda-wood-and-mutuna-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/appeal-no-4-of-2020-attorney-general-vs-rajan-mahthani-july-2025-justice-mutuna-js/: quality-gate-no-text
- https://judiciaryzambia.com/app-4-of-2020-the-attorney-general-vs-rajan-mahthani-apr-2025-justice-musonda-kabuka-mutuna-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/scz-8-011-2022-faustin-kabwe-bimal-thaker-vs-ndola-trust-school-ltd-attorney-general-mar-202-justice-musonda-kaoma-and-kabuka-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/app-no-07-2024-star-drilling-and-exploration-ltd-vs-national-technologies-ltd-and-11-others-feb-2025-justice-mutuna-js/: quality-gate-no-text
- https://judiciaryzambia.com/app-no-07-2024-star-drilling-and-exploration-ltd-vs-national-technologies-ltd-and-11-others-feb-2025-justice-mutuna-js-2/: duplicate-source-hash-in-batch
- https://judiciaryzambia.com/app-04-2023-zamtel-vs-felix-musonda-and-29-others-feb-2025-justice-musonda-wood-chisanga-jjs/: exception:OperationalError
- https://judiciaryzambia.com/2025-ccz-0019-mputa-ngalande-vs-attorney-general-may-2026-munalula-chisunka-mulongoti-kawimbe-and-mulife-jjc/: exception:OperationalError
- https://judiciaryzambia.com/false-social-media-claims-alleging-the-resignation-of-the-chief-justice-of-zambia/: exception:OperationalError
- https://judiciaryzambia.com/2023-hpf-640-chambata-banda-1-other-vs-simba-international-school-2-others-april-2026-justice-t-s-musonda/: exception:OperationalError
- https://judiciaryzambia.com/chief-justice-dr-munba-malila-sc-congratulates-hon-mr-justice-martin-sitwala-mwanwambwa-on-his-election-as-president-of-the-comesa-court-of-justice/: exception:OperationalError
- https://judiciaryzambia.com/the-child-justice-forum/: no-pdf-url-found
- https://judiciaryzambia.com/appeal-no-172-2018-like-silishebo-vs-the-people-jun-2019-justice-j-chinyamajs/: no-pdf-url-found
- https://judiciaryzambia.com/2025-ccz-0019-mputa-ngalande-vs-attorney-general-may-2026-munalula-chisunka-mulongoti-kawimbe-and-mulife-jjc/: duplicate-source-hash-in-batch
- https://judiciaryzambia.com/2025-ccz-003-zambia-civil-liberties-union-vs-commissioner-for-refuges-and-3-others-feb-2026-coram-munalula-shilimi-musaluke-chisunka-mulongoti-mwandenga-and-mulife-jjc/: quality-gate-no-text
- https://judiciaryzambia.com/2026-ccz-001-peoples-action-for-the-countrys-transformation-vs-electral-commission-of-zambia-mar-2026-coram-shilimi-musaluke-chisunka-mulongoti-mwandenga-kawimba-and-mulife-jjc/: quality-gate-no-text
- https://judiciaryzambia.com/2025-ccz-0011-munir-zulu-vs-the-attorney-general-2-others-mar-2026-coram-shilimi-musaluke-mwandenga-kawimbe-and-mulife-jjc/: quality-gate-no-text
- https://judiciaryzambia.com/2025-ccz-0010-munir-zulu-vs-the-attorney-general-2-others-mar-2026-coram-shilimi-musaluke-mwandenga-kawimbe-and-mulife-jjc/: quality-gate-no-text
- https://judiciaryzambia.com/2025-ccz-0025-climate-action-professionals-zambia-vs-the-attorney-general-mar-2026-coram-munalula-chisunka-mulongoti-kawimbe-and-mulife-jjc/: quality-gate-no-text
- https://judiciaryzambia.com/2025-ccz-0032-makebi-zulu-vs-attorney-general-feb-2026-justice-munalula-shilimi-musaluke-chishunka-mulongtoti-mwendenga-and-kawimbe-jjc/: quality-gate-no-text
- https://judiciaryzambia.com/2025-ccz-0029-law-association-of-zambia-5-others-vs-the-attorney-general-feb-025-coram-munalula-shilimi-musaluke-chisunka-mwandenga-and-mulife-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/2025-ccz-002-morgan-ngona-vs-attorney-general-and-miles-bwalya-sampa-jan-2026-justice-musaluke-chisunka-mulongoti-mwandenga-kawimbe-and-mulife-jcc/: quality-gate-no-text
- https://judiciaryzambia.com/2024-ccz-0019-tresford-chali-vs-the-judicial-complaints-commission-and-attorney-general-jan-2026-justice-shilimi-musaluke-chisunka-mulongoti-mwandenga-kawimbe-and-mulife-jcc/: quality-gate-no-text
- https://judiciaryzambia.com/false-social-media-claims-alleging-the-resignation-of-the-chief-justice-of-zambia/: duplicate-source-hash-in-batch
- https://judiciaryzambia.com/2023-hpf-640-chambata-banda-1-other-vs-simba-international-school-2-others-april-2026-justice-t-s-musonda/: duplicate-source-hash-in-batch
- https://judiciaryzambia.com/chief-justice-dr-munba-malila-sc-congratulates-hon-mr-justice-martin-sitwala-mwanwambwa-on-his-election-as-president-of-the-comesa-court-of-justice/: duplicate-source-hash-in-batch
- https://judiciaryzambia.com/the-child-justice-forum/: no-pdf-url-found
- https://judiciaryzambia.com/2017-ccz-004-dr-daniel-pule-3-others-v-attorney-general-davies-mwila-oct-2017-justice-mulenga/: no-pdf-url-found
- https://judiciaryzambia.com/app-no-1516-2021-davies-chishala-and-tony-nyembe-vs-the-people-jan-2025-justice-malila-hamaundu-and-kaoma-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/scz-8-011-2022-faustin-kabwe-1-other-vs-ndola-trust-school-ltd-aug-2024-justice-malila-hamaundu-kaoma-mutuna-and-chisanga-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/app-03-2024-road-development-agency-and-safricas-zambia-limited-7th-august-2024-justice-malila-cj-hamaundu-and-mutuna-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/app-011-2022-billis-farm-ltd-1-and-molosoni-chipabwamba-others-july-2024-justice-malila-hamaundu-chisanga-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/app-011-2023-finsbury-investments-ltd-and-murray-roberts-construction-1-other-24th-july-2024-justice-malila-cj-kaoma-and-kabuka-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/scz-8-05-2023-jayesh-shah-vs-mwenda-mwimanenwa-nyambe-1-other-24th-july-2024-justice-malila-cj-wood-and-kabuka-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/app-03-2022-benson-kaunda-vs-the-people-6th-june-2024-justice-hamaundu-kaoma-and-chinyama-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/app-010-2024-kalaluka-mushoke-and-the-people-10th-june-2024-justice-malila-cj-hamaundu-nd-chusanga-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/app-012-2022-mike-muloba-vs-the-people-6th-june-2024-justice-hamaundu-kaoma-and-chinyama-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/app-021-022-2023-dickson-shamboko-1-other-and-the-people-11th-june-2024-justice-malila-cj-hamahundu-and-chisanga-jjs/: quality-gate-no-text
- https://judiciaryzambia.com/2025-ccz-0019-mputa-ngalande-vs-attorney-general-may-2026-munalula-chisunka-mulongoti-kawimbe-and-mulife-jjc/: duplicate-source-hash-in-batch
- https://judiciaryzambia.com/false-social-media-claims-alleging-the-resignation-of-the-chief-justice-of-zambia/: duplicate-source-hash-in-batch
- https://judiciaryzambia.com/2023-hpf-640-chambata-banda-1-other-vs-simba-international-school-2-others-april-2026-justice-t-s-musonda/: duplicate-source-hash-in-batch
- https://judiciaryzambia.com/chief-justice-dr-munba-malila-sc-congratulates-hon-mr-justice-martin-sitwala-mwanwambwa-on-his-election-as-president-of-the-comesa-court-of-justice/: duplicate-source-hash-in-batch
- https://judiciaryzambia.com/the-child-justice-forum/: no-pdf-url-found
- https://judiciaryzambia.com/appeal-no-20-2018-juldan-motors-ltd-july-danobo-vs-nasser-ibrahim-olypa-sibongile-danobo-feb-2019-justice-mulongotija/: no-pdf-url-found
- https://judiciaryzambia.com/hp-208-2023-the-people-vs-phillip-zyambo-1-other-feb-2024-justice-siloka/: quality-gate-no-text
- https://judiciaryzambia.com/hpa-20-2025-violet-zulu-vs-the-people-jan-2026-justice-newa/: quality-gate-no-text
- https://judiciaryzambia.com/2023-hpf-531-alex-chibwe-vs-agness-siwale-may-2024-justice-bah-matandala/: quality-gate-no-text
- https://judiciaryzambia.com/2011-hp-576-mary-zulu-1-other-vs-attorney-general-jul-2024-justice-chawatama/: quality-gate-no-text
- https://judiciaryzambia.com/2020-hp-0248-edward-chanda-sosala-vs-kingsland-city-investment-limited-1-other-feb-2024-justice-chinyanwa-zulu/: quality-gate-no-text
- https://judiciaryzambia.com/2020-hp-0537-bearven-mengo-vs-anderson-situmbeko-other-feb-2024-justice-chibbabbuka/: quality-gate-no-text
- https://judiciaryzambia.com/2020-hpf-378-administrator-general-vs-jennifer-tembo-njobvu-mar-2024-justice-chinyanwa-zulu/: quality-gate-no-text
- https://judiciaryzambia.com/2020-hpf-d179-nchimunya-nicholas-nakalonga-vs-osiya-mupatayi-may-2024-justice-bah-matandala/: pdf-fetch-fail:UnicodeEncodeError
- https://judiciaryzambia.com/2021-hp-0649-kaulmas-investments-ltd-vs-the-commissioner-of-lands-other-feb-2024-justice-chibbabbuka/: quality-gate-no-text
- https://judiciaryzambia.com/2018-hp-1780-mwala-martin-mukwaibe-3-other-vs-zesco-limited-1-other-aug-2025-justice-bah-matandala/: quality-gate-no-text

