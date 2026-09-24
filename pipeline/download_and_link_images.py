import asyncio
import httpx
import os
import json
import csv
import re
import subprocess
import urllib.request
import urllib.parse
import shutil
import time
import sqlite3

import paths

# Paths. NOTE: images/ was dropped from this repo (third-party, going
# public) — local_img_dir is a scratch download target only, not tracked.
local_img_dir = str(paths.REPO_ROOT / "images")
gdrive_sync_dir = r"<drive-mirror>\Google Arts & Culture"  # historical, Windows/OPTILAB-only
gdrive_img_dir = os.path.join(gdrive_sync_dir, "images") if os.path.exists(gdrive_sync_dir) else None

os.makedirs(local_img_dir, exist_ok=True)
if gdrive_img_dir:
    os.makedirs(gdrive_img_dir, exist_ok=True)

spreadsheet_id = paths.SHEET_ID
parent_folder_id = paths.drive_folder_id()  # GDrive 'Google Arts & Culture' folder
img_folder_id = "REDACTED_DRIVE_FOLDER_ID"    # GDrive 'images' folder

# Load enriched data
json_path = str(paths.DATA / "favorites_enriched.json")
tsv_path = str(paths.DATA / "favorites_enriched.tsv")

with open(json_path, "r", encoding="utf-8") as f:
    favorites = json.load(f)

print(f"Starting Image Collection & Drive Linking for {len(favorites)} artworks...")

# 1. Download all images locally and to GDrive Desktop
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
}

def clean_filename(idx, title, aid):
    title_str = title or "untitled"
    # Clean ASCII slug
    slug = re.sub(r'[^a-zA-Z0-9_\-]+', '-', title_str).strip("-").lower()[:60]
    return f"{idx:04d}_{slug}_{aid}.jpg"

async def download_image(client, semaphore, item, total, progress):
    idx = item["index"]
    aid = item["asset_id"]
    title = item.get("title")
    filename = clean_filename(idx, title, aid)
    filepath = os.path.join(local_img_dir, filename)
    
    # Check if already downloaded and valid
    if os.path.exists(filepath) and os.path.getsize(filepath) > 2000:
        progress["cached"] += 1
        return filename, filepath, os.path.getsize(filepath)
        
    img_url = item.get("max_preview_url") or (item.get("image_url") + "=s1200")
    if not img_url.startswith("http"):
        img_url = "https:" + img_url
        
    async with semaphore:
        for attempt in range(4):
            try:
                resp = await client.get(img_url, timeout=25.0)
                if resp.status_code == 200 and len(resp.content) > 1000:
                    with open(filepath, "wb") as f:
                        f.write(resp.content)
                    if gdrive_img_dir:
                        dest = os.path.join(gdrive_img_dir, filename)
                        with open(dest, "wb") as f:
                            f.write(resp.content)
                    progress["downloaded"] += 1
                    done = progress["downloaded"] + progress["cached"]
                    if done % 50 == 0 or done == total:
                        print(f"  [Image Progress] {done}/{total} saved ({progress['downloaded']} downloaded, {progress['cached']} cached)...")
                    return filename, filepath, len(resp.content)
                elif resp.status_code == 429:
                    await asyncio.sleep(1.5 ** attempt)
            except Exception:
                await asyncio.sleep(1.0)
                
    return filename, None, 0

async def batch_download_all():
    semaphore = asyncio.Semaphore(14)
    progress = {"downloaded": 0, "cached": 0}
    
    start = time.time()
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=30.0) as client:
        tasks = [download_image(client, semaphore, item, len(favorites), progress) for item in favorites]
        results = await asyncio.gather(*tasks)
        
    elapsed = time.time() - start
    print(f"\nDownloaded/verified {len(results)} images in {elapsed:.2f} seconds!")
    return results

# Run Download
download_results = asyncio.run(batch_download_all())

# 2. Query Google Drive API to map Drive File IDs and Web URLs
print("\nFetching Google Drive File IDs and URLs from Drive API...")
token = subprocess.check_output('gcloud auth print-access-token', shell=True, text=True).strip()

def get_all_drive_files(folder_id):
    files_map = {}
    page_token = None
    while True:
        q = urllib.parse.quote(f"'{folder_id}' in parents and trashed = false")
        url = f"https://www.googleapis.com/drive/v3/files?q={q}&pageSize=1000&fields=nextPageToken,files(id,name,webViewLink,size)"
        if page_token:
            url += f"&pageToken={page_token}"
        req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            for f in data.get("files", []):
                files_map[f["name"]] = {
                    "id": f["id"],
                    "webViewLink": f.get("webViewLink")
                }
            page_token = data.get("nextPageToken")
            if not page_token:
                break
    return files_map

drive_files = get_all_drive_files(img_folder_id)
print(f"Drive API returned {len(drive_files)} existing files in 'images' folder.")

# 3. Check for any missing files in Google Drive cloud folder and upload via Drive API
missing_in_drive = []
for filename, filepath, size in download_results:
    if filepath and filename not in drive_files:
        missing_in_drive.append((filename, filepath))

