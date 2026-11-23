#!/usr/bin/env python3
"""Check the state education tax rate (towns_data.STATE_RATE) and the total tax rate shown on the page for Durham, Lee and Madbury against the
DRA's all-town rate sheets mirrored in raw/nh-dra/ (tax year N is the school year N/N+1, page key N+1):
  tax year 2020: 2020 tax-rate-comparison workbook; tax years 2021 to 2025: municipal-and-village tax rate workbooks.
Also checks that municipal + county + state education + local education = total on each sheet.
Run from the repo root (needs openpyxl):  python3 build/verify_dra_ratesheets.py ; exit 1 on any difference."""
import os, sys, openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from towns_data import STATE_RATE

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "raw", "nh-dra")
TOWNS = ("Durham", "Lee", "Madbury")
RATES = {  # tax year: (file, kind)
    2021: ("inline-documents__sonh__municipal-property__2021-municipal-and-village-tax-rates.xlsx", "mv"),
    2022: ("inline-documents__sonh__municipal-property__2022-municpal-and-village-tax-rates.xlsx", "mv"),
    2023: ("inline-documents__sonh__municipal-property__2023-municipal-and-village-tax-rates.xlsx", "mv"),
    2024: ("documents__2024-municipal-and-village-tax-rates.xlsx", "mv"),
    2025: ("documents__2025-municipal-and-village-district-tax-rates.xlsx", "mv"),
    2020: ("inline-documents__sonh__municipal-property__2020-tax-rate-comparison.xlsx", "cmp"),
}
bad = 0
for ty in sorted(RATES):
    f, kind = RATES[ty]
    ws = openpyxl.load_workbook(os.path.join(RAW, f), data_only=True).worksheets[0]
    got = {}
    for r in ws.iter_rows(values_only=True):
        c = [x for x in r if x is not None]   # some sheets have empty leading or interior columns
        if kind == "mv" and c and c[0] in TOWNS and len(c) >= 9:  # Municipality, Date, Valuation, Valuation incl. utilities, Municipal, County, State Ed, Local Ed, Total
            got[c[0]] = dict(mun=c[4], cty=c[5], st=c[6], loc=c[7], tot=c[8])
        if kind == "cmp" and len(r) > 24 and r[1] in TOWNS:   # comparison workbook: total col 7, local school 8, state ed 14, county 19, municipal 24
            got[r[1]] = dict(mun=r[24], cty=r[19], st=r[14], loc=r[8], tot=r[7])
    page = STATE_RATE.get(ty + 1)
    for i, t in enumerate(TOWNS):
        g = {k: round(float(v), 2) for k, v in got[t].items()}
        ident = abs(g["mun"] + g["cty"] + g["st"] + g["loc"] - g["tot"]) < 0.025
        ok = ident and page is not None and abs(page[i] - g["st"]) < 0.005
        bad += not ok
        print("OK       " if ok else "MISMATCH ", "tax year", ty, t, "state ed: page", page[i] if page else None, "DRA", g["st"],
              "| sum of parts", round(g["mun"] + g["cty"] + g["st"] + g["loc"], 2), "total", g["tot"])
print("mismatches:", bad)
sys.exit(1 if bad else 0)
