"""Bilingual "reading the figure" cells for the Week 8 notebook.

READS: (marker, english, chinese) — the markdown cell is inserted right after the code cell whose source contains `marker`.
Numbers come from the seeded run (RNG 570); build_week8_notebook.py checks them against the executed outputs.
"""

INTRO_22_EN = r"""
### 2.2 The six operations on two simple shapes (slide 12)
Before the real data, two toy layers with **one feature each** and their own attribute tables:

| Layer | Shape in the figure | Stands for | Attribute table |
|---|---|---|---|
| **A — input** | blue dashed **square** (2 × 2 units) | a forest stand | `A_name` = "forest stand", `A_ha` = 400 |
| **B — overlay** | amber dashed **circle** covering A's right half | a nature reserve | `B_zone` = "reserve", `B_gap` = 1 (GAP status) |

Each panel applies one operation to A and B. The **teal area is the geometry of the result**; the grey line under each panel lists the **columns of the result's attribute table**. The cell prints both input tables first and every result table after the figure.
"""
INTRO_22_ZH = r"""
### 2.2 用两个简单图形演示六种操作（第 12 页）
在用真实数据之前，先看两个示意图层，**每层只有一个要素**，各自带一张属性表：

| 图层 | 图中的形状 | 代表什么 | 属性表 |
|---|---|---|---|
| **A —— 输入图层** | 蓝色虚线**正方形**（2 × 2 单位） | 一块林地 | `A_name` = "forest stand"，`A_ha` = 400（公顷） |
| **B —— 叠加图层** | 橙色虚线**圆形**，盖住 A 的右半部分 | 一个自然保护区 | `B_zone` = "reserve"，`B_gap` = 1（GAP 保护等级） |

每个小图对 A 和 B 做一种操作。**青色区域是结果的几何形状**；每个小图下方的灰色文字列出**结果属性表中有哪些列**。这个单元格会先打印两个输入属性表，画图之后再打印六种结果的属性表。
"""

