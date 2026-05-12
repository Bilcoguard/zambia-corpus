#!/usr/bin/env python3
"""Repair worker batch 033 — fixes up to 8 corrupted/empty Act/SI bodies.

Follows SKILL.md repair worker spec (v4, 2026-05-12 tick).
Handles three URL types:
  1. parliament.gov.zm direct-PDF URLs       → curl + pdfplumber + pdftotext + OCR fallback
  2. parliament.gov.zm /node/<id> URLs       → fetch HTML, extract PDF link, then PDF pipeline
  3. zambialii.org HTML URLs                  → try source.pdf variant first, else HTML body
TMPDIR-routed atomic copy to work around FUSE journal limitations.
"""
import os, sys, re, time, json, sqlite3, ssl, glob, shutil, tempfile, hashlib, subprocess
import urllib.request, urllib.error, urllib.parse
from datetime import datetime, timezone
from html.parser import HTMLParser

# ───────────────────────────── SSL / opener ──────────────────────────────
def _build_ctx():
    ctx = ssl.create_default_context()
    extra_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "certs")
    if os.path.isdir(extra_dir):
        for pem in sorted(glob.glob(os.path.join(extra_dir, "*.pem"))):
            try:
                ctx.load_verify_locations(cafile=pem)
            except Exception as e:
                print(f"WARN: failed to load {pem}: {e}", file=sys.stderr)
    return ctx
SSL_CTX = _build_ctx()
OPENER = urllib.request.build_opener(urllib.request.HTTPSHandler(context=SSL_CTX))

WORKDIR  = "/sessions/upbeat-beautiful-johnson/mnt/corpus"
PDF_DIR  = os.path.join(WORKDIR, "_repair_b033_pdfs")
TMPROOT  = os.path.join(WORKDIR, "_repair_b033_tmpdb")
DB       = os.path.join(WORKDIR, "corpus.sqlite")
GAPS     = os.path.join(WORKDIR, "gaps.md")
LOG      = os.path.join(WORKDIR, "worker.log")
COSTS    = os.path.join(WORKDIR, "costs.log")
HEADERS  = {'User-Agent': 'KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)'}
CERT     = os.path.join(WORKDIR, "scripts/certs/rapidssl_tls_rsa_ca_g1.pem")

# v4 manifest — still-needing-repair set computed at start of tick (live DB check).
# Continues from b032 (1989/1996 zambialii + 2008/2010 parliament). b033 targets
# next 8 stub Acts from manifest in 2010/2011 parliament series.
MANIFEST = [
    ("act-zm-2010-050-property-transfer-tax-amendment", "https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Property%20Transfer%20Tax%20%28Amendment%29%202010A_0.PDF"),
    ("act-zm-2011-006-the-english-law-extent-of-application-amendment-act-2011", "https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/The%20English%20Law%20Act.pdf"),
    ("act-zm-2011-007-the-high-court-amendment-act-2011", "https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/The%20High%20Court%20Amendment%20Act%2C%20%202011.pdf"),
    ("act-zm-2011-008-the-supreme-court-amendment-act-2011", "https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/The%20Supreme%20Court%20Act%2C%202011.pdf"),
    ("act-zm-2011-009-the-zambia-institute-of-advanced-legal-education-amendment-act-2011", "https://www.parliament.gov.zm/sites/default/files/documents/acts/No9_2011.pdf"),
    ("act-zm-2011-010-the-presidental-emoluments-amendment-act-2011", "https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Bills%20-Presidential%20%28Emoluments%29%28Amendment%29%202011.pdf"),
    ("act-zm-2011-027-income-tax-amendment-act-2011", "https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Income%20Tax%20%28Amendment%29%20Act%202011.PDF"),
    ("act-zm-2011-029-zambia-development-agency-amendment-act-2011", "https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/The%20Zambia%20Development%20Agency%20%28Amendment%29%20Act%202011.pdf"),
    ("act-zm-2011-030-value-added-tax-amendment-act-2011", "https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Value%20Added%20%20Tax%20%28Amendment%29%20Act%2C%202011.pdf"),
    ("act-zm-2012-003-the-anti-corruption-act-2012", "https://www.parliament.gov.zm/sites/default/files/documents/acts/Anti%20Corruption%20Act%2C%202012.PDF"),
]

import pdfplumber

MAX_BATCH_SIZE = 8
BATCH_LABEL = "033"


# ────────────────────────── small helpers ───────────────────────────────
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
    """Download URL with rapidssl CA cert. Returns (status_code, bytes)."""
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
            for pg in pages[:30]:                       # safety cap
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
        self.base = ""
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            d = dict(attrs)
            href = d.get("href", "")
            if href and href.lower().endswith((".pdf", ".pdf?")) or ".pdf" in href.lower():
                self.pdfs.append(href)


