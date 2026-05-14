#!/usr/bin/env python3
"""
Repair batch 0652 (SI tail) — continues b0650 drainage of Condition-B SIs.
Picks the first 5 alphabetical no-body SIs not yet attempted (2018 cohort).
"""
import hashlib
import os
import re
import subprocess
import sqlite3
import time

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
WORKDIR = "/sessions/modest-optimistic-dijkstra/mnt/corpus/_repair_b0652_pdfs"
DB = "/sessions/modest-optimistic-dijkstra/mnt/corpus/corpus.sqlite"
CRAWL_DELAY = 5
PARSER_VERSION = "repair-0.6.2"

TARGETS = [
    "si-zm-2018-002-education-military-training-establishment-of-zambia-management-dissolution-regulations-2018",
    "si-zm-2018-003-zambia-defence-university-declaration-order-2018",
    "si-zm-2018-007-railways-transportation-of-heavy-goods-regulations-2018",
    "si-zm-2018-014-tourism-and-hospitality-accommodation-establishment-standards-regulations-2018",
    "si-zm-2018-021-electoral-process-local-government-by-election-election-date-and-time-of-poll-order-2018",
]


def fetch_url(url, dest_path):
    cmd = ["curl", "-sS", "-L", "-A", UA, "--max-time", "60", "-o", dest_path, url]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl failed for {url}: {r.stderr.strip()}")
    return dest_path


def discover_source_pdf(akn_html_path):
    with open(akn_html_path, "rb") as f:
        html = f.read().decode("utf-8", errors="replace")
    m = re.search(r'href="([^"]+source\.pdf)"', html)
    if not m:
        return None
    href = m.group(1)
    if href.startswith("/"):
        return "https://zambialii.org" + href
    if href.startswith("http"):
        return href
    return "https://zambialii.org/" + href


def extract_pdf_text(pdf_path):
    import pdfplumber
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    body = "\n\n".join(pages).strip()
    body = re.sub(r"(\d+)\.([A-Z])", r"\1. \2", body)
    return body


def quality_gate(body):
    if len(body) < 200:
        return False, f"body-too-short({len(body)})"
    lines = body.strip().split("\n")
    digit_lines = sum(1 for l in lines if l.strip().isdigit())
    if digit_lines > len(lines) * 0.5 and len(lines) > 10:
        return False, f"line-numbers-only(digit={digit_lines}/total={len(lines)})"
    markers = re.search(r"\b(Act|Regulations|section|Order|Statutory Instrument|By-Laws|Rules|Notice|enacted|Parliament)\b", body)
    if not markers:
        return False, "no-legal-markers"
    return True, "ok"


def repair_one(rec_id, src_url, i):
    html_path = os.path.join(WORKDIR, f"si{i}.html")
    pdf_path = os.path.join(WORKDIR, f"si{i}.pdf")

    fetch_url(src_url, html_path)
    time.sleep(CRAWL_DELAY)

    pdf_url = discover_source_pdf(html_path)
    if not pdf_url:
        return False, 0, None, "no-source-pdf-href"

    fetch_url(pdf_url, pdf_path)
    time.sleep(CRAWL_DELAY)

    body = extract_pdf_text(pdf_path)
    ok, reason = quality_gate(body)
    if not ok:
        return False, len(body), None, f"quality-gate-fail:{reason}"

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
    results = []
    for i, tid in enumerate(TARGETS, 1):
        conn = sqlite3.connect(DB)
        conn.execute("PRAGMA cell_size_check=OFF")
        try:
            cur = conn.cursor()
            cur.execute("SELECT source_url FROM records WHERE id=?", (tid,))
            row = cur.fetchone()
        finally:
            conn.close()
        if not row or not row[0]:
            results.append((tid, False, 0, None, "id-not-in-db"))
            print(f"[{i}/{len(TARGETS)}] {tid}: SKIP no-url", flush=True)
            continue
        try:
            ok, n, sha8, note = repair_one(tid, row[0], i)
            results.append((tid, ok, n, sha8, note))
            print(f"[{i}/{len(TARGETS)}] {tid}: {'OK' if ok else 'FAIL'} bytes={n} sha8={sha8} ({note})", flush=True)
        except Exception as e:
            results.append((tid, False, 0, None, f"exception:{type(e).__name__}:{e}"))
            print(f"[{i}/{len(TARGETS)}] {tid}: EXCEPTION {type(e).__name__}: {e}", flush=True)

    ok_count = sum(1 for r in results if r[1])
    total_bytes = sum(r[2] for r in results if r[1])
    print(f"\nSI SUMMARY: OK={ok_count}/{len(results)} bytes={total_bytes}")
    chain = "+".join(r[3] for r in results if r[1] and r[3])
    print(f"  SHA256(8) chain: {chain}")
    return results


if __name__ == "__main__":
    main()
