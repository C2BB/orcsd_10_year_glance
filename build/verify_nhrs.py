"""Independent check of build/nhrs_rows.py against the mirrored NHRS PDFs in raw/nhrs/.

For every measurement year (2017-2025) and both plans (GASB 68 pension, GASB 75 retiree health) it extracts the text of the PDF
with pdftotext, takes the lines for "Oyster River Coop SD" and confirms that each value typed in nhrs_rows.py appears on them:
  GASB 68: share %, contribution, net pension liability, total deferred outflows, total deferred inflows, total pension expense
           (and that the last three figures on the amounts line add up: share of plan expense + amortization = total expense)
  GASB 75: share %, contribution, net OPEB liability, total OPEB expense
It also confirms that the audited net pension liability (build/audit_metrics.json) for FY2018 to FY2024 equals the NHRS figure.

Run from the repo root:  python3 build/verify_nhrs.py --dir raw/nhrs        (needs pdftotext from poppler)
"""
import argparse, glob, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import nhrs_rows

ap = argparse.ArgumentParser()
ap.add_argument("--dir", default=os.path.join(HERE, "..", "raw", "nhrs"))
a = ap.parse_args()

NUM = re.compile(r"\(?-?\$?\d[\d,]*(?:\.\d+)?\)?%?")


def tokens(text):
    out = set()
    for m in NUM.findall(text):
        neg = m.startswith("(")
        t = m.strip("()$%").replace(",", "").replace("$", "")
        if t in ("", "-"):
            continue
        try:
            v = float(t)
        except ValueError:
            continue
        out.add(("%" if m.endswith("%") else "n", -v if neg else v))
    return out


def orcsd_text(path):
    txt = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    lines = txt.splitlines()
    got = []
    for i, ln in enumerate(lines):
        if re.search(r"Oyster River Coop", ln, re.I):
            got.append(ln + " " + (lines[i + 1] if i + 1 < len(lines) and not re.search(r"[A-Za-z]{4}", lines[i + 1]) else ""))
    return got


files = {}
for p in glob.glob(os.path.join(a.dir, "gasb*_*__*.pdf")):
    b = os.path.basename(p)
    files[(b[:6], int(b[7:11]))] = p

F = nhrs_rows.fields()
bad = 0
n = 0


def check(label, lines, want):
    global bad, n
    tok = set()
    for ln in lines:
        tok |= tokens(ln)
    for name, kind, v in want:
        n += 1
        ok = (kind, round(v, 8)) in {(k, round(x, 8)) for k, x in tok}
        if not ok:
            bad += 1
            print("MISSING", label, name, v)


for my in nhrs_rows.measurement_years():
    fy = my + 1
    g = lambda k: F[k][fy]
    p68 = files.get(("gasb68", my))
    p75 = files.get(("gasb75", my))
    assert p68 and p75, ("missing pdf", my)
    L68 = orcsd_text(p68)
    L75 = orcsd_text(p75)
    check("gasb68 %d" % my, L68, [("share", "%", g("nhrs_share")), ("contribution", "n", g("nhrs_con")), ("NPL", "n", g("nhrs_npl")),
                                  ("deferred outflows", "n", g("nhrs_do")), ("deferred inflows", "n", -g("nhrs_di")), ("expense", "n", g("nhrs_exp"))])
    check("gasb75 %d" % my, L75, [("share", "%", g("nhrs_oshare")), ("contribution", "n", g("nhrs_ocon")), ("NOL", "n", g("nhrs_onl")), ("expense", "n", g("nhrs_oexp"))])
    # the amounts line ends with: share of plan expense, net amortization, total expense
    amt = [ln for ln in L68 if re.search(r"\d[\d,]{6,}\s", ln) and str(f"{g('nhrs_npl'):,.0f}") in ln]
    n += 1
    if len(amt) != 1:
        bad += 1
        print("NO AMOUNTS LINE", my)
    else:
        nums = [float(x.strip("()").replace(",", "")) * (-1 if x.startswith("(") else 1) for x in re.findall(r"\(?[\d,]+\)?", amt[0].replace("%", " ")) if re.search(r"\d", x)]
        last3 = nums[-3:]
        n += 1
        if abs(last3[0] + last3[1] - last3[2]) > 1 or last3[2] != g("nhrs_exp"):
            bad += 1
            print("EXPENSE ROLL FAIL", my, last3, g("nhrs_exp"))

audit = json.load(open(os.path.join(HERE, "audit_metrics.json")))
for y, v in audit.items():
    n += 1
    if v["net_pension"]["v"] != F["nhrs_npl"][int(y)]:
        bad += 1
        print("AUDIT != NHRS", y, v["net_pension"]["v"], F["nhrs_npl"][int(y)])

print("%d checks, %d problems" % (n, bad))
sys.exit(1 if bad else 0)
