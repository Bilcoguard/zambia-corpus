#!/usr/bin/env python3
"""Repair worker batch 004 — fixes up to 8 corrupted Act/SI bodies.

Follows SKILL.md repair worker spec (2026-05-07 tick).
TMPDIR-routed atomic copy to work around FUSE journal limitations.
"""
import os, sys, re, time, json, sqlite3, ssl, glob, shutil, tempfile, urllib.request, urllib.error
from datetime import datetime, timezone

# Build SSL context using system trust + scripts/certs/*.pem
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

WORKDIR = "/sessions/admiring-elegant-shannon/mnt/corpus"
PDF_DIR = "/tmp/repair-batch-004-pdfs"
DB = os.path.join(WORKDIR, "corpus.sqlite")
GAPS = os.path.join(WORKDIR, "gaps.md")
LOG = os.path.join(WORKDIR, "worker.log")
HEADERS = {'User-Agent': 'KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)'}

# Full MANIFEST in order — script will check each in order and pick the first 8 still-corrupted
MANIFEST = [
    ("act-zm-2026-001-teaching-profession-act","https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%201%20OF%202026%2C%20The%20Teaching%20Professions.pdf"),
    ("act-zm-2023-021-the-competition-and-consumer-protection-amendment-act-2023","https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2021%20of%202023%2C%20The%20Competition%20and%20Consumer%20Protection%20%28Amendment%29.pdf"),
    ("act-zm-2026-005-national-payment-system-act","https://www.parliament.gov.zm/sites/default/files/documents/acts/National%20Payment%20System%20Act%20No.%205%20of%202026.pdf"),
    ("act-zm-2025-002-geological-minerals-development-2025","https://www.parliament.gov.zm/sites/default/files/documents/acts/Acts%20No.%202%20of%202025%2C%20The%20Geological%20Minerals%20Development.pdf"),
    ("act-zm-2025-026-zambia-national-broadcasting-corporation-act","https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2026%20of%202025%2C%20The%20Zambia%20National%20%20Broadcasting%20Corporation%20Act-2.pdf"),
    ("act-zm-2026-009-banking-and-financial-services-act","https://www.parliament.gov.zm/sites/default/files/documents/acts/Banking%20and%20Finance%20Act%2C%202026.pdf"),
    ("act-zm-2026-010-the-state-owned-enterprise-act-2026-act-no-10-of-2026","https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20State-Owned%20Enterprise%20Act%2C%202026.pdf"),
    ("act-zm-financial-intelligence-centre-act-2010","https://zambialii.org/akn/zm/act/2010/46/eng@2010-11-29/source.pdf"),
    ("act-zm-2023-024-the-access-to-information-act-2023-act-no-24-of-2023","https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2024%20of%202023%2C%20The%20Access%20to%20Information%20Act%2C%202023.pdf"),
    ("act-zm-2026-007-agricultural-credits-and-warehouse-receipts-act","https://www.parliament.gov.zm/sites/default/files/documents/acts/THE%20AGRICULTURAL%20CREDITS%20AND%20WAREHOUSE%20RECEIPTSACT%20No.%207%20OF%202026%2C.pdf"),
    ("act-zm-2011-014-tolls-act-2011","https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20Tolls%20%20Act%2C%202011.pdf"),
    ("act-zm-2024-004-human-rights-commission-act-2024","https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20Human%20Rights%20Commission%20Act%20No.%204%20of%202024.pdf"),
    ("act-zm-2026-006-food-reserve-act","https://www.parliament.gov.zm/sites/default/files/documents/acts/Food%20Reserve%20Agency%20Act%2C%202026.pdf"),
    ("act-zm-2026-003-immigration-control-act","https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20Immigration%20Control%20Act%2C%202026.pdf"),
    ("act-zm-2024-008-zambia-qualifications-authority-act-2024","https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20Zambia%20Qualification%20Authority%20Act%20%208%20of%202024.pdf"),
    ("act-zm-2025-001-plant-health-2025","https://www.parliament.gov.zm/sites/default/files/documents/acts/Acts%20No.%201%20of%202025%2C%20The%20Plant%20Health.pdf"),
    ("act-zm-2025-029-zambia-institute-of-procurement-and-supply-act","https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2029%20of%202025%2C%20The%20Zambia%20Institute%20of%20Procurement%20and%20Supply%20Act.pdf"),
    ("act-zm-2016-002-constitution-2016","https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/Constitution%20of%20Zambia%20%20%28Amendment%29%2C%202016-Act%20No.%202_0.pdf"),
    ("act-zm-2026-008-agricultural-marketing-act","https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20Agricultural%20Marketing%20Act%20No.%208%2C%202026.pdf"),
    ("act-zm-2010-027-the-animal-health","https://www.parliament.gov.zm/sites/default/files/documents/acts/Animal%20Health%20act.pdf"),
    ("act-zm-2025-023-companies-amendment-act","https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2023%20of%202025%2C%20The%20Companies%20%28Amendment%29.pdf"),
    ("act-zm-2025-008-border-management-trade-facilitation-act2025","https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%208%20of%202025%20-%20The%20Border%20Management%20and%20Trade%20Facilitation%20Act%20.pdf"),
    ("act-zm-2024-030-antiterrorism-nonproliferation-2024","https://www.parliament.gov.zm/sites/default/files/documents/acts/Acts%20No.%2030%20for%202024%2C%20The%20Ant-Terrorism%20and%20Non-Proliferation%2C%20pdf.pdf"),
    ("act-zm-2025-003-cyber-security-2025","https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%203%20of%202025%2C%20The%20Cyber%20Security_0.pdf"),
    ("act-zm-2026-011-the-zambia-deposit-insurance-corporation-act-2026-act-no-11-of-2026","https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20Zambia%20Deposit%20Insurance%20coporaion%20act%2C%202026.pdf"),
    ("act-zm-2010-034-the-national-prosecution-authority-act-2010","https://www.parliament.gov.zm/sites/default/files/documents/acts/National%20Prosecution%20Authority%20Act%202010.pdf"),
    ("act-zm-2023-017-the-public-procurement-amendment-act-2023","https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2017%20of%202023%2C%20The%20Public%20Procurement.pdf"),
    ("act-zm-2024-001-constituency-development-fund-act-2024","https://www.parliament.gov.zm/sites/default/files/documents/acts/ACT%20No.%201%20OF%202024%2C%20THE%20CONSTITUENCY%20DEVELOPMENT%20FUND.pdf"),
    ("act-zm-2025-025-independent-broadcasting-authority-act","https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2025%20of%202025%2C%20The%20%20Independent%20Broadcasting%20Authority%20Act-2.pdf"),
    ("act-zm-2025-004-cyber-crime-2025","https://www.parliament.gov.zm/sites/default/files/documents/acts/Acts%20No.%204%20of%202025%2C%20The%20Cyber%20Crimes.pdf"),
    ("act-zm-2011-013-the-zambia-qualifications-authority-act-2011","https://www.parliament.gov.zm/sites/default/files/documents/acts/Zambia_Qualifications_Authority_Act11-1.pdf"),
    ("act-zm-2011-023-education-act-2011","https://www.parliament.gov.zm/sites/default/files/documents/acts/Education%20Act%202011.pdf"),
    ("act-zm-2011-031-customs-and-excise-amendment-act-2011","https://www.parliament.gov.zm/sites/default/files/documents/amendment_act/The%20Customs%20and%20Excise%20%28Amendment%29%20Act%2C%202011.pdf"),
    ("act-zm-2010-024-the-competition-and-consumer-protection-2010","https://www.parliament.gov.zm/sites/default/files/documents/acts/The%20Competition%20and%20Consumer%20Protection%202010.pdf"),
    ("act-zm-2011-004-urban-and-regional-act-2011","https://www.parliament.gov.zm/sites/default/files/documents/acts/Urban_and_Regional_Act_2011%20No.%204%20of%202011.pdf"),
    ("act-zm-2023-018-the-public-private-partnership-act-2023","https://www.parliament.gov.zm/sites/default/files/documents/acts/Act%20No.%2018%20of%202023%2C%20The%20Public-Private%20Partnership.pdf"),
    ("act-zm-2024-010-civil-aviation-authority-amendment-act-2024","https://zambialii.org/akn/zm/act/2024/10/eng@2024-08-16/source.pdf"),
    ("act-zm-2024-011-civil-aviation-amendment-act-2024","https://zambialii.org/akn/zm/act/2024/11/eng@2024-08-16/source.pdf"),
    ("act-zm-2016-005-civil-aviation-act-2016","https://zambialii.org/akn/zm/act/2016/5/eng@2016-01-06/source.pdf"),
    ("si-zm-financial-intelligence-centre-prescribed-threshold-regulations-2022","https://zambialii.org/akn/zm/act/si/2022/53/eng@2022-08-19/source.pdf"),
    ("si-zm-financial-intelligence-centre-general-regulations-2022","https://zambialii.org/akn/zm/act/si/2022/54/eng@2022-08-19/source.pdf"),
    ("si-zm-financial-intelligence-centre-general-regulations-2016","https://zambialii.org/akn/zm/act/si/2016/9/eng@2016-01-29/source.pdf"),
]

