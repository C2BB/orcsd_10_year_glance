#!/usr/bin/env python3
"""Parse the "Annual Report Card" tables (Section II) of the ORCSD annual reports, 2018 to 2026 (raw/orcsd/Annual_Reports__<year>_ORCSD_Annual_Report.pdf),
into long-form records: build/annual_report_tables.json  [{report, table, metric, period, fy, entity, value, pdf_page}, ...].
Every table is printed with the district value next to the state value ("Source: NH Dept. of Education ..." on most), and each report reprints several
years, so the same metric-year appears in several reports; build/conflicts.py compares those vintages and compares them with the state's own files.
Needs `pdftotext` (poppler). Run from the repo root:  python3 build/annual_extract.py
FY key = year the school year ends ("17/18" -> 2018). Enrollment, SAT, special education and similar tables carry the October 1 / test-year label as printed."""
import json, os, re, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
REPORTS = range(2018, 2027)
NUM = re.compile(r"\$?\(?-?\d[\d,]*\.?\d*\)?|(?<![\d])\.\d+")

def pages(year):
    p = os.path.join(ROOT, "raw", "orcsd", "Annual_Reports__%d_ORCSD_Annual_Report.pdf" % year)
    t = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout
    return [x.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("’", "'") for x in t.split("\f")]

def nums(s):
    out = []
    for m in NUM.finditer(s):
        tok = m.group(0).replace("$", "").replace(",", "").replace("(", "-").replace(")", "")
        try: out.append(float(tok))
        except ValueError: pass
    return out

def fy_of(label):
    """'17/18' or '17-18' -> 2018; '2019' -> 2019 (as printed)."""
    m = re.fullmatch(r"(\d\d)[/-](\d\d)", label)
    if m: return 2000 + int(m.group(2))
    if re.fullmatch(r"20\d\d", label): return int(label)
    return None

def year_header(lines, start, maxlook=8):
    """First line at/after start with >= 3 period tokens -> (index, [labels])."""
    for k in range(start, min(start + maxlook, len(lines))):
        toks = re.findall(r"\b(?:\d\d[/-]\d\d|20\d\d)\b", lines[k])
        if len(toks) >= 3: return k, toks
    return None, []

def table(pg, title, rows, pairs, report, name, page_no, out, stop=r"^\s*Source:", maxper=None):
    """rows: [(label regex, metric)]; pairs: values come as District, State per period."""
    lines = pg.splitlines()
    t0 = next((i for i, l in enumerate(lines) if re.search(title, l, re.I)), None)
    if t0 is None: return False
    h, labs = year_header(lines, t0)
    if h is None: return False
    if maxper: labs = labs[:maxper]
    n = len(labs)
    for k in range(h + 1, min(h + 25, len(lines))):
        ln = lines[k]
        if re.search(stop, ln): break
        for rx, metric in rows:
            m = re.match(r"\s*(" + rx + r")\b", ln, re.I)
            if m:
                tail = re.split(r"\s{3,}(?:Mast Way|Moharimet|Middle|High)\b", ln[m.end():])[0]   # the ratio table shares its lines with Teacher Experience
                v = nums(tail)
                want = n * 2 if pairs else n
                labs_i = labs
                if pairs and len(v) == 2 * (n + 1) and name in ("cost_per_pupil",):
                    # the report prints one more column than its header names (2026 report): the last column is the year after the last label
                    last = fy_of(labs[-1]); nxt = "%02d/%02d" % ((last - 2001 + 1) % 100, (last - 2000 + 1) % 100)
                    labs_i = labs + [nxt]; want = len(v)
                if len(v) != want:
                    out.append({"report": report, "table": name, "metric": metric, "period": "PARSE?", "fy": None, "entity": "", "value": None,
                                "pdf_page": page_no, "raw": ln.strip()[:160]})
                    break
                for j, lab in enumerate(labs_i):
                    if pairs:
                        out.append({"report": report, "table": name, "metric": metric, "period": lab, "fy": fy_of(lab), "entity": "district", "value": v[2 * j], "pdf_page": page_no})
                        out.append({"report": report, "table": name, "metric": metric, "period": lab, "fy": fy_of(lab), "entity": "state", "value": v[2 * j + 1], "pdf_page": page_no})
                    else:
                        out.append({"report": report, "table": name, "metric": metric, "period": lab, "fy": fy_of(lab), "entity": "district", "value": v[j], "pdf_page": page_no})
                break
    return True

def find(pgs, title):
    for i, p in enumerate(pgs):
        if re.search(title, p, re.I) and i > 20 - 8: return i
    return None

def sat(pg, report, page_no, out):
    """Rows 'YYYY ORHS NH National ORHS NH National' (reading and writing, math); older rows split verbal / math / writing (<=2016)."""
    sec = re.split(r"Verbal \(Reading\)", pg)[0]
    for ln in sec.splitlines():
        m = re.match(r"\s*(20\d\d)\s+(.*)$", ln)
        if not m: continue
        v = nums(m.group(2))
        if len(v) == 6:
            for ent, rw, ma in (("district", v[0], v[3]), ("state", v[1], v[4]), ("national", v[2], v[5])):
                out.append({"report": report, "table": "sat", "metric": "sat_rw", "period": m.group(1), "fy": int(m.group(1)), "entity": ent, "value": rw, "pdf_page": page_no})
                out.append({"report": report, "table": "sat", "metric": "sat_math", "period": m.group(1), "fy": int(m.group(1)), "entity": ent, "value": ma, "pdf_page": page_no})

