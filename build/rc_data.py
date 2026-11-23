# Report-card, audit and EFA data, keyed by FY end year (2018 = school year 2017-18).
# Sources: ORCSD annual reports (2023, 2024, 2026 editions, Section II "Annual Report Card" and NESDEC pages),
# ORCSD audited financial statements (June 30 year-end), NH DOE Education Freedom Account by-municipality reports.
Y = range(2018, 2028)

def per(vals, start=2018):
    return {start + i: v for i, v in enumerate(vals)}

RC = {}
def put(name, d):
    RC[name] = d

# October 1 enrollment by level (K and grades 1-4 combined as "K-4"); NH DOE history printed in the ORCSD 2026 report
K  = per([119, 92, 120, 101, 128, 127, 119, 139, 130])
EL = per([576, 589, 551, 513, 486, 497, 510, 518, 553])
put("en_k4", {**{y: K[y] + EL[y] for y in K}, 2027: 675})  # FY27: ORCSD Oct 7, 2026 board packet (district count)
put("en_ms", per([659, 667, 665, 658, 629, 643, 618, 585, 560, 563]))
put("en_hs", per([793, 809, 832, 835, 858, 843, 838, 825, 795, 788]))

# General fund balances at June 30 (audited statements); FY2025 audit not yet posted
put("fb_tot", {2018: 1864974, 2019: 1718793, 2020: 2746428, 2021: 3816193, 2022: 3706994, 2023: 3343147, 2024: 3629203})
put("fb_un",  {2018: 188357,  2019: 127243,  2020: 414071,  2021: 828933,  2022: 1130890, 2023: 754798,  2024: 318833})
put("fb_com", {2018: 1493229, 2019: 1557413, 2020: 2322307, 2021: 2575093, 2022: 2343483, 2023: 2543657, 2024: 3279007})

# Average class size, DOE data printed in the ORCSD reports (district school / NH average by grade band); 2017-18 to 2025-26 (2025-26 from the iPlatform Average Class Size By School report, as of Oct 1, 2025)
put("cs_mw12", per([21.1, 20.8, 20.0, 16.3, 17.6, 17.9, 17.5, 18.0, 18.0]))
put("cs_mo12", per([21.2, 20.8, 18.5, 17.3, 17.6, 20.8, 17.6, 19.2, 17.9]))
put("cs_mw34", per([19.1, 21.1, 21.1, 17.7, 19.8, 18.6, 21.2, 19.1, 18.8]))
put("cs_mo34", per([20.9, 21.1, 18.7, 19.4, 19.8, 19.5, 20.0, 17.9, 19.1]))
put("cs_st12", per([16.1, 17.4, 17.2, 16.2, 16.2, 16.5, 16.4, 15.9, 15.2]))
put("cs_st34", per([17.5, 18.8, 18.7, 17.2, 17.5, 17.6, 17.9, 17.1, 16.6]))

# SAT, Oyster River High School vs NH (spring of the school year); national averages printed in the report are not used
put("sat_rw",    per([573, 580, 577, 577, 557, 559, 563, 566]))
put("sat_m",     per([578, 564, 567, 566, 561, 560, 541, 545]))
put("sat_rw_nh", per([535, 508, 528, 531, 512, 506, 526, 510]))
put("sat_m_nh",  per([528, 516, 512, 514, 494, 488, 508, 491]))

