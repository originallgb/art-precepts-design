import asyncio
import httpx
import json
import csv
import os
import re
import base64
import sqlite3
import subprocess
import time
import shutil
import urllib.request

import paths

# Configuration
project_id = paths.gcp_project_id()
location = "us-central1"
model = "gemini-2.5-flash"
endpoint_url = f"https://{location}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{location}/publishers/google/models/{model}:generateContent"

local_img_dir = str(paths.REPO_ROOT / "images")  # historical: images/ was dropped from this repo
catalogue_dir = str(paths.CATALOGUE)
os.makedirs(catalogue_dir, exist_ok=True)

gdrive_sync_dir = r"<drive-mirror>\Google Arts & Culture"  # historical, Windows/OPTILAB-only
gdrive_catalogue_dir = os.path.join(gdrive_sync_dir, "catalogue") if os.path.exists(gdrive_sync_dir) else None
if gdrive_catalogue_dir:
    os.makedirs(gdrive_catalogue_dir, exist_ok=True)

db_path = r"<agy-session>\scratch\multimodal_analysis.db"  # historical, Windows/OPTILAB-only
spreadsheet_id = paths.SHEET_ID

# 1. Initialize SQLite Cache
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS analysis_cache (
    index_num INTEGER PRIMARY KEY,
    asset_id TEXT,
    title TEXT,
    json_result TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Seed SQLite with pilot results if available
pilot_path = r"<agy-session>\scratch\pilot_results.json"  # historical, Windows/OPTILAB-only
if os.path.exists(pilot_path):
    with open(pilot_path, "r", encoding="utf-8") as f:
        pilot_data = json.load(f)
    for p in pilot_data:
        c.execute("INSERT OR REPLACE INTO analysis_cache (index_num, asset_id, title, json_result) VALUES (?, ?, ?, ?)",
                  (p["index"], "", p["title"], json.dumps(p["critique"])))
    conn.commit()

# Load favorites dataset
with open(str(paths.DATA / "favorites_enriched.json"), "r", encoding="utf-8") as f:
    favorites = json.load(f)

print(f"Total favorites to process: {len(favorites)}")

system_prompt = """You are an elite design critic and architectural visual analyst.
Your task is to analyze the provided visual artwork and its curatorial metadata to extract foundational Design Precepts and actionable Design Heuristics.

Evaluate the work through 5 rigorous, distinct Angles:
1. Composition & Lineage: Underlying geometric grid, visual hierarchy, focal flow, balance, and historical lineage.
2. Utility & Ergonomics: If translated into a digital interface, physical product, or spatial system, what are its affordances, focus-directing mechanisms, and structural rules?
3. Visual Language & Semiotics: Visual signifiers, symbolic encoding, narrative friction, and emotional valence beyond the literal depiction.
4. Light, Space & Materiality: Light/shadow dynamics, void vs. mass (negative space handling), spatial perspective, and tactile surface qualities.
5. Color & Typography: Palette balance, contrast profiles, chromatic temperatures (with exact hex codes), and typographic/calligraphic weight.

CRITICAL TONE DIRECTIVES:
- BAN ALL ART-CRITICAL CLICHÉS AND GENERIC FILLER (e.g. "stunning study in contrasts", "captivating brushwork", "breathtaking", "seamless blend", "poignant testament").
- Use precise, analytical, and technical vocabulary.
- Focus entirely on what a software designer, visual architect, or product engineer can extract and apply.
"""

response_schema = {
    "type": "OBJECT",
    "properties": {
        "visual_composition": {
            "type": "OBJECT",
            "properties": {
                "focal_flow": {"type": "STRING", "description": "How the viewer's eye travels across the composition"},
                "geometric_structure": {"type": "STRING", "description": "Underlying geometric grid or framing structure"},
                "symmetry_balance": {"type": "STRING", "description": "Symmetry and distribution of visual weight"},
                "framing_density": {"type": "STRING", "enum": ["sparse", "balanced", "dense", "claustrophobic"]}
            },
            "required": ["focal_flow", "geometric_structure", "symmetry_balance", "framing_density"]
        },
        "color_and_light": {
            "type": "OBJECT",
            "properties": {
                "palette_hex": {
                    "type": "ARRAY",
                    "items": {"type": "STRING"},
                    "description": "5 dominant hex color codes extracted from the image"
                },
                "chromatic_temperature": {"type": "STRING", "enum": ["warm", "neutral", "cool", "mixed"]},
                "light_source_profile": {"type": "STRING", "enum": ["diffuse", "chiaroscuro", "direct", "ambient", "luminescent"]},
                "contrast_level": {"type": "STRING", "enum": ["low", "medium", "high", "extreme"]}
            },
            "required": ["palette_hex", "chromatic_temperature", "light_source_profile", "contrast_level"]
        },
        "texture_and_materiality": {
            "type": "OBJECT",
            "properties": {
                "perceived_surface": {"type": "STRING", "description": "Tactile surface quality (e.g. matte, toothy paper, glazed oil, woven canvas)"},
                "material_honesty": {"type": "STRING", "description": "How honestly the medium reveals its physical tools and substrates"},
                "spatial_depth_handling": {"type": "STRING", "enum": ["flat_graphic", "layered_shallow", "deep_perspective", "atmospheric_void"]}
            },
            "required": ["perceived_surface", "material_honesty", "spatial_depth_handling"]
        },
        "semiotics_and_emotion": {
            "type": "OBJECT",
            "properties": {
                "core_symbols": {"type": "ARRAY", "items": {"type": "STRING"}},
                "emotional_valence": {"type": "STRING", "description": "Psychological tension or emotional mood"},
                "narrative_themes": {"type": "ARRAY", "items": {"type": "STRING"}}
            },
            "required": ["core_symbols", "emotional_valence", "narrative_themes"]
        },
        "design_vernacular": {
            "type": "OBJECT",
            "properties": {
                "historical_lineage": {"type": "ARRAY", "items": {"type": "STRING"}},
                "structural_motifs": {"type": "ARRAY", "items": {"type": "STRING"}},
                "typographic_cues": {"type": "STRING", "description": "Observations on letterforms, annotations, or calligraphic rhythm"}
            },
            "required": ["historical_lineage", "structural_motifs", "typographic_cues"]
        },
        "precept_critique": {
            "type": "STRING",
            "description": "Exactly three rigorous, dense sentences identifying why this piece matters to a designer, avoiding all clichés."
        },
        "design_heuristics": {
            "type": "ARRAY",
            "items": {"type": "STRING"},
            "description": "3 to 5 concrete design rules, UI patterns, or spatial guidelines derived from this artwork"
        }
    },
    "required": [
        "visual_composition",
        "color_and_light",
        "texture_and_materiality",
        "semiotics_and_emotion",
        "design_vernacular",
        "precept_critique",
        "design_heuristics"
    ]
}

# Image file map by 4-digit prefix
image_files = os.listdir(local_img_dir)
img_by_prefix = {}
for fn in image_files:
    pfx = fn[:4]
    if pfx.isdigit():
        img_by_prefix[int(pfx)] = os.path.join(local_img_dir, fn)

def get_token():
    return subprocess.check_output('gcloud auth print-access-token', shell=True, text=True).strip()

async def analyze_item(client, semaphore, item, token, progress, lock):
    idx = item["index"]
    aid = item.get("asset_id", "")
    title = item.get("title", "Untitled")
    
    # Check cache first
    with lock:
        c.execute("SELECT json_result FROM analysis_cache WHERE index_num = ?", (idx,))
        row = c.fetchone()
        if row:
            progress["cached"] += 1
            progress["done"] += 1
            if progress["done"] % 25 == 0 or progress["done"] == progress["total"]:
                print(f"  [Progress] {progress['done']}/{progress['total']} ({progress['cached']} cached, {progress['analyzed']} analyzed)...")
            return idx, json.loads(row[0])

    img_path = img_by_prefix.get(idx)
    if not img_path or not os.path.exists(img_path):
        progress["done"] += 1
        return idx, None

    with open(img_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    creator = item.get("creator") or "Unknown"
    date = item.get("date_created") or "Unknown"
    medium = item.get("medium") or "Unknown"
    partner = item.get("partner_name") or "Unknown"
    desc = item.get("curatorial_description") or ""

    prompt_text = f"""Analyze this artwork from the Catalogue:
Title: {title}
Creator: {creator}
Date Created: {date}
Medium: {medium}
Holding Institution: {partner}
Dimensions: {item.get('physical_dimensions_raw')}
Aspect Ratio: {item.get('aspect_ratio')} ({item.get('aspect_ratio_standard')})
Curatorial Description: {desc}

Perform the 5-Angle analysis and output the requested JSON schema."""

    body = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"inlineData": {"mimeType": "image/jpeg", "data": img_b64}},
                    {"text": prompt_text}
                ]
            }
        ],
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }
    }

    async with semaphore:
        for attempt in range(4):
            try:
                resp = await client.post(
                    endpoint_url,
                    json=body,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    },
                    timeout=35.0
                )
                if resp.status_code == 200:
                    res_json = resp.json()
                    raw_text = res_json["candidates"][0]["content"]["parts"][0]["text"]
                    parsed = json.loads(raw_text)
                    
                    with lock:
                        c.execute("INSERT OR REPLACE INTO analysis_cache (index_num, asset_id, title, json_result) VALUES (?, ?, ?, ?)",
                                  (idx, aid, title, json.dumps(parsed)))
                        conn.commit()
                        
                    progress["analyzed"] += 1
                    progress["done"] += 1
                    if progress["done"] % 25 == 0 or progress["done"] == progress["total"]:
                        print(f"  [Progress] {progress['done']}/{progress['total']} ({progress['cached']} cached, {progress['analyzed']} analyzed)...")
                    return idx, parsed
                elif resp.status_code == 429:
                    await asyncio.sleep(2.0 ** attempt)
                else:
                    await asyncio.sleep(1.0)
            except Exception as e:
                await asyncio.sleep(1.5)
                
    progress["done"] += 1
    return idx, None

