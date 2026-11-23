#!/usr/bin/env python3
"""Add raw/MANIFEST.csv rows for the NH DOE / DRA files mirrored on 2026-11-23 (DOE 'financial reports', 'staffing and salary',
'other state aid', 'assessment' and College Board pages; DRA 'municipal and property reports'). Run from the repo root after the files are in raw/.
Each file is the original download, unmodified; the sha256 is computed here from the stored file."""
import csv, hashlib, os, sys
DOE = 'https://www.education.nh.gov/sites/g/files/ehbemt326/files/'
DRA = 'https://www.revenue.nh.gov/sites/g/files/ehbemt736/files/'
DOE_GROUPS = [(24,'financial-reports'),(26,'state-adequate-education-aid'),(30,'assessment-data'),(59,'staffing-and-salary-reports'),
              (68,'other-state-aid-programs'),(79,'district-staffing-reports'),(103,'non-statewide-assessment-college-board-reports'),(111,'restraint-and-seclusion')]
def names(p):
    return [l.split()[2] for l in open(p) if l.strip()]
def group(i):
    for end, g in DOE_GROUPS:
        if i <= end: return g
def used(name, g):
    b = name.split('__')[-1]
    import re
    m = re.match(r'admin-sal-(\d\d)-(\d\d)', b) or re.match(r'salaries(\d\d)-(\d\d)', b)
    if m and 'principal' not in b: return 'cpay:20%s-%s' % (m.group(1), m.group(2))
    if b == 'salaries20-21.xlsx': return 'cpay:2020-21 (same data as the _1 csv)'
    m = re.match(r'(summary-of-rev|state[-_]summary|summaryrevexp)', b)
    if m:
        y = re.search(r'(\d{2})[-_](\d{2})|fy(\d{4})|20(\d\d)-20(\d\d)|fy2021', b)
        return 'instr,spec,adm,local,fed (NH shares)'
    if re.match(r'fte-district', b): return 'nts (FTE staff, checked against page values)'
    if re.match(r'teach[-_]att', b): return 'tdeg (teacher degrees, checked against page values)'
    if re.match(r'teach[-_]sal[-_]sched', b) or b.startswith('teacher-salary-schedule'): return 'tmax (top of salary scale)'
    if 'restraint' in b: return 'restr (annual report; Oyster River rows)'
    if 'adequacy-fy-28' in b or 'adequacy-explained-fy-2028' in b: return 'page notes (FY28 estimate, not charted)'
    if 'tax-rate' in b: return 'rate,sch (checked by build/verify_dra_rates.py)'
    return 'listed on DOE page %s; not charted' % g
def main():
    man = list(csv.DictReader(open('raw/MANIFEST.csv', newline='')))
    have = {r['stored_as'] for r in man}
    cols = ['file','source_url','bytes','sha256_of_original','stored_as','retrieved','used_by','status']
    new = []
    for i, n in enumerate(names('.stage/map_edu.txt'), 1):
        new.append((n, DOE + n[len('nh-doe/'):].replace('__', '/'), group(i)))
    for n in names('.stage/map_dra.txt'):
        new.append((n, DRA + n[len('nh-dra/'):].replace('__', '/'), 'municipal-and-property-reports'))
    add = 0; missing = []
    byname = {r['stored_as']: r for r in man}
    for n, url, g in new:
        if n in have:
            r = byname[n]
            if r['retrieved'] == '2026-11-23' and r['status'] == 'mirrored' and n.startswith('nh-doe/'): r['used_by'] = used(n, g)
            continue
        if not os.path.exists('raw/' + n): missing.append(n); continue
        data = open('raw/' + n, 'rb').read()
        u = used(n, g) if n.startswith('nh-doe/') else ('rate,sch (checked by build/verify_dra_rates.py)' if 'tax-rate-c' in n else 'listed on DRA municipal and property reports page; not charted')
        man.append(dict(file=n, source_url=url, bytes=len(data), sha256_of_original=hashlib.sha256(data).hexdigest(), stored_as=n,
                        retrieved='2026-11-23', used_by=u, status='mirrored')); add += 1
    with open('raw/MANIFEST.csv', 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(man)
    print('added', add, 'rows; total', len(man), '; missing', len(missing))
    for m in missing: print(' MISSING', m)
main()
