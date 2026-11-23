#!/usr/bin/env python3
"""Check every DOE-25 value on the page against the workbooks in raw/nh-doe25/ (needs openpyxl).

 1. the hand-typed District Profile values in build/doe25.py (D) against the 'District Profile' sheet of each year's workbook;
 2. the rows built by build/doe25_rows.py (General Fund by type, fund equity by fund, instructional pay, spending by school)
    against a fresh, independent read of the same workbooks, and against each other (tie-outs).
Run from the repo root:  python3 build/verify_doe25.py [--dir raw/nh-doe25]
Exit status 1 if anything differs by more than 50 cents."""
import glob, json, os, re, sys, warnings
warnings.filterwarnings("ignore")
import openpyxl
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
import doe25, doe25_rows

DIR = sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else "raw/nh-doe25"
IDS = {2018: 131, 2019: 306, 2020: 484, 2021: 544, 2022: 946, 2023: 1131, 2024: 2221, 2025: 2414}
bad, ok = [], 0


def chk(what, a, b, tol=0.5):
    global ok
    if a is None or b is None or abs(a - b) > tol:
        bad.append((what, a, b))
    else:
        ok += 1


def num(c):
    return c if isinstance(c, (int, float)) and not isinstance(c, bool) else None


PROFILE = [  # (label prefix, key); longest prefix first
    ("total recurring expenditures", "rec"), ("total expenditures", "tot"), ("total revenues", "rev_tot"),
    ("regular education", "reg"), ("special programs", "spec"), ("vocational programs", "voc"), ("other instructional programs", "oi"),
    ("student support services", "ss"), ("instructional staff support", "isup"), ("gen", "gab"), ("school administration", "sadm"),
    ("business services", "bus"), ("plant operations", "plant"), ("transportation", "trans"), ("bond interest", "bint"),
    ("food service", "food"), ("facility construction", "constr"), ("bonds & notes principal", "prin"), ("local property tax", "rev_local"),
    ("tuition, food", "rev_oth_local"), ("state foundation", "rev_adeq"), ("other state aid", "rev_ostate"), ("federal aid", "rev_fed"),
]


def profile(ws):
    out = {}
    for r in ws.iter_rows(values_only=True):
        cells = [c for c in r if c is not None]
        lab = next((str(c).strip().lower() for c in cells if isinstance(c, str) and re.search(r"[a-z]{4}", c.lower()) and not re.fullmatch(r"[\d,&+\-\s]+", c)), None)
        if lab is None:
            continue
        if lab.startswith("district total"):
            out["cpp"] = num(cells[-1]) if num(cells[-1]) is not None else next((num(c) for c in cells if num(c) is not None), None)
            continue
        if "administration & business" in lab:
            k = "gab"
        else:
            k = next((k for p, k in PROFILE if lab.startswith(p) and p != "gen"), None)
        if k and k not in out:
            v = next((num(c) for c in cells if num(c) is not None and not (isinstance(c, str))), None)
            vs = [num(c) for c in cells if isinstance(c, (int, float))]
            # first numeric after the label text; a leading numeric function code (1100, 2100...) is skipped
            i = next(i for i, c in enumerate(cells) if isinstance(c, str) and c.strip().lower() == lab)
            after = [num(c) for c in cells[i + 1:] if num(c) is not None]
            out[k] = after[0] if after else None
    return out


def find(ws, prefix, hdr=None):
    """rows of the DOE25 sheet whose column-A text starts with prefix"""
    return [[c.value for c in row] for row in ws.iter_rows(min_col=1, max_col=14) if isinstance(row[0].value, str) and row[0].value.strip().upper().startswith(prefix.upper())]


def vals(row):
    return [c for c in row[1:] if isinstance(c, (int, float)) and not isinstance(c, bool)]


W = {}
for y, i in IDS.items():
    f = glob.glob(os.path.join(DIR, "*id%d.xlsx" % i))
    if not f:
        sys.exit("missing workbook for FY%d in %s" % (y, DIR))
    W[y] = openpyxl.load_workbook(f[0], data_only=True)

