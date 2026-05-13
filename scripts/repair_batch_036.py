#!/usr/bin/env python3
"""Repair worker batch 036 — fixes up to 8 corrupted/empty/stub Act/SI bodies.

Follows SKILL.md repair worker spec (v4, 2026-05-13 tick).
Continuation of b035 (which finished the 2013 manifest run). b036 picks up
in manifest declaration order: 2013-016, 2013-019, 2014-001, 2014-002,
2016-008, 2016-009, 2017-008, 2021-026.

All eight targets verified as still needing repair via live-DB query before
selection (manifest_remaining=32 of 88 at start of tick).
"""
import os, sys, re, time, json, sqlite3, ssl, glob, shutil, tempfile, hashlib, subprocess
import urllib.request, urllib.error, urllib.parse
from datetime import datetime, timezone
from html.parser import HTMLParser

# ───────────────────────────── paths ────────────────────────────────────
WORKDIR  = "/sessions/happy-exciting-brahmagupta/mnt/corpus"
PDF_DIR  = os.path.join(WORKDIR, "_repair_b036_pdfs")
TMPROOT  = os.path.join(WORKDIR, "_repair_b036_tmpdb")
DB       = os.path.join(WORKDIR, "corpus.sqlite")
GAPS     = os.path.join(WORKDIR, "gaps.md")
LOG      = os.path.join(WORKDIR, "worker.log")
COSTS    = os.path.join(WORKDIR, "costs.log")
HEADERS  = {'User-Agent': 'KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)'}
CERT     = os.path.join(WORKDIR, "scripts/certs/rapidssl_tls_rsa_ca_g1.pem")

# Next 8 manifest records in declaration order.
MANIFEST = [
    ("act-zm-2013-016-the-customs-and-excise-amendment-2013",
     "https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Customs%20and%20Excise%20%28Amendment%29%20Act%202013.PDF"),
    ("act-zm-2013-019-the-appropriation-act-2013",
     "https://www.parliament.gov.zm/sites/default/files/documents/acts/Appropriation%20Act%202013.PDF"),
    ("act-zm-2014-001-the-legal-practitioner-amendment-act",
     "https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Legal%20Practitioners%20Act%202014.PDF"),
    ("act-zm-2014-002-the-service-commissions-amendment-act-2014-act-no-2-of-2014",
     "https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Services%20Commissions%28Amendment%29%20Act%202014.PDF"),
    ("act-zm-2016-008-the-constitutional-court",
     "https://www.parliament.gov.zm/sites/default/files/documents/acts/N.A.A%208-2018-Constitutional%20Court%2C%20Act.pdf"),
    ("act-zm-2016-009-the-superior-courts-number-of-judges",
     "https://www.parliament.gov.zm/sites/default/files/documents/acts/N.A.A%209-2016%20-%20Superior%20Courts%20%28Number%20of%20Judges%29%20.pdf"),
    ("act-zm-2017-008-supplementary-appropriation-2017",
     "https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%208%20of%202017%20-%20Supplementaty%20Appropriation%20Act.pdf"),
    ("act-zm-2021-026-the-health-professions-amendment-act-2021",
     "https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2026%20of%202021%2C%20The%20Health%20Professions%20%20%28Amendment%29%20Act%202021%20%281%29.pdf"),
]

import pdfplumber

MAX_BATCH_SIZE = 8
BATCH_LABEL = "036"


# ────────────────────────── helpers ─────────────────────────────────────
def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def gap(record_id, reason, url):
    line = f"| {record_id} | REPAIR-{BATCH_LABEL} | {reason} | {url} | {now_iso()} |\n"
    with open(GAPS, "a") as f:
        f.write(line)


def log(msg):
    line = f"{now_iso()}\trepair-batch-{BATCH_LABEL}\t{msg}\n"
    print(line.rstrip())
    with open(LOG, "a") as f:
        f.write(line)


def is_corrupted(body):
    if body is None or not body.strip() or len(body) < 200:
        return True
    lines = body.strip().split('\n')
    num_lines = sum(1 for l in lines if l.strip().isdigit())
    return (num_lines > len(lines) * 0.5 and len(lines) > 10)


