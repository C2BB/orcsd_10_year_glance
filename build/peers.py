"""Peer-district comparison: where ORCSD sits among New Hampshire K-12 districts.

Inputs (all mirrored in raw/nh-doe, see raw/MANIFEST.csv):
  * Cost per pupil by district, FY2018-FY2025 (NH DOE Bureau of School Finance).
  * Statewide disaggregated assessment files, 2018-2026: District Level, All grades, regular denominator,
    share at levels 3 and 4 (reading/ELA, math), mean growth percentile, and the SES subgroup's
    share of tested students (SES = socioeconomically disadvantaged, DOE's term).

Peer set = the districts that report elementary, middle and high cost per pupil in that year's DOE file
(the same K-12 set the page already ranks cost per pupil against: 53 or 54 districts).
FY2026 has no cost file yet; the FY2025 peer set is used for FY2026 results.

Run `python3 peers.py` to print diagnostics; make_data.py imports compute().
"""
import csv, gzip, os, re, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, '..', 'raw', 'nh-doe') + os.sep

CPP = {2018: 'inline-documents__cost_per_pupil_by_district_17-18.csv',
       2019: 'inline-documents__cost-pupil-district18-19.csv',
       2020: 'inline-documents__sonh__costperpupil2019-20web.csv',
       2021: 'inline-documents__sonh__cpp-fy2021.csv',
       2022: 'inline-documents__sonh__cpp-fy2022.csv',
       2023: 'inline-documents__sonh__cpp-fy2023.csv',
       2024: 'inline-documents__sonh__cost-per-pupil-fy2024.csv',
       2025: 'inline-documents__sonh__cost-per-pupil-fy2025.csv'}
ASSESS = {2018: 'inline-documents__assessment18.csv.gz',
          2019: 'inline-documents__assessment19.csv.gz',
          2021: 'inline-documents__sonh__assessment21.csv.gz',
          2022: 'inline-documents__sonh__assessment22.csv.gz',
          2023: 'inline-documents__sonh__disaggregateddata2023.csv.gz',
          2024: 'inline-documents__sonh__disaggdata2024-1_0.csv.gz',
          2025: 'inline-documents__sonh__publicdatadisaggregated1_0.csv.gz',
          2026: 'inline-documents__2026__publicdisaggregateddata2026_csvformat.csv.gz'}
ORCSD_ID = 423
ALIAS = {'gov wentworth reg': 'governor wentworth reg', 'wiltonlyndeboro coop': 'wiltonlyndeborough coop'}


def _num(s):
    s = (s or '').strip().replace('$', '').replace(',', '')
    try:
        return float(s)
    except ValueError:
        return None


def _norm(s):
    s = s.lower().strip()
    s = re.sub(r'\bcooperative\b', 'coop', s)
    s = re.sub(r'\bregional\b', 'reg', s)
    s = re.sub(r'[^a-z0-9 ]', '', s)
    s = re.sub(r'\s+', ' ', s)
    return ALIAS.get(s, s)


def cost_file(fy):
    out = {}
    with open(R + CPP[fy], encoding='utf-8-sig', newline='') as f:
        for row in csv.reader(f):
            if len(row) < 8 or not row[0].strip().isdigit():
                continue
            out[int(row[0])] = dict(name=row[3].strip(), el=_num(row[4]), mid=_num(row[5]), hi=_num(row[6]), tot=_num(row[7]))
    return out


def k12(fy):
    return {i: v for i, v in cost_file(fy).items() if v['el'] and v['mid'] and v['hi'] and v['tot']}


def _fay(s):
    """Midpoint of DOE's rounded student-count range, '1,025 - 1,030' -> 1027.5."""
    m = re.match(r'\s*([\d,]+)\s*-\s*([\d,]+)', s or '')
    if not m:
        return None
    a, b = (float(x.replace(',', '')) for x in m.groups())
    return (a + b) / 2


def assessments(fy):
    """{norm(district): {...}} for District Level, All grades, regular denominator."""
    out = {}
    with gzip.open(R + ASSESS[fy], 'rt', encoding='utf-8-sig', newline='') as f:
        for r in csv.DictReader(f):
            lv = r.get('Level of Data') or r.get('replevel')
            if lv not in ('District Level', 'dis'):
                continue
            if (r.get('DenominatorType') or 'Regular') != 'Regular':
                continue
            gr = (r.get('Grade') if r.get('Grade') is not None else r.get('grade') or '').strip()
            if gr not in ('All grades', '0'):
                continue
            name = (r.get('District') or r.get('disname') or '').strip()
            sub = (r.get('Subgroup') or r.get('subgroup') or '').strip()
            subj = (r.get('Subject') or r.get('subject') or '').strip().lower()
            key = {'rea': 'ela', 'ela': 'ela', 'mat': 'mat', 'sci': 'sci'}.get(subj)
            if not key:
                continue
            prof = _num(r.get('Above prof% (lvl 3&4)') or r.get('pAboveprof'))
            sgp = _num(r.get('Mean SGP') or r.get('MeanSGP'))
            n = _fay(r.get('Total FAY Students') or r.get('NumberStudents'))
            d = out.setdefault(_norm(name), {'name': name})
            if sub == 'All students':
                d[key] = prof
                if key in ('ela', 'mat'):
                    d['sgp_' + key] = sgp
                if key == 'mat':
                    d['n_mat'] = n
            elif sub == 'SES' and key == 'mat':
                d['n_ses_mat'] = n
    return out


