#!/usr/bin/env python3
"""NH habitual truancy rate and Oyster River count from the DOE School Safety workbooks (Section 6: Truancy).
rate = sum(students habitually truant) / sum(enrollment) over every school row in the sheet, per 100 students.
Run from the repo root:  python3 build/nh_truancy.py   (needs openpyxl; prints the values used in build/rc_data.py).
Pass --check to also compare with the values in build/rc_data.py (exit 1 on a difference)."""
import glob, os, re, sys, warnings
warnings.filterwarnings('ignore')
import openpyxl
args = [a for a in sys.argv[1:] if not a.startswith('--')]
D = args[0] if args else 'raw/nh-doe'
FILES = {2018: '2020-04__safety2017-18', 2019: '2020-04__safety2018-19', 2020: 'sonh__safety19-20', 2021: 'sonh__safety20-21',
         2022: 'sonh__safety21-22', 2023: 'sonh__safety22-23', 2024: 'sonh__safety23-24_0', 2025: 'sonh__safety24-25'}
def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None
out = {}
for fy, stem in FILES.items():
    wb = openpyxl.load_workbook(os.path.join(D, f'inline-documents__{stem}.xlsx'), read_only=True, data_only=True)
    ws = [w for w in wb.worksheets if re.search(r'ruancy', w.title)][0]
    rows = list(ws.iter_rows(values_only=True))
    h = next(i for i, r in enumerate(rows) if any(c and str(c).strip().lower() == 'enrollment' for c in r))
    ci = next(j for j, c in enumerate(rows[h]) if c and str(c).strip().lower() == 'enrollment')
    ti = next(j for j, c in enumerate(rows[h]) if c and 'habitually truant' in str(c).lower())
    ni = next(j for j, c in enumerate(rows[h]) if c and re.search(r'school\s*name|^school$', str(c).strip().lower()))
    enr = tru = 0; n = 0; orc = 0
    for r in rows[h + 1:]:
        e, t = num(r[ci]), num(r[ti])
        if e is None or t is None or not r[ni]: continue   # skips blank and footnote rows (the sheets have no total row)
        enr += e; tru += t; n += 1
        if r[0] == 5 and 423 in r[:3]: orc += t   # SAU 5, district 423 (charter schools sharing the 423 number are excluded)
    out[fy] = (round(tru / enr * 100, 2), orc, n, int(enr), int(tru))
    print(f'FY{fy}: NH {out[fy][0]:.2f} per 100  ({int(tru)} / {int(enr)} students, {n} schools); Oyster River {orc}')
print('trunt_nh =', [round(v[0], 1) if k == 2018 else v[0] for k, v in out.items()])
print('truant (Oyster River) =', [v[1] for v in out.values()])

if '--check' in sys.argv:
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rc_data.py')).read()
    nh = eval(re.search(r"put\('trunt_nh', per\((\[.*?\])\)\)", src).group(1))
    oy = eval(re.search(r'put\("truant", per\((\[.*?\])\)\)', src).group(1))
    ok = nh == [round(v[0], 2) if round(v[0], 1) != v[0] else round(v[0], 1) for v in out.values()] or all(abs(a - b[0]) < 0.006 for a, b in zip(nh, out.values()))
    ok = ok and oy == [v[1] for v in out.values()]
    print('rc_data.py matches the workbooks' if ok else 'MISMATCH with rc_data.py'); sys.exit(0 if ok else 1)
