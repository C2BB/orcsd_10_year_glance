"""ORCSD's figures from the NH Retirement System (NHRS) employer reporting schedules, GASB 68 (pension) and GASB 75 (retiree health).

NHRS publishes, every year, one schedule of employer allocations and one schedule of pension (or OPEB) amounts that list every
participating employer, including "Oyster River Coop SD" (the teacher group).  Source: https://www.nhrs.org/employers/employer-resources/gasb/gasb-reports
The PDFs are mirrored in raw/nhrs/ (see raw/MANIFEST.csv) and build/verify_nhrs.py re-reads every number below from them.

Fiscal year key = the year the school year ends.  NHRS reports at a June 30 measurement date and the district's audit uses
that report one year later (the audit for the year ended June 30, 2024 shows the liability measured at June 30, 2023), so
measurement year Y is stored under fiscal year Y+1.  That is why the page has FY2026 values before the FY2025 audit is posted.

Fields (all for "Oyster River Coop SD"):
  nhrs_share   proportionate share of the NHRS employer pool for pensions, %
  nhrs_npl     net pension liability, $
  nhrs_do      total deferred outflows of resources (pension), $
  nhrs_di      total deferred inflows of resources (pension), $, shown positive
  nhrs_exp     total employer pension expense, $
  nhrs_con     employer pension contributions for the year, $
  nhrs_oshare  proportionate share for the medical subsidy (OPEB), %
  nhrs_onl     net OPEB liability for the medical subsidy, $
  nhrs_oexp    total employer OPEB expense, $ (negative = credit)
  nhrs_ocon    employer OPEB contributions for the year, $
"""

# measurement year: (share %, NPL, deferred outflows, deferred inflows (positive), total pension expense, contributions,
#                    OPEB share %, net OPEB liability, OPEB expense, OPEB contributions)
_NHRS = {
    2017: (0.65124480, 32028173, 4492208, 884793, 3709432, 2385792, 0.81346437, 3719435, 417357, 482141),
    2018: (0.70086645, 33748138, 5253897, 1100965, 4136716, 2962266, 0.64748977, 2964504, -265695, 286404),
    2019: (0.69276755, 33333582, 3225345, 1307836, 4835664, 3014797, 0.63766395, 2795590, -18660, 291004),
    2020: (0.71051541, 45445639, 10294656, 706715, 7598033, 3156408, 0.70332542, 3078519, 538383, 326464),
    2021: (0.72354364, 32066870, 5656436, 9443661, 3320547, 3324150, 0.71646897, 2869149, 229111, 344300),
    2022: (0.69216221, 39703339, 5096341, 1492470, 4253098, 4007724, 0.69156272, 2613328, -7711, 291210),
    2023: (0.70047728, 39214679, 3360030, 961587, 4929084, 4212316, 0.69702100, 2381861, 77874, 305061),
    2024: (0.67276659, 34886575, 1144545, 2662682, 3643634, 4055160, 0.63663128, 1979030, -173611, 225888),
    2025: (0.66995842, 33330977, 2335340, 3046513, 1886212, 4248770, 0.61992763, 1853631, 133542, 231001),
}
_KEYS = ("nhrs_share", "nhrs_npl", "nhrs_do", "nhrs_di", "nhrs_exp", "nhrs_con", "nhrs_oshare", "nhrs_onl", "nhrs_oexp", "nhrs_ocon")


def measurement_years():
    return sorted(_NHRS)


def fields():
    """{field: {fiscal_year_end: value}}"""
    out = {k: {} for k in _KEYS}
    for my, vals in _NHRS.items():
        for k, v in zip(_KEYS, vals):
            out[k][my + 1] = v
    return out


if __name__ == "__main__":
    for k, d in fields().items():
        print(k, [d.get(y) for y in range(2018, 2027)])
