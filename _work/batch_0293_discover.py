"""Batch 0293 — Phase 4 / final-letter alphabet exhaust + upstream-acts refresh.

Inherited closing state (from b0290 + b0291 + b0292):

  - acts_in_force: chronological-first sweep complete through 2026/11.
  - sis_corporate-modern: alphabets A,B,C,I,M,P,S,T,V probed (b0291) — empty.
  - sis_tax-modern: 3 candidates OCR-deferred (b0291).
  - sis_employment-modern: alphabets E,F,J,L,N,W probed (b0292) —
                           1 candidate (2022/13) OCR-deferred (already in OCR
                           backlog from b0184/0200/0205/0221).
  - sis_mining-modern: alphabet=M empty (b0291).
  - sis_family-modern: empty across F,J,L,M,W.
  - case_law_scz, sis_data_protection: at upstream steady state.

This tick closes the alphabet exhaust by probing the 7 remaining uncovered
high-yield letters (D, G, H, K, O, R, U) plus refreshing two upstream Act
sources (zambialii /legislation/recent and parliament /acts-of-parliament
page 0). 4 letters are intentionally omitted (Q, X, Y, Z — never have legal
listings on this jurisdiction).

Probe-only (zero record writes expected).

Outputs:
  _work/batch_0293_alphabet_<X>.html
  _work/batch_0293_zambialii_recent.html
  _work/batch_0293_parliament_p0.html
  _work/batch_0293_probe.json
"""
import sys, os, json, hashlib, time, urllib.request, re, glob, ssl
from datetime import datetime, timezone
from bs4 import BeautifulSoup

# Build SSL context with extra certs from scripts/certs/ (per fetch_one.py).
# Needed for parliament.gov.zm (RapidSSL chain not in default trust store).
EXTRA_CERTS_DIR = "scripts/certs"
SSL_CTX = ssl.create_default_context()
if os.path.isdir(EXTRA_CERTS_DIR):
    for pem in sorted(glob.glob(os.path.join(EXTRA_CERTS_DIR, "*.pem"))):
        try:
            SSL_CTX.load_verify_locations(cafile=pem)
        except Exception as e:
            print(f"WARN: failed to load {pem}: {e}", file=sys.stderr)
HTTPS_HANDLER = urllib.request.HTTPSHandler(context=SSL_CTX)
OPENER = urllib.request.build_opener(HTTPS_HANDLER)

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
ZLII_CRAWL = 6.0       # zambialii robots Crawl-delay 5s + 1s margin
PARLIA_CRAWL = 11.0    # parliament robots Crawl-delay 10s + 1s margin

ROBOTS_ZLII = "https://zambialii.org/robots.txt"
ROBOTS_PARL = "https://www.parliament.gov.zm/robots.txt"
EXPECTED_ROBOTS_ZLII = "fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0"
EXPECTED_ROBOTS_PARL = "278e83bcf567badfebcdea4d5d20ca9898e4449fe4eb2e3b5a08227b4ca9b762"

ALPHABETS = ['D', 'G', 'H', 'K', 'O', 'R', 'U']

# Sub-phase classifiers (priority_order items 2,3,4,7,8)
CORP_PAT = re.compile(
    r'\b(Companies|Co-?operatives?|Insurance|Securities|Banking|Pensions?|'
    r'Citizens\s+Economic\s+Empowerment|Public\s+Procurement|PACRA)\b',
    re.I,
)
TAX_PAT = re.compile(
    r'\b(Income\s+Tax|Value\s+Added\s+Tax|VAT|Customs|Excise|Property\s+Transfer|'
    r'Tax|Revenue|Duties)\b',
    re.I,
)
EMP_PAT = re.compile(
    r'\b(Employment|Labour|NAPSA|National\s+Pension|Workers[\']?\s+Compensation|'
    r'Workmen[\']?s\s+Compensation|Minimum\s+Wage|Industrial\s+(?:and\s+Labour\s+)?Relations|'
    r'Factories|Apprenticeship|Occupational\s+Health)\b',
    re.I,
)
MIN_PAT = re.compile(r'\b(Mines|Mining|Minerals?)\b', re.I)
FAM_PAT = re.compile(
    r'\b(Marriage|Matrimonial|Children|Juvenile|Maintenance|Adoption|Affiliation)\b',
    re.I,
)
DPA_PAT = re.compile(r'\b(Data\s+Protection|Cyber)\b', re.I)