async def run_batch():
    token = get_token()
    semaphore = asyncio.Semaphore(10) # 10 concurrent requests
    progress = {"total": len(favorites), "done": 0, "cached": 0, "analyzed": 0}
    lock = asyncio.Lock()
    
    # We need a standard threading lock or single thread for SQLite
    import threading
    sql_lock = threading.Lock()
    
    print(f"\n--- Launching Interactive Multimodal Vision Pipeline for {len(favorites)} Artworks ---")
    start = time.time()
    
    limits = httpx.Limits(max_keepalive_connections=12, max_connections=15)
    async with httpx.AsyncClient(limits=limits, timeout=40.0) as client:
        tasks = [analyze_item(client, semaphore, item, token, progress, sql_lock) for item in favorites]
        results = await asyncio.gather(*tasks)
        
    elapsed = time.time() - start
    print(f"\nAll {len(results)} items processed in {elapsed:.2f} seconds ({progress['analyzed']} analyzed, {progress['cached']} cached)!")
    return dict(results)

# Run batch
results_map = asyncio.run(run_batch())

# 2. Build Enriched Dataset with Precept Critiques & Heuristics
print("\nMerging analyses into analyzed datasets...")
enriched_analyzed = []
for item in favorites:
    idx = item["index"]
    critique_obj = results_map.get(idx) or {}
    
    heuristics = critique_obj.get("design_heuristics", [])
    heuristics_str = " | ".join(heuristics) if heuristics else ""
    
    color_obj = critique_obj.get("color_and_light", {})
    palette = color_obj.get("palette_hex", [])
    palette_str = ", ".join(palette) if palette else ""
    
    rec = {
        **item,
        "precept_critique": critique_obj.get("precept_critique"),
        "design_heuristics": heuristics_str,
        "extracted_palette": palette_str,
        "chromatic_temperature": color_obj.get("chromatic_temperature"),
        "light_profile": color_obj.get("light_source_profile"),
        "contrast_level": color_obj.get("contrast_level"),
        "focal_flow": critique_obj.get("visual_composition", {}).get("focal_flow"),
        "framing_density": critique_obj.get("visual_composition", {}).get("framing_density"),
        "spatial_depth": critique_obj.get("texture_and_materiality", {}).get("spatial_depth_handling"),
    }
    enriched_analyzed.append(rec)

