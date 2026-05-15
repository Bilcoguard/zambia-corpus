#!/usr/bin/env python3
"""
Repair worker tick b0657.

Targets up to MAX_BATCH_SIZE records with NULL/empty bodies (or corrupted/stub
bodies per v4 prompt).  Drains ZambiaLII SI cohort.  Quality-gated, crash-safe
per-record commit.
"""
from __future__ import annotations
import hashlib
import io
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/sessions/hopeful-modest-babbage/mnt/corpus")
WORK_DB = Path("/tmp/corpus_work.sqlite")  # operate on tmpfs copy to dodge virtiofs journal quirks
os.chdir(ROOT)

TICK = "b0657"
PARSER_VERSION = "repair-0.6.3"
MAX_BATCH_SIZE = 8
WALL_CLOCK_BUDGET_S = 60 * 18  # leave 2 min headroom inside 20-min limit
UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
CERT_PATH = ROOT / "scripts" / "certs" / "rapidssl_tls_rsa_ca_g1.pem"
CRAWL_DELAY = 5.0

WORKER_LOG = ROOT / "worker.log"
GAPS_LOG = ROOT / "gaps.md"
COSTS_LOG = ROOT / "costs.log"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg: str) -> None:
    line = f"[{now_iso()}] [repair-{TICK}] {msg}\n"
    sys.stdout.write(line)
    sys.stdout.flush()
    with WORKER_LOG.open("a", encoding="utf-8") as f:
        f.write(line)


def log_gap(rid: str, reason: str) -> None:
    with GAPS_LOG.open("a", encoding="utf-8") as f:
        f.write(f"- [{now_iso()}] repair-{TICK} {rid}: {reason}\n")


def log_cost(msg: str) -> None:
    with COSTS_LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{now_iso()}] repair-{TICK} {msg}\n")


def find_repair_targets(conn: sqlite3.Connection) -> list[tuple[str, str, str]]:
    """Run all three v4 conditions; return [(id, type, url), ...]."""
    cur = conn.cursor()
    targets: list[tuple[str, str, str]] = []
    seen: set[str] = set()

    # Condition A: corrupted (digit-ratio)
    cur.execute(
        "SELECT id, type, source_url, body FROM records "
        "WHERE body IS NOT NULL AND body != '' AND length(body) > 10"
    )
    for rid, rtype, url, body in cur.fetchall():
        lines = body.strip().split("\n")
        digit_lines = sum(1 for l in lines if l.strip().isdigit())
        if digit_lines > len(lines) * 0.5 and len(lines) > 10:
            if rid not in seen:
                targets.append((rid, rtype, url))
                seen.add(rid)

    # Condition B: no body (acts and SIs only, skip judgments)
    cur.execute(
        "SELECT id, type, source_url FROM records "
        "WHERE (body IS NULL OR body = '') AND type IN ('act','si') "
        "ORDER BY id"
    )
    for rid, rtype, url in cur.fetchall():
        if rid not in seen:
            targets.append((rid, rtype, url))
            seen.add(rid)

    # Condition C: stub body (act/si <200 chars)
    cur.execute(
        "SELECT id, type, source_url FROM records "
        "WHERE type IN ('act','si') AND body IS NOT NULL "
        "AND length(body) > 0 AND length(body) < 200"
    )
    for rid, rtype, url in cur.fetchall():
        if rid not in seen:
            targets.append((rid, rtype, url))
            seen.add(rid)

    return targets


def http_get(url: str, *, binary: bool = False, timeout: int = 60) -> bytes | str:
    """Fetch a URL using curl with our certificate bundle."""
    cmd = [
        "curl", "-sSL", "--fail",
        "--cacert", str(CERT_PATH),
        "-A", UA,
        "--max-time", str(timeout),
        url,
    ]
    res = subprocess.run(cmd, capture_output=True, timeout=timeout + 10)
    if res.returncode != 0:
        raise RuntimeError(f"curl failed ({res.returncode}): {res.stderr.decode('utf-8', 'replace')[:400]}")
    if binary:
        return res.stdout
    return res.stdout.decode("utf-8", "replace")


