# GLBL 570 · Methodologies of Global Studies — Week 8: Spatial Analysis for Global Studies

Companion notebook, lab materials and data for Week 8 (Module 4, GIS weeks 7–8).

- **`GLBL570_Week8_Spatial_Analysis_Lab.ipynb`** follows the eight chapters of the Week 8 lecture (what is spatial analysis ·
  overlay · proximity: distance and buffer · clusters and hotspots · remote sensing and machine learning · the politics of categories ·
  ethics, representation and data use · lab activities) and writes 16 figures into `outputs/` — 11 used in the lecture deck, 5 supplementary. Every figure is followed by a
  "Reading the figure" cell (data · what we did · what it shows), and every analytical section ends with a `CANNOT ESTABLISH:` line.
- **`GLBL570_Week8_Lab/`** is the self-contained hands-on lab (GIS Workshop II) for students: one folder per task, the lab guide and a README.

## Contents

| Path | What it is |
|---|---|
| `GLBL570_Week8_Spatial_Analysis_Lab.ipynb` | The notebook, saved with outputs (English) |
| `GLBL570_Week8_Lab/` | **Student lab package** — `README.md` (schedule and files), `GLBL570_Week8_Lab_Guide.pdf`, and data folders `Task1_Overlay/`, `Task2_Buffer/`, `Task3_Image_Classification/`, `Task4_Memo/`, `Extensions/`. Nothing else needs to be downloaded |
| `GLBL570_Week8_Lab.zip` | The same lab package as one download (43 MB) — give this to students; it unzips to `GLBL570_Week8_Lab/` |
| `GLBL570_Week8_Lab_Guide.pdf` | The 7-page lab guide: the files each task uses, and exact QGIS / SCP steps with self-check numbers for Tasks 1–4 |
| `notebook_data_week8/` | Week 8 data: PAD-US 4.1 protected areas, NLCD 2021 and SRTM for Mount Hood – Columbia Gorge, Cox's Bazar camp outlines, UCDP events near the camps, and for the classification task a spring Sentinel-2 scene, 30 m NLCD and ready-made training / validation areas. See `notebook_data_week8/README.md`. Used by the notebook; the lab package has its own copies, so students do not need this folder |
| `notebook_data_week7/` | Week 7 layers the notebook reuses (U.S. counties + ACS, states, earthquakes, world countries, UCDP 2023, Illinois NLCD, Champaign Sentinel-2) — the Week 7 data pack, renamed. See `notebook_data_week7/README.md`. Not needed for the lab |
| `outputs/` | The 16 lecture figures (PNG, 220 dpi; PDF for line-work figures) and the memo the notebook fills in |
| `scripts/` | Rebuild the data: `build_lab_data_week8.py` (vectors, tables), `fetch_rasters_gee_week8.py` (rasters), `build_scp_training_week8.py` (spring scene, 30 m NLCD, training and validation areas), `make_lab_package_week8.py` (assembles `GLBL570_Week8_Lab/`) |
| `plan/` | Regenerate the notebooks: `build_week8_notebook.py` (builds the English notebook; reading texts in `week8_reads.py`) and `make_week8_zh.py` (run after executing the notebook: removes the build metadata; also writes a Chinese review copy, which is not distributed here); source files for the lab package README and memo template |
| `requirements.txt` | Python libraries (includes scikit-learn) |

## Run the notebook
* CPU only, no internet needed. A full run takes about 5–7 minutes.
* Tested on Python 3.9 (NumPy 1.26) and Python 3.12 (NumPy 2.5, pandas 3.0). On I-GUIDE use the `geoai-edu` kernel.
* `pip install -r requirements.txt`, open the notebook **from the repository root** (it reads `notebook_data_week7/` and `notebook_data_week8/`), then *Run All*.
* The last cell checks that all 16 figures were written and prints the headline numbers for the lecture.

## The lab (GIS Workshop II, 60 minutes)

| Time | Task | Folder |
|---|---|---|
| 0–15′ | Task 1 · Overlay — forest × PAD-US protected areas around Mount Hood: how much forest is protected (GAP 1–2 vs GAP 1–3)? | `Task1_Overlay/` |
| 15–30′ | Task 2 · Buffer — how many of the 33 Rohingya camps lie within 1 / 5 / 10 km of a 2023 conflict event? | `Task2_Buffer/` |
| 30–45′ | Task 3 · Image classification with the QGIS SCP plug-in — random forest on Sentinel-2, summer only vs summer + spring (validation accuracy ≈ 0.66 vs ≈ 0.81) | `Task3_Image_Classification/` |
| 45–55′ | Task 4 · Export the result map(s) and write a 200–300-word memo with one policy implication | `Task4_Memo/` |
| after class | Optional extensions: A · Moran's I / LISA / Gi* (GeoDa) · C · OSINT aggregation of conflict events | `Extensions/` |

Give students `GLBL570_Week8_Lab/` (or the ZIP made by `python scripts/make_lab_package_week8.py`). They need QGIS 3.28+,
the Semi-Automatic Classification Plugin with scikit-learn (Task 3), and GeoDa only for Extension A.

## Figures (lecture deck slide → file in `outputs/`)
Slide numbers follow the final Week 8 deck (56 slides, slide order).
9 `spatial_shuffle_test` · 12 `overlay_operations` · 13 `overlay_policy_forest_protected` · 17 `buffer_sensitivity` ·
18 `distance_to_water_development` · 22, 24 `clusters_moran_lisa` · 23–24 `hotspots_getis_ord` · 28 `rs_ndvi_classification` ·
appendix: 47 `point_pattern_nn` · 48 `rs_ndvi_classification` · 50 `maup_two_aggregations` · 56 `ethics_point_vs_aggregated`.
Supplementary (not in the slides; used by the lab or extending a slide with our data): `proximity_toolbox` ·
`data_preprocessing_dissolve_integrate` · `spatial_correlation_two_variables` · `ml_confusion_matrix` · `categories_forest_definitions`.

## Rebuilding the data (optional)
`requests` for `build_lab_data_week8.py`; `earthengine-api`, `google-auth` and an Earth Engine service-account key for
`fetch_rasters_gee_week8.py` and `build_scp_training_week8.py` — set the environment variables `GEE_KEY` (path to the JSON key)
and `GEE_PROJECT`. Never commit the key.

## Data sources
USGS PAD-US 4.1; USGS/MRLC NLCD 2021; NASA/USGS SRTM; ISCG/RRRC Rohingya camp outlines (HDX, CC0); UCDP GED v24.1 (CC BY 4.0);
U.S. Census Bureau ACS 2018–2022 and boundaries; USGS Earthquake Catalog 2025; Natural Earth; Copernicus Sentinel-2 (2023).
Licences and caveats are listed in the data READMEs.
