#!/usr/bin/env python3
"""Check towns_data.FILES (equalized valuation + ADM-R for Durham, Lee, Madbury) against the DOE's
machine-readable "equalized valuation per pupil" CSVs mirrored in raw/nh-doe/ (equal_pupil*, eqprt*, EVPP*).
Run from the repo root:  python3 build/verify_towns_eqprt.py
Every FILES entry must be found in exactly the CSV(s) listed; a difference prints MISMATCH and exits 1."""
import csv, glob, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from towns_data import FILES

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PAT = ["equal_pupil*", "equal-pupil*", "eqprt*", "EVPP*"]
TOWNS = ("DURHAM", "LEE", "MADBURY")

def num(s):
    s = re.sub(r"[^0-9.]", "", s or "")
    return float(s) if s else None

def read(path):
    """-> {town: (equalized valuation, ADM-R)} for the three towns, from the rows that follow the OYSTER RIVER COOP row
    (older files have no CTY/SAU/DIS/LOC columns, so the row is found by name, not by district number)."""
    out = {}; in_block = False
    with open(path, newline="", encoding="latin-1") as f:
        for r in csv.reader(f):
            cells = [c.strip().upper().replace("(", "").strip() for c in r]
            name = next((c for c in cells[:6] if c and not c.replace(" ", "").isdigit()), "")
            if name.startswith("OYSTER RIVER COOP"):
                in_block = True; continue
            if in_block and name in TOWNS:
                vals = [num(c) for c in r if num(c) is not None and re.search(r"\d{2,}", c)]
                vals = [v for v in vals][-3:] if len(vals) >= 3 else vals
                if len(vals) >= 2:
                    out[name] = (vals[0], vals[1])
            elif in_block and name and name not in TOWNS:
                in_block = False
    return out

files = []
for p in PAT:
    files += glob.glob(os.path.join(ROOT, "raw", "nh-doe", "*" + p + ".csv")) + glob.glob(os.path.join(ROOT, "raw", "nh-doe", "*__" + p + ".csv"))
files = sorted(set(files))
data = {os.path.basename(p): read(p) for p in files}
data = {k: v for k, v in data.items() if len(v) == 3}
bad = 0
for fy, (fv, adm) in sorted(FILES.items()):
    want = {t: (fv[i], adm[i]) for i, t in enumerate(TOWNS)}
    hit = [k for k, v in data.items() if all(abs(v[t][0] - want[t][0]) < 1 and abs(v[t][1] - want[t][1]) < 0.005 for t in TOWNS)]
    print(fy, "OK  " if hit else "MISMATCH", ", ".join(hit) or "no CSV matches these values")
    bad += not hit
extra = {}
for k, v in sorted(data.items()):
    if not any(all(abs(v[t][0] - FILES[fy][0][i]) < 1 for i, t in enumerate(TOWNS)) for fy in FILES):
        extra[k] = v
for k, v in extra.items():
    print("not in FILES:", k, {t: v[t] for t in TOWNS})
print("files read:", len(data), "| FILES entries:", len(FILES), "| mismatches:", bad)
sys.exit(1 if bad else 0)
