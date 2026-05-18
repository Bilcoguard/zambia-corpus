#!/usr/bin/env python3
"""Repair worker batch b0697 — ZambiaLII SI repair (continuation of b0695).

Per Repair Corpus Worker v4 SKILL.md (Steps 1-7):
  - Live SQL identification (all three conditions).
  - For zambialii.org AKN-SI pages: fetch HTML, find /akn/.../source.pdf,
    download the PDF, extract with pdfplumber, OCR fallback if needed.
  - Quality gate (length, digit-ratio, legal-text markers).
  - UPDATE records + DELETE+INSERT records_fts per record; commit per record.
  - Cap at MAX_BATCH_SIZE = 8 per tick.
"""
import os, sys, re, hashlib, time, sqlite3, subprocess, json
from urllib.parse import urljoin

import requests
import pdfplumber

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
DB = "corpus.sqlite"
BATCH = "b0697"
PARSER = "repair-0.6.97"
CERT = "scripts/certs/rapidssl_tls_rsa_ca_g1.pem"
MAX_BATCH = 8
TIME_BUDGET = 17 * 60  # seconds — leaves headroom under 20-min wall-clock

t_start = time.time()

def log(msg):
    line = f"[{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}] {BATCH} {msg}"
    print(line, flush=True)
    with open("worker.log", "a") as f:
        f.write(line + "\n")

def gap(msg):
    with open("gaps.md", "a") as f:
        f.write(f"- {BATCH} {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}: {msg}\n")

def cost(action, bytes_=0, sec=0.0):
    with open("costs.log", "a") as f:
        f.write(f"{BATCH}\t{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\t{action}\tbytes={bytes_}\tsec={sec:.2f}\n")

def digit_ratio_ok(body: str) -> bool:
    lines = body.strip().split('\n')
    if len(lines) <= 10:
        return True
    digit_lines = sum(1 for l in lines if l.strip().isdigit())
    return not (digit_lines > len(lines) * 0.5)

def quality_ok(body: str):
    if not body or len(body) < 200:
        return False, f"body too short ({len(body) if body else 0} chars)"
    if not digit_ratio_ok(body):
        return False, "fails digit-ratio test (line-numbers-only)"
    body_l = body.lower()
    markers = ["section", " act", "regulation", "order", "enacted", "minister",
               "appointed", "schedule", "by virtue"]
    if not any(m in body_l for m in markers):
        return False, "no recognisable legal text markers"
    return True, "ok"

def normalise_sections(text: str) -> str:
    text = re.sub(r'(?m)^(\d+)\.([A-Z])', r'\1. \2', text)
    return text

session = requests.Session()
session.headers.update({"User-Agent": UA})

def fetch_html(url):
    t0 = time.time()
    r = session.get(url, timeout=30, allow_redirects=True, verify=True)
    dt = time.time() - t0
    cost("fetch_html", len(r.content), dt)
    r.raise_for_status()
    return r.text, str(r.url)

def fetch_pdf(url, dst):
    t0 = time.time()
    if "parliament.gov.zm" in url:
        rc = subprocess.run(
            ["curl", "--cacert", CERT, "-fL",
             "-A", UA, "-o", dst, "--max-time", "60", url],
            capture_output=True, text=True)
        dt = time.time() - t0
        size = os.path.getsize(dst) if os.path.exists(dst) else 0
        cost("fetch_pdf_curl", size, dt)
        if rc.returncode != 0:
            return False, f"curl rc={rc.returncode}: {rc.stderr[:200]}"
    else:
        r = session.get(url, timeout=60)
        dt = time.time() - t0
        cost("fetch_pdf", len(r.content), dt)
        if r.status_code != 200:
            return False, f"HTTP {r.status_code}"
        with open(dst, "wb") as f:
            f.write(r.content)
    return True, "ok"

def extract_pdf(path):
    text_parts = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                if t.strip():
                    text_parts.append(t)
    except Exception as e:
        return "", f"pdfplumber error: {e}"
    text = "\n\n".join(text_parts)
    return normalise_sections(text), "ok"

def find_pdf_in_html(html, base_url):
    m = re.search(r'href="(/akn/[^"]+/source\.pdf)"', html)
    if m:
        return urljoin(base_url, m.group(1))
    m = re.search(r'data-pdf="(/akn/[^"]+\.pdf)"', html)
    if m:
        return urljoin(base_url, m.group(1))
    m = re.search(r'href="(https?://[^"]+\.pdf)"', html, re.I)
    if m:
        return m.group(1)
    return None