def spec_ed(pg, report, page_no, out):
    lines = pg.splitlines()
    t0 = next((i for i, l in enumerate(lines) if re.search(r"Special Education Statistics", l)), None)
    if t0 is None: return
    h, labs = year_header(lines, t0 + 1, 6)
    if h is None: return
    names = [("Elementary", "sped_elem"), ("Middle School", "sped_middle"), ("High School", "sped_high"), (r"Ages 3-5", "sped_ood_3_5"), (r"Ages 6-21", "sped_ood_6_21"), ("Totals", "sped_total")]
    for k in range(h + 1, min(h + 14, len(lines))):
        for rx, metric in names:
            m = re.match(r"\s*(" + rx + r")\b", lines[k])
            if m:
                v = nums(lines[k][m.end():])
                if len(v) != len(labs):
                    out.append({"report": report, "table": "special_ed", "metric": metric, "period": "PARSE?", "fy": None, "entity": "", "value": None, "pdf_page": page_no, "raw": lines[k].strip()[:160]})
                else:
                    for lab, x in zip(labs, v):
                        out.append({"report": report, "table": "special_ed", "metric": metric, "period": lab, "fy": int(lab) + 1, "entity": "district", "value": x, "pdf_page": page_no})
                break

def enrollment(pg, report, page_no, out):
    lines = pg.splitlines()
    t0 = next((i for i, l in enumerate(lines) if re.search(r"Official Enrollment Counts", l)), None)
    if t0 is None: return
    h, labs = year_header(lines, t0 + 1, 6)
    if h is None: return
    for k in range(h + 1, min(h + 8, len(lines))):
        for rx, metric in (("Kindergarten", "enr_k"), ("Elementary", "enr_elem"), ("Middle", "enr_middle"), ("High School", "enr_high"), ("Totals", "enr_total")):
            m = re.match(r"\s*(" + rx + r")\b", lines[k])
            if m:
                v = nums(lines[k][m.end():])
                if len(v) == len(labs):
                    for lab, x in zip(labs, v):
                        out.append({"report": report, "table": "enrollment", "metric": metric, "period": lab, "fy": fy_of(lab), "entity": "district", "value": x, "pdf_page": page_no})
                else:
                    out.append({"report": report, "table": "enrollment", "metric": metric, "period": "PARSE?", "fy": None, "entity": "", "value": None, "pdf_page": page_no, "raw": lines[k].strip()[:160]})
                break

def class_size(pg, report, page_no, out):
    lines = pg.splitlines()
    t0 = next((i for i, l in enumerate(lines) if re.search(r"Average Class Size", l)), None)
    if t0 is None: return
    h, labs = year_header(lines, t0)
    if h is None: return
    band = None
    for k in range(h + 1, min(h + 12, len(lines))):
        ln = lines[k]
        if re.search(r"Source:", ln): break
        m = re.match(r"\s*(?:Gr (1&2|3&4)\s+)?(Mast Way|Moharimet|Middle School)\s+(.*)$", ln)
        if not m: continue
        if m.group(1): band = m.group(1)
        school = m.group(2)
        metric = "class_%s_%s" % ("middle" if school == "Middle School" else ("g" + band.replace("&", "") ), "" if school == "Middle School" else school.lower().replace(" ", ""))
        metric = metric.rstrip("_")
        v = nums(m.group(3))
        if len(v) != 2 * len(labs):
            out.append({"report": report, "table": "class_size", "metric": metric, "period": "PARSE?", "fy": None, "entity": "", "value": None, "pdf_page": page_no, "raw": ln.strip()[:160]})
            continue
        for j, lab in enumerate(labs):
            out.append({"report": report, "table": "class_size", "metric": metric, "period": lab, "fy": fy_of(lab), "entity": "district", "value": v[2 * j], "pdf_page": page_no})
            out.append({"report": report, "table": "class_size", "metric": metric, "period": lab, "fy": fy_of(lab), "entity": "state", "value": v[2 * j + 1], "pdf_page": page_no})

def teacher_exp(pg, report, page_no, out):
    """'Teacher Experience': staff with 14+ years, by school, 4 periods; printed to the right of the Student-to-Teacher-Ratio table."""
    lines = pg.splitlines()
    t0 = next((i for i, l in enumerate(lines) if re.search(r"Teacher Experience", l)), None)
    if t0 is None: return
    h, labs = year_header(lines, t0)
    if h is None or len(labs) < 8: return
    labs = labs[-4:]
    for k in range(h + 1, min(h + 8, len(lines))):
        m = re.search(r"\s{2,}(Mast Way|Moharimet|Middle|High)\s+([\d\s]+)$", lines[k])
        if m:
            v = nums(m.group(2))
            if len(v) == 4:
                for lab, x in zip(labs, v):
                    out.append({"report": report, "table": "teacher_experience", "metric": "exp14_" + m.group(1).lower().replace(" ", ""), "period": lab, "fy": fy_of(lab), "entity": "district", "value": x, "pdf_page": page_no})

