"""Download the Week 8 rasters for the Mt Hood / Columbia Gorge focus area from Google Earth Engine.

  notebook_data_week8/raster/focus_nlcd2021_30m.tif   NLCD 2021 land cover, raw class codes, uint8 + colour table,
                                                 on the native NLCD 30 m grid (EPSG:5070)
  notebook_data_week8/raster/focus_srtm_90m.tif       SRTM elevation (m), int16, 90 m, EPSG:5070
  notebook_data_week8/raster/nlcd_classes.csv         value -> label table (value attribute table)

Needs an Earth Engine service-account key: set GEE_KEY (path to JSON) and GEE_PROJECT.
Run after build_lab_data_week8.py, from the repository root:  python scripts/fetch_rasters_gee_week8.py
"""
import csv
import io
import os
from pathlib import Path

import ee
import geopandas as gpd
import numpy as np
import rasterio
import requests
from google.oauth2 import service_account
from rasterio.features import geometry_mask

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebook_data_week8" / "raster"
OUT.mkdir(parents=True, exist_ok=True)
CRS = "EPSG:5070"
NLCD_X0, NLCD_Y0 = -2493045.0, 3310005.0                 # origin of the CONUS NLCD 30 m grid (EPSG:5070)

cred = service_account.Credentials.from_service_account_file(
    os.environ["GEE_KEY"], scopes=["https://www.googleapis.com/auth/earthengine"])
ee.Initialize(cred, project=os.environ["GEE_PROJECT"])

focus = gpd.read_file(ROOT / "notebook_data_week8" / "vector" / "focus_counties_pnw.shp").to_crs(CRS)
area = focus.union_all()


def aligned_grid(bounds, res, x0=0.0, y0=0.0):
    xmin = x0 + np.floor((bounds[0] - x0) / res) * res
    xmax = x0 + np.ceil((bounds[2] - x0) / res) * res
    ymin = y0 + np.floor((bounds[1] - y0) / res) * res
    ymax = y0 + np.ceil((bounds[3] - y0) / res) * res
    return float(xmin), float(ymax), int(round((xmax - xmin) / res)), int(round((ymax - ymin) / res))


def fetch(img, res, name, dtype, nodata, x0=0.0, y0=0.0, tile=3000, colormap=None, description=None):
    xmin, ymax, w, h = aligned_grid(area.bounds, res, x0, y0)
    data = np.full((h, w), nodata, dtype=dtype)
    for r0 in range(0, h, tile):                         # tiles keep each request under the EE size limit
        for c0 in range(0, w, tile):
            tw, th = min(tile, w - c0), min(tile, h - r0)
            url = img.getDownloadURL({"crs": CRS, "dimensions": f"{tw}x{th}", "format": "GEO_TIFF",
                                      "crs_transform": [res, 0, xmin + c0 * res, 0, -res, ymax - r0 * res]})
            resp = requests.get(url, timeout=900)
            if not resp.ok:
                raise RuntimeError(f"{name} tile ({r0},{c0}): HTTP {resp.status_code}: {resp.text[:300]}")
            with rasterio.open(io.BytesIO(resp.content)) as src:
                data[r0:r0 + th, c0:c0 + tw] = src.read(1).astype(dtype)
    transform = rasterio.Affine(res, 0, xmin, 0, -res, ymax)
    data[geometry_mask([area], out_shape=(h, w), transform=transform)] = nodata      # outside the focus area
    profile = dict(driver="GTiff", width=w, height=h, count=1, dtype=dtype, crs=CRS, transform=transform,
                   nodata=nodata, compress="deflate", predictor=1 if dtype == "uint8" else 2,
                   tiled=True, blockxsize=256, blockysize=256)
    with rasterio.open(OUT / name, "w", **profile) as dst:
        dst.write(data, 1)
        if colormap:
            dst.write_colormap(1, colormap)
        if description:
            dst.set_band_description(1, description)
        dst.build_overviews([2, 4, 8, 16], rasterio.enums.Resampling.nearest if colormap
                            else rasterio.enums.Resampling.average)
    print(f"{name}: {w}x{h} {dtype}  {(OUT / name).stat().st_size / 1e6:.1f} MB")


# 1. NLCD 2021 on its native 30 m grid: raw class codes (do NOT pre-collapse to forest / non-forest)
nlcd = (ee.ImageCollection("USGS/NLCD_RELEASES/2021_REL/NLCD")
        .filter(ee.Filter.eq("system:index", "2021")).first().select("landcover"))
info = nlcd.getInfo()["properties"]
values, palette, names = info["landcover_class_values"], info["landcover_class_palette"], info["landcover_class_names"]
cmap = {int(v): tuple(int(p[i:i + 2], 16) for i in (0, 2, 4)) + (255,) for v, p in zip(values, palette)}
cmap[0] = (0, 0, 0, 0)
fetch(nlcd.unmask(0).toUint8(), 30.0, "focus_nlcd2021_30m.tif", "uint8", 0, NLCD_X0, NLCD_Y0,
      colormap=cmap, description="nlcd_class")
with open(OUT / "nlcd_classes.csv", "w", newline="") as fh:
    csv.writer(fh).writerows([("value", "label")] + [(v, n.split(":")[0].strip()) for v, n in zip(values, names)])

# 2. SRTM elevation, 90 m (only used for 5 km summaries)
dem = ee.Image("USGS/SRTMGL1_003").select("elevation").resample("bilinear")
fetch(dem.unmask(-32768).toInt16(), 90.0, "focus_srtm_90m.tif", "int16", -32768, description="elevation_m")
