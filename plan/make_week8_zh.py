"""After the English notebook has been executed: write the Chinese review copy and clean the English one.

Every markdown cell built by build_week8_notebook.py carries its Chinese text in metadata["zh"]. The Chinese copy
uses that text; code cells and their outputs are copied unchanged. The metadata is then removed from the English file.
Run from the repo root:  python plan/make_week8_zh.py
"""
import copy
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
EN = ROOT / "GLBL570_Week8_Spatial_Analysis_Lab.ipynb"
ZH = ROOT / "GLBL570_Week8_Spatial_Analysis_Lab_zh.ipynb"

en = nbf.read(EN, 4)
zh = copy.deepcopy(en)
for ce, cz in zip(en.cells, zh.cells):
    if ce.cell_type == "markdown":
        assert "zh" in ce.metadata, ce.source[:60]
        cz.source = ce.metadata.pop("zh")
        cz.metadata.pop("zh", None)
nbf.write(zh, ZH)
nbf.write(en, EN)
n_md = sum(c.cell_type == "markdown" for c in en.cells)
print(f"wrote {ZH.name}: {n_md} markdown cells in Chinese, {len(en.cells) - n_md} code cells copied with outputs")
