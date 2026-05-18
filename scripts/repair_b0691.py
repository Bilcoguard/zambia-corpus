#!/usr/bin/env python3
"""b0691 repair worker — ZambiaLII SI repair (continuation of b0688 drainage).

Same parser pattern as repair_b0688.py (parser version repair-0.6.85+);
only path-config and batch identifier differ. This tick continues to drain
the remaining 81 zambialii AKN-SI Condition-B records.

Parser version: repair-0.6.91.
"""
import sqlite3, urllib.request, urllib.error, ssl, re, os, sys, hashlib, json, time, subprocess, shutil
from pathlib import Path
from bs4 import BeautifulSoup

WORKSPACE = Path("/sessions/wizardly-trusting-goldberg/mnt/corpus")
PDF_DIR = Path("/tmp/b0691_pdfs")
PDF_DIR.mkdir(parents=True, exist_ok=True)
CERT = WORKSPACE / "scripts" / "certs" / "rapidssl_tls_rsa_ca_g1.pem"
UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
MAX_BATCH = 8
TIME_LIMIT = 18 * 60
START_T = time.time()
BATCH = "b0691"

TMP_DIR = Path("/tmp/b0691_recover")
TMP_DIR.mkdir(parents=True, exist_ok=True)
SRC_DB = WORKSPACE / "corpus.sqlite"
DB = TMP_DIR / "corpus.sqlite"

if not DB.exists() or DB.stat().st_mtime < SRC_DB.stat().st_mtime:
    print(f"Staging DB to {DB} ...")
    shutil.copy2(SRC_DB, DB)


def now_sec():
    return time.time() - START_T


def http_get(url, out_path=None, timeout=45):
    if "parliament.gov.zm" in url and out_path is not None:
        cmd = ["curl", "--cacert", str(CERT), "-L", "-A", UA, "--max-time", str(timeout),
               "-o", str(out_path), url]
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode != 0:
            raise RuntimeError(f"curl failed: {r.stderr.decode(errors='ignore')[:300]}")
        return out_path.read_bytes()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    if out_path is not None:
        out_path.write_bytes(data)
    return data


def extract_pdf_text(pdf_path):
    import pdfplumber
    text_parts = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                t = page.extract_text() or ""
                text_parts.append(t)
    except Exception as e:
        return "", str(e)
    return "\n".join(text_parts).strip(), None


def normalise_text(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"^(\d{1,4})\.([A-Z])", r"\1. \2", text, flags=re.MULTILINE)
    text = "\n".join(l.rstrip() for l in text.split("\n"))
    return text


def digit_ratio_test(body):
    lines = body.strip().split("\n")
    if len(lines) <= 10:
        return False
    digit_lines = sum(1 for l in lines if l.strip().isdigit())
    return digit_lines > len(lines) * 0.5


def quality_gate(body):
    if not body or len(body) <= 200:
        return False, "too_short"
    if digit_ratio_test(body):
        return False, "line_numbers_only"
    low = body.lower()
    if not any(kw in low for kw in ("section", "act", "regulation", "order", "by-law",
                                    "enacted", "schedule", "statutory", "minister",
                                    "republic of zambia", "rule", "notice", "preamble")):
        return False, "no_legal_text"
    return True, "ok"


