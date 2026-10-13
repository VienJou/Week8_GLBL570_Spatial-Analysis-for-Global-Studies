"""Build notebook_data_week8/ (vectors and tables) for the Week 8 spatial-analysis notebook.

  vector/focus_counties_pnw.shp         6 counties around Mt Hood / Columbia Gorge (from the Week 7 pack)
  vector/padus41_mthood_gorge.shp       PAD-US 4.1 protected areas intersecting the focus area (USGS GAP)
  vector/coxsbazar_camps_2023.shp       Rohingya refugee camp outlines, Cox's Bazar (ISCG / HDX, CC0)
  tables/ucdp_ged_2023_near_camps.csv   UCDP GED 2023 events within 300 km of the camps (lat/lon)

Rasters (NLCD 2021, SRTM) are built by fetch_rasters_gee_week8.py.
Run from the repository root:  python scripts/build_lab_data_week8.py
"""
import io
import time
import warnings
import zipfile
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
W7 = ROOT / "notebook_data_week7"
OUT = ROOT / "notebook_data_week8"
VEC, TAB = OUT / "vector", OUT / "tables"
for d in (VEC, TAB):
    d.mkdir(parents=True, exist_ok=True)

FOCUS = {"41051": "Multnomah", "41005": "Clackamas", "41027": "Hood River", "41065": "Wasco",
         "53011": "Clark", "53059": "Skamania"}
PADUS = "https://services.arcgis.com/v01gqwM5QqNysAAi/arcgis/rest/services/Manager_Name_PADUS/FeatureServer/0/query"
PAD_FIELDS = ["OBJECTID", "Unit_Nm", "Category", "GAP_Sts", "IUCN_Cat", "Mang_Name", "Mang_Type",
              "Own_Name", "Des_Tp", "Date_Est", "State_Nm", "GIS_Acres"]
CAMPS = ("https://data.humdata.org/dataset/1a67eb3b-57d8-4062-b562-049ad62a85fd/resource/"
         "ace4b0a6-ef0f-46e4-a50a-8c552cfe7bf3/download/20230412_a1_camp_outlines.zip")
S = requests.Session()
S.headers["User-Agent"] = "GLBL570-teaching-data-build"


def write_shp(gdf, name):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        gdf.to_file(VEC / f"{name}.shp", encoding="UTF-8")


# ---------------------------------------------------------------- focus area (Week 7 counties)
counties = gpd.read_file(W7 / "vector" / "us_counties_geometry.shp")
focus = counties[counties["GEOID"].isin(FOCUS)][["GEOID", "STUSPS", "NAME", "ALAND", "AWATER", "geometry"]]
assert len(focus) == len(FOCUS), focus["GEOID"].tolist()
write_shp(focus, "focus_counties_pnw")
focus_4326 = focus.to_crs(4326)
bbox = ",".join(f"{v:.4f}" for v in focus_4326.total_bounds)

# ---------------------------------------------------------------- PAD-US 4.1 (paged, generalised to ~30 m)
pages, offset = [], 0
while True:
    for attempt in range(8):                                       # the service rate-limits large geometry requests (429)
        r = S.get(PADUS, timeout=600, params={
            "where": "Category <> 'Proclamation'", "geometry": bbox, "geometryType": "esriGeometryEnvelope",
            "inSR": 4326, "spatialRel": "esriSpatialRelIntersects", "outFields": ",".join(PAD_FIELDS),
            "maxAllowableOffset": 0.0003, "geometryPrecision": 6,   # GeoJSON output is in degrees: 0.0003° ≈ 25–33 m
            "resultOffset": offset, "resultRecordCount": 200, "orderByFields": "OBJECTID", "f": "geojson"})
        if r.ok and r.content.lstrip().startswith(b'{"type":"FeatureCollection"'):
            break
        wait = 15 * 2 ** min(attempt, 3)
        print(f"  page at offset {offset} refused ({r.text[:60]!r}); waiting {wait} s")
        time.sleep(wait)
    else:
        raise RuntimeError(f"PAD-US page at offset {offset} failed 8 times")
    page = gpd.read_file(io.BytesIO(r.content))
    if page.empty:
        break
    pages.append(page)
    offset += len(page)                                            # the server may return fewer than requested
    print(f"  PAD-US: {offset} features")
    time.sleep(2)                                                  # be polite to the public service
pad = pd.concat(pages, ignore_index=True).set_crs(4326, allow_override=True)
pad = pad[pad.geometry.notna() & ~pad.geometry.is_empty]
pad["geometry"] = pad.geometry.make_valid()
pad = gpd.clip(pad, focus_4326.union_all())                       # keep only the focus area
pad["geometry"] = pad.geometry.make_valid()                       # clipping can leave invalid rings
pad = pad.explode(index_parts=False)
pad = pad[pad.geom_type.isin(["Polygon", "MultiPolygon"])].dissolve(by="OBJECTID", as_index=False)
pad["Date_Est"] = pad["Date_Est"].astype(str).str.strip().replace({"None": "", "nan": ""})
write_shp(pad[PAD_FIELDS + ["geometry"]].rename(columns={"OBJECTID": "padus_oid"}), "padus41_mthood_gorge")

# ---------------------------------------------------------------- refugee camps (camp level only, no blocks)
r = S.get(CAMPS, timeout=600)
r.raise_for_status()
z = zipfile.ZipFile(io.BytesIO(r.content))
tmp = OUT / "_camps_tmp"
z.extractall(tmp)
camps = gpd.read_file(next(tmp.rglob("*.shp")))
camps = camps[["CampSSID", "CampName", "CampLabel", "Settlement", "Upazila", "Union", "AreaSqKM", "geometry"]]
# The source .prj is WGS 84 / UTM 46N plus a vertical CRS, which a Shapefile .prj cannot hold.
# Keep the horizontal part (EPSG:32646): coordinates are unchanged, nothing is reprojected.
assert camps.crs.name == "WGS 84 / UTM zone 46N" and 4e5 < camps.total_bounds[0] < 5e5, camps.crs
camps = camps.set_crs(32646, allow_override=True)
write_shp(camps, "coxsbazar_camps_2023")
for f in sorted(tmp.rglob("*"), reverse=True):
    f.unlink() if f.is_file() else f.rmdir()
tmp.rmdir()

# ---------------------------------------------------------------- UCDP events near the camps
ged = pd.read_csv(W7 / "tables" / "ucdp_ged_events_2023.csv")
pts = gpd.GeoDataFrame(ged, geometry=gpd.points_from_xy(ged.longitude, ged.latitude), crs=4326)
near = pts.to_crs(32646).distance(camps.to_crs(32646).union_all()) <= 300_000
sub = ged[near.values]
sub.to_csv(TAB / "ucdp_ged_2023_near_camps.csv", index=False)
(TAB / "ucdp_ged_2023_near_camps.csvt").write_text((W7 / "tables" / "ucdp_ged_events_2023.csvt").read_text())

for f in sorted(OUT.rglob("*")):
    if f.is_file():
        print(f"{f.relative_to(ROOT)}  {f.stat().st_size / 1e6:.2f} MB")
print(f"PAD-US features: {len(pad)} | camps: {len(camps)} | UCDP events near camps: {len(sub)}")