# What graduates do next (High School Completers table), 2017-18 to 2023-24; district / NH, percent
# Graduation and state-test participation: NH DOE iExplore / iAchieve (Tableau dashboards), school years labeled by the DOE (2026 = 2025-26)
put("grad4", per([94.74, 97.25, 97.06, 96.12, 96.79, 93.85, 97.06, 98.19, 99.48]))
put("grad5", per([97.21, 96.30, 97.80, 97.06, 96.12, 97.24, 94.90, 97.06, 99.10]))
put("psenr", per([70.33, 68.68, 71.21, 74.37, 69.67, 73.26, 68.29, 74.77, None]))
put("pt_ela", per([98, 98, None, 89, 96, 96, 96, 96, 95]))
put("pt_mat", per([98, 98, None, 89, 96, 97, 96, 96, 95]))
put("pt_sci", per([94, 90, None, 72, 95, 95, 95, 91, 89]))
# Staffing and student-profile indicators: NH DOE iExplore (Tableau), Oyster River Coop (District) and State of New Hampshire; DOE year labels (2026 = 2025-26)
# Share of students suspended (NH DOE iReport, ESSA profile, All Students, school year label as the DOE shows it)
put("iss_rate", per([1.43, 1.18, 0.85, 0.19, 1.56, 2.27, 2.82, 2.41, 1.79]))
put("oss_rate", per([0.95, 0.89, 0.19, 0.05, 1.12, 0.87, 0.63, 0.59, 0.65]))
put("cslr", per([None, None, None, 210.70, 210.10, 194.55, 191.91, 174.75, 158.77]))
put("cslr_nh", per([None, None, None, 246.38, 227.35, 219.56, 210.24, 202.44, 200.37]))
put("cert", per([94.38, 93.67, 94.48, 95.86, 88.68, 88.61, 85.88, 91.67, 92.66]))
put("cert_nh", per([89.96, 90.06, 89.50, 89.92, 90.13, 88.77, 87.78, 86.55, 86.22]))
put("swd", per([15.84, 15.84, 15.21, 15.34, 16.85, 18.08, 17.43, 17.36, 17.49]))
put("swd_nh", per([16.42, 16.92, 16.80, 18.17, 18.60, 18.94, 19.82, 20.27, 20.41]))
put("col4",     per([68.5, 72.6, 70.7, 69.2, 66.7, 65.8, 73.3, 70.2]))
put("col4_nh",  per([52.3, 50.8, 51.8, 49.4, 49.6, 50.8, 49.8, 49.9]))
put("coll",     per([19.0, 13.6, 10.1, 14.4, 14.6, 13.4, 13.6, 13.8]))
put("coll_nh",  per([20.2, 20.2, 16.4, 16.0, 15.6, 16.8, 17.0, 17.0]))
put("colw",     per([10.9, 11.4, 12.6, 12.4, 16.4, 14.4, 10.7, 13.3]))
put("colw_nh",  per([17.8, 17.9, 18.3, 20.9, 24.2, 22.2, 23.7, 23.0]))
put("colm",     per([1.6, 2.1, 1.5, 2.0, 1.4, 0.5, 1.0, 0.9]))
put("colm_nh",  per([3.3, 2.9, 2.7, 2.3, 1.8, 1.9, 1.9, 2.4]))

# Special education counts as of October 1 of the school year (district sped dept); 2017-18 to 2025-26
put("sp_el",  per([86, 96, 115, 71, 65, 67, 84, 81, 83]))
put("sp_ms",  per([105, 100, 107, 108, 109, 125, 102, 93, 95]))
put("sp_hs",  per([120, 85, 90, 90, 106, 110, 115, 120, 116]))
put("sp_o35", per([17, 24, 0, 17, 21, 20, 18, 15, 10]))
put("sp_o621", per([5, 3, 4, 5, 8, 8, 11, 8, 7]))
put("sp_tot", per([333, 308, 316, 291, 309, 330, 330, 317, 311]))

# Free and reduced lunch eligibility (NH DOE, October 1 count) and English learners (district / NH counts)
put("frl", per([129, 138, 112, 158, 117, 170, 196, 162, 145]))
put("ell", per([44, 47, 47, 43, 32, 34, 33, 36, 40]))
put("ell_nh", per([4961, 4640, 4626, 5436, 4787, 5154, 5286, 5741, 6023]))

# Education Freedom Account students living in Durham, Lee and Madbury (NH DOE by-municipality reports; weighted counts)
put("efa_dur", {2022: 2.0, 2023: 3.0, 2024: 11.2, 2025: 14.0, 2026: 48.0})
put("efa_lee", {2022: 5.2, 2023: 5.8, 2024: 13.8, 2025: 13.0, 2026: 29.0})
put("efa_mad", {2022: 0.0, 2023: 0.0, 2024: 2.4, 2025: 5.0, 2026: 14.0})
put("efa_aid", {2022: 37253.05, 2023: 39817.41, 2024: 136610.0, 2025: 165648.0, 2026: 451013.40})

# Dropouts (district count, NH count), 2017-18 to 2024-25
put("drop",    per([1, 1, 0, 1, 1, 4, 0, 0], 2018))
put("drop_nh", per([593, 572, 523, 734, 808, 709, 581, 532], 2018))

# Tri-City Career Technology Center, ORHS students, 2017-18 to 2024-25
put("ctc", per([33, 36, 53, 57, 69, 72, 77, 101], 2018))

