#!/usr/bin/env python3
"""Add rows to raw/MANIFEST.csv for files that were just placed in raw/ from a download map.
Run from the repo root:   python3 build/add_manifest.py <map file> [<map file> ...] [--retrieved YYYY-MM-DD]
A map file has one line per file, `sha8 size raw-name` (raw-name = nh-doe/... or nh-dra/..., the path under raw/). The source URL is rebuilt
from the raw name (path after the last /files/ with `/` written as `__`). Existing rows are never changed. `used_by` comes from used() below;
edit it when a file starts feeding a row. The stored file is the original download, so sha256_of_original is computed from it."""
import csv, datetime, hashlib, os, re, sys

BASE = {'nh-doe/': 'https://www.education.nh.gov/sites/g/files/ehbemt326/files/',
        'nh-dra/': 'https://www.revenue.nh.gov/sites/g/files/ehbemt736/files/'}
COLS = ['file', 'source_url', 'bytes', 'sha256_of_original', 'stored_as', 'retrieved', 'used_by', 'status']
RULES = [  # (regex on the file's base name, used_by text); first match wins
    (r'equal[-_]pupil|eqprt|EVPP', 'towns_data FILES: equalized value and ADM (checked by build/verify_towns_eqprt.py)'),
    (r'allocation[-_]special[-_]ed', 'adq_sped (checked by build/verify_doe_files.py)'),
    (r'efa-by-muni', 'efa row (checked by build/verify_doe_files.py)'),
    (r'build-dist', 'cited in the page notes (FY28 estimate); not charted'),
    (r'tax-rate-calculation|tax-rate-caluclation', 'rate,sch (checked by build/verify_dra_rates.py)'),
    (r'cooperative-school-district-apportionments', 'app (apportionment shares)'),
]

def used(name):
    b = name.split('__')[-1]
    for pat, text in RULES:
        if re.search(pat, b, re.I): return text
    return 'listed on the %s page; not charted' % ('DRA municipal and property reports' if name.startswith('nh-dra/') else 'DOE')

def main():
    args = sys.argv[1:]
    retrieved = datetime.date.today().isoformat()
    if '--retrieved' in args:
        i = args.index('--retrieved'); retrieved = args[i + 1]; del args[i:i + 2]
    names = [l.split(' ', 2)[2].strip() for f in args for l in open(f) if l.strip()]
    man = list(csv.DictReader(open('raw/MANIFEST.csv', newline='')))
    have = {r['stored_as'] for r in man}
    add, missing = 0, []
    for n in names:
        if n in have: continue
        if not os.path.exists('raw/' + n): missing.append(n); continue
        base = next(v for k, v in BASE.items() if n.startswith(k))
        data = open('raw/' + n, 'rb').read()
        man.append(dict(file=n, source_url=base + n.split('/', 1)[1].replace('__', '/'), bytes=len(data),
                        sha256_of_original=hashlib.sha256(data).hexdigest(), stored_as=n, retrieved=retrieved, used_by=used(n), status='mirrored'))
        add += 1
    with open('raw/MANIFEST.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(man)
    print('added', add, 'rows; total', len(man), '; missing', len(missing))
    for m in missing: print(' MISSING', m)

main()
