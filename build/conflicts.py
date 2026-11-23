#!/usr/bin/env python3
"""Compare figures the district prints (annual reports, audited statements) with the state's own figures for the same measure and year, and log every difference.
Inputs (all in the repo):  build/annual_report_tables.json (annual_extract.py), build/audit_metrics.json (audit_extract.py),
  raw/nh-doe/dashboard-exports-2026-11-22/iexplore_compare_all_entities.tsv (NH DOE iExplore, district and school entities), data/orcsd_years.json (the page's own values, which come from DOE-25, DOE files and the reports).
Outputs:  data/conflicts.csv (every comparison made: agreements too) and CONFLICTS.md (the differences, explained).   Run from the repo root:  python3 build/conflicts.py
Verdicts:  agree = same to the printed precision;  CONFLICT = the two sources print different numbers for the same measure and year and nothing about definitions explains it;
           definition = differs because the two sources count different things (dates, populations, fund coverage); the note says how;  internal = the district disagrees with itself.
Year key = FY (year the school year ends); iExplore 'doe_year' is the same key (verified: 2015-16 enrollment 2,054 is doe_year 2016)."""
import csv, json, os, re, collections

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
P = lambda *a: os.path.join(ROOT, *a)
AR = json.load(open(P("build", "annual_report_tables.json")))
AU = {int(k): v for k, v in json.load(open(P("build", "audit_metrics.json"))).items()}
BT = json.load(open(P("build", "budget_tables.json")))
MS = json.load(open(P("build", "ms26_tables.json")))["lines"]
PAGE = {int(r["fy"][:4]) + 1: r for r in json.load(open(P("data", "orcsd_years.json")))["rows"]}
IX = collections.defaultdict(dict)       # (indicator, entity) -> {fy: value}
for r in csv.DictReader(open(P("raw", "nh-doe", "dashboard-exports-2026-11-22", "iexplore_compare_all_entities.tsv")), delimiter="\t"):
    v = r["value"].strip().replace("$", "").replace(",", "").replace("%", "")
    try: IX[(r["indicator"], r["entity"])][int(r["doe_year"])] = float(v)
    except ValueError: pass            # '*CS' (suppressed) and the like
DIST, STATE = "Oyster River Coop (District)", "State of New Hampshire"
SCH = {"hs": "Oyster River High School", "ms": "Oyster River Middle School", "mw": "Mast Way School", "mo": "Moharimet School"}

# the report card, latest report that prints each (metric, entity, fy)
RC = {}
for r in AR:
    if r["fy"] is None or r["value"] is None: continue
    k = (r["metric"], r["entity"], r["fy"])
    if k not in RC or r["report"] > RC[k][1]: RC[k] = (r["value"], r["report"], r["pdf_page"], r["table"])
def rc(metric, fy, ent="district"):
    return RC.get((metric, ent, fy))

OUT = []
def add(cls, topic, fy, a, b, tol=0.0, rel=0.0, verdict_if_diff="CONFLICT", note=""):
    """a, b = (label, value, where) ; compares numerically."""
    if a[1] is None or b[1] is None: return
    d = a[1] - b[1]
    ok = abs(d) <= tol + rel * abs(b[1]) + 1e-9
    OUT.append(dict(cls=cls, topic=topic, fy=fy, a_source=a[0], a_value=a[1], a_where=a[2], b_source=b[0], b_value=b[1], b_where=b[2],
                    diff=round(d, 4), diff_pct=round(100 * d / b[1], 2) if b[1] else "", verdict="agree" if ok else verdict_if_diff, note="" if ok else note))

def RCs(metric, fy, ent="district"):
    x = rc(metric, fy, ent)
    return None if x is None else ("ORCSD annual report %d, Report Card" % x[1], x[0], "%s p.%d" % (os.path.basename("Annual_Reports__%d_ORCSD_Annual_Report.pdf" % x[1]), x[2]))
def IXs(ind, fy, ent=DIST, label="NH DOE iExplore"):
    v = IX.get((ind, ent), {}).get(fy)
    return None if v is None else (label + " (" + ind + ")", v, "raw/nh-doe/dashboard-exports-2026-11-22/iexplore_compare_all_entities.tsv")
def PG(key, fy, label):
    v = PAGE.get(fy, {}).get(key)
    return None if v is None else (label, v, "data/orcsd_years.json field " + key)
def AUs(key, fy):
    x = AU.get(fy, {}).get(key)
    return None if x is None else ("ORCSD audit FY%d" % fy, x["v"], "Audit_Reports__%d_ORCSD_Audit_Report.pdf p.%d" % (fy, x["pdf_page"]))

def both(f, *args, **kw):
    pass

# ---------------------------------------------------------------- 1. district report card vs state (iExplore) --------------------------------------------
for fy in range(2016, 2027):
    a, b = RCs("enr_total", fy), IXs("Total Enrollment", fy)
    if a and b: add("district-vs-state", "Enrollment, October 1, all grades", fy, a, b)
    a, b = RCs("enr_high", fy), IXs("Total Enrollment", fy, SCH["hs"])
    if a and b: add("district-vs-state", "Enrollment, high school (grades 9-12)", fy, a, b)
    a, b = RCs("enr_middle", fy), IXs("Total Enrollment", fy, SCH["ms"])
    if a and b: add("district-vs-state", "Enrollment, middle school (grades 5-8)", fy, a, b)
    ka, kb = rc("enr_k", fy), rc("enr_elem", fy)
    if ka and kb:
        a = ("ORCSD annual report %d, Report Card" % max(ka[1], kb[1]), ka[0] + kb[0], "Kindergarten + Elementary rows")
        m1, m2 = IXs("Total Enrollment", fy, SCH["mw"]), IXs("Total Enrollment", fy, SCH["mo"])
        if m1 and m2: add("district-vs-state", "Enrollment, K-4 (Mast Way + Moharimet)", fy, a, ("NH DOE iExplore (Total Enrollment, Mast Way + Moharimet)", m1[1] + m2[1], m1[2]))
    for lvl, ent in (("ratio", None),):
        pass
    a, b = RCs("avg_teacher_salary", fy), IXs("Average Teacher Salary ($)", fy)
    if a and b: add("district-vs-state", "Average teacher salary, district", fy, a, b)
    a, b = RCs("avg_teacher_salary", fy, "state"), IXs("Average Teacher Salary ($)", fy, STATE)
    if a and b: add("district-vs-state", "Average teacher salary, NH", fy, a, b, tol=5)
    # dropouts: count (report) vs rate (iExplore): rate = count / grades 9-12 enrollment
    c, hs, rate = rc("dropouts", fy), rc("enr_high", fy), IX.get(("Dropout Rate (%)", DIST), {}).get(fy)
    if c and hs and rate is not None:
        add("district-vs-state", "Dropouts, % of grade 9-12 enrollment (report count / report grade 9-12 enrollment)", fy,
            ("ORCSD annual report %d (%d dropouts / %d grade 9-12)" % (c[1], c[0], hs[0]), round(100 * c[0] / hs[0], 2), "Report Card: Drop Out Rate, Official Enrollment Counts"),
            ("NH DOE iExplore (Dropout Rate %)", rate, "iexplore_compare_all_entities.tsv"), tol=0.015)
    # students with disabilities, English learners, economically disadvantaged: district counts / enrollment vs state percent
    s, e = rc("sped_total", fy), rc("enr_total", fy)
    p = IX.get(("Students with Disability (%)", DIST), {}).get(fy)
    if s and e and p is not None:
        add("district-vs-state", "Students with disabilities, % of enrollment (district's Oct 1 special-education count / enrollment)", fy,
            ("ORCSD annual report %d (%d / %d)" % (s[1], s[0], e[0]), round(100 * s[0] / e[0], 2), "Report Card: Special Education Statistics"),
            ("NH DOE iExplore (Students with Disability %)", p, "iexplore_compare_all_entities.tsv"), tol=0.4)
    l = rc("lep_students", fy); p = IX.get(("English Language Learner (%)", DIST), {}).get(fy)
    if l and e and p is not None:
        add("district-vs-state", "English learners, % of enrollment (report count / enrollment)", fy,
            ("ORCSD annual report %d (%d / %d)" % (l[1], l[0], e[0]), round(100 * l[0] / e[0], 2), "Report Card: Limited English Proficiency"),
            ("NH DOE iExplore (English Language Learner %)", p, "iexplore_compare_all_entities.tsv"), tol=0.4)
    f = rc("frl_students", fy); p = IX.get(("Economically Disadvantaged Students (%)", DIST), {}).get(fy)
    if f and e and p is not None:
        add("district-vs-state", "Free/reduced lunch eligible vs economically disadvantaged, % of enrollment (report count / enrollment)", fy,
            ("ORCSD annual report %d (%d / %d)" % (f[1], f[0], e[0]), round(100 * f[0] / e[0], 2), "Report Card: Free/Reduced Lunch Eligibility"),
            ("NH DOE iExplore (Economically Disadvantaged %)", p, "iexplore_compare_all_entities.tsv"), tol=0.4)
    # cost per pupil: report prints three levels; compare with the DOE school-finance file values the page holds
    for m, key, lab in (("cpp_k4", "cpp_el", "K-4"), ("cpp_58", "cpp_ms", "5-8"), ("cpp_912", "cpp_hs", "9-12")):
        a, b = RCs(m, fy), PG(key, fy, "NH DOE Bureau of School Finance, Cost per Pupil by District (as on the page)")
        if a and b: add("district-vs-state", "Cost per pupil, %s" % lab, fy, a, b, tol=1)

