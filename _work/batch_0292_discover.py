"""Batch 0292 — Phase 4 / sis_employment + sis_mining + sis_family probe.

Probes zambialii alphabets E, F, J, L, N, W for novel modern (>=2017) SIs
matching employment/mining/family title patterns. Probe-only (no record
writes). Outputs:

  _work/batch_0292_alphabet_<X>.html — raw listing HTML per alphabet
  _work/batch_0292_probe.json        — structured findings + candidate picks
"""
import sys, os, json, hashlib, time, urllib.request, re, glob
from datetime import datetime, timezone
from bs4 import BeautifulSoup

UA = "KateWestonLegal-CorpusBuilder/1.0 (contact: peter@bilcoguard.com)"
HEADERS = {"User-Agent": UA}
CRAWL = 6.0  # zambialii robots Crawl-delay 5s + 1s margin

ROBOTS_URL = "https://zambialii.org/robots.txt"
EXPECTED_ROBOTS = "fce67b697ee4ef44e0694134e23108c2701b5e7661eed885013efb9b75dcd8f0"

ALPHABETS = ['E', 'F', 'J', 'L', 'N', 'W']

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


def fetch(url):
    time.sleep(CRAWL)
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=45).read()


def main():
    # 1) Robots re-verify
    robots = fetch(ROBOTS_URL)
    robots_sha = hashlib.sha256(robots).hexdigest()
    print(f"robots.txt sha256={robots_sha}")
    assert robots_sha == EXPECTED_ROBOTS, f"robots drift: {robots_sha}"
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    with open('costs.log', 'a') as f:
        f.write(json.dumps({'date': today, 'url': ROBOTS_URL,
                            'bytes': len(robots), 'batch': '0292',
                            'kind': 'probe'}) + '\n')

    # 2) Build existing on-disk SI key set
    existing = set()
    for f in glob.glob('records/sis/**/si-zm-*.json', recursive=True) + \
             glob.glob('records/sis/si-zm-*.json'):
        fn = os.path.basename(f)
        parts = fn.split('-')
        if len(parts) >= 4:
            try:
                yr = int(parts[2])
                num = int(parts[3])
                existing.add((yr, num))
            except Exception:
                pass
    print(f"existing SI keys on disk: {len(existing)}")

    # 3) Probe each alphabet (reuse cached HTML if present from prior run)
    all_results = {}
    for alpha in ALPHABETS:
        url = f"https://zambialii.org/legislation/?alphabet={alpha}"
        out = f'_work/batch_0292_alphabet_{alpha}.html'
        if os.path.exists(out):
            html = open(out, 'rb').read()
            sha = hashlib.sha256(html).hexdigest()
            print(f"  reused {out} sha256={sha[:16]} len={len(html)}")
        else:
            print(f"GET {url}")
            html = fetch(url)
            sha = hashlib.sha256(html).hexdigest()
            with open(out, 'wb') as f:
                f.write(html)
            print(f"  saved {out} sha256={sha[:16]} len={len(html)}")
            with open('costs.log', 'a') as f:
                f.write(json.dumps({'date': today, 'url': url,
                                    'bytes': len(html), 'batch': '0292',
                                    'kind': 'probe'}) + '\n')

        soup = BeautifulSoup(html, 'html.parser')
        si_links = []
        seen = set()
        for a in soup.find_all('a', href=True):
            h = a['href']
            m = re.match(r'/akn/zm/act/si/(\d{4})/(\d+)(?:/eng@(\d{4}-\d{2}-\d{2}))?', h)
            if m:
                yr = int(m.group(1))
                num = int(m.group(2))
                eng = m.group(3)
                key = (yr, num)
                if key in seen:
                    continue
                seen.add(key)
                title = a.get_text(strip=True)
                si_links.append({'yr': yr, 'num': num, 'href': h,
                                 'eng_date': eng, 'title': title})

        modern = [s for s in si_links if s['yr'] >= 2017]
        novel = [s for s in modern if (s['yr'], s['num']) not in existing]
        print(f"  alphabet={alpha}: total={len(si_links)} modern={len(modern)} novel={len(novel)}")

        # Classify each novel by sub-phase
        for n in novel:
            t = n['title']
            if EMP_PAT.search(t):
                n['sub_phase'] = 'sis_employment'
            elif MIN_PAT.search(t):
                n['sub_phase'] = 'sis_mining'
            elif FAM_PAT.search(t):
                n['sub_phase'] = 'sis_family'
            else:
                n['sub_phase'] = None  # off-priority

        all_results[alpha] = {
            'total': len(si_links),
            'modern_count': len(modern),
            'novel': novel,
            'html_sha': sha,
            'html_path': out,
        }

        novel_in_priority = [n for n in novel if n['sub_phase']]
        novel_off = [n for n in novel if not n['sub_phase']]
        for n in sorted(novel_in_priority, key=lambda x: (-x['yr'], x['num']))[:25]:
            print(f"    [{n['sub_phase']}] {n['yr']}/{n['num']:>3} ({n['eng_date']}) {n['title'][:90]}")
        if novel_off:
            print(f"  novel-off-priority on alphabet={alpha}: {len(novel_off)}")
            for n in novel_off[:5]:
                print(f"    [off]               {n['yr']}/{n['num']:>3} ({n['eng_date']}) {n['title'][:90]}")

    # 4) Build candidate picks list (within priority_order sub-phases)
    picks = []
    for alpha, data in all_results.items():
        for n in data['novel']:
            if n['sub_phase'] in ('sis_employment', 'sis_mining', 'sis_family'):
                picks.append({**n, 'alpha': alpha})
    picks_sorted = sorted(picks, key=lambda x: (
        ['sis_employment', 'sis_mining', 'sis_family'].index(x['sub_phase']),
        -x['yr'], x['num']
    ))
    print()
    print(f"In-priority candidates (sis_employment + sis_mining + sis_family): {len(picks_sorted)}")
    for p in picks_sorted[:30]:
        print(f"  [{p['sub_phase']}] {p['yr']}/{p['num']:>3} {p['title'][:100]}")

    off_priority = []
    for alpha, data in all_results.items():
        for n in data['novel']:
            if n['sub_phase'] is None:
                off_priority.append({**n, 'alpha': alpha})
    off_sorted = sorted(off_priority, key=lambda x: (-x['yr'], x['num']))
    print()
    print(f"Off-priority novel modern SIs (reserved): {len(off_sorted)}")
    for p in off_sorted[:30]:
        print(f"  {p['yr']}/{p['num']:>3} {p['title'][:100]}")

    out = {
        'alphabets': all_results,
        'picks': picks_sorted,
        'off_priority': off_sorted,
        'existing_count': len(existing),
        'robots_sha': robots_sha,
    }
    with open('_work/batch_0292_probe.json', 'w') as f:
        json.dump(out, f, indent=2)
    print("saved _work/batch_0292_probe.json")


if __name__ == '__main__':
    main()
