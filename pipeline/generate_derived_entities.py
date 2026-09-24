import json
import csv
import os
import re
import subprocess
import urllib.request
import urllib.parse
import shutil

import paths

gdrive_sync_dir = r"<drive-mirror>\Google Arts & Culture"  # historical, Windows/OPTILAB-only
json_path = str(paths.DATA / "favorites_enriched.json")
tsv_path = str(paths.DATA / "favorites_enriched.tsv")
spreadsheet_id = paths.SHEET_ID

# Load enriched data
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Loaded {len(data)} items for derived entity generation.")

# Load raw favorites for data_ia access
raw_json_path = str(paths.DATA / "favorites.json")
with open(raw_json_path, "r", encoding="utf-8") as f:
    raw_favs = json.load(f)

data_ia_map = {item["asset_id"]: item.get("data_ia") for item in raw_favs if item.get("asset_id")}

def parse_fraction(val_str):
    parts = val_str.strip().split()
    total = 0.0
    for p in parts:
        if "/" in p:
            num, den = p.split("/")
            total += float(num) / float(den)
        else:
            total += float(p)
    return total

def parse_dimensions(dim_str):
    if not dim_str:
        return None, None, None
    s = dim_str.strip()
    
    # 1. w... x h... cm
    m_wh_cm = re.search(r"w\s*([0-9\.]+)\s*x\s*h\s*([0-9\.]+)\s*cm", s, re.I)
    if m_wh_cm:
        return round(float(m_wh_cm.group(2)), 2), round(float(m_wh_cm.group(1)), 2), None
        
    m_hw_cm = re.search(r"h\s*([0-9\.]+)\s*x\s*w\s*([0-9\.]+)\s*cm", s, re.I)
    if m_hw_cm:
        return round(float(m_hw_cm.group(1)), 2), round(float(m_hw_cm.group(2)), 2), None
        
    # Standard H x W [x D] cm
    m_cm = re.search(r"([0-9\.]+)\s*(?:[x×]|by)\s*([0-9\.]+)(?:\s*(?:[x×]|by)\s*([0-9\.]+))?\s*cm", s, re.I)
    if m_cm:
        h = float(m_cm.group(1))
        w = float(m_cm.group(2))
        d = float(m_cm.group(3)) if m_cm.group(3) else None
        return round(h, 2), round(w, 2), round(d, 2) if d else None
        
    # mm
    m_wh_mm = re.search(r"w\s*([0-9\.]+)\s*x\s*h\s*([0-9\.]+)\s*mm", s, re.I)
    if m_wh_mm:
        return round(float(m_wh_mm.group(2)) / 10.0, 2), round(float(m_wh_mm.group(1)) / 10.0, 2), None
        
    m_mm = re.search(r"([0-9\.]+)\s*(?:[x×]|by)\s*([0-9\.]+)(?:\s*(?:[x×]|by)\s*([0-9\.]+))?\s*mm", s, re.I)
    if m_mm:
        h = float(m_mm.group(1)) / 10.0
        w = float(m_mm.group(2)) / 10.0
        d = (float(m_mm.group(3)) / 10.0) if m_mm.group(3) else None
        return round(h, 2), round(w, 2), round(d, 2) if d else None
        
    # inches
    m_in = re.search(r"([0-9\s/]+)\s*(?:[x×]|by)\s*([0-9\s/]+)(?:\s*(?:[x×]|by)\s*([0-9\s/]+))?\s*(?:in|inches|\")", s, re.I)
    if m_in:
        try:
            h = parse_fraction(m_in.group(1)) * 2.54
            w = parse_fraction(m_in.group(2)) * 2.54
            d = (parse_fraction(m_in.group(3)) * 2.54) if m_in.group(3) else None
            return round(h, 2), round(w, 2), round(d, 2) if d else None
        except Exception:
            pass

    return None, None, None

