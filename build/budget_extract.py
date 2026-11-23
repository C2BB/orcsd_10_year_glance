#!/usr/bin/env python3
"""Extract the budget tables printed in the ORCSD annual reports (raw/orcsd/Annual_Reports__<year>_ORCSD_Annual_Report.pdf) into build/budget_tables.json:
  dept   - "General Fund Budget Comparison / ORCSD FY nn Budget Summary by Location" (2018-2024 reports; text pages): General Fund by department, three columns
           (expended = actual two years back, approved = current year, proposed = next year), FY = year the school year ends.
  funds  - the operating-budget warrant article's split by fund (Fund 10 general, 21 food service, 22 federal, 23 pass-through) and the default budget (2018-2026 reports)
  tax    - the estimated tax-rate impact per $1,000 for Durham, Lee and Madbury that the warrant explanation prints for the operating budget (where printed)
Needs `pdftotext`. Run from the repo root:  python3 build/budget_extract.py [--check]"""
import json, os, re, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
REPORTS = range(2018, 2027)
DEPTS = [("Mast Way", "mastway"), ("Moharimet", "moharimet"), ("Middle School", "middle"), ("High School", "high"), ("Special Ed", "specialed"), ("SAU/ADM", "sau"),
         ("Transportation", "transport"), ("Technology", "technology"), ("Facilities", "facilities"), ("TOTAL", "total"), ("Debt Service", "debt"), ("Food Service", "food")]

def pages(y):
    p = os.path.join(ROOT, "raw", "orcsd", "Annual_Reports__%d_ORCSD_Annual_Report.pdf" % y)
    t = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout
    return [x.replace("‐", "-").replace("‑", "-").replace("–", "-") for x in t.split("\f")]

def num(s):
    s = s.replace("$", "").replace(",", "").strip()
    neg = s.startswith("(") or s.startswith("-")
    s = s.strip("()-")
    return -float(s) if neg else float(s)

def dept(y, pg, out):
    for i, p in enumerate(pg):
        if "Budget Summary by Location" not in p: continue
        lines = p.split("Budget Summary by Location", 1)[1].splitlines()
        hdr = next((l for l in lines if re.search(r"\d{4}/\d{2}", l)), "")
        yrs = re.findall(r"(\d{4})/(\d{2})", hdr)                   # e.g. 2016/17 2017/18 2018/19
        if len(yrs) < 3: continue
        fys = [int(a) + 1 for a, b in yrs[:3]]
        for l in lines:
            m = re.match(r"\s*(Mast Way|Moharimet|Middle School|High School|Special Ed|SAU/ADM\w*|Transportation|Technology|Facilities|TOTAL)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s", l)
            if not m: continue
            key = "sau" if m.group(1).startswith("SAU") else dict(DEPTS)[m.group(1)]
            for kind, fy, v in zip(("expended", "approved", "proposed"), fys, (m.group(2), m.group(3), m.group(4))):
                out["dept"].append({"report": y, "dept": key, "kind": kind, "fy": fy, "value": num(v), "pdf_page": i + 1})
        return

def funds(y, pg, out):
    txt = re.sub(r"[\uf000-\uf0ff\u2022]", " ", "\n".join(pg))
    # warrant breakdown (2019-2025): "Fund 10 General Fund $x / Fund 21 Food Service $x / Fund 22 Federal Funds $x / Fund 23 Pass Through $x / Total $x Default $x"
    m = re.search(r"Operating Budget for (\d{4})-(\d\d) consists of:\s*Fund 10 General Fund\s+\$\s*([\d,]+)\s*Fund 21 Food Service\s+\$\s*([\d,]+)\s*Fund 22 Federal Funds\s+\$\s*([\d,]+)\s*Fund 23 Pass Through\s+\$\s*([\d,]+)\s*Total\s+\$\s*([\d,]+)\s+Default\s+\$\s*([\d,]+)", txt)
    where = None
    if m:
        fy = int(m.group(1)) + 1
        v = [num(x) for x in m.groups()[2:]]
        where = next(i + 1 for i, p in enumerate(pg) if "Operating Budget for" in p and "consists of" in p)
    else:
        # ballot text (2018, 2026): "totaling $T ... (Default Budget) ... Fund 10 = $a ... Fund 21 = $b ... Fund 22 = $c ... Fund 23 = $d"
        m2 = re.search(r"totaling \$\s*([\d,]+)\.?\s*Should this article be\s+defeated, the operating budget shall be \$\s*([\d,]+)\s*\(Default Budget\)", txt)
        m3 = re.search(r"Fund 10\s*=\s*\$\s*([\d,]+)[^;]*;\s*Fund 21\s*=\s*\$\s*([\d,]+)[^;]*;\s*Fund 22\s*=\s*\$\s*([\d,]+)[^;]*;\s*Fund 23\s*=\s*\$\s*([\d,]+)", txt)
        if not (m2 and m3): return
        fy = y + 1
        v = [num(m3.group(1)), num(m3.group(2)), num(m3.group(3)), num(m3.group(4)), num(m2.group(1)), num(m2.group(2))]
        where = next(i + 1 for i, p in enumerate(pg) if "(Default Budget)" in p)
    out["funds"].append({"report": y, "fy": fy, "general_fund": v[0], "food_service": v[1], "federal": v[2], "pass_through": v[3], "total": v[4], "default": v[5], "pdf_page": where})

