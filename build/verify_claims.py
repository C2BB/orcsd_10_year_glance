#!/usr/bin/env python3
"""Recompute the 'Why have property taxes gone up?' numbers (build/claims.py) a second way and compare.

Reads data/orcsd_years.json (rows and the claims block) and build/doe25.py.  Independent of claims.py: it recomputes from the row fields
with its own arithmetic.  Run from the repo root or build/:  python3 build/verify_claims.py   (exit status 1 on any difference)
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import doe25
J = json.load(open(os.path.join(HERE, "orcsd_years.json")))
R = {int(r["fy"][:4]) + 1: r for r in J["rows"]}
C = J["claims"]
bad = n = 0


def pn(t):
    return float(t.replace("\u2212", "-").rstrip("%"))


def chk(what, got, want, tol=0.01):
    global bad, n
    n += 1
    if got is None or want is None or abs(got - want) > tol:
        bad += 1
        print("DIFF", what, got, want)


# 1. the categories of operating spending add to the DOE-25 recurring total in every year (so the bridge is complete)
FN = ["fn_reg", "fn_voc", "fn_oi", "fn_spec", "fn_ss", "fn_isup", "fn_gab", "fn_sadm", "fn_bus", "fn_plant", "fn_trans", "fn_food", "fn_bint"]
for y in range(2018, 2026):
    chk("categories add to recurring spending FY%d" % y, sum(R[y][k] for k in FN), doe25.D[y]["rec"], 1.0)
    chk("recurring spending on the page FY%d" % y, R[y]["actual_recurring"], doe25.D[y]["rec"], 1.0)
# 2. the bridge
a, b = R[2018], R[2025]
sp = {r["id"]: r for r in C["bridge"]["spend"]}
groups = {"instruction": ["fn_reg", "fn_voc", "fn_oi"], "special": ["fn_spec"], "support": ["fn_ss", "fn_isup"], "admin": ["fn_gab", "fn_sadm", "fn_bus"],
          "plant": ["fn_plant"], "transport": ["fn_trans"], "food": ["fn_food"], "interest": ["fn_bint"]}
for k, ks in groups.items():
    chk("bridge %s FY18" % k, sp[k]["av"], sum(a[x] for x in ks), 1)
    chk("bridge %s FY25" % k, sp[k]["bv"], sum(b[x] for x in ks), 1)
chk("increase shares add to 100%", sum(pn(r["inc_share"]) for r in C["bridge"]["spend"]), 100.0, 0.3)
chk("base shares add to 100%", sum(pn(r["base_share"]) for r in C["bridge"]["spend"]), 100.0, 0.3)
chk("total spending FY18", C["bridge"]["total"]["av"], doe25.D[2018]["rec"], 1)
chk("total spending FY25", C["bridge"]["total"]["bv"], doe25.D[2025]["rec"], 1)
chk("bond principal FY18", C["bridge"]["principal"]["av"], doe25.D[2018]["prin"], 1)
chk("bond principal FY25", C["bridge"]["principal"]["bv"], doe25.D[2025]["prin"], 1)
rv = {r["id"]: r for r in C["bridge"]["revenue"]}
for k, f in (("local", "rev_local"), ("otherlocal", "rev_oth_local"), ("adequacy", "rev_adeq"), ("otherstate", "rev_ostate"), ("federal", "rev_fed")):
    chk("revenue %s FY18" % k, rv[k]["av"], doe25.D[2018][f], 1)
    chk("revenue %s FY25" % k, rv[k]["bv"], doe25.D[2025][f], 1)
chk("revenue lines add to total FY18", sum(r["av"] for r in C["bridge"]["revenue"]), doe25.D[2018]["rev_tot"], 1)
chk("revenue lines add to total FY25", sum(r["bv"] for r in C["bridge"]["revenue"]), doe25.D[2025]["rev_tot"], 1)
chk("revenue increase shares add to 100%", sum(pn(r["inc_share"]) for r in C["bridge"]["revenue"]), 100.0, 0.3)
chk("local property tax equals the school levy from the DOE values files FY25", doe25.D[2025]["rev_local"], b["levy_tot"], 1)
# 3. baseline and cards, recomputed
bl = {x["id"]: x for x in C["baseline"]}
chk("levy FY18", bl["levy"]["av"], a["levy_tot"], 1); chk("levy FY25", bl["levy"]["bv"], b["levy_tot"], 1)
chk("enrollment", bl["enr"]["bv"], b["enrollment"], 0)
chk("tax rate FY25", bl["rate"]["bv"], 1000 * b["levy_tot"] / b["eq_tot"], 0.001)
cards = {c["id"]: {s["label"]: s for s in c["stats"]} for c in C["cards"]}
st = cards["state"]
chk("state share FY18", st["State aid, share of district revenue"]["av"], 100 * (doe25.D[2018]["rev_adeq"] + doe25.D[2018]["rev_ostate"]) / doe25.D[2018]["rev_tot"], 0.001)
chk("state share FY25", st["State aid, share of district revenue"]["bv"], 100 * (doe25.D[2025]["rev_adeq"] + doe25.D[2025]["rev_ostate"]) / doe25.D[2025]["rev_tot"], 0.001)
chk("state aid per student FY25", st["State aid per student"]["bv"], (doe25.D[2025]["rev_adeq"] + doe25.D[2025]["rev_ostate"]) / 2097, 0.01)
chk("retirement contributions FY25", st["Retirement system contributions paid by the district"]["bv"], b["nhrs_con"], 1)
ad = cards["admin"]["Administration and business spending"]
chk("administration FY18", ad["av"], doe25.D[2018]["gab"] + doe25.D[2018]["sadm"] + doe25.D[2018]["bus"], 1)
chk("administration FY25", ad["bv"], doe25.D[2025]["gab"] + doe25.D[2025]["sadm"] + doe25.D[2025]["bus"], 1)
spd = cards["sped"]["Special programs spending"]
chk("special programs FY18", spd["av"], doe25.D[2018]["spec"], 1); chk("special programs FY25", spd["bv"], doe25.D[2025]["spec"], 1)
ds = cards["debt"]["Interest plus principal paid"]
chk("debt service FY25", ds["bv"], doe25.D[2025]["bint"] + doe25.D[2025]["prin"], 1)
chk("bond principal owed FY25", cards["debt"]["Bond principal still owed at year end"]["bv"], 43780000, 1)
cp = cards["enrollment"]["Cost per pupil (NH DOE)"]
chk("cost per pupil FY25", cp["bv"], doe25.D[2025]["cpp"], 0.5)
lee = cards["towns"]["Share of the school levy: Lee"]
chk("Lee share FY25", lee["bv"], 100 * b["levy_lee"] / (b["levy_dur"] + b["levy_lee"] + b["levy_mad"]), 0.001)
chk("levy towns add to the district FY25", b["levy_dur"] + b["levy_lee"] + b["levy_mad"], b["levy_tot"], 1)
efa = cards["efa"]["Accounts held by residents of the three towns"]
chk("EFA accounts FY26", efa["bv"], sum((R[2026][k] or 0) for k in ("efa_dur", "efa_lee", "efa_mad")), 0.001)
print("%d checks, %d differences" % (n, bad))
sys.exit(1 if bad else 0)
