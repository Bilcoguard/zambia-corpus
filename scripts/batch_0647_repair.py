#!/usr/bin/env python3
"""b0647 — Repair worker batch.

Continues the b0643/b0644/b0645 pattern: body-only updates to
Condition-B SIs at zambialii.org bare-path AKN URLs (HTML viewer →
source.pdf discovery → pdfplumber). No FTS shadow-table mutation.
corpus.sqlite NOT staged this tick per parity rule
(records=1928, records_fts=1924, gap=4 unchanged since b038).

journal_mode=MEMORY + temp_store=MEMORY to bypass FUSE bindfs EPERM on
corpus.sqlite-journal unlink (chronic blocker discovered at b0644).
"""
import hashlib
import json
import re
import sqlite3
import time
import urllib.request
from datetime import datetime, timezone

import pdfplumber

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
CRAWL_DELAY = 5  # seconds per zambialii robots.txt
BATCH = "b0647-repair"
PARSER_VERSION = "repair-0.6.0"
WORKDIR = "/sessions/youthful-compassionate-planck/tmp/repair_b0647"


def fetch(url, dest=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
        if dest:
            with open(dest, "wb") as f:
                f.write(data)
        return data


def discover_pdf(html_bytes, base_url):
    text = html_bytes.decode("utf-8", errors="replace")
    m = re.search(r'href="([^"]*source\.pdf)"', text)
    if not m:
        return None
    href = m.group(1)
    if href.startswith("/"):
        proto_host = re.match(r"^(https?://[^/]+)", base_url).group(1)
        return proto_host + href
    return href


def extract_pdf_text(path):
    parts = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            parts.append(t)
    return "\n".join(parts)


def normalise(text):
    text = re.sub(r"(\d+)\.([A-Z])", r"\1. \2", text)
    return text


def quality_gate(body):
    if not body or len(body) < 200:
        return False, "too_short"
    lines = body.strip().split("\n")
    digit_lines = sum(1 for l in lines if l.strip().isdigit())
    if digit_lines > len(lines) * 0.5 and len(lines) > 10:
        return False, "line_numbers_only"
    markers = ["Act", "Regulations", "section", "Order", "ENACTED",
               "Statutory Instrument", "By-Laws", "Rules", "Notice"]
    if not any(m.lower() in body.lower() for m in markers):
        return False, "no_legal_markers"
    return True, "ok"


def main():
    with open(f"{WORKDIR}/candidates.json") as f:
        candidates = json.load(f)

    con = sqlite3.connect("corpus.sqlite")
    cur = con.cursor()
    cur.execute("PRAGMA cell_size_check = OFF")
    cur.execute("PRAGMA temp_store = MEMORY")
    cur.execute("PRAGMA journal_mode = MEMORY")

    results = []
    for i, (rid, url) in enumerate(candidates):
        entry = {"id": rid, "url": url}
        try:
            html = fetch(url)
            pdf_url = discover_pdf(html, url)
            entry["pdf_url"] = pdf_url
            if not pdf_url:
                entry["result"] = "FAIL_NO_PDF_LINK"
                results.append(entry)
                continue
            pdf_path = f"{WORKDIR}/{i}.pdf"
            fetch(pdf_url, dest=pdf_path)
            body = extract_pdf_text(pdf_path)
            body = normalise(body)
            ok, reason = quality_gate(body)
            entry["body_len"] = len(body)
            entry["qg"] = reason
            if not ok:
                entry["result"] = f"FAIL_QG_{reason}"
                results.append(entry)
                continue
            h = hashlib.sha256(body.encode("utf-8")).hexdigest()
            ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            cur.execute(
                "UPDATE records SET body = ?, source_hash = ?, fetched_at = ?, parser_version = ? WHERE id = ?",
                (body, h, ts, PARSER_VERSION, rid),
            )
            con.commit()
            entry["result"] = "OK"
            entry["sha"] = h
            results.append(entry)
        except Exception as e:
            entry["result"] = f"ERR_{type(e).__name__}"
            entry["err"] = str(e)[:200]
            results.append(entry)
        time.sleep(CRAWL_DELAY)

    con.close()
    with open(f"{WORKDIR}/results.json", "w") as f:
        json.dump(results, f, indent=2)
    for r in results:
        print(r.get("result"), r["id"][:60], "len=", r.get("body_len"))


if __name__ == "__main__":
    main()
