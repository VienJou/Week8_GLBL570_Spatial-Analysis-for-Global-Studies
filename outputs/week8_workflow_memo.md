# Week 8 workflow memo

## Question
[One sentence: what policy question does this analysis answer?]

## Data and units
- Focus area: Clackamas, Clark, Hood River, Multnomah, Skamania, Wasco (6 counties), EPSG:5070 (equal-area, metres)
- Forest: NLCD 2021, 30 m, classes [41, 42, 43]. Five other defensible definitions give 9,233–12,010 km² (§6.1).
- Protected areas: PAD-US 4.1, GAP status 1–2 = "protected" here; GAP 1–3 would change the answer (§2.4).

## Operations and results
1. Overlay: 14.0% of forest is inside GAP 1–2 (1,377 of 9,860 km²); 73.3% inside GAP 1–3.
2. Buffer: 64%–100% of the 33 Cox's Bazar camps are "near conflict" for radii 1–100 km.
3. Clustering: Moran's I = 0.496 (pseudo p = 0.001, queen weights, 999 permutations, 3,107 contiguous-U.S. counties).
4. Classification: overall accuracy 0.68; weakest class Barren land (rock/sand/clay) (recall 0.00).

## One policy implication
[What should change, for whom, on the strength of this?]

## What this analysis cannot establish
[Correlation vs mechanism; designation vs outcome; Euclidean vs travel distance; MAUP; label quality.]

## AI engagement / Ethics
[What did the AI propose, and what did it fill in silently? Does any output locate vulnerable people precisely?]
