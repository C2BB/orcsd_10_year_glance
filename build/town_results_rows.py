"""Page fields for Oyster River results by town of residence (build/town_results.json, from town_results_extract.py).

{field: {fiscal_year_end: value}}; fiscal year key = the year the school year ends (the 2022 test is FY2021-22 = 2022).
  twp_<t>      mean of the reading and math shares at levels 3 and 4 (t = dur, lee, mad)
  tw_rea_<t>, tw_mat_<t>, tw_sci_<t>   the three subjects
  tw_sgp_<t>   mean of the reading and math mean growth percentiles (when both are published)
  tw_n_<t>     tested students (midpoint of the DOE's rounded count, math)
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
TOWN = {"Durham": "dur", "Lee": "lee", "Madbury": "mad"}


def fields():
    D = json.load(open(os.path.join(HERE, "town_results.json")))
    out = {}
    for y, towns in D.items():
        for name, t in TOWN.items():
            c = towns[name]
            rea, mat, sci = c["rea"]["prof"], c["mat"]["prof"], c["sci"]["prof"]
            out.setdefault("twp_" + t, {})[int(y)] = round((rea + mat) / 2, 1)
            out.setdefault("tw_rea_" + t, {})[int(y)] = rea
            out.setdefault("tw_mat_" + t, {})[int(y)] = mat
            if sci is not None:
                out.setdefault("tw_sci_" + t, {})[int(y)] = sci
            if c["rea"]["sgp"] is not None and c["mat"]["sgp"] is not None:
                out.setdefault("tw_sgp_" + t, {})[int(y)] = round((c["rea"]["sgp"] + c["mat"]["sgp"]) / 2, 1)
            out.setdefault("tw_n_" + t, {})[int(y)] = sum(c["mat"]["n"]) / 2
    return out


if __name__ == "__main__":
    for k, v in sorted(fields().items()):
        print(k, v)
