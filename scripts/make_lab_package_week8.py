"""Assemble the self-contained Week 8 lab package: one root folder, one sub-folder per task, the lab guide and a
README at the root, then a ZIP for Canvas. Students need nothing from the Week 7 download.

Run from the repo root:  python scripts/make_lab_package_week8.py
Inputs:  lab_data/ (Week 7 pack), lab_data_week8/, plan/week8_memo_template_student.md, plan/week8_lab_package_README.md, GLBL570_Week8_Lab_Guide.pdf
Output:  GLBL570_Week8_Lab/  and  GLBL570_Week8_Lab.zip
"""
import shutil
import zipfile
from pathlib import Path

import rasterio

ROOT = Path(__file__).resolve().parents[1]
W7, W8 = ROOT / "lab_data", ROOT / "lab_data_week8"
PKG = ROOT / "GLBL570_Week8_Lab"
SHP = (".shp", ".shx", ".dbf", ".prj", ".cpg")

TASKS = {
    "Task1_Overlay": [W8 / "raster/focus_nlcd2021_30m.tif", W8 / "raster/nlcd_classes.csv",
                      W8 / "vector/padus41_mthood_gorge.shp", W8 / "vector/focus_counties_pnw.shp"],
    "Task2_Buffer": [W8 / "vector/coxsbazar_camps_2023.shp", W8 / "tables/ucdp_ged_2023_near_camps.csv"],
    "Task3_Image_Classification": [W8 / "raster/champaign_nlcd2021_30m.tif", W8 / "raster/nlcd_classes.csv",
                                   W8 / "vector/champaign_training_rois.gpkg", W8 / "vector/champaign_validation_rois.gpkg"],
    "Task4_Memo": [],
    "Extensions/A_Spatial_Statistics": [W7 / "vector/us_counties_acs2022.shp", W7 / "vector/us_counties_acs2022_field_dictionary.csv"],
    "Extensions/C_OSINT": [W7 / "tables/ucdp_ged_events_2023.csv", W7 / "vector/world_countries_ne110m.shp"],
}


def copy_with_sidecars(src: Path, dst_dir: Path) -> None:
    """Copy a file plus the files it cannot work without (.shp sidecars, .csvt type file)."""
    group = [src.with_suffix(s) for s in SHP] if src.suffix == ".shp" else [src, src.with_suffix(".csvt")]
    for f in group:
        if f.exists():
            shutil.copy2(f, dst_dir / f.name)
    assert (dst_dir / src.name).exists(), src


def split_bands(src: Path, dst_dir: Path, prefix: str) -> None:
    """One GeoTIFF per band: the SCP band set works best with single-band rasters."""
    dst_dir.mkdir(parents=True, exist_ok=True)
    names = {"B4_red": "B04_red", "B3_green": "B03_green", "B2_blue": "B02_blue", "B8_nir": "B08_nir"}
    with rasterio.open(src) as s:
        prof = s.profile | {"count": 1, "compress": "deflate", "predictor": 2}
        for k in range(1, s.count + 1):
            with rasterio.open(dst_dir / f"{prefix}_{names[s.descriptions[k - 1]]}.tif", "w", **prof) as out:
                out.write(s.read(k), 1)
                out.set_band_description(1, names[s.descriptions[k - 1]])


if PKG.exists():
    shutil.rmtree(PKG)
for task, files in TASKS.items():
    d = PKG / task
    d.mkdir(parents=True)
    for f in files:
        copy_with_sidecars(f, d)
split_bands(W7 / "raster/champaign_sentinel2_2023_10m.tif", PKG / "Task3_Image_Classification/summer_2023", "S2_summer")
split_bands(W8 / "raster/champaign_sentinel2_2023spring_10m.tif", PKG / "Task3_Image_Classification/spring_2023", "S2_spring")
shutil.copy2(ROOT / "plan/week8_memo_template_student.md", PKG / "Task4_Memo/week8_memo_template.md")   # blank: the notebook memo has the answers
shutil.copy2(ROOT / "GLBL570_Week8_Lab_Guide.pdf", PKG / "GLBL570_Week8_Lab_Guide.pdf")
shutil.copy2(ROOT / "plan/week8_lab_package_README.md", PKG / "README.md")

zpath = ROOT / "GLBL570_Week8_Lab.zip"
zpath.unlink(missing_ok=True)
with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(PKG.rglob("*")):
        if f.is_file():
            z.write(f, f.relative_to(ROOT))
n = sum(1 for f in PKG.rglob("*") if f.is_file())
print(f"{PKG.name}/: {n} files, {sum(f.stat().st_size for f in PKG.rglob('*') if f.is_file()) / 1e6:.1f} MB; "
      f"{zpath.name}: {zpath.stat().st_size / 1e6:.1f} MB")
