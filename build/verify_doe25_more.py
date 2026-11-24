#!/usr/bin/env python3
"""Check the DOE-25 tuition, transportation and bond-schedule rows (build/doe25_rows.py) against an independent read of
the workbooks in raw/nh-doe25/, and against each other.  Needs openpyxl.  Run from the repo root:
    python3 build/verify_doe25_more.py
Exit status 1 if anything differs by more than a dollar (except the documented exception below)."""
import os, re, sys, warnings
warnings.filterwarnings("ignore")
import openpyxl
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import doe25_rows

DIR = "raw/nh-doe25"
IDS = {2018: 131, 2019: 306, 2020: 484, 2021: 544, 2022: 946, 2023: 1131, 2024: 2221, 2025: 2414}
bad, ok = [], 0


def chk(what, a, b, tol=1.0):
    global ok
    if a is None or b is None or abs(a - b) > tol:
        bad.append((what, a, b))
    else:
        ok += 1


def nums(row):
    return [c.value for c in row[1:14] if isinstance(c.value, (int, float)) and not isinstance(c.value, bool)]


R = doe25_rows.fields()
beg_total = {}
for y, i in IDS.items():
    ws = openpyxl.load_workbook("%s/DOE25_id%d.xlsx" % (DIR, i), data_only=True)["DOE25"]
    tui = {"Regular": 0.0, "Special": 0.0, "Vocational": 0.0, "SpecialPrivate": 0.0}
    n_tui = 0
    last = {}
    for row in ws.iter_rows(min_col=1, max_col=14):
        a = row[0].value
        if not isinstance(a, str):
            continue
        t = a.strip()
        m = re.match(r"(Regular|Special|Vocational) Program Tuition to (.+)$", t)
        if m:
            n = nums(row)
            v = n[-1] if n else 0.0
            n_tui += 1
            tui[m.group(1)] += v
            if m.group(1) == "Special" and m.group(2).startswith("Private"):
                tui["SpecialPrivate"] += v
            continue
        for key, pat in (("reg", "Regular To and From"), ("sped", "All Special Education Transportation"),
                         ("voc", "Vocational Education Transportation"), ("intra", "Intra-District Transportation"),
                         ("oth", "Other Transportation"),
                         ("rp", "Remaining Principal Balance Due"), ("ri", "Remaining Interest Balance Due"),
                         ("np", "Amount of Principal to be Paid Next Fiscal Year"), ("ni", "Amount of Interest to be Paid Next Fiscal Year"),
                         ("nt", "Total Debt Next Fiscal Year"), ("bp", "Principal at Beginning of Year")):
            if t.startswith(pat):
                assert key not in last, (y, key)
                last[key] = nums(row)
    assert n_tui == 12, (y, n_tui)
    chk("tuit_reg FY%d" % y, R["tuit_reg"][y], tui["Regular"])
    chk("tuit_voc FY%d" % y, R["tuit_voc"][y], tui["Vocational"])
    chk("tuit_priv FY%d" % y, R["tuit_priv"][y], tui["SpecialPrivate"])
    chk("tuit_spub FY%d" % y, R["tuit_spub"][y], tui["Special"] - tui["SpecialPrivate"])
    chk("tuit_tot FY%d" % y, R["tuit_tot"][y], sum(tui[k] for k in ("Regular", "Special", "Vocational")))
    chk("tuition equals the special-education tuition already on the page (rsd_tui) FY%d" % y, R["tuit_priv"][y] + R["tuit_spub"][y], R["rsd_tui"][y])
    # transportation: the last number of each row is the total for that trip type
    tr = lambda k: (last[k][-1] if last[k] else 0.0)
    chk("trans_reg FY%d" % y, R["trans_reg"][y], tr("reg"))
    chk("trans_sped FY%d" % y, R["trans_sped"][y], tr("sped"))
    chk("trans_voc FY%d" % y, R["trans_voc"][y], tr("voc"))
    chk("trans_oth FY%d" % y, R["trans_oth"][y], tr("intra") + tr("oth"))
    chk("trans_tot FY%d" % y, R["trans_tot"][y], tr("reg") + tr("sped") + tr("voc") + tr("intra") + tr("oth"))
    # bond schedule: last number = total column; the issue columns add to it; principal plus interest = total due
    for k, f in (("rp", "bond_prin"), ("ri", "bond_int"), ("np", "ds_prin"), ("ni", "ds_int"), ("nt", "ds_tot")):
        chk("%s FY%d" % (f, y), R[f][y], last[k][-1])
    chk("issue principals add to total FY%d" % y, sum(R["bond_p%d" % s][y] for s in range(1, 6)), R["bond_prin"][y])
    chk("issue payments add to total FY%d" % y, sum(R["ds_n%d" % s][y] for s in range(1, 6)), R["ds_tot"][y])
    chk("principal + interest due = total due FY%d" % y, R["ds_prin"][y] + R["ds_int"][y], R["ds_tot"][y])
    beg_total[y] = last["bp"][-1]
# roll-forward: this year's opening principal equals last year's closing principal (documented exceptions: FY2022 and FY2025)
for y in range(2019, 2026):
    if y == 2022:
        chk("FY2022 opening principal is $1,020,000 below FY2021 closing (DOE-25 filing inconsistency, issue 5)", beg_total[y] - R["bond_prin"][y - 1], -1020000.0)
    elif y == 2025:
        chk("FY2025 opening principal is $150,000 below FY2024 closing (DOE-25 filing: the $1.5M issue shows two annual payments, issue 1)", beg_total[y] - R["bond_prin"][y - 1], -150000.0)
    else:
        chk("opening principal FY%d = closing FY%d" % (y, y - 1), beg_total[y], R["bond_prin"][y - 1])
print("%d checks, %d differences" % (ok, len(bad)))
for b in bad:
    print("DIFF", b)
sys.exit(1 if bad else 0)
