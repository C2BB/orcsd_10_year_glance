#!/usr/bin/env python3
"""Check raw/MANIFEST.csv against the files in raw/.
  - every manifest row parses to 8 columns and its stored file exists
  - sha256 of the stored file matches (rows whose stored copy is a gzip of the original are skipped)
  - every file under raw/ is listed (except MANIFEST.csv and README files)
Run from the repo root:  python3 build/verify_raw.py
"""
import csv, hashlib, os, sys
root = 'raw'
rows = list(csv.reader(open(os.path.join(root, 'MANIFEST.csv'), newline='')))
hdr, rows = rows[0], rows[1:]
bad = 0
listed = set()
for r in rows:
    if len(r) != len(hdr):
        print('BAD COLUMNS', r[:2]); bad += 1; continue
    d = dict(zip(hdr, r))
    f = d['stored_as']
    listed.add(f)
    p = os.path.join(root, f)
    if not os.path.exists(p):
        print('MISSING', f); bad += 1; continue
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    if h != d['sha256_of_original'] and not f.endswith('.gz') and d['status'] != 'stored gzipped':
        print('SHA MISMATCH', f); bad += 1
unlisted = []
for dp, dn, fn in os.walk(root):
    for n in fn:
        rel = os.path.relpath(os.path.join(dp, n), root)
        if rel in ('MANIFEST.csv', 'TRACE.md') or n.startswith('README') or n == '.DS_Store':
            continue
        if rel not in listed:
            unlisted.append(rel)
for u in sorted(unlisted):
    print('NOT IN MANIFEST', u)
print(f'{len(rows)} manifest rows, {bad} problems, {len(unlisted)} unlisted files')
sys.exit(1 if bad or unlisted else 0)