def quality_pass(text):
    if len(text) <= 500:
        return False, f"QUALITY_FAIL:{len(text)}chars"
    if is_corrupted(text):
        return False, "QUALITY_FAIL:still_line_numbers"
    has_word = bool(re.search(r'\b[A-Za-z]{6,}\b', text))
    if not has_word:
        return False, "QUALITY_FAIL:no_long_word"
    markers = ('ACT', 'PARLIAMENT', 'ZAMBIA', 'ENACT', 'SECTION', 'AMEND', 'GOVERNMENT', 'CAP')
    hit = sum(1 for m in markers if m in text.upper())
    if hit < 2:
        return False, f"QUALITY_FAIL:not_enough_legal_markers({hit})"
    return True, "OK"


def normalise_sections(text):
    """Collapse blank-line runs, strip form-feeds, split concatenated section numbers."""
    text = text.replace('\x0c', '\n')
    text = re.sub(r'\n{3,}', '\n\n', text)
    lines = text.split('\n')
    output = []
    for line in lines:
        stripped = line.strip()
        m = re.match(r'^(?:Section\s+)?(\d{1,3})\.?\s+([A-Z])', stripped)
        if m:
            first_sec = int(m.group(1))
            rest_start = m.end() - 1
            rest = stripped[rest_start:]
            split_done = False
            for match in re.finditer(r'\s(\d{1,3})\s([A-Z][a-z])', rest):
                candidate_num = int(match.group(1))
                if candidate_num > first_sec and candidate_num <= first_sec + 5 and candidate_num <= 500:
                    split_pos = match.start() + rest_start
                    output.append(stripped[:split_pos].rstrip())
                    output.append(stripped[split_pos:].lstrip())
                    split_done = True
                    break
            if not split_done:
                output.append(line)
        else:
            output.append(line)
    return '\n'.join(output)


# ────────────────────────── download via curl ────────────────────────────
def curl_get(url, dest, *, accept="*/*"):
    cmd = [
        "curl", "--silent", "--show-error", "--location", "--max-time", "120",
        "-A", HEADERS["User-Agent"],
        "-H", f"Accept: {accept}",
        "-w", "%{http_code}",
        "-o", dest,
    ]
    if os.path.exists(CERT):
        cmd[1:1] = ["--cacert", CERT]
    cmd.append(url)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=140)
    code = proc.stdout.strip()
    try:
        status = int(code)
    except ValueError:
        status = -1
    if proc.returncode != 0 and status == -1:
        raise RuntimeError(f"curl rc={proc.returncode} stderr={proc.stderr[:200]}")
    data = b""
    if os.path.exists(dest):
        with open(dest, "rb") as f:
            data = f.read()
    return status, data


def extract_pdf_text(path):
    text = ""
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text += t + "\n"
    except Exception as e:
        log(f"pdfplumber error on {path}: {e}")
    if len(text.strip()) >= 200:
        return text, "pdfplumber"
    # pdftotext layout fallback
    try:
        proc = subprocess.run(
            ["pdftotext", "-layout", path, "-"],
            capture_output=True, text=True, timeout=120
        )
        text2 = proc.stdout or ""
        if len(text2.strip()) >= 200:
            return text2, "pdftotext"
    except Exception as e:
        log(f"pdftotext error: {e}")
    # OCR fallback (poppler + tesseract)
    try:
        with tempfile.TemporaryDirectory() as td:
            subprocess.run(
                ["pdftoppm", "-r", "200", "-gray", path, os.path.join(td, "p")],
                capture_output=True, timeout=300, check=True,
            )
            pages = sorted(glob.glob(os.path.join(td, "p-*.pgm"))) or sorted(glob.glob(os.path.join(td, "p-*.png")))
            ocr_text = []
            for pg in pages[:30]:
                pr = subprocess.run(
                    ["tesseract", pg, "-", "-l", "eng", "--psm", "6"],
                    capture_output=True, text=True, timeout=120,
                )
                if pr.stdout:
                    ocr_text.append(pr.stdout)
            text3 = "\n".join(ocr_text)
            if len(text3.strip()) >= 200:
                return text3, f"ocr({len(pages)}pp)"
    except Exception as e:
        log(f"OCR error: {e}")
    return text, "pdfplumber-poor"


# ───────────────────────── HTML helpers (stdlib) ─────────────────────────
class _PDFLinkFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.pdfs = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            d = dict(attrs)
            href = d.get("href", "")
            if href and (href.lower().endswith((".pdf", ".pdf?")) or ".pdf" in href.lower()):
                self.pdfs.append(href)


