# Repair Batch b0701 — Summary

**Date:** 2026-05-18
**Worker:** repair-corpus
**Parser:** repair-0.6.101
**Elapsed:** 24.4 s (well under 20-min budget)

## Targets identified (live SQL)

- Condition A (corrupted digit-line bodies): 0
- Condition B (no-body acts/sis): 49
- Condition C (stub acts/sis < 200 chars): 0
- **Dedup targets:** 49
- **Picked (MAX_BATCH=8):** 8

## Outcome

- Repaired: **8**
- Failed: **0**
- Remaining (Condition B for next tick): **41**

## Repaired IDs

| ID | body len |
|---|---|
| si-zm-2022-016-local-authorities-superannuation-fund-pension-management-rules-2022 | 44,742 |
| si-zm-2022-017-customs-and-excise-electronic-machinery-and-equipment-suspension-amendment-regulations-2022 | 1,654 |
| si-zm-2022-018-electoral-process-general-election-election-date-and-time-of-poll-order-2022 | 1,891 |
| si-zm-2022-020-public-holidays-declaration-notice-2022 | 897 |
| si-zm-2022-021-electoral-process-local-government-by-elections-election-date-and-time-of-poll-order-2022 | 1,975 |
| si-zm-2022-025-tourism-and-hospitality-registration-of-hotel-managers-temporary-disapplication-of-registration-fee-regulations-2022 | 1,566 |
| si-zm-2022-026-tourism-and-hospitality-licensing-temporary-disapplication-of-renewal-and-retention-fees-regulations-2022 | 1,602 |
| si-zm-2022-027-citizenship-of-zambia-amendment-regulations-2022 | 1,574 |

All 8 sources: ZambiaLII AKN-SI HTML pages → `/akn/.../source.pdf` → pdfplumber extraction → quality gate passed (length > 200, digit-ratio ok, legal-text markers present).

## Integrity

- records: 1954
- records_fts: 1954
- match: **true**
- PRAGMA quick_check: **ok**

## B2 sync

Deferred to host — rclone not available in sandbox.

## Notes

- All 8 records fetched cleanly (HTTP 200) — zambialii.org availability remains stable since the b0697 recovery.
- One body (si-zm-2022-020 public-holidays-declaration-notice) came in at 897 chars — short but valid; quality gate passed (a brief declaration notice).
- The 44,742-char si-zm-2022-016 (Local Authorities Superannuation Fund Pension Management Rules) is by far the largest body in this batch — full rule set with schedules.
- DB record count is 1954 (records and records_fts both), confirming b0699-jiw's 8 inserted ZMCC 2024 records (02,04,05,06,07,08,10,13) remain in the live DB; their working-tree json files / judges_registry.yaml diff / batch-0699-jiw.md may still be orphan-pending recovery on the next jiw tick per b0700-phase8 ORPHAN_NOTE — that recovery is out of repair-worker scope and unaffected here (this repair tick mutated only the 8 SI rows above).
- No corrupted or stub bodies in the database this tick — Conditions A and C both empty.
