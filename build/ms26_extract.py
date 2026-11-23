#!/usr/bin/env python3
"""Extract the NH DRA MS-26 (Proposed Budget: Appropriations and Estimates of Revenue) that the 2025 and 2026 ORCSD annual reports reprint as page images
(pages 16-20) into build/ms26_tables.json.  Needs `pdftoppm` and `tesseract` (OCR at 250 dpi, --psm 6); the OCR text is also checked: every subtotal is re-added from its lines.
Report Y covers expenditures for FY Y-1 (actual), appropriations FY Y (approved), proposed FY Y+1; revenues: actual FY Y-1, revised estimate FY Y, estimate FY Y+1.
Run from the repo root:  python3 build/ms26_extract.py"""
import json, os, re, subprocess, sys, tempfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SECTIONS = ["Instruction", "Support Services", "General Administration", "Executive Administration", "Non-Instructional Services", "Facilities Acquisition and Construction", "Other Outlays", "Fund Transfers",
            "Special Warrant Articles", "Individual Warrant Articles", "Local Sources", "State Sources", "Federal Sources", "Other Financing Sources"]
LEAD = {"Instruction": "1", "Support Services": "2", "General Administration": "2", "Executive Administration": "2", "Non-Instructional Services": "3", "Facilities Acquisition and Construction": "4", "Other Outlays": "5", "Fund Transfers": "5"}
# OCR misreads that the page's own subtotal exposes (a 1 read as 4); each is confirmed by re-adding the section: 3,573,674 + 150,000 + 1,249,628 + 30,000 = 5,003,302
OVERRIDE = {(2025, "revenue", "1500-1599"): {2: 150000.0}}
VAL = r"\$\s?[\dOo][\d,]*"

def ocr(y, page):
    pdf = os.path.join(ROOT, "raw", "orcsd", "Annual_Reports__%d_ORCSD_Annual_Report.pdf" % y)
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-r", "250", "-f", str(page), "-l", str(page), "-png", pdf, os.path.join(d, "p")], check=True)
        png = [f for f in os.listdir(d) if f.endswith(".png")][0]
        return subprocess.run(["tesseract", os.path.join(d, png), "-", "--psm", "6"], capture_output=True, text=True).stdout

def v(s): return float(s.replace("$", "").replace(" ", "").replace(",", "").replace("O", "0").replace("o", "0"))

def parse(y, page, txt, out):
    sec = None; part = "revenue" if "Revenues" in txt.split("\n", 1)[0] or "Revised" in txt[:300] else "appropriations"
    last = None
    for ln in txt.splitlines():
        s = re.sub(r"\$(\d{1,3}) (\d{3})\b", r"$\1,\2", ln.strip().replace("§", "5").replace("«", " "))      # OCR: 'sixes' and thousands separators
        s = re.sub(r"[\"“”'‘’]\s?(\d{2,3},\d{3})\b", r"$\1", s)                                 # a dollar sign read as a quote mark
        for n in SECTIONS:
            if s.startswith(n) and not re.search(VAL, s) or s == n:
                sec = n; break
        if s.startswith("Purpose:") and last is not None:
            last["purpose_note"] = s[8:].strip(); continue
        vals = re.findall(VAL, s)
        if not vals: continue
        head = re.split(VAL, s, maxsplit=1)[0].strip()
        sub = re.match(r"(.*Subtotal|Total [A-Za-z ]+)$", head)
        m = re.match(r"^(\d{4}(?:-\d{4})?)\s*(?:\(\d+\))?\s*[=_|~—-]*\s*(.*?)(?:\s+(\d{3}))?$", head)
        part = "revenue" if sec in ("Local Sources", "State Sources", "Federal Sources", "Other Financing Sources") else "appropriations"
        rec = {"report": y, "pdf_page": page, "part": part, "section": sec, "values": [v(x) for x in vals]}
        if sub: rec.update(kind="subtotal", label=head)
        elif m:
            acct = m.group(1)
            if sec in LEAD and acct[0] != LEAD[sec]: acct = LEAD[sec] + acct[1:]      # OCR reads a leading 1 as 4
            if "-" in acct:
                a, b = acct.split("-"); b = (LEAD.get(sec, b[0]) + b[1:]) if sec in LEAD else b; acct = a + "-" + b
            rec.update(kind="line", account=acct, purpose=m.group(2).strip(" _|~—-=:"), article=m.group(3))
        else: continue
        k = (y, rec.get("account"), rec.get("article") or "")
        for i, x in OVERRIDE.get((y, part, rec.get("account")), {}).items(): rec["values"][i] = x; rec["ocr_corrected"] = True
        out.append(rec); last = rec

def main():
    out = {"lines": []}
    for y in (2025, 2026):
        for pg in (17, 18, 19, 20, 21):
            txt = ocr(y, pg)
            if not re.search(r"Appropriations|Revenues|Warrant Articles", txt[:400]): continue
            parse(y, pg, txt, out["lines"])
    # self-check: subtotals re-added from their lines
    bad = 0
    for y in (2025, 2026):
        cur = []; 
        for r in [x for x in out["lines"] if x["report"] == y]:
            if r["kind"] == "line": cur.append(r)
            elif r["kind"] == "subtotal" and cur:
                n = len(r["values"]); sec_lines = [c for c in cur if c["section"] == r["section"] and len(c["values"]) == n]
                if r["label"].endswith("Subtotal") and sec_lines:
                    sm = [sum(c["values"][i] for c in sec_lines) for i in range(n)]
                    ok = all(abs(a - b) < 1.5 for a, b in zip(sm, r["values"]))
                    r["check"] = "ok" if ok else "MISMATCH"
                    if not ok: bad += 1; print("MISMATCH", y, r["section"], r["values"], sm)
                cur = [c for c in cur if c["section"] != r["section"]]
    json.dump(out, open(os.path.join(ROOT, "build", "ms26_tables.json"), "w"), indent=0)
    print(len(out["lines"]), "records;", bad, "subtotal mismatches")

if __name__ == "__main__":
    main()