def school_year_enrollment(pg, report, page_no, out):
    """'YYYY-YYYY School Year Enrollment' (October 1, by school and grade, last column = school total)."""
    m = re.search(r"(20\d\d)-(20\d\d) School Year Enrollment", pg)
    if not m: return
    fy = int(m.group(2)); lines = pg.split(m.group(0), 1)[1].splitlines()
    for ln in lines[:12]:
        mm = re.match(r"\s*(Mast Way|Moharimet|Middle|High|Totals)\b(.*)$", ln)
        if mm:
            v = re.findall(r"\d[\d,]*", mm.group(2).replace("X", " "))
            if v:
                key = {"Mast Way": "sye_mastway", "Moharimet": "sye_moharimet", "Middle": "sye_middle", "High": "sye_high", "Totals": "sye_total"}[mm.group(1)]
                out.append({"report": report, "table": "school_year_enrollment", "metric": key, "period": "%d-%d" % (fy - 1, fy), "fy": fy, "entity": "district",
                            "value": float(v[-1].replace(",", "")), "pdf_page": page_no, "grades": [int(x.replace(",", "")) for x in v[:-1]]})

def votes(pg, report, page_no, out):
    for m in re.finditer(r"Article\s+(\d+)\s+(.+?)\s{2,}([\d,]+)\s+([\d,]+)\s+(Passed|Failed|Defeated)", pg):
        out.append({"report": report, "table": "vote", "metric": "article_%s" % m.group(1), "period": m.group(2).strip(), "fy": None, "entity": "yes", "value": float(m.group(3).replace(",", "")), "pdf_page": page_no})
        out.append({"report": report, "table": "vote", "metric": "article_%s" % m.group(1), "period": m.group(2).strip(), "fy": None, "entity": "no", "value": float(m.group(4).replace(",", "")), "pdf_page": page_no})

def main():
    out = []
    for y in REPORTS:
        pgs = pages(y)
        for i, pg in enumerate(pgs):
            pn = i + 1
            if re.search(r"High School SAT Scores", pg): sat(pg, y, pn, out); spec_ed(pg, y, pn, out)
            if re.search(r"Student to Teacher Ratio", pg):
                table(pg, r"Student to Teacher Ratio", [(r"Oyster River", "student_teacher_ratio")], True, y, "ratio", pn, out, maxper=4)
                teacher_exp(pg, y, pn, out)
                table(pg, r"Average Teacher Salary", [(r"Oyster River", "avg_teacher_salary")], True, y, "salary", pn, out)
                table(pg, r"Limited English Proficiency", [(r"(?=\d)", "lep_students")], True, y, "lep", pn, out, stop=r"Source:")
            if re.search(r"Official Enrollment Counts", pg):
                enrollment(pg, y, pn, out)
                school_year_enrollment(pg, y, pn, out)
                class_size(pg, y, pn, out)
                table(pg, r"Student Attendance Rate", [("Kindergarten", "att_k"), ("Elementary", "att_elem"), ("Middle School", "att_middle"), ("High School", "att_high")], True, y, "attendance", pn, out)
                table(pg, r"Cost Per Pupil", [(r"K-4", "cpp_k4"), (r"5-8", "cpp_58"), (r"9-12", "cpp_912")], True, y, "cost_per_pupil", pn, out)
            if re.search(r"High School Completers", pg):
                table(pg, r"High School Completers", [(r"Entering 4 yr\. college", "comp_4yr"), (r"Entering less than 4 yr", "comp_less4"), (r"Returning to post second", "comp_postsec"),
                                                       (r"Employed", "comp_employed"), (r"Armed Forces", "comp_armed"), (r"Unemployed", "comp_unemployed"), (r"Unknown", "comp_unknown")], True, y, "completers", pn, out)
                table(pg, r"Drop Out Rate", [(r"Oyster River", "dropouts")], True, y, "dropouts", pn, out)
                table(pg, r"Teacher Educational Attainment", [(r"% Bachelor.s", "deg_bachelors"), (r"% Masters", "deg_masters"), (r"% Beyond Masters", "deg_beyond")], True, y, "teacher_degrees", pn, out)
                table(pg, r"Free/Reduced Lunch Eligibility", [(r"Oyster River", "frl_students")], False, y, "frl", pn, out)
                table(pg, r"Career Technology", [(r"High School students", "cte_students")], False, y, "cte", pn, out)
            if re.search(r"RESULTS OF \d{4} ANNUAL MEETING", pg): votes(pg, y, pn, out)
    json.dump(out, open(os.path.join(ROOT, "build", "annual_report_tables.json"), "w"), indent=0)
    bad = [r for r in out if r["period"] == "PARSE?"]
    print(len(out), "records;", len(bad), "rows needing a look")
    for r in bad[:40]: print(" ", r["report"], r["table"], r["metric"], "|", r["raw"])

if __name__ == "__main__":
    main()
