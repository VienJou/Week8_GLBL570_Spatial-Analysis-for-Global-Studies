# GLBL 570 Week 8: Spatial Analysis for Global Studies (companion notebook + lab data)

`GLBL570_Week8_Spatial_Analysis_Lab.ipynb` follows the eight chapters of the Week 8 lecture (overlay · buffer and proximity ·
clusters and hotspots · remote sensing and machine learning · the politics of categories · discussion · lab) and writes the
15 figures the lecture deck uses into `outputs/`. Every analytical section ends with a `CANNOT ESTABLISH:` line naming what
the result does not show.

## Contents

| Path | What it is |
|---|---|
| `GLBL570_Week8_Spatial_Analysis_Lab.ipynb` | The notebook (saved with outputs) |
| `lab_data_week8/` | Week 8 additions: PAD-US 4.1 protected areas and NLCD 2021 / SRTM rasters for Mount Hood–Columbia Gorge, Cox's Bazar refugee-camp outlines, UCDP conflict events near the camps. See `lab_data_week8/README.md` (sources, licences, CRS, pitfalls) |
| `lab_data/` | The Week 7 data pack, unchanged (U.S. counties + ACS, earthquakes, world countries, UCDP 2023, Illinois rasters, Champaign Sentinel-2). See `lab_data/README.md`; built by the Week 7 repository [GLBL570-Week7-GIS](https://github.com/VienJou/GLBL570-Week7-GIS) |
| `outputs/` | The 15 lecture figures (PNG, 220 dpi; PDF for line-work figures) and the memo template |
| `scripts/` | Rebuild `lab_data_week8/` (`build_lab_data_week8.py`; rasters: `fetch_rasters_gee_week8.py`) |
| `requirements.txt` | Python libraries (includes scikit-learn for §5) |

## Run
* CPU only, no internet needed. Full run ≈ 3.5–5 minutes.
* Tested on Python 3.9 (NumPy 1.26) and Python 3.12 (NumPy 2.5, pandas 3.0). On I-GUIDE use the `geoai-edu` kernel.
* `pip install -r requirements.txt`, open the notebook **from the repository root** (paths are relative), then *Run All*.
* The last cell checks that all 15 figures were written and prints the headline numbers for the lecture.
* Rebuilding the data is optional: `requests` for `build_lab_data_week8.py`; `earthengine-api`, `google-auth` and an
  Earth Engine key (`GEE_KEY`, `GEE_PROJECT` environment variables) for `fetch_rasters_gee_week8.py`.

## Figures (deck slide → file in `outputs/`)
17 `overlay_operations` · 18 `overlay_policy_forest_protected` · 21 `distance_to_water_development` · 23 `buffer_sensitivity` ·
24 `proximity_toolbox` · 25 `data_preprocessing_dissolve_integrate` · 27 `clusters_moran_lisa` · 28 `spatial_correlation_two_variables` ·
33 `hotspots_getis_ord` · 34 `point_pattern_nn` · 37 `rs_ndvi_classification` · 41 `ml_confusion_matrix` ·
43 `categories_forest_definitions` · 45 `maup_two_aggregations` · 46 `ethics_point_vs_aggregated`

## Data sources
USGS PAD-US 4.1; USGS/MRLC NLCD 2021; NASA/USGS SRTM; ISCG/RRRC Rohingya camp outlines (HDX, CC0); UCDP GED v24.1 (CC BY 4.0);
U.S. Census Bureau ACS 2018–2022 and boundaries; USGS Earthquake Catalog 2025; Natural Earth; Copernicus Sentinel-2.
Licences and caveats are listed in the two data READMEs.
