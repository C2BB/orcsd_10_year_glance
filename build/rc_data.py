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
put("en_hs", per([793, 809, 832, 835, 858, 843, 838, 825, 796, 788]))

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
# NH: the College Board's New Hampshire SAT annual reports (hosted by the NH DOE), Total row = all NH graduates of that class who took the SAT. The district's own reports print different
# NH figures (508/516, 528/512, 531/514, 512/494, 506/488, 526/508, 510/491 for 2019-2025); they are in CONFLICTS.md, the state's are used here (state-first rule).
put("sat_rw_nh", per([535, 533, 531, 540, 530, 526, 520, 523]))
put("sat_m_nh",  per([528, 526, 524, 526, 521, 508, 503, 495]))

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
put("truant", per([58, 93, 163, 165, 101, 47, 29, 105]))  # Oyster River schools (SAU 5, district 423); reproduced by build/nh_truancy.py
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
put("restr",   per([0, 0, 0, 0, 0, 34, 0, 3, 1]))  # FY26: NH DOE corrected restraint and seclusion report SY2025-26 (Nov 17, 2026): Mast Way 1
put("seclu",   per([0, 0, 0, 0, 0, 0, 13, 23, 1]))  # FY26: Mast Way 1 seclusion; FY18-22, FY23 (34) and FY25 also match the DOE annual report PDFs in raw/nh-doe

put("vote_y", per([1516, 789, 1047, 2720, 1584, 2205, 894, 1208, 1164, 1897]))
put("vote_n", per([263, 282, 504, 462, 435, 689, 303, 415, 551, 1110]))


