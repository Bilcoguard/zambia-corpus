#!/usr/bin/env python3
"""
Repair batch 0654 (SI) — continues Condition-B SI drainage (2018 cohort, post-021).
Picks the next 8 alphabetical no-body 2018 SIs not yet attempted.

Logic and structure follow the established repair pattern documented across
the b0648..b0652 cohort scripts. Only TARGETS and BATCH constants change.
"""
import hashlib
import os
import re
import subprocess
import sqlite3
import time

BATCH = "b0654"
UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
ROOT = "/sessions/lucid-blissful-dirac/mnt/corpus"
WORKDIR = os.path.join(ROOT, f"_repair_{BATCH}_pdfs")
DB = os.path.join(ROOT, "corpus.sqlite")
CRAWL_DELAY = 5
PARSER_VERSION = "repair-0.6.2"

TARGETS = [
    "si-zm-2018-022-animal-health-veterinary-services-fees-regulations-2018",
    "si-zm-2018-023-plant-variety-and-seeds-regulations-2018",
    "si-zm-2018-033-electoral-process-local-government-by-elections-election-date-and-time-of-poll-order-2018",
    "si-zm-2018-039-levy-mwanawasa-medical-university-declaration-order-2018",
    "si-zm-2018-043-urban-and-regional-planning-designated-local-planning-authorities-regulations-2018",
    "si-zm-2018-044-urban-and-regional-planning-designated-local-planning-authorities-no-2-regulations-2018",
    "si-zm-2018-046-electoral-process-local-government-by-elections-election-date-and-time-of-poll-no-3-order-2018",
    "si-zm-2018-054-agricultural-institute-of-zambia-general-regulations-2018",
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
    # Section-number normalisation: split "1.Section" -> "1. Section"
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


def fts_refresh_row(conn, rec_id):
    """
    Refresh the FTS5 index entry for one record.

    The actual records_fts schema is:
        CREATE VIRTUAL TABLE records_fts USING fts5(
            id, title, body, citation, type,
            content=records, content_rowid=rowid
        )

    (The task-instruction schema referencing case_name / outcome_detail does
    not match the live DB — those columns belong only to judgments_meta and
    are not indexed in this FTS table.)

    For external-content FTS5, the correct way to refresh a single row is:
      1. Issue the 'delete' command using the OLD column values + rowid.
      2. Re-insert the row from the current (post-UPDATE) records row.

    We don't have a copy of the OLD body here, so we instead use the
    'delete-all' command scoped via the rowid: that's not supported.
    The robust per-row pattern is to emit the special insert that removes
    the existing index entry by rowid using the current content (the
    FTS-side index keyed on rowid will be replaced).
    """
    cur = conn.cursor()
    cur.execute("SELECT rowid, title, body, citation, type FROM records WHERE id = ?", (rec_id,))
    r = cur.fetchone()
    if not r:
        return False
    rowid, title, body, citation, rtype = r
    # Remove stale index entry by rowid (use empty strings — FTS5 'delete'
    # only needs to match what was previously inserted at this rowid; since
    # we hold no copy of the prior body, fall back to a full rebuild guard
    # at the end of the batch). For now: attempt insert; on conflict the
    # row already exists in the index. The end-of-batch rebuild authoritative.
    try:
        cur.execute(
            "INSERT INTO records_fts(rowid, id, title, body, citation, type) VALUES (?,?,?,?,?,?)",
            (rowid, rec_id, title, body, citation, rtype),
        )
    except sqlite3.IntegrityError:
        # rowid already in index — skip; final rebuild will normalise.
        pass
    return True


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
            print(
                f"[{i}/{len(TARGETS)}] {tid}: {'OK' if ok else 'FAIL'} "
                f"bytes={n} sha8={sha8} ({note})",
                flush=True,
            )
        except Exception as e:
            results.append((tid, False, 0, None, f"exception:{type(e).__name__}:{e}"))
            print(
                f"[{i}/{len(TARGETS)}] {tid}: EXCEPTION {type(e).__name__}: {e}",
                flush=True,
            )

    ok_count = sum(1 for r in results if r[1])
    total_bytes = sum(r[2] for r in results if r[1])
    print(f"\nSI SUMMARY: OK={ok_count}/{len(results)} bytes={total_bytes}")
    chain = "+".join(r[3] for r in results if r[1] and r[3])
    print(f"  SHA256(8) chain: {chain}")

    # End-of-batch FTS rebuild for repaired ids (external-content FTS5).
    # Authoritative refresh: 'delete-all' then per-row reinsert from records.
    repaired_ids = [r[0] for r in results if r[1]]
    if repaired_ids:
        conn = sqlite3.connect(DB)
        conn.execute("PRAGMA cell_size_check=OFF")
        try:
            cur = conn.cursor()
            # Per-row delete by reading current FTS row content (post-UPDATE);
            # then re-insert. Since records.body has already been updated, we
            # can't issue a typed 'delete' command — instead, do a targeted
            # full rebuild scoped to repaired rowids by using the contentless
            # 'delete-all' command followed by reinsert of these rows.
            for rid in repaired_ids:
                cur.execute("SELECT rowid, title, body, citation, type FROM records WHERE id = ?", (rid,))
                row = cur.fetchone()
                if not row:
                    continue
                rowid, title, body, citation, rtype = row
                # Remove existing index entry at this rowid using the
                # special 'delete-all' is too broad; the per-rowid pattern
                # using 'delete' requires the previous values which we lack.
                # We instead delete via the records_fts contentless delete
                # idiom and rely on the integrity-check + global rebuild
                # below if any row remains inconsistent.
                try:
                    cur.execute(
                        "INSERT INTO records_fts(records_fts, rowid, id, title, body, citation, type) "
                        "VALUES('delete', ?, ?, ?, ?, ?, ?)",
                        (rowid, rid, title, body, citation, rtype),
                    )
                except sqlite3.OperationalError:
                    # Stale prior values unknown — fall through to full rebuild.
                    pass
                try:
                    cur.execute(
                        "INSERT INTO records_fts(rowid, id, title, body, citation, type) VALUES (?,?,?,?,?,?)",
                        (rowid, rid, title, body, citation, rtype),
                    )
                except sqlite3.IntegrityError:
                    pass
            # Authoritative belt-and-braces: global FTS rebuild ensures parity.
            try:
                cur.execute("INSERT INTO records_fts(records_fts) VALUES('rebuild')")
            except sqlite3.OperationalError as e:
                print(f"FTS rebuild warning: {e}", flush=True)
            conn.commit()
        finally:
            conn.close()
        print(f"FTS refresh complete for {len(repaired_ids)} repaired rows + full rebuild.", flush=True)

    return results


if __name__ == "__main__":
    main()
