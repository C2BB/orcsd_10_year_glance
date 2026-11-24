"""The 'Why have property taxes gone up?' section: baseline numbers, eight common explanations tested against the data, and two bridge tables
(where the extra spending went, and who paid for it).  Everything is computed from the dataset rows (build/make_data.py passes them in), so
no number is typed here.  Every stat carries the raw values (av, bv) next to the display strings; build/verify_claims.py recomputes them independently.

Window: FY2017-18 (rows[0]) to FY2024-25 (rows[7]), the latest year with actual spending in the DOE-25.  'After inflation' uses the
Northeast CPI-U fiscal-year averages already in the dataset (cpi_ne).
"""
import re
import doe25


def _m(v, d=2):
    return "$%.*fM" % (d, v / 1e6)


def _d(v):
    return "${:,.0f}".format(v)


def _p(v, d=1, sign=False):
    return (("%+.*f%%" if sign else "%.*f%%") % (d, v)).replace("-", "\u2212")


def _pts(v):
    return ("%+.1f pts" % v).replace("-", "\u2212")


def _prose(t):
    """Sentences read 'rose 9%', not 'rose +9%': drop the plus sign in running text."""
    return re.sub(r"\+(?=\d)", "", t)


def compute(rows):
    A, B, C, E = rows[0], rows[7], rows[8], rows[9]          # FY18, FY25, FY26, FY27
    cpi = B["cpi_ne"] / A["cpi_ne"]
    cpi_pct = 100 * (cpi - 1)

    def chg(a, b):
        return 100 * (b / a - 1)

    def real(a, b):
        return 100 * (b / a / cpi - 1)

    def stat(label, a, b, fa, fb, av=None, bv=None, pct=True, real_too=False, note=None, text=None):
        if text:
            return {"label": label, "text": text}
        s = {"label": label, "a": fa, "b": fb}
        if av is not None:
            s["av"], s["bv"] = round(av, 4), round(bv, 4)
            if pct:
                s["chg"] = _p(chg(av, bv), 1, True)
                if real_too:
                    s["real"] = _p(real(av, bv), 1, True)
        if note:
            s["note"] = note
        return s

    out = {"window": {"a": A["fy"], "b": B["fy"], "cpi_pct": round(cpi_pct, 1)}}

    # ---------------------------------------------------------------- baseline
    levy_a, levy_b, levy_c = A["levy_tot"], B["levy_tot"], C["levy_tot"]
    rec_a, rec_b = A["actual_recurring"], B["actual_recurring"]
    rate_a, rate_b, rate_c = 1000 * levy_a / A["eq_tot"], 1000 * levy_b / B["eq_tot"], 1000 * levy_c / C["eq_tot"]
    out["baseline"] = [
        {"id": "levy", "title": "Local school property tax raised", "a": _m(levy_a, 1), "b": _m(levy_b, 1), "chg": _p(chg(levy_a, levy_b), 1, True), "av": levy_a, "bv": levy_b,
         "note": "FY 2025-26: %s (%s since FY 2017-18)" % (_m(levy_c, 1), _p(chg(levy_a, levy_c), 0, True))},
        {"id": "spend", "title": "Operating spending", "a": _m(rec_a, 1), "b": _m(rec_b, 1), "chg": _p(chg(rec_a, rec_b), 1, True), "av": rec_a, "bv": rec_b,
         "note": "After inflation %s (prices rose %s)" % (_p(real(rec_a, rec_b), 1, True), _p(cpi_pct, 1, True))},
        {"id": "enr", "title": "Students (October 1)", "a": "{:,}".format(A["enrollment"]), "b": "{:,}".format(B["enrollment"]), "chg": _p(chg(A["enrollment"], B["enrollment"]), 1, True),
         "av": A["enrollment"], "bv": B["enrollment"], "note": "FY 2026-27: {:,} ({} since FY 2017-18)".format(E["enrollment"], _p(chg(A["enrollment"], E["enrollment"]), 1, True))},
        {"id": "rate", "title": "School tax per $1,000 of property value, whole district", "a": "$%.2f" % rate_a, "b": "$%.2f" % rate_b, "chg": _p(chg(rate_a, rate_b), 0, True), "av": rate_a, "bv": rate_b,
         "note": "Property values rose %s while the levy rose %s. FY 2025-26: $%.2f. Each town's own rate depends on its own values." % (_p(chg(A["eq_tot"], B["eq_tot"]), 0, True), _p(chg(levy_a, levy_b), 0, True), rate_c)},
    ]

    # ---------------------------------------------------------------- the bridge: where the extra spending went
    def cat(r, keys):
        return sum(r[k] for k in keys)
    cats = [("Instruction (regular, vocational and other)", ("fn_reg", "fn_voc", "fn_oi"), "instruction"),
            ("Special programs", ("fn_spec",), "special"),
            ("Student and instructional support (counselors, nurses, library, curriculum)", ("fn_ss", "fn_isup"), "support"),
            ("Administration (central, school and business)", ("fn_gab", "fn_sadm", "fn_bus"), "admin"),
            ("Buildings (plant operations)", ("fn_plant",), "plant"),
            ("Transportation", ("fn_trans",), "transport"),
            ("Food service", ("fn_food",), "food"),
            ("Bond interest", ("fn_bint",), "interest")]
    inc = rec_b - rec_a
    spend_rows = []
    for name, keys, cid in cats:
        a, b = cat(A, keys), cat(B, keys)
        spend_rows.append({"id": cid, "name": name, "a": _m(a), "b": _m(b), "chg": _p(chg(a, b), 1, True), "real": _p(real(a, b), 1, True),
                           "base_share": _p(100 * a / rec_a), "inc_share": _p(100 * (b - a) / inc), "av": a, "bv": b,
                           "flag": "faster" if chg(a, b) > chg(rec_a, rec_b) else "slower"})
    prin_a, prin_b = doe25.D[2018]["prin"], doe25.D[2025]["prin"]
    out["bridge"] = {
        "spend": spend_rows,
        "total": {"name": "Operating spending (the measure used elsewhere on the page)", "a": _m(rec_a), "b": _m(rec_b), "chg": _p(chg(rec_a, rec_b), 1, True), "real": _p(real(rec_a, rec_b), 1, True), "av": rec_a, "bv": rec_b},
        "principal": {"name": "Bond principal repaid (not counted in operating spending)", "a": _m(prin_a), "b": _m(prin_b), "chg": _p(chg(prin_a, prin_b), 1, True), "real": _p(real(prin_a, prin_b), 1, True), "av": prin_a, "bv": prin_b},
        "total_all": {"name": "Operating spending plus bond principal", "a": _m(rec_a + prin_a), "b": _m(rec_b + prin_b), "chg": _p(chg(rec_a + prin_a, rec_b + prin_b), 1, True), "real": _p(real(rec_a + prin_a, rec_b + prin_b), 1, True), "av": rec_a + prin_a, "bv": rec_b + prin_b},
    }
    revs = [("Local property tax", "rev_local", "local"), ("Other local revenue (tuition, meals, interest, rentals)", "rev_oth_local", "otherlocal"),
            ("State adequacy aid and the statewide education property tax kept in the district", "rev_adeq", "adequacy"), ("Other state aid (building aid, special education aid, other)", "rev_ostate", "otherstate"),
            ("Federal aid", "rev_fed", "federal")]
    rinc = B["rev_tot"] - A["rev_tot"]
    out["bridge"]["revenue"] = [{"id": cid, "name": n, "a": _m(A[k]), "b": _m(B[k]), "chg": _p(chg(A[k], B[k]), 1, True), "base_share": _p(100 * A[k] / A["rev_tot"]), "end_share": _p(100 * B[k] / B["rev_tot"]),
                                 "inc_share": _p(100 * (B[k] - A[k]) / rinc), "av": A[k], "bv": B[k]} for n, k, cid in revs]
    out["bridge"]["revenue_total"] = {"name": "Total revenue", "a": _m(A["rev_tot"]), "b": _m(B["rev_tot"]), "chg": _p(chg(A["rev_tot"], B["rev_tot"]), 1, True), "av": A["rev_tot"], "bv": B["rev_tot"]}
    by = {r["id"]: r for r in spend_rows}

    # ---------------------------------------------------------------- the eight claims
    cards = []
    state_a, state_b = A["rev_adeq"] + A["rev_ostate"], B["rev_adeq"] + B["rev_ostate"]
    sh_a, sh_b = 100 * state_a / A["rev_tot"], 100 * state_b / B["rev_tot"]
    pps_a, pps_b = state_a / A["enrollment"], state_b / B["enrollment"]
    extra = sh_a / 100 * B["rev_tot"] - state_b
    cards.append({
        "id": "state", "title": "“The state is pushing costs onto local taxpayers.”", "name": "Downshifting",
        "shows": "State aid per student rose %s while prices rose %s. The state's share of the district's revenue fell from %s to %s; at the FY 2017-18 share the state would have paid %s more in FY 2024-25, about %s of the local tax. The retirement contributions the district must make rose %s." % (
            _p(chg(pps_a, pps_b), 0, True), _p(cpi_pct, 0, True), _p(sh_a), _p(sh_b), _m(extra, 1), _p(100 * extra / B["rev_local"]), _p(chg(A["nhrs_con"], B["nhrs_con"]), 0, True)),
        "stats": [
            stat("State aid, share of district revenue", sh_a, sh_b, _p(sh_a), _p(sh_b), sh_a, sh_b, pct=False, note=_pts(sh_b - sh_a)),
            stat("State aid per student", pps_a, pps_b, _d(pps_a), _d(pps_b), pps_a, pps_b, real_too=True),
            stat("State building aid for school bonds", A["bld_aid"], B["bld_aid"], _d(A["bld_aid"]) + " a year", _d(B["bld_aid"]), A["bld_aid"], B["bld_aid"], pct=False, note="paid through FY 2022-23, none since FY 2023-24"),
            stat("Retirement system contributions paid by the district", A["nhrs_con"], B["nhrs_con"], _m(A["nhrs_con"]), _m(B["nhrs_con"]), A["nhrs_con"], B["nhrs_con"]),
            ],
        "limits": "How much the state should carry is a policy question this page cannot answer. State aid here includes the statewide education property tax, which is collected on local tax bills and kept in the district. Retirement rates are set by the NH Retirement System.",
        "links": [["Local tax vs. state aid per student", "pay"], ["State adequacy aid", "aid"], ["Local share of revenue", "local"], ["State building aid", "bldaid"], ["Retirement system shortfall", "nhrs"]]})

    efa = lambda r: (r["efa_dur"] or 0) + (r["efa_lee"] or 0) + (r["efa_mad"] or 0)
    y22, y25, y26, y27 = rows[4], B, C, E
    cards.append({
        "id": "efa", "title": "“Education Freedom Accounts (vouchers) are driving it.”", "name": "Education Freedom Accounts",
        "shows": "Accounts held by residents of Durham, Lee and Madbury rose from about %d (FY 2021-22) to %d (FY 2025-26). Over those years the district's state adequacy aid did not fall (%s in FY 2024-25, %s in FY 2025-26, %s estimated for FY 2026-27), and the state's phase-out grants to the district were about %s a year. Enrollment fell by %d students between FY 2021-22 and FY 2025-26, while the number of accounts rose by %d." % (
            round(efa(y22)), round(efa(y26)), _m(y25["adq_total"], 2), _m(y26["adq_total"], 2), _m(y27["adq_total"], 2), "$" + "{:,}".format(int(round(y26["efa_po"], -3))), y22["enrollment"] - y26["enrollment"], round(efa(y26) - efa(y22))),
        "stats": [
            stat("Accounts held by residents of the three towns", efa(y22), efa(y26), "%d (FY22)" % round(efa(y22)), "%d (FY26)" % round(efa(y26)), efa(y22), efa(y26), pct=False, note="%d in FY 2026-27" % round(efa(y27))),
            stat("District enrollment", y22["enrollment"], y26["enrollment"], "{:,} (FY22)".format(y22["enrollment"]), "{:,} (FY26)".format(y26["enrollment"]), y22["enrollment"], y26["enrollment"]),
            stat("State adequacy aid and statewide education tax paid to the district", y25["adq_total"], y26["adq_total"], _m(y25["adq_total"]) + " (FY25)", _m(y26["adq_total"]) + " (FY26, state estimate)", y25["adq_total"], y26["adq_total"]),
            stat("State phase-out grants to the district for students who left", y25["efa_po"], y26["efa_po"], _d(y25["efa_po"]) + " (FY25)", _d(y26["efa_po"]) + " (FY26)", y25["efa_po"], y26["efa_po"], pct=False),
            ],
        "limits": "The DOE does not say how many account holders were previously in ORCSD schools. The accounts are paid by the state's Education Trust Fund, not by district taxes; the district feels them through its adequacy aid, which the state reduces for each account holder, and that reduction is already in the aid figures shown.",
        "links": [["Education Freedom Account students", "efa"], ["State adequacy aid", "aid"], ["Students enrolled", "students"], ["Enrollment projections vs. actual", "proj"]]})

    adm_sh_a, adm_sh_b = 100 * cat(A, ("fn_gab", "fn_sadm", "fn_bus")) / rec_a, 100 * cat(B, ("fn_gab", "fn_sadm", "fn_bus")) / rec_b
    ad = by["admin"]
    cards.append({
        "id": "admin", "title": "“Administration and overhead are too big.”", "name": "Administration",
        "shows": "Administration spending grew %s against %s for operating spending as a whole, and is now %s of operating spending against %s for the average NH district. It accounts for %s of the increase in spending. The superintendent's pay is the highest among %d NH superintendents and %s above the median." % (
            ad["chg"], _p(chg(rec_a, rec_b), 0, True), _p(adm_sh_b), _p(B["nh_adm_sh"]), ad["inc_share"], B["co_sup_n"], _p(100 * (B["co_sup"] / B["co_sup_med"] - 1), 0)),
        "stats": [
            stat("Administration and business spending", ad["av"], ad["bv"], _m(ad["av"]), _m(ad["bv"]), ad["av"], ad["bv"], real_too=True),
            stat("Share of operating spending (NH average in note)", adm_sh_a, adm_sh_b, _p(adm_sh_a), _p(adm_sh_b), adm_sh_a, adm_sh_b, pct=False, note="NH average %s → %s" % (_p(A["nh_adm_sh"]), _p(B["nh_adm_sh"]))),
            stat("Superintendent pay (rank among NH superintendents)", A["co_sup"], B["co_sup"], "%s (#%d of %d)" % (_d(A["co_sup"]), A["co_sup_rk"], A["co_sup_n"]), "%s (#%d of %d)" % (_d(B["co_sup"]), B["co_sup_rk"], B["co_sup_n"]), A["co_sup"], B["co_sup"], note="NH median %s → %s" % (_d(A["co_sup_med"]), _d(B["co_sup_med"]))),
            stat("Students per non-teacher staff member, all support staff (FY21 to FY25)", rows[3]["nts"], B["nts"], "%.1f" % rows[3]["nts"], "%.1f" % B["nts"], rows[3]["nts"], B["nts"], pct=False, note="NH %.1f → %.1f; fewer students per staff member means more staff" % (rows[3]["nts_nh"], B["nts_nh"])),
            ],
        "limits": "These are the DOE's categories: general, school and business administration. Some administrative work may be booked elsewhere, and a smaller student count spreads fixed administration over fewer students. Non-teacher staff includes aides, nurses and others, not only administrators.",
        "links": [["Administration and business share", "adm"], ["General Fund spending by type", "gfo"], ["Superintendent and central-office pay", "cpay"], ["Students per non-teacher staff", "nts"]]})

    sp = by["special"]
    sp_sh_a, sp_sh_b = 100 * A["fn_spec"] / rec_a, 100 * B["fn_spec"] / rec_b
    su = by["support"]
    cards.append({
        "id": "sped", "title": "“Special education spending is driving it.”", "name": "Special education",
        "shows": "Spending the DOE classes as special programs grew %s against %s for operating spending as a whole, and fell from %s to %s of the budget (NH average %s). It accounts for %s of the increase. The share of students with disabilities rose from %s to %s, below the NH average of %s." % (
            sp["chg"], _p(chg(rec_a, rec_b), 0, True), _p(sp_sh_a), _p(sp_sh_b), _p(B["nh_spec_sh"]), sp["inc_share"], _p(A["swd"]), _p(B["swd"]), _p(B["swd_nh"])),
        "stats": [
            stat("Special programs spending", sp["av"], sp["bv"], _m(sp["av"]), _m(sp["bv"]), sp["av"], sp["bv"], real_too=True),
            stat("Share of operating spending", sp_sh_a, sp_sh_b, _p(sp_sh_a), _p(sp_sh_b), sp_sh_a, sp_sh_b, pct=False, note="NH average %s → %s" % (_p(A["nh_spec_sh"]), _p(B["nh_spec_sh"]))),
            stat("Students with disabilities, share of students", A["swd"], B["swd"], _p(A["swd"]), _p(B["swd"]), A["swd"], B["swd"], pct=False, note="NH %s → %s" % (_p(A["swd_nh"]), _p(B["swd_nh"]))),
            stat("Tuition paid to private and other schools for special programs", A["tuit_priv"], B["tuit_priv"], _d(A["tuit_priv"]), _d(B["tuit_priv"]), A["tuit_priv"], B["tuit_priv"], note="peak %s in FY 2021-22" % _d(rows[4]["tuit_priv"])),
            stat("State special education aid", A["rsd_aid"], B["rsd_aid"], _d(A["rsd_aid"]), _d(B["rsd_aid"]), A["rsd_aid"], B["rsd_aid"], note="peak %s in FY 2022-23" % _d(rows[5]["rsd_aid"])),
            ],
        "limits": "Special programs is the DOE-25 category for special education and similar programs. Related services booked under student and instructional support, such as therapists, are outside it, and that category rose %s (%s of the increase)." % (su["chg"], su["inc_share"]),
        "links": [["Special programs per student", "spec"], ["Special education spending and what offsets it", "rsa"], ["Tuition paid to other schools", "tuit"], ["State special education aid", "spedaid"], ["Students with disabilities vs. NH", "swd"]]})

    ben_a, ben_b = 100 * A["instr_ben"] / A["instr_sal"], 100 * B["instr_ben"] / B["instr_sal"]
    ins = by["instruction"]
    cards.append({
        "id": "pay", "title": "“Teacher pay and benefits are the problem.”", "name": "Salaries and benefits",
        "shows": "Instruction spending overall grew %s, slower than the %s for operating spending, with salaries up %s and benefits up %s. Benefits rose from %s to %s of salaries. Average teacher pay is %s above the NH average, down from %s." % (
            ins["chg"], _p(chg(rec_a, rec_b), 0, True), _p(chg(A["instr_sal"], B["instr_sal"]), 0, True), _p(chg(A["instr_ben"], B["instr_ben"]), 0, True), _p(ben_a), _p(ben_b),
            _p(100 * (C["t_avg"] / C["t_avg_state"] - 1), 0), _p(100 * (A["t_avg"] / A["t_avg_state"] - 1), 0)),
        "stats": [
            stat("Instruction salaries", A["instr_sal"], B["instr_sal"], _m(A["instr_sal"]), _m(B["instr_sal"]), A["instr_sal"], B["instr_sal"], real_too=True),
            stat("Instruction benefits", A["instr_ben"], B["instr_ben"], _m(A["instr_ben"]), _m(B["instr_ben"]), A["instr_ben"], B["instr_ben"], real_too=True),
            stat("Average teacher salary (FY18 to FY26)", A["t_avg"], C["t_avg"], _d(A["t_avg"]), _d(C["t_avg"]), A["t_avg"], C["t_avg"], note="NH %s → %s" % (_d(A["t_avg_state"]), _d(C["t_avg_state"]))),
            stat("Starting teacher salary (FY18 to FY26)", A["t_start"], C["t_start"], _d(A["t_start"]), _d(C["t_start"]), A["t_start"], C["t_start"], note="NH %s → %s" % (_d(A["t_start_state"]), _d(C["t_start_state"]))),
            stat("Students per teacher (FY18 to FY26)", A["ratio"], C["ratio"], "%.1f" % A["ratio"], "%.1f" % C["ratio"], A["ratio"], C["ratio"], pct=False, note="NH %.1f → %.1f" % (A["ratio_state"], C["ratio_state"])),
            ],
        "limits": "Averages hide the mix of experience and degrees, and the DOE's average-salary file has a gap for 2022-23 and repeats one year, so the page shows FY 2025-26 from the DOE's latest staffing report.",
        "links": [["Teacher, aide and other instructional pay", "pers"], ["Instruction salaries and benefits", "staff"], ["Benefits as a share of salaries", "ben"], ["Average teacher salary vs. NH", "tavg"], ["Starting salary vs. NH", "tstart"]]})

    ds_a, ds_b = A["fn_bint"] + prin_a, B["fn_bint"] + prin_b
    in_ = by["interest"]
    cards.append({
        "id": "debt", "title": "“Debt and the new buildings are the problem.”", "name": "Bonds and buildings",
        "shows": "Bond principal still owed rose from %s to %s after borrowing in FY 2019-20 to FY 2021-22. Interest and principal paid rose from %s to %s, which is %s of the increase in operating spending plus principal. The state building aid that offset part of the cost ended after FY 2022-23. Payments due next year are %s, %s of operating spending." % (
            _m(A["bond_prin"], 1), _m(B["bond_prin"], 1), _m(ds_a), _m(ds_b), _p(100 * (ds_b - ds_a) / ((rec_b + prin_b) - (rec_a + prin_a))), _m(B["ds_tot"]), _p(100 * B["ds_tot"] / rec_b)),
        "stats": [
            stat("Bond principal still owed at year end", A["bond_prin"], B["bond_prin"], _m(A["bond_prin"], 1), _m(B["bond_prin"], 1), A["bond_prin"], B["bond_prin"]),
            stat("Bond interest paid", A["fn_bint"], B["fn_bint"], _m(A["fn_bint"]), _m(B["fn_bint"]), A["fn_bint"], B["fn_bint"]),
            stat("Interest plus principal paid", ds_a, ds_b, _m(ds_a), _m(ds_b), ds_a, ds_b),
            stat("Bond payments due in the following year", A["ds_tot"], B["ds_tot"], _m(A["ds_tot"]), _m(B["ds_tot"]), A["ds_tot"], B["ds_tot"]),
            stat("State building aid for school bonds", A["bld_aid"], B["bld_aid"], _d(A["bld_aid"]) + " a year", _d(B["bld_aid"]), A["bld_aid"], B["bld_aid"], pct=False, note="through FY 2022-23"),
            ],
        "limits": "Whether the projects were needed is outside this page; it measures what they cost.",
        "links": [["School bonds still owed", "bonds"], ["Bond payments due next year", "dsvc"], ["Money borrowed and drawn from reserves", "fin"], ["State building aid", "bldaid"], ["Long-term debt and pension obligations", "debt"]]})

    cards.append({
        "id": "enrollment", "title": "“Fewer students, so each one costs more.”", "name": "Falling enrollment",
        "shows": "Operating spending rose %s while enrollment fell %s, so cost per pupil rose %s, about %s after inflation. Among NH K-12 districts ORCSD's cost per pupil moved from #%d highest of %d to #%d of %d." % (
            _p(chg(rec_a, rec_b), 0, True), _p(abs(chg(A["enrollment"], B["enrollment"])), 0), _p(chg(A["nhed_cpp"], B["nhed_cpp"]), 0, True), _p(real(A["nhed_cpp"], B["nhed_cpp"]), 0, True), A["cpp_rank"], A["cpp_rank_n"], B["cpp_rank"], B["cpp_rank_n"]),
        "stats": [
            stat("Students enrolled", A["enrollment"], B["enrollment"], "{:,}".format(A["enrollment"]), "{:,}".format(B["enrollment"]), A["enrollment"], B["enrollment"], note="{:,} in FY 2026-27 ({})".format(E["enrollment"], _p(chg(A["enrollment"], E["enrollment"]), 1, True))),
            stat("Cost per pupil (NH DOE)", A["nhed_cpp"], B["nhed_cpp"], _d(A["nhed_cpp"]), _d(B["nhed_cpp"]), A["nhed_cpp"], B["nhed_cpp"], real_too=True),
            stat("Rank in cost per pupil among NH K-12 districts (1 = highest)", A["cpp_rank"], B["cpp_rank"], "#%d of %d" % (A["cpp_rank"], A["cpp_rank_n"]), "#%d of %d" % (B["cpp_rank"], B["cpp_rank_n"]), A["cpp_rank"], B["cpp_rank"], pct=False),
            ],
        "limits": "Many costs, such as buildings, buses and administration, do not fall when a few students leave. The page cannot say which costs could have been cut.",
        "links": [["Students enrolled", "students"], ["Cost per pupil", "cpp"], ["Cost per pupil vs. NH average and rank", "cmp"], ["Enrollment projections vs. actual", "proj"]]})

    sh = lambda r, k: 100 * r[k] / r["levy_tot"]
    gr = lambda k: chg(A[k], B[k])
    cards.append({
        "id": "towns", "title": "“Our town is paying more than its share.”", "name": "Durham, Lee and Madbury",
        "shows": "Lee's share of the school levy rose from %s to %s while Durham's fell from %s to %s. Durham's property values grew fastest (%s against %s for Lee), and its school tax rate fell %s; Lee's fell %s. Lee's school tax rate per $1,000 of full value ranks #%d highest of %d NH towns, up from #%d of %d." % (
            _p(sh(A, "levy_lee")), _p(sh(B, "levy_lee")), _p(sh(A, "levy_dur")), _p(sh(B, "levy_dur")), _p(gr("eq_dur"), 0, True), _p(gr("eq_lee"), 0, True),
            _p(abs(chg(A["tax_dur"], B["tax_dur"])), 0), _p(abs(chg(A["tax_lee"], B["tax_lee"])), 0), B["rks_rank_lee"], B["rks_n"], A["rks_rank_lee"], A["rks_n"]),
        "stats": [
            stat("Share of the school levy: Durham", sh(A, "levy_dur"), sh(B, "levy_dur"), _p(sh(A, "levy_dur")), _p(sh(B, "levy_dur")), sh(A, "levy_dur"), sh(B, "levy_dur"), pct=False),
            stat("Share of the school levy: Lee", sh(A, "levy_lee"), sh(B, "levy_lee"), _p(sh(A, "levy_lee")), _p(sh(B, "levy_lee")), sh(A, "levy_lee"), sh(B, "levy_lee"), pct=False),
            stat("Share of the school levy: Madbury", sh(A, "levy_mad"), sh(B, "levy_mad"), _p(sh(A, "levy_mad")), _p(sh(B, "levy_mad")), sh(A, "levy_mad"), sh(B, "levy_mad"), pct=False),
            stat("School tax rate per $1,000 (Durham, Lee, Madbury)", A["tax_lee"], B["tax_lee"], "$%.2f / $%.2f / $%.2f" % (A["tax_dur"], A["tax_lee"], A["tax_mad"]), "$%.2f / $%.2f / $%.2f" % (B["tax_dur"], B["tax_lee"], B["tax_mad"]), A["tax_lee"], B["tax_lee"], pct=False, note="tax years 2017 and 2024"),
            stat("Property value (equalized) growth, FY18 to FY25", 0, 0, "", "", text="Durham %s · Lee %s · Madbury %s" % (_p(gr("eq_dur"), 0, True), _p(gr("eq_lee"), 0, True), _p(gr("eq_mad"), 0, True))),
            ],
        "limits": "The split follows a formula set in the cooperative agreement: half by each town's student count and half by its property value, using values from a few years earlier. Whether that split is fair is a question for the voters of the three towns.",
        "links": [["Each town's share of the school levy", "share"], ["School tax per $1,000 of property value", "eff"], ["Local school tax rate by town", "rate"], ["Share of the budget the formula assigns", "app"], ["Rank among NH towns", "rks"]]})
    for c in cards:
        c["shows"] = _prose(c["shows"])
        c["limits"] = _prose(c["limits"])
    for b in out["baseline"]:
        if "note" in b and b["id"] != "spend":
            b["note"] = _prose(b["note"])
    out["cards"] = cards
    return out
