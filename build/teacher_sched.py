#!/usr/bin/env python3
"""Top of the teacher salary scale, Oyster River vs the NH average, from the DOE 'Teacher Salary Schedule' files in raw/nh-doe/.
Each file lists, per district and degree level (BA, BA30, MA, MA30, ...), the minimum and maximum salary and the number of steps.
The NH figure is the unweighted average over districts that listed that degree level. No 2022-23 schedule file was found on the DOE page.
Prints put() lines for rc_data.py."""
import csv, os, re, statistics, openpyxl
RAW = os.environ.get('NH_RAW', 'raw/nh-doe/inline-documents__')  # run from the repo root
F = {2018: 'teach_sal_sched17-18.csv', 2019: 'teach_sal_sched18-19.csv', 2020: 'teach_sal_sched19-20.csv', 2021: 'sonh__teach-sal-sched20-21_0.csv',
     2022: 'sonh__teach-sal-sched21-22.csv', 2024: 'sonh__teach-sal-schedl23-24.csv', 2025: 'sonh__teach-sal-sched24-25.xlsx', 2026: 'sonh__teacher-salary-schedule-25-26.xlsx'}
DEG = {'BA', 'BA30', 'MA', 'MA30', 'MA45', 'MA60', 'DOC', 'CAGS', 'PHD'}
def num(x):
    try: return float(str(x).replace('$', '').replace(',', '').strip())
    except Exception: return None
def rows(path):
    if path.endswith('.xlsx'):
        for r in openpyxl.load_workbook(path, data_only=True).worksheets[0].iter_rows(values_only=True): yield list(r)
    else:
        for r in csv.reader(open(path, encoding='utf-8-sig', errors='replace')): yield r
def load(fy):
    out = {}   # (sau, degree) -> (min, max, steps)
    for r in rows(RAW + F[fy]):
        r = [c for c in r]
        try: sau = int(float(str(r[0])))
        except Exception: continue
        d = [i for i, c in enumerate(r) if isinstance(c, str) and c.strip().upper() in DEG]
        if not d: continue
        i = d[0]; lo, hi = num(r[i + 1]), num(r[i + 2])
        if lo and hi: out[(sau, r[i].strip().upper())] = (lo, hi, num(r[i + 3]) if len(r) > i + 3 else None)
    return out
res = {}
for fy in F:
    d = load(fy)
    row = {}
    for deg in ('BA', 'MA'):
        vals = [v for (s, g), v in d.items() if g == deg]
        row[deg] = dict(oy=d.get((5, deg)), nh_min=statistics.mean(v[0] for v in vals), nh_max=statistics.mean(v[1] for v in vals), n=len(vals))
    res[fy] = row
if __name__ == '__main__':
    def series(f): return '[' + ', '.join(str(f(res[y])) if y in res else 'None' for y in range(2018, 2027)) + ']'
    for deg, nm in (('MA', 'ma'), ('BA', 'ba')):
        print("put('ts_%s_max', per(%s))" % (nm, series(lambda r: int(r[deg]['oy'][1]))))
        print("put('ts_%s_max_nh', per(%s))" % (nm, series(lambda r: round(r[deg]['nh_max']))))
    print("put('ts_ma_steps', per(%s))" % series(lambda r: int(r['MA']['oy'][2])))
    print("put('ts_ma_n', per(%s))" % series(lambda r: r['MA']['n']))
    for y in res: print('#', y, 'MA oy', res[y]['MA']['oy'], 'nh min/max', round(res[y]['MA']['nh_min']), round(res[y]['MA']['nh_max']), 'n', res[y]['MA']['n'], '| BA oy', res[y]['BA']['oy'], round(res[y]['BA']['nh_min']), round(res[y]['BA']['nh_max']))
