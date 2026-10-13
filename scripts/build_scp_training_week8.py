"""Ready-made training and validation areas for the Week 8 SCP image-classification task (Champaign–Urbana).

  lab_data_week8/raster/champaign_nlcd2021_30m.tif         NLCD 2021, native 30 m grid, Sentinel-2 scene extent
  lab_data_week8/raster/champaign_sentinel2_2023spring_10m.tif   Sentinel-2 L2A median Apr–May 2023, bands R,G,B,NIR,
                                                           on the same 10 m grid as the Week 7 summer scene
  lab_data_week8/vector/champaign_training_rois.gpkg       training polygons for SCP  (Import vector)
  lab_data_week8/vector/champaign_validation_rois.gpkg     separate polygons for SCP  (Postprocessing ▸ Accuracy)

Each polygon is a 90 m square (3 × 3 NLCD cells, 9 × 9 Sentinel-2 pixels) whose nine NLCD cells all belong to the same
macroclass, so no polygon straddles a class boundary. Fields follow the SCP v8 import convention:
macroclass_id, macroclass_name, class_id, class_name. Training and validation squares are at least 300 m apart.
The script also trains a random forest on the training squares (the same thing SCP does) and prints the accuracy on the
validation squares, which the lab guide quotes as the self-check.

Why a spring scene: in a Jun–Sep composite, crops and forest are both dense green canopy and the four bands barely
separate them (validation accuracy 0.66). In April–May the fields are bare soil; adding that date raises accuracy to ~0.81.

Needs an Earth Engine key for steps 1 and 1b: GEE_KEY (path to JSON) and GEE_PROJECT. Run from the repo root.
"""
import io
import os
from pathlib import Path

import ee
import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
import requests
from google.oauth2 import service_account
from scipy import ndimage
from shapely.geometry import box
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

ROOT = Path(__file__).resolve().parents[1]
S2 = ROOT / "lab_data" / "raster" / "champaign_sentinel2_2023_10m.tif"
OUT_R, OUT_V = ROOT / "lab_data_week8" / "raster", ROOT / "lab_data_week8" / "vector"
NLCD30 = OUT_R / "champaign_nlcd2021_30m.tif"
SPRING = OUT_R / "champaign_sentinel2_2023spring_10m.tif"
NLCD_X0, NLCD_Y0, RES = -2493045.0, 3310005.0, 30.0            # CONUS NLCD 30 m grid origin (EPSG:5070)
MACRO = {1: ("Water", [11]), 2: ("Developed", [22, 23, 24]), 3: ("Forest", [41, 42, 43]),
         4: ("Grass and pasture", [71, 81]), 5: ("Cropland", [82])}
N_TRAIN, N_VAL, MIN_SEP = 40, 30, 300.0
rng = np.random.default_rng(570)

# ---------------------------------------------------------------- 1. NLCD 30 m for the scene extent
with rasterio.open(S2) as s2:
    b = s2.bounds
xmin = NLCD_X0 + np.floor((b.left - NLCD_X0) / RES) * RES
xmax = NLCD_X0 + np.ceil((b.right - NLCD_X0) / RES) * RES
ymax = NLCD_Y0 + np.ceil((b.top - NLCD_Y0) / RES) * RES
ymin = NLCD_Y0 + np.floor((b.bottom - NLCD_Y0) / RES) * RES
w, h = int(round((xmax - xmin) / RES)), int(round((ymax - ymin) / RES))
if not NLCD30.exists():
    cred = service_account.Credentials.from_service_account_file(
        os.environ["GEE_KEY"], scopes=["https://www.googleapis.com/auth/earthengine"])
    ee.Initialize(cred, project=os.environ["GEE_PROJECT"])
    img = (ee.ImageCollection("USGS/NLCD_RELEASES/2021_REL/NLCD").filter(ee.Filter.eq("system:index", "2021"))
           .first().select("landcover"))
    props = img.getInfo()["properties"]
    cmap = {int(v): tuple(int(p[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
            for v, p in zip(props["landcover_class_values"], props["landcover_class_palette"])}
    url = img.unmask(0).toUint8().getDownloadURL({"crs": "EPSG:5070", "dimensions": f"{w}x{h}", "format": "GEO_TIFF",
                                                  "crs_transform": [RES, 0, xmin, 0, -RES, ymax]})
    resp = requests.get(url, timeout=600); resp.raise_for_status()
    with rasterio.open(io.BytesIO(resp.content)) as src:
        data = src.read(1)
    prof = dict(driver="GTiff", width=w, height=h, count=1, dtype="uint8", crs="EPSG:5070", nodata=0,
                transform=rasterio.Affine(RES, 0, xmin, 0, -RES, ymax), compress="deflate")
    with rasterio.open(NLCD30, "w", **prof) as dst:
        dst.write(data, 1); dst.write_colormap(1, cmap); dst.set_band_description(1, "nlcd_class")
# ---------------------------------------------------------------- 1b. spring Sentinel-2 composite on the summer grid
if not SPRING.exists():
    cred = service_account.Credentials.from_service_account_file(
        os.environ["GEE_KEY"], scopes=["https://www.googleapis.com/auth/earthengine"])
    ee.Initialize(cred, project=os.environ["GEE_PROJECT"])
    with rasterio.open(S2) as s2:
        prof, W, H, t2 = s2.profile.copy(), s2.width, s2.height, s2.transform
    aoi = ee.Geometry.Rectangle([-88.4, 39.95, -88.1, 40.25])
    spring = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(aoi).filterDate("2023-04-01", "2023-05-31")
              .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20)).median().select(["B4", "B3", "B2", "B8"]).toUint16())
    data = np.zeros((4, H, W), dtype="uint16")
    for r0 in range(0, H, 1000):                                  # tiles keep each request under the EE size limit
        for c0 in range(0, W, 1000):
            tw, th = min(1000, W - c0), min(1000, H - r0)
            url = spring.getDownloadURL({"crs": "EPSG:5070", "dimensions": f"{tw}x{th}", "format": "GEO_TIFF",
                                         "crs_transform": [10, 0, t2.c + c0 * 10, 0, -10, t2.f - r0 * 10]})
            resp = requests.get(url, timeout=600); resp.raise_for_status()
            with rasterio.open(io.BytesIO(resp.content)) as src:
                data[:, r0:r0 + th, c0:c0 + tw] = src.read()
    prof.update(compress="deflate", predictor=2)
    with rasterio.open(SPRING, "w", **prof) as dst:
        dst.write(data)
        for k, d in enumerate(["B4_red", "B3_green", "B2_blue", "B8_nir"], 1):
            dst.set_band_description(k, d)
    print(f"{SPRING.name}: {W}x{H}, {SPRING.stat().st_size / 1e6:.1f} MB")

