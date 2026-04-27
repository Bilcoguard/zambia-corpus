"""Parse the 6 cached alphabet HTML listings and classify novel modern SIs.
Reads _work/batch_0292_alphabet_{E,F,J,L,N,W}.html and writes
_work/batch_0292_probe.json.
"""
import os, json, hashlib, re, glob
from bs4 import BeautifulSoup

ALPHABETS = ['E', 'F', 'J', 'L', 'N', 'W']

EMP_PAT = re.compile(
    r'\b(Employment|Labour|NAPSA|National\s+Pension|Workers?[\']?\s+Compensation|'
    r'Workmen[\']?s\s+Compensation|Minimum\s+Wage|Industrial\s+(?:and\s+Labour\s+)?Relations|'
    r'Factories|Apprenticeship|Occupational\s+Health)\b', re.I)
MIN_PAT = re.compile(r'\b(Mines|Mining|Minerals?)\b', re.I)
FAM_PAT = re.compile(
    r'\b(Marriage|Matrimonial|Children|Juvenile|Maintenance|Adoption|Affiliation)\b',
    re.I)

# Build existing on-disk SI key set
existing = set()
for f in glob.glob('records/sis/**/si-zm-*.json', recursive=True) + \
         glob.glob('records/sis/si-zm-*.json'):
    fn = os.path.basename(f)
    parts = fn.split('-')
    if len(parts) >= 4:
        try:
            yr = int(parts[2]); num = int(parts[3])
            existing.add((yr, num))
        except Exception:
            pass
print(f"existing SI keys on disk: {len(existing)}")

all_results = {}
for alpha in ALPHABETS:
    path = f'_work/batch_0292_alphabet_{alpha}.html'
    html = open(path, 'rb').read()
    sha = hashlib.sha256(html).hexdigest()
    soup = BeautifulSoup(html, 'html.parser')
    si_links = []
    seen = set()
    for a in soup.find_all('a', href=True):
        h = a['href']
        m = re.match(r'/akn/zm/act/si/(\d{4})/(\d+)(?:/eng@(\d{4}-\d{2}-\d{2}))?', h)
        if m:
            yr = int(m.group(1)); num = int(m.group(2)); eng = m.group(3)
            key = (yr, num)
            if key in seen:
                continue
            seen.add(key)
            title = a.get_text(strip=True)
            si_links.append({'yr': yr, 'num': num, 'href': h,
                             'eng_date': eng, 'title': title})
    modern = [s for s in si_links if s['yr'] >= 2017]
    novel = [s for s in modern if (s['yr'], s['num']) not in existing]
    for n in novel:
        t = n['title']
        if EMP_PAT.search(t):
            n['sub_phase'] = 'sis_employment'
        elif MIN_PAT.search(t):
            n['sub_phase'] = 'sis_mining'
        elif FAM_PAT.search(t):
            n['sub_phase'] = 'sis_family'
        else:
            n['sub_phase'] = None
    all_results[alpha] = {
        'total': len(si_links),
        'modern_count': len(modern),
        'novel': novel,
        'html_sha': sha,
        'html_path': path,
    }
    print(f"alphabet={alpha}: total={len(si_links)} modern={len(modern)} novel={len(novel)}")
    for n in sorted(novel, key=lambda x: (-x['yr'], x['num']))[:30]:
        sp = n['sub_phase'] or 'off'
        print(f"  [{sp}] {n['yr']}/{n['num']:>3} ({n['eng_date']}) {n['title'][:90]}")

picks = []
for alpha, data in all_results.items():
    for n in data['novel']:
        if n['sub_phase'] in ('sis_employment', 'sis_mining', 'sis_family'):
            picks.append({**n, 'alpha': alpha})
order = ['sis_employment', 'sis_mining', 'sis_family']
picks_sorted = sorted(picks, key=lambda x: (order.index(x['sub_phase']),
                                            -x['yr'], x['num']))
off_priority = []
for alpha, data in all_results.items():
    for n in data['novel']:
        if n['sub_phase'] is None:
            off_priority.append({**n, 'alpha': alpha})
off_sorted = sorted(off_priority, key=lambda x: (-x['yr'], x['num']))

print(f"\nIn-priority candidates: {len(picks_sorted)}")
for p in picks_sorted:
    print(f"  [{p['sub_phase']}] {p['yr']}/{p['num']:>3} {p['title'][:100]}")
print(f"\nOff-priority novel modern SIs (reserved): {len(off_sorted)}")
for p in off_sorted[:30]:
    print(f"  {p['yr']}/{p['num']:>3} {p['title'][:100]}")

out = {
    'alphabets': all_results,
    'picks': picks_sorted,
    'off_priority': off_sorted,
    'existing_count': len(existing),
}
with open('_work/batch_0292_probe.json', 'w') as f:
    json.dump(out, f, indent=2)
print('\nsaved _work/batch_0292_probe.json')