def extract_zambialii_pdf_url(html: str, page_url: str) -> str | None:
    """Find the source.pdf link on a ZambiaLII document page."""
    # Direct match for .pdf hrefs
    m = re.search(r'href="(/akn/[^"]+/source\.pdf)"', html)
    if m:
        return "https://zambialii.org" + m.group(1)
    m = re.search(r'href="(https?://[^"]*source\.pdf)"', html)
    if m:
        return m.group(1)
    # Look for any /akn/...pdf href
    m = re.search(r'href="(/akn/[^"]+\.pdf)"', html)
    if m:
        return "https://zambialii.org" + m.group(1)
    # Sometimes the URL is a laws.africa media link
    m = re.search(r'href="(https?://[^"]*laws\.africa[^"]+\.pdf)"', html)
    if m:
        return m.group(1)
    return None


def extract_pdf_text(pdf_bytes: bytes) -> str:
    import pdfplumber
    out_pages = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            try:
                txt = page.extract_text() or ""
            except Exception as e:
                txt = ""
            out_pages.append(txt)
    return "\n\n".join(out_pages).strip()


def normalise_text(text: str) -> str:
    # Split concatenated section numbers like "10.Foo" -> "10. Foo"
    text = re.sub(r"(\d+)\.([A-Z])", r"\1. \2", text)
    # Collapse trailing whitespace on lines
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text.strip()


def quality_gate(body: str) -> tuple[bool, str]:
    if len(body) < 200:
        return False, f"too short ({len(body)} chars)"
    lines = body.strip().split("\n")
    digit_lines = sum(1 for l in lines if l.strip().isdigit())
    if len(lines) > 10 and digit_lines > len(lines) * 0.5:
        return False, "digit-line-ratio fail (line-numbers-only)"
    # legal markers
    markers = ("Act", "Section", "section", "Regulation", "Order", "Statutory", "enacted",
               "Republic of Zambia", "GOVERNMENT", "Government", "Minister")
    if not any(m in body for m in markers):
        return False, "no legal markers found"
    return True, "ok"


