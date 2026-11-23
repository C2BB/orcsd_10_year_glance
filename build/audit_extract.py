#!/usr/bin/env python3
"""Extract the headline numbers from the district's audited financial statements (raw/orcsd/Audit_Reports__<FY>_ORCSD_Audit_Report.pdf, FY2018-FY2024)
into build/audit_metrics.json: one record per fiscal year, each value with its PDF page. Needs `pdftotext` (poppler). Run from the repo root:
    python3 build/audit_extract.py            # writes build/audit_metrics.json and prints a table
    python3 build/audit_extract.py --check    # also checks each year's values: general fund balance vs rc_data.py, net position = capital + restricted + unrestricted, balance-sheet sums; exit 1 on any miss
FY key = year ended June 30. Values are as printed (dollars). Government-wide figures are accrual basis; "fund" figures are modified accrual (governmental funds)."""
import json, os, re, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
YEARS = range(2018, 2025)
NUM = re.compile(r"\(?\$?\s?\d[\d,]*(?:\.\d+)?\)?|(?<![\w-])--(?![\w-])")

def pdf_pages(fy):
    p = os.path.join(ROOT, "raw", "orcsd", "Audit_Reports__%d_ORCSD_Audit_Report.pdf" % fy)
    t = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout
    return [pg.replace("‐", "-").replace("‑", "-").replace("–", "-") for pg in t.split("\f")]

def nums(line):
    out = []
    for m in NUM.finditer(line):
        s = m.group(0).strip()
        if s == "--": out.append(0.0); continue
        neg = s.startswith("(") and s.endswith(")")
        v = float(re.sub(r"[^\d.]", "", s) or 0)
        out.append(-v if neg else v)
    return out

def find_page(pages, pat, start=0, skip_toc=True):
    for i in range(start, len(pages)):
        if i < 3 and skip_toc: continue
        if re.search(pat, pages[i], re.M | re.I): return i
    return None

def grab(pages, pg, label, col=0, after=None, occurrence=0):
    """First number columns on the line that starts with `label` (regex) on page index pg; col -1 = last column."""
    if pg is None: return None
    lines = pages[pg].splitlines(); seen = 0
    for k, ln in enumerate(lines):
        if after and not re.search(after, "\n".join(lines[:k + 1]), re.I): continue
        if re.match(r"\s*(?:" + label + r")\b", ln, re.I):
            # drop footnote-ish page numbers: need at least one number after the label text
            n = nums(re.sub(r"^\s*[A-Za-z][^\d(\-$]*", "", ln))
            if not n: continue
            if seen < occurrence: seen += 1; continue
            return (n[col], pg + 1)
    return None