import pdfplumber

MAX_BATCH_SIZE = 8
BATCH_LABEL = "004"


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def gap(record_id, reason, url):
    line = f"| {record_id} | REPAIR | {reason} | {url} | {now_iso()} |\n"
    with open(GAPS, "a") as f:
        f.write(line)


def is_corrupted(body):
    if body is None or not body.strip():
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
    return True, "OK"


def normalise_sections(text):
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


def download_pdf(url, dest):
    req = urllib.request.Request(url, headers=HEADERS)
    with OPENER.open(req, timeout=90) as r:
        data = r.read()
    with open(dest, "wb") as f:
        f.write(data)
    return data


def extract_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text


def main():
    os.makedirs(PDF_DIR, exist_ok=True)
    # TMPDIR-routed atomic copy pattern (FUSE journal limitations)
    tmp_root = tempfile.mkdtemp(prefix=f"repair_batch_{BATCH_LABEL}_")
    tmp_db = os.path.join(tmp_root, "corpus.sqlite")
    shutil.copy2(DB, tmp_db)
    conn = sqlite3.connect(tmp_db)
    c = conn.cursor()

    # Pre-flight: integrity
    c.execute("PRAGMA integrity_check")
    integ = c.fetchone()
    print(f"PRE integrity: {integ}")
    if integ != ("ok",):
        print("ABORT: pre-flight integrity not OK")
        conn.close()
        return 2

    # Identify still-corrupted in MANIFEST order
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

    print(f"Queue ({len(queue)}):")
    for rid, _ in queue:
        print(f"  - {rid}")

    results = []
    fetches = 0
    successes = 0

    for i, (rid, url) in enumerate(queue):
        # Rate limit: 2s between downloads (not before the first)
        if i > 0:
            time.sleep(2)

        pdf_path = os.path.join(PDF_DIR, f"{rid}.pdf")
        try:
            print(f"[{i+1}/{len(queue)}] Fetching {rid}...")
            data = download_pdf(url, pdf_path)
            fetches += 1
        except urllib.error.HTTPError as e:
            results.append({"rid": rid, "status": "fail", "reason": f"http_{e.code}", "url": url})
            gap(rid, f"HTTP_{e.code}", url)
            fetches += 1
            print(f"  -> HTTP {e.code}")
            continue
        except Exception as e:
            results.append({"rid": rid, "status": "fail", "reason": f"download_error:{type(e).__name__}:{str(e)[:120]}", "url": url})
            gap(rid, f"DOWNLOAD_ERR:{type(e).__name__}", url)
            print(f"  -> err {type(e).__name__}: {e}")
            continue

        if not data.startswith(b"%PDF-"):
            results.append({"rid": rid, "status": "fail", "reason": "NOT_A_PDF", "size": len(data), "url": url})
            gap(rid, "NOT_A_PDF", url)
            print(f"  -> NOT_A_PDF ({len(data)} bytes)")
            continue

        try:
            text = extract_text(pdf_path)
        except Exception as e:
            results.append({"rid": rid, "status": "fail", "reason": f"extract_error:{type(e).__name__}:{str(e)[:120]}", "url": url})
            gap(rid, f"EXTRACT_ERR:{type(e).__name__}", url)
            print(f"  -> extract err {type(e).__name__}: {e}")
            continue

        if len(text) < 200:
            # OCR fallback - not available
            results.append({"rid": rid, "status": "fail", "reason": f"scanned_pdf_ocr_unavailable:{len(text)}chars", "url": url})
            with open(LOG, "a") as f:
                f.write(f"{now_iso()}\trepair-batch-{BATCH_LABEL}\tocrmypdf not available - deferred {rid}\n")
            gap(rid, f"OCR_UNAVAILABLE:{len(text)}chars", url)
            print(f"  -> OCR needed (only {len(text)}c extracted), deferred")
            continue

        text = normalise_sections(text)
        ok, qreason = quality_pass(text)
        if not ok:
            results.append({"rid": rid, "status": "fail", "reason": qreason, "chars": len(text), "url": url})
            gap(rid, qreason, url)
            print(f"  -> quality fail: {qreason}")
            continue

        # Update DB
        c.execute("UPDATE records SET body=? WHERE id=?", (text, rid))
        if c.rowcount != 1:
            results.append({"rid": rid, "status": "fail", "reason": f"update_rowcount:{c.rowcount}", "url": url})
            print(f"  -> update rowcount {c.rowcount} (expected 1)")
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
        results.append({"rid": rid, "status": "ok", "chars": len(text), "pdf_bytes": len(data), "url": url})
        print(f"  -> OK ({len(text)}c body, {len(data)}B PDF)")

    # Integrity check
    c.execute("SELECT COUNT(*) FROM records")
    rec_count = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM records_fts")
    fts_count = c.fetchone()[0]
    integrity_ok = (rec_count == fts_count)

    # Post-mutation integrity_check
    c.execute("PRAGMA integrity_check")
    post_integ = c.fetchone()
    print(f"POST integrity: {post_integ}")

    out = {
        "ts": now_iso(),
        "batch": BATCH_LABEL,
        "queue_size": len(queue),
        "fetches": fetches,
        "successes": successes,
        "results": results,
        "rec_count": rec_count,
        "fts_count": fts_count,
        "integrity_ok": integrity_ok and post_integ == ("ok",),
        "post_integ": post_integ[0] if post_integ else None,
    }
    conn.close()
    if out["integrity_ok"] and successes > 0:
        # Atomic copy back to FUSE
        shutil.copy2(tmp_db, DB)
        out["db_synced"] = True
    else:
        out["db_synced"] = False
        if not out["integrity_ok"]:
            out["INTEGRITY_FAIL"] = True
    shutil.rmtree(tmp_root, ignore_errors=True)
    print()
    print(json.dumps(out, indent=2))

    # Persist run log
    with open(os.path.join(WORKDIR, f"_repair_batch_{BATCH_LABEL}_result.json"), "w") as f:
        json.dump(out, f, indent=2)

    return 0 if out["integrity_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
