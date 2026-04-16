# Batch 0103 Report

- **Date**: 2026-04-16T17:30:00Z
- **Phase**: 4 (Bulk Ingestion)
- **Records added**: 8
- **Total sections**: 178
- **Fetches this batch**: 16 (8 detail pages + 8 PDFs)
- **Source**: ZambiaLII (zambialii.org)
- **Integrity checks**: ALL PASS

## Records

- **Air Services (Aerial Application Permit) Regulations, 1985** (SI 45 of 1985): 4 sections, PDF — `act-zm-1985-045-air-services-aerial-application-permit-regulations-1985`
- **Animal Health (Livestock Cleansing) Order, 2014** (SI 16 of 2014): 2 sections, PDF — `act-zm-2014-016-animal-health-livestock-cleansing-order-2014`
- **Animal Health (Control and Prevention of Animal Disease) Order, 2014** (SI 24 of 2014): 2 sections, PDF — `act-zm-2014-024-animal-health-control-and-prevention-of-animal-disease-order-2014`
- **Animal Health (Veterinary Services Fees) Regulations, 2018** (SI 22 of 2018): 67 sections, PDF — `act-zm-2018-022-animal-health-veterinary-services-fees-regulations-2018`
- **Animal Health (Notifiable Diseases) Regulations, 2019** (SI 81 of 2019): 53 sections, PDF — `act-zm-2019-081-animal-health-notifiable-diseases-regulations-2019`
- **Animal Health (Designated Border Inspection Posts) Regulations, 2020** (SI 87 of 2020): 2 sections, PDF — `act-zm-2020-087-animal-health-designated-border-inspection-posts-regulations-2020`
- **Animal Health (Bee Keeping) Regulations, 2020** (SI 94 of 2020): 39 sections, PDF — `act-zm-2020-094-animal-health-bee-keeping-regulations-2020`
- **Animal Health (Destruction of Pigs) (Compensation) Order, 2021** (SI 25 of 2021): 9 sections, PDF — `act-zm-2021-025-animal-health-destruction-of-pigs-compensation-order-2021`

## Notes
- Parser version: 0.4.0
- All records are Statutory Instruments under the Animal Health Act 2010 (plus one Air Services SI)
- ZambiaLII AKN URL pattern confirmed: /akn/zm/act/si/{year}/{num}/eng@{date}
- Discovery also identified 8 more SIs from page 1 and ~45 items on page 2 (Appropriation Acts 2000-2021, plus substantive SIs) — queued for next batch
- Pre-existing corpus duplicate issue identified: 25 records exist in both top-level records/acts/ and year subdirectories from earlier batches; git-rm staged for dedup commit
- SQLite rebuild deferred (sandbox root fs at 100%)
- B2 sync deferred (rclone not available in sandbox)