# ratio: report vs DOE Student-to-Teacher file (page), district and state
for fy in range(2016, 2027):
    a, b = RCs("student_teacher_ratio", fy), PG("ratio", fy, "NH DOE Student to Teacher Ratio (as on the page)")
    if a and b: add("district-vs-state", "Student-to-teacher ratio, district", fy, a, b, tol=0.05)
    a, b = RCs("student_teacher_ratio", fy, "state"), PG("ratio_state", fy, "NH DOE Student to Teacher Ratio, NH (as on the page)")
    if a and b: add("district-vs-state", "Student-to-teacher ratio, NH", fy, a, b, tol=0.05)

# ---------------------------------------------------------------- 2. state vs state (iExplore vs DOE-25 values the page holds) -----------------------------
for fy in range(2016, 2026):
    for ind, key, lab, kw in (("Total Expenditures ($)", "actual_total", "NH DOE DOE-25 (District Profile: Total Expenditures)", {}),
                              ("Average Cost Per Pupil ($)", "nhed_cpp", "NH DOE Cost per Pupil by District file", {}),
                              ("Average Teacher Salary ($)", "t_avg_file", "NH DOE Teacher Average Salary file", {}),
                              ("Total Revenues ($)", "rev_tot", "NH DOE DOE-25 (District Profile: Total Revenues)", {})):
        a, b = IXs(ind, fy), PG(key, fy, lab)
        if a and b: add("state-vs-state", ind.replace(" ($)", "") + ", district", fy, b, a, tol=1, **kw)

# ---------------------------------------------------------------- 3. audited statements vs state (DOE-25) ---------------------------------------------------
for fy in range(2018, 2025):
    a, b = AUs("f_expenditures_total", fy), PG("actual_total", fy, "NH DOE DOE-25, Total Expenditures")
    if a and b: add("district-vs-state", "Total expenditures, governmental funds (audit) vs DOE-25 total expenditures", fy, a, b, tol=1, verdict_if_diff="different basis")
    a, b = AUs("f_revenues_total", fy), PG("rev_tot", fy, "NH DOE DOE-25, Total Revenues")
    if a and b: add("district-vs-state", "Total revenues, governmental funds (audit) vs DOE-25 total revenues", fy, a, b, tol=1, verdict_if_diff="different basis")
    a, b = AUs("gf_fb_total", fy), PG("fb_tot", fy, "ORCSD audit, as on the page")
    if a and b: add("district-vs-district", "General fund balance, audit vs page", fy, a, b, tol=1)


# ---------------------------------------------------------------- 4. state vs state, and the district against itself ---------------------------------------------------
def tot(r, fy, ents):
    xs = [IX.get(("Total Enrollment", SCH[e]), {}).get(fy) for e in ents]
    return None if None in xs else sum(xs)
for fy in range(2016, 2027):
    d, sm = IX.get(("Total Enrollment", DIST), {}).get(fy), tot(None, fy, ("hs", "ms", "mw", "mo"))
    if d is not None and sm is not None:
        add("state-vs-state", "iExplore enrollment: district figure vs the sum of its four schools", fy,
            ("NH DOE iExplore, Oyster River Coop (District) Total Enrollment", d, "iexplore_compare_all_entities.tsv"),
            ("NH DOE iExplore, Mast Way + Moharimet + Middle + High", sm, "iexplore_compare_all_entities.tsv"))
    a, b = PG("t_avg_state", fy, "NH DOE Teacher Average Salary file, NH (as on the page)"), IXs("Average Teacher Salary ($)", fy, STATE)
    if a and b: add("state-vs-state", "Average teacher salary, NH: DOE salary file vs iExplore", fy, a, b, tol=5)

# school-year enrollment table (the district's own October 1 count) -------------------------------------------------------------------------------------------
SYE = collections.defaultdict(dict)
for r in AR:
    if r["table"] == "school_year_enrollment": SYE[(r["report"], r["fy"])][r["metric"]] = (r["value"], r["pdf_page"])
for (rep, fy), d in sorted(SYE.items()):
    if len(d) < 4 or rep == 2021: continue            # the 2021 report's table is not in the usual layout
    where = "Annual_Reports__%d_ORCSD_Annual_Report.pdf p.%d" % (rep, list(d.values())[0][1])
    sm = sum(d[k][0] for k in ("sye_mastway", "sye_moharimet", "sye_middle", "sye_high"))
    if "sye_total" in d:
        add("district-internal", "School Year Enrollment table: printed Totals row vs the sum of its four school rows", fy,
            ("ORCSD annual report %d, printed Totals row" % rep, d["sye_total"][0], where), ("same table, sum of the four school rows", sm, where))
    o = rc("enr_total", fy)
    if o: add("district-internal", "Same-year October 1 enrollment: School Year Enrollment table (sum of schools) vs Official Enrollment Counts table", fy,
              ("ORCSD annual report %d, School Year Enrollment (ORCSD Oct 1 report), sum of schools" % rep, sm, where), ("ORCSD annual report %d, Official Enrollment Counts (NH DOE)" % o[1], o[0], "Annual_Reports__%d_ORCSD_Annual_Report.pdf p.%d" % (o[1], o[2])))
    for k, e, nm in (("sye_high", "hs", "high school"), ("sye_middle", "ms", "middle school"), ("sye_mastway", "mw", "Mast Way"), ("sye_moharimet", "mo", "Moharimet")):
        b = IXs("Total Enrollment", fy, SCH[e])
        if b: add("district-vs-state", "School Year Enrollment table vs iExplore: %s" % nm, fy, ("ORCSD annual report %d, School Year Enrollment (ORCSD Oct 1 report)" % rep, d[k][0], where), b)