def _pct(rank, n):
    """Percentile with 100 = highest of n districts (rank 1 = highest)."""
    return round(100 * (n - rank) / (n - 1), 1) if n > 1 else None


def _ols(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx
    a = my - b * mx
    ss_tot = sum((y - my) ** 2 for y in ys)
    ss_res = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    return a, b, (1 - ss_res / ss_tot if ss_tot else 0)


def compute():
    fields = {}     # fy -> ORCSD fields for the years table
    peers = {}      # fy -> rows for the scatter: [name, cost, proficiency, ses share, growth, is_orcsd]
    cache = {fy: k12(fy) for fy in CPP}
    for fy in range(2018, 2027):
        f = {}
        costs = cache.get(fy)
        cset = costs or cache[2025]
        if costs:
            vals = sorted((v['tot'] for v in costs.values()), reverse=True)
            o = costs[ORCSD_ID]['tot']
            rk = 1 + sum(1 for v in vals if v > o)
            f.update(pe_cost=round(o), pe_cost_rank=rk, pe_cost_n=len(vals), pe_cost_pct=_pct(rk, len(vals)),
                     pe_cost_med=round(statistics.median(vals)))
        if fy not in ASSESS:
            fields[fy] = f
            continue
        A = assessments(fy)
        rows = []
        for did, v in cset.items():
            a = A.get(_norm(v['name']))
            if not a or a.get('ela') is None or a.get('mat') is None:
                continue
            sg = None
            if a.get('sgp_ela') is not None and a.get('sgp_mat') is not None:
                sg = (a['sgp_ela'] + a['sgp_mat']) / 2
            ses = None
            if a.get('n_mat') and a.get('n_ses_mat') is not None:
                ses = 100 * a['n_ses_mat'] / a['n_mat']
            rows.append(dict(id=did, name=v['name'], cost=costs[did]['tot'] if costs else None,
                             prof=(a['ela'] + a['mat']) / 2, ela=a['ela'], mat=a['mat'], sgp=sg, ses=ses))
        o = next((r for r in rows if r['id'] == ORCSD_ID), None)
        if not o:
            fields[fy] = f
            continue
        n = len(rows)
        rk = 1 + sum(1 for r in rows if r['prof'] > o['prof'])
        f.update(pe_n=n, pe_prof=round(o['prof'], 1), pe_prof_rank=rk, pe_prof_pct=_pct(rk, n),
                 pe_prof_med=round(statistics.median(r['prof'] for r in rows), 1), pe_ela=o['ela'], pe_mat=o['mat'])
        sg = [r for r in rows if r['sgp'] is not None]
        if o['sgp'] is not None and len(sg) > 5:
            rk = 1 + sum(1 for r in sg if r['sgp'] > o['sgp'])
            f.update(pe_sgp=round(o['sgp'], 1), pe_sgp_rank=rk, pe_sgp_n=len(sg), pe_sgp_pct=_pct(rk, len(sg)),
                     pe_sgp_med=round(statistics.median(r['sgp'] for r in sg), 1))
        se = [r for r in rows if r['ses'] is not None]
        if o['ses'] is not None and len(se) > 10:
            a_, b_, r2 = _ols([r['ses'] for r in se], [r['prof'] for r in se])
            exp = a_ + b_ * o['ses']
            res = o['prof'] - exp
            resid = [r['prof'] - (a_ + b_ * r['ses']) for r in se]
            rk = 1 + sum(1 for x in resid if x > res)
            f.update(pe_ses=round(o['ses'], 1), pe_ses_med=round(statistics.median(r['ses'] for r in se), 1),
                     pe_exp=round(exp, 1), pe_res=round(res, 1), pe_res_rank=rk, pe_res_n=len(se),
                     pe_slope=round(b_, 3), pe_r2=round(r2, 3))
        fields[fy] = f
        peers[fy] = [[r['name'], round(r['cost']) if r['cost'] else None, round(r['prof'], 1),
                      round(r['ses'], 1) if r['ses'] is not None else None,
                      round(r['sgp'], 1) if r['sgp'] is not None else None,
                      1 if r['id'] == ORCSD_ID else 0] for r in sorted(rows, key=lambda r: r['name'])]
    return fields, peers


if __name__ == '__main__':
    F, P = compute()
    for fy in sorted(F):
        print(fy, F[fy])
    for fy in sorted(P):
        print(fy, 'peers', len(P[fy]), 'no cost', sum(1 for p in P[fy] if p[1] is None), 'no ses', sum(1 for p in P[fy] if p[3] is None))
    for fy in sorted(ASSESS):
        cset = k12(fy if fy in CPP else 2025)
        A = assessments(fy)
        miss = [v['name'] for v in cset.values() if _norm(v['name']) not in A]
        nul = [v['name'] for v in cset.values() if _norm(v['name']) in A and (A[_norm(v['name'])].get('ela') is None or A[_norm(v['name'])].get('mat') is None)]
        print(fy, 'unmatched', miss, 'no ela/math', nul)