def fetch_zambialii_body(record_id, source_url):
    if source_url.startswith("//"):
        source_url = "https:" + source_url
    if not source_url.startswith("http"):
        source_url = "https://zambialii.org" + source_url
    try:
        html = http_get(source_url).decode("utf-8", errors="replace")
    except Exception as e:
        return None, f"html_fetch_failed: {e}"
    soup = BeautifulSoup(html, "html.parser")
    pdf_href = None
    for a in soup.find_all("a", href=True):
        if "source.pdf" in a["href"]:
            pdf_href = a["href"]
            break
    if pdf_href:
        if pdf_href.startswith("/"):
            pdf_url = "https://zambialii.org" + pdf_href
        elif pdf_href.startswith("http"):
            pdf_url = pdf_href
        else:
            pdf_url = "https://zambialii.org/" + pdf_href
        pdf_path = PDF_DIR / (record_id + ".pdf")
        try:
            http_get(pdf_url, out_path=pdf_path)
        except Exception as e:
            return None, f"pdf_fetch_failed: {e}"
        text, err = extract_pdf_text(pdf_path)
        if err:
            return None, f"pdf_extract_failed: {err}"
        text = normalise_text(text)
        if len(text) >= 200:
            return text, "pdf"
    body_div = None
    for sel in [".akn-act", ".akn-statutoryInstrument", ".akn-doc",
                "[class*=akn-act]", "[class*=akn-statutory]",
                "main", "article", ".content", "#content"]:
        body_div = soup.select_one(sel)
        if body_div and len(body_div.get_text(strip=True)) > 200:
            break
    if not body_div:
        return None, "no_html_body"
    text = body_div.get_text(separator="\n", strip=True)
    text = normalise_text(text)
    return text, "html"


def main():
    conn = sqlite3.connect(str(DB))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT id, source_url, type, title, citation, body FROM records
        WHERE (body IS NULL OR body = '')
          AND type IN ('act', 'si')
        ORDER BY type, id
    """)
    targets = cur.fetchall()
    print(f"Records needing repair: {len(targets)}")

    repaired = []
    failed = []
    for rec in targets:
        if len(repaired) >= MAX_BATCH:
            break
        if now_sec() > TIME_LIMIT:
            print(f"Time limit approaching, stopping after {len(repaired)} repaired")
            break
        rid = rec["id"]
        url = rec["source_url"]
        print(f"\n[{len(repaired)+1}] {rid}")
        print(f"  URL: {url}")
        try:
            body, source = fetch_zambialii_body(rid, url)
        except Exception as e:
            failed.append((rid, f"exception: {e}"))
            print(f"  EXCEPTION: {e}")
            continue
        if body is None:
            failed.append((rid, source or "unknown"))
            print(f"  FAILED: {source}")
            continue
        ok, reason = quality_gate(body)
        if not ok:
            failed.append((rid, f"quality_gate:{reason}"))
            print(f"  QUALITY FAIL: {reason} (len={len(body)})")
            continue
        body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
        cur.execute("SELECT rowid FROM records WHERE id = ?", (rid,))
        old_rowid = cur.fetchone()["rowid"]
        try:
            cur.execute(
                "INSERT INTO records_fts(records_fts, rowid, id, title, body, citation, type) "
                "VALUES('delete', ?, ?, ?, ?, ?, ?)",
                (old_rowid, rec["id"], rec["title"], rec["body"] or "", rec["citation"], rec["type"]),
            )
        except sqlite3.OperationalError:
            pass
        cur.execute("UPDATE records SET body = ?, source_hash = ? WHERE id = ?",
                    (body, body_hash, rid))
        cur.execute("""
            INSERT INTO records_fts(rowid, id, title, body, citation, type)
            SELECT rowid, id, title, body, citation, type FROM records WHERE id = ?
        """, (rid,))
        conn.commit()
        print(f"  OK ({source}, body_len={len(body)})")
        repaired.append({"id": rid, "url": url, "source": source, "body_len": len(body)})
        time.sleep(1.0)

    cur.execute("SELECT COUNT(*) FROM records")
    rcount = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM records_fts")
    fcount = cur.fetchone()[0]
    print(f"\nrecords={rcount}, records_fts={fcount}")
    try:
        cur.execute("PRAGMA quick_check")
        qc = cur.fetchone()[0]
    except Exception as e:
        qc = f"error: {e}"
    print(f"quick_check: {qc}")

    result = {
        "batch": BATCH,
        "repaired": repaired,
        "failed": failed,
        "remaining_after": len(targets) - len(repaired),
        "records_count": rcount,
        "fts_count": fcount,
        "quick_check": qc,
        "elapsed_sec": int(now_sec()),
    }
    (TMP_DIR / "result.json").write_text(json.dumps(result, indent=2))
    print(f"\nSummary: repaired={len(repaired)} failed={len(failed)}")
    conn.close()
    return result


if __name__ == "__main__":
    main()