# arithmetic inside the report card ------------------------------------------------------------------------------------------------------------------------------
by = collections.defaultdict(dict)
for r in AR:
    if r["fy"] is None or r["value"] is None or r["entity"] not in ("district",): continue
    by[(r["report"], r["fy"])][r["metric"]] = (r["value"], r["pdf_page"], r["table"])
for (rep, fy), d in sorted(by.items()):
    wh = lambda m: "Annual_Reports__%d_ORCSD_Annual_Report.pdf p.%d" % (rep, d[m][1])
    if all(k in d for k in ("enr_k", "enr_elem", "enr_middle", "enr_high", "enr_total")):
        add("district-internal", "Official Enrollment Counts: Totals row vs the sum of its level rows", fy, ("ORCSD annual report %d, Totals row" % rep, d["enr_total"][0], wh("enr_total")),
            ("same table, K + Elementary + Middle + High", sum(d[k][0] for k in ("enr_k", "enr_elem", "enr_middle", "enr_high")), wh("enr_total")), tol=0)
    if all(k in d for k in ("sped_elem", "sped_middle", "sped_high", "sped_ood_3_5", "sped_ood_6_21", "sped_total")):
        add("district-internal", "Special Education Statistics: Totals row vs the sum of its rows", fy + 0, ("ORCSD annual report %d, Totals row" % rep, d["sped_total"][0], wh("sped_total")),
            ("same table, sum of the five rows", sum(d[k][0] for k in ("sped_elem", "sped_middle", "sped_high", "sped_ood_3_5", "sped_ood_6_21")), wh("sped_total")), tol=0)
    ks = [k for k in d if k.startswith("comp_")]
    if len(ks) == 7:
        add("district-internal", "High School Completers: the seven percentages add to 100", fy, ("ORCSD annual report %d, sum of district percentages" % rep, round(sum(d[k][0] for k in ks), 1), wh(ks[0])),
            ("100", 100.0, "table definition"), tol=1.0)
    ks = [k for k in d if k.startswith("deg_")]
    if len(ks) == 3:
        add("district-internal", "Teacher Educational Attainment: the three percentages add to 100", fy, ("ORCSD annual report %d, sum of district percentages" % rep, round(sum(d[k][0] for k in ks), 1), wh(ks[0])),
            ("100", 100.0, "table definition"), tol=0.6)

# values repeated from the prior year (every level identical) ------------------------------------------------------------------------------------------------
def repeat_check(metrics, label, ents=("district", "state"), fyr=range(2013, 2027)):
    for ent in ents:
        for fy in fyr:
            got = [(rc(m, fy, ent), rc(m, fy - 1, ent)) for m in metrics]
            if all(a and b for a, b in got) and all(a[0] == b[0] for a, b in got):
                a0 = got[0][0]
                OUT.append(dict(cls="district-internal", topic=label + " (%s): every row identical to the prior year's" % ent, fy=fy,
                                a_source="ORCSD annual report %d (FY%d)" % (a0[1], fy), a_value="; ".join("%s=%s" % (m, g[0][0]) for m, g in zip(metrics, got)),
                                a_where="Annual_Reports__%d_ORCSD_Annual_Report.pdf p.%d" % (a0[1], a0[2]),
                                b_source="same report (FY%d)" % (fy - 1), b_value="", b_where="", diff="", diff_pct="", verdict="CONFLICT",
                                note="Identical to the last digit across all rows, which real data almost never are: the column was probably copied forward rather than updated."))
repeat_check(["att_k", "att_elem", "att_middle", "att_high"], "Student attendance rate")
repeat_check(["avg_teacher_salary"], "Average teacher salary")
repeat_check(["student_teacher_ratio"], "Student-to-teacher ratio", ents=("state",))
repeat_check(["cpp_k4", "cpp_58", "cpp_912"], "Cost per pupil", ents=("district", "state"))


# ---------------------------------------------------------------- 5. budget tables in the annual reports (build/budget_tables.json) -------------------------------------------
ARW = lambda y, pg: "Annual_Reports__%d_ORCSD_Annual_Report.pdf p.%s" % (y, pg)
DEPT = collections.defaultdict(dict)                      # (report, kind, fy) -> {dept: (value, page)}
for r in BT["dept"]: DEPT[(r["report"], r["kind"], r["fy"])][r["dept"]] = (r["value"], r["pdf_page"])
for (rep, kind, fy), d in sorted(DEPT.items()):          # (a) the nine department rows against the printed TOTAL row
    if "total" not in d: continue
    sm = sum(v[0] for k, v in d.items() if k != "total")
    add("district-internal", "Budget Summary by Location (%s): printed TOTAL row vs the sum of its department rows" % kind, fy,
        ("ORCSD annual report %d, printed TOTAL row" % rep, d["total"][0], ARW(rep, d["total"][1])), ("same table, sum of the nine department rows", sm, ARW(rep, d["total"][1])), tol=0)
FUND = {(f["report"]): f for f in BT["funds"]}
for rep, f in sorted(FUND.items()):                      # (b) the warrant article's four funds against its printed total
    add("district-internal", "Operating-budget warrant article: Fund 10 + 21 + 22 + 23 vs the printed total", f["fy"],
        ("ORCSD annual report %d, printed total" % rep, f["total"], ARW(rep, f["pdf_page"])), ("same article, sum of the four funds", f["general_fund"] + f["food_service"] + f["federal"] + f["pass_through"], ARW(rep, f["pdf_page"])), tol=0)
for (rep, kind, fy), d in sorted(DEPT.items()):          # (c) the year's budget as proposed one report earlier vs as approved in the next
    if kind != "approved" or "total" not in d: continue
    pr = DEPT.get((rep - 1, "proposed", fy))
    if pr and "total" in pr:
        add("district-internal", "General Fund budget: approved total vs the same year's proposed total printed a year earlier", fy,
            ("ORCSD annual report %d, approved" % rep, d["total"][0], ARW(rep, d["total"][1])), ("ORCSD annual report %d, proposed" % (rep - 1), pr["total"][0], ARW(rep - 1, pr["total"][1])), tol=0, verdict_if_diff="different basis",
            note="The approved General Fund total is above the total proposed a year earlier in every year (by 0.1% to 2.7%). For FY2019 the gap ($118,959) equals the two contract articles on the same warrant ($54,083 + $64,876); the reports do not explain the other years (FY2021: $1.25M). A proposed total is not a ceiling on what is approved.")
