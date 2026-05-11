# JIW Batch 0590 — Court of Appeal sweep (judiciaryzambia.com page 4)

**Timestamp:** 2026-05-11T10:18:00Z
**Worker:** judgment-ingestion-worker
**Sweep:** judiciary-coa-sweep page 4 (continuation of b0584/b0587)

## Summary

- **+1 record written** to corpus.sqlite (records=1888→1889, records_fts=1888→1889, judgments_meta=198→199).
- **7 records parsed successfully but DEFERRED** to next-tick insertion due to pre-existing FTS5 page-tree corruption (b0587 observation). All 7 have raw PDFs+HTML on disk and have been logged in `gaps.md` under reason code `deferred_fts5_corruption_pending_repair_worker_rebuild`.
- **0 deduplicates** — page 4 is all new content.
- **0 confirmed-404 stubs.**
- **fetches=18** (1 listing + 8 post HTML + 8 PDFs + 1 PDF refetch for truncation).
- **cumulative_today=34/500** (16 from b0584, 18 from b0590).

## Inserted record

| ID | Case | Citation | Outcome | Judges |
|---|---|---|---|---|
| `judgment-zm-2026-coa-382-musonda-chizinga-v-capstone-management-company-limited` | Musonda Chizinga v Capstone Management Company Limited (APP/382/2023) | [2026] ZMCA | dismissed | Chashi JJA, Ngulube JJA, Banda-Bobo JJA |

## Parsed but deferred (records_fts insert blocked)

| ID (would-be) | Case | Outcome | Judges |
|---|---|---|---|
| judgment-zm-2026-coa-237-the-examination-council-of-zambia-v-christopher-mkandawire | The Examination Council of Zambia v Christopher Mkandawire (APP/237/2023) | set-aside | Chashi, Ngulube, Banda-Bobo |
| judgment-zm-2026-coa-099-geoffrey-muyonga-...-v-ahmed-abdulkadir-... | Geoffrey Muyonga Sitwala Kaliki & Vincent Lubinda v Ahmed Abdulkadir Barakadle Mohammed (APPLN/099/2025) | struck-out | Chashi, Ngulube, Banda-Bobo |
| judgment-zm-2026-coa-279-kangwa-musenga-2-others-v-victor-muyumba-4-others | Kangwa Musenga & 2 Others v Victor Muyumba & 4 Others (APP/279/2023) | dismissed | Chashi, Makungu, Banda-Bobo |
| judgment-zm-2026-coa-231-lisboa-casino-limited-v-director-of-public-prosecutions | Lisboa Casino Limited v Director of Public Prosecutions (APP/231/2023) | dismissed | Kondolo SC, Makungu, Chembe |
| judgment-zm-2026-coa-317-the-university-of-zambia-v-ossie-mangani-zulu | The University of Zambia v Ossie Mangani Zulu (APP/317/2024) | dismissed | Kondolo SC, Makungu, Chembe |
| judgment-zm-2026-coa-568-chieftainess-lesa-v-mponwe-farms-limited-others | Chieftainess Lesa v Mponwe Farms Limited & Others (CAZ/08/568/2025) | refused | Banda-Bobo (single-judge chambers ruling) |
| judgment-zm-2026-coa-172-wesley-sibanda-...-v-point-present-investment-limited | Wesley Sibanda & Feediness Sakala Sibanda v Point Present Investment Limited (APP/172/2024) | dismissed | Kondolo SC, Majula, Muzenga |

## Parser v0.3.7-inline improvements (this tick)

Iterated on v0.3.6 anchor pack. Improvements applied:
- **Outcome pattern bag enlarged** to handle:
  - `appeal ... is consequently dismissed` (Wesley Sibanda)
  - `is accordingly set aside` / `judgment ... is accordingly set aside` (Examination Council)
  - `motions ... be struck out` / `struck off the active cause list` (Geoffrey Muyonga)
  - `appeal lacks merit and is ... dismissed` (Musonda Chizinga, Kangwa Musenga)
  - `ground X of the appeal partially succeeds` / `all the other grounds of appeal fail` (Lisboa Casino)
- **URL-preferred case_name** — parse from slug between case_id and date, avoid first-match-in-body false positives from cited cases (e.g. Kuntawala v Chirundu, American Cynamid v Ethicon).
- **URL-preferred judges** — `coram-X-Y-Z-jja` slug parsing; codifies the trailing-role-applies-to-all rule (v0.3.4) and embedded-SC handling (`kondolo-sc-makungu-chembe-jja` → Kondolo SC + Makungu JJA + Chembe JJA).
- **Reversed-surname order** — handle `bobo-banda` slug ordering by reversing to canonical `banda-bobo` → Banda-Bobo JJA.
- **Noise-word filter** for judge tokens — `ruling`, `justice`, `judgment`, `order`, `decision` dropped before lookup.
- **Bug rescue**: refetched truncated PDF for Wesley Sibanda (post HTML link still valid; original 1.44 MB truncated → re-fetched 2.28 MB; sha changed; manifest updated before parse).

## Pre-existing blocker (carried forward from b0587)

`PRAGMA integrity_check` reports FTS5 page-tree corruption (pages 14599, 28316-28340). New `INSERT INTO records_fts` fails for 7 of 8 records this tick with `database disk image is malformed`. The 1 record that succeeded inserted before the corrupted FTS pages were touched. CHECK8 (records=fts) still holds because failed FTS inserts triggered a rollback of the corresponding `records` row.

**Action required:** repair-worker tick to drop+recreate `records_fts` and reindex from `records.body`/`records.title`. Until then JIW yield is severely degraded — ~1 of N inserts per tick.

## Sweep position (for next tick)

- `judiciary-coa-sweep: page 5` (page 4 fully processed; 8 CoA-pattern candidates: 1 written, 7 v0.3.7-parsed-but-deferred-fts5).
- Pages 1-3 already done; the listing page 4 has 8 articles processed; 2 further posts on page 4 (`appeal-108-pilatus`, `app-38-mweene-mwiinga`) deferred to b0591 as overflow due to MAX_BATCH_SIZE=8.

## CHECK results (inserted record)

| Check | Result |
|---|---|
| CHECK1 (judges non-empty) | PASS (3 judges) |
| CHECK2 (issue_tags non-empty) | PASS (6 tags) |
| CHECK3 (outcome enum) | PASS (`dismissed`) |
| CHECK4 (judges resolve in registry) | PASS |
| CHECK5 (no duplicate IDs) | PASS |
| CHECK6 (raw_sha256 on-disk match) | PASS (`d89a0bea7e19...`) |
| CHECK7 (no dup case_name+court+date) | PASS |
| CHECK8 (records=fts count) | PASS (1889=1889) |

## Judges registry

- Added 1 canonical: `Kondolo SC` (court: Court of Appeal, title: JJA SC). Pre-emptive for next-tick reparse of deferred Lisboa Casino + UNZA records.
- Inserted record uses already-registered judges (Chashi JJA, Ngulube JJA, Banda-Bobo JJA).

## Notes

- Execution mode: inline runner, no derivative script committed (sandbox session safety constraint).
- User-Agent: `KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)`.
- Rate limit honoured: ~2s between post page fetches.
- Pre-tick backup: `corpus.sqlite.bak.b0590-pre-20260511T101817Z` (116,375,552 bytes).
- B2 sync deferred to host (rclone not in sandbox).
