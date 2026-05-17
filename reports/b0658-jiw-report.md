# JIW batch b0658 report

- Tick: **b0658-jiw**
- UTC: 2026-05-15T09:27:00Z → 2026-05-15T09:30:12Z
- Wall-clock used: ~192 s (well within 1200 s budget)
- Fetches consumed: 3 / 500 daily budget (8 cumulative today across all workers)
- Records before: 1922 (records_fts=1922, parity OK)
- Records after:  **1925** (records_fts=1925, parity OK, quick_check ok)
- Net delta: **+3 judgments**
- Skipped: 0
- Failures: 0

## Priority elected

priority-(c) ZMSC 2024 gap-fill — per b0654-jiw recommendation. Cached HTML for 6 outstanding ZMSC 2024 IDs (#18, #22, #26, #28, #29, #31) was already on disk from b0622/b0626. Fetched 3 corresponding `source.pdf` files; parsed via `pdfplumber`; metadata hand-curated to parser_version `0.3.2-jiw-b0658`.

## Records inserted

1. **`judgment-zm-2024-zmsc-18-the-people-v-evelyn-mwansa-and-ors`** — Supreme Court of Zambia, [2024] ZMSC 18, decided 2024-05-16.
   - Panel: Muyovwe JJS, Hamaundu JJS (delivered), Chinyama JJS.
   - Three consolidated appeals (Appeal Nos. 12, 13, 14 of 2020) by the State against inadequate murder sentence.
   - Outcome: **allowed** — six-year sentence quashed; mandatory death sentence substituted as required by law at time of offence; finding of extenuating circumstances reversed as having no basis.
2. **`judgment-zm-2024-zmsc-22-george-banda-v-the-people`** — Supreme Court of Zambia, [2024] ZMSC 22, decided 2024-03-06.
   - Panel: Hamaundu JJS (delivered), Mutuna JJS, Chisanga JJS.
   - Criminal appeal from a court martial conviction (Appeal No. 51/2022).
   - Outcome: **dismissed** — court martial's finding of guilt upheld; no miscarriage of justice in handling of convening order or witness-summons rights.
3. **`judgment-zm-2024-zmsc-31-konkola-copper-mines-plc-in-liquidation-v-attorney-general-and-ors`** — Supreme Court of Zambia, [2024] ZMSC 31, decided 2024-10-23.
   - Single judge in chambers: Lady Justice R.M.C. Kaoma JS.
   - Application for leave to appeal in mining-cadastre / consent-transfer dispute (SCZ/7/20/2024).
   - Outcome: **granted** — Court of Appeal Act s.13(3)(a)(c)(d) threshold met (reasonable prospects + compelling reason — non-communication of Mining Cadastre's consent and right-of-appeal); leave granted; costs to abide.

## Mining-law note (high-relevance flag for Peter)

ZMSC 31 (KCM v AG) is directly relevant to the firm's mining-cadastre work — it interprets:
- **Court of Appeal Act s.13(3)(a)(c)(d)** — leave-to-appeal threshold criteria.
- **Mines and Minerals Development Act, s.97(1)** — procedure where the Director of Mining Cadastre issues a decision affecting affected parties (here, granting consent to a third party without communicating that decision or the right of appeal to the holder).

The judge held that an applicant cannot be faulted for not invoking the s.97(1) appeal procedure if the Director never communicates the underlying decision — a holding with direct relevance to cadastre-related disputes the firm advises on.

## Integrity checks

- CHECK1 every record has ≥1 judge: **PASS**
- CHECK2 `issue_tags` non-empty: **PASS**
- CHECK3 outcome ∈ enum: **PASS** (allowed, dismissed, granted)
- CHECK4 all judge names resolve in `judges_registry.yaml`: **PASS** (no new judges added)
- CHECK5 no duplicate IDs: **PASS**
- CHECK6 raw_sha256 matches on-disk PDF: **PASS** (all 3)
- CHECK7 no duplicate (case_name + court + date_decided): **PASS**
- CHECK8 `records` = `records_fts` = 1925: **PASS**

## Workarounds

- **tmpfs staging:** virtiofs FUSE journal-unlink restriction still in effect; first direct-insert attempt failed with `disk I/O error` on COMMIT. Re-ran via `/tmp/corpus_work_b0658.sqlite` (own UID, isolated filename), then rewrote-in-place into `corpus.sqlite` per `scripts/repair_b0657.py` pattern. Stale journal renamed to `.b0658-jiw-poststaging.bak`. Tmp working file removed at end of tick.

## Sweep state

ZambiaLII ZMSC 2024 gap-fill is now 29/33 (88 %). Remaining gaps: #4 (un-cached), #26 (HTML cached, ~1.66 MB PDF), #28 (5.92 MB), #29 (9.03 MB). Other sweep cursors unchanged from b0654-jiw.

## Cumulative judgment-corpus snapshot

- Total records: 1925 (judgments + acts + SIs combined)
  - judgment: 241 (+3 this tick)
  - act: 1145
  - si: 539
- Judgment JSON files on disk under `records/judgments/`: 235 (DB judgment-row count is 241, suggesting 6 historical rows have no on-disk JSON — flagged for future repair-worker reconciliation; out of scope this tick).
- Progress toward 800-judgment target: **241 / 800 (≈30 %)**.

## Next tick

Recommend continuing ZMSC 2024 gap-fill (#26 and possibly #4) at b0659-jiw, then surveying ZMCC 2025 gaps. CoA sweep page-9+ remains deferred until scanned-PDF repair backlog drains.