def find_pdf_in_html(html_bytes, base_url):
    finder = _PDFLinkFinder()
    try:
        finder.feed(html_bytes.decode("utf-8", errors="replace"))
    except Exception as e:
        log(f"html parse error: {e}")
        return None
    if not finder.pdfs:
        return None
    return urllib.parse.urljoin(base_url, finder.pdfs[0])


# ──────────────────────── per-record handlers ────────────────────────────
def repair_pdf_url(rid, url, pdf_path):
    status, data = curl_get(url, pdf_path, accept="application/pdf")
    if status != 200:
        return None, f"HTTP_{status}"
    if not data.startswith(b"%PDF-"):
        return None, f"NOT_A_PDF({len(data)}B)"
    text, method = extract_pdf_text(pdf_path)
    return (text, method, data), None


def repair_node_url(rid, url, work_dir):
    html_path = os.path.join(work_dir, f"{rid}.html")
    status, html = curl_get(url, html_path, accept="text/html")
    if status != 200:
        return None, f"HTTP_{status}"
    pdf_url = find_pdf_in_html(html, url)
    if not pdf_url:
        return None, "NO_PDF_LINK"
    log(f"  node resolved -> {pdf_url}")
    pdf_path = os.path.join(work_dir, f"{rid}.pdf")
    return repair_pdf_url(rid, pdf_url, pdf_path)


