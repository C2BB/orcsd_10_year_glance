#!/usr/bin/env python3
"""Cross-check the transcribed school-level values (raw/nh-doe/extracts-2026-11-22/iexplore-school-level.py)
and ESSA ratings (ireport-essa-ratings.txt) against the raw dashboard exports in raw/nh-doe/dashboard-exports-2026-11-22/.
Every DOE year 2016-2026 is in the export; a blank cell on the page must be absent from the export too."""
import csv, os
D = 'raw/nh-doe/dashboard-exports-2026-11-22/'
E = 'raw/nh-doe/extracts-2026-11-22/'
rows = list(csv.DictReader(open(D + 'iexplore_compare_all_entities.tsv', newline=''), delimiter='\t'))
ns = {}; exec(open(E + 'iexplore-school-level.py').read(), ns)
IND = dict(enr='Total Enrollment', ela_p='Proficiency - ELA (%)', mat_p='Proficiency - Math (%)', ela_g='Student Growth - ELA',
           mat_g='Student Growth - Math', cpp='Average Cost Per Pupil ($)', swd='Students with Disability (%)',
           cert='Educators certified in the subject (%)', exp='Experienced Educators (%)', cslr='Students/Counselors Ratio',
           nts='Students/Non-Teacher Staff Ratio', viol='Incidents of Violence')
NAME = {'HS': 'Oyster River High School', 'MS': 'Oyster River Middle School', 'MW': 'Mast Way School', 'MO': 'Moharimet School'}
have = {}
for x in rows:
    have[(x['entity'], x['indicator'], int(x['doe_year']))] = x['value']
ok = bad = absent = 0
for k, s in ns['SCHOOLS'].items():
    for f, ind in IND.items():
        if f not in s: continue
        for i, v in enumerate(s[f]):
            y = 2016 + i
            raw = have.get((NAME[k], ind, y))
            if raw is None:
                absent += 1
                if v not in (None,'C'): print('ABSENT but page has value', k, f, y, v)
                continue
            try: rv = float(raw.replace('%','').replace('$','').replace(',','').strip())
            except ValueError: rv = None
            if v is None or v == 'C': good = rv is None or v == 'C'
            else: good = rv is not None and abs(rv - float(v)) < 0.006
            if good: ok += 1
            else: bad += 1; print('DIFF', k, f, y, 'page', v, 'raw', raw)
print(f'school-level: {ok} match, {bad} differ, {absent} not in export (page value is also blank)')

# ---- ESSA ratings (extracts/ireport-essa-ratings.txt) vs the iExplore 'ESSA' rows in the raw export ----
RIND = dict(ach='Achievement Rating', ccr='College and Career Readiness Rating', grad='Graduation Rate Rating',
            el='English Language Proficiency Rating', eq='Equity Rating', gro='Growth Rating')
ok = bad = 0
for line in open(E + 'ireport-essa-ratings.txt'):
    p = line.split()
    if len(p) != 2 or '.' not in p[0] or p[0].split('.')[0] not in NAME: continue
    sch, m = p[0].split('.'); vals = p[1].split(',')
    for i, v in enumerate(vals):
        y = 2018 + i
        raw = (have.get((NAME[sch], RIND[m], y)) or '').strip()
        norm = raw if raw.startswith('*') else ('' if raw in ('', 'N/A') else str(int(float(raw))))
        want = '' if v == '-' else v
        if norm == want: ok += 1
        else: bad += 1; print('ESSA DIFF', sch, m, y, 'page', v, 'raw', repr(raw))
print(f'essa ratings: {ok} match, {bad} differ')
