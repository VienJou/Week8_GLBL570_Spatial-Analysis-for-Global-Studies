# GLBL 570 · Methodologies of Global Studies — Week 8 Lab: GIS Workshop II

Everything you need for today's lab is in this folder. You do **not** need the Week 7 download.
Step-by-step instructions, with the exact QGIS menus and numbers to check your work against, are in
**`GLBL570_Week8_Lab_Guide.pdf`**. Open it next to QGIS.

## What you will do (60 minutes)

| Time | Task | Folder | What you hand in |
|---|---|---|---|
| 0–15′ | **Task 1 · Overlay** — what share of the forest around Mount Hood (Oregon/Washington) is protected, under a strict (GAP 1–2) and a broad (GAP 1–3) definition? | `Task1_Overlay/` | forest area inside and outside protection, km² and % |
| 15–30′ | **Task 2 · Buffer** — how many of the 33 Rohingya refugee camps in Cox's Bazar lie within 1, 5 and 10 km of a 2023 conflict event, under the rules "≥ 1 event" and "≥ 3 events"? | `Task2_Buffer/` | camp counts for each radius and rule |
| 30–45′ | **Task 3 · Image classification** — classify a Sentinel-2 image of Champaign–Urbana with a random forest in QGIS (SCP plug-in): first with a summer image, then with summer + spring. Training and check areas are provided | `Task3_Image_Classification/` | overall and per-class accuracy of both runs; the class map |
| 45–55′ | **Task 4 · Map and memo** — export your result map(s) and write a 200–300-word memo with ONE policy implication | `Task4_Memo/` (template) | map(s) + memo |
| 55–60′ | Submit on Canvas | | |
| after class | **Optional extensions** — A: is poverty clustered across U.S. counties? (Moran's I, LISA, Gi*) · C: turn 2023 conflict-event points into a country map | `Extensions/` | — |

## What is in each folder

| Folder | File | What it is |
|---|---|---|
| `Task1_Overlay/` | `focus_nlcd2021_30m.tif` | NLCD 2021 land cover, 30 m, EPSG:5070. Forest = classes 41, 42, 43. Class names in `nlcd_classes.csv` |
| | `padus41_mthood_gorge.shp` | 3,043 protected areas (PAD-US 4.1), EPSG:4326. `GAP_Sts` = protection level 1–4 (stored as text) |
| | `focus_counties_pnw.shp` | The six study counties, EPSG:4269 |
| `Task2_Buffer/` | `coxsbazar_camps_2023.shp` | 33 refugee-camp outlines, EPSG:32646 (UTM 46N, metres). Camp level only |
| | `ucdp_ged_2023_near_camps.csv` | 410 conflict events of 2023 near the camps; columns `longitude`, `latitude`, `deaths_best`, `where_prec` |
| `Task3_Image_Classification/` | `summer_2023/S2_summer_B02_blue.tif` … `B08_nir.tif` | Sentinel-2 L2A median, June–September 2023, Champaign–Urbana; one file per band (blue, green, red, near-infrared), 10 m, EPSG:5070, reflectance × 10,000 |
| | `spring_2023/S2_spring_B02_blue.tif` … `B08_nir.tif` | The same four bands for April–May 2023, on the same grid — fields are still bare soil |
| | `champaign_training_rois.gpkg` | 154 training squares (90 × 90 m) in 5 classes: 1 Water · 2 Developed · 3 Forest · 4 Grass and pasture · 5 Cropland. Fields `macroclass_id`, `macroclass_name`, `class_id`, `class_name` — ready for SCP *Import vector* |
| | `champaign_validation_rois.gpkg` | 120 separate check squares, ≥ 300 m from any training square — for SCP *Postprocessing ▸ Accuracy* |
| | `champaign_nlcd2021_30m.tif` | NLCD 2021 land cover, 30 m, the source of the class labels (class names in `nlcd_classes.csv`) |
| `Task4_Memo/` | `week8_memo_template.md` | Memo headings: question · data and units · operations and results · one policy implication · what it cannot establish · AI and ethics |
| `Extensions/A_Spatial_Statistics/` | `us_counties_acs2022.shp` | 3,144 U.S. counties with ACS 2018–2022 data, EPSG:4269. Poverty = `pov_pct`; field names in `us_counties_acs2022_field_dictionary.csv` |
| `Extensions/C_OSINT/` | `ucdp_ged_events_2023.csv`, `world_countries_ne110m.shp` | All 24,205 UCDP conflict events of 2023 (`longitude`, `latitude`, `deaths_best`) and 177 country outlines (Natural Earth), EPSG:4326 |

**Keep every `.csvt` next to its `.csv`, and every `.dbf`, `.prj`, `.shx`, `.cpg` next to its `.shp`.** QGIS needs them.

## Before you start
- QGIS 3.28 or later with the **Semi-Automatic Classification Plugin** (SCP) and scikit-learn — install before class (Task 3). Extension A also needs **GeoDa** (free, geodacenter.github.io).
- Distances and areas only work in metres: use EPSG:5070 for Task 1 and EPSG:32646 for Task 2.
- Save outputs as GeoPackage (`.gpkg`) files in your own folder, not as temporary layers.

## Ethics
The camp layer contains camp outlines only. Do not map individual shelters or blocks, and think before you publish exact
locations of conflict events (Extension C asks you to reflect on this).

## Sources and licences
PAD-US 4.1 (USGS Gap Analysis Project, public domain) · NLCD 2021 (USGS/MRLC, public domain) · Rohingya camp outlines
(RRRC / ISCG, UNHCR, IOM via HDX, CC0) · UCDP GED v24.1 (Uppsala Conflict Data Program, CC BY 4.0) · ACS 2018–2022 and county
boundaries (U.S. Census Bureau) · Sentinel-2 L2A, 2023 (Copernicus/ESA, via Google Earth Engine) · Natural Earth (public domain).