def fetch(url, crawl):
    time.sleep(crawl)
    req = urllib.request.Request(url, headers=HEADERS)
    return OPENER.open(req, timeout=45).read()


def classify(title):
    if CORP_PAT.search(title):
        return 'sis_corporate'
    if TAX_PAT.search(title):
        return 'sis_tax'
    if EMP_PAT.search(title):
        return 'sis_employment'
    if MIN_PAT.search(title):
        return 'sis_mining'
    if FAM_PAT.search(title):
        return 'sis_family'
    if DPA_PAT.search(title):
        return 'sis_data_protection'
    return None


def log_cost(today, url, n, batch, kind):
    with open('costs.log', 'a') as f:
        f.write(json.dumps({'date': today, 'url': url,
                            'bytes': n, 'batch': batch,
                            'kind': kind}) + '\n')


def main():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    batch = '0293'

    # 1) Robots re-verify (zambialii)
    zlii_robots_path = '_work/batch_0293_zambialii_robots.txt'
    if os.path.exists(zlii_robots_path):
        robots = open(zlii_robots_path, 'rb').read()
        rsha = hashlib.sha256(robots).hexdigest()
        print(f"zambialii robots.txt sha256={rsha} (reused)")
    else:
        robots = fetch(ROBOTS_ZLII, ZLII_CRAWL)
        rsha = hashlib.sha256(robots).hexdigest()
        print(f"zambialii robots.txt sha256={rsha}")
        with open(zlii_robots_path, 'wb') as f:
            f.write(robots)
        log_cost(today, ROBOTS_ZLII, len(robots), batch, 'probe')
    assert rsha == EXPECTED_ROBOTS_ZLII, f"zambialii robots drift: {rsha}"

    # 2) Build existing on-disk SI + Act key sets
    sis_existing = set()
    for fp in glob.glob('records/sis/**/si-zm-*.json', recursive=True) + \
              glob.glob('records/sis/si-zm-*.json'):
        fn = os.path.basename(fp)
        m = re.match(r'si-zm-(\d{4})-(\d+)\.json', fn)
        if m:
            sis_existing.add((int(m.group(1)), int(m.group(2))))
    print(f"existing SI keys on disk: {len(sis_existing)}")

    acts_existing = set()
    for fp in glob.glob('records/acts/**/act-zm-*.json', recursive=True) + \
              glob.glob('records/acts/act-zm-*.json'):
        fn = os.path.basename(fp)
        m = re.match(r'act-zm-(\d{4})-(\d+)\.json', fn)
        if m:
            acts_existing.add((int(m.group(1)), int(m.group(2))))
    print(f"existing Act keys on disk: {len(acts_existing)}")

    # 3) Refresh /legislation/recent (looks for new Acts upstream)
    recent_url = "https://zambialii.org/legislation/recent"
    out = '_work/batch_0293_zambialii_recent.html'
    if os.path.exists(out):
        html = open(out, 'rb').read()
        sha = hashlib.sha256(html).hexdigest()
        print(f"  reused {out} sha256={sha[:16]} len={len(html)}")
    else:
        print(f"GET {recent_url}")
        html = fetch(recent_url, ZLII_CRAWL)
        sha = hashlib.sha256(html).hexdigest()
        with open(out, 'wb') as f:
            f.write(html)
        log_cost(today, recent_url, len(html), batch, 'probe')
        print(f"  saved {out} sha256={sha[:16]} len={len(html)}")

    soup = BeautifulSoup(html, 'html.parser')
    recent_acts = []
    seen = set()
    for a in soup.find_all('a', href=True):
        m = re.match(r'/akn/zm/act/(\d{4})/(\d+)', a['href'])
        if m:
            yr, num = int(m.group(1)), int(m.group(2))
            if (yr, num) not in seen:
                seen.add((yr, num))
                recent_acts.append({
                    'yr': yr, 'num': num,
                    'title': a.get_text(strip=True)[:120],
                    'in_corpus': (yr, num) in acts_existing,
                })
    in_corpus_count = sum(1 for x in recent_acts if x['in_corpus'])
    novel_acts_recent = [x for x in recent_acts if not x['in_corpus']]
    print(f"  /legislation/recent: {len(recent_acts)} act links; "
          f"{in_corpus_count} in corpus; {len(novel_acts_recent)} novel")
    for x in novel_acts_recent:
        print(f"    NOVEL: {x['yr']}/{x['num']} {x['title']}")

    # 4) Probe each alphabet (D, G, H, K, O, R, U)
    all_results = {}
    for alpha in ALPHABETS:
        url = f"https://zambialii.org/legislation/?alphabet={alpha}"
        out = f'_work/batch_0293_alphabet_{alpha}.html'
        if os.path.exists(out):
            html = open(out, 'rb').read()
            sha = hashlib.sha256(html).hexdigest()
            print(f"  reused {out} sha256={sha[:16]} len={len(html)}")
        else:
            print(f"GET {url}")
            html = fetch(url, ZLII_CRAWL)
            sha = hashlib.sha256(html).hexdigest()
            with open(out, 'wb') as f:
                f.write(html)
            log_cost(today, url, len(html), batch, 'probe')
            print(f"  saved {out} sha256={sha[:16]} len={len(html)}")

        soup = BeautifulSoup(html, 'html.parser')
        si_links = []
        seen = set()
        for a in soup.find_all('a', href=True):
            h = a['href']
            m = re.match(r'/akn/zm/act/si/(\d{4})/(\d+)(?:/eng@(\d{4}-\d{2}-\d{2}))?', h)
            if m:
                yr, num = int(m.group(1)), int(m.group(2))
                eng = m.group(3)
                key = (yr, num)
                if key in seen:
                    continue
                seen.add(key)
                title = a.get_text(strip=True)
                si_links.append({'yr': yr, 'num': num, 'href': h,
                                 'eng_date': eng, 'title': title})

        modern = [s for s in si_links if s['yr'] >= 2017]
        novel = [s for s in modern if (s['yr'], s['num']) not in sis_existing]
        for n in novel:
            n['sub_phase'] = classify(n['title'])
        print(f"  alphabet={alpha}: total={len(si_links)} modern={len(modern)} novel={len(novel)}")
        for n in sorted(novel, key=lambda x: (x['sub_phase'] or 'zzz', -x['yr'], x['num']))[:25]:
            sp = n['sub_phase'] or 'off'
            print(f"    [{sp:>22}] {n['yr']}/{n['num']:>3} ({n['eng_date']}) {n['title'][:90]}")

        all_results[alpha] = {
            'total': len(si_links),
            'modern_count': len(modern),
            'novel': novel,
            'html_sha': sha,
            'html_path': out,
        }

    # 5) Refresh parliament /acts-of-parliament page 0
    parl_robots_path = '_work/batch_0293_parliament_robots.txt'
    if os.path.exists(parl_robots_path):
        parl_robots = open(parl_robots_path, 'rb').read()
        parl_rsha = hashlib.sha256(parl_robots).hexdigest()
        print(f"parliament robots.txt sha256={parl_rsha} (reused)")
    else:
        parl_robots = fetch(ROBOTS_PARL, PARLIA_CRAWL)
        parl_rsha = hashlib.sha256(parl_robots).hexdigest()
        print(f"parliament robots.txt sha256={parl_rsha}")
        with open(parl_robots_path, 'wb') as f:
            f.write(parl_robots)
        log_cost(today, ROBOTS_PARL, len(parl_robots), batch, 'probe')
    parl_robots_drift = parl_rsha != EXPECTED_ROBOTS_PARL

    parl_url = "https://www.parliament.gov.zm/acts-of-parliament"
    out = '_work/batch_0293_parliament_p0.html'
    if os.path.exists(out):
        parl_html = open(out, 'rb').read()
        parl_sha = hashlib.sha256(parl_html).hexdigest()
        print(f"  reused {out} sha256={parl_sha[:16]} len={len(parl_html)}")
    else:
        print(f"GET {parl_url}")
        parl_html = fetch(parl_url, PARLIA_CRAWL)
        parl_sha = hashlib.sha256(parl_html).hexdigest()
        with open(out, 'wb') as f:
            f.write(parl_html)
        log_cost(today, parl_url, len(parl_html), batch, 'probe')
        print(f"  saved {out} sha256={parl_sha[:16]} len={len(parl_html)}")

    parl_soup = BeautifulSoup(parl_html, 'html.parser')
    parl_acts = []
    parl_seen = set()
    for a in parl_soup.find_all('a', href=True):
        h = a['href']
        # Parliament listing: hrefs of form /acts/act-no-N-of-YYYY or similar
        m = re.search(r'(?:act[-_]?no[-_]?|the-)(\d+)[-_]of[-_](\d{4})', h, re.I)
        if m:
            num, yr = int(m.group(1)), int(m.group(2))
            key = (yr, num)
            if key in parl_seen:
                continue
            parl_seen.add(key)
            parl_acts.append({
                'yr': yr, 'num': num,
                'href': h,
                'title': a.get_text(strip=True)[:120],
                'in_corpus': key in acts_existing,
            })
    parl_in_corpus = sum(1 for x in parl_acts if x['in_corpus'])
    parl_novel = [x for x in parl_acts if not x['in_corpus']]
    print(f"  parliament page0: {len(parl_acts)} act links; "
          f"{parl_in_corpus} in corpus; {len(parl_novel)} novel")
    for x in parl_novel:
        print(f"    NOVEL: {x['yr']}/{x['num']} {x['title']} -> {x['href']}")

    # 6) Build candidate picks list (in priority_order sub-phases)
    picks = []
    off = []
    for alpha, data in all_results.items():
        for n in data['novel']:
            row = dict(n)
            row['alpha'] = alpha
            if n['sub_phase'] in ('sis_corporate', 'sis_tax',
                                  'sis_employment', 'sis_mining',
                                  'sis_family', 'sis_data_protection'):
                picks.append(row)
            else:
                off.append(row)

    PRIORITY = ['sis_corporate', 'sis_tax', 'sis_employment',
                'sis_mining', 'sis_family', 'sis_data_protection']
    picks.sort(key=lambda x: (PRIORITY.index(x['sub_phase']),
                              -x['yr'], x['num']))
    off.sort(key=lambda x: (-x['yr'], x['num']))

    print()
    print(f"In-priority candidates (priority_order matches): {len(picks)}")
    for p in picks[:30]:
        print(f"  [{p['sub_phase']:>22}] {p['yr']}/{p['num']:>3} {p['title'][:100]}")
    print()
    print(f"Off-priority novel modern SIs (reserved): {len(off)}")
    for p in off[:30]:
        print(f"  {p['yr']}/{p['num']:>3} {p['title'][:100]}")

    out_obj = {
        'batch': batch,
        'fetched_at_utc': datetime.now(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z'),
        'zambialii_robots_sha': rsha,
        'parliament_robots_sha': parl_rsha,
        'parliament_robots_drift_from_b0290': parl_robots_drift,
        'parliament_expected_robots_sha': EXPECTED_ROBOTS_PARL,
        'alphabets': all_results,
        'picks': picks,
        'off_priority': off,
        'recent_acts': recent_acts,
        'recent_acts_in_corpus': in_corpus_count,
        'recent_acts_novel': novel_acts_recent,
        'parliament_acts_p0': parl_acts,
        'parliament_in_corpus': parl_in_corpus,
        'parliament_novel': parl_novel,
        'sis_existing_count': len(sis_existing),
        'acts_existing_count': len(acts_existing),
    }
    with open('_work/batch_0293_probe.json', 'w') as f:
        json.dump(out_obj, f, indent=2)
    print("saved _work/batch_0293_probe.json")


if __name__ == '__main__':
    main()