# ---- Added Nov 22, 2026 (second data sweep) ----
# Town enrollment: NH DOE iPlatform "Town Level Enrollment By Grade" (ReportID 12), public-school students living in each town, Oct 1 count; FY27 = preliminary Oct 1, 2026 run.
put('en_dur', per([958, 952, 947, 918, 929, 923, 905, 875, 846, 839]))
put('en_dur_k4', per([324, 318, 314, 291, 284, 281, 277, 280, 289, 281]))
put('en_dur_ms', per([320, 314, 305, 300, 300, 308, 311, 289, 261, 264]))
put('en_dur_hs', per([314, 311, 313, 314, 333, 318, 301, 294, 286, 282]))
put('en_dur_ps', per([0, 9, 15, 13, 12, 16, 16, 12, 10, 12]))
put('en_lee', per([704, 706, 718, 687, 698, 728, 716, 715, 729, 711]))
put('en_lee_k4', per([251, 245, 251, 228, 238, 244, 249, 264, 279, 265]))
put('en_lee_ms', per([217, 224, 218, 224, 221, 233, 228, 215, 216, 217]))
put('en_lee_hs', per([236, 230, 238, 226, 224, 238, 230, 225, 224, 218]))
put('en_lee_ps', per([0, 7, 11, 9, 15, 13, 9, 11, 10, 11]))
put('en_mad', per([359, 373, 374, 358, 337, 333, 322, 341, 320, 329]))
put('en_mad_k4', per([127, 122, 107, 98, 96, 101, 106, 114, 114, 130]))
put('en_mad_ms', per([127, 136, 146, 140, 114, 106, 84, 85, 85, 83]))
put('en_mad_hs', per([105, 105, 113, 116, 124, 123, 130, 135, 115, 112]))
put('en_mad_ps', per([0, 10, 8, 4, 3, 3, 2, 7, 6, 4]))
# School-level and district indicators: NH DOE iExplore (Compare dashboard, *Download Compare), DOE years 2018-2026 (2016-2017 not used); COVID-year gaps are None.
put('sc_hs_ela', per([79, 85, None, 88, 79, 79, 80, 86, 82]))
put('sc_hs_mat', per([67, 75, None, 66, 63, 61, 53, 55, 51]))
put('sc_hs_cert', per([86.89, 88.52, 89.23, 89.06, 73.68, 78.69, 79.71, 83.33, 85.51]))
put('sc_hs_exp', per([92.86, 91.67, 90.28, 92.96, 82.67, 86.84, 83.33, 84.42, 90.28]))
put('sc_hs_cslr', per([None, None, None, 167.0, 171.6, 168.6, 167.6, 165.0, 113.71]))
put('sc_hs_swd', per([15.26, 13.35, 13.22, 12.93, 15.5, 16.49, 16.95, 17.94, 19.1]))
put('sc_hs_enr', per([793, 809, 832, 835, 858, 843, 838, 825, 796]))
put('sc_hs_nts', per([None, None, None, 20.72, 20.67, 17.71, 20.74, 17.55, 20.95]))
put('sc_ms_ela', per([76, 72, None, 67, 69, 76, 73, 73, 71]))
put('sc_ms_mat', per([72, 72, None, 51, 65, 68, 68, 65, 69]))
put('sc_ms_gela', per([49, 48, None, None, 53, 55, 54, 50, 51]))
put('sc_ms_gmat', per([55, 56, None, None, 61, 62, 57, 55, 59]))
put('sc_ms_cert', per([98.08, 93.62, 96.23, 100, 94.44, 94.23, 87.04, 96.72, 98.18]))
put('sc_ms_exp', per([90.63, 84.85, 89.39, 93.85, 93.65, 95.45, 93.65, 88.89, 91.23]))
put('sc_ms_cslr', per([None, None, None, 219.33, 209.67, 160.75, 154.5, 117.0, 140.0]))
put('sc_ms_swd', per([16.69, 15.74, 16.99, 18.39, 21.14, 21.31, 18.12, 17.26, 18.57]))
put('sc_ms_enr', per([659, 667, 665, 658, 629, 643, 618, 585, 560]))
put('sc_ms_nts', per([None, None, None, 21.02, 20.62, 19.37, 15.89, 13.83, 19.05]))
put('sc_mw_ela', per([76, 67, None, 83, 70, 73, 70, 75, 82]))
put('sc_mw_mat', per([84, 78, None, 75, 69, 73, 74, 74, 75]))
put('sc_mw_gela', per([60, 56, None, None, 53, 63, 53, 65, 66]))
put('sc_mw_gmat', per([66, 70, None, None, 58, 60, 55, 64, 70]))
put('sc_mw_cert', per([100, 100, 100, 100, 100, 100, 100, 100, 100]))
put('sc_mw_exp', per([88.46, 92.86, 96.67, 93.33, 90.32, 96.67, 93.1, 80.65, 81.48]))
put('sc_mw_cslr', per([None, None, None, 326.0, 323.0, 327.0, 331.0, 348.0, 368.0]))
put('sc_mw_swd', per([11.36, 11.51, 10.46, 10.12, 10.22, 13.76, 12.99, 12.64, 11.96]))
put('sc_mw_enr', per([352, 365, 373, 326, 323, 327, 331, 348, 368]))
put('sc_mw_nts', per([None, None, None, 12.54, 15.24, 15.5, 12.78, 12.7, 19.37]))
put('sc_mo_ela', per([76, 75, None, 81, 73, 72, 74, 74, 83]))
put('sc_mo_mat', per([72, 77, None, 71, 76, 74, 68, 74, 84]))
put('sc_mo_gela', per([42, 56, None, None, 48, 52, 47, 43, 54]))
put('sc_mo_gmat', per([37, 64, None, None, 56, 45, 47, 48, 59]))
put('sc_mo_cert', per([100, 100, 100, 100, 100, 95.45, 95.83, 100, 100]))
put('sc_mo_exp', per([100, 100, 100, 96.55, 96.55, 100, 96.3, 96.55, 96.0]))
put('sc_mo_cslr', per([None, None, None, 288.0, 291.0, 297.0, 298.0, 309.0, 315.0]))
put('sc_mo_swd', per([20.12, 21.84, 16.78, 17.01, 14.09, 15.82, 18.12, 17.48, 16.19]))
put('sc_mo_enr', per([343, 316, 298, 288, 291, 297, 298, 309, 315]))
put('sc_mo_nts', per([None, None, None, 10.47, 12.33, 11.34, 10.24, 10.55, 16.15]))
put('exp_doe', per([92.59, 90.77, 92.42, 93.85, 89.5, 92.54, 89.45, 86.7, 89.73]))
put('exp_doe_nh', per([85.79, 85.74, 85.06, 84.95, 84.55, 83.78, 83.54, 83.68, 83.36]))
put('nts', per([None, None, None, 16.84, 17.99, 16.71, 15.49, 14.36, 18.95]))
put('nts_nh', per([None, None, None, 22.18, 23.45, 24.8, 22.78, 21.81, 21.05]))
# Central-office pay: NH DOE 'Salaries of superintendents, assistant superintendents and business administrators' files (FY18-FY26; FY26 is the DOE's preliminary file).
# Reproduced by build/admin_pay.py (reads raw/nh-doe/*salaries*, *admin-sal*). Oyster River = SAU #5. NH median = median of SAUs (ID < 200) that listed a figure that year; n = how many.
put('co_sup', per([163017, 167908, 172945, 178133, 178133, 192651, 200357, 210000, 210000]))
put('co_sup_med', per([123600, 127154, 132000, 132700, 134239, 139467, 145249, 148500, 147000]))
put('co_sup_n', per([95, 96, 89, 99, 92, 98, 95, 91, 101]))
put('co_sup_rk', per([4, 2, 2, 1, 1, 1, 1, 1, 1]))
put('co_asst', per([118990, 122560, 128560, 132417, 136390, 143210, 148938, 171000, 171000]))
put('co_asst_med', per([110527, 114900, 117760, 120391.5, 130203, 130593, 133150, 135290.5, 136500]))
put('co_asst_n', per([42, 40, 37, 42, 21, 40, 38, 44, 43]))
put('co_asst_rk', per([10, 9, 5, 5, 3, 3, 4, 1, 1]))
put('co_ba', per([110373, 113684, 118231, 121778, 125431, 131703, 125000, 139000, 125000]))
put('co_ba_med', per([92000, 93840, 98066.44, 100477.5, 106954, 110000, 111240, 116901, 117210]))
put('co_ba_n', per([91, 91, 82, 98, 53, 81, 93, 91, 98]))
put('co_ba_rk', per([15, 14, 13, 13, 9, 8, 25, 10, 31]))
# Top of the teacher salary schedule (Oyster River vs NH average of districts), DOE 'Teacher Salary Schedule' files; no 2022-23 file found. Reproduced by build/teacher_sched.py
put('ts_ma_max', per([74639, 75013, 75388, 77742, 78519, None, 80098, 80899, 84401]))
put('ts_ma_max_nh', per([64450, 65332, 66355, 66866, 68313, None, 70903, 73797, 75633]))
put('ts_ba_max', per([68206, 68547, 68890, 71179, 71891, None, 73336, 74069, 77062]))
put('ts_ba_max_nh', per([57243, 57778, 59001, 59938, 60841, None, 63119, 65818, 68119]))
put('ts_ma_steps', per([14, 14, 14, 15, 15, None, 15, 15, 13]))
put('ts_ma_n', per([93, 87, 88, 96, 94, None, 100, 94, 99]))
# NH statewide shares (all districts), DOE 'State Summary Revenue and Expenditures of School Districts' FY18-FY25; reproduced by build/nh_summary.py
put('nh_adm_sh', per([10.452, 10.432, 10.687, 10.696, 10.447, 10.535, 10.675, 10.845]))
put('nh_spec_sh', per([19.654, 19.665, 19.895, 19.278, 19.203, 19.349, 19.715, 20.362]))
put('nh_instr_sh', per([63.106, 62.855, 62.865, 62.165, 61.546, 61.126, 60.472, 60.532]))
put('nh_local_sh', per([61.507, 62.131, 62.561, 60.681, 60.048, 61.435, 60.924, 63.524]))
put('nh_state_sh', per([31.609, 31.152, 31.444, 30.907, 29.452, 28.313, 28.675, 28.193]))
put('nh_fed_sh', per([5.344, 5.115, 4.82, 7.134, 8.887, 8.705, 8.412, 6.034]))
put('nh_plant_sh', per([8.027, 8.23, 8.027, 8.653, 8.318, 8.884, 9.285, 8.977]))
put('nh_trans_sh', per([4.438, 4.517, 4.139, 3.998, 4.548, 4.826, 5.111, 5.361]))
put('nh_debt_sh', per([1.479, 1.419, 1.354, 1.199, 1.139, 1.128, 1.132, 1.049]))
put('tts', per([None, None, None, 0.63, 0.66, 0.63, 0.6, 0.59, 0.64]))
put('tts_nh', per([None, None, None, 0.67, 0.68, 0.68, 0.67, 0.67, 0.66]))
# FTE staff by category, NH DOE iPlatform "Full Time Equivalent Staff Count by District" (ReportID 38), Oyster River Coop, Oct 1 counts
put('ft_teach', per([175.1, 181.1, 182.1, 179.1, 179.1, 180.2, 178.6, 180.0, 178.0]))
put('ft_aide', per([100.1, 92.3, 83.8, 77.8, 98.0, 83.2, 72.0, 77.4, 85.0]))
put('ft_lib', per([4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]))
put('ft_spec', per([27.9, 36.8, 44.7, 30.7, 36.2, 52.9, 54.3, 51.1, 46.0]))
put('ft_adm', per([8.4, 9.2, 9.2, 9.2, 10.2, 10.2, 5.6, 10.2, 10.4]))
put('ft_oth', per([39.6, 72.8, 71.2, 74.2, 59.4, 54.0, 65.4, 73.7, 41.5]))
# IDEA indicator 5 (iReport IDEA Report): share of students with IEPs ages 6-21 in regular class 80%+ of the day (5A), under 40% (5B), separate facilities (5C). DOE repeats prior-year values in 2018-19 and 2019-20 (state too), so those are left blank.
put('incl', per([69.9, None, 72.96, 82.84, 89.26, 90.91, 90.32, 91.09]))
put('incl_nh', per([70.81, None, None, 73.75, 75.42, 78.03, 80.2, 82.13]))
put('incl_lt40', per([4.84, None, None, 4.1, 4.03, 1.3, 0.65, 0.66]))
put('incl_lt40_nh', per([9.05, None, None, 8.95, 8.38, 6.97, 5.43, 4.53]))
put('incl_sep', per([4.91, None, None, 1.49, 4.03, 0.97, 0.32, 0.33]))
put('incl_sep_nh', per([2.84, None, None, 2.46, 1.95, 1.52, 1.24, 1.1]))
# NH suspension rates, iReport ESSA profile for State of NH (All Students), % of students
put('iss_nh', per([3.62, 3.72, 2.56, 0.89, 3.22, 3.48, 3.67, 3.29, 2.9]))
put('oss_nh', per([3.98, 4.15, 3.03, 1.37, 3.98, 4.12, 4.11, 4.41, 4.05]))
# NH habitual truancy: sum of habitually truant students over sum of school enrollment, all NH schools in the DOE School Safety workbooks (2017-18 to 2024-25), per 100 students
put('trunt_nh', per([10.4, 13.94, 11.25, 17.14, 17.23, 16.41, 17.12, 18.79]))  # reproduced by build/nh_truancy.py (FY20 corrected from 11.19 to 11.25 on 2026-11-23)
# State ESSA ratings 1-4 per school (iReport ESSA - Indicators (District)); None = not rated (COVID years), suppressed (<11 students) or not applicable
put('es_hs_ach', per([3, 3, None, 3, 3, 3, 3, 3, 3]))
put('es_hs_ccr', per([3, 3, None, 3, 3, 2, 3, 4, 4]))
put('es_hs_grad', per([4, 4, None, 4, 4, 4, 4, 4, 4]))
put('es_mo_ach', per([3, 4, None, 4, 4, 4, 3, 4, 4]))
put('es_mo_el', per([4, 3, None, None, None, None, None, None, None]))
put('es_mo_eq', per([1, 3, None, None, 2, 3, 1, 1, 3]))
put('es_mo_gro', per([2, 3, None, None, 3, 2, 2, 2, 3]))
put('es_ms_ach', per([4, 3, None, 3, 3, 4, 3, 3, 3]))
put('es_ms_eq', per([2, 2, None, None, 3, 3, 3, 2, 3]))
put('es_ms_gro', per([3, 3, None, None, 3, 3, 3, 3, 3]))
put('es_mw_ach', per([4, 4, None, 4, 4, 4, 3, 4, 4]))
put('es_mw_el', per([None, 3, None, None, None, None, None, None, 3]))
put('es_mw_eq', per([3, 4, None, None, 2, 4, 3, 3, 4]))
put('es_mw_gro', per([4, 4, None, None, 3, 4, 3, 4, 4]))
put('es_ach', per([3.5, 3.5, None, 3.5, 3.5, 3.75, 3.0, 3.5, 3.5]))
put('es_eq', per([2.0, 3.0, None, None, 2.33, 3.33, 2.33, 2.0, 3.33]))
put('es_gro', per([3.0, 3.33, None, None, 3.0, 3.0, 2.67, 3.0, 3.33]))
put("drop", {**RC["drop"], 2026: 0})  # FY26: iExplore dropout rate 0.00% (NH DOE)

