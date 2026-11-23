# How Durham, Lee and Madbury share the Oyster River school bill (keyed by FY end year; 2018 = 2017-18).
# Formula (NH DOE "Apportionment formulas for regional and cooperative school districts", July 1 2024):
#   Oyster River: total operating budget 50% on ADM, 50% on equalized valuation; adequacy aid credited to the pre-existing districts (towns).
# ADM-R and equalized valuation (with utilities) per town: NH DOE "Equalized valuation per pupil" files (equal_pupil / eqprt).
# The apportionment uses the latest such file available when the budget is set; FY -> file year below.
FILE_YEAR = {2018: 2016, 2019: 2017, 2020: 2018, 2021: 2019, 2022: 2020, 2023: 2021, 2024: 2021, 2025: 2022, 2026: 2023, 2027: 2024}
FILES = {  # file year: ((Durham, Lee, Madbury) equalized valuation incl. utilities, (Durham, Lee, Madbury) ADM in residence)
 2016: ((1033119311, 467333437, 225773770), (920.06, 648.92, 359.47)),
 2017: ((1080145993, 473960648, 239636957), (964.22, 689.74, 377.68)),
 2018: ((1144424005, 530857155, 254256479), (963.33, 705.58, 362.07)),
 2019: ((1224495847, 560387773, 275891455), (944.84, 709.18, 367.45)),
 2020: ((1312883720, 603422994, 294845323), (936.09, 722.91, 371.17)),
 2021: ((1799956129, 765244402, 383968500), (932.81, 688.37, 332.78)),
 2022: ((1843008917, 926583074, 450086126), (915.25, 720.04, 333.99)),
 2023: ((2057334965, 1037459517, 464778711), (897.52, 712.64, 324.56)),
 2024: ((2489181140, 1028205671, 486516161), (871.56, 711.17, 336.11)),
}
# Official apportionment percentages printed in the ORCSD annual reports (the "Present Budget Year" column), Durham, Lee, Madbury
APP_OFFICIAL = {
 2018: (53.7791, 30.3612, 15.8597), 2019: (53.8495, 30.1769, 15.9736), 2020: (53.3713, 31.1265, 15.5022),
 2021: (53.0797, 31.1378, 15.7826), 2022: (52.7423, 31.4492, 15.8086), 2023: (54.0882, 30.7527, 15.1591),
 2024: (54.3861, 30.5890, 15.0250),
 # FY2025 and FY2026: NH DOE Bureau of School Finance cooperative apportionment sheets published by the Department of Revenue Administration (combined % for current expenses)
 2025: (51.8592, 32.6712, 15.4696), 2026: (52.09371, 32.98994, 14.91635),
}
# State credits applied to each town's share = adequacy grant + SWEPT retained (Durham, Lee, Madbury).
# FY2018-2023: figures printed in the ORCSD annual reports' apportionment table; FY2024-2027: NH DOE adequate education aid municipal summaries.
CREDITS = {
 2018: (3684580, 3422583, 1621667), 2019: (3724930, 3454640, 1558624), 2020: (3824275, 3669942, 1657319),
 2021: (3818752, 4102698, 1935542), 2022: (3902397, 3772709, 1732476), 2023: (3895674, 3644089, 1580360),
 2024: (4143830.67, 3935723.95, 1648535.60), 2025: (4164537, 3964668, 1645118), 2026: (4106562, 3888671, 1717159),  # FY2025-26: final state aid per the DOE cooperative apportionment sheets
 2027: (4078953.07, 4208915.72, 1723365.35),
}
# State education property tax rate per $1,000 by tax year (FY-1): printed in the ORCSD annual reports' tax rate impact tables (current-year column)
STATE_RATE = {
 2018: (2.34, 2.39, 2.23), 2019: (2.01, 2.29, 2.23), 2020: (2.01, 2.39, 2.17), 2021: (2.00, 2.32, 1.84),
 2022: (1.98, 1.52, 1.84), 2023: (1.53, 1.11, 1.27), 2024: (1.39, 1.50, 1.79), 2025: (1.21, 1.53, 1.77), 2026: (1.06, 1.57, 0.99),
}
def town_fields(y, r):
    f = {}
    fy_ = FILE_YEAR[y]; fv, adm = FILES[fy_]
    for i, k in enumerate(("dur", "lee", "mad")):
        f["fv_" + k] = fv[i]; f["adm_" + k] = adm[i]
        f["cr_" + k] = CREDITS[y][i]
        sr = STATE_RATE.get(y); f["ssr_" + k] = sr[i] if sr else None
    f["adm_file"] = fy_
    if y in APP_OFFICIAL:
        app = APP_OFFICIAL[y]; basis = "official"
    elif r.get("levy_dur") is not None:  # gross share = (net levy + state credits) / total; reproduces the official figure for FY2024 to 0.001 point
        g = [r["levy_" + k] + CREDITS[y][i] for i, k in enumerate(("dur", "lee", "mad"))]
        s = sum(g); app = tuple(round(x / s * 100, 4) for x in g); basis = "derived"
    else:  # FY2027: 50% value share + 50% ADM share from the latest DOE file; no levy split published yet
        sv = sum(fv); sa = sum(adm)
        app = tuple(round(((fv[i] / sv) + (adm[i] / sa)) / 2 * 100, 4) for i in range(3)); basis = "estimate"
    for i, k in enumerate(("dur", "lee", "mad")):
        f["app_" + k] = app[i]
    f["app_basis"] = basis
    return f