# Save JSON and TSV
json_out = str(paths.DATA / "favorites_analyzed.json")
tsv_out = str(paths.DATA / "favorites_analyzed.tsv")

with open(json_out, "w", encoding="utf-8") as f:
    json.dump(enriched_analyzed, f, ensure_ascii=False, indent=2)
print(f"Saved: {json_out}")

fieldnames = list(enriched_analyzed[0].keys())
with open(tsv_out, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter="\t")
    writer.writeheader()
    for r in enriched_analyzed:
        writer.writerow({k: ("" if r[k] is None else str(r[k])) for k in fieldnames})
print(f"Saved: {tsv_out}")

# Sync to Google Drive
if os.path.exists(gdrive_sync_dir):
    shutil.copy2(json_out, os.path.join(gdrive_sync_dir, "favorites_analyzed.json"))
    shutil.copy2(tsv_out, os.path.join(gdrive_sync_dir, "favorites_analyzed.tsv"))
    print(f"Synced analyzed datasets to Google Drive Desktop: {gdrive_sync_dir}")

# 3. Generate 800 Catalogue Markdown Notes
print("\nGenerating 800 Catalogue Markdown notes in catalogue/...")
for item in enriched_analyzed:
    idx = item["index"]
    aid = item.get("asset_id", "")
    title = item.get("title", "Untitled")
    creator = item.get("creator", "Unknown")
    date = item.get("date_created", "Unknown")
    critique_obj = results_map.get(idx) or {}
    
    # Slug filename
    slug = re.sub(r'[^a-zA-Z0-9_\-]+', '-', title).strip("-").lower()[:50]
    filename = f"{idx:04d}_{slug}_{aid}.md"
    file_path = os.path.join(catalogue_dir, filename)
    
    heuristics = critique_obj.get("design_heuristics", [])
    heuristics_md = "\n".join([f"- {h}" for h in heuristics]) if heuristics else "- None extracted"
    
    symbols = critique_obj.get("semiotics_and_emotion", {}).get("core_symbols", [])
    symbols_md = ", ".join(symbols) if symbols else "None"
    
    motifs = critique_obj.get("design_vernacular", {}).get("structural_motifs", [])
    motifs_md = ", ".join(motifs) if motifs else "None"

    # Relative path to image
    local_img = item.get("local_image_file") or f"images/{idx:04d}_{slug}_{aid}.jpg"

    note_content = f"""---
index: {idx}
asset_id: "{aid}"
title: "{title}"
creator: "{creator}"
date_created: "{date}"
medium: "{item.get('medium') or ''}"
aspect_ratio: {item.get('aspect_ratio') or 'null'}
aspect_ratio_standard: "{item.get('aspect_ratio_standard') or ''}"
orientation: "{item.get('orientation') or ''}"
partner_name: "{item.get('partner_name') or ''}"
dominant_color: "{item.get('dominant_color') or ''}"
chromatic_temperature: "{item.get('chromatic_temperature') or ''}"
contrast_level: "{item.get('contrast_level') or ''}"
framing_density: "{item.get('framing_density') or ''}"
spatial_depth: "{item.get('spatial_depth') or ''}"
gdrive_file_id: "{item.get('gdrive_file_id') or ''}"
wikidata_qid: "{item.get('wikidata_qid') or ''}"
---

# [{idx:04d}] {title}
**Creator**: {creator}  
**Date**: {date} | **Holding Museum**: {item.get('partner_name')}  
**Physical Dimensions**: {item.get('physical_dimensions_raw')} | **Medium**: {item.get('medium')}

![{title}](../{local_img})

---

## Precept Critique
{critique_obj.get('precept_critique', 'No critique available.')}

---

## Actionable Design Heuristics
{heuristics_md}

---

## The 5 Evaluative Angles

### 1. Composition & Lineage
- **Focal Flow**: {critique_obj.get('visual_composition', {}).get('focal_flow', 'N/A')}
- **Geometric Structure**: {critique_obj.get('visual_composition', {}).get('geometric_structure', 'N/A')}
- **Symmetry & Balance**: {critique_obj.get('visual_composition', {}).get('symmetry_balance', 'N/A')}
- **Framing Density**: {critique_obj.get('visual_composition', {}).get('framing_density', 'N/A')}
- **Historical Lineage**: {', '.join(critique_obj.get('design_vernacular', {}).get('historical_lineage', []))}

### 2. Utility & Ergonomics
- **Structural Motifs**: {motifs_md}
- **Affordance Takeaway**: High utility for framing, content pacing, and visual hierarchy.

### 3. Visual Language & Semiotics
- **Core Symbols**: {symbols_md}
- **Emotional Valence**: {critique_obj.get('semiotics_and_emotion', {}).get('emotional_valence', 'N/A')}
- **Narrative Themes**: {', '.join(critique_obj.get('semiotics_and_emotion', {}).get('narrative_themes', []))}

### 4. Light, Space & Materiality
- **Light Profile**: {critique_obj.get('color_and_light', {}).get('light_source_profile', 'N/A')}
- **Surface Quality**: {critique_obj.get('texture_and_materiality', {}).get('perceived_surface', 'N/A')}
- **Spatial Depth**: {critique_obj.get('texture_and_materiality', {}).get('spatial_depth_handling', 'N/A')}
- **Material Honesty**: {critique_obj.get('texture_and_materiality', {}).get('material_honesty', 'N/A')}

### 5. Color & Typography
- **Palette**: `{item.get('extracted_palette') or 'N/A'}`
- **Contrast**: {critique_obj.get('color_and_light', {}).get('contrast_level', 'N/A')}
- **Typographic Cues**: {critique_obj.get('design_vernacular', {}).get('typographic_cues', 'N/A')}

---

## User Notes & Project Overrides
*Add personal reflections, project assignments, or aesthetic tags here.*
"""
    with open(file_path, "w", encoding="utf-8") as nf:
        nf.write(note_content)
    
    # Copy to GDrive sync if available
    if gdrive_catalogue_dir:
        dest_gdrive_note = os.path.join(gdrive_catalogue_dir, filename)
        with open(dest_gdrive_note, "w", encoding="utf-8") as gnf:
            gnf.write(note_content)

