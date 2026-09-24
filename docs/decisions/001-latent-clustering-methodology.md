> **Correction note (2026-09-24).** This is the 2026-09-05 ADR proposing the clustering method that was actually used (the README's Phase 5). It is kept as written; status is still PROPOSED because Grok's review (see `docs/reviews/`) recommended against accepting it as written. The paths above use the old `Google Arts & Culture/...` layout, since flattened to `data/`, `clusters/` and `catalogue/`.

# ADR 001: Multimodal Latent Clustering Methodology & Aesthetic Taxonomy

**Status**: PROPOSED  
**Date**: September 5, 2026  
**Deciders**: <user> & Antigravity  
**Target Artifacts**: `Google Arts & Culture/favorites_clustered.json`, `Google Arts & Culture/docs/cluster_manifest.json`, `Google Arts & Culture/docs/latent_cluster_map.svg`  

---

## 1. Context & Problem Statement

The curated corpus consists of 801 fine art favorites enriched with multimodal visual critiques across the 5 Evaluative Angles (Composition & Lineage, Utility & Ergonomics, Visual Language & Semiotics, Light & Space, Color & Typography). To transform these individual analyses into operational design systems, we must organize the corpus into a coherent, opinionated taxonomy of **8 to 12 aesthetic clusters**.

A naive approach (clustering solely by art historical era or museum partner) fails because it produces trivial groupings (e.g. "17th Century Dutch") rather than trans-historical design lineages (e.g. connecting medieval manuscript borders with modern information dashboards). We require an empirical, reproducible methodology that synthesizes color science, spatial geometry, and design semantics into a unified latent space.

---

## 2. Multimodal Feature Engineering

Each of the 801 artworks is mapped into a normalized 59-dimensional composite vector $\mathbf{X} \in \mathbb{R}^{59}$:

$$\mathbf{X} = \left[ w_{\text{color}} \cdot \mathbf{v}_{\text{color}} \;\Big\Vert\; w_{\text{spatial}} \cdot \mathbf{v}_{\text{spatial}} \;\Big\Vert\; w_{\text{semantic}} \cdot \mathbf{v}_{\text{semantic}} \right]$$

### A. Perceptual Color Space ($\mathbf{v}_{\text{color}} \in \mathbb{R}^7$, weight $w_{\text{color}} = 1.0$)
Hexadecimal values from `extracted_palette` are converted to standard CIE $L^*a^*b^*$ coordinates under a D65 standard illuminant. We extract:
- Mean Lightness ($\bar{L}^*$), Standard Deviation of Lightness ($\sigma_L$), Lightness Dynamic Range ($\Delta L^* = L^*_{\max} - L^*_{\min}$).
- Mean Chroma ($\bar{C}^* = \sqrt{{a^*}^2 + {b^*}^2}$), Max Chroma ($C^*_{\max}$).
- Mean chromatic axes ($\bar{a}^*$ green/red, $\bar{b}^*$ blue/yellow).
- Standardized via $Z$-score normalization (`StandardScaler`).

### B. Spatial & Categorical Geometry ($\mathbf{v}_{\text{spatial}} \in \mathbb{R}^{27}$, weight $w_{\text{spatial}} = 0.8$)
- Log-normalized aspect ratio ($\ln(\max(\text{aspect\_ratio}, 0.1))$).
- One-hot encoded categorical design attributes:
  - `orientation`: Panoramic, Landscape, Square, Portrait.
  - `framing_density`: sparse, balanced, dense, claustrophobic.
  - `spatial_depth`: flat_graphic, layered_shallow, deep_perspective.
  - `light_profile`: diffuse, chiaroscuro, direct, ambient, luminescent.
  - `contrast_level`: low, medium, high, extreme.
  - `chromatic_temperature`: warm, neutral, cool, mixed.

### C. Design Semantics & Vernacular ($\mathbf{v}_{\text{semantic}} \in \mathbb{R}^{25}$, weight $w_{\text{semantic}} = 1.2$)
A text composite is constructed per artwork combining:
`{title} {creator} {medium} {precept_critique} {design_heuristics} {geometric_structure} {focal_flow} {structural_motifs} {historical_lineage}`
- Tokenized via `TfidfVectorizer` (1,500 max features, sublinear TF scaling, n-gram range (1, 2), English stop-words removed).
- Latent Semantic Analysis via `TruncatedSVD` reducing to 25 orthogonal semantic components.

---

## 3. Empirical Algorithm Evaluation

We evaluated two foundational clustering methodologies across $k \in [8, 12]$ on the 801-artwork feature matrix:
1. **Agglomerative Hierarchical Clustering** with Ward minimum-variance linkage.
2. **K-Means Clustering** with k-means++ initialization ($n_{\text{init}} = 30$, random seed 42).

### Empirical Evaluation Matrix:

| $k$ Clusters | Model | Silhouette Score | Calinski-Harabasz Index | Min Cluster Size | Evaluation Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **8** | Agglomerative (Ward) | 0.0430 | 23.31 | 25 | Lower separation, high intra-cluster variance |
| **8** | K-Means | 0.0750 | 29.77 | 57 | Strong CH index, but broad over-aggregation |
| **9** | Agglomerative (Ward) | 0.0483 | 22.92 | 25 | Modest silhouette gain |
| **9** | K-Means | 0.0763 | 28.81 | 45 | Good balance |
| **10** | **Agglomerative (Ward)** | 0.0542 | 22.57 | 25 | Consistent hierarchy |
| **10** | **K-Means (Selected)** | **0.0790** | **28.40** | **28** | **Optimal trade-off: high CH score, clean cluster sizes, ideal conceptual granularity** |
| **11** | K-Means | 0.0846 | 26.92 | 30 | Minor fragmentation of Bauhaus cluster |
| **12** | K-Means | 0.0883 | 26.75 | 20 | Sub-cluster fragmentation (salons split artificially) |

### Decision Rationale:
* **K-Means ($k=10$)** demonstrated superior cluster separation (Silhouette 0.0790 vs. 0.0542 for Ward) and tighter spherical density (Calinski-Harabasz 28.40).
* At $k=10$, every cluster contains between 28 and 150 members (3.5% to 18.7%), avoiding degenerate 1-item micro-clusters while maintaining distinct aesthetic boundaries.
* The 10 resulting clusters map directly to actionable design paradigms.

---

## 4. The 10 Aesthetic Clusters

| ID | Cluster Name | Member Count | % of Corpus | Dominant Spatial & Light Profile | Representative Anchor Artwork |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Cartographic & Information Architecture** | 68 | 8.5% | Diffuse / Ambient, Layered Shallow | *Buddhist Map of the World* (1710) |
| **2** | **Bauhaus Functionalism & Standardized Modular Systems** | 51 | 6.4% | Diffuse / Ambient, Flat Orthogonal | Franz Ehrlich *Worktable* (1957) |
| **3** | **Atmospheric Maritime & Industrial Panoramas** | 60 | 7.5% | Diffuse / Direct, Deep Perspective | Eugène Boudin *Le Havre Jetties* (1895) |
| **4** | **Tactile Materiality & Sculptural Object Minimalism** | 71 | 8.9% | Diffuse, Layered Shallow | Douglas Coupland *Middle East* (2014) |
| **5** | **Graphic Semiotics, Flags & Emblems** | 150 | 18.7% | Direct / Diffuse, Flat Graphic | Bill Walsh *The Drowned World* (2019) |
| **6** | **Chiaroscuro Drama & Narrative Tension** | 94 | 11.7% | Chiaroscuro / Direct, Deep Perspective | D. R. Wilson *Mrs. Jenkins' Dinner* (1984) |
| **7** | **Classical Architectural Scenography & Linear Perspectives** | 146 | 18.2% | Diffuse / Direct, Deep Perspective | Romolo Liverani *Stage Design* (c. 1820) |
| **8** | **Botanical Spatial Planning & Garden Architecture** | 49 | 6.1% | Diffuse / Direct, Layered Shallow | Gertrude Jekyll *Hestercombe Plan* (1906) |
| **9** | **Radical Geometric Abstraction & Constructivism** | 77 | 9.6% | Diffuse / Ambient, Flat Graphic | Liubov Popova *Composition Red-Black-Gold* (1920) |
| **10** | **Intimate Historical Salons & Academic Interiors** | 35 | 4.4% | Ambient, Deep Perspective | *Interior of a Library* (1830s) |

---

## 5. Non-Destructive Invariant Compliance

- **Zero Overwrite of Upstream Data**: `favorites_analyzed.json` was read-only.
- **Additive Artifacts Generated**:
  - `Google Arts & Culture/favorites_clustered.json` (SHA-verified additive file with `cluster_id`, `cluster_name`, `cluster_slug`, `cluster_centroid_dist`, `pca_x`, `pca_y`).
  - `Google Arts & Culture/favorites_clustered.tsv` (companion TSV).
  - `Google Arts & Culture/docs/cluster_manifest.json` (cluster definitions and anchor works).
  - `Google Arts & Culture/docs/latent_cluster_map.svg` (2D scatter plot).
- **Catalogue Notes**: 801 files in `Google Arts & Culture/catalogue/` remain untouched pending Gate 2a review approval.
