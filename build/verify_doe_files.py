#!/usr/bin/env python3
"""Check two page rows against the DOE's machine-readable files mirrored in raw/nh-doe/ (run from the repo root):
  * special education adequacy aid (`adq_sped`) against the "Allocation for Special Education ADM-R in Adequate Education Aid" CSVs, FY2018-FY2024
  * Education Freedom Account students and the state's calculated adequate-education cost for them (`efa_dur/lee/mad`, `efa_aid`)
    against the "EFA by muni" workbooks, FY2022-FY2027
Values come from data/orcsd_years.json (what the page draws). Prints one line per check; exit 1 on any difference."""
import csv, glob, json, os, re, sys
import openpyxl

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = os.path.join(ROOT, "raw", "nh-doe")
rows = {int(r["fy"][:4]) + 1: r for r in json.load(open(os.path.join(ROOT, "data", "orcsd_years.json")))["rows"]}
bad = 0

def fnum(s):
    s = re.sub(r"[^0-9.]", "", str(s))
    return float(s) if s else None

def check(label, page, doe, tol):
    global bad
    ok = page is not None and doe is not None and abs(page - doe) <= tol
    bad += not ok
    print(("OK       " if ok else "MISMATCH "), label, "page", page, "DOE file", doe)

# --- special education allocation: file name carries the school year; the Oyster River Coop row holds the amount
SPED = {2018: "inline-documents__allocation_special_ed_fy17-18.csv", 2019: "inline-documents__allocation_special_ed_fy18-19.csv",
        2020: "inline-documents__sonh__allocation-special-ed-fy20.csv", 2021: "inline-documents__sonh__allocation-special-ed-fy21.csv",
        2022: "inline-documents__sonh__allocation-special-ed-fy22.csv", 2023: "inline-documents__sonh__allocation-special-ed-fy23.csv",
        2024: "inline-documents__sonh__allocation-special-ed-fy24.csv"}
for fy, name in SPED.items():
    val = None
    for r in csv.reader(open(os.path.join(RAW, name), newline="", encoding="latin-1")):
        names = [i for i, c in enumerate(r) if c.strip().upper().startswith("OYSTER RIVER COOP")]
        if names:  # the amount is the first number after the name (the district number 423 sits before it in newer files)
            val = next(fnum(c) for c in r[names[0] + 1:] if fnum(c))
    check("FY%d special-ed aid" % fy, rows[fy]["adq_sped"], val, 1.0)  # page keeps FY19-FY20 and FY24 to the dollar; others to the cent

# --- EFA by municipality: SFY file, rows for Durham / Lee / Madbury; the last "Total Calculated Cost" column is not at a fixed index,
#     so find it from the header text.
EFA = {2022: "inline-documents__sonh__efa-by-muni-as-of-06-30-2022_0.xlsx", 2023: "inline-documents__sonh__efa-by-muni-as-of-06-30-2023.xlsx",
       2024: "inline-documents__sonh__efa-by-muni-as-of-04-01-2024-.xlsx", 2025: "inline-documents__sonh__efa-by-muni-as-of-03-02-2025.xlsx",
       2026: "inline-documents__sonh__efa-by-muni-as-of-3-02-2026.xlsx", 2027: "media__media_document__efa-by-muni-as-of-10-02-2026.xlsx"}
for fy, name in EFA.items():
    ws = openpyxl.load_workbook(os.path.join(RAW, name), data_only=True).worksheets[0]
    hdr = [[c for c in r] for r in ws.iter_rows(min_row=1, max_row=8, values_only=True)]
    cost_col = next(i for r in hdr for i, c in enumerate(r) if isinstance(c, str) and c.startswith("Total Calculated Cost"))
    got = {}
    for r in ws.iter_rows(values_only=True):
        if len(r) > 6 and r[5] in ("Durham", "Lee", "Madbury") and r[4] == r[0]:  # students in column G, cost in the header's column
            got[r[5]] = (r[6], r[cost_col])
    for t, k in (("Durham", "dur"), ("Lee", "lee"), ("Madbury", "mad")):
        check("FY%d EFA students %s" % (fy, t), rows[fy]["efa_" + k], got[t][0], 0.05)
    check("FY%d EFA adequate-education cost, 3 towns" % fy, rows[fy]["efa_aid"], sum(v[1] for v in got.values()), 1.0)
print("mismatches:", bad)
sys.exit(1 if bad else 0)