class _BodyTextExtractor(HTMLParser):
    SKIP = {"script", "style", "noscript", "head", "title", "nav", "footer", "header"}
    def __init__(self):
        super().__init__()
        self.skip_depth = 0
        self.parts = []
    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_depth += 1
    def handle_endtag(self, tag):
        if tag in self.SKIP and self.skip_depth > 0:
            self.skip_depth -= 1
    def handle_data(self, data):
        if self.skip_depth == 0:
            s = data.strip()
            if s:
                self.parts.append(s)


def find_pdf_in_html(html_bytes, base_url):
    finder = _PDFLinkFinder()
    try:
        finder.feed(html_bytes.decode("utf-8", errors="replace"))
    except Exception as e:
        log(f"html parse error: {e}")
        return None
    if not finder.pdfs:
        return None
    href = finder.pdfs[0]
    return urllib.parse.urljoin(base_url, href)


def extract_html_body(html_bytes):
    extractor = _BodyTextExtractor()
    try:
        extractor.feed(html_bytes.decode("utf-8", errors="replace"))
    except Exception as e:
        log(f"html body parse error: {e}")
        return ""
    return "\n".join(extractor.parts)


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


def repair_zambialii_html(rid, url, work_dir):
    candidates = []
    if not url.endswith("/source.pdf"):
        candidates.append(url.rstrip("/") + "/source.pdf")
    candidates.append(url)
    for cand in candidates:
        log(f"  zambialii try -> {cand}")
        path = os.path.join(work_dir, f"{rid}_zlii.bin")
        status, data = curl_get(cand, path, accept="*/*")
        if status != 200 or not data:
            continue
        if data.startswith(b"%PDF-"):
            pdf_path = os.path.join(work_dir, f"{rid}.pdf")
            os.rename(path, pdf_path)
            text, method = extract_pdf_text(pdf_path)
            return (text, f"zlii_{method}", data), None
        body = extract_html_body(data)
        if len(body.strip()) >= 500:
            return (body, "zlii_html", data), None
        log(f"  zambialii html only {len(body)}c — too short, trying next")
    return None, "ZAMBIALII_NO_USABLE_CONTENT"


# ───────────────────────────── main ──────────────────────────────────────
def main():
    os.makedirs(PDF_DIR, exist_ok=True)
    journal_path = DB + "-journal"
    try:
        if os.path.exists(journal_path) and os.path.getsize(journal_path) > 0:
            with open(journal_path, "r+b") as f:
                f.truncate(0)
            log("truncated stale corpus.sqlite-journal")
    except Exception as e:
        log(f"journal truncate WARN: {e}")

    os.makedirs(TMPROOT, exist_ok=True)
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

    queue = []
    for rid, url in MANIFEST:
        c.execute("SELECT body FROM records WHERE id=?", (rid,))
        row = c.fetchone()
        if not row:
            continue
        if is_corrupted(row[0] or ""):
            queue.append((rid, url))
        if len(queue) >= MAX_BATCH_SIZE:
            break

    log(f"Queue ({len(queue)}): " + ", ".join(rid for rid, _ in queue))

    results = []
    fetches = 0
    successes = 0

    for i, (rid, url) in enumerate(queue):
        if i > 0:
            time.sleep(2)

        try:
            host = urllib.parse.urlparse(url).hostname or ""
            log(f"[{i+1}/{len(queue)}] {rid}  ({host})")
            if "parliament.gov.zm" in host and "/node/" in url:
                outcome, err = repair_node_url(rid, url, PDF_DIR)
            elif "parliament.gov.zm" in host:
                outcome, err = repair_pdf_url(rid, url, os.path.join(PDF_DIR, f"{rid}.pdf"))
            elif "zambialii" in host:
                outcome, err = repair_zambialii_html(rid, url, PDF_DIR)
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
    integrity_ok = (rec_count == fts_count)
    c.execute("PRAGMA quick_check")
    qc = c.fetchone()
    c.execute("PRAGMA integrity_check")
    post_integ = c.fetchone()
    log(f"POST quick_check: {qc}    integrity_check: {post_integ}")

    out = {
        "ts": now_iso(),
        "batch": BATCH_LABEL,
        "queue_size": len(queue),
        "fetches": fetches,
        "successes": successes,
        "results": results,
        "rec_count": rec_count,
        "fts_count": fts_count,
        "integrity_ok": integrity_ok and post_integ == ("ok",) and qc == ("ok",),
        "post_integ": post_integ[0] if post_integ else None,
        "quick_check": qc[0] if qc else None,
    }
    conn.close()
    if out["integrity_ok"] and successes > 0:
        shutil.copy2(tmp_db, DB)
        out["db_synced"] = True
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
