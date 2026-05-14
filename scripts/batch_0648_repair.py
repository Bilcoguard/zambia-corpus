#!/usr/bin/env python3
"""
Repair batch 0648 — continues b0647's drainage of Condition-B SIs.

Pattern (per b0641/b0643/b0644/b0645/b0647):
- Body-only UPDATE (no FTS touch) to preserve parity rule.
- journal_mode=MEMORY to avoid orphan journals.
- zambialii AKN HTML → source.pdf → pdfplumber → quality gate.
- 5s crawl delay between zambialii fetches (robots.txt).
- CA cert needed only for parliament.gov.zm — zambialii uses standard CAs.
"""
import hashlib
import os
import re
import subprocess
import sqlite3
import sys
import time
import urllib.request

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
WORKDIR = "/sessions/zen-busy-gates/tmp/repair_b0648"
DB = "/sessions/zen-busy-gates/mnt/corpus/corpus.sqlite"
CERT = "/sessions/zen-busy-gates/mnt/corpus/scripts/certs/rapidssl_tls_rsa_ca_g1.pem"
CRAWL_DELAY = 5
PARSER_VERSION = "repair-0.6.1"

# Targets: next 8 Condition-B SIs alphabetically continuing from b0647's 2016/04+ cohort.
TARGETS = [
    "si-zm-2016-040-zambia-wildlife-zambia-wildlife-police-uniforms-and-badges-regulations-2016",
    "si-zm-2016-041-zambia-wildlife-game-animals-order-2016",
    "si-zm-2016-042-zambia-wildlife-protected-animals-order-2016",
    "si-zm-2016-043-zambia-wildlife-export-prohibition-order-2016",
    "si-zm-2016-049-national-prosecutions-authority-witness-allowances-and-expenses-regulations-2016",
    "si-zm-2016-059-national-museums-entry-fees-regulations-2016",
    "si-zm-2016-062-electoral-process-code-of-conduct-enforcement-regulations-2016",
    "si-zm-2016-063-electoral-process-general-regulations-2016",
]


def fetch_url(url, dest_path):
    """Fetch URL with curl (uses system CA store)."""
    cmd = [
        "curl", "-sS", "-L",
        "-A", UA,
        "--max-time", "60",
        "-o", dest_path,
        url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl failed for {url}: {r.stderr.strip()}")
    return dest_path


def discover_source_pdf(akn_html_path):
    """Find the source.pdf link inside a zambialii AKN HTML viewer page."""
    with open(akn_html_path, "rb") as f:
        html = f.read().decode("utf-8", errors="replace")
    # Match href to source.pdf
    m = re.search(r'href="([^"]+source\.pdf)"', html)
    if not m:
        raise RuntimeError("no source.pdf href found in HTML")
    href = m.group(1)
    if href.startswith("/"):
        return "https://zambialii.org" + href
    if href.startswith("http"):
        return href
    return "https://zambialii.org/" + href


def extract_pdf_text(pdf_path):
    """Extract text via pdfplumber, page by page."""
    import pdfplumber
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            pages.append(t)
    body = "\n\n".join(pages).strip()
    # Section-marker normalisation: "12.A" → "12. A"
    body = re.sub(r"(\d+)\.([A-Z])", r"\1. \2", body)
    return body


def quality_gate(body):
    """Quality checks: length, digit-ratio, legal-markers."""
    if len(body) < 200:
        return False, f"body-too-short({len(body)})"
    lines = body.strip().split("\n")
    digit_lines = sum(1 for l in lines if l.strip().isdigit())
    if digit_lines > len(lines) * 0.5 and len(lines) > 10:
        return False, f"line-numbers-only(digit={digit_lines}/total={len(lines)})"
    markers = re.search(
        r"\b(Act|Regulations|section|Order|Statutory Instrument|By-Laws|Rules|Notice)\b",
        body,
    )
    if not markers:
        return False, "no-legal-markers"
    return True, "ok"


def repair_one(rec_id, src_url, i):
    """Run the full pipeline for one record. Returns (ok, body_bytes, sha8, note)."""
    html_path = os.path.join(WORKDIR, f"{i}.html")
    pdf_path = os.path.join(WORKDIR, f"{i}.pdf")

    # Step 1: fetch HTML
    fetch_url(src_url, html_path)
    time.sleep(CRAWL_DELAY)

    # Step 2: discover source PDF
    pdf_url = discover_source_pdf(html_path)

    # Step 3: fetch PDF
    fetch_url(pdf_url, pdf_path)
    time.sleep(CRAWL_DELAY)

    # Step 4: extract text
    body = extract_pdf_text(pdf_path)

    # Step 5: quality gate
    ok, reason = quality_gate(body)
    if not ok:
        return False, len(body), None, f"quality-gate-fail:{reason}"

    # Step 6: compute hash + UPDATE
    h = hashlib.sha256(body.encode("utf-8")).hexdigest()
    sha8 = h[:8]

    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA cell_size_check=OFF")
    conn.execute("PRAGMA journal_mode=MEMORY")
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE records SET body=?, source_hash=?, fetched_at=?, parser_version=? WHERE id=?",
            (body, h, int(time.time()), PARSER_VERSION, rec_id),
        )
        if cur.rowcount != 1:
            conn.rollback()
            return False, len(body), sha8, f"update-rowcount={cur.rowcount}"
        conn.commit()
    finally:
        conn.close()
    return True, len(body), sha8, "ok"


def main():
    os.makedirs(WORKDIR, exist_ok=True)
    # Resolve each target's URL from the DB.
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA cell_size_check=OFF")
    cur = conn.cursor()
    url_map = {}
    for tid in TARGETS:
        cur.execute("SELECT source_url FROM records WHERE id=?", (tid,))
        row = cur.fetchone()
        if row is None:
            url_map[tid] = None
        else:
            url_map[tid] = row[0]
    conn.close()

    results = []
    for i, tid in enumerate(TARGETS, 1):
        url = url_map.get(tid)
        if not url:
            results.append((tid, False, 0, None, "id-not-in-db"))
            print(f"[{i}/8] {tid}: SKIP id-not-in-db", flush=True)
            continue
        try:
            ok, n, sha8, note = repair_one(tid, url, i)
            results.append((tid, ok, n, sha8, note))
            print(f"[{i}/8] {tid}: {'OK' if ok else 'FAIL'} bytes={n} sha8={sha8} ({note})", flush=True)
        except Exception as e:
            results.append((tid, False, 0, None, f"exception:{e}"))
            print(f"[{i}/8] {tid}: EXCEPTION {e}", flush=True)

    print("\nSUMMARY:")
    ok_count = sum(1 for r in results if r[1])
    total_bytes = sum(r[2] for r in results if r[1])
    print(f"  OK: {ok_count}/{len(results)}")
    print(f"  Total body bytes written: {total_bytes}")
    print(f"  SHA256(8) chain: {'+'.join(r[3] for r in results if r[1] and r[3])}")


if __name__ == "__main__":
    main()