def repair_one(rid, url, rtype, conn):
    log(f"REPAIR start id={rid} url={url}")
    safe_name = re.sub(r'[^A-Za-z0-9_-]', '_', rid)[:60]
    tmp_pdf = f"/tmp/{safe_name}.pdf"
    if os.path.exists(tmp_pdf):
        os.remove(tmp_pdf)
    try:
        if "zambialii.org" in url and not url.endswith(".pdf"):
            html, eff_url = fetch_html(url)
            pdf_url = find_pdf_in_html(html, eff_url)
            if not pdf_url:
                gap(f"{rid}: no PDF link found in HTML")
                return False, "no-pdf-link"
            ok, msg = fetch_pdf(pdf_url, tmp_pdf)
            if not ok:
                gap(f"{rid}: PDF fetch failed: {msg}")
                return False, f"pdf-fetch-{msg}"
            body, msg = extract_pdf(tmp_pdf)
            if msg != "ok":
                gap(f"{rid}: extract failed: {msg}")
                return False, msg
        elif url.endswith(".pdf") or "/source.pdf" in url:
            ok, msg = fetch_pdf(url, tmp_pdf)
            if not ok:
                gap(f"{rid}: PDF fetch failed: {msg}")
                return False, f"pdf-fetch-{msg}"
            body, msg = extract_pdf(tmp_pdf)
            if msg != "ok":
                gap(f"{rid}: extract failed: {msg}")
                return False, msg
        else:
            gap(f"{rid}: unknown URL pattern {url}")
            return False, "unknown-url"

        ok, why = quality_ok(body)
        if not ok:
            gap(f"{rid}: quality gate failed — {why} (len={len(body)})")
            return False, f"quality-{why}"

        body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
        c = conn.cursor()
        c.execute("""UPDATE records SET body=?, source_hash=?, fetched_at=?, parser_version=?
                     WHERE id=?""",
                  (body, body_hash, time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                   PARSER, rid))
        c.execute("DELETE FROM records_fts WHERE id=?", (rid,))
        c.execute("""
            INSERT INTO records_fts (rowid, id, title, body, citation, type)
            SELECT rowid, id, title, body, citation, type
            FROM records WHERE id=?
        """, (rid,))
        conn.commit()
        log(f"REPAIR ok id={rid} body_len={len(body)} hash={body_hash[:12]}")
        return True, f"len={len(body)}"
    finally:
        if os.path.exists(tmp_pdf):
            try: os.remove(tmp_pdf)
            except: pass

def main():
    conn = sqlite3.connect(DB, timeout=60)
    c = conn.cursor()
    c.execute("PRAGMA journal_mode=MEMORY")
    c.execute("PRAGMA synchronous=OFF")
    c.execute("PRAGMA busy_timeout=60000")

    # Condition B (no body, acts/sis only)
    c.execute("""
      SELECT id, source_url, type FROM records
      WHERE (body IS NULL OR body = '') AND type IN ('act','si')
      ORDER BY id
    """)
    all_targets = c.fetchall()
    log(f"Condition B (no-body acts/sis): {len(all_targets)}")

    # Condition A (corrupted digit-line body)
    c.execute("""SELECT id, source_url, type, body FROM records
                  WHERE body IS NOT NULL AND length(body) > 10
                    AND type IN ('act','si','judgment')""")
    corrupted = []
    for rid, url, rtype, body in c.fetchall():
        lines = body.strip().split('\n')
        digit_lines = sum(1 for l in lines if l.strip().isdigit())
        if digit_lines > len(lines) * 0.5 and len(lines) > 10:
            corrupted.append((rid, url, rtype))
    log(f"Condition A (corrupted): {len(corrupted)}")

    # Condition C (stub acts/sis)
    c.execute("""SELECT id, source_url, type FROM records
                  WHERE type IN ('act','si') AND length(body) > 0 AND length(body) < 200""")
    stubs = c.fetchall()
    log(f"Condition C (stubs): {len(stubs)}")

    seen = set()
    targets = []
    for r in all_targets + corrupted + stubs:
        if r[0] in seen: continue
        seen.add(r[0])
        targets.append(r)

    log(f"Total dedup targets: {len(targets)}; picking up to {MAX_BATCH}")

    if not targets:
        log("All repair targets fixed — repair worker idle")
        # Per SKILL.md Step 2 final note.

    repaired = []
    failed = []
    for rid, url, rtype in targets[:MAX_BATCH]:
        if time.time() - t_start > TIME_BUDGET:
            log("Time budget exhausted; stopping early")
            break
        try:
            ok, msg = repair_one(rid, url, rtype, conn)
            if ok:
                repaired.append((rid, msg))
            else:
                failed.append((rid, msg))
        except Exception as e:
            log(f"REPAIR exception id={rid}: {e}")
            failed.append((rid, f"exception:{e}"))
        time.sleep(1.0)

    c.execute("SELECT COUNT(*) FROM records"); rc = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM records_fts"); fc = c.fetchone()[0]
    log(f"INTEGRITY records={rc} records_fts={fc} match={rc==fc}")
    c.execute("PRAGMA quick_check")
    qc = c.fetchone()[0]
    log(f"PRAGMA quick_check: {qc}")

    remaining = len(targets) - len(repaired)

    summary = {
        "batch": BATCH,
        "parser": PARSER,
        "identified_no_body": len(all_targets),
        "identified_corrupted": len(corrupted),
        "identified_stub": len(stubs),
        "dedup_targets": len(targets),
        "repaired": len(repaired),
        "failed": len(failed),
        "remaining": remaining,
        "records": rc,
        "records_fts": fc,
        "integrity_match": rc == fc,
        "quick_check": qc,
        "elapsed_sec": round(time.time() - t_start, 1),
        "repaired_ids": repaired,
        "failed_ids": failed,
    }
    print("\nSUMMARY:")
    print(json.dumps(summary, indent=2, default=str))
    with open(f"reports/repair-batch-{BATCH}-summary.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    conn.close()
    return summary

if __name__ == "__main__":
    main()
