#!/usr/bin/env python3
"""Tie the by-town results to the district results already on the page (iAchieve / DOE district file).

The district's reading and math shares must equal the student-weighted mean of its towns' shares (Durham, Lee, Madbury and the
few Barrington tuition students), within the rounding of the DOE's whole-number shares and rounded student counts.  Run from the
repo root:  python3 build/verify_town_results.py   (the workbook re-read is town_results_extract.py --check, which needs openpyxl).
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, "town_results.json")))
rows = {int(r["fy"][:4]) + 1: r for r in json.load(open(os.path.join(HERE, "orcsd_years.json")))["rows"]}
bad = n = 0
for y, towns in sorted(T.items()):
    r = rows[int(y)]
    for subj, key in (("rea", "ela"), ("mat", "math")):
        num = den = 0.0
        for name, c in towns.items():
            w = sum(c["mat"]["n"]) / 2
            num += w * c[subj]["prof"]
            den += w
        wm = num / den
        n += 1
        flag = abs(wm - r[key]) > 1.6
        bad += flag
        print(("DIFF " if flag else "ok   ") + "%s %s: weighted towns %.1f vs district %s" % (y, subj, wm, r[key]))
print("%d tie-outs, %d differences" % (n, bad))
sys.exit(1 if bad else 0)
