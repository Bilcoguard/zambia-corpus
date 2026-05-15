#!/usr/bin/env python3
"""Repair worker tick — fixes broken SI/act records.

Honours:
 - MAX_BATCH_SIZE = 8
 - 20-min wall clock
 - User-Agent: KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)
 - Uses scripts/certs/rapidssl_tls_rsa_ca_g1.pem for parliament.gov.zm
"""
from __future__ import annotations
import os, sys, time, json, hashlib, re, sqlite3, subprocess, tempfile, traceback
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path('/sessions/wonderful-admiring-fermat/mnt/corpus')
DB = ROOT / 'corpus.sqlite'
CERT = ROOT / 'scripts/certs/rapidssl_tls_rsa_ca_g1.pem'
UA = 'KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)'
MAX_BATCH = 8
TICK_LIMIT_S = 20 * 60 - 90  # leave ~90s for git/commit/push
PER_RECORD_LIMIT_S = 180

START = time.time()
LOG_LINES = []
GAP_LINES = []
COST_LINES = []
REPAIRED = []

def log(msg: str):
    ts = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    line = f'[{ts}] [repair-b0652] {msg}'
    print(line, flush=True)
    LOG_LINES.append(line)

def gap(rid: str, reason: str):
    ts = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    GAP_LINES.append(f'- {ts} | {rid} | {reason}')


def time_left() -> float:
    return TICK_LIMIT_S - (time.time() - START)


def curl_get(url: str, out: Path, timeout: int = 60) -> tuple[int, int]:
    cmd = [
        'curl', '-A', UA, '--cacert', str(CERT), '-L', '-sS',
        '--max-time', str(timeout),
        '-o', str(out), '-w', '%{http_code} %{size_download}',
        url,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 30)
        out_text = (proc.stdout or '').strip().split()
        if len(out_text) >= 2:
            return int(out_text[0]), int(out_text[1])
        return 0, 0
    except Exception as exc:  # noqa: BLE001
        log(f'curl failed for {url}: {exc}')
        return 0, 0


def extract_pdf_text(pdf_path: Path) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            text = '\n'.join((p.extract_text() or '') for p in pdf.pages)
        return text
    except Exception as exc:  # noqa: BLE001
        log(f'pdfplumber failed on {pdf_path}: {exc}')
        return ''


def ocr_pdf(pdf_path: Path) -> Path | None:
    out = pdf_path.with_suffix('.ocr.pdf')
    try:
        subprocess.run(
            ['ocrmypdf', '--force-ocr', '--skip-big', '500', '--quiet', str(pdf_path), str(out)],
            check=True, timeout=PER_RECORD_LIMIT_S,
        )
        return out if out.exists() else None
    except Exception as exc:  # noqa: BLE001
        log(f'ocrmypdf failed on {pdf_path}: {exc}')
        return None


def normalise_sections(text: str) -> str:
    """Lightweight section-number normalisation.
    Splits things like '1.Thisrule' -> '1. This rule' and breaks long
    digit-only runs like '1234' that appear glued to text only when the
    pattern is clearly a stuck section header. Conservative.
    """
    if not text:
        return text
    # insert a space after a section-number followed by a capital letter when
    # there's no whitespace separator
    text = re.sub(r'(?m)(^\s*\d+\.)([A-Z])', r'\1 \2', text)
    # collapse 3+ blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


def quality_gate(text: str) -> tuple[bool, str]:
    if not text or len(text) < 200:
        return False, f'short ({len(text or "")} chars)'
    lines = text.strip().split('\n')
    digit_lines = sum(1 for l in lines if l.strip().isdigit())
    if len(lines) > 10 and digit_lines > len(lines) * 0.5:
        return False, 'line-numbers-only'
    lower = text.lower()
    markers = ['act', 'section', 'order', 'regulation', 'rule', 'enacted', 'instrument', 'minister', 'commission', 'gazette', 'republic']
    if not any(m in lower for m in markers):
        return False, 'no-legal-markers'
    return True, 'ok'


def fetch_html(url: str, out: Path) -> bool:
    code, size = curl_get(url, out, timeout=45)
    return code == 200 and size > 0


def find_pdf_link_in_html(html_path: Path, base_url: str) -> str | None:
    try:
        from bs4 import BeautifulSoup
    except Exception:
        log('bs4 not available')
        return None
    try:
        html = html_path.read_text(errors='replace')
    except Exception:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    # Highest priority: source.pdf style links
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.lower().endswith('.pdf'):
            if href.startswith('//'):
                href = 'https:' + href
            elif href.startswith('/'):
                p = urlparse(base_url)
                href = f'{p.scheme}://{p.netloc}{href}'
            return href
    return None