# Long-term obligations at June 30, from the audited statement of net position (page 14 of each audit; build/audit_extract.py -> build/audit_metrics.json)
import json as _json, os as _os
_AU = {int(y): v for y, v in _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "audit_metrics.json"))).items()}
def _au(k): return {y: v[k]["v"] for y, v in _AU.items() if k in v}
put("debt_bonds", {y: int(_au("bonds_current")[y] + _au("bonds_noncurrent")[y]) for y in _AU})
put("debt_pension", {y: int(v) for y, v in _au("net_pension").items()})
put("debt_opeb", {y: int(v) for y, v in _au("net_opeb").items()})
put("debt_total", {y: RC["debt_bonds"][y] + RC["debt_pension"][y] + RC["debt_opeb"][y] for y in _AU})
put("netpos", {y: int(v) for y, v in _au("net_position").items()})
put("debt_int", {y: int(v) for y, v in _au("interest_expense").items()})

# Budget tables printed in the annual reports (build/budget_extract.py -> build/budget_tables.json)
_BT = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "budget_tables.json")))
_DEPTS = ["mastway", "moharimet", "middle", "high", "specialed", "sau", "transport", "technology", "facilities"]
def _dept(kind, dept):
    d = {}
    for r in sorted(_BT["dept"], key=lambda r: r["report"]):       # later reports overwrite earlier ones for the same year
        if r["kind"] == kind and r["dept"] == dept: d[r["fy"]] = int(r["value"])
    return d
