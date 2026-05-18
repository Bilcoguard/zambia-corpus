# Batch b0629-jiw — TICK ABORTED

- **Worker:** judgment-ingestion-worker
- **Start:** 2026-05-13T07:08Z (UTC)
- **End:** 2026-05-13T07:08Z
- **Wall-clock:** ~2 minutes
- **Records inserted:** 0
- **Records deferred:** 0 (state unchanged from b0628-repair handoff)
- **Fetches:** 0. Cumulative today: **21 / 500**.
- **B2 sync:** deferred to host (rclone not in sandbox).
- **Git push:** none (no corpus mutation this tick).

## Verdict

Aborted before any wire fetch or database write. Per `b0627-jiw` handoff rule #1, the disk-full precondition still holds:

```
df /
/dev/nvme0n1p1  9.6G  9.5G   15M 100% /
```

This is the **third consecutive JIW tick** with the same state (`b0626-jiw` → `b0627-jiw` → `b0629-jiw`). Zero bytes have been freed on the sandbox `/` partition in the ~3 hours since `b0626-jiw` first observed the condition; no host-side `/tmp` rotation has occurred between the three sessions.

## Host-side state at tick start

| Property | Value | Notes |
|----------|-------|-------|
| sandbox `/` | 9.5G / 9.6G (15 MB free) | 100% — blocking PDF parse and multi-row FTS5 commits |
| corpus mount | 217G / 229G (12 GB free) | 95% — fine for cache/raw writes |
| `corpus.sqlite` mtime | 2026-05-13T06:13:14Z (~54 min pre-tick) | b0628-repair final commit, host worker now quiescent |
| `corpus.sqlite-journal` | 57968 bytes, 2026-05-13T05:17:38Z mtime | unchanged from b0627-jiw; benign per read-path integrity check |
| read-path integrity | `records=1928` `records_fts=1928` `quick_check=ok` | CHECK1–CHECK8 pass via `file:…?mode=ro&immutable=1` URI open |
| owned-by-current-UID `/tmp` blockers | zero | all large `/tmp/*` files owned by prior session UIDs |

UID audit confirms the chronic condition: `/tmp/test-corpus.sqlite` (116 MB, owner `magical-cool-brown`) and seven similar 112 MB SQLite copies owned by prior sessions still cannot be removed (`Operation not permitted`).

## Why this tick aborted rather than attempting `b0628-repair`'s scratch-copy pattern

`b0628-repair` (commit `b309694`) successfully wrote +4.6 MB of body-text repairs at the same disk-full state using the scratch-copy-on-mount + `shutil.copy2` swap-back pattern. The pattern works for repair workers because they reparse already-cached raw bytes in-memory and emit a single-pass UPDATE against the live DB.

The JIW pipeline cannot use this pattern unmodified because:

1. **PDF parsing.** `pdfplumber.open()` on a multi-MB PDF spills working state into `mkstemp(dir=tempfile.gettempdir())`. Per `b0626-jiw` finding, re-routing `TMPDIR` to the corpus mount did **not** prevent the spill from landing in `/`. With 15 MB free, this fails on the first medium-sized PDF.
2. **Multi-row FTS5 transaction.** The JIW insert is a single atomic commit across `records` + `judgments_meta` + `records_fts`. `b0626-jiw` observed this commit reliably fails with `sqlite3.OperationalError: disk I/O error` under the disk-full state, even when single-row writes to `corpus_meta` succeed in between contention windows.

Operator note (m) in `gaps.md` captures the refactor that could unblock JIW under disk-full: wire-fetch to corpus mount, parse with `pdfplumber.open(BytesIO(...))` exclusively (force in-memory), and apply the scratch-copy-on-mount commit pattern. This is outside this tick's scope.

## Cached state — unchanged

| File | Size | Status |
|------|-----:|--------|
| `raw/zambialii/zmsc/2024/zmsc-2024-{18,22,26,28,29,31}-eng.html` | 41–47 KB each | still cached, zero re-fetch cost for next commit-capable JIW |
| `raw/zambialii/zmsc/2024/zmsc-2024-11-source.pdf` | 18 MB | publisher-duplicate of ZMSC 9/2024; will be dedup-skipped |
| `raw/zambialii/zmsc/2024/_orphan_b0626/judgment-zm-2024-zmsc-11-…json` | – | orphan relocated by b0627-jiw, audit-only |

## Sweep position — unchanged

- `judiciary-coa-sweep`: still stalled behind the disk-full state + scanned-PDF cliff (b0617/b0618).
- ZMSC 2024 gap fill: 6 cached HTML pages awaiting PDF fetch + ingest.
- ZMSC 2024 publisher-duplicate sanity checks (zmsc-26↔25, zmsc-28↔29): outstanding.

## Logs appended (no commit)

- `worker.log`: 11 START/observation/STOP lines.
- `costs.log`: 2 lines (fetches=0 abort summary + B2 sync verdict).
- `gaps.md`: one new ## section documenting the 3rd-consecutive abort and operator action items.
- `reports/batch-b0629-jiw.md`: this file.

Per `b0627-jiw` handoff rule #1: no `git add`, no `git commit`, no push. Host-side sweep will pick up the log appends.

## Operator action required

(k) Sandbox `/` 100 % full is now **chronic across 3 JIW ticks with zero host-side intervention**. Severity: HIGH-and-CHRONIC. Without `/tmp` rotation between sessions, JIW cannot advance.

(m) Optional refactor of JIW pipeline to avoid `/tmp` and use scratch-copy-on-mount would unblock the worker under the same disk-full state that repair workers already tolerate.

## Next tick (b0630-jiw, t+60min)

1. `df /` — if still > 99 % full, abort again with minimal log entry.
2. If freed: `PRAGMA journal_mode=TRUNCATE` preflight, then drain the 6 cached ZMSC 2024 HTML pages (PDF fetch + parse + ingest), with publisher-duplicate sanity checks against the existing 2024 ZMSC records.
3. After ZMSC 2024 gap drained: re-attempt priority-b judiciary CoA page 1 (still zero coverage; scanned-PDF cliff still expected at the OCR layer).
4. If 5 consecutive JIW ticks have aborted with this state (currently at 3), surface to operator as a chronic-blocker handoff. Do NOT flip `complete: true`.
