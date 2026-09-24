import json
import csv
import os
import re
import sqlite3
import shutil
import urllib.request
import subprocess

import paths

local_img_dir = str(paths.REPO_ROOT / "images")  # historical: images/ was dropped from this repo
catalogue_dir = str(paths.CATALOGUE)
os.makedirs(catalogue_dir, exist_ok=True)

gdrive_sync_dir = r"<drive-mirror>\Google Arts & Culture"  # historical, Windows/OPTILAB-only
gdrive_catalogue_dir = os.path.join(gdrive_sync_dir, "catalogue") if os.path.exists(gdrive_sync_dir) else None
if gdrive_catalogue_dir:
    os.makedirs(gdrive_catalogue_dir, exist_ok=True)

db_path = r"%USERPROFILE%\.gemini\antigravity\brain\agy-session-2287\scratch\multimodal_analysis.db"  # historical, Windows/OPTILAB-only
spreadsheet_id = paths.SHEET_ID

# 1. Load SQLite cache
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("SELECT index_num, json_result FROM analysis_cache")
results_map = {}
for row in c.fetchall():
    try:
        results_map[row[0]] = json.loads(row[1])
    except Exception:
        pass

print(f"Loaded {len(results_map)} analyses from SQLite cache.")

# Load favorites dataset
with open(str(paths.DATA / "favorites_enriched.json"), "r", encoding="utf-8") as f:
    favorites = json.load(f)

# Build analyzed dataset
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
        "precept_critique": critique_obj.get("precept_critique") or "",
        "design_heuristics": heuristics_str,
        "extracted_palette": palette_str,
        "chromatic_temperature": color_obj.get("chromatic_temperature") or "",
        "light_profile": color_obj.get("light_source_profile") or "",
        "contrast_level": color_obj.get("contrast_level") or "",
        "focal_flow": critique_obj.get("visual_composition", {}).get("focal_flow") or "",
        "framing_density": critique_obj.get("visual_composition", {}).get("framing_density") or "",
        "spatial_depth": critique_obj.get("texture_and_materiality", {}).get("spatial_depth_handling") or "",
    }
    enriched_analyzed.append(rec)

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
    print(f"Synced datasets to Google Drive Desktop: {gdrive_sync_dir}")

# 2. Generate 800 Catalogue Markdown Notes
print("\nGenerating Catalogue Markdown notes in catalogue/...")
generated_count = 0
for item in enriched_analyzed:
    idx = item["index"]
    aid = item.get("asset_id") or ""
    raw_title = item.get("title")
    title = raw_title.strip() if raw_title else "Untitled"
    creator = item.get("creator") or "Unknown"
    date = item.get("date_created") or "Unknown"
    critique_obj = results_map.get(idx) or {}
    
    slug = re.sub(r'[^a-zA-Z0-9_\-]+', '-', title).strip("-").lower()[:50]
    if not slug:
        slug = "untitled"
    filename = f"{idx:04d}_{slug}_{aid}.md"
    file_path = os.path.join(catalogue_dir, filename)
    
    heuristics = critique_obj.get("design_heuristics", [])
    heuristics_md = "\n".join([f"- {h}" for h in heuristics]) if heuristics else "- None extracted"
    
    symbols = critique_obj.get("semiotics_and_emotion", {}).get("core_symbols", [])
    symbols_md = ", ".join(symbols) if symbols else "None"
    
    motifs = critique_obj.get("design_vernacular", {}).get("structural_motifs", [])
    motifs_md = ", ".join(motifs) if motifs else "None"

    local_img = item.get("local_image_file") or f"images/{idx:04d}_{slug}_{aid}.jpg"

    note_content = f"""---
index: {idx}
asset_id: "{aid}"
title: "{title.replace('"', "''")}"
creator: "{creator.replace('"', "''")}"
date_created: "{date.replace('"', "''")}"
medium: "{str(item.get('medium') or '').replace('"', "''")}"
aspect_ratio: {item.get('aspect_ratio') or 'null'}
aspect_ratio_standard: "{item.get('aspect_ratio_standard') or ''}"
orientation: "{item.get('orientation') or ''}"
partner_name: "{str(item.get('partner_name') or '').replace('"', "''")}"
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
**Date**: {date} | **Holding Museum**: {item.get('partner_name') or 'Unknown'}  
**Physical Dimensions**: {item.get('physical_dimensions_raw') or 'Unknown'} | **Medium**: {item.get('medium') or 'Unknown'}

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
    
    if gdrive_catalogue_dir:
        dest_gdrive_note = os.path.join(gdrive_catalogue_dir, filename)
        with open(dest_gdrive_note, "w", encoding="utf-8") as gnf:
            gnf.write(note_content)
            
    generated_count += 1

print(f"Generated {generated_count} Catalogue Markdown notes.")

# 3. Update Google Sheet
print("\nUpdating Google Sheet with Precept Critiques & Heuristics...")
def get_token():
    return subprocess.check_output('gcloud auth print-access-token', shell=True, text=True).strip()

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

print("\n--- COMPLETE ---")
print(f"Spreadsheet: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")