for _k in _DEPTS:
    put("bd_a_" + _k, {y: v for y, v in _dept("approved", _k).items() if y >= 2018})
    put("bd_e_" + _k, {y: v for y, v in _dept("expended", _k).items() if y >= 2018})
put("bd_appr", {y: v for y, v in _dept("approved", "total").items() if y >= 2018})
put("bd_exp", {y: v for y, v in _dept("expended", "total").items() if y >= 2018})
for _name, _key in (("f10", "general_fund"), ("f21", "food_service"), ("f22", "federal"), ("f23", "pass_through"), ("dflt", "default")):
    put(_name, {r["fy"]: int(r[_key]) for r in _BT["funds"]})
put("bd_unspent", {y: RC["bd_appr"][y] - RC["bd_exp"][y] for y in RC["bd_exp"] if y in RC["bd_appr"]})
# total operating budget (all funds) minus the default budget: what the vote adds (or removes) relative to the default
put("dflt_gap", {y: RC["f10"][y] + RC["f21"][y] + RC["f22"][y] + RC["f23"][y] - RC["dflt"][y] for y in RC["dflt"]})
# the district's estimated change in the local school tax rate (per $1,000) from the proposed budget, by town: proposed rate minus current rate, assessed value held fixed
for _t in ("durham", "lee", "madbury"):
    put("ti_" + _t[:3], {r["fy_prop"]: round(r["local_rate"][1] - r["local_rate"][0], 2) for r in _BT["tax"] if r["town"] == _t})