# (d) what the district says it spent (General Fund, two years back) vs the audit and vs DOE-25
EXP = {}
for (rep, kind, fy), d in sorted(DEPT.items()):
    if kind == "expended" and "total" in d: EXP[fy] = (d["total"][0], rep, d["total"][1])
for fy, (v, rep, pg) in sorted(EXP.items()):
    a = ("ORCSD annual report %d, General Fund budget comparison, 'expended'" % rep, v, ARW(rep, pg))
    b = AUs("gf_expenditures_total", fy)
    if b: add("district-vs-district", "General Fund spending: annual report's 'expended' vs the audit's General Fund expenditures", fy, a, b, rel=0.005, verdict_if_diff="different basis",
              note="Within 0.5% in FY2021-FY2024 (agree); FY2018-FY2020 differ by 0.9-7.6%. The report's table is the business office's own budget-basis figure and the audit is GAAP, so small differences (encumbrances, on-behalf payments) are expected.")
    b = PG("actual_recurring", fy, "NH DOE DOE-25, recurring expenditures (as on the page)")
    if b: add("district-vs-state", "General Fund spending: annual report's 'expended' vs DOE-25 recurring expenditures", fy, a, b, rel=0.005, verdict_if_diff="different basis",
              note="The district's 'expended' General Fund total is within 0.3% of the audit but 0.5-6% from the state's DOE-25 'recurring' figure for the same year. DOE-25 excludes some items (capital, debt principal, food service and grant funds), so the two are not meant to match, and no document reconciles them. The page shows the DOE-25 figure.")
# (e) tax rates: the district's printed 'current' rate vs the state's rate for the same year and town
TOWN = {"durham": "dur", "lee": "lee", "madbury": "mad"}
TAXR = {}
for t in BT["tax"]:
    lr, k = t["local_rate"], TOWN[t["town"]]
    if not lr or len(lr) < 2: continue
    TAXR[(t["report"], t["town"])] = t
    cur = PAGE.get(t["fy_cur"], {}).get("tax_" + k)
    add("district-vs-state", "Local school tax rate per $1,000 in the annual report's 'current' column vs the NH DRA rate", t["fy_cur"],
        ("ORCSD annual report %d, Tax Rate Impact, %s current" % (t["report"], t["town"].title()), lr[0], ARW(t["report"], t["pdf_page"])),
        ("NH DRA tax rate, %s (as on the page)" % t["town"].title(), cur, "data/orcsd_years.json field tax_" + k), tol=0.011, verdict_if_diff="CONFLICT")
    if len(lr) >= 3:                                         # printed impact (the column is headed 'Impact Revised') vs the difference of the two printed rates
        add("district-internal", "Tax Rate Impact: printed 'Impact Revised' vs proposed rate minus current rate", t["fy_prop"],
            ("ORCSD annual report %d, %s printed 'Impact Revised'" % (t["report"], t["town"].title()), lr[2], ARW(t["report"], t["pdf_page"])),
            ("same table, proposed minus current local rate", round(lr[1] - lr[0], 2), ARW(t["report"], t["pdf_page"])), tol=0.011, verdict_if_diff="different basis",
            note="The table's last column is headed 'Impact Revised', so it is a later estimate (after the budget was revised) set beside a proposed-rate column that was not revised; the two do not subtract to it. For example FY2025, Durham: proposed rate 12.15 minus current 11.58 = 0.57, printed revised impact 0.40. The page's estimate row uses proposed minus current.")
    nv = t.get("nav")
    if nv and len(nv) == 2:
        add("district-internal", "Tax Rate Impact: net assessed value in the 'current' and 'proposed' columns (held fixed, so they should be equal)", t["fy_cur"],
            ("ORCSD annual report %d, %s current column" % (t["report"], t["town"].title()), nv[0], ARW(t["report"], t["pdf_page"])), ("same table, proposed column", nv[1], ARW(t["report"], t["pdf_page"])), tol=0,
            note="Digits transposed in one column (235,434,027 vs 235,343,027); the proposed rate is computed from the second figure, so the effect on the rate is small.")
# (f) projection against what happened: proposed rate vs the state's actual rate the following year
for (rep, town), t in sorted(TAXR.items()):
    k = TOWN[town]; act = PAGE.get(t["fy_prop"], {}).get("tax_" + k)
    add("district-projection", "Projected local school rate per $1,000 (district, assessed value held fixed) vs the NH DRA rate that was set", t["fy_prop"],
        ("ORCSD annual report %d, %s proposed rate" % (rep, town.title()), t["local_rate"][1], ARW(rep, t["pdf_page"])),
        ("NH DRA tax rate, %s (as on the page)" % town.title(), act, "data/orcsd_years.json field tax_" + k), tol=0.011, verdict_if_diff="projection",
        note="Not an error: the district's projection holds each town's assessed value and the state tax apportionment fixed, so it isolates the budget's effect. The rate that is actually set moves with revaluations, enrollment shares and state aid, and has differed from the projection by several dollars per $1,000 in some years (for example Durham FY2024).")


# ---------------------------------------------------------------- 6. NH DRA MS-26 (reprinted as images in the 2025 and 2026 annual reports; build/ms26_tables.json, OCR) --------------------------------------
MSW = lambda y, pg: "Annual_Reports__%d_ORCSD_Annual_Report.pdf p.%s (MS-26, OCR)" % (y, pg)
FNMAP = {"1100-1199": ("fn_reg", "regular programs"), "1200-1299": ("fn_spec", "special programs"), "1300-1399": ("fn_voc", "vocational programs"), "1400-1499": ("fn_oi", "other instruction programs"),
         "2000-2199": ("fn_ss", "student support services"), "2200-2299": ("fn_isup", "instructional staff services"), "2400-2499": ("fn_sadm", "school administration"),
         "2500-2599": ("fn_bus", "business"), "2600-2699": ("fn_plant", "plant operations and maintenance"), "2700-2799": ("fn_trans", "student transportation"), "5120": ("fn_bint", "debt service, interest")}
for r in MS:
    if r.get("kind") != "line" or r["part"] != "appropriations" or r["section"] not in ("Instruction", "Support Services", "Executive Administration", "Other Outlays"): continue
    k = FNMAP.get(r["account"])
    if not k: continue
    fy = r["report"] - 1
    add("state-vs-state", "Expenditure by function, MS-26 (NH DRA form) vs DOE-25 (NH DOE form): " + k[1], fy, ("ORCSD annual report %d, MS-26 actual" % r["report"], r["values"][0], MSW(r["report"], r["pdf_page"])),
        PG(k[0], fy, "NH DOE DOE-25 (as on the page)"), tol=2, verdict_if_diff="CONFLICT",
        note="FY2024 plant operations is printed as $0 in the 2025 report's MS-26 (the printed subtotals add up with it), against $4,362,304 in DOE-25, so that report's MS-26 actual column understates FY2024 spending by about that amount. Otherwise: two state forms filed by the district for the same fiscal year give different amounts for the same function. Regular programs, vocational, student support, school administration, transportation and debt interest tie (to $1 rounding); special programs, other instruction, instructional staff services and plant operations do not, with DOE-25 higher in each case. The documents do not say why. The page shows DOE-25.")