def repair_record(conn: sqlite3.Connection, rid: str, rtype: str, url: str) -> tuple[bool, str]:
    """Returns (success, message)."""
    log(f"repair START {rid} <- {url}")
    t0 = time.time()

    try:
        host = url.split("/")[2].lower()
    except Exception:
        return False, f"bad url: {url}"

    pdf_bytes: bytes | None = None
    pdf_source: str = ""

    try:
        if url.lower().endswith(".pdf"):
            # Direct PDF
            pdf_bytes = http_get(url, binary=True)
            pdf_source = url
        elif "zambialii.org" in host or "laws.africa" in host:
            html = http_get(url)
            pdf_url = extract_zambialii_pdf_url(html, url)
            if not pdf_url:
                return False, "no source.pdf link on ZambiaLII page"
            time.sleep(2.0)
            pdf_bytes = http_get(pdf_url, binary=True)
            pdf_source = pdf_url
        elif "parliament.gov.zm" in host:
            if "/node/" in url:
                html = http_get(url)
                m = re.search(r'href="([^"]+\.[Pp][Dd][Ff][^"]*)"', html)
                if not m:
                    return False, "no PDF link on parliament /node page"
                pdf_link = m.group(1)
                if pdf_link.startswith("/"):
                    pdf_link = "https://www.parliament.gov.zm" + pdf_link
                time.sleep(2.0)
                pdf_bytes = http_get(pdf_link, binary=True)
                pdf_source = pdf_link
            else:
                pdf_bytes = http_get(url, binary=True)
                pdf_source = url
        else:
            return False, f"unsupported host: {host}"
    except Exception as e:
        return False, f"fetch error: {e}"

    if not pdf_bytes or len(pdf_bytes) < 100:
        return False, f"empty/short PDF ({len(pdf_bytes) if pdf_bytes else 0} bytes)"

    try:
        body = extract_pdf_text(pdf_bytes)
    except Exception as e:
        return False, f"pdfplumber error: {e}"

    if len(body) < 200:
        # No OCR available in this env; record gap
        return False, f"low-text extract ({len(body)} chars) and OCR unavailable"

    body = normalise_text(body)
    ok, reason = quality_gate(body)
    if not ok:
        return False, f"quality gate: {reason}"

    src_hash = hashlib.sha256(pdf_bytes).hexdigest()
    fetched_at = now_iso()

    # Per-record commit (crash-safe)
    cur = conn.cursor()
    cur.execute(
        "UPDATE records SET body=?, source_hash=?, fetched_at=?, parser_version=? WHERE id=?",
        (body, src_hash, fetched_at, PARSER_VERSION, rid),
    )
    # Rebuild FTS for this record.  FTS schema is content=records external
    # content (columns: id, title, body, citation, type) keyed by rowid.
    cur.execute(
        "DELETE FROM records_fts WHERE rowid = (SELECT rowid FROM records WHERE id = ?)",
        (rid,),
    )
    cur.execute(
        """INSERT INTO records_fts (rowid, id, title, body, citation, type)
           SELECT rowid, id, title, body, citation, type
           FROM records WHERE id = ?""",
        (rid,),
    )
    conn.commit()
    elapsed = time.time() - t0
    log(f"repair OK {rid} chars={len(body)} sha={src_hash[:8]} elapsed={elapsed:.1f}s")
    log_cost(f"{rid} bytes_pdf={len(pdf_bytes)} bytes_body={len(body)} elapsed={elapsed:.1f}s")
    return True, "ok"