# Special education expenditures and offsetting revenue "per RSA 32:11-a", printed in the 2025 report (2022-23, 2023-24) and the 2026 report (2023-24, 2024-25); FY = year the school year ends.
# The 2026 report repeats FY2024 and its figures match the 2025 report to the dollar. Revenue total FY2023 is printed $987,617 (its three lines add to $987,618).
_RSA = {  # fy: (special ed 1200, related services, transportation 2722, IDEA grant 1210, total, state aid, Medicaid, IDEA, total revenues)
    2023: (7500199, 2248265, 305784, 558569, 10612817, 298552, 130497, 558569, 987617),
    2024: (8023162, 2413345, 406057, 520529, 11363093, 295029, 168136, 520529, 983694),
    2025: (8419644, 2620469, 259742, 500208, 11800063, 133198, 195370, 500208, 828776)}
for _i, _n in enumerate(("rsa_cost", "rsa_rel", "rsa_trn", "rsa_idea", "rsa_tot", "rsa_aid", "rsa_med", "rsa_fed", "rsa_rev")):
    put(_n, {y: v[_i] for y, v in _RSA.items()})
put("rsa_net", {y: v[4] - v[8] for y, v in _RSA.items()})

FIELDS = sorted(RC)
def fields_for(y):
    return {k: RC[k].get(y) for k in FIELDS}

