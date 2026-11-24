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

        # ---- General Fund equity by component and trust-fund equity (balance sheet, DOE25 sheet rows 30-53; GF = first fund column, trust = fifth)
        bs = [r for r in rows if r["sheet"] == "DOE25" and 30 <= r["row"] <= 53]
        def bsum(pred, col=0):
            return sum(_nz((list(r["values"]) + [None] * 5)[col]) for r in bs if pred(r["label"].strip().upper()))
        put("fb_prep", y, bsum(lambda l: l.startswith("RESERVE FOR PREPAID")))
        put("fb_vote", y, bsum(lambda l: l.startswith("RESERVE FOR AMTS VOTED")))
        put("fb_enc", y, bsum(lambda l: l.startswith("RESERVE FOR ENCUMBRANCES") or l.startswith("RESERVED FOR ENCUMBRANCES")) + bsum(lambda l: l.startswith("RESERVE FOR CONTINUING")))
        put("fb_ret", y, bsum(lambda l: l.startswith("UNASSIGNED FUND BALANCE RETAINED")))
        put("fb_una", y, bsum(lambda l: l == "UNASSIGNED FUND BALANCE"))
        put("fb_trust", y, bsum(lambda l: l == "TOTAL FUND EQUITY", 4))

        # ---- Special education expenditure detail (DOE25 sheet page 21: instruction, related services, administration, legal, transportation; page 22 tuition) and its revenue lines
        def last(r):
            n = [x for x in r["values"] if isinstance(x, (int, float))]
            return n[-1] if n else 0.0
        p21 = {str(r["line"]): r for r in rows if r["sheet"] == "DOE25" and str(r["page"]) == "21" and str(r["line"]) in ("4", "8", "12", "16", "20", "21")}
        assert set(p21) == {"4", "8", "12", "16", "20", "21"}, (y, sorted(p21))
        for k, ln in (("rsd_ins", "4"), ("rsd_rel", "8"), ("rsd_adm", "12"), ("rsd_leg", "16"), ("rsd_trn", "20"), ("rsd_sub", "21")):
            put(k, y, last(p21[ln]))
        put("rsd_tui", y, sum(last(r) for r in rows if r["sheet"] == "DOE25" and r["label"].startswith(("Special Program Tuition", "Special Program Residential"))))
        put("rsd_tot", y, out["rsd_sub"][y] + out["rsd_tui"][y])
        def rev(acct):
            m = [r for r in rows if r["sheet"] == "DOE25" and str(r["acct"]) == acct and 100 < r["row"] < 175]
            assert len(m) == 1, (y, acct, len(m))
            return sum(_nz(x) for x in m[0]["values"][:5])
        put("rsd_aid", y, rev("3230")); put("rsd_idea", y, rev("4570")); put("rsd_med", y, rev("4580"))
        put("rsd_rev", y, out["rsd_aid"][y] + out["rsd_idea"][y] + out["rsd_med"][y])
        put("rsd_net", y, out["rsd_tot"][y] - out["rsd_rev"][y])

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

        # ---- Tuition paid to other schools, by program (ACTIVITY block; the fourth number is the all-schools total)
        act = [r for r in rows if r["sheet"] == "DOE25" and r.get("hdr") == "ACTIVITY"]
        tui = []
        for r in act:
            m = re.match(r"(Regular|Special|Vocational) Program Tuition to (.+)$", r["label"].strip())
            if m:
                tui.append((m.group(1), m.group(2), _nz(r["values"][3])))
        assert len(tui) == 12, (y, len(tui))
        priv = sum(v for kind, dest, v in tui if kind == "Special" and dest.startswith("Private"))
        put("tuit_priv", y, priv)
        put("tuit_spub", y, sum(v for kind, dest, v in tui if kind == "Special") - priv)
        put("tuit_voc", y, sum(v for kind, dest, v in tui if kind == "Vocational"))
        put("tuit_reg", y, sum(v for kind, dest, v in tui if kind == "Regular"))
        put("tuit_tot", y, sum(v for kind, dest, v in tui))

        # ---- Student transportation by type of trip (ACTIVITY block, accounts 2721 to 2729; sixth number is the total)
        def tr(prefix):
            m = [r for r in act if r["label"].strip().startswith(prefix)]
            assert len(m) == 1, (y, prefix, len(m))
            return _nz(m[0]["values"][5])
        put("trans_reg", y, tr("Regular To and From"))
        put("trans_sped", y, tr("All Special Education Transportation"))
        put("trans_voc", y, tr("Vocational Education Transportation"))
        put("trans_oth", y, tr("Intra-District Transportation") + tr("Other Transportation"))
        put("trans_tot", y, sum(out[k][y] for k in ("trans_reg", "trans_sped", "trans_voc", "trans_oth")))

        # ---- Bond debt schedule (the statement block that holds the debt lines; five issue columns then a total)
        ds = [r for r in rows if r["sheet"] == "DOE25" and r.get("hdr") == "STATEMENT OF ANALYSIS OF CHANGE IN FUND EQUITY"]

        def dl(prefix):
            m = [r for r in ds if r["label"].strip().startswith(prefix)]
            assert len(m) == 1, (y, prefix, len(m))
            return (list(m[0]["values"]) + [None] * 7)[:6]
        rp, ri = dl("Remaining Principal Balance Due"), dl("Remaining Interest Balance Due")
        np_, ni, nt = (dl("Amount of Principal to be Paid Next Fiscal Year"), dl("Amount of Interest to be Paid Next Fiscal Year"),
                       dl("Total Debt Next Fiscal Year"))
        put("bond_prin", y, _nz(rp[5])); put("bond_int", y, _nz(ri[5]))
        put("ds_prin", y, _nz(np_[5])); put("ds_int", y, _nz(ni[5])); put("ds_tot", y, _nz(nt[5]))
        for i in range(5):
            put("bond_p%d" % (i + 1), y, _nz(rp[i]))
            put("ds_n%d" % (i + 1), y, _nz(nt[i]))
    return out


if __name__ == "__main__":
    f = fields()
    for k in sorted(f):
        print(k, [f[k].get(y) for y in YEARS])
