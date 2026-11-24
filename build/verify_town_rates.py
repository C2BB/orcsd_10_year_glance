#!/usr/bin/env python3
"""Cross-check build/town_rates.json (NH DOE values files) against the DRA tax rate comparison workbooks, and report coverage.

The DOE's equalized local education rate and the DRA's 'Equalized School Tax Rate' are the same quantity (net school taxes over the
town's equalized valuation with utilities), published by two agencies; they should agree town by town to the cent.  Needs openpyxl.
Run from the repo root:  python3 build/verify_town_rates.py
Differences are listed; the exit status is 1 only if fewer than 95% of the common towns agree within 0.02."""
import json, os, re, sys, warnings
warnings.filterwarnings("ignore")
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "raw", "nh-dra")
D = json.load(open(os.path.join(HERE, "town_rates.json")))
DRA = {2020: "inline-documents__sonh__municipal-property__2020-tax-rate-comparison.xlsx", 2021: "documents__2021-tax-rate-comparison.xlsx",
       2022: "inline-documents__sonh__municipal-property__2022-tax-rate-comparison.xlsx", 2023: "documents__2023-tax-rate-comparison.xlsx",
       2024: "documents__2024-tax-rate-comparison.xlsx"}


def norm(s):
    return re.sub(r"[^A-Z]", "", re.sub(r"\(.*?\)", "", s.upper()))


allgood = True
for y, f in DRA.items():
    ws = openpyxl.load_workbook(os.path.join(RAW, f), read_only=True, data_only=True)["Alpha order"]
    dra = {}
    for r in ws.iter_rows(values_only=True):
        r = list(r)
        if len(r) > 2 and isinstance(r[1], str) and (r[0] is None or isinstance(r[0], str)):
            r = r[1:]
        if len(r) > 9 and isinstance(r[0], str) and isinstance(r[2], (int, float)) and isinstance(r[8], (int, float)):
            dra[norm(r[0])] = (r[8], r[2])
    doe = {norm(k): v for k, v in D[str(y)].items()}
    common = sorted(set(doe) & set(dra))
    off = [(k, round(doe[k][1], 2), round(dra[k][0], 2)) for k in common if abs(doe[k][1] - dra[k][0]) > 0.02]
    good = len(common) - len(off)
    print("%d: %d towns in both, %d agree within 0.02 (%.0f%%); DOE only %d, DRA only %d" % (y, len(common), good, 100.0 * good / len(common), len(set(doe) - set(dra)), len(set(dra) - set(doe))))
    for o in off[:6]:
        print("     differs:", o)
    allgood &= good / len(common) >= 0.95
base = set(D["2025"])
for y in sorted(D):
    miss = sorted(base - set(D[y]))
    print(y, "towns:", len(D[y]), ("missing vs 2025: " + ", ".join(miss[:12])) if miss else "")
sys.exit(0 if allgood else 1)