def main() -> int:
    start = time.time()
    log(f"tick start (max_batch={MAX_BATCH_SIZE}, budget={WALL_CLOCK_BUDGET_S}s)")

    # Stage the DB on tmpfs to bypass virtiofs journal-unlink quirks.
    import shutil
    db_src = ROOT / "corpus.sqlite"
    if WORK_DB.exists():
        WORK_DB.unlink()
    shutil.copy2(db_src, WORK_DB)
    log(f"staged db to {WORK_DB} ({WORK_DB.stat().st_size} bytes)")
    db = sqlite3.connect(str(WORK_DB), timeout=60)

    targets = find_repair_targets(db)
    log(f"discovery total_targets={len(targets)}")

    if not targets:
        log("All repair targets fixed — repair worker idle")
        db.close()
        return 0

    batch = targets[:MAX_BATCH_SIZE]
    log(f"batch_size={len(batch)} first={batch[0][0]} last={batch[-1][0]}")

    fixed = 0
    failed = 0
    failed_details: list[tuple[str, str]] = []
    succeeded: list[tuple[str, int]] = []

    for rid, rtype, url in batch:
        if time.time() - start > WALL_CLOCK_BUDGET_S:
            log("wall-clock budget reached — stopping")
            break
        try:
            ok, msg = repair_record(db, rid, rtype, url)
        except Exception as e:
            ok, msg = False, f"unhandled exception: {e}"
        if ok:
            fixed += 1
            # capture body len
            cur = db.cursor()
            cur.execute("SELECT length(body) FROM records WHERE id=?", (rid,))
            blen = cur.fetchone()[0]
            succeeded.append((rid, blen))
        else:
            failed += 1
            failed_details.append((rid, msg))
            log_gap(rid, msg)
            log(f"repair FAIL {rid}: {msg}")
        time.sleep(CRAWL_DELAY)

    # Integrity check
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM records")
    rcount = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM records_fts")
    fcount = cur.fetchone()[0]
    integrity_ok = rcount == fcount
    log(f"integrity records={rcount} records_fts={fcount}")

    qcheck = db.execute("PRAGMA quick_check").fetchone()[0]
    if qcheck != "ok":
        log(f"PRAGMA quick_check returned: {qcheck}")
    db.close()

    # Promote tmpfs DB back to virtiofs only if integrity OK AND at least one fix
    if integrity_ok and fixed > 0:
        import shutil
        target = ROOT / "corpus.sqlite"
        # In-place overwrite (virtiofs blocks unlink); use rewrite-in-place via open w+b
        with open(WORK_DB, "rb") as src, open(target, "r+b") as dst:
            dst.seek(0)
            while True:
                chunk = src.read(1 << 20)
                if not chunk:
                    break
                dst.write(chunk)
            dst.truncate()
            dst.flush()
            os.fsync(dst.fileno())
        log(f"promoted tmpfs db -> {target} ({target.stat().st_size} bytes)")
        # Clean stale journal that may have been left behind by host sqlite use
        stale = ROOT / "corpus.sqlite-journal"
        if stale.exists():
            try:
                stale.rename(ROOT / f"corpus.sqlite-journal.{TICK}-poststaging.bak")
                log("moved post-staging stale journal")
            except Exception as e:
                log(f"warn: stale journal rename failed: {e}")
    elif fixed == 0:
        log("no successful repairs; skipping db promotion")
    else:
        log("integrity mismatch; aborting db promotion (changes remain in tmpfs only)")

    elapsed = time.time() - start
    log(f"tick complete fixed={fixed} failed={failed} elapsed={elapsed:.1f}s")

    # Write batch report
    report_path = ROOT / "reports" / f"repair-batch-0657.md"
    lines = [
        f"# Repair batch 0657 — {fixed} record(s) fixed, {failed} failed",
        "",
        f"**Worker**: repair-corpus (scheduled-task, v4 prompt)",
        f"**Tick**: {TICK}",
        f"**Parser version**: {PARSER_VERSION}",
        f"**Wall-clock**: {elapsed:.1f}s (budget {WALL_CLOCK_BUDGET_S}s)",
        f"**Date**: {now_iso()}",
        "",
        "## Targets discovered",
        f"- Total records needing repair (live DB scan): **{len(targets)}**",
        f"- Selected this tick: **{len(batch)}** (MAX_BATCH_SIZE={MAX_BATCH_SIZE})",
        "",
        "## Records repaired",
        "",
        "| # | ID | Bytes |",
        "|---|---|------:|",
    ]
    for i, (rid, blen) in enumerate(succeeded, 1):
        lines.append(f"| {i} | {rid} | {blen:,} |")
    if failed_details:
        lines += [
            "",
            "## Failed (gapped for retry)",
            "",
            "| ID | Reason |",
            "|---|---|",
        ]
        for rid, reason in failed_details:
            lines.append(f"| {rid} | {reason} |")
    lines += [
        "",
        "## Integrity",
        f"- `records` count: **{rcount}**",
        f"- `records_fts` count: **{fcount}**",
        f"- Integrity OK: **{integrity_ok}**",
        f"- `PRAGMA quick_check`: **{qcheck}**",
        "",
        "## Pipeline",
        "",
        "Standard v4 pipeline: live-DB discovery (Conditions A/B/C) → fetch (curl + RapidSSL CA) → pdfplumber extract → section-number normalise → quality gate (length + digit-line ratio + legal markers) → per-record UPDATE + FTS rebuild + commit (crash-safe).",
        "",
        "Crawl delay 5 s between fetches.  Judgments with no body skipped (handled by judgment-ingestion worker).",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    log(f"report written: {report_path.name}")

    # Print summary to stdout
    print("\n=== TICK SUMMARY ===")
    print(f"discovered: {len(targets)}")
    print(f"batched:    {len(batch)}")
    print(f"fixed:      {fixed}")
    print(f"failed:     {failed}")
    print(f"integrity:  {'OK' if integrity_ok else 'MISMATCH'} ({rcount} vs {fcount})")
    print(f"elapsed:    {elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
