"""Page fields: where Durham, Lee and Madbury rank among New Hampshire towns on school and total tax rates per $1,000 of full value.

Reads build/town_rates.json (town_rates_extract.py, NH DOE values files, tax years 2017 to 2025).  Tax year Y is shown against the
school year Y to Y+1, so the fiscal-year key is Y+1.  For each year, among the towns with a nonzero rate:
  rks_<t> / rkt_<t>        percentile, 0 to 100, share of towns with a LOWER rate (100 = highest rate)   t = dur, lee, mad
  rks_val_<t> / rkt_val_<t>   the rate per $1,000 of equalized value (school = local education rate; total = all property taxes)
  rks_rank_<t> / rkt_rank_<t> rank, 1 = lowest rate
  rks_n, rks_med, rkt_n, rkt_med   number of towns and their median rate
"""
import json, os, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
TOWN = {"DURHAM": "dur", "LEE": "lee", "MADBURY": "mad"}


def fields():
    D = json.load(open(os.path.join(HERE, "town_rates.json")))
    out = {}
    for y, towns in D.items():
        fy = int(y) + 1
        for pref, idx in (("rks", 1), ("rkt", 2)):
            pool = [v[idx] for v in towns.values() if v[idx] > 0]
            n = len(pool)
            out.setdefault(pref + "_n", {})[fy] = n
            out.setdefault(pref + "_med", {})[fy] = round(statistics.median(pool), 2)
            for name, t in TOWN.items():
                v = towns[name][idx]
                lower = sum(1 for x in pool if x < v)
                out.setdefault(pref + "_" + t, {})[fy] = round(100.0 * lower / (n - 1), 1)
                out.setdefault(pref + "_val_" + t, {})[fy] = round(v, 2)
                out.setdefault(pref + "_rank_" + t, {})[fy] = lower + 1
    return out


if __name__ == "__main__":
    for k, v in sorted(fields().items()):
        print(k, v)
