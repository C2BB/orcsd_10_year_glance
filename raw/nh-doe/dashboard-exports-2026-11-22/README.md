# NH DOE dashboard exports (retrieved 2026-11-22)

The NH DOE iExplore and iReport dashboards (Tableau) have no download button for the tables this page uses. These two
files are the underlying worksheet data, read with the Tableau Embedding API (`getSummaryDataAsync`) after setting the
dashboard parameters in a browser, then copied here byte for byte (SHA-256 checked end to end).

- `iexplore_compare_all_entities.tsv` : iExplore "Compare Dashboard", worksheet `*Download Compare`. Parameters
  `Compare: Entity A/B (+ Download)` = each entity, `Year ID Param` = 2018, 2021, 2024, 2026.
- `ireport_essa_idea_suspension.tsv` : iReport. Parameters `Search for School or District Name (Master)` and `Select Year`.
  Worksheets: ESSA Profiles (District) `SE - In School`, `SE - Out of School`, `SE - Expusions`, `ESSA - Indicators (District)`
  (filtered to the three Oyster River schools), and IDEA Report `Indicator 5: School-Age Placement`.
  The first lines of each file (`#`) record the exact parameters and columns.

Year labels follow NH DOE: 2018 = school year 2017-18 (page FY18).
The dashboards are live and may change; these files are the values as of the retrieval date.

Note: `ireport_essa_idea_suspension.tsv` contains only the header (no rows) for the `ESSA - Indicators (District)`
worksheet; that worksheet returned every NH school and was left out. ESSA ratings used on the page are checked against
the iExplore export instead (`python3 build/verify_dashboard_values.py`).
