#!/usr/bin/env python3
"""Extract every New Hampshire town's equalized school and total tax rates from the NH DOE 'Valuations, Property Tax Assessments
and Tax Rates of School Districts' files (one per tax year, 2017 to 2025), and write build/town_rates.json.

Source files (raw/nh-doe, mirrored; see raw/MANIFEST.csv): values2017.pdf, values2018.csv, equalized-values-2019.csv,
values-2020-revised_0.csv, values-2021.xlsx, values-2022.csv, values-2023.csv, values-report-for-web.xlsx (2024),
values-report-2025.csv (2026 folder).  Each lists school districts and, under multi-town districts, their member towns; a
single-town district is one row whose district code equals its location code.  Columns used: (3) equalized valuation of school
districts for local taxes, and the equalized tax rate per $1,000: local education (col 20) and total (col 23).

JSON: {tax_year: {TOWN NAME: [equalized valuation, equalized local education rate, equalized total rate]}}
Needs openpyxl and pypdf (the 2017 file is a PDF).
   python3 build/town_rates_extract.py            writes the JSON
   python3 build/town_rates_extract.py --check    re-reads the files and compares with the JSON (exit 1 on a difference)
"""
import csv, json, os, re, sys, warnings
warnings.filterwarnings("ignore")
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "raw", "nh-doe")
FILES = {2018: "inline-documents__values2018.csv", 2019: "inline-documents__sonh__equalized-values-2019.csv",
         2020: "inline-documents__sonh__values-2020-revised_0.csv", 2021: "inline-documents__sonh__values-2021.xlsx",
         2022: "inline-documents__sonh__values-2022.csv", 2023: "inline-documents__sonh__values-2023.csv",
         2024: "inline-documents__sonh__values-report-for-web.xlsx", 2025: "inline-documents__2026__values-report-2025.csv"}
PDF2017 = "inline-documents__values2017.pdf"


def num(c):
    try:
        return float(str(c).replace(",", "").strip())
    except ValueError:
        return None


def table(f):
    if f.endswith(".xlsx"):
        ws = openpyxl.load_workbook(os.path.join(RAW, f), read_only=True, data_only=True).active
        return [list(r) for r in ws.iter_rows(values_only=True)]
    return list(csv.reader(open(os.path.join(RAW, f), encoding="utf-8-sig", newline="")))


def towns(f):
    out = {}
    for r in table(f):
        c = [("" if x is None else str(x).strip()) for x in r] + [""] * 26
        if not re.fullmatch(r"\d+", c[0]) or not re.fullmatch(r"\d+", c[1]):
            continue
        town = c[3] or (c[2] if c[0] == c[1] else "")      # member town row, or a single-town district
        loc, tot, val = num(c[20]), num(c[23]), num(c[6])
        if not town or loc is None or tot is None or val is None:
            continue
        key = town.upper()
        if key in out and out[key][0] >= val:
            continue
        out[key] = [round(val), loc, tot]
    return out


def towns_2017(names):
    from pypdf import PdfReader
    out = {}
    for p in PdfReader(os.path.join(RAW, PDF2017)).pages:
        for line in p.extract_text().splitlines():
            m = re.match(r"^([A-Z][A-Z .'&-]+?) ((?:[\d,]+(?:\.\d+)? ){14}[\d,]+(?:\.\d+)?)\s*$", line.strip())
            if not m or m.group(1) not in names:
                continue
            v = [num(x) for x in m.group(2).split()]
            if len(v) == 15:
                key = m.group(1)
                if key not in out or out[key][0] < v[2]:
                    out[key] = [round(v[2]), v[11], v[14]]
    return out


def read():
    data = {y: towns(f) for y, f in FILES.items()}
    data[2017] = towns_2017(set(data[2018]))
    return {str(y): data[y] for y in sorted(data)}


if __name__ == "__main__":
    data = read()
    p = os.path.join(HERE, "town_rates.json")
    if "--check" in sys.argv:
        same = json.loads(json.dumps(data)) == json.load(open(p))
        print("town_rates.json matches the files" if same else "DIFFERENT from the files")
        sys.exit(0 if same else 1)
    json.dump(data, open(p, "w"), separators=(",", ":"), sort_keys=True)
    for y, t in data.items():
        print(y, len(t), t.get("DURHAM"), t.get("LEE"), t.get("MADBURY"))