def ms_total(rep, i):
    """Operating budget = sum of the line items of the eight operating sections (OCR'd subtotal rows are used only as a check in ms26_extract.py; the Facilities subtotal row is unreadable in the 2025 report)."""
    return sum(r["values"][i] for r in MS if r["report"] == rep and r.get("kind") == "line" and r["part"] == "appropriations" and r["section"] in ("Instruction", "Support Services", "General Administration", "Executive Administration", "Non-Instructional Services", "Facilities Acquisition and Construction", "Other Outlays", "Fund Transfers") and len(r["values"]) >= 3)
for rep in (2025, 2026):
    pg = next(r["pdf_page"] for r in MS if r["report"] == rep)
    add("state-vs-district", "Operating budget approved for the current year: MS-26 vs the adopted budget on the page", rep, ("ORCSD annual report %d, MS-26 appropriations, current year" % rep, ms_total(rep, 1), MSW(rep, pg)),
        PG("budget", rep, "Adopted budget (as on the page)"), tol=1, verdict_if_diff="different basis",
        note="The MS-26 'appropriations for the current year' column includes the individual warrant articles (the union contracts) that the page's operating-budget figure leaves out: for FY2026 the gap, $1,672,126, is exactly the 2025 report's Individual Warrant Articles total. The FY2025 gap ($139,869) is probably the same kind of item; the report does not itemise it.")
    add("state-vs-district", "Operating budget proposed for next year: MS-26 recommended vs the budget on the page", rep + 1, ("ORCSD annual report %d, MS-26 operating budget recommended" % rep, ms_total(rep, 2), MSW(rep, pg)),
        PG("budget", rep + 1, "Budget (as on the page)"), tol=1, verdict_if_diff="different basis",
        note="For FY2027 the page's $62,365,067 is $519,000 above the MS-26's $61,846,067 (the $519K figure is the amendment discussed in the district's budget record); for FY2026 the MS-26 operating total is what the voters were asked to approve before amendment.")
    add("state-vs-state", "Total expenditures, MS-26 actual vs DOE-25 recurring expenditures", rep - 1, ("ORCSD annual report %d, MS-26 actual (sum of subtotals)" % rep, ms_total(rep, 0), MSW(rep, pg)),
        PG("actual_recurring", rep - 1, "NH DOE DOE-25 recurring expenditures (as on the page)"), tol=2, verdict_if_diff="different basis",
        note="The MS-26 actual column is the general fund as the district reported it to the DRA; DOE-25 recurring excludes some items. The page shows DOE-25.")

# ---------------------------------------------------------------- 7. NH SAT means: the district's printed "State" column vs the College Board's NH report (hosted by the DOE) ------------------------------
for fy in range(2018, 2026):
    for metric, key, nm in (("sat_rw", "sat_rw_nh", "evidence-based reading and writing"), ("sat_math", "sat_m_nh", "math")):
        a = RCs(metric, fy, "state")
        b = PG(key, fy, "College Board NH SAT annual report, class of %d, Total row (as on the page)" % fy)
        if a and b: add("district-vs-state", "New Hampshire average SAT, %s: district annual report's State column vs the College Board NH report" % nm, fy, a, b, tol=0.5,
                        note="The district's printed 'State' averages differ from the College Board's New Hampshire report (all NH graduates who took the SAT) in every year but 2018, by up to 27 points; the district's figures do not match any other total-group table in that report either, and the source of the district's column is not stated. The page now uses the College Board figure.")

# ---------------------------------------------------------------- 8. special education expenditures "per RSA 32:11-a" (annual reports 2025 and 2026) -------------------------------------------
RSAW = lambda fy: "Annual_Reports__%d_ORCSD_Annual_Report.pdf p.15 (RSA 32:11-a table)" % (2025 if fy <= 2024 else 2026)
def msl(rep, acct, part="appropriations"):
    return next((r for r in MS if r["report"] == rep and r.get("kind") == "line" and r["part"] == part and r.get("account") == acct), None)
for fy in (2023, 2024, 2025):
    a = PG("rsa_cost", fy, "ORCSD annual report, RSA 32:11-a table, special education costs (1200)"); a = None if a is None else (a[0], a[1], RSAW(fy))
    b = PG("fn_spec", fy, "NH DOE DOE-25, special programs (as on the page)")
    if a and b: add("district-vs-state", "Special education programs (function 1200): RSA 32:11-a table vs DOE-25", fy, a, b, tol=2, verdict_if_diff="CONFLICT",
                    note="The district's RSA 32:11-a table, the MS-26 (DRA) and the DOE-25 (DOE) give three different amounts for special programs in the same year (FY2025: $8,419,644, $7,470,356, $7,970,563). The documents do not say why; the table may include the district's share of costs that the two state forms classify elsewhere. The page's special-education row uses the district's table and labels it as the district's.")
    for rep in (2025, 2026):
        m = msl(rep, "1200-1299")
        if m and rep - 1 == fy and a: add("district-vs-state", "Special education programs (function 1200): RSA 32:11-a table vs MS-26", fy, a, ("ORCSD annual report %d, MS-26 special programs actual" % rep, m["values"][0], MSW(rep, m["pdf_page"])), tol=2, verdict_if_diff="CONFLICT")
    sa = PG("rsa_aid", fy, "ORCSD annual report, RSA 32:11-a table, state special education aid")
    for rep in (2025, 2026):
        m = msl(rep, "3230", "revenue")
        if m and rep - 1 == fy and sa: add("district-vs-state", "State special education aid: RSA 32:11-a table vs MS-26 revenue (3230)", fy, (sa[0], sa[1], RSAW(fy)), ("ORCSD annual report %d, MS-26 actual revenue" % rep, m["values"][0], MSW(rep, m["pdf_page"])), tol=2)
    me = PG("rsa_med", fy, "ORCSD annual report, RSA 32:11-a table, Medicaid reimbursement")
    for rep in (2025, 2026):
        m = msl(rep, "4580", "revenue")
        if m and rep - 1 == fy and me: add("district-vs-state", "Medicaid reimbursement: RSA 32:11-a table vs MS-26 revenue (4580)", fy, (me[0], me[1], RSAW(fy)), ("ORCSD annual report %d, MS-26 actual revenue" % rep, m["values"][0], MSW(rep, m["pdf_page"])), tol=2)

