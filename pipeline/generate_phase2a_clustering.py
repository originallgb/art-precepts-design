import json
import sqlite3
import math
import os
import csv
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD, PCA
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import KMeans

import paths

def hex_to_cielab(hex_str):
    hex_str = hex_str.strip().lstrip('#')
    if len(hex_str) != 6:
        return (50.0, 0.0, 0.0)
    try:
        r = int(hex_str[0:2], 16) / 255.0
        g = int(hex_str[2:4], 16) / 255.0
        b = int(hex_str[4:6], 16) / 255.0
    except ValueError:
        return (50.0, 0.0, 0.0)

    def gamma_inv(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    rl, gl, bl = gamma_inv(r), gamma_inv(g), gamma_inv(b)
    X = rl * 0.4124564 + gl * 0.3575761 + bl * 0.1804375
    Y = rl * 0.2126729 + gl * 0.7151522 + bl * 0.0721750
    Z = rl * 0.0193339 + gl * 0.1191920 + bl * 0.9503041

    Xn, Yn, Zn = 0.95047, 1.00000, 1.08883
    xr, yr, zr = X / Xn, Y / Yn, Z / Zn

    def f(t):
        return t ** (1.0 / 3.0) if t > 0.008856 else (7.787 * t) + (16.0 / 116.0)

    L = (116.0 * f(yr)) - 16.0
    a = 500.0 * (f(xr) - f(yr))
    b = 200.0 * (f(yr) - f(zr))
    return (L, a, b)

# 1. Load Data
with open(paths.DATA / "favorites_analyzed.json", "r", encoding="utf-8") as f:
    items = json.load(f)

db_path = r"%USERPROFILE%\.gemini\antigravity\brain\agy-session-2287\scratch\multimodal_analysis.db"
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT index_num, json_result FROM analysis_cache")
sqlite_map = {row[0]: json.loads(row[1]) for row in c.fetchall()}

# 2. Build Feature Matrices
# A. Color features
color_features = []
for item in items:
    hexes = [h.strip() for h in (item.get("extracted_palette") or "").split(",") if h.strip().startswith("#")] or ["#808080"]
    labs = [hex_to_cielab(h) for h in hexes]
    L_vals = [lab[0] for lab in labs]
    chroma_vals = [math.sqrt(lab[1]**2 + lab[2]**2) for lab in labs]
    color_features.append([
        np.mean(L_vals), np.std(L_vals) if len(L_vals) > 1 else 0.0,
        np.max(L_vals) - np.min(L_vals), np.mean(chroma_vals), np.max(chroma_vals),
        np.mean([lab[1] for lab in labs]), np.mean([lab[2] for lab in labs])
    ])
color_arr = StandardScaler().fit_transform(np.array(color_features))

# B. Spatial / Categorical features
cat_data = [[
    item.get("orientation") or "Unknown", item.get("framing_density") or "balanced",
    item.get("spatial_depth") or "layered_shallow", item.get("light_profile") or "diffuse",
    item.get("contrast_level") or "medium", item.get("chromatic_temperature") or "neutral"
] for item in items]
ar_vals = [[math.log(max(float(item.get("aspect_ratio") or 1.0), 0.1))] for item in items]
cat_arr = OneHotEncoder(sparse_output=False, handle_unknown="ignore").fit_transform(cat_data)
ar_arr = StandardScaler().fit_transform(np.array(ar_vals))
spatial_arr = np.hstack([cat_arr, ar_arr])

# C. Semantic text features
corpus = []
for item in items:
    sq = sqlite_map.get(item.get("index"), {})
    critique = item.get("precept_critique") or ""
    heuristics = item.get("design_heuristics") or ""
    title = item.get("title") or ""
    creator = item.get("creator") or ""
    medium = item.get("medium") or ""
    vc = sq.get("visual_composition", {})
    geo = vc.get("geometric_structure", "")
    flow = vc.get("focal_flow", "")
    dv = sq.get("design_vernacular", {})
    motifs = " ".join(dv.get("structural_motifs", [])) if isinstance(dv.get("structural_motifs"), list) else str(dv.get("structural_motifs", ""))
    lineage = " ".join(dv.get("historical_lineage", [])) if isinstance(dv.get("historical_lineage"), list) else str(dv.get("historical_lineage", ""))
    corpus.append(f"{title} {creator} {medium} {critique} {heuristics} {geo} {flow} {motifs} {lineage}")

tfidf = TfidfVectorizer(max_features=1500, stop_words="english", ngram_range=(1, 2), sublinear_tf=True)
svd = TruncatedSVD(n_components=25, random_state=42)
semantic_arr = StandardScaler().fit_transform(svd.fit_transform(tfidf.fit_transform(corpus)))

# Unified feature matrix
X = np.hstack([1.0 * color_arr, 0.8 * spatial_arr, 1.2 * semantic_arr])

# 3. K-Means Clustering (k=10)
k = 10
km = KMeans(n_clusters=k, random_state=42, n_init=30)
labels = km.fit_predict(X)

# 4. 2D Coordinates via PCA
pca2d = PCA(n_components=2, random_state=42)
coords2d = pca2d.fit_transform(X)

# Define Curated Cluster Metadata
cluster_definitions = {
    0: {
        "cluster_id": 1,
        "name": "Cartographic & Information Architecture",
        "slug": "cartographic-information-architecture",
        "color": "#2563EB",  # Blue
        "thesis": "Dense visual information systems utilizing hieratic scaling, multi-scalar data layers, and ornamental boundary framing to organize complex relational data.",
        "core_precept": "Layer micro-detail within rigorous macro-borders to prevent cognitive overload in data-dense interfaces."
    },
    1: {
        "cluster_id": 2,
        "name": "Bauhaus Functionalism & Standardized Modular Systems",
        "slug": "bauhaus-functionalism-modular-systems",
        "color": "#D97706",  # Amber/Ochre
        "thesis": "Orthogonal technical drafting, standardized unit ranges, and honest functional joinery where every line corresponds to physical affordance and spatial efficiency.",
        "core_precept": "Form is an ergonomic consequence of standard module constraints and honest material dimensions."
    },
    2: {
        "cluster_id": 3,
        "name": "Atmospheric Maritime & Industrial Panoramas",
        "slug": "atmospheric-maritime-industrial-panoramas",
        "color": "#0D9488",  # Teal
        "thesis": "Expansive horizontal vistas and deep atmospheric perspective balanced by sharp vertical mechanical interventions (masts, cranes, steam conduits).",
        "core_precept": "Anchor vast low-contrast negative space with high-contrast structural silhouettes on the horizon."
    },
    3: {
        "cluster_id": 4,
        "name": "Tactile Materiality & Sculptural Object Minimalism",
        "slug": "tactile-materiality-sculptural-minimalism",
        "color": "#78716C",  # Stone
        "thesis": "Restraint in form emphasizing the tactile honesty of materials (stone, wood, resin, paper) and intentional voids as positive design elements.",
        "core_precept": "Let physical surface texture and material weight communicate quality rather than ornamental decoration."
    },
    4: {
        "cluster_id": 5,
        "name": "Graphic Semiotics, Flags & Emblems",
        "slug": "graphic-semiotics-flags-emblems",
        "color": "#DC2626",  # Red
        "thesis": "High-contrast heraldic signs, bold poster flat planes, and distilled symbolic motifs designed for immediate cognitive registration across distance.",
        "core_precept": "Maximize silhouette contrast and reduce chromatic noise to achieve instant visual recognition."
    },
    5: {
        "cluster_id": 6,
        "name": "Chiaroscuro Drama & Narrative Tension",
        "slug": "chiaroscuro-drama-narrative-tension",
        "color": "#7C3AED",  # Purple
        "thesis": "Dramatic deep-shadow staging and directional key lighting directing viewer focus with extreme psychological and narrative intensity.",
        "core_precept": "Use deep shadow as an active subtractive framing device to dramatize the single illuminated action point."
    },
    6: {
        "cluster_id": 7,
        "name": "Classical Architectural Scenography & Linear Perspectives",
        "slug": "architectural-scenography-linear-perspective",
        "color": "#475569",  # Slate
        "thesis": "Monumental linear perspectives, Palladian proportional balance, and theatrical structural framing governing viewer movement through space.",
        "core_precept": "Establish clear architectural sightlines and symmetrical axes before distributing secondary asymmetric content."
    },
    7: {
        "cluster_id": 8,
        "name": "Botanical Spatial Planning & Garden Architecture",
        "slug": "botanical-spatial-planning-garden-architecture",
        "color": "#16A34A",  # Green
        "thesis": "Harmonious balance between geometric terrace boundaries and organic vegetative flow, structuring movement through living spatial zones.",
        "core_precept": "Create formal structural borders that contain and frame organic, fluid internal elements."
    },
    8: {
        "cluster_id": 9,
        "name": "Radical Geometric Abstraction & Constructivism",
        "slug": "geometric-abstraction-constructivism",
        "color": "#EA580C",  # Orange
        "thesis": "Dynamic diagonal axes, floating non-objective planes, and pure chromatic vectors creating kinetic equilibrium without representational baggage.",
        "core_precept": "Generate visual energy through asymmetrical balance and stark diagonal vector tensions."
    },
    9: {
        "cluster_id": 10,
        "name": "Intimate Historical Salons & Academic Interiors",
        "slug": "intimate-salons-academic-interiors",
        "color": "#B45309",  # Brown/Brass
        "thesis": "Enclosed, human-scale domestic and scholarly chambers characterized by warm ambient light, dense intellectual curation, and acoustic containment.",
        "core_precept": "Design high-density information environments with warm low-glare palettes to foster sustained contemplative focus."
    }
}

# 5. Build Enriched Output Dataset (Non-Destructive Additive)
clustered_items = []
for j, item in enumerate(items):
    c_idx = int(labels[j])
    c_def = cluster_definitions[c_idx]
    
    # Calculate distance to cluster centroid
    centroid = km.cluster_centers_[c_idx]
    dist_to_centroid = float(np.linalg.norm(X[j] - centroid))
    
    new_item = dict(item)  # Clone
    new_item["cluster_id"] = c_def["cluster_id"]
    new_item["cluster_name"] = c_def["name"]
    new_item["cluster_slug"] = c_def["slug"]
    new_item["cluster_centroid_dist"] = round(dist_to_centroid, 4)
    new_item["pca_x"] = round(float(coords2d[j, 0]), 4)
    new_item["pca_y"] = round(float(coords2d[j, 1]), 4)
    clustered_items.append(new_item)

# Save favorites_clustered.json
clustered_json_path = str(paths.DATA / "favorites_clustered.json")
with open(clustered_json_path, "w", encoding="utf-8") as f:
    json.dump(clustered_items, f, indent=2, ensure_ascii=False)
print(f"Saved {len(clustered_items)} records to {clustered_json_path}")

# Save favorites_clustered.tsv
clustered_tsv_path = str(paths.DATA / "favorites_clustered.tsv")
fieldnames = list(clustered_items[0].keys())
with open(clustered_tsv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    writer.writerows(clustered_items)
print(f"Saved TSV table to {clustered_tsv_path}")

# 6. Build Cluster Manifest
manifest = {
    "version": "1.0.0",
    "total_artworks": len(clustered_items),
    "cluster_count": k,
    "clusters": []
}

for i in range(k):
    c_def = cluster_definitions[i]
    c_items = [it for it in clustered_items if it["cluster_id"] == c_def["cluster_id"]]
    # Sort by centroid distance to get top anchor works
    c_items_sorted = sorted(c_items, key=lambda x: x["cluster_centroid_dist"])
    anchors = [{
        "index": it.get("index"),
        "title": it.get("title"),
        "creator": it.get("creator"),
        "date": it.get("date_created"),
        "centroid_dist": it["cluster_centroid_dist"],
        "asset_id": it.get("asset_id"),
        "local_image": it.get("local_image_file")
    } for it in c_items_sorted[:6]]
    
    manifest["clusters"].append({
        "cluster_id": c_def["cluster_id"],
        "name": c_def["name"],
        "slug": c_def["slug"],
        "color_hex": c_def["color"],
        "member_count": len(c_items),
        "percentage": round(len(c_items) / len(clustered_items) * 100, 2),
        "aesthetic_thesis": c_def["thesis"],
        "core_precept": c_def["core_precept"],
        "anchor_works": anchors
    })

manifest_path = str(paths.CLUSTERS / "cluster_manifest.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print(f"Saved cluster manifest to {manifest_path}")

# 7. Generate 2D Vector SVG Map
svg_width, svg_height = 1200, 800
pad = 80
plot_w = svg_width - 320 - (2 * pad)
plot_h = svg_height - (2 * pad)

xs = [it["pca_x"] for it in clustered_items]
ys = [it["pca_y"] for it in clustered_items]
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)

def map_x(val):
    return pad + ((val - min_x) / (max_x - min_x)) * plot_w

def map_y(val):
    return pad + (1.0 - ((val - min_y) / (max_y - min_y))) * plot_h

svg_lines = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}" style="background-color: #0F172A; font-family: -apple-system, BlinkMacSystemFont, sans-serif;">',
    f'<defs>',
    f'<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3" result="glow"/><feMerge><feMergeNode in="glow"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
    f'</defs>',
    f'<!-- Title & Header -->',
    f'<text x="{pad}" y="45" fill="#F8FAFC" font-size="22" font-weight="bold">Catalogue Latent Aesthetic Clusters (2D Coordinate Manifold)</text>',
    f'<text x="{pad}" y="65" fill="#94A3B8" font-size="13">801 Artworks | Multimodal Feature Space (CIELAB Color, Spatial Affordances, Precept Semantics)</text>',
    f'<!-- Plot Grid Background -->',
    f'<rect x="{pad}" y="{pad}" width="{plot_w}" height="{plot_h}" fill="#1E293B" rx="8" stroke="#334155" stroke-width="1"/>',
    f'<line x1="{map_x(0)}" y1="{pad}" x2="{map_x(0)}" y2="{pad + plot_h}" stroke="#334155" stroke-dasharray="4,4" stroke-width="1"/>',
    f'<line x1="{pad}" y1="{map_y(0)}" x2="{pad + plot_w}" y2="{map_y(0)}" stroke="#334155" stroke-dasharray="4,4" stroke-width="1"/>'
]