def repair_record(rid: str, url: str, conn: sqlite3.Connection) -> bool:
    """Attempt to repair one record. Returns True on success."""
    log(f'repair START {rid} <- {url}')
    t0 = time.time()
    work = Path(tempfile.mkdtemp(prefix='repair_'))
    try:
        pdf_path: Path | None = None
        text = ''

        if url.lower().endswith('.pdf'):
            pdf_path = work / 'doc.pdf'
            code, size = curl_get(url, pdf_path)
            if code != 200 or size < 1000:
                gap(rid, f'pdf fetch failed http={code} size={size} url={url}')
                return False
        elif 'zambialii.org' in url or 'laws.africa' in url:
            # First try: fetch HTML to find linked PDF
            html_path = work / 'page.html'
            if not fetch_html(url, html_path):
                gap(rid, f'html fetch failed url={url}')
                return False
            pdf_link = find_pdf_link_in_html(html_path, url)
            if pdf_link:
                pdf_path = work / 'doc.pdf'
                code, size = curl_get(pdf_link, pdf_path)
                if code != 200 or size < 1000:
                    gap(rid, f'linked pdf fetch failed http={code} size={size} url={pdf_link}')
                    return False
            else:
                # Try the conventional /source.pdf endpoint
                guess = url.rstrip('/') + '/eng@/source.pdf'
                # Better: just append /source.pdf if URL looks akn
                if '/akn/' in url:
                    guess = url.rstrip('/') + '/source.pdf'
                pdf_path = work / 'doc.pdf'
                code, size = curl_get(guess, pdf_path)
                if code != 200 or size < 1000:
                    # extract from html as fallback
                    try:
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(html_path.read_text(errors='replace'), 'html.parser')
                        body_div = soup.select_one('.akn-act, [class*="akn-"], .document-content')
                        if body_div:
                            text = body_div.get_text(' ', strip=True)
                    except Exception:
                        pass
                    if not text or len(text) < 200:
                        gap(rid, f'no usable pdf or html body for {url}')
                        return False
        elif 'parliament.gov.zm' in url:
            pdf_path = work / 'doc.pdf'
            code, size = curl_get(url, pdf_path)
            if code != 200 or size < 1000:
                gap(rid, f'parl pdf fetch failed http={code} size={size} url={url}')
                return False
        else:
            gap(rid, f'unknown url scheme: {url}')
            return False

        if pdf_path and pdf_path.exists() and not text:
            text = extract_pdf_text(pdf_path)
            if len(text.strip()) < 200:
                log(f'low-text extract ({len(text)} chars) — running OCR fallback')
                ocred = ocr_pdf(pdf_path)
                if ocred:
                    text = extract_pdf_text(ocred)

        text = normalise_sections(text)

        ok, reason = quality_gate(text)
        if not ok:
            gap(rid, f'quality gate: {reason}')
            return False

        # Persist
        src_hash = hashlib.sha256(text.encode('utf-8', errors='replace')).hexdigest()
        cur = conn.cursor()
        cur.execute('UPDATE records SET body=?, source_hash=? WHERE id=?', (text, src_hash, rid))
        # Rebuild FTS for this record. Schema: records_fts(id, title, body, citation, type)
        # content=records, content_rowid=rowid — keep rowid aligned with records.rowid.
        cur.execute('SELECT rowid FROM records WHERE id=?', (rid,))
        row = cur.fetchone()
        if row is None:
            gap(rid, 'rowid lookup failed after update')
            return False
        rec_rowid = row[0]
        cur.execute('DELETE FROM records_fts WHERE rowid=?', (rec_rowid,))
        cur.execute(
            '''INSERT INTO records_fts (rowid, id, title, body, citation, type)
               SELECT rowid, id, title, body, citation, type
               FROM records WHERE id=?''',
            (rid,),
        )
        conn.commit()
        elapsed = time.time() - t0
        log(f'repair OK {rid} chars={len(text)} elapsed={elapsed:.1f}s')
        REPAIRED.append((rid, len(text), round(elapsed, 1), url))
        COST_LINES.append(f'{rid} | bytes={len(text)} | seconds={elapsed:.1f}')
        return True
    finally:
        try:
            for p in work.iterdir():
                p.unlink(missing_ok=True)
            work.rmdir()
        except Exception:
            pass