# Teacher education (share of professional staff), 2017-18 to 2024-25 except 2019-20 (not printed)
put("td_b",    {2018: 26.0, 2019: 25.5, 2020: 23.7, 2021: 22.7, 2022: 19.0, 2023: 16.9, 2024: 19.7, 2025: 23.6, 2026: 22.9})
put("td_m",    {2018: 74.0, 2019: 66.7, 2020: 67.7, 2021: 67.8, 2022: 79.8, 2023: 82.5, 2024: 70.0, 2025: 67.4, 2026: 65.7})
put("td_x",    {2018: 0.0,  2019: 7.8,  2020: 8.6,  2021: 9.5,  2022: 1.1,  2023: 0.6,  2024: 10.3, 2025: 9.0,  2026: 11.4})
put("td_b_nh", {2018: 38.9, 2019: 38.1, 2020: 37.0, 2021: 35.9, 2022: 35.4, 2023: 35.4, 2024: 34.9, 2025: 34.7, 2026: 34.8})
put("td_m_nh", {2018: 58.9, 2019: 59.6, 2020: 60.4, 2021: 61.2, 2022: 61.5, 2023: 62.0, 2024: 62.1, 2025: 61.8, 2026: 61.5})
put("td_x_nh", {2018: 1.8,  2019: 1.9,  2020: 2.3,  2021: 2.2,  2022: 2.4,  2023: 2.3,  2024: 2.7,  2025: 3.1,  2026: 3.2})

# Staff with 14+ years of experience, count by school (school district office), 2017-18 to 2024-25 (2017-18 to 2020-21 from the 2020 and 2022 reports)
put("tx_mw", per([19, 24, 26, 25, 23, 20, 18, 18], 2018))
put("tx_mo", per([30, 30, 30, 30, 21, 26, 22, 23], 2018))
put("tx_ms", per([42, 42, 42, 44, 38, 41, 41, 38], 2018))
put("tx_hs", per([42, 45, 54, 55, 50, 47, 45, 44], 2018))

# Attendance by school level, district / NH (percent); the ORCSD report prints 2022-23 and 2023-24 identically and 2024-25 looks re-based
AT = {  # key: (K, Elem, MS, HS) district then NH
    2018: ((96.2, 96.3, 96.3, 95.0), (94.2, 95.3, 94.7, 93.2)),
    2019: ((95.6, 96.0, 96.2, 95.7), (94.2, 95.1, 94.3, 92.9)),
    2020: ((97.7, 97.5, 97.2, 97.1), (95.4, 96.1, 94.9, 94.0)),
    2021: ((98.1, 98.1, 97.8, 94.9), (93.3, 94.5, 93.0, 91.3)),
    2022: ((92.7, 92.7, 93.3, 91.9), (90.7, 91.9, 91.1, 89.3)),
    2023: ((93.3, 93.3, 95.2, 92.6), (92.3, 93.3, 92.8, 90.8)),
    # 2025-26: NH DOE iPlatform Attendance Rate by School (run 2026-11-22). Kindergarten and elementary are the simple average of Mast Way (95.6, 95.7) and Moharimet (93.0, 95.1)
    2026: ((94.3, 95.4, 95.7, 92.7), (94.5, 95.0, 94.0, 92.2)),
}
AT_REPEAT = {2024: ((93.3, 93.3, 95.2, 92.6), (92.3, 93.3, 92.8, 90.8)),
             2025: ((98.2, 98.3, 97.5, 97.9), (97.6, 97.7, 97.5, 97.0))}
for i, nm in enumerate(("k", "e", "m", "h")):
    put("at_" + nm, {y: v[0][i] for y, v in AT.items()})
    put("at_" + nm + "_nh", {y: v[1][i] for y, v in AT.items()})
    put("atx_" + nm, {y: v[0][i] for y, v in AT_REPEAT.items()})

# Enrollment projections (K-12). Each year shows the latest projection printed before that school year began.
# District Long Range Planning Committee (LRPC): 2018 report -> 2018-19; 2019 report -> 2019-20; 2020 report -> 2020-21;
# 2021 report -> 2021-22; 2022 report -> 2022-23; 2023 report -> 2023-24 and later (the 2024 report repeats the 2023 tables).
# NESDEC: 2021 report -> 2021-22; 2022 report -> 2022-23; 2023 report -> 2023-24 and later. No NESDEC tables in 2018 to 2020, and none in 2025 or 2026.
put("pr_nes",  {2022: 2128, 2023: 2062, 2024: 2118, 2025: 2139, 2026: 2149, 2027: 2170})
put("pr_lrpc", {2019: 2153, 2020: 2175, 2021: 2136, 2022: 2115, 2023: 2076, 2024: 2047, 2025: 2015, 2026: 1988, 2027: 1978})

