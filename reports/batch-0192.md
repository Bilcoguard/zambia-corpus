# Batch 0192 — Phase 4 sis_data_protection

- Started: 2026-04-24T18:07:13Z
- Completed: 2026-04-24T18:08:15Z
- Phase: phase_4_bulk
- Sub-phase: sis_data_protection (priority_order item 6)
- Records written: 5/5
- Fetches used: 10 (5 AKN HTML + 5 PDF)

## Records

- `si-zm-2021-021-cyber-security-and-cyber-crimes-act-commencement-order-2021` — Cyber Security and Cyber Crimes Act (Commencement) Order, 2021 (2 sections; sha256 d9bad08068591b94…; 8,831 bytes)
- `si-zm-2021-022-data-protection-act-commencement-order-2021` — Data Protection Act (Commencement) Order, 2021 (2 sections; sha256 b4389aa8f70ca09a…; 8,672 bytes)
- `si-zm-2021-023-electronic-communications-and-transactions-commencement-order-2021` — Electronic Communications and Transactions (Commencement) Order, 2021 (2 sections; sha256 506f7e09232a39cf…; 9,182 bytes)
- `si-zm-2016-031-postal-and-courier-services-general-regulations-2015` — Postal and Courier Services (General) Regulations, 2015 (107 sections; sha256 cdbb92fa3b6c0010…; 200,988 bytes)
- `si-zm-2003-022-postal-services-courier-service-licence-regulations-2003` — Postal Services (Courier Service) (Licence) Regulations, 2003 (24 sections; sha256 7f4c984d82787e53…; 1,555,475 bytes)

## Integrity

- CHECK1 unique IDs within batch: PASS
- CHECK2 no HEAD collision: PASS
- CHECK3 source_hash matches on-disk raw (5/5 sha256 verified): PASS
- CHECK4 no unresolved amended_by/repealed_by cross-refs: PASS
- CHECK5 required fields present: PASS

## Sub-phase notes

- Continues sis_data_protection rotation from batch 0191 (priority_order item 6).
- Three 2021 commencement orders for the Cyber/Data/ECT package — short SIs with 2 parsed sections each (commencement text). These are the canonical in-force trigger instruments for the 2021 digital-economy statutes.
- Two postal/courier SIs (2016/31 and 2003/22) expand the electronic-communications corridor: courier-services licensing is often cited alongside ECT and cyber-crimes legal analysis.
- Cumulative sis_data_protection records after this batch: 15 (10 prior + 5 this tick).

## Gaps

- None.

## Next tick plan

- Rotate to sis_mining (priority_order item 7) once sis_data_protection crosses ~18-20 records OR yield thins. Alternative: continue sis_data_protection with Data Protection Act sub-regs (transfer, processing), Cyber Crimes Act transitional provisions, ECT Act schedules.
- Infrastructure follow-up (non-blocking): rclone not available in sandbox — B2 sync deferred to host (`rclone sync raw/ b2raw:kwlp-corpus-raw/ --fast-list --transfers 4`). corpus.sqlite stale rollback-journal still blocks in-sandbox FTS rebuild.