# ---------------------------------------------------------------- 9. General Fund: audited statements vs the DOE-25 Statement of Analysis of Change in Fund Equity -----------------------------
DOEFE = lambda fy: "raw/nh-doe25 DOE25_id%d.xlsx, DOE25 sheet, Statement of Analysis of Change in Fund Equity" % {2018: 131, 2019: 306, 2020: 484, 2021: 544, 2022: 946, 2023: 1131, 2024: 2221, 2025: 2414}[fy]
for fy in range(2018, 2025):
    for au, pg, topic in (("gf_fb_total", "fe_gen_end", "General Fund balance at June 30: audit vs DOE-25 fund equity"),
                          ("gf_revenues_total", "fe_gen_rev", "General Fund revenue: audit vs DOE-25 (revenue and other additions)"),
                          ("gf_expenditures_total", "fe_gen_exp", "General Fund expenditures: audit vs DOE-25 (expenditures and other deletions)")):
        a, b = AUs(au, fy), PG(pg, fy, "NH DOE DOE-25, General Fund")
        if a and b: add("district-vs-state", topic, fy, a, (b[0], b[1], DOEFE(fy)), tol=1, verdict_if_diff="different basis")
    pa, pb = AU.get(fy - 1, {}).get("gf_fb_total"), AU.get(fy, {}).get("gf_fb_total")
    if pa and pb:
        d_au = pb["v"] - pa["v"]
        d_doe = PAGE[fy]["fe_gen_end"] - PAGE[fy]["fe_gen_beg"]
        add("district-vs-state", "Change in General Fund balance during the year: audit (year over year) vs DOE-25 fund equity", fy,
            ("ORCSD audits FY%d and FY%d, General Fund balance difference" % (fy - 1, fy), d_au, "Audit_Reports__%d_ORCSD_Audit_Report.pdf p.%d" % (fy, pb["pdf_page"])),
            ("NH DOE DOE-25, General Fund equity June 30 less July 1", round(d_doe, 2), DOEFE(fy)), tol=1000, verdict_if_diff="CONFLICT")

# ---------------------------------------------------------------- notes, size, de-duplication, output ----------------------------------------------------------------------
NOTES = [  # (topic prefix, note) - applied to rows that differ and have no note yet
 ("General Fund balance at June 30: audit vs DOE-25", "Not reconciled. The audit's General Fund balance is $0.6M to $1.8M higher than the DOE-25's General Fund equity in every year. Neither document says why; the audit's balance includes nonspendable, restricted and committed amounts, so the DOE-25 equity may be a narrower measure. The page's fund balance row uses the audit; the new fund-results row uses the DOE-25 (state first). Ask the business office which one the state intends to be comparable."),
 ("Change in General Fund balance during the year", "The two documents disagree about whether the General Fund ran a surplus or a deficit: FY2019 (audit -$146K, DOE-25 +$294K), FY2022 (audit -$109K, DOE-25 +$158K) and FY2024 (audit +$286K, DOE-25 -$139K) have opposite signs; the other four years agree on direction but not on size. The audit includes transfers and items the DOE-25's revenue and expenditure lines treat differently; the business office can reconcile the two."),
 ("Enrollment, October 1, all grades", "The district's Report Card prints the sum of the four schools for FY2019, FY2020 and FY2026 (2,157, 2,168, 2,038), which is also what the DOE's student-to-teacher file uses (2,157, 2,168, 2,038), but the DOE district total in FY2016-FY2018 and FY2021-FY2025. So the state itself has two figures: its district total (iExplore) and the sum of its schools, 25-34 apart from FY2019 on. The page uses the iExplore district total in every year."),
 ("Budget Summary by Location", "Arithmetic inside the district's own table: the FY2024 approved rows add to $1,000 more than the printed total (the other tables tie to the dollar)."),
 ("Expenditure by function, MS-26", "State: DOE-25 (the MS-26 figure is in this log)"), ("Operating budget approved for the current year", "Adopted budget (agrees)"), ("Operating budget proposed", "The page's budget series (see note)"), ("Total expenditures, MS-26", "State: DOE-25"),
 ("New Hampshire average SAT", "State: College Board NH SAT annual report (hosted by the NH DOE). Oyster River High School comes from the district (no state series)."),
 ("Special education programs (function 1200)", "District's RSA 32:11-a table, labeled as the district's (the DOE-25 special programs figure is on the Spending by function rows)"),
 ("State special education aid", "n/a (agrees)"), ("Medicaid reimbursement", "n/a"),
 ("Local school tax rate per $1,000 in the annual report", "The district's 'current' rate is the state's rate for that year; where they differ the page shows the state's."),
 ("Enrollment, high school", "One student: the district prints 795, iExplore 796 for FY2026 (iExplore's four schools sum to 2,039; the report prints 2,038)."),
 ("Average teacher salary, NH", "The state average the report prints is not the one the DOE's current files give. In FY2018 the report prints $53,984; the DOE salary file and iExplore both give about $58,277. FY2024: the DOE salary file and the report agree ($67,096); iExplore gives $66,576."),
 ("Student-to-teacher ratio, NH", "The report's NH column does not match the DOE ratio file: FY2024 prints 12.02 (DOE 11.3) and FY2025 prints 11.24, which is also the FY2023 figure (DOE 11.17)."),
 ("iExplore enrollment: district figure", "Inside the DOE's own dashboard, the district total is above the sum of its four schools by 25-34 students from FY2019 on (equal for FY2016-FY2018). The dashboard does not say who the extra students are."),
 ("Students with disabilities", "The district's October 1 special-education count (in-district plus out-of-district placements, from the special-education office) gives a lower share than the DOE's count; the gap grows from 0.3 percentage points in FY2018 to 2.2 in FY2026. The documents do not say which counts which students, so neither can be called wrong."),
 ("Total expenditures, governmental funds", "Not reconciled. The audit is GAAP, all governmental funds (general, capital project and nonmajor funds); DOE-25 is the state's own form filed by the business office. FY2021 and FY2022 are the closest (2.5% and 3.2%), the years of the large capital project; FY2018 is 13.6% apart and not explained by the audit's debt service or its $3.9M capital-lease issuance alone."),
 ("Total revenues, governmental funds", "Not reconciled; the audit is higher every year by 0.7-3.0% (GAAP fund coverage versus the DOE-25 form)."),
 ("Official Enrollment Counts: Totals row", "The level rows sum to 25-30 fewer than the printed total from FY2021 on. The printed total is the DOE district total; the level rows are school figures (same gap inside iExplore)."),
 ("School Year Enrollment table: printed Totals row", "The printed Totals row (2,106) does not match the sum of its own four school rows (2,083); the Totals row's grade columns do not match the school rows either (e.g. kindergarten 101 vs Mast Way 62 + Moharimet 66)."),
 ("Same-year October 1 enrollment", "The district's own October 1 report and the DOE's count differ by up to 47 students for the same date, in both directions."),
 ("School Year Enrollment table vs iExplore", "The district's own October 1 report differs from the DOE's school count by 1-19 students; FY2022 high school is 19 below (839 vs 858)."),
]
def size(o):
    if o["verdict"] == "agree": return ""
    try: pct = abs(float(o["diff_pct"]))
    except (TypeError, ValueError): return "pattern"
    return "rounding" if pct < 0.05 else ("minor" if pct < 1 else "material")
for o in OUT:
    if o["verdict"] != "agree" and not o["note"]:
        o["note"] = next((n for pre, n in NOTES if o["topic"].startswith(pre)), "")
    o["size"] = size(o)
# the same in-report inconsistency is reprinted by later reports: keep one row, list the reports
merged, seen = [], {}
for o in OUT:
    if o["cls"] == "district-internal" and o["verdict"] != "agree" and o["topic"].startswith(("Official Enrollment Counts", "School Year", "Same-year")):
        k = (o["topic"], o["fy"], o["a_value"], o["b_value"])
        if k in seen: seen[k]["a_source"] += "; also in report " + re.search(r"report (\d{4})", o["a_source"]).group(1); continue
        seen[k] = o
    merged.append(o)
