# GLBL 570 · Week 8 lab data

These layers sit beside `notebook_data/` (the Week 7 layers the notebook reuses) and feed `../GLBL570_Week8_Spatial_Analysis_Lab.ipynb`.
All open in QGIS 3.x without plug-ins. Built by `scripts/build_lab_data_week8.py` (vectors, tables) and
`scripts/fetch_rasters_gee_week8.py` (rasters). Total size ≈ 11 MB; no file exceeds 5 MB.

## Files

| Folder / file | Type | CRS (as stored) | What it is |
|---|---|---|---|
| `vector/focus_counties_pnw.shp` | polygons, 6 | EPSG:4269 | Focus area: Multnomah, Clackamas, Hood River, Wasco (OR), Clark, Skamania (WA) — copied from the Week 7 county layer |
| `vector/padus41_mthood_gorge.shp` | polygons, 3,043 | EPSG:4326 | PAD-US 4.1 protected areas intersecting the focus area, clipped to it. Fields: `padus_oid`, `Unit_Nm`, `Category`, `GAP_Sts`, `IUCN_Cat`, `Mang_Name`, `Mang_Type`, `Own_Name`, `Des_Tp`, `Date_Est`, `State_Nm`, `GIS_Acres` |
| `vector/coxsbazar_camps_2023.shp` | polygons, 33 | EPSG:32646 (WGS 84 / UTM 46N) | Rohingya refugee **camp** outlines, Cox's Bazar, Bangladesh (camp level only — no blocks, no shelters) |
| `tables/ucdp_ged_2023_near_camps.csv` (+ `.csvt`) | table with lon/lat, 410 rows | EPSG:4326 | UCDP GED 2023 events within 300 km of the camps (same columns as the Week 7 UCDP table) |
| `raster/focus_nlcd2021_30m.tif` | uint8, 1 band + colour table | EPSG:5070 | NLCD 2021 land cover, **raw class codes**, on the native CONUS NLCD 30 m grid; 0 = outside the focus area |
| `raster/focus_srtm_90m.tif` | int16, 1 band | EPSG:5070 | SRTM elevation (m), 90 m; −32768 = outside the focus area |
| `raster/nlcd_classes.csv` | table | — | NLCD class value → label (value attribute table) |
| `raster/champaign_nlcd2021_30m.tif` | uint8, 1 band + colour table | EPSG:5070 | NLCD 2021, native 30 m grid, covering the Champaign Sentinel-2 scene (source of the classification labels) |
| `raster/champaign_sentinel2_2023spring_10m.tif` | uint16, 4 bands | EPSG:5070 | Sentinel-2 L2A median, Apr–May 2023, bands 1–4 = red, green, blue, NIR (× 10,000), on the same 10 m grid as the Week 7 summer scene |
| `vector/champaign_training_rois.gpkg` | polygons, 154 | EPSG:5070 | Classification training squares (90 × 90 m, one NLCD macroclass each): fields `macroclass_id`, `macroclass_name`, `class_id`, `class_name` for SCP *Import vector* |
| `vector/champaign_validation_rois.gpkg` | polygons, 120 | EPSG:5070 | Separate check squares, ≥ 300 m from any training square, same fields |

Reused from `notebook_data/` (the Week 7 pack): `us_counties_acs2022.shp` (contiguous-U.S. counties for §1 and §4), `us_states.shp`, `usgs_earthquakes_2025_m25.shp`, `world_countries_ne110m.shp`, `ucdp_ged_events_2023.csv`, the Champaign Sentinel-2 scene and the Illinois NLCD (§5).

## Sources and licences

| Layer | Source | Licence |
|---|---|---|
| PAD-US 4.1 | USGS Gap Analysis Project, *Protected Areas Database of the United States 4.1* (2024), via the USGS ArcGIS FeatureServer `Manager_Name_PADUS` | U.S. Government work, public domain |
| NLCD 2021 | USGS / MRLC National Land Cover Database, via Google Earth Engine `USGS/NLCD_RELEASES/2021_REL/NLCD` | Public domain |
| SRTM | NASA / USGS SRTM 1 arc-second v3, via Earth Engine `USGS/SRTMGL1_003` | Public domain |
| Camp outlines | RRRC / ISCG Site Management Sector, UNHCR, IOM — *Outline of camps of Rohingya refugees in Cox's Bazar* (A1, 2023-04-12), HDX | **CC0 / public domain** (redistribution allowed) |
| Conflict events | Uppsala Conflict Data Program, UCDP GED v24.1 (Sundberg & Melander 2013; Davies et al. 2024) | CC BY 4.0 — cite UCDP |
| County boundaries | U.S. Census Bureau cartographic boundaries (Week 7 pack) | Public domain |

No source needs an API key to *use* the data. Rebuilding the rasters needs an Earth Engine service account: set the environment
variables `GEE_KEY` (path to the JSON key) and `GEE_PROJECT`. Never commit the key.

## Known pitfalls

- **PAD-US records overlap.** A wilderness sits inside a national forest inside a scenic area, each as its own record. Summing `GIS_Acres`
  or polygon areas gives 15,665 km²; the dissolved footprint is 9,977 km². Always dissolve before measuring area (notebook §3.3).
- **"Protected" depends on GAP status.** GAP 1–2 (managed for biodiversity) covers 2,085 km² of the focus area; GAP 1–3 (adds multiple-use
  land such as most national-forest land) covers 9,774 km². State which one you used. `Category = 'Proclamation'` (administrative
  boundaries, not protection) was excluded at download.
- **`Date_Est` is filled for only 11 % of records**; do not analyse establishment dates without checking coverage.
- **PAD-US geometry was generalised at download** (`maxAllowableOffset = 0.0003°`, ≈ 25–33 m), which suits 30 m analysis but not parcel-level
  work. A few polygons become invalid after reprojection to EPSG:5070 — repair them (`make_valid`; QGIS *Fix geometries*) before overlay.
- **Native CRS notes.** PAD-US is maintained in a USGS Albers projection; the FeatureServer returns GeoJSON in EPSG:4326, which is stored
  unchanged. SRTM (native 1 arc-second, EPSG:4326) was resampled by Earth Engine to 90 m in EPSG:5070 so it shares the analysis grid;
  NLCD is on its native 30 m Albers grid. Everything else is stored in its native CRS; the notebook reprojects.
- **Camp CRS.** The source `.prj` combines UTM 46N with a vertical CRS, which a Shapefile cannot store; only the horizontal part
  (EPSG:32646) was kept — coordinates are unchanged.
- **Ethics.** Only camp-level outlines are included. Block and sub-block layers exist on HDX but are not redistributed here; never publish a
  map that locates individual shelters.
- **UCDP location precision (`where_prec`).** Of the 410 events, 233 are precision 5 (known only to a wider area). Every event within 5 km of
  a camp is precision 1–2; three precision-5 events lie 5–10 km away. The camp-share results in the notebook are identical when only
  precise events (precision 1–2) are used — check this again if you change the radii or the region.
- **Classification squares** come from `scripts/build_scp_training_week8.py`: 5 macroclasses (1 Water = 11 · 2 Developed = 22–24 · 3 Forest = 41–43 ·
  4 Grass and pasture = 71, 81 · 5 Cropland = 82); NLCD 21 (developed, open space) is left out because it is mostly lawn. A random forest on the
  summer bands alone reaches 0.66 validation accuracy; adding the spring bands gives 0.81 (cropland recall 0.56 → 0.88). Labels are 2021, imagery 2023.
- **SRTM** has a few small negative values along the Columbia River (artefacts). **NLCD** is a 2021 snapshot.
