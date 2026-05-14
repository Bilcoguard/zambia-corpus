#!/usr/bin/env python3
"""
Repair batch 0652 — fix 5 manifest acts whose body rows return
DatabaseError/UTF-8 errors on read. Re-fetches each PDF from
parliament.gov.zm, extracts text, and UPDATEs the body field with
journal_mode=MEMORY (body-only — no FTS touch to preserve parity rule).

CA cert: RapidSSL G1 (Python's certifi bundle lacks it).
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
CACERT = "/sessions/modest-optimistic-dijkstra/mnt/corpus/scripts/certs/rapidssl_tls_rsa_ca_g1.pem"
CRAWL_DELAY = 5
PARSER_VERSION = "repair-0.6.2"

# 5 manifest acts that returned DatabaseError or UTF-8 errors on read.
TARGETS = [
    ("act-zm-2012-013-property-transfer-tax-amendment-act-2012",
     "https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Property%20Transfer%20tax%20%28Amendment%29%2C%202012.PDF"),
    ("act-zm-2021-028-the-engineering-institution-of-zambia-amendment-act-2021",
     "https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2028%20of%202021%2C%20The%20Engineering%20Institution%20of%20Zambia%20%28Amendment%29%202021_0.pdf"),
    ("act-zm-2021-030-the-chartered-institute-of-logistics-and-transport-amendment-act-2021",
     "https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2030%20OF%202021%2C%20THE%20ZAMBIA%20CHARTERED%20INSTITUTE%20OF%20LOGISTICS%20AND%20TRANSPORT%20%28AMENDMENT%29pdf_0.pdf"),
    ("act-zm-2023-022-the-income-tax-amendment-act-2023",
     "https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2022%20of%202023%2C%20The%20Income%20Tax%20%28Amendment%29.pdf"),
    ("act-zm-2023-025-the-customs-and-excise-amendment-act-2023-act-no-25-of-2023",
     "https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2025%20of%202023%2C%20The%20Customs%20and%20Excise%20%28Amendment%29.pdf"),
]


def fetch_pdf(url, dest_path):
    cmd = [
        "curl", "-sS", "-L",
        "--cacert", CACERT,
        "-A", UA,
        "--max-time", "90",
        "-o", dest_path,
        url,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl failed for {url}: {r.stderr.strip()}")
    return dest_path


def extract_pdf_text(pdf_path):
    import pdfplumber
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text() or ""
            pages.append(t)
    body = "\n\n".join(pages).strip()
    # Normalise concatenated section numbers like "5.A" -> "5. A"
    body = re.sub(r"(\d+)\.([A-Z])", r"\1. \2", body)
    return body


def quality_gate(body):
    if len(body) < 200:
        return False, f"body-too-short({len(body)})"
    lines = body.strip().split("\n")
    digit_lines = sum(1 for l in lines if l.strip().isdigit())
    if digit_lines > len(lines) * 0.5 and len(lines) > 10:
        return False, f"line-numbers-only(digit={digit_lines}/total={len(lines)})"
    markers = re.search(
        r"\b(Act|Regulations|section|Order|Statutory Instrument|By-Laws|Rules|Notice|enacted|Parliament)\b",
        body,
    )
    if not markers:
        return False, "no-legal-markers"
    return True, "ok"


def repair_one(rec_id, url, i):
    pdf_path = os.path.join(WORKDIR, f"{i:02d}_{rec_id[:40]}.pdf")
    fetch_pdf(url, pdf_path)
    size = os.path.getsize(pdf_path)
    if size < 1000:
        return False, 0, None, f"pdf-too-small({size}B)"
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
    for i, (tid, url) in enumerate(TARGETS, 1):
        try:
            ok, n, sha8, note = repair_one(tid, url, i)
            results.append((tid, ok, n, sha8, note))
            print(f"[{i}/{len(TARGETS)}] {tid}: {'OK' if ok else 'FAIL'} bytes={n} sha8={sha8} ({note})", flush=True)
        except Exception as e:
            results.append((tid, False, 0, None, f"exception:{type(e).__name__}:{e}"))
            print(f"[{i}/{len(TARGETS)}] {tid}: EXCEPTION {type(e).__name__}: {e}", flush=True)

    print("\nSUMMARY:")
    ok_count = sum(1 for r in results if r[1])
    total_bytes = sum(r[2] for r in results if r[1])
    print(f"  OK: {ok_count}/{len(results)}")
    print(f"  Total body bytes written: {total_bytes}")
    chain = "+".join(r[3] for r in results if r[1] and r[3])
    print(f"  SHA256(8) chain: {chain}")
    return results


if __name__ == "__main__":
    main()
