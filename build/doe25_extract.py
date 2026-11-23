#!/usr/bin/env python3
"""Extract every numeric line of the NH DOE-25 workbooks for Oyster River (raw/nh-doe25/DOE25_id*.xlsx, FY2018-FY2025) into build/doe25_all.json.
Sheets: 'DOE25' (the whole annual financial report: balance sheet, revenues, expenditures by function x object x fund, special education, transportation, ...), 'Salaries-Benefits',
'School Level Expenditures' (Oyster River schools only), 'Food Service Attachment W', 'ESEA OTHER TITLE PROGRAMS', 'Indirect Cost Rate', 'MS-25' (balance sheet by fund).
Each record: fy, sheet, row (spreadsheet row), label, page/line/acct (the form's own page and line numbers), hdr (the column-header row in force), values (cells right of the label, None for blanks).
Needs openpyxl.  Run from the repo root:  python3 build/doe25_extract.py [--dir raw/nh-doe25]"""
import json, os, re, sys, warnings
warnings.filterwarnings("ignore")
import openpyxl

IDS = {2018: 131, 2019: 306, 2020: 484, 2021: 544, 2022: 946, 2023: 1131, 2024: 2221, 2025: 2414}
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

def num(c):
    return round(float(c), 2) if isinstance(c, (int, float)) and not isinstance(c, bool) else None

def main_sheet(ws, fy, out):
    hdr = None
    for i, r in enumerate(ws.iter_rows(values_only=True), 1):
        lab = r[0].strip() if isinstance(r[0], str) else None
        vals = [num(c) for c in r[5:14]]
        if lab and sum(isinstance(c, str) and c.strip() in ("Salaries", "Employee Benefits", "Purchased Services", "Supplies", "Property", "Other", "Total", "Fund 10", "Fund 21", "Fund 22", "Fund 30", "Fund 70") for c in r[:14]) >= 3:
            hdr = lab; continue
        if not lab or not any(v is not None for v in vals): continue
        out.append(dict(fy=fy, sheet="DOE25", row=i, label=lab, page=str(r[1]).strip() if r[1] is not None else None, line=r[2] if isinstance(r[2], int) else None,
                        acct=r[4] if isinstance(r[4], int) else None, hdr=hdr, values=vals))

def table_sheet(ws, fy, name, out, ncols, only=None):
    for i, r in enumerate(ws.iter_rows(values_only=True), 1):
        cells = list(r[:ncols])
        lab = next((c.strip() for c in cells if isinstance(c, str) and c.strip()), None)
        vals = [num(c) for c in cells]
        if lab and any(v is not None for v in vals) and (only is None or only(cells)):
            out.append(dict(fy=fy, sheet=name, row=i, label=lab, values=vals, text=[c if isinstance(c, str) else None for c in cells]))

def main():
    d = os.path.join(ROOT, "raw", "nh-doe25")
    if "--dir" in sys.argv: d = sys.argv[sys.argv.index("--dir") + 1]
    out = []
    for fy, i in IDS.items():
        wb = openpyxl.load_workbook(os.path.join(d, "DOE25_id%d.xlsx" % i), data_only=True)
        main_sheet(wb["DOE25"], fy, out)
        for sheet, name, nc in (("Salaries-Benefits", "Salaries-Benefits", 3), ("Food Service Attachment W", "Food Service", 3), ("ESEA OTHER TITLE PROGRAMS", "ESEA", 5), ("CARES", "CARES", 6),
                                ("Indirect Cost Rate", "Indirect Cost Rate", 8), ("MS-25", "MS-25", 8)):
            if sheet in wb.sheetnames: table_sheet(wb[sheet], fy, name, out, nc)
        if "District & DOE Notes" in wb.sheetnames:                      # the district's and the DOE's own notes on the filing (page, line, note)
            for r_i, r in enumerate(wb["District & DOE Notes"].iter_rows(values_only=True), 1):
                t = [c for c in r[:4] if isinstance(c, str) and c.strip()]
                if len(t) >= 1 and any(isinstance(c, (int, float)) for c in r[:2]) or (len(t) >= 1 and r_i > 5 and len(t[-1]) > 25):
                    out.append(dict(fy=fy, sheet="Notes", row=r_i, label=t[-1].strip(), page=r[0], line=r[1]))
        if "School Level Expenditures" not in wb.sheetnames: continue
        ws = wb["School Level Expenditures"]
        # only Oyster River's own schools: 'Oyster River ...' / 'Mast Way' / 'Moharimet' (the sheet is statewide below the district's own rows)
        for r_i, r in enumerate(ws.iter_rows(values_only=True), 1):
            nm = r[0] if isinstance(r[0], str) else None
            if nm and (nm.startswith("Oyster River") or nm.strip().lower() in ("mast way school", "moharimet school") or nm.startswith("Out of District")) and r_i < 60:
                out.append(dict(fy=fy, sheet="School Level", row=r_i, label=nm.strip(), school_id=r[1], values=[num(c) for c in r[3:9]] + [num(c) for c in r[10:17]],
                                text=["state_local, federal, grand_total, (check cols), then instruction 1000, support 2100, instr staff 2200, school admin 2400, teacher salaries, aide salaries, books"]))
        # the district's own header row for the same sheet (instruction/support/admin/salaries/aides/books totals)
    json.dump(out, open(os.path.join(ROOT, "build", "doe25_all.json"), "w"), separators=(",", ":"))
    import collections
    print(len(out), "records", dict(collections.Counter((r["sheet"]) for r in out)))

if __name__ == "__main__":
    main()