import html

# Draw scatter points
for it in clustered_items:
    cx = map_x(it["pca_x"])
    cy = map_y(it["pca_y"])
    c_idx = it["cluster_id"] - 1
    color = cluster_definitions[c_idx]["color"]
    title_str = str(it.get("title") or "Untitled")
    creator_str = str(it.get("creator") or "Unknown")
    c_name_str = str(it.get("cluster_name") or "")
    
    tooltip = html.escape(f"[{it.get('index')}] {title_str} by {creator_str} (Cluster {it['cluster_id']}: {c_name_str})")
    svg_lines.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="4.5" fill="{color}" fill-opacity="0.8" stroke="#0F172A" stroke-width="0.75"><title>{tooltip}</title></circle>')

# Draw Sidebar / Legend
legend_x = svg_width - 320
legend_y = pad + 10
svg_lines.append(f'<!-- Legend -->')
svg_lines.append(f'<rect x="{legend_x}" y="{pad}" width="300" height="{plot_h}" fill="#1E293B" rx="8" stroke="#334155" stroke-width="1"/>')
svg_lines.append(f'<text x="{legend_x + 16}" y="{pad + 30}" fill="#F8FAFC" font-size="14" font-weight="bold">Aesthetic Clusters (k=10)</text>')

for i in range(k):
    c_def = cluster_definitions[i]
    c_items = [it for it in clustered_items if it["cluster_id"] == c_def["cluster_id"]]
    item_y = pad + 65 + (i * 68)
    color = c_def["color"]
    name_escaped = html.escape(c_def["name"][:32])
    
    svg_lines.append(f'<circle cx="{legend_x + 22}" cy="{item_y}" r="6.5" fill="{color}"/>')
    svg_lines.append(f'<text x="{legend_x + 36}" y="{item_y - 2}" fill="#F1F5F9" font-size="11" font-weight="bold">{c_def["cluster_id"]}. {name_escaped}</text>')
    svg_lines.append(f'<text x="{legend_x + 36}" y="{item_y + 12}" fill="#94A3B8" font-size="10">{len(c_items)} works ({len(c_items)/len(clustered_items):.1%})</text>')

svg_lines.append('</svg>')

svg_path = str(paths.CLUSTERS / "latent_cluster_map.svg")
with open(svg_path, "w", encoding="utf-8") as f:
    f.write("\n".join(svg_lines))
print(f"Saved SVG map to {svg_path}")