def get_standard_ratio_label(ar):
    if ar is None:
        return None
    # Compare with common standard aspect ratios
    known_ratios = [
        (1.0, "1:1 (Square)"),
        (4/3, "4:3 (Standard)"),
        (3/2, "3:2 (Classic 35mm)"),
        (16/9, "16:9 (Widescreen)"),
        (16/10, "16:10"),
        (2.0, "2:1 (Univisium)"),
        (2.35, "21:9 (Cinemascope)"),
        (3.0, "3:1 (Panoramic)"),
        (3/4, "3:4 (Portrait)"),
        (2/3, "2:3 (Portrait)"),
        (9/16, "9:16 (Vertical)"),
        (1/2, "1:2 (Tall Vertical)"),
    ]
    for ratio_val, label in known_ratios:
        if abs(ar - ratio_val) <= 0.04:
            return label
    return f"{ar:.2f}:1"

def get_orientation(ar):
    if ar is None:
        return None
    if ar >= 2.0:
        return "Panoramic (Landscape)"
    elif ar > 1.05:
        return "Landscape"
    elif ar >= 0.95:
        return "Square"
    elif ar >= 0.5:
        return "Portrait"
    else:
        return "Panoramic (Portrait / Vertical Scroll)"

updated_records = []
for item in data:
    aid = item["asset_id"]
    data_ia = data_ia_map.get(aid)
    
    # 1. Master pixel dimensions from data_ia
    master_w, master_h = None, None
    focal_count = None
    if data_ia:
        nums = [int(x) for x in data_ia.split(",") if x.strip().isdigit()]
        if len(nums) >= 2:
            master_w = nums[0]
            master_h = nums[1]
            if len(nums) > 2:
                focal_count = (len(nums) - 2) // 4
                
    # Megapixels
    megapixels = round((master_w * master_h) / 1_000_000, 2) if (master_w and master_h) else None
    
    # 2. Aspect ratio
    ar = item.get("aspect_ratio")
    if ar is None and master_w and master_h:
        ar = round(master_w / master_h, 4)
        
    ar_label = get_standard_ratio_label(ar)
    orientation = get_orientation(ar)
    
    # 3. Physical dimensions parsing
    raw_dim = item.get("physical_dimensions")
    parsed_h_cm, parsed_w_cm, parsed_d_cm = parse_dimensions(raw_dim)
    
    # If aspect ratio is still None, compute from physical dimensions
    if ar is None and parsed_w_cm and parsed_h_cm and parsed_h_cm > 0:
        ar = round(parsed_w_cm / parsed_h_cm, 4)
        ar_label = get_standard_ratio_label(ar)
        orientation = get_orientation(ar)
        
    # 4. Scan Density (DPI)
    dpi = None
    if master_w and parsed_w_cm and parsed_w_cm > 0:
        width_inches = parsed_w_cm / 2.54
        dpi = round(master_w / width_inches, 1)
        
    # 5. Image Delivery URLs
    base_img = item.get("image_url")
    max_preview_url = (base_img + "=s1200") if base_img else None
    
    # Build updated record with logical grouping
    rec = {
        "index": item["index"],
        "title": item["title"],
        "original_title": item.get("original_title"),
        "creator": item.get("creator"),
        "creator_lifespan": item.get("creator_lifespan"),
        "creator_nationality": item.get("creator_nationality"),
        "date_created": item.get("date_created"),
        "location_created": item.get("location_created"),
        "medium": item.get("medium"),
        "object_type": item.get("object_type"),
        
        # Dimensions & Ratios
        "aspect_ratio": ar,
        "aspect_ratio_standard": ar_label,
        "orientation": orientation,
        "master_width_px": master_w,
        "master_height_px": master_h,
        "megapixels": megapixels,
        "focal_anchors_count": focal_count,
        "physical_dimensions_raw": raw_dim,
        "parsed_height_cm": parsed_h_cm,
        "parsed_width_cm": parsed_w_cm,
        "parsed_depth_cm": parsed_d_cm,
        "resolution_density_dpi": dpi,
        
        # Museum / Partner
        "partner_name": item.get("partner_name"),
        "partner_city_country": item.get("partner_city_country"),
        "partner_website": item.get("partner_website"),
        "partner_lat": item.get("partner_lat"),
        "partner_long": item.get("partner_long"),
        
        # Curatorial & Rights
        "curatorial_description": item.get("curatorial_description"),
        "provenance": item.get("provenance"),
        "credit_line": item.get("credit_line"),
        "inventory_number": item.get("inventory_number"),
        "external_catalog_url": item.get("external_catalog_url"),
        "rights": item.get("rights"),
        "art_movements": item.get("art_movements"),
        "tags_and_topics": item.get("tags_and_topics"),
        "dominant_color": item.get("dominant_color"),
        
        # Linked Open Data & URLs
        "wikidata_qid": item.get("wikidata_qid"),
        "wikipedia_url": item.get("wikipedia_url"),
        "commons_image_url": item.get("commons_image_url"),
        "asset_id": aid,
        "link": item["link"],
        "image_url": base_img,
        "max_preview_url": max_preview_url,
    }
    updated_records.append(rec)