# ---- 1. typed District Profile values
for y in IDS:
    P = profile(W[y]["District Profile"])
    for k, v in doe25.D[y].items():
        if k in P:
            chk("profile %s FY%d" % (k, y), v, P[k])
        else:
            bad.append(("profile %s FY%d not found in workbook" % (k, y), v, None))

# ---- 2. rows from doe25_rows.py against an independent read
R = doe25_rows.fields()
for y in IDS:
    wb = W[y]
    ws = wb["DOE25"]
    g = find(ws, "Total Expenditures General Fund")
    assert len(g) == 1
    gv = vals(g[0])[-7:]
    for k, v in zip(("gfo_sal", "gfo_ben", "gfo_pur", "gfo_sup", "gfo_prop", "gfo_oth", "gfo_tot"), gv):
        chk("%s FY%d" % (k, y), R[k][y], v)
    chk("General Fund parts add to total FY%d" % y, sum(R[k][y] for k in ("gfo_sal", "gfo_ben", "gfo_pur", "gfo_sup", "gfo_prop", "gfo_oth")), R["gfo_tot"][y])
    # fund equity statement: first three fund columns (General, Food Service, Special Revenue) of each line
    FE = {}
    for row in ws.iter_rows(min_col=1, max_col=14):
        a = row[0].value
        if row[0].row > 440 and isinstance(a, str):
            u = a.strip().upper()
            for tag, pat in (("beg", "TOTAL FUND EQUITY, JULY 1"), ("add", "TOTAL ADDITIONS"), ("del", "TOTAL DELETIONS"), ("end", "TOTAL FUND EQUITY JUNE 30")):
                if u.startswith(pat):
                    FE[tag] = [c.value if isinstance(c.value, (int, float)) else 0.0 for c in row[5:8]]
    assert set(FE) == {"beg", "add", "del", "end"}, (y, sorted(FE))
    for j, f in enumerate(("gen", "food", "spr")):
        chk("fe_%s_beg FY%d" % (f, y), R["fe_%s_beg" % f][y], FE["beg"][j])
        chk("fe_%s_rev FY%d" % (f, y), R["fe_%s_rev" % f][y], FE["add"][j])
        chk("fe_%s_exp FY%d" % (f, y), R["fe_%s_exp" % f][y], FE["del"][j])
        chk("fe_%s_end FY%d" % (f, y), R["fe_%s_end" % f][y], FE["end"][j])
        # tie-out: opening + additions - deletions = closing
        chk("fe_%s roll-forward FY%d" % (f, y), R["fe_%s_beg" % f][y] + R["fe_%s_rev" % f][y] - R["fe_%s_exp" % f][y], R["fe_%s_end" % f][y], 0.5)
        if y > 2018:
            chk("fe_%s opening FY%d = closing FY%d" % (f, y, y - 1), R["fe_%s_beg" % f][y], R["fe_%s_end" % f][y - 1], 0.5)
    # food service fund against the Food Service Attachment W (FY2020 on)
    if "Food Service Attachment W" in wb.sheetnames:
        fs = wb["Food Service Attachment W"]
        for row in fs.iter_rows(values_only=True):
            t = " ".join(str(c) for c in row if isinstance(c, str))
            n = [c for c in row if isinstance(c, (int, float))]
            if n and t.strip().startswith("Fund Equity End of Year"):
                chk("food service equity (Attachment W) FY%d" % y, R["fe_food_end"][y], n[0], 0.5)
            if n and t.strip().startswith("Total Expenditures"):
                chk("food service expenditures (Attachment W) FY%d" % y, R["fe_food_exp"][y], n[0], 5.0)
    # General Fund equity components add to the total; trust funds read independently
    chk("GF equity components add to total FY%d" % y, sum(R[k][y] for k in ("fb_prep", "fb_vote", "fb_enc", "fb_ret", "fb_una")), R["fe_gen_end"][y], 1.0)
    chk("trust-fund equity FY%d" % y, R["fb_trust"][y], [c.value for c in next(row for row in ws.iter_rows(min_col=1, max_col=14) if row[0].row < 60 and isinstance(row[0].value, str) and row[0].value.strip() == "Total Fund Equity")[5:10]][4])
    # special education detail: page 21 total (line 21), special-program tuition (page 22), revenue accounts 3230 / 4570 / 4580
    p21 = [row for row in ws.iter_rows(min_col=1, max_col=14) if str(row[1].value).strip() == "21" and str(row[2].value).strip() == "21"]
    assert len(p21) == 1, (y, len(p21))
    chk("special education page 21 total FY%d" % y, R["rsd_sub"][y], [c.value for c in p21[0][3:14] if isinstance(c.value, (int, float))][-1])
    tui = 0.0
    for row in ws.iter_rows(min_col=1, max_col=14):
        if isinstance(row[0].value, str) and row[0].value.strip().startswith(("Special Program Tuition", "Special Program Residential")):
            n = [c.value for c in row[1:14] if isinstance(c.value, (int, float))]
            tui += n[-1] if n else 0.0
    chk("special-program tuition FY%d" % y, R["rsd_tui"][y], tui)
    for acct, k in (("3230", "rsd_aid"), ("4570", "rsd_idea"), ("4580", "rsd_med")):
        m = [row for row in ws.iter_rows(min_col=1, max_col=14) if str(row[4].value).strip() == acct and 100 < row[0].row < 175]
        assert len(m) == 1, (y, acct, len(m))
        chk("%s FY%d" % (k, y), R[k][y], sum(c.value for c in m[0][5:10] if isinstance(c.value, (int, float))))
    # the district's RSA 32:11-a revenue total (FY2023-FY2025 reports) equals the DOE-25 revenue lines
    if y in (2023, 2024, 2025):
        import rc_data
        chk("district RSA table revenue = DOE-25 revenue lines FY%d" % y, rc_data._RSA[y][8], R["rsd_rev"][y], 1.0)
    # Salaries-Benefits: per-block class sums tie to block totals, and four blocks tie to the Profile's instruction pay
    sb = wb["Salaries-Benefits"]
    tot = [0.0, 0.0]
    cls = [0.0, 0.0]
    for row in sb.iter_rows(values_only=True):
        t = next((c.strip().lower() for c in row if isinstance(c, str)), "")
        n = [c for c in row if isinstance(c, (int, float))]
        if t == "totals" and len(n) >= 2:
            tot[0] += n[0]; tot[1] += n[1]
    chk("instructional salaries, four blocks, FY%d" % y, sum(R["pers_%s_sal" % c][y] for c in "tao"), tot[0], 1.0)
    chk("instructional benefits, four blocks, FY%d" % y, sum(R["pers_%s_ben" % c][y] for c in "tao"), tot[1], 1.0)
    if y in (2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025):
        o = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "orcsd_years.json")))["rows"][y - 2018]
        chk("pers salaries = page instr_sal FY%d" % y, sum(R["pers_%s_sal" % c][y] for c in "tao"), o["instr_sal"], 1.5)
        chk("pers benefits = page instr_ben FY%d" % y, sum(R["pers_%s_ben" % c][y] for c in "tao"), o["instr_ben"], 1.5)
    # School Level Expenditures: each school's state/local + federal = its grand total
    if "School Level Expenditures" in wb.sheetnames:
        sl = wb["School Level Expenditures"]
        seen = {}
        for ri, row in enumerate(sl.iter_rows(values_only=True), 1):
            nm = row[0] if isinstance(row[0], str) else ""
            low = nm.strip().lower()
            if ri < 60 and (low in ("mast way school", "moharimet school") or low.startswith("oyster river")) and not low.startswith("oyster river coop"):
                n = [c for c in row[3:9] if isinstance(c, (int, float))]
                if n:
                    seen[low] = n[-1] if len(n) >= 3 else n[0]
        key = {"sch_mw": "mast way school", "sch_mo": "moharimet school", "sch_ms": "oyster river middle school", "sch_hs": "oyster river high school", "sch_ps": "oyster river preschool education program"}
        for k, nm in key.items():
            if nm in seen:
                chk("%s FY%d" % (k, y), R[k][y], seen[nm])
            elif R[k].get(y) is not None:
                bad.append(("%s FY%d present in rows but not in workbook" % (k, y), R[k][y], None))

print("checked ok: %d   differences: %d" % (ok, len(bad)))
for b in bad:
    print("DIFF", *b)
sys.exit(1 if bad else 0)