def extract(fy):
    pg = pdf_pages(fy); r = {}
    def put(k, v):
        if v is not None: r[k] = {"v": v[0], "pdf_page": v[1]}
    # --- statement of net position (government-wide, accrual)
    i = find_page(pg, r"^\s*STATEMENT OF NET POSITION\s*$")
    j = i
    for lab, key in [(r"Cash and short-term investments", "cash"), (r"Net pension liability", "net_pension"), (r"Net OPEB liability", "net_opeb"),
                     (r"Net investment in capital assets", "net_inv_capital"), (r"Unrestricted", "net_unrestricted"),
                     (r"Total Net Position", "net_position")]:
        for p in (i, i + 1 if i is not None else None):
            v = grab(pg, p, lab)
            if v: put(key, v); break
    # bonds: label differs by year ("Bonds payable" through 2020; "Bonds and loans payable" from 2021)
    cur = nonc = None
    for p in (i, i + 1 if i is not None else None):
        for ln in (pg[p].splitlines() if p is not None else []):
            if re.match(r"\s*Bonds( and loans)? payable,? net of current portion", ln, re.I): nonc = nonc or (nums(ln)[0], p + 1)
            elif re.match(r"\s*Bonds( and loans)? payable\s+[\$\d(]", ln, re.I): cur = cur or (nums(ln)[0], p + 1)
    put("bonds_current", cur); put("bonds_noncurrent", nonc)
    # capital assets: sum of the capital lines on the statement (land/CIP + other, or ROU + other)
    cap = 0; capp = None
    for p in (i,):
        if p is None: continue
        inblock = False
        for ln in pg[p].splitlines():
            if re.match(r"\s*Capital assets", ln, re.I): inblock = True; continue
            if inblock and re.match(r"\s*(Land and construction in progress|Right-to-use|Other (capital )?assets|Other assets, net)", ln, re.I):
                n = nums(re.sub(r"^\s*[A-Za-z][^\d(\-$]*", "", ln)) ; cap += n[0] if n else 0; capp = p + 1
            elif inblock and re.match(r"\s*(Total|Deferred|Liabilities)", ln, re.I): break
    if capp: r["capital_assets"] = {"v": cap, "pdf_page": capp}
    # --- government-wide activities
    a = find_page(pg, r"^\s*STATEMENT OF ACTIVITIES\s*$")
    v = grab(pg, a, r"Total Governmental Activities", col=0); put("expenses_total", v)
    v = grab(pg, a, r"Total Governmental Activities", col=1); put("charges_for_services", v)
    v = grab(pg, a, r"Total Governmental Activities", col=2); put("operating_grants", v)
    for lab, key in [(r"Property taxes", "property_taxes"), (r"Tuition", "tuition_revenue"), (r"Investment income", "investment_income"),
                     (r"Interest expense", "interest_expense"), (r"Instruction", "exp_instruction")]:
        put(key, grab(pg, a, lab, col=0 if key != "interest_expense" and key != "exp_instruction" else 0))
    put("change_net_position", grab(pg, a, r"Change in Net Position"))
    # --- governmental funds balance sheet (general fund = first column, total = last)
    b = find_page(pg, r"^\s*BALANCE SHEET\s*$")
    for lab, key in [(r"Nonspendable", "fb_nonspendable"), (r"Restricted", "fb_restricted"), (r"Committed", "fb_committed"),
                     (r"Assigned", "fb_assigned"), (r"Unassigned", "fb_unassigned"), (r"Total Fund Balances", "fb_total")]:
        v = grab(pg, b, lab, col=0)
        if v: put("gf_" + key, v)
    v = grab(pg, b, r"Total Fund Balances", col=-1); put("govfunds_fb_total", v)
    # --- governmental funds revenues and expenditures (total column = last)
    s = find_page(pg, r"STATEMENT OF REVENUES, EXPENDITURES, AND\s*\n?\s*CHANGES IN FUND BALANCES", )
    if s is not None and not re.search(r"^\s*Revenues", pg[s], re.M): s += 1
    for lab, key in [(r"Property taxes", "f_property_taxes"), (r"Tuition", "f_tuition"), (r"Intergovernmental", "f_intergovernmental"),
                     (r"Charges for services", "f_charges"), (r"Total Revenues", "f_revenues_total"), (r"Instruction", "f_exp_instruction"),
                     (r"Student", "f_exp_student"), (r"Instructional staff", "f_exp_instr_staff"), (r"General administration", "f_exp_gen_admin"),
                     (r"School administration", "f_exp_school_admin"), (r"Business", "f_exp_business"), (r"Operation and maintenance", "f_exp_operations"),
                     (r"Student transportation", "f_exp_transport"), (r"Principal", "f_debt_principal"), (r"Interest", "f_debt_interest"),
                     (r"Capital outlay", "f_capital_outlay"), (r"Total Expenditures", "f_expenditures_total")]:
        v = grab(pg, s, lab, col=-1)
        if v: put(key, v)
    # general-fund column (first number column) for the two totals, and debt service ("Debt service" on one line in FY2018-19; principal + interest after)
    put("gf_revenues_total", grab(pg, s, r"Total Revenues", col=0)); put("gf_expenditures_total", grab(pg, s, r"Total Expenditures", col=0))
    ds = grab(pg, s, r"Debt service", col=0)
    if ds and ds[0]: put("gf_debt_service", ds)
    elif "f_debt_principal" in r and "f_debt_interest" in r:
        pr, it = grab(pg, s, r"Principal", col=0), grab(pg, s, r"Interest", col=0)
        if pr and it: put("gf_debt_service", (pr[0] + it[0], pr[1]))
    co = grab(pg, s, r"Capital outlay", col=0)
    if co: put("gf_capital_outlay", co)
    return r, pg

def main():
    out = {}
    for fy in YEARS:
        out[fy], _ = extract(fy)
    json.dump(out, open(os.path.join(ROOT, "build", "audit_metrics.json"), "w"), indent=1, sort_keys=True)
    keys = sorted({k for r in out.values() for k in r})
    print("%-22s" % "field", *["FY%d" % y for y in YEARS], sep=" ")
    for k in keys:
        print("%-22s" % k, *[("%12s" % ("{:,.0f}".format(out[y][k]["v"]) if k in out[y] else "-")) for y in YEARS])

def check(out):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from rc_data import RC
    bad = 0
    for fy, r in out.items():
        g = lambda k: r[k]["v"] if k in r else None
        t = []
        for k, rk in (("gf_fb_total", "fb_tot"), ("gf_fb_unassigned", "fb_un"), ("gf_fb_committed", "fb_com")):
            t.append((k + " = rc_data " + rk, g(k) == RC[rk].get(fy)))
        # net position = net investment in capital + restricted + unrestricted; the implied restricted part (a plug, not printed on every page here) must be small and positive
        implied = g("net_position") - g("net_inv_capital") - g("net_unrestricted")
        t.append(("implied restricted net position between 0 and $5M", 0 <= implied < 5e6))
        t.append(("bonds, pension and OPEB all found", all(g(k) for k in ("bonds_noncurrent", "net_pension", "net_opeb", "net_position"))))
        t.append(("total revenues and expenditures found", all(g(k) for k in ("f_revenues_total", "f_expenditures_total"))))
        for name, ok in t:
            if not ok: bad += 1; print("MISMATCH FY%d %s" % (fy, name))
    print("audit_extract --check: %d mismatches" % bad)
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
    if "--check" in sys.argv: check({fy: extract(fy)[0] for fy in YEARS})