# ───────────────────────────── main ──────────────────────────────────────
def main():
    os.makedirs(PDF_DIR, exist_ok=True)
    os.makedirs(TMPROOT, exist_ok=True)

    journal_path = DB + "-journal"
    try:
        if os.path.exists(journal_path) and os.path.getsize(journal_path) > 0:
            with open(journal_path, "r+b") as f:
                f.truncate(0)
            log("truncated stale corpus.sqlite-journal")
    except Exception as e:
        log(f"journal truncate WARN: {e}")

    tmp_root = tempfile.mkdtemp(prefix=f"repair_batch_{BATCH_LABEL}_", dir=TMPROOT)
    tmp_db = os.path.join(tmp_root, "corpus.sqlite")
    shutil.copy2(DB, tmp_db)
    conn = sqlite3.connect(tmp_db)
    conn.execute("PRAGMA journal_mode=TRUNCATE")
    conn.execute("PRAGMA synchronous=NORMAL")
    c = conn.cursor()

    c.execute("PRAGMA integrity_check")
    integ = c.fetchone()
    log(f"PRE integrity: {integ}")
    if integ != ("ok",):
        log("ABORT: pre-flight integrity not OK")
        conn.close()
        return 2

    c.execute("SELECT COUNT(*) FROM records")
    pre_records = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM records_fts")
    pre_fts = c.fetchone()[0]
    log(f"PRE counts: records={pre_records} records_fts={pre_fts}")

    # Build queue from manifest: skip any that have since been repaired by another worker.
    queue = []
    for rid, url in MANIFEST:
        c.execute("SELECT body FROM records WHERE id=?", (rid,))
        row = c.fetchone()
        if not row:
            log(f"  skip {rid} (not in DB)")
            continue
        if is_corrupted(row[0] or ""):
            queue.append((rid, url))
        else:
            log(f"  skip {rid} (already repaired upstream, {len(row[0] or '')}c)")
        if len(queue) >= MAX_BATCH_SIZE:
            break

    log(f"Queue ({len(queue)}): " + ", ".join(rid for rid, _ in queue))

    results = []
    fetches = 0
    successes = 0
    t_start = time.time()

    for i, (rid, url) in enumerate(queue):
        if i > 0:
            time.sleep(2)
        # 18-minute soft cap (leave room for swap-back + housekeeping)
        if time.time() - t_start > 18 * 60:
            log(f"  TIME_CAP — stopping at {i}/{len(queue)} to stay under 20-min wall-clock")
            break

        try:
            host = urllib.parse.urlparse(url).hostname or ""
            log(f"[{i+1}/{len(queue)}] {rid}  ({host})")
            if "parliament.gov.zm" in host and "/node/" in url:
                outcome, err = repair_node_url(rid, url, PDF_DIR)
            elif "parliament.gov.zm" in host:
                outcome, err = repair_pdf_url(rid, url, os.path.join(PDF_DIR, f"{rid}.pdf"))
            else:
                outcome, err = None, f"UNKNOWN_HOST:{host}"
            fetches += 1
        except Exception as e:
            results.append({"rid": rid, "status": "fail", "reason": f"fetch_error:{type(e).__name__}:{str(e)[:200]}", "url": url})
            gap(rid, f"FETCH_ERR:{type(e).__name__}", url)
            log(f"  -> exc {type(e).__name__}: {e}")
            continue

        if outcome is None:
            results.append({"rid": rid, "status": "fail", "reason": err, "url": url})
            gap(rid, err, url)
            log(f"  -> {err}")
            continue

        text, method, raw_data = outcome
        text = normalise_sections(text)
        ok, qreason = quality_pass(text)
        if not ok:
            results.append({"rid": rid, "status": "fail", "reason": qreason, "chars": len(text), "method": method, "url": url})
            gap(rid, qreason, url)
            log(f"  -> quality fail: {qreason}  ({method} {len(text)}c)")
            continue

        src_hash = hashlib.sha256(raw_data).hexdigest()
        c.execute(
            "UPDATE records SET body=?, source_hash=?, fetched_at=?, parser_version=? WHERE id=?",
            (text, src_hash, now_iso(), f"repair-batch-{BATCH_LABEL}-{method}", rid),
        )
        if c.rowcount != 1:
            results.append({"rid": rid, "status": "fail", "reason": f"update_rowcount:{c.rowcount}", "url": url})
            log(f"  -> update rowcount {c.rowcount} (expected 1)")
            continue

        c.execute("DELETE FROM records_fts WHERE id=?", (rid,))
        c.execute("""
            INSERT INTO records_fts (id, type, title, citation, case_name, outcome_detail, body)
            SELECT id, type, title, citation,
                (SELECT case_name FROM judgments_meta WHERE judgments_meta.id = records.id),
                (SELECT outcome_detail FROM judgments_meta WHERE judgments_meta.id = records.id),
                body
            FROM records WHERE id = ?
        """, (rid,))
        conn.commit()
        successes += 1
        results.append({"rid": rid, "status": "ok", "chars": len(text), "method": method, "src_bytes": len(raw_data), "url": url})
        log(f"  -> OK {len(text)}c via {method}  src={len(raw_data)}B")

    c.execute("SELECT COUNT(*) FROM records")
    rec_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM records_fts")
    fts_count = c.fetchone()[0]
    parity_ok = (rec_count == fts_count)
    c.execute("PRAGMA quick_check")
    qc = c.fetchone()
    c.execute("PRAGMA integrity_check")
    post_integ = c.fetchone()
    log(f"POST quick_check: {qc}    integrity_check: {post_integ}")
    log(f"POST counts: records={rec_count}  records_fts={fts_count}  fixed={successes}  failed={len(results)-successes}")

    out = {
        "ts": now_iso(),
        "batch": BATCH_LABEL,
        "queue_size": len(queue),
        "fetches": fetches,
        "successes": successes,
        "results": results,
        "rec_count": rec_count,
        "fts_count": fts_count,
        "parity_ok": parity_ok,
        "post_integ": post_integ[0] if post_integ else None,
        "quick_check": qc[0] if qc else None,
        "integrity_ok": parity_ok and post_integ == ("ok",) and qc == ("ok",),
    }
    conn.close()

    if out["integrity_ok"] and successes > 0:
        # Atomic swap-back. On FUSE EPERM, fall back to byte-copy.
        try:
            os.replace(tmp_db, DB)
            out["db_synced"] = "os.replace"
        except Exception as e:
            log(f"os.replace failed: {e}; falling back to copy")
            shutil.copy2(tmp_db, DB)
            out["db_synced"] = "shutil.copy2"
    else:
        out["db_synced"] = False
        if not out["integrity_ok"]:
            out["INTEGRITY_FAIL"] = True
    shutil.rmtree(tmp_root, ignore_errors=True)
    print()
    print(json.dumps(out, indent=2))

    with open(os.path.join(WORKDIR, f"_repair_batch_{BATCH_LABEL}_result.json"), "w") as f:
        json.dump(out, f, indent=2)

    with open(COSTS, "a") as f:
        f.write(f"{now_iso()}\trepair-batch-{BATCH_LABEL}\tfetches={fetches}\tsuccesses={successes}\n")

    return 0 if out["integrity_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
