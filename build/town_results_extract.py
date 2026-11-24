#!/usr/bin/env python3
"""Extract Oyster River results by town of residence from the NH DOE 'by town responsible' assessment workbooks.

Reads (raw/nh-doe, mirrored; see raw/MANIFEST.csv):
  2022, 2023, 2024  disagdata2022_2023_2024_bytownresponsible_static.xlsx   (2024 also in disagdata2024bytownresponsible_static.xlsx)
  2025              publicdatabytown.xlsx
  2026              disagdatabytownresponsible_2026_0.xlsx
Keeps District Level rows for 'Oyster River Coop', Grade 'All grades', Subgroup 'All students', for the towns Durham, Lee and
Madbury (Barrington's few tuition students are kept too, for the district tie-out).  Writes build/town_results.json:
  {year: {town: {subject: {"n": [low, high], "prof": percent or null, "sgp": number or null, "part": percent or null}}}}
'prof' is the share at levels 3 and 4; the DOE suppresses very small cells ('* n < 11'), which become null.
Needs openpyxl.   python3 build/town_results_extract.py            writes the JSON
                  python3 build/town_results_extract.py --check    re-reads the workbooks and compares with the JSON (exit 1 on a difference)
"""
import json, os, re, sys, warnings
warnings.filterwarnings("ignore")
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "raw", "nh-doe")
FILES = {
    "2022-2024": "inline-documents__sonh__disagdata2022_2023_2024_bytownresponsible_static.xlsx",
    "2024-only": "inline-documents__sonh__disagdata2024bytownresponsible_static.xlsx",
    "2025": "inline-documents__sonh__publicdatabytown.xlsx",
    "2026": "inline-documents__2026__disagdatabytownresponsible_2026_0.xlsx",
}
TOWNS = ("Durham", "Lee", "Madbury", "Barrington")


def num(v):
    try:
        return float(str(v).replace(",", "").strip())
    except ValueError:
        return None


def rng(s):
    m = re.match(r"\s*([\d,]+)\s*-\s*([\d,]+)", str(s))
    return [int(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))] if m else None


def read():
    out = {}
    for tag, f in FILES.items():
        ws = openpyxl.load_workbook(os.path.join(RAW, f), read_only=True, data_only=True).active
        for i, r in enumerate(ws.iter_rows(values_only=True)):
            if i == 0 or r[3] != "Oyster River Coop" or r[1] != "District Level":
                continue
            if str(r[6]) != "All grades" or str(r[7]).strip() != "All students" or r[2] not in TOWNS:
                continue
            rec = {"n": rng(r[8]), "prof": num(r[13]), "sgp": num(r[14]), "part": num(r[15])}
            cell = out.setdefault(str(r[0]), {}).setdefault(r[2], {})
            if r[5] in cell:
                assert cell[r[5]] == rec, ("duplicate rows disagree", tag, r[0], r[2], r[5], cell[r[5]], rec)
            cell[r[5]] = rec
    return out


if __name__ == "__main__":
    data = read()
    p = os.path.join(HERE, "town_results.json")
    if "--check" in sys.argv:
        old = json.load(open(p))
        same = json.loads(json.dumps(data)) == old
        print("town_results.json matches the workbooks" if same else "DIFFERENT from the workbooks")
        sys.exit(0 if same else 1)
    json.dump(data, open(p, "w"), indent=1, sort_keys=True)
    print("wrote", p, {y: sorted(t) for y, t in sorted(data.items())})