# FY2025 unassigned general fund balance at June 30, 2025 per the June 2025 monthly financial report (preliminary, unaudited; FY2025 audit not posted)
put("fb_un_pre", {2025: 63580})

# ---- Added Nov 22, 2026: NH DOE other state aid programs and School Safety Data Collection (all keyed by FY end year) ----
# Building aid distribution FY10-FY26 and FY27-FY41 (revised June 30, 2026): Oyster River $523,742 a year 2012-13 to 2022-23, $0 from 2023-24.
put("bld_aid", {**{y: 523742 for y in range(2018, 2024)}, **{y: 0 for y in range(2024, 2028)}})
# Special education aid (catastrophic aid files for FY18-FY19, special education aid files FY20-FY26): entitlement, prorated amount paid, district cost of eligible students.
put("sp_ent",  per([156156.02, 97745.61, 132495.13, 64621.45, 94722.74, 303788.10, 266626.35, 193622.58, 228296.35]))
put("sp_paid", {2018: 113058.01, 2019: 68637.78, 2020: 125171.88, 2023: 298551.79, 2024: 232066.75, 2025: 133198.08, 2026: 208073.36})
put("sp_cost", per([625043.46, 454063.48, 449604.54, 199212.75, 296057.34, 757434.00, 866237.19, 520819.47, 428753.60]))
# Career technology tuition and transportation aid (by school year; Oyster River tuition payment is $0 in every file)
put("cte_tt", per([3754.20, 4255.40, 4636.70, 1965.60, 8024.10, 7887.60, 12800.60, 14043.90]))
# EFA phase-out grant to the district (FY2023, FY2025, FY2026 files; FY2024 file unreadable)
put("efa_po", {2023: 6626.65, 2025: 10067.00, 2026: 9616.56})
# EFA by municipality as of Oct 2, 2026 (FY27): base-aid students Durham 52, Lee 30, Madbury 20; total calculated cost $533,277
_efa = {"efa_dur": 52.0, "efa_lee": 30.0, "efa_mad": 20.0, "efa_aid": 533277.0}
for _k, _v in _efa.items():
    RC[_k][2027] = _v
# School Safety Data Collection (NH DOE), district totals over Mast Way, Moharimet, Middle, High (and preschool where listed)
put("truant", per([58, 93, 163, 165, 101, 47, 29, 105]))
put("iss",     per([43, 23, 22, 3, 25, 40, 59, 55]))
put("oss",     per([19, 23, 5, 1, 14, 14, 18, 14]))
put("expel",   per([0, 0, 0, 0, 0, 0, 0, 0]))
put("bul_rep", per([11, 1, 3, 2, 9, 9, 13, 11]))
put("bul_cyb", per([2, 0, 1, 0, 1, 2, 2, 2]))
put("bul_act", per([4, 1, 1, 0, 2, 6, 4, 7]))
put("bul_acy", per([2, 0, 0, 0, 0, 2, 1, 1]))
put("vio_inj", per([0, 5, 0, 0, 0, 1, 1, 0]))
put("vio_non", per([6, 0, 2, 0, 4, 6, 3, 19]))
put("weap",    per([2, 2, 1, 0, 0, 2, 0, 0]))
put("drug",    per([34, 8, 2, 0, 6, 2, 1, 2]))
put("alc",     per([0, 0, 0, 1, 0, 0, 1, 1]))
put("vio_oth", per([1, 0, 0, 0, 1, 1, 0, 0]))
put("restr",   per([0, 0, 0, 0, 0, 34, 0, 3]))
put("seclu",   per([0, 0, 0, 0, 0, 0, 13, 23]))

put("vote_y", per([1516, 789, 1047, 2720, 1584, 2205, 894, 1208, 1164, 1897]))
put("vote_n", per([263, 282, 504, 462, 435, 689, 303, 415, 551, 1110]))

FIELDS = sorted(RC)
def fields_for(y):
    return {k: RC[k].get(y) for k in FIELDS}
