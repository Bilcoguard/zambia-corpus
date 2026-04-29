# Batch 0344 — Phase 5 ZMCC re-parse with tightened disposition policy

- **Tick start:** 2026-04-29T14:02Z
- **Phase:** phase_5_judgments (lowest approved + incomplete)
- **Source:** ZambiaLII Constitutional Court of Zambia — raw HTML+PDF pairs
  already on disk from b0343 (no re-fetch this tick).
- **Bounded unit:** re-parse the 8 candidates persisted at b0343 under a
  tightened parser (`parser_version: 0.3.0`, `scripts/batch_0344_parse.py`).
- **Result:** 3 records written, 5 deferred.

## Parser policy change (b0343 follow-up)

Per b0343 worker.log entry, the previous policy allowed disposition
inference from `pdf-tail` and `pdf-full` regex sweeps, which produced
unsafe matches against words appearing inside citations to OTHER cases or
mid-paragraph analysis fragments (b0343 examples: "d by Judge Mulonda.",
"another v Attorney Generall4l.", "the Godfrey Miyanda v Attorney General
case supra.", "proved or demonstrated to the required standard.").

`scripts/batch_0344_parse.py` (parser_version 0.3.0) tightens the policy:

- **PRIMARY** (preferred): match disposition phrases in the ZambiaLII
  summary `<dd>` block. Patterns extended to recognise common ConCourt
  summary phrasing — `Court dismissed …`, `Court (allowed|granted|upheld|
  overturned) …`, `Application for <X> dismissed`, `joinder granted` /
  `Court granted joinder`.
- **SECONDARY** (only when summary fails): match in the PDF body, but
  *only* within an 800-character window starting at an explicit ORDER
  ANCHOR. Anchors are limited to: "It is ordered", "It is hereby ordered",
  "It is accordingly ordered", "We accordingly order", "We hereby order",
  "We make the following order", "We therefore order", "We order as
  follows", "The order(s) of the Court", "The following order(s)".
- `pdf-tail` and `pdf-full` sweeps are **removed outright**.
- Soft anchors that previously matched ("for the foregoing", "in
  conclusion", "we conclude", "accordingly,") are **rejected outright**.
- `outcome_detail` safety guards: must start at a word boundary (rejects
  mid-word fragments), must contain ≥4-letter alphabetic content
  totalling ≥12 chars, must not contain cross-reference markers like
  `case supra`, ` supra`, `another v `, `and another v `, `Generall4l`,
  `Mulonda`.

## Records written (3)

| ID | Citation | Date | Outcome | Source | Judges |
| --- | --- | --- | --- | --- | --- |
| `judgment-zm-2025-zmcc-27-munir-zuu-and-anor-v-attorney-general-and-ors` | [2025] ZMCC 27 | 2025-12-05 | dismissed | summary: "Court dismissed application to disqualify petitioners' counsel for alleged conflict absent evidence of confidential information or real prejudice" | Mulongoti (single judge) |
| `judgment-zm-2025-zmcc-29-law-association-of-zambia-and-ors-v-attorney-gener` | [2025] ZMCC 29 | 2025-12-08 | allowed | summary: "Court granted joinder to two intended interested parties, holding standing rules broad and persons may appear in person" | Kawimbe (single judge) |
| `judgment-zm-2025-zmcc-31-munir-zulu-and-anor-v-attorney-general-and-ors` | [2025] ZMCC 31 | 2025-12-10 | dismissed | summary: "Application for contempt dismissed for being procedurally misconceived for failing to invoke a proper rule or authority" | Mulongoti (single judge) |

All three are single-judge ConCourt sittings (procedural / interlocutory
matters), which is permitted under the schema (`judges` array
`minItems: 1`).

The three judges all resolve in `judges_registry.yaml`. The b0344 parser
adds two new aliases to existing canonical entries:

- `HON. LADY JUSTICE MARIA MAPANI - KAWIMBE` → canonical `Kawimbe`.
- `Lady Justice J.Z Mulongoti` → canonical `Mulongoti` (with new short
  title `J` recorded alongside the existing `JCC`).

No new canonicals were created.

## Deferred (5) — recorded in `gaps.md`

All five summaries describe holdings, issues, or ratio decidendi without
an enum-mappable disposition phrase, AND no eligible PDF order anchor
match was found within the strict 800-character window.

| ID candidate | Reason |
| --- | --- |
| [2026] ZMCC 1 — Tresford Chali v Judicial Complaints Commission | Summary: "A challenge to the JCC's report and removals must proceed by judicial review in the High Court, not by original petition here." — describes the holding, no disposition phrase. |
| [2025] ZMCC 33 — Miles Bwalya Sampa v Attorney General | Summary: "Issuance of newly created shares (subscription) did not amount to disposal of State equity triggering Article 210 parliamentary approval." — ratio without disposition. |
| [2025] ZMCC 32 — Law Association of Zambia v Attorney General | Summary: "Renewal before the full Court is the proper route to challenge a single judge's interlocutory ruling; late conservatory relief denied." — describes the procedural holding. |
| [2025] ZMCC 30 — Legal Resources Foundation v Attorney General | Summary is a question of law: "Whether the applicant proved a prima facie constitutional breach and irreparable harm to justify staying judicial appointments." |
| [2025] ZMCC 28 — Brian Mundubile v Hakainde Hichilema | Summary describes the holding ("constitutional challenges implicating the President must proceed against the Attorney-General") but no disposition phrase. |

The raw HTML+PDF for all five remain on disk at
`raw/zambialii/judgments/zmcc/{2025,2026}/`. A future tick can either
hand-anchor the PDF order paragraphs or extend the safe summary patterns.

## Integrity checks (`scripts/integrity_check_b0344.py`)

```
PASS — new-record integrity check (3 records).
PASS — no duplicate IDs in records/judgments/.
```

Per-record hash audit:
- All 3 `source_hash` values match `sha256:` of the on-disk raw HTML.
- All 3 `raw_sha256` values match `sha256` of the on-disk raw PDF.
- All 3 records satisfy schema (required fields, court enum, outcome
  enum, role enum, judges resolved, ≥1 issue_tag, regex patterns).

## Budget impact

- Fresh fetches this tick: **0** (re-parsed already-persisted raw bytes).
- Cumulative today: **78/2000 fetches (~3.9%)** — unchanged from b0343
  end-state.
- Token budget: unchanged (parser-only re-run).

## Phase 5 progress

- **Records to date:** 12 / 100–160 target (was 9 at b0343 end; +3 this tick).
- **ZMCC 2026:** 8 of 10 records ingested (2026/{02..10}); 2026/01 still
  deferred (summary describes holding only).
- **ZMCC 2025:** 1 record ingested (2025/{27}); deferred 5 (2025/{28, 30,
  32, 33}, 2026/01); 26 candidates 2025/{1..26} not yet attempted.
- **ZMCC 2025/29 and 2025/31** ingested this tick.

## B2 sync

Deferred to host. `rclone` not available in the sandbox (logged in
`worker.log` as in prior ticks).

## Next tick

- Begin sweep of ZMCC 2025/{1..26} — most-recent-first — using the
  tightened parser. Stage fetches in groups of ≤4 to avoid the
  long-running-fetcher kill seen at b0342.
- For the 5 deferred candidates with raw on disk: a future enhancement
  would hand-anchor the PDF order paragraphs (extract text near "ORDER",
  "It is ordered", numbered conclusion paragraphs) and add specific
  patterns. Not attempted this tick to keep within the 20-min budget.
