"""Values for the page rows that come from the DOE-25 workbooks beyond the District Profile sheet.

Reads build/doe25_all.json (made by doe25_extract.py from raw/nh-doe25/*.xlsx) and returns
{field: {fiscal_year_end: value}}.  rc_data.py calls fields(); verify_doe25_rows.py re-reads the
workbooks independently and checks every number returned here.

Fiscal year key = the year the school year ends (FY2018 = 2017-18).
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
YEARS = range(2018, 2026)


def _load():
    return json.load(open(os.path.join(HERE, "doe25_all.json")))


def _nz(v):
    return v if isinstance(v, (int, float)) else 0.0


def fields():
    D = _load()
    out = {}

    def put(k, y, v):
        out.setdefault(k, {})[y] = round(v, 2)

    for y in YEARS:
        rows = [r for r in D if r["fy"] == y]
        # ---- General Fund expenditures by type (DOE25 sheet, "Total Expenditures General Fund")
        g = [r for r in rows if r["sheet"] == "DOE25" and r["label"].startswith("Total Expenditures General Fund")]
        assert len(g) == 1, (y, len(g))
        v = [_nz(x) for x in g[0]["values"][:7]]
        for k, x in zip(("gfo_sal", "gfo_ben", "gfo_pur", "gfo_sup", "gfo_prop", "gfo_oth", "gfo_tot"), v):
            put(k, y, x)

        # ---- Change in fund equity by fund (General, Food Service, Special Revenue)
        st = [r for r in rows if r["sheet"] == "DOE25" and r.get("hdr") == "STATEMENT OF ANALYSIS OF CHANGE IN FUND EQUITY"]

        def one(prefix):
            m = [r for r in st if r["label"].upper().startswith(prefix)]
            assert len(m) == 1, (y, prefix, len(m))
            return [_nz(x) for x in m[0]["values"][:3]]
        beg, rev, add, exp, dele, end = (one("TOTAL FUND EQUITY, JULY 1"), one("REVENUE"), one("TOTAL ADDITIONS"),
                                         one("EXPENDITURES"), one("TOTAL DELETIONS"), one("TOTAL FUND EQUITY JUNE 30"))
        for i, f in enumerate(("gen", "food", "spr")):
            put("fe_%s_rev" % f, y, add[i])          # total additions = revenue + other additions
            put("fe_%s_exp" % f, y, dele[i])         # total deletions = expenditures + other deletions
            put("fe_%s_end" % f, y, end[i])
            put("fe_%s_beg" % f, y, beg[i])

        # ---- Instructional personnel by job class (Salaries-Benefits sheet; blocks 1100, 1200, 1300, 1400)
        sb = [dict(r, values=(list(r["values"]) + [None, None, None])[1:3]) for r in rows if r["sheet"] == "Salaries-Benefits"]
        blocks, cur = [], None
        for r in sb:
            lab = r["label"].strip().lower()
            if lab == "totals":
                cur = {"tot": r["values"][:2], "cls": {}}
                blocks.append(cur)
            elif cur is not None and re.search(r"teacher", lab):
                cur["cls"]["t"] = r["values"][:2]
            elif cur is not None and re.search(r"aide", lab):
                cur["cls"]["a"] = r["values"][:2]
            elif cur is not None and re.search(r"other", lab):
                cur["cls"]["o"] = r["values"][:2]
        assert len(blocks) == 4, (y, len(blocks))
        for c in ("t", "a", "o"):
            put("pers_%s_sal" % c, y, sum(_nz(b["cls"].get(c, [0, 0])[0]) for b in blocks))
            put("pers_%s_ben" % c, y, sum(_nz(b["cls"].get(c, [0, 0])[1]) for b in blocks))

        # ---- Spending by school, all funds (School Level Expenditures; first sheet year is FY2019)
        sl = [r for r in rows if r["sheet"] == "School Level"]
        for r in sl:
            lab = r["label"].lower()
            vals = r["values"]
            if not vals or lab.startswith("oyster river coop"):
                continue
            tot = _nz(vals[2]) if len(vals) > 2 and vals[2] is not None else _nz(vals[0])
            if lab.startswith("mast way"):
                k = "sch_mw"
            elif lab.startswith("moharimet"):
                k = "sch_mo"
            elif "preschool" in lab:
                k = "sch_ps"
            elif "middle" in lab:
                k = "sch_ms"
            elif "high" in lab:
                k = "sch_hs"
            elif lab.startswith("out of district"):
                k = "sch_od"
            else:
                continue
            if k == "sch_od":
                out.setdefault(k, {})[y] = round(out.get(k, {}).get(y, 0) + tot, 2)
            else:
                put(k, y, tot)
    return out


if __name__ == "__main__":
    f = fields()
    for k in sorted(f):
        print(k, [f[k].get(y) for y in YEARS])