OUT = merged
PAGE_USES = [  # (topic prefix, what the page shows; rule: state first)
 ("Enrollment, October 1", "State: NH DOE iExplore district total, every year"),
 ("Enrollment, high school", "State: iExplore school figure (FY2026 now 796)"), ("Enrollment, middle", "State (equal to report)"), ("Enrollment, K-4", "State (equal to report)"),
 ("Average teacher salary", "State: DOE salary file (FY2018 NH $58,278; FY2023 and FY2025 district values not plotted)"),
 ("Student-to-teacher", "State: DOE ratio file"), ("Cost per pupil", "State: DOE school-finance file"),
 ("Students with disabilities", "State: iExplore share. The district's own Oct 1 special-education count is a separate row labeled as district data"),
 ("Dropouts", "District counts (the state publishes a rate only; they agree)"),
 ("General Fund spending", "Page shows the DOE-25 recurring figure (state) in the finance rows; the 'budget not spent' row uses the district's approved and expended figures because the state has no series for the approved budget"),
 ("General Fund budget: approved", "District (no state series): page's operating-budget-versus-default row uses the warrant article"),
 ("Operating-budget warrant", "District (no state series)"),
 ("Tax Rate Impact", "District estimate, labeled as an estimate on the page; the actual rate change from the state's series is in the hover"),
 ("Projected local school rate", "Page shows the district's estimate and the state's actual change side by side"),
 ("Total expenditures", "State: DOE-25"), ("Total revenues", "State: DOE-25"), ("General fund balance", "Audit (no state series)"),
 ("iExplore enrollment", "State: iExplore district total (not the school sum)"), ("School Year Enrollment", "Not used"), ("Same-year", "Not used"), ("Official Enrollment Counts", "Level rows shown as printed; total is the iExplore district total")]
for o in OUT:
    o["page_uses"] = next((u for pre, u in PAGE_USES if o["topic"].startswith(pre)), "")
FIELDS = ["cls", "verdict", "size", "page_uses", "topic", "fy", "a_source", "a_value", "a_where", "b_source", "b_value", "b_where", "diff", "diff_pct", "note"]