# Write updated files
print(f"Writing updated JSON: {json_path}")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(updated_records, f, ensure_ascii=False, indent=2)

print(f"Writing updated TSV: {tsv_path}")
field_order = list(updated_records[0].keys())
with open(tsv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=field_order, delimiter="\t")
    writer.writeheader()
    for r in updated_records:
        writer.writerow({k: ("" if r[k] is None else str(r[k])) for k in field_order})

# Copy to GDrive sync
if os.path.exists(gdrive_sync_dir):
    print(f"Copying to Google Drive sync: {gdrive_sync_dir}")
    shutil.copy2(json_path, os.path.join(gdrive_sync_dir, "favorites_enriched.json"))
    shutil.copy2(tsv_path, os.path.join(gdrive_sync_dir, "favorites_enriched.tsv"))

# Update Google Sheet
print("\nUpdating Native Google Sheet...")
token = subprocess.check_output('gcloud auth print-access-token', shell=True, text=True).strip()

req_meta = urllib.request.Request(
    f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}",
    headers={'Authorization': f'Bearer {token}'}
)
with urllib.request.urlopen(req_meta) as resp:
    meta = json.loads(resp.read().decode())

sheet_obj = meta["sheets"][0]
sheet_id = sheet_obj["properties"]["sheetId"]
sheet_title = sheet_obj["properties"]["title"]

rows_data = [field_order]
for r in updated_records:
    row = [("" if r[k] is None else str(r[k])) for k in field_order]
    rows_data.append(row)

# 1. Expand sheet size
expand_body = {
    "requests": [
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "title": "Enriched Favorites",
                    "gridProperties": {
                        "rowCount": len(rows_data) + 20,
                        "columnCount": len(field_order) + 5,
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

# 2. Populate values
val_body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {
            "range": "'Enriched Favorites'!A1",
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
    print(f"Updated Google Sheet: {res.get('totalUpdatedRows')} rows, {res.get('totalUpdatedColumns')} columns, {res.get('totalUpdatedCells')} cells.")

# 3. Format Header, alignment, auto-resize
print("Applying Google Sheet styling...")
format_requests = [
    # Header format: Dark Navy (#102a43), bold white text, center aligned
    {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 0,
                "endColumnIndex": len(field_order)
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {"red": 0.06, "green": 0.20, "blue": 0.45},
                    "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontSize": 10},
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
        }
    },
    # Center index column
    {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 1,
                "endRowIndex": len(rows_data),
                "startColumnIndex": 0,
                "endColumnIndex": 1
            },
            "cell": {
                "userEnteredFormat": {"horizontalAlignment": "CENTER"}
            },
            "fields": "userEnteredFormat(horizontalAlignment)"
        }
    },
    # Auto-resize columns
    {
        "autoResizeDimensions": {
            "dimensions": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": 0,
                "endIndex": len(field_order)
            }
        }
    }
]

fmt_req = urllib.request.Request(
    f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate",
    data=json.dumps({"requests": format_requests}).encode("utf-8"),
    headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
    method="POST"
)
with urllib.request.urlopen(fmt_req) as resp:
    print("Styling applied successfully!")

print("\n--- DERIVED ENTITIES PIPELINE COMPLETE ---")
print(f"Spreadsheet URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")
