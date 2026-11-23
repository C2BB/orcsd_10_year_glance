# ORCSD "Ten years at a glance"

Independent school-finance and outcomes dashboard for the Oyster River Cooperative School District (Durham, Lee, Madbury), FY 2017-18 to FY 2026-27, built from public NH DOE, NH DRA, BLS and ORCSD records. Not an official publication of the district or the state.

Live page: https://c2bb.github.io/orcsd_10_year_glance/

## Layout

| Path | What it is |
|---|---|
| `index.html`, `app.js` | The page. Loads `data/*.json` at runtime, then draws. |
| `data/orcsd_years.json` | One row per fiscal year with every value the page shows (plus `meta` documenting each field). |
| `data/sources.json` | Per-row, per-year links to the original file or section page. |
| `dist/ORCSD_Ten_Years_at_a_Glance.html` | Same page as one file with the data inlined; works from disk or as an attachment. |
| `raw/` | Copies of the source files the values were taken from (`raw/MANIFEST.csv` lists the original URL, retrieval date, size and SHA-256 of each). |
| `build/` | Scripts that regenerate `data/` and the page from the raw values. |

## Rebuilding

```
cd build
python3 make_data.py     # rc_data.py + doe25.py + nhdoe_values.py + towns_data.py -> orcsd_years.json
python3 build_pages.py   # -> ../index.html, ../app.js, ../data/, ../dist/
```

Fiscal-year key = year the school year ends (FY 2018 = 2017-18). Many values were read by hand from PDFs (annual reports, DOE PDFs); those are keyed in `build/rc_data.py` and `build/towns_data.py` with comments naming the source file.

To preview locally: `python3 -m http.server` in the repo root and open http://localhost:8000/ (browsers block `fetch` on `file://`, which is why `dist/` exists).

## Caveats

Some figures are estimates or computed (tagged on the page). Source files can move or disappear on the agency sites, which is why copies are kept in `raw/`. Prose notes on the page contain a few numbers typed in as text; the charts and labels come from `data/orcsd_years.json`.

## About `raw/`

Large statewide assessment CSVs are stored gzipped (`.csv.gz`); `MANIFEST.csv` records the SHA-256 of the original file. Every file listed in the manifest is mirrored; a row marked `link-only (not mirrored)` would mean a copy could not be made, and its source URL is still listed.