def md():
    C = [o for o in OUT if o["verdict"] == "CONFLICT"]; B = [o for o in OUT if o["verdict"] == "different basis"]; PJ = [o for o in OUT if o["verdict"] == "projection"]; A = [o for o in OUT if o["verdict"] == "agree"]
    L = ["# Conflicts between district-printed and state-reported figures", "",
         "Generated by `build/conflicts.py` from `build/annual_report_tables.json` (the Report Card tables of the nine ORCSD annual reports, 2018-2026), `build/audit_metrics.json` (the audited statements, FY2018-FY2024), "
         "the NH DOE iExplore export in `raw/nh-doe/dashboard-exports-2026-11-22/`, and the DOE files the page already holds. Every comparison made, agreements included, is in `data/conflicts.csv` with the file and page of both numbers. "
         "Year key is the fiscal year (2017-18 = FY2018).", "",
         "**%d comparisons: %d agree, %d conflict, %d differ by basis, %d are the district's projection set against what happened.** A *conflict* means two sources print different numbers for the same measure and year and nothing about definitions explains it. "
         "A *different basis* row is a difference the documents explain only in part (audit vs the state's DOE-25 form). Where the district disagrees with itself, the row says so (`district-internal`)." % (len(OUT), len(A), len(C), len(B), len(PJ)), "",
         "## Rule used on the page: state first", "",
         "Where the district and the state print different numbers for the same measure, the page shows the state's (NH DOE or DRA) and the district's figure stays in this log. Where two state series disagree, the page uses the DOE's headline district figure and the others are listed here. District figures are used only where the state has no series for the measure (class size, Oyster River High School SAT, special-education counts, completers, dropout counts, the audited balance sheet).", "",
         "## What matters most", "",
         "1. **Enrollment: the DOE has two totals, and the district mixes them.** The DOE's district total (iExplore) is 25-34 above the sum of its own four schools every year from FY2019 on (the DOE student-to-teacher file uses roughly the school sum). The district's Report Card prints the DOE district total for FY2021-FY2025 but the school sum for FY2019, FY2020 and FY2026 (2,157, 2,168, 2,038 against the district total 2,190, 2,202, 2,064). Its own Official Enrollment table therefore has a Totals row 25-30 above the sum of its level rows from FY2021. **The page now uses the iExplore district total throughout.**",
         "2. **The annual report's second enrollment table (School Year Enrollment, the district's own October 1 report) disagrees with both.** For FY2022 it prints a Totals row of 2,106 that does not equal its four school rows (2,083), and the DOE says 2,130; high school is 839 against the DOE's 858.",
         "3. **The report's NH average teacher salary for FY2018 ($53,984) is not what the DOE files give ($58,277).** The report prints the DOE's 6/29/18 file; the DOE's current salary file and iExplore agree with each other at about $58,277. FY2024 differs the other way: the report and the DOE salary file say $67,096, iExplore says $66,576.",
         "4. **Student-to-teacher ratio, NH column:** the FY2025 figure (11.24) repeats FY2023's; DOE has 11.17. FY2024 prints 12.02 against DOE 11.3.",
         "5. **Columns copied forward.** The attendance table (FY2023-24 repeats FY2022-23 for every level, district and state) and the district's average teacher salary (FY2025 = FY2024 = $80,573, which the DOE file also repeats) are identical to the prior year. The cost-per-pupil table prints one more column than its header names (2026 report) and two NH figures with a decimal point for a comma (22.107 and 20.583).",
         "6. **Students with disabilities:** the district's October 1 special-education count gives a lower share of enrollment than the DOE's count, by 0.3 points in FY2018 widening to 2.2 points in FY2026. Both are plausible counts of different things; the documents do not say which students each includes.",
         "7. **Audited statements vs DOE-25:** the audit's governmental-funds expenditures exceed DOE-25 total expenditures by 2.5-13.6% and revenues by 0.7-3.0% every year. They are different forms (GAAP funds vs the state's DOE-25) and were not reconciled to the dollar; FY2018 is the widest gap. The audit's general-fund balance agrees with the page to the dollar in all seven years.",
         "8. **Budget tables (new):** the annual reports' own arithmetic ties to the dollar except the FY2024 approved department rows, which add to $1,000 more than the printed total (and two $1 rounding differences in the 2024 report). The approved General Fund total exceeds the total proposed a year earlier every year (FY2021 by $1.25M); only FY2019 is explained by the report (two contract articles).",
         "9. **Tax-rate impact tables:** the table's 'current' local rate equals the state's rate for that year and town (the page uses the state's). The last column is headed 'Impact Revised' and does not subtract to proposed minus current (FY2025 Durham: 12.15 - 11.58 = 0.57, printed 0.40). The 2018 report prints Madbury's assessed value as 235,434,027 in one column and 235,343,027 in the other.",
         "10. **Projected versus set rates:** holding assessed value fixed, the district's projected next-year rate differs from the rate the DRA set by under $1 per $1,000 in most town-years but by $2.61 to $9.19 in five (Durham FY2019 and FY2024, Madbury FY2021 and FY2026, Lee FY2022), because revaluations and state aid moved the real rate. See the section near the end.",
         "11. **District 'expended' General Fund (budget table) vs the audit vs DOE-25:** within 0.5% of the audit in FY2021-FY2024 but 0.9-7.6% apart in FY2018-FY2020, and 0.5-5.9% above the state's DOE-25 recurring figure in every year; none of the documents reconciles them.",
         "12. **MS-26 (the NH DRA budget form, reprinted as images in the 2025 and 2026 reports; OCR'd, every subtotal re-added) vs DOE-25:** for FY2024 and FY2025 regular programs, vocational, student support, school administration, business, transportation and debt interest tie to the dollar, but special programs ($312K and $500K), other instruction, instructional staff services and (FY2025) plant operations differ, DOE-25 mostly higher. The 2025 report's MS-26 prints FY2024 plant operations as $0 against $4.36M in DOE-25, so its total actual spending is $4.3M low. The MS-26's FY2026 'appropriated' column includes the $1.67M of union-contract warrant articles that the page's operating budget leaves out.",
         "13. **NH SAT averages:** the district's printed State column does not match the College Board's New Hampshire report (the DOE hosts it) in any year but 2018, by up to 27 points; the page now uses the College Board's figures for all graduates (class of 2018-2025).",
         "14. **Special education spending, three amounts for one year:** for FY2025 special programs are $8,419,644 in the district's RSA 32:11-a table, $7,970,563 in the DOE-25 and $7,470,356 in the MS-26 (FY2024: $8,023,162, $7,694,329, $8,006,444). The state aid and Medicaid lines of the RSA table tie to the MS-26 revenue lines to the dollar, so the disagreement is in expenditure classification. The page shows the district's table in its own row, labeled as the district's.",
         "15. **General Fund: the audit and the DOE-25 disagree about the balance and about the direction of change.** The audit's General Fund balance is $0.6M to $1.8M above the DOE-25's General Fund equity every year FY2018-FY2024, and in FY2019, FY2022 and FY2024 they disagree on whether the fund gained or lost money during the year (e.g. FY2024: audit +$286K, DOE-25 -$139K). The page's fund-results row uses the DOE-25 (state first); the fund balance row uses the audit. See General Fund balance in the log below.",
         "", "## Where the Report Card matches the state", "",
         "Enrollment by level, average teacher salary (district), cost per pupil by level, student-to-teacher ratio (district), dropout counts against iExplore's dropout rate (count divided by grade 9-12 enrollment), and iExplore totals of expenditures, revenues, cost per pupil and salary against the DOE-25 and DOE files the page holds all agree wherever both exist (counts in the CSV). "
         "The Report Card is tied to the DOE for these measures; the differences above are where it is not.", ""]
    topics = collections.OrderedDict()
    for o in C: topics.setdefault(o["topic"], []).append(o)
    L += ["## Every conflict", ""]
    for t, rows in topics.items():
        L.append("### " + t); L.append("")
        if rows[0]["note"]: L += [rows[0]["note"], ""]
        if rows[0].get("page_uses"): L += ["**On the page:** " + rows[0]["page_uses"], ""]
        L.append("| FY | A | value | B | value | diff | size |"); L.append("|---|---|---|---|---|---|---|")
        for o in rows:
            f = lambda v: ("{:,.2f}".format(v).rstrip("0").rstrip(".") if isinstance(v, float) else str(v))
            L.append("| %s | %s (%s) | %s | %s (%s) | %s | %s | %s |" % (o["fy"], o["a_source"], o["a_where"], f(o["a_value"]), o["b_source"], o["b_where"], f(o["b_value"]), f(o["diff"]) if o["diff"] != "" else "", o["size"]))
        L.append("")
    L += ["## Differences of basis", ""]
    for t in sorted({o["topic"] for o in B}):
        rows = [o for o in B if o["topic"] == t]
        L += ["**%s.** %s" % (t, rows[0]["note"]), "", "| FY | A | B | diff % |", "|---|---|---|---|"]
        L += ["| %s | %s: %s | %s: %s | %s |" % (o["fy"], o["a_source"], "{:,.2f}".format(o["a_value"]).rstrip("0").rstrip("."), o["b_source"], "{:,.2f}".format(o["b_value"]).rstrip("0").rstrip("."), o["diff_pct"]) for o in rows]
        L.append("")
    L += ["## The district's tax-rate projection against the rate that was set", "",
          "Each annual report prints a projected local school rate per $1,000 for the next year (assessed value held fixed). The table below sets it against the NH DRA rate that was actually set. The projection is meant to isolate the budget's effect, so a gap is not an error; it shows how much the real rate moves for other reasons (revaluations, enrollment shares, state aid). ",
          "", "| FY | town | projected | set by DRA | diff |", "|---|---|---|---|---|"]
    for o in PJ:
        L.append("| %s | %s | %s | %s | %+.2f |" % (o["fy"], re.search(r"(Durham|Lee|Madbury)", o["a_source"]).group(1), o["a_value"], o["b_value"], o["diff"]))
    L.append("")
    L += ["## Other defects found in the printed documents", "",
          "These are not two-source conflicts, but they affect which number to trust.", "",
          "- **District, 2021 annual report:** the Average Class Size table's Middle School row prints five column pairs under six headings (and zeros for the district), so it cannot be read; the Audit Balance Sheet and Statement of Revenues pages reprint the FY2019 statements where the FY2020 ones belong (the page uses the 2020 audit itself for FY2020).",
          "- **District, 2026 annual report:** the Cost Per Pupil table names six years in its header and prints seven columns; the last column is read here as the next year. Two NH figures carry a period for a comma (22.107, 20.583). The Official Enrollment table prints 2,038 for 2025-26; the School Year Enrollment table beside it prints 2,040.",
          "- **District, attendance:** the report's 2023-24 column repeats 2022-23 and the 2024-25 column jumps to about 98% for the district and the state alike, which looks like a change in how it is measured; the page leaves those years out.",
          "- **State, teacher salary file:** FY2023 lists $63,538 for Oyster River (about 17% under the years on either side) and FY2025 repeats the FY2024 figure of $80,573 to the dollar although the staff count changed. The page does not plot either.",
          "- **State, iExplore:** the district enrollment above the sum of its four schools (above); cost per pupil for FY2026 is suppressed (`*CS`).", ""]
    L += ["## Limits", "",
          "Compared: the Report Card tables (SAT and special-education counts have no independent state series here), audit totals against DOE-25, iExplore against the DOE files. **Not compared:** the annual reports' budget-by-location table for FY2025 onward (it is an image in the 2025 and 2026 reports) and the revenue tables against DOE-25 by function; NH SAT by year against the College Board's state reports; district per-school class size against iExplore (different definitions); anything the DOE publishes only in Tableau pages that could not be exported. "
          "A *conflict* here means only that two printed numbers differ; the third source that would settle which is right is not always in hand, and the notes say where it is not.", ""]
    return "\n".join(L)

if __name__ == "__main__":
    with open(P("data", "conflicts.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore"); w.writeheader(); w.writerows(OUT)
    open(P("CONFLICTS.md"), "w").write(md())
    c = collections.Counter(o["verdict"] for o in OUT)
    print(len(OUT), "comparisons", dict(c))
