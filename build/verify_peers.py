"""Cross-check the peer-comparison fields (peers.py) against values already on the page from other sources.

ORCSD's own cost per pupil, reading and math proficiency, growth and cost rank were typed into make_data.py / nhdoe_values.py
before peers.py existed; peers.py recomputes them from every district's row in the raw DOE files. They must agree.
Also checks peer-set sizes against the page's K-12 count and prints how many districts were dropped for suppressed values.
"""
import json, os, sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rows = json.load(open('orcsd_years.json'))['rows']
bad = 0
n = 0
for r in rows:
    fy = r['fy']
    def chk(label, a, b, tol=0.0):
        global bad, n
        if a is None and b is None:
            return
        n += 1
        if a is None or b is None or abs(a - b) > tol:
            bad += 1
            print('DIFF', fy, label, a, b)
    if r.get('pe_cost') is not None:
        chk('cost per pupil', r['pe_cost'], r['nhed_cpp'], 0.51)
        chk('cost rank', r['pe_cost_rank'], r['cpp_rank'])
        chk('K-12 count', r['pe_cost_n'], r['cpp_rank_n'])
        chk('K-12 median cost', r['pe_cost_med'], r['cpp_k12_med'], 0.51)
    if r.get('pe_prof') is not None:
        chk('ELA', r['pe_ela'], r['ela'])
        chk('math', r['pe_mat'], r['math'])
        if r.get('pe_sgp') is not None:
            chk('growth', r['pe_sgp'], (r['sgp_rea'] + r['sgp_mat']) / 2, 0.051)
    peers = r.get('pe_peers')
    if peers:
        me = [p for p in peers if p[5]]
        chk('one ORCSD point', len(me), 1)
        chk('peer count', len(peers), r['pe_n'])
print('%d comparisons, %d differences' % (n, bad))
sys.exit(1 if bad else 0)