def nums(s):
    o = []
    for m in re.finditer(r"\(?-?\$?\s*(-?[\d,]*\.?\d+)\)?%?", s):
        try: o.append(float(m.group(1).replace(",", "")))
        except ValueError: pass
    return o

def tax(y, pg, out):
    """'Tax Rate Impacts & Apportionment' (2018-2024 reports) and 'Estimated Tax Impact' (2025-2026): the district's projected tax-rate impact of the proposed budget, by town.
    Report Y: current column = FY Y (tax year Y-1), proposed column = FY Y+1. Assessed value is held fixed in both columns, so the 'impact' is the budget's effect alone."""
    for i, p in enumerate(pg):
        if "LOCAL property tax rate" not in p or "net assessed value" not in p: continue
        k = p.index("Tax Rate Impact:") if "Tax Rate Impact:" in p else 0
        seg = p[k:]
        # apportionment block (before the rate block), if on this page
        app = p[:k]
        for town, nxt in (("Durham", "Lee"), ("Lee", "Madbury"), ("Madbury", None)):
            if nxt: m = re.search(town + r"\s*\n([\s\S]*?)(?=\n\s*" + nxt + r")", seg)
            else: m = re.search(town + r"\s*\n([\s\S]*?)(?=House Valued|\Z)", seg)
            if not m: continue
            b = m.group(1)
            def f(label):
                mm = re.search(label + r"([^\n]*)", b); return nums(mm.group(1)) if mm else None
            rec = {"report": y, "town": town.lower(), "fy_cur": y, "fy_prop": y + 1, "pdf_page": i + 1,
                   "nav": f("net assessed value"), "local_rate": f("LOCAL property tax rate"), "state_rate": f("STATE school rate")}
            # apportionment %, apportioned $, state grant, state tax, kindergarten aid, net to apportion (2018-2024)
            ma = re.search(r"\n\s*" + town + r"\s+([\d.]+)%\s+([\d.]+)%([\s\S]*?)(?=\n\s*(?:Lee|Madbury|Tax Rate Impact))", app)
            if ma:
                blk = ma.group(3)
                g = lambda lab: (nums(re.search(lab + r"([^\n]*)", blk).group(1)) if re.search(lab + r"([^\n]*)", blk) else None)
                rec.update(app_pct=[float(ma.group(1)), float(ma.group(2))], apportioned=g("apportioned \\$"), state_grant=g("less state grant \\$"), state_tax=g("less state tax \\$"),
                           kg_aid=g("[Ll]ess kindergarten aid"), net=g("net to apportion \\$"))
            out["tax"].append(rec)
        # house tax impact (2025-2026 reports): $300,000 / $600,000 / $900,000 homes, current vs proposed
        mh = re.search(r"House Valued at[\s\S]*", seg)
        if mh:
            town = None
            for ln in mh.group(0).splitlines():
                t = re.match(r"\s*(Durham|Lee|Madbury)\s*$", ln)
                if t: town = t.group(1).lower(); continue
                mv = re.match(r"\s*\$([\d,]+)\s+\$([\d,]+)\s+\$([\d,]+)\s+(\()?\$([\d,]+)\)?", ln)
                if mv and town:
                    v = [float(x.replace(",", "")) for x in (mv.group(1), mv.group(2), mv.group(3), mv.group(5))]; v[3] = -v[3] if mv.group(4) else v[3]
                    out.setdefault("house", []).append({"report": y, "town": town, "house_value": v[0], "tax_current": v[1], "tax_proposed": v[2], "impact": v[3], "fy_cur": y, "fy_prop": y + 1, "pdf_page": i + 1})
        return

def main():
    out = {"dept": [], "funds": [], "tax": []}
    for y in REPORTS:
        pg = pages(y)
        dept(y, pg, out); funds(y, pg, out); tax(y, pg, out)
    json.dump(out, open(os.path.join(ROOT, "build", "budget_tables.json"), "w"), indent=0)
    print(len(out["dept"]), "dept records;", len(out["funds"]), "fund records;", len(out["tax"]), "tax records;", len(out.get("house", [])), "house records")
    for f in out["funds"]: print(f)
    tot = {(r["report"], r["kind"]): r["value"] for r in out["dept"] if r["dept"] == "total"}
    print(sorted(tot.items()))

if __name__ == "__main__":
    main()