READS = [
("lag = W @ x", r"""
**Reading the figure**
- **Data:** % of residents below the poverty line (ACS 2018–2022) for the **3,107 counties of the contiguous United States** (48 states + DC). Nantucket MA and San Juan WA are dropped because, as islands, they touch no other county.
- **What we did:**
  - **(a)** maps the real rates in five equal-count classes (quintiles).
  - **The shuffle test (slide 9):** keep all 3,107 rates but hand them to the counties in random order — the same numbers with the geography removed. **(b)** maps one such shuffle with the same colours.
  - **(c)** compares the two maps' histograms; **(d)** plots each county's rate against the **average rate of the counties it touches** (the *spatial lag*; neighbours share an edge or a corner, "queen" rule) for both maps; **(e)** repeats the shuffle 999 times and records r each time.
- **What it shows:**
  - **(a) vs (b) — the eye sees it at once.** The real map has large, solid regions: high poverty across the Mississippi Delta and the Deep South, Appalachian Kentucky, the Rio Grande border of Texas and New Mexico, and Native American reservations in South Dakota and the Southwest; low poverty across the Upper Midwest and around big East-Coast metros. The shuffled map is salt-and-pepper with no regions.
  - **(c) cannot tell them apart:** the two histograms coincide bar for bar. A histogram, mean or median (here 1.6–55.8 %, median 13.4 %) is non-spatial.
  - **(d) and (e) can:** on the real map a county's rate and its neighbours' average are clearly related (**r = 0.67**); on the shuffled map the relationship disappears (r = 0.03). Across 999 shuffles r never exceeded 0.08 — **none came close to 0.67**. Poverty in the U.S. is strongly spatially autocorrelated: where a county is tells you a lot about its rate.
  - §4.1 measures the same thing with the standard statistic, Moran's I, and finds which counties form the clusters.
""", r"""
**读图说明**
- **数据：** **美国本土 3,107 个县**（48 州加华盛顿特区）的贫困率（贫困线以下人口占比，ACS 2018–2022）。马萨诸塞州的楠塔基特县和华盛顿州的圣胡安县是海岛，不与任何县相邻，因此被剔除。
- **做了什么：**
  - **(a)** 把真实贫困率按五分位（每一档县数相同）上色。
  - **随机打乱检验（课件第 9 页）：** 3,107 个数值不变，但随机分配给各县——数值完全相同、地理位置被打乱的"假地图"。**(b)** 用相同配色画出打乱一次后的地图。
  - **(c)** 比较两张地图的直方图；**(d)** 对两张地图分别画"每个县的贫困率 vs **与它相邻各县的平均贫困率**"（即"空间滞后"；邻接按 queen 规则：共边或共点即为邻居）；**(e)** 打乱 999 次，每次记录 r。
- **结论：**
  - **(a) 和 (b) 一眼就能分出来。** 真实地图上有成片的区域：密西西比三角洲和南方腹地、肯塔基州的阿巴拉契亚山区、得克萨斯和新墨西哥的格兰德河边境、南达科他州和西南部的印第安保留地是成片的高贫困区；中西部北部（明尼苏达、艾奥瓦、内布拉斯加等）和东海岸大城市周边是成片的低贫困区。打乱后的地图则像撒了一把椒盐，看不出任何区域。
  - **(c) 分不出来：** 两个直方图逐条重合。直方图、均值、中位数（这里 1.6%–55.8%，中位数 13.4%）都是非空间统计。
  - **(d) 和 (e) 分得出来：** 真实地图上，一个县的贫困率和邻居的平均贫困率明显相关（**r = 0.67**）；打乱后这种关系消失（r = 0.03）。999 次打乱中 r 最大也只有 0.08——**没有一次接近 0.67**。美国的贫困具有很强的空间自相关：知道一个县在哪里，就能对它的贫困率猜个大概。
  - §4.1 用标准统计量 Moran's I 衡量同一件事，并找出是哪些县构成了这些聚集区。
"""),
('save(fig, "overlay_operations.png"', r"""
**Reading the figure**
- **Data:** the two toy layers in the table above — A, a square forest stand (`A_name`, `A_ha`); B, a circular reserve (`B_zone`, `B_gap`) overlapping A's right half. Not real places.
- **What we did:** applied each operation to A and B with GeoPandas (`gpd.clip`, `gpd.overlay(how=...)`) and drew the result in teal; the printout above lists every result's rows and values.
- **What it shows:** **Clip and Intersect produce the same half-disc** (where A and B overlap), but Clip's table has only A's columns while Intersect's has A's *and* B's — only Intersect can tell you which reserve, and which GAP status, a piece of forest falls in. **Erase** keeps the part of A outside B. **Union** keeps everything, cut into pieces at every edge (B's columns are empty where only A exists, and vice versa). **Identity** keeps all of A, split where B covers it. **Update** keeps A outside B and replaces the overlap with B — shape *and* attributes — so the result also covers B's part outside A.
""", r"""
**读图说明**
- **数据：** 上表中的两个示意图层——A 是正方形林地（属性 `A_name`、`A_ha`），B 是盖住 A 右半部分的圆形保护区（属性 `B_zone`、`B_gap`）。它们不是真实地点。
- **做了什么：** 用 GeoPandas（`gpd.clip`、`gpd.overlay(how=...)`）对 A 和 B 分别执行六种操作，结果画成青色；上方打印出每种结果的行和属性值。
- **结论：** **Clip 和 Intersect 得到的形状完全相同**（A 与 B 重叠的半圆），但 Clip 的属性表只有 A 的列，Intersect 则同时有 A 和 B 的列——只有 Intersect 能告诉你一块林地落在哪个保护区、属于哪个 GAP 等级。**Erase** 保留 A 在 B 以外的部分。**Union** 保留全部区域，并在每条边界处切开（只有 A 的地方 B 的列为空，反之亦然）。**Identity** 保留 A 的全部，并在被 B 覆盖处切开。**Update（更新）** 保留 A 在 B 以外的部分，把重叠部分换成 B——几何和属性都换——所以结果也包括 B 在 A 以外的部分。
"""),
('print(f"inputs: {len(Acty)} counties', r"""
**Reading the table**
- **Data:** A = the 6 focus counties (columns `NAME`, `STUSPS`); B = the 360 PAD-US units with GAP status 1–2 (columns `Unit_Nm`, `GAP`, `Mang_Name`).
- **What we did:** ran the same six operations on the real layers and recorded the number of output rows, their total area and their columns.
- **What it shows:** **Clip** returns 6 rows — one clipped piece per county — with county columns only (2,085 km²). **Intersect** returns 382 rows, one per county × protected-unit piece, and each piece now knows its unit, GAP status and manager. Intersect's area (2,474 km²) is *larger* than Clip's because PAD-US units overlap and every overlapping unit contributes its own piece; the same overlap pushes Union's area (20,116 km²) above the focus area (19,726 km²). §3.3 removes this with Dissolve. **Erase** gives the 17,642 km² of county land outside strict protection.
""", r"""
**读表说明**
- **数据：** A = 6 个聚焦县（列：`NAME`、`STUSPS`）；B = GAP 等级为 1–2 的 360 个 PAD-US 保护单元（列：`Unit_Nm`、`GAP`、`Mang_Name`）。
- **做了什么：** 在真实图层上执行同样的六种操作，记录输出的行数、总面积和列。
- **结论：** **Clip** 输出 6 行（每个县一个被裁剪的部分），只有县的列（2,085 km²）。**Intersect** 输出 382 行，每行是"县 × 保护单元"的一个片段，并且每个片段都带上了所属保护单元、GAP 等级和管理机构。Intersect 的面积（2,474 km²）*大于* Clip，是因为 PAD-US 保护单元互相重叠，每个重叠的单元都会生成自己的片段；同样的原因使 Union 的面积（20,116 km²）超过了聚焦区总面积（19,726 km²）。§3.3 用 Dissolve 解决这个问题。**Erase** 得到严格保护区以外的 17,642 km² 县域土地。
"""),
('save(fig, "overlay_policy_forest_protected.png"', r"""
**Reading the figure**
- **Data:** *(a) Input A, raster:* NLCD 2021 land cover, 30 m; forest = classes 41–43 (deciduous, evergreen, mixed), 9,860 km², converted to polygons. The inset shows where the six counties lie. *(b) Input B, vector:* the 3,043 PAD-US 4.1 units in the six counties, each with a **GAP status** (USGS Gap Analysis Project) — **1** wilderness left to natural processes (Mount Hood, Mark O. Hatfield, Salmon-Huckleberry wildernesses); **2** managed for biodiversity (White River Wildlife Area, wild-and-scenic river corridors); **3** protected from conversion but open to logging, grazing and mining (Mt. Hood and Gifford Pinchot national forests, the Columbia Gorge Scenic Area); **4** no known protection mandate.
- **What we did:** dissolved the units into a strict layer (GAP 1–2) and a broad one (GAP 1–3); **Intersect**ed the forest with each and **Erase**d it from each. *(c)* colours every piece of forest by the strongest protection it falls under; *(d)* gives the areas, with the bar colours matching *(c)*.
- **What it shows:** compare (b) and (c): the dark-green wilderness patches in (b) are the only places where the forest in (c) is dark green — **1,377 km², 14.0 % of the forest**. The light-green national forests that cover most of (b) add 5,855 km², taking the total to **7,232 km², 73.3 %**. The tan forest in (c) lies outside every GAP 1–3 unit — mainly in Clackamas (831 km²), Wasco (687 km²) and Clark (469 km²) — on land PAD-US does not record as GAP 1–3 (private, tribal, state or local land, or GAP 4). The "conservation gap" is 86 % or 27 % of the forest depending on one definition — a policy choice, not a GIS output (§6.1).
""", r"""
**读图说明**
- **数据：** *(a) 输入 A，栅格*：NLCD 2021 土地覆盖，30 m；森林 = 41–43 类（落叶林、常绿林、混交林），共 9,860 km²，已转为多边形。左上角小图标出这六个县的位置。*(b) 输入 B，矢量*：六个县内的 3,043 个 PAD-US 4.1 保护地单元，每个都有 **GAP 等级**（美国地质调查局 Gap Analysis Project）——**1** 荒野区，任其自然演替（胡德山、马克·哈特菲尔德、萨蒙-哈克尔贝里荒野区）；**2** 以生物多样性为管理目标（白河野生动物区、"荒野与风景河流"河道）；**3** 禁止改变用途，但允许采伐、放牧、采矿（胡德山和吉福德·平肖国家森林、哥伦比亚河峡谷国家风景区）；**4** 没有已知的保护要求。
- **做了什么：** 把保护单元融合成严格图层（GAP 1–2）和宽泛图层（GAP 1–3）；分别与森林做 **Intersect**，并从森林中 **Erase**。*(c)* 按每块森林所处的最高保护等级上色；*(d)* 给出面积，柱子颜色与 *(c)* 一致。
- **结论：** 对照 (b) 和 (c)：(b) 中深绿色的荒野区，正是 (c) 中森林呈深绿色的地方——**1,377 km²，占森林 14.0%**。覆盖 (b) 大部分面积的浅绿色国家森林又增加了 5,855 km²，合计 **7,232 km²，73.3%**。(c) 中浅棕色的森林不在任何 GAP 1–3 单元内——主要在克拉克马斯（831 km²）、沃斯科（687 km²）和克拉克（469 km²）——PAD-US 没有把这些土地记为 GAP 1–3（可能是私有、部落、州或地方土地，或 GAP 4）。"保护缺口"按一种定义是森林的 86%，按另一种是 27%——这是政策选择，不是 GIS 的输出（§6.1）。
"""),
('save(fig, "distance_to_water_development.png"', r"""
**Reading the figure**
- **Data:** NLCD 2021 at 30 m for the focus area; *water* = class 11, *developed* = classes 21–24.
- **What we did:** computed for every land cell its straight-line distance to the nearest water cell (left map, capped at 5 km), grouped the cells into 7 distance bands, and computed the share developed in each band (right, and the table above).
- **What it shows:** development **peaks 100–250 m from water (17.7 %) and falls steadily to 3.2 % beyond 5 km**. The 0–100 m band is lower (7.7 %) because river banks, floodplains and wetlands are rarely built on. Developed land is closer to water than land in general (median 1.76 km vs 2.81 km). This is an association, not a cause — see the CANNOT ESTABLISH line.
""", r"""
**读图说明**
- **数据：** 聚焦区 30 m 分辨率的 NLCD 2021；*水体* = 第 11 类，*已开发用地* = 第 21–24 类。
- **做了什么：** 为每个陆地像元计算到最近水体像元的直线距离（左图，超过 5 km 按 5 km 显示），把像元分成 7 个距离段，计算每段中已开发用地的比例（右图及上方表格）。
- **结论：** 开发比例**在离水 100–250 m 处最高（17.7%），之后逐步下降，到 5 km 以外只有 3.2%**。0–100 m 段较低（7.7%），因为河岸、洪泛区和湿地很少被开发。已开发用地比一般土地更靠近水体（中位距离 1.76 km 对 2.81 km）。这只是关联，不是因果——见 CANNOT ESTABLISH 一行。
"""),
("share3 = [", r"""
**Reading the table**
- **Data:** 33 camp outlines (26 in Ukhia, 7 in Teknaf) and 410 UCDP 2023 events within 300 km (399 in Myanmar, 10 in Bangladesh, 1 in India).
- **What we did:** measured, in metres (UTM 46N), the distance from every camp polygon to every event; then, for each radius, counted the share of camps with at least 1 — or at least 3 — events within that radius.
- **What it shows:** the median camp is **0.8 km from its nearest event** and 2.4 km from its third-nearest: several 2023 events were recorded in or right next to the camps. Restricting to precisely located events (UCDP `where_prec` ≤ 2) gives exactly the same shares.
""", r"""
**读表说明**
- **数据：** 33 个难民营边界（乌基亚 26 个、特克纳夫 7 个），以及 300 km 范围内的 410 起 UCDP 2023 冲突事件（缅甸 399 起、孟加拉国 10 起、印度 1 起）。
- **做了什么：** 在以米为单位的坐标系（UTM 46N）中，计算每个营地多边形到每个事件的距离；再对每个半径，统计半径内至少有 1 起（或至少 3 起）事件的营地占比。
- **结论：** 营地到最近事件的距离中位数是 **0.8 km**，到第三近事件是 2.4 km：2023 年有多起事件发生在营地内或紧邻营地处。只保留定位精确的事件（UCDP `where_prec` ≤ 2）后，各比例完全不变。
"""),
('save(fig, "buffer_sensitivity.png"', r"""
**Reading the figure**
- **Data:** as above; the map zooms on the camps and the Bangladesh–Myanmar border.
- **What we did:** *Left* — buffers of 5, 10 and 25 km around every event (darker = closer), camps in red. *Right* — the share of the 33 camps counted "near conflict" at seven radii — 1, 2, 5, 10, 25, 50 and 100 km — under two rules (≥ 1 event, ≥ 3 events within the radius). The tick labels are ordinary kilometres; only the spacing is logarithmic (each step multiplies the radius rather than adding to it), so the short radii, where the share changes fastest, are not squeezed into the left edge.
- **What it shows:** two choices move the answer, and they are separate:
  - **The radius.** Under the "≥ 1 event" rule (red line), 64 % of camps are "near conflict" at 1 km, 79 % at 2 km, 97 % at 5 km, and all of them from 10 km on.
  - **The rule.** Under the stricter "≥ 3 events" rule (blue line) the curve is lower at every radius and reaches 100 % only at 25 km. Read the two lines at the **same** radius to see the effect of the rule alone: at 1 km 64 % vs 27 %; at 5 km 97 % vs 76 %; at 10 km 100 % vs 85 %. From 25 km on both rules give 100 %, so they no longer separate the camps at all.
  - So "how many camps are at risk?" has no single answer: it ranges from 27 % to 100 % depending on the radius *and* the rule. The memo must state and justify both.
""", r"""
**读图说明**
- **数据：** 同上；地图放大到营地和孟加拉国—缅甸边境一带。
- **做了什么：** *左图*——围绕每起事件画 5、10、25 km 缓冲区（颜色越深越近），红色是营地。*右图*——在 1、2、5、10、25、50、100 km 七个半径下，33 个营地中被算作"靠近冲突"的比例，分两种规则：半径内至少 1 起事件、至少 3 起事件。横轴刻度上的数字就是普通的公里数，只是刻度**间距**按对数排列（每往右一格，半径是乘上一个倍数而不是加上一个固定值），这样比例变化最快的小半径段（1–10 km）不会被挤在左边。
- **结论：** 有两个选择会改变答案，而且是两件不同的事：
  - **半径。** 按"至少 1 起事件"的规则（红线），半径 1 km 时 64% 的营地"靠近冲突"，2 km 时 79%，5 km 时 97%，10 km 及以上全部营地都算。
  - **规则。** 按更严格的"至少 3 起事件"规则（蓝线），每个半径下的比例都更低，要到 25 km 才达到 100%。在**同一半径**下比较两条线，才能单独看出规则的影响：1 km 时 64% 对 27%；5 km 时 97% 对 76%；10 km 时 100% 对 85%。25 km 及以上两种规则都是 100%，已经完全区分不出营地之间的差别。
  - 所以"有多少营地处于风险中"没有唯一答案：取决于半径**和**规则，从 27% 到 100% 都有可能。备忘录必须写明并论证这两个选择。
"""),
('save(fig, "proximity_toolbox.png"', r"""
**Reading the figure**
- **Data:** one point per camp — a representative point inside each of the 33 camp outlines (outlines in grey).
- **What we did:** three proximity tools on the same points: a single 800 m buffer; rings at 400, 800 and 1,600 m; and Thiessen (Voronoi) polygons, which assign every location to its nearest camp centre.
- **What it shows:** in the dense northern cluster (Ukhia) the buffers merge into one zone and the Thiessen cells are small and cut across the camp outlines themselves; around the scattered southern camps (Teknaf) the cells become very large. The "nearest centre" rule ignores the real boundaries people live within.
""", r"""
**读图说明**
- **数据：** 每个营地取一个点——33 个营地边界（灰色）内各取一个代表点。
- **做了什么：** 对同一组点使用三种邻近工具：单一 800 m 缓冲区；400、800、1,600 m 的多环缓冲区；泰森（Voronoi）多边形，即把每个位置分配给离它最近的营地中心。
- **结论：** 在北部密集的营地群（乌基亚）中，缓冲区连成一片，泰森多边形很小，而且会穿过营地边界本身；在南部分散的营地（特克纳夫）周围，多边形变得非常大。"离最近中心"的规则忽略了人们实际生活所在的边界。
"""),
('save(fig, "data_preprocessing_dissolve_integrate.png"', r"""
**Reading the figure**
- **Data:** the 3,043 PAD-US records in the focus area; for Integrate, the 2,434 *fee* (ownership) parcels, shown for the 12 × 12 km window with the most slivers.
- **What we did:** *Dissolve* — merged the records by GAP status (panel 2) and, separately, merged everything into one footprint. *Integrate* — snapped all vertices to a 30 m grid so nearly-coincident edges become identical; counted small overlaps (purple) and gaps (red) under 2 ha before and after.
- **What it shows:** adding up the raw records gives 15,665 km², but the land actually covered is **9,977 km² — summing records overstates protected land by 57 %**. Dissolving by GAP status still leaves 12,352 km², because different GAP classes overlap. Integrate cuts overlaps from 540 to 206 and gaps from 483 to 250, but also **deletes 204 parcels** smaller than the tolerance: the tolerance is an analytical choice too.
""", r"""
**读图说明**
- **数据：** 聚焦区内 3,043 条 PAD-US 记录；Integrate 部分用其中 2,434 个 *fee*（产权）地块，并只显示碎片最多的 12 × 12 km 窗口。
- **做了什么：** *Dissolve*——按 GAP 等级合并记录（第 2 幅），另外再把全部记录合并成一个总覆盖范围。*Integrate*——把所有顶点吸附到 30 m 网格上，使几乎重合的边界完全重合；统计处理前后小于 2 公顷的细小重叠（紫色）和缝隙（红色）。
- **结论：** 直接把原始记录的面积相加是 15,665 km²，但实际覆盖的土地只有 **9,977 km²——简单相加把受保护面积高估了 57%**。按 GAP 等级融合后仍有 12,352 km²，因为不同 GAP 等级之间也有重叠。Integrate 把重叠从 540 处减到 206 处、缝隙从 483 处减到 250 处，但同时**删掉了 204 个**小于容差的地块：容差本身也是一个分析选择。
"""),
('save(fig, "clusters_moran_lisa.png"', r"""
**Reading the figure**
- **Data:** % below poverty for the 3,107 contiguous-U.S. counties from §1; neighbours = counties sharing a border or a corner (queen contiguity).
- **What we did:** Global Moran's I (one number for the whole map; the slope of the line in the left panel), its significance from 999 random reshuffles of the values (right), and Local Moran / LISA (one label per county, p < 0.05; middle).
- **What it shows:**
  - **I = 0.50, pseudo p = 0.001** (the smallest value 999 reshuffles can give): reshuffled maps give I between about −0.03 and +0.03, and **none reached 0.50**. Strong positive spatial autocorrelation.
  - **High-High (442 counties, poor among poor)** form the regions seen in §1: Georgia (66), Mississippi (61), Kentucky (55), Louisiana (39), Texas (35), Arkansas (32), Alabama (28), New Mexico (18). **Low-Low (503)** cover the Upper Midwest (Nebraska 52, Minnesota 51, Iowa 42, Wisconsin 33), northern Virginia and the Washington DC suburbs, and the Colorado–Utah Front Range.
  - **Outliers are small and worth a look:** 69 High-Low counties (a poor county among richer neighbours, e.g. Riley KS, home of a large university, and Philadelphia PA, a city ringed by suburbs) and 39 Low-High. The highest rate in the country, Oglala Lakota SD (55.8 %), is *not* significant: of its 8 neighbours only two are very poor (Jackson 38 %, Bennett 30 %) and five are at or below the national median (8–13 %), so their average (17.7 %) is only a little above the median — it is neither surrounded by poor counties nor by rich ones.
  - **Scale matters:** run on the 118 counties of Oregon, Washington and Idaho alone, the same variable gave I = 0.09 (p = 0.04). Autocorrelation is a property of the variable *and* the study area.
  - 3,107 tests at p < 0.05 expect about 155 false positives, so single counties at the edge of a cluster are uncertain; the large regions are not.
""", r"""
**读图说明**
- **数据：** §1 中美国本土 3,107 个县的贫困率；邻居 = 共边或共点的县（queen 邻接）。
- **做了什么：** 全局 Moran's I（整张地图一个数值，即左图中直线的斜率）；把数值随机打乱 999 次得到它的显著性（右图）；局部 Moran / LISA（每个县一个标签，p < 0.05，中图）。
- **结论：**
  - **I = 0.50，伪 p = 0.001**（999 次打乱能给出的最小值）：打乱后的 I 大约在 −0.03 到 +0.03 之间，**没有一次达到 0.50**。这是很强的正空间自相关。
  - **高-高（442 个县，穷县被穷县包围）**构成了 §1 中看到的那些区域：佐治亚（66）、密西西比（61）、肯塔基（55）、路易斯安那（39）、得克萨斯（35）、阿肯色（32）、阿拉巴马（28）、新墨西哥（18）。**低-低（503 个县）**覆盖中西部北部（内布拉斯加 52、明尼苏达 51、艾奥瓦 42、威斯康星 33）、北弗吉尼亚和华盛顿特区郊区，以及科罗拉多—犹他的落基山东麓。
  - **异常值不多，但值得一看：** 69 个高-低县（周围较富、自身较穷，例如堪萨斯州的赖利县，有一所大型大学；宾夕法尼亚州的费城，被富裕郊区包围）和 39 个低-高县。全国贫困率最高的南达科他州奥格拉拉拉科塔县（55.8%）反而*不*显著：它的 8 个邻县中只有两个很穷（杰克逊县 38%、贝内特县 30%），另有五个处于或低于全国中位数（8%–13%），邻居平均只有 17.7%，仅略高于中位数——它既不算被穷县包围，也不算被富县包围。
  - **尺度很重要：** 如果只用俄勒冈、华盛顿、爱达荷三州的 118 个县，同一个变量的 I 只有 0.09（p = 0.04）。空间自相关既取决于变量，也取决于研究范围。
  - 在 p < 0.05 下做 3,107 次检验，预计约有 155 个假阳性，所以聚集区边缘的个别县不确定；但大片区域是可靠的。
"""),
('save(fig, "spatial_correlation_two_variables.png"', r"""
**Reading the figure**
- **Data:** the focus area cut into ~5 km cells (761 cells at least 80 % inside it); for each cell, mean elevation (SRTM) and % forest (NLCD 41–43).
- **What we did:** mapped the two variables side by side and plotted one against the other, with Pearson r and Spearman ρ.
- **What it shows:** a **moderate positive correlation (r = 0.45, ρ = 0.48)**: higher cells tend to be more forested. The scatter is not one cloud, though — many cells at 500–1,100 m have almost no forest: the dry plateau east of the Cascades (Wasco County), where rainfall rather than elevation limits trees. This is correlation **between two variables**; figure 7 measured autocorrelation of **one**. Neighbouring cells are not independent, so the effective sample is smaller than 761.
""", r"""
**读图说明**
- **数据：** 把聚焦区切成约 5 km 的网格（761 个至少 80% 位于区内的格子）；每个格子取平均海拔（SRTM）和森林比例（NLCD 41–43 类）。
- **做了什么：** 把两个变量并排成图，再画两者的散点图，计算 Pearson r 和 Spearman ρ。
- **结论：** 两者呈**中等正相关（r = 0.45，ρ = 0.48）**：海拔越高的格子森林越多。但散点并不是一团：很多海拔 500–1,100 m 的格子几乎没有森林——那是喀斯喀特山脉以东的干旱高原（沃斯科县），那里限制树木的是降水而不是海拔。这是**两个变量之间**的相关；图 7 衡量的是**一个变量**的自相关。相邻格子并不独立，所以有效样本量小于 761。
"""),
('save(fig, "hotspots_getis_ord.png"', r"""
**Reading the figure**
- **Data:** the same 3,107 counties and poverty rates as figure 7.
- **What we did:** Getis-Ord Gi* — for each county, is the sum of its own and its neighbours' rates unusually high (hot spot) or low (cold spot)? z-scores classed at 95 % and 99 % confidence.
- **What it shows:**
  - **478 hot-spot counties** (334 at 99 %): the Mississippi Delta and the Black Belt of Georgia, Alabama and South Carolina, eastern Kentucky, the Texas–Mexico border, the Navajo and Apache lands of Arizona and New Mexico, and the Lakota reservations of South Dakota.
  - **345 cold-spot counties** (104 at 99 %): Minnesota, Wisconsin, Iowa and Nebraska, the Washington DC–Baltimore suburbs, New Hampshire, and the Denver and Salt Lake City areas. 2,284 counties are not significant.
  - Gi* and LISA largely agree here (422 counties are both LISA High-High and Gi* hot) because the clusters are large. They still answer different questions — LISA asks whether a county **resembles** its neighbours, Gi* whether the county-plus-neighbours window is **high or low as a whole**. The **circled counties** show the difference (table above the map):
    - **Riley, KS** and **Philadelphia, PA** (22.7 % each) are LISA **High-Low outliers** — poor counties ringed by richer ones (a large university; a city inside its suburbs). In Gi* their richer neighbours pull the window down, so they are grey: Gi* has no outlier class and they disappear.
    - **Oglala Lakota, SD** (55.8 %, the poorest county in the country) is the reverse: **not significant in LISA** (p = 0.054) but a **99 % Gi* hot spot**. Gi* counts the county's own extreme value inside the window; LISA compares it with random sets of neighbours, and with a value this extreme even random neighbours give a large product.
    - Report which statistic you used: Gi* to delimit a region for intervention, LISA to find the places that break the regional pattern.
""", r"""
**读图说明**
- **数据：** 与图 7 相同的 3,107 个县及其贫困率。
- **做了什么：** Getis-Ord Gi*——对每个县，判断"自身加邻居"的贫困率总和是否异常地高（热点）或低（冷点）；按 95% 和 99% 置信度对 z 值分级。
- **结论：**
  - **478 个热点县**（其中 99% 置信的 334 个）：密西西比三角洲以及佐治亚、阿拉巴马、南卡罗来纳的"黑带"，肯塔基东部，得克萨斯—墨西哥边境，亚利桑那和新墨西哥的纳瓦霍、阿帕奇保留地，以及南达科他州的拉科塔保留地。
  - **345 个冷点县**（其中 99% 置信的 104 个）：明尼苏达、威斯康星、艾奥瓦、内布拉斯加，华盛顿特区—巴尔的摩郊区，新罕布什尔，以及丹佛和盐湖城周边。其余 2,284 个县不显著。
  - 这里 Gi* 和 LISA 基本一致（422 个县既是 LISA 高-高又是 Gi* 热点），因为聚集区很大。但两者回答的问题不同——LISA 问一个县和邻居**像不像**，Gi* 问"自己 + 邻居"这一片**整体高不高**。**图中圈出的县**说明了差别（见地图上方的表）：
    - **堪萨斯州赖利县**和**宾夕法尼亚州费城**（都是 22.7%）在 LISA 中是**高-低异常值**——穷县被较富的县包围（一个有大型大学，一个是被郊区环绕的城市）。在 Gi* 中，较富的邻居把整片的平均拉低，所以是灰色：Gi* 没有异常值这一类，它们直接消失了。
    - **南达科他州奥格拉拉拉科塔县**（55.8%，全国最穷）正好相反：在 LISA 中**不显著**（p = 0.054），在 Gi* 中却是 **99% 热点**。Gi* 把这个县自己极高的值也算进窗口；LISA 则拿它和随机抽取的"假邻居"比较，自身值这么极端时，随机邻居算出的乘积也很大，真实值就显得不突出。
    - 报告时写明用的是哪一种：要圈定干预的区域范围用 Gi*，要找打破区域格局的特殊地点用 LISA。
"""),
('save(fig, "point_pattern_nn.png"', r"""
**Reading the figure**
- **Data:** three point layers. *Left*: the 1,974 USGS earthquakes of magnitude ≥ 2.5 recorded on land in the contiguous U.S. in 2025. *Centre*: 1,974 points scattered completely at random over the same land (simulated). *Right*: one point inside each of the 297 counties of Iowa, Kansas and Nebraska.
- **What we did:** for every point, measured the distance to its nearest other point, averaged it, and divided by the average expected if the same number of points were scattered at random over the same area (Clark-Evans ratio R; the table above lists the distances and z-scores). The bar at the bottom places the three R values on one scale.
- **What it shows:**
  - **Clustered, R = 0.27:** earthquakes sit 8.4 km from their nearest neighbour on average, against 31.4 km if random. 87 % of them fall in six states (California 678, Texas 488, Nevada 278, Idaho 125, New Mexico 74, Kansas 65): along the plate boundary in California and Nevada, and in oil-and-gas fields of West Texas, New Mexico and Kansas, where much of the shaking is linked to wastewater injection.
  - **Random, R = 1.03:** close to 1, as it should be. It is slightly above 1 (z = 2.5) because this simple test makes no correction for the border: points near the coast or the national border have no neighbours on one side, so their nearest neighbour is a little farther away. Read R values near 1 with that in mind.
  - **Dispersed, R = 1.69:** Plains counties were surveyed as a near-regular grid, so their points keep their distance from each other — 36.6 km apart against 21.7 km if random.
  - The same R statistic separates the three patterns; the maps make the meaning of "R < 1" and "R > 1" visible.
""", r"""
**读图说明**
- **数据：** 三个点图层。*左*：2025 年美国本土陆地上记录到的 1,974 次 2.5 级及以上地震（USGS）。*中*：在同一片陆地上完全随机撒下的 1,974 个点（模拟）。*右*：艾奥瓦、堪萨斯、内布拉斯加三州 297 个县，每个县内取一个点。
- **做了什么：** 对每个点计算它到最近另一个点的距离，取平均，再除以"同样数量的点在同样面积上随机分布"时的期望平均距离，得到 Clark-Evans 比值 R（上方表格列出了距离和 z 值）。底部的数轴把三个 R 值放在同一把尺子上。
- **结论：**
  - **聚集，R = 0.27：** 地震到最近另一次地震平均只有 8.4 km，随机分布时应为 31.4 km。87% 的地震集中在六个州（加利福尼亚 678、得克萨斯 488、内华达 278、爱达荷 125、新墨西哥 74、堪萨斯 65）：一部分沿加州和内华达的板块边界分布，另一部分在得克萨斯西部、新墨西哥和堪萨斯的油气田，那里很多地震与废水回注有关。
  - **随机，R = 1.03：** 接近 1，符合预期。它略大于 1（z = 2.5），是因为这个简单检验没有做边界校正：靠近海岸或国境线的点一侧没有邻居，最近邻距离会偏大一点。所以 R 在 1 附近时要谨慎解读。
  - **分散，R = 1.69：** 大平原各州的县是按近似规则的网格划分的，所以各县的点彼此保持距离——平均相距 36.6 km，随机分布时应为 21.7 km。
  - 同一个 R 统计量能区分这三种格局；地图让"R < 1"和"R > 1"的含义一目了然。
"""),
('save(fig, "rs_ndvi_classification.png"', r"""
**Reading the figure**
- **Data:** a Sentinel-2 summer-2023 composite of Champaign–Urbana, IL (10 m; red, green, blue and near-infrared bands) and NLCD 2021 land cover as training labels.
- **What we did:** (1) natural colour; (2) false colour, with near-infrared shown as red; (3) NDVI = (NIR − red)/(NIR + red); (4) a random-forest classification of every pixel.
- **What the model was given:**
  - **Input (features), one row per 10 m pixel, 5 numbers:** surface reflectance in red (B4), green (B3), blue (B2) and near-infrared (B8) — the file stores reflectance × 10,000, the notebook divides by 10,000 — plus NDVI computed from B8 and B4.
  - **Label (target):** the NLCD 2021 class code of the same location (e.g. 82 = cultivated crops, 21–24 = developed). The label raster is the Week 7 NLCD at **150 m**, resampled by nearest neighbour onto the 10 m Sentinel-2 grid, so each label is a 15 × 15-pixel block; classes with fewer than 2,000 pixels in the scene were dropped (11 classes kept).
  - **Samples:** 120,000 randomly chosen labelled pixels, split 70 / 30 (84,000 training, 36,000 test), stratified by class. No hand-drawn training polygons: the labels come from an existing map, which is why §5 calls NLCD "treated as truth".
- **What it shows:** vegetation reflects strongly in near-infrared, so crops turn bright red in (2) and green in (3), while the city stands out with low NDVI. The classifier reproduces the broad pattern — urban core vs cropland — but figure 12 shows how often it is right, class by class.
""", r"""
**读图说明**
- **数据：** 伊利诺伊州香槟–厄巴纳的 Sentinel-2 2023 年夏季合成影像（10 m；红、绿、蓝、近红外四个波段），以 NLCD 2021 土地覆盖作为训练标签。
- **做了什么：** (1) 真彩色；(2) 假彩色，近红外显示为红色；(3) NDVI =（近红外 − 红）/（近红外 + 红）；(4) 用随机森林对每个像元分类。
- **模型的输入和标签：**
  - **输入（特征）：** 每个 10 m 像元一行，5 个数：红（B4）、绿（B3）、蓝（B2）、近红外（B8）四个波段的地表反射率（文件里存的是反射率 × 10,000，notebook 中除以 10,000），再加上由 B8 和 B4 算出的 NDVI。
  - **标签（目标）：** 同一位置的 NLCD 2021 类别代码（例如 82 = 耕地，21–24 = 各级建成区）。标签栅格是第 7 周数据包里 **150 m** 的 NLCD，用最近邻法重采样到 Sentinel-2 的 10 m 网格上，所以每个标签实际是 15 × 15 个像元的方块；影像范围内少于 2,000 个像元的类别被剔除（保留 11 类）。
  - **样本：** 随机抽取 120,000 个带标签像元，按类别分层，70% 训练（84,000）、30% 测试（36,000）。没有手绘训练多边形——标签来自一张现成的地图，所以 §5 说 NLCD 是"被当作真值"的。
- **结论：** 植被在近红外波段反射很强，所以农田在 (2) 中呈亮红色、在 (3) 中呈绿色，城区则表现为低 NDVI。分类器大致还原了"城区—农田"的格局，但逐类的准确程度要看图 12。
"""),
('save(fig, "ml_confusion_matrix.png"', r"""
**Reading the figure**
- **Data:** 36,000 test pixels the model never saw during training, each with its NLCD label and the model's prediction.
- **What we did:** a row-normalised confusion matrix (each row = one true class; the cells show where its pixels were predicted to go) and the recall of each class (share of that class found).
- **What it shows:** overall accuracy is **0.68**, but **60 % of the test pixels are cultivated crops** (recall 0.91), and they carry the score. Developed classes are found 33–44 % of the time, forests 3–14 %, woody wetlands and barren land never; most minority pixels are predicted as crops (the dark column). Part of the "error" belongs to the labels: NLCD here is 150 m, the image 10 m.
""", r"""
**读图说明**
- **数据：** 模型训练时从未见过的 36,000 个测试像元，每个都有 NLCD 标签和模型预测结果。
- **做了什么：** 按行归一化的混淆矩阵（每一行是一个真实类别，格子显示该类像元被预测成了什么），以及每一类的召回率（该类中被正确找出的比例）。
- **结论：** 总体准确率是 **0.68**，但**测试像元中有 60% 是耕地**（召回率 0.91），总分主要靠它撑起来。各类已开发用地只有 33–44% 被找出，森林类 3–14%，木本湿地和裸地一个都没找出；大部分少数类像元都被预测成了耕地（深色的那一列）。部分"错误"其实来自标签：这里的 NLCD 是 150 m，而影像是 10 m。
"""),
('save(fig, "categories_forest_definitions.png"', r"""
**Reading the figure**
- **Data:** NLCD 2021 at 30 m for the focus area (about 19,700 km² of land), and PAD-US for "protected".
- **What we did:** counted forest area under five defensible definitions — canopy classes 41–43; the same, dropping patches below FAO's 0.5 ha minimum or below 1 km²; adding woody wetlands (90); adding shrub/scrub (52, FAO's "other wooded land"). The second table does the same for "protected", from GAP 1 only to any PAD-US record.
- **What it shows:** forest ranges from **9,233 to 12,010 km² (× 1.30) without a single pixel changing**; the shrub rule alone adds about 1,975 km². "Protected" ranges from 1,425 km² (GAP 1, 7.2 % of the area) to 9,977 km² (any record, 50.6 %) — a factor of 7. The category is a choice with consequences (Robbins).
""", r"""
**读图说明**
- **数据：** 聚焦区 30 m 的 NLCD 2021（陆地约 19,700 km²），以及用来定义"受保护"的 PAD-US。
- **做了什么：** 按五种都说得通的"森林"定义计算面积——只算林冠类 41–43；同样的类别，但去掉小于 FAO 最小标准 0.5 公顷或小于 1 km² 的斑块；再加上木本湿地（90 类）；再加上灌丛（52 类，即 FAO 的"其他林地"）。第二张表对"受保护"做同样的事，从只算 GAP 1 到任何 PAD-US 记录。
- **结论：** **一个像元都没变，森林面积却在 9,233 到 12,010 km² 之间（相差 1.30 倍）**；仅灌丛这一条规则就多出约 1,975 km²。"受保护"面积从 1,425 km²（只算 GAP 1，占 7.2%）到 9,977 km²（任何记录，占 50.6%），相差约 7 倍。类别本身就是一个有后果的选择（Robbins）。
"""),
('save(fig, "maup_two_aggregations.png"', r"""
**Reading the figure**
- **Data:** the 24,205 UCDP conflict events of 2023 worldwide, with their best-estimate deaths.
- **What we did:** summed the deaths two ways — by country (left) and by 500 km × 500 km equal-area grid cell (right) — and for each measured how concentrated the violence looks: the share held by the top unit, and how many units hold half of all deaths.
- **What it shows:** by country, **Ukraine alone holds 53 % of deaths and 1 of 67 countries holds half**; by grid cell the top cell holds 30 % and it takes **3 of 196 cells** to reach half. The ranking changes too (countries: Ukraine, Mexico, Sudan; cells: Ukraine, Russia, Jordan — cells are named by the country at their centre, so the "Jordan" cell also covers neighbouring areas). Same events, different units, different story: the MAUP.
""", r"""
**读图说明**
- **数据：** 2023 年全球 24,205 起 UCDP 冲突事件及其死亡人数（最佳估计）。
- **做了什么：** 用两种方式汇总死亡人数——按国家（左）和按 500 km × 500 km 的等面积网格（右）——并分别衡量暴力的集中程度：排名第一的单元占多少比例，以及多少个单元合计占全部死亡的一半。
- **结论：** 按国家汇总，**乌克兰一国就占 53%，67 个国家中 1 个就占了一半**；按网格汇总，排名第一的格子占 30%，需要 **196 个格子中的 3 个**才达到一半。排名也变了（国家：乌克兰、墨西哥、苏丹；格子：乌克兰、俄罗斯、约旦——格子按中心点所在国家命名，所以"约旦"格子也覆盖了周边地区）。同样的事件，换一种单元，故事就不同了：这就是 MAUP。
"""),
('save(fig, "ethics_point_vs_aggregated.png"', r"""
**Reading the figure**
- **Data:** the same 24,205 events; country populations from Natural Earth.
- **What we did:** *left* — every event at its exact coordinates, dot size by deaths; *right* — deaths per million people by country.
- **What it shows:** both maps highlight the same regions (Ukraine, the Sahel and Sudan, Myanmar, Mexico), so aggregating costs almost nothing for the policy picture — while the left map locates places where people were killed precisely enough to be misused.
""", r"""
**读图说明**
- **数据：** 同样的 24,205 起事件；各国人口来自 Natural Earth。
- **做了什么：** *左图*——每起事件画在精确坐标上，点的大小表示死亡人数；*右图*——按国家计算每百万人口的死亡数。
- **结论：** 两张图突出的是同样的地区（乌克兰、萨赫勒与苏丹、缅甸、墨西哥），所以汇总几乎不损失对政策有用的信息——而左图把有人遇难的地点定位得足够精确，有被滥用的风险。
"""),
]
