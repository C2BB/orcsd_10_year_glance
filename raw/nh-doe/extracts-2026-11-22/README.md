# Extracts pulled 2026-11-22 (eighteenth pass)

These are transcriptions of what the NH DOE Tableau and iPlatform pages returned, not byte copies of a file: those sources are live dashboards with no downloadable file. Each is a plain-text table; the page's numbers come from build/rc_data.py, which was generated from these.

- iplatform-town-enrollment-by-grade.py: iPlatform Town Level Enrollment By Grade (ReportID 12), Durham/Lee/Madbury, per grade, SchoolYear 2018 to 2027 (FY key; 2027 = first DOE run, Oct 1 2026).
- iexplore-school-level.py: iExplore Compare dashboard, Oyster River High School / Middle School / Mast Way / Moharimet and the district, DOE years 2016 to 2026 (enrollment, proficiency, growth, certified, experienced, counselor, non-teacher ratio, SWD, cost per pupil, violence incidents).
- ireport-essa-ratings.txt: iReport ESSA Indicators (District), ratings 1 to 4 by school, FY2018 to FY2026.
- gen_block.py: script that turned these (plus the iReport IDEA and state-entity suspension values, FTE staff report values and truancy rates listed in it) into the put(...) lines in build/rc_data.py.
How to re-pull: see HANDOFF.md, "How data gets in".