if missing_in_drive:
    print(f"Uploading {len(missing_in_drive)} files directly to Google Drive via API...")
    for i, (fn, fp) in enumerate(missing_in_drive):
        # Multipart upload
        metadata = {"name": fn, "parents": [img_folder_id]}
        with open(fp, "rb") as f:
            f_bytes = f.read()
        boundary = "-------314159265358979323846"
        body = (
            f"--{boundary}\r\n"
            f"Content-Type: application/json; charset=UTF-8\r\n\r\n"
            f"{json.dumps(metadata)}\r\n"
            f"--{boundary}\r\n"
            f"Content-Type: image/jpeg\r\n\r\n"
        ).encode("utf-8") + f_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")
        
        req_up = urllib.request.Request(
            "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name,webViewLink",
            data=body,
            headers={'Authorization': f'Bearer {token}', 'Content-Type': f'multipart/related; boundary={boundary}'},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req_up) as resp:
                up_res = json.loads(resp.read().decode())
                drive_files[fn] = {
                    "id": up_res["id"],
                    "webViewLink": up_res.get("webViewLink")
                }
                if (i + 1) % 50 == 0 or (i + 1) == len(missing_in_drive):
                    print(f"  [Drive Upload] {i+1}/{len(missing_in_drive)} uploaded...")
        except Exception as e:
            time.sleep(0.5)

print(f"\nAll Google Drive files mapped: {len(drive_files)} files.")

# 4. Attach image columns to dataset
final_records = []
for i, item in enumerate(favorites):
    fn, fp, size = download_results[i]
    d_info = drive_files.get(fn, {})
    
    gdrive_id = d_info.get("id")
    gdrive_url = d_info.get("webViewLink") or (f"https://drive.google.com/file/d/{gdrive_id}/view" if gdrive_id else None)
    
    # Inline Google Sheets IMAGE formula
    img_formula = f'=IMAGE("{item["max_preview_url"]}")' if item.get("max_preview_url") else ""
    
    rec = {
        # Visual Thumbnail first in spreadsheet
        "thumbnail_preview": img_formula,
        **item,
        # Image Files & Drive Links
        "local_image_file": f"images/{fn}" if fp else None,
        "gdrive_file_id": gdrive_id,
        "gdrive_image_url": gdrive_url,
    }
    final_records.append(rec)

# Save JSON and TSV
print(f"\nWriting updated JSON: {json_path}")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(final_records, f, ensure_ascii=False, indent=2)

print(f"Writing updated TSV: {tsv_path}")
field_order = list(final_records[0].keys())
with open(tsv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=field_order, delimiter="\t")
    writer.writeheader()
    for r in final_records:
        writer.writerow({k: ("" if r[k] is None else str(r[k])) for k in field_order})

# Copy to GDrive Desktop sync
if gdrive_sync_dir and os.path.exists(gdrive_sync_dir):
    shutil.copy2(json_path, os.path.join(gdrive_sync_dir, "favorites_enriched.json"))
    shutil.copy2(tsv_path, os.path.join(gdrive_sync_dir, "favorites_enriched.tsv"))

# 5. Update Google Sheet
print("\nUpdating Native Google Sheet with Image Columns & Previews...")
token = subprocess.check_output('gcloud auth print-access-token', shell=True, text=True).strip()

req_meta = urllib.request.Request(
    f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}",
    headers={'Authorization': f'Bearer {token}'}
)
with urllib.request.urlopen(req_meta) as resp:
    meta = json.loads(resp.read().decode())

sheet_obj = meta["sheets"][0]
sheet_id = sheet_obj["properties"]["sheetId"]

rows_data = [field_order]
for r in final_records:
    row = [("" if r[k] is None else str(r[k])) for k in field_order]
    rows_data.append(row)

# Expand sheet size
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

# Populate values (USER_ENTERED parses =IMAGE formulas!)
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
    print(f"Populated Google Sheet: {res.get('totalUpdatedRows')} rows, {res.get('totalUpdatedColumns')} columns, {res.get('totalUpdatedCells')} cells.")

# Style Header & Column dimensions
format_requests = [
    # Header format
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
                    "backgroundColor": {"red": 0.05, "green": 0.18, "blue": 0.40},
                    "textFormat": {"foregroundColor": {"red": 1.0, "green": 1.0, "blue": 1.0}, "bold": True, "fontSize": 10},
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
        }
    },
    # Set thumbnail column width to 80px
    {
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": 0,
                "endIndex": 1
            },
            "properties": {
                "pixelSize": 85
            },
            "fields": "pixelSize"
        }
    },
    # Set row heights for visual gallery effect (height: 60px for data rows)
    {
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "ROWS",
                "startIndex": 1,
                "endIndex": len(rows_data)
            },
            "properties": {
                "pixelSize": 55
            },
            "fields": "pixelSize"
        }
    },
    # Auto-resize remaining columns
    {
        "autoResizeDimensions": {
            "dimensions": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": 1,
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
    print("Formatting applied successfully!")

print("\n==========================================")
print("     ALL IMAGES DOWNLOADED & LINKED       ")
print("==========================================")
print(f"1. Local Images Directory: {local_img_dir}")
print(f"2. Google Drive Images:    {gdrive_img_dir}")
print(f"3. Google Sheet:           https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")