with rasterio.open(NLCD30) as src:
    nlcd, tf = src.read(1), src.transform
print(f"{NLCD30.name}: {nlcd.shape[1]}x{nlcd.shape[0]} cells; classes {dict(zip(*np.unique(nlcd, return_counts=True)))}")

# ---------------------------------------------------------------- 2. homogeneous 3 x 3 squares per macroclass
macro = np.zeros_like(nlcd)
for mid, (_, codes) in MACRO.items():
    macro[np.isin(nlcd, codes)] = mid
labels = pd.read_csv(ROOT / "lab_data" / "raster" / "nlcd_classes.csv").set_index("value").label.to_dict()
rows = []
for mid, (mname, _) in MACRO.items():
    same = ndimage.minimum_filter((macro == mid).astype(np.uint8), size=3, mode="constant") == 1
    same[[0, -1], :] = False; same[:, [0, -1]] = False
    rr, cc = np.nonzero(same)
    order = rng.permutation(len(rr))
    picked = []
    for k in order:                                               # spread the squares out: >= MIN_SEP between any two
        x, y = tf * (cc[k] + 0.5, rr[k] + 0.5)
        if all((x - px) ** 2 + (y - py) ** 2 >= MIN_SEP ** 2 for px, py, *_ in picked):
            picked.append((x, y, rr[k], cc[k]))
        if len(picked) == N_TRAIN + N_VAL:
            break
    print(f"  {mname}: {len(rr):,} homogeneous cells -> {len(picked)} squares")
    for n, (x, y, r, c) in enumerate(picked):
        code = int(nlcd[r, c])
        rows.append({"macroclass_id": mid, "macroclass_name": mname, "class_id": code, "class_name": labels[code],
                     "set": "training" if n < min(N_TRAIN, int(len(picked) * 4 / 7)) else "validation",
                     "geometry": box(x - 1.5 * RES, y - 1.5 * RES, x + 1.5 * RES, y + 1.5 * RES)})
roi = gpd.GeoDataFrame(rows, crs="EPSG:5070")
for name in ("training", "validation"):
    out = OUT_V / f"champaign_{name}_rois.gpkg"
    out.unlink(missing_ok=True)
    roi[roi.set == name].drop(columns="set").reset_index(drop=True).to_file(out, layer=f"{name}_rois", driver="GPKG")
    print(f"{out.name}: {(roi.set == name).sum()} polygons", roi[roi.set == name].macroclass_name.value_counts().to_dict())

# ---------------------------------------------------------------- 3. self-check: random forest as SCP runs it
from rasterio.features import rasterize
with rasterio.open(S2) as src:
    summer, s2tf, shape = src.read().astype("float32"), src.transform, (src.height, src.width)
with rasterio.open(SPRING) as src:
    spring = src.read().astype("float32")


def label_raster(gdf):
    return rasterize(((g, m) for g, m in zip(gdf.geometry, gdf.macroclass_id)), out_shape=shape, transform=s2tf,
                     fill=0, dtype="uint8")


Ltr, Lva = label_raster(roi[roi.set == "training"]), label_raster(roi[roi.set == "validation"])
names = [MACRO[m][0] for m in sorted(MACRO)]
for tag, stack in [("Run 1 · summer only (4 bands)", summer), ("Run 2 · summer + spring (8 bands)", np.concatenate([summer, spring]))]:
    rf = RandomForestClassifier(n_estimators=100, random_state=570, n_jobs=-1).fit(stack[:, Ltr > 0].T, Ltr[Ltr > 0])
    y, pred = Lva[Lva > 0], rf.predict(stack[:, Lva > 0].T)
    cm = confusion_matrix(y, pred, labels=sorted(MACRO))
    print(f"\n{tag}: {int((Ltr > 0).sum()):,} training px, {len(y):,} validation px, overall accuracy {accuracy_score(y, pred):.3f}")
    print(pd.DataFrame(cm, index=[f"true {n}" for n in names], columns=names).to_string())
    print("recall:", {n: round(cm[i, i] / cm[i].sum(), 2) for i, n in enumerate(names)})
    full = rf.predict(stack.reshape(stack.shape[0], -1).T)
    print("share of scene:", {MACRO[m][0]: f"{100 * np.mean(full == m):.0f}%" for m in sorted(MACRO)})