def main():
    os.chdir(ROOT)
    if not DB.exists():
        log(f'no database at {DB}')
        return 1
    if not CERT.exists():
        log(f'cert missing at {CERT}')
        return 1

    conn = sqlite3.connect(str(DB), timeout=60)
    cur = conn.cursor()
    # Disk-journal creation fails on this filesystem (operation-not-permitted on
    # journal removal — see b0654/b0656 .bak files). MEMORY journal mode avoids
    # the issue. Each repair is wrapped in commit() so the at-risk window per
    # record is sub-second.
    cur.execute('PRAGMA journal_mode=MEMORY')
    cur.execute('PRAGMA synchronous=NORMAL')
    cur.execute('PRAGMA busy_timeout=30000')

    # Identify repair targets — only acts and SIs with empty body
    # (judgments are handled by another worker; the previous diagnostic showed 0 stub/0 corrupted in those types)
    cur.execute(
        """SELECT id, source_url FROM records
           WHERE (body IS NULL OR body='') AND type IN ('act','si')
           ORDER BY id"""
    )
    no_body = cur.fetchall()

    # Stub bodies (acts/sis only)
    cur.execute(
        """SELECT id, source_url FROM records
           WHERE type IN ('act','si') AND length(body) > 0 AND length(body) < 200
           ORDER BY id"""
    )
    stubs = cur.fetchall()

    # Corrupted bodies — line-numbers-only
    cur.execute(
        """SELECT id, source_url, body FROM records
           WHERE body IS NOT NULL AND body != '' AND length(body) > 10
             AND type IN ('act','si')"""
    )
    corrupted = []
    for rid, url, body in cur.fetchall():
        lines = body.strip().split('\n')
        digit_lines = sum(1 for l in lines if l.strip().isdigit())
        if digit_lines > len(lines) * 0.5 and len(lines) > 10:
            corrupted.append((rid, url))

    targets: list[tuple[str, str]] = []
    seen = set()
    for tlist in (corrupted, no_body, stubs):
        for rid, url in tlist:
            if rid in seen:
                continue
            seen.add(rid)
            targets.append((rid, url))

    log(f'repair candidates total={len(targets)} '
        f'(corrupted={len(corrupted)}, no_body={len(no_body)}, stubs={len(stubs)})')
    if not targets:
        log('All repair targets fixed — repair worker idle')
        Path('worker.log').open('a').write('All repair targets fixed — repair worker idle\n')
        return 0

    batch = targets[:MAX_BATCH]
    fixed = 0
    failed = 0
    for rid, url in batch:
        if time_left() < PER_RECORD_LIMIT_S:
            log(f'time guard hit (left={time_left():.0f}s) — stopping batch early')
            break
        try:
            ok = repair_record(rid, url, conn)
            if ok:
                fixed += 1
            else:
                failed += 1
        except Exception as exc:  # noqa: BLE001
            traceback.print_exc()
            gap(rid, f'unhandled exception: {exc}')
            failed += 1

    # Integrity check
    cur.execute('SELECT COUNT(*) FROM records'); n_rec = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM records_fts'); n_fts = cur.fetchone()[0]
    log(f'integrity records={n_rec} records_fts={n_fts}')
    if n_rec != n_fts:
        gap('-', f'records_fts mismatch records={n_rec} fts={n_fts}')

    try:
        cur.execute('PRAGMA quick_check').fetchall()
    except Exception as exc:  # noqa: BLE001
        gap('-', f'quick_check failed: {exc}')

    conn.close()

    # Write logs
    log(f'tick complete fixed={fixed} failed={failed} elapsed={time.time()-START:.1f}s')

    with open(ROOT / 'worker.log', 'a') as f:
        for line in LOG_LINES:
            f.write(line + '\n')
    if GAP_LINES:
        with open(ROOT / 'gaps.md', 'a') as f:
            f.write(f'\n## repair tick b0652 ({time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})\n')
            for g in GAP_LINES:
                f.write(g + '\n')
    if COST_LINES:
        with open(ROOT / 'costs.log', 'a') as f:
            f.write(f'\n# repair tick b0652 {time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}\n')
            for c in COST_LINES:
                f.write(c + '\n')

    # Batch report
    reports_dir = ROOT / 'reports'
    reports_dir.mkdir(exist_ok=True)
    report = reports_dir / f'repair_b0652_{int(START)}.md'
    with report.open('w') as f:
        f.write('# Repair batch b0652\n\n')
        f.write(f'- Started: {time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(START))}\n')
        f.write(f'- Candidates total: {len(targets)} (no_body={len(no_body)}, stubs={len(stubs)}, corrupted={len(corrupted)})\n')
        f.write(f'- Batch attempted: {len(batch)}\n')
        f.write(f'- Fixed: {fixed}\n')
        f.write(f'- Failed: {failed}\n\n')
        f.write('## Repaired records\n\n')
        for rid, blen, sec, url in REPAIRED:
            f.write(f'- `{rid}` — {blen} chars in {sec}s — {url}\n')
        if GAP_LINES:
            f.write('\n## Gaps logged this tick\n\n')
            for g in GAP_LINES:
                f.write(g + '\n')

    print(f'REPAIRED_COUNT={fixed}')
    print(f'REPORT={report}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