print(f"Generated {len(enriched_analyzed)} Catalogue Markdown notes.")

# 4. Update Google Sheet
print("\nUpdating Google Sheet with Precept Critiques & Heuristics...")
token = get_token()
req_meta = urllib.request.Request(
    f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}",
    headers={'Authorization': f'Bearer {token}'}
)
with urllib.request.urlopen(req_meta) as resp:
    meta = json.loads(resp.read().decode())

sheet_obj = meta["sheets"][0]
sheet_id = sheet_obj["properties"]["sheetId"]

rows_data = [fieldnames]
for r in enriched_analyzed:
    row = [("" if r[k] is None else str(r[k])) for k in fieldnames]
    rows_data.append(row)

# Expand sheet
expand_body = {
    "requests": [
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "title": "Catalogue Precepts",
                    "gridProperties": {
                        "rowCount": len(rows_data) + 20,
                        "columnCount": len(fieldnames) + 5,
                        "frozenRowCount": 1
                    }
                },
                "fields": "title,gridProperties"
            }
        }
    ]
}
req_expand = urllib.request.Request(
    f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate",
    data=json.dumps(expand_body).encode("utf-8"),
    headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
    method="POST"
)
with urllib.request.urlopen(req_expand) as resp:
    pass

# Populate values
val_body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {
            "range": "'Catalogue Precepts'!A1",
            "majorDimension": "ROWS",
            "values": rows_data
        }
    ]
}
req_val = urllib.request.Request(
    f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values:batchUpdate",
    data=json.dumps(val_body).encode("utf-8"),
    headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
    method="POST"
)
with urllib.request.urlopen(req_val) as resp:
    res = json.loads(resp.read().decode())
    print(f"Populated Google Sheet: {res.get('totalUpdatedRows')} rows, {res.get('totalUpdatedColumns')} columns, {res.get('totalUpdatedCells')} cells.")

print("\n--- FULL MULTIMODAL PIPELINE COMPLETE ---")
print(f"Spreadsheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")
