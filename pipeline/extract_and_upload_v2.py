import email
from email import policy
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import subprocess
import os
import json
import csv
import shutil
import time

import paths

mhtml_path = r"%USERPROFILE%\Downloads\Your favorites — Google Arts & Culture.mhtml"  # historical, one-time source download
local_dir = str(paths.DATA)
gdrive_sync_dir = r"<drive-mirror>\Google Arts & Culture"  # historical, Windows/OPTILAB-only

print("1. Parsing MHTML file...")
with open(mhtml_path, "rb") as f:
    msg = email.message_from_binary_file(f, policy=policy.default)

for part in msg.walk():
    if part.get_content_type() == "text/html":
        html = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='replace')
        break

soup = BeautifulSoup(html, "html.parser")
sec = soup.find("section", class_="vW5J4")
grid_items = sec.find_all("div", class_=lambda c: c and "os1Bab" in c)

# Collect all asset items from top of page to bottom
raw_items = []
for div in grid_items:
    a = div.find("a")
    if not a:
        continue
    href = a.get("href", "")
    if "/asset/" not in href:
        continue
    
    title = a.get("title")
    if not title:
        h3 = a.find("h3")
        title = h3.get_text(strip=True) if h3 else None
        
    sub_el = a.find(class_=lambda x: x and "Z8Qc2" in x)
    subtitle = sub_el.get_text(strip=True) if sub_el else None
    
    path_parts = urllib.parse.urlparse(href).path.strip("/").split("/")
    asset_id = path_parts[-1] if len(path_parts) >= 2 else None
    
    data_bgsrc = a.get("data-bgsrc")
    data_ia = a.get("data-ia")
    a_style = a.get("style")
    div_style = div.get("style")
    
    raw_items.append({
        "title": title,
        "subtitle": subtitle,
        "asset_id": asset_id,
        "link": href,
        "data_bgsrc": data_bgsrc,
        "data_ia": data_ia,
        "style": a_style,
        "container_style": div_style,
    })

total_count = len(raw_items)
print(f"Total asset items found: {total_count}")

# Assign chronological index:
# Top of page is newest (index = total_count = 801)
# Bottom of page is oldest (index = 1)
records = []
for i, item in enumerate(raw_items):
    index_num = total_count - i
    item_record = {
        "index": index_num,
        "title": item["title"],
        "subtitle": item["subtitle"],
        "asset_id": item["asset_id"],
        "link": item["link"],
        "data_bgsrc": item["data_bgsrc"],
        "data_ia": item["data_ia"],
        "style": item["style"],
        "container_style": item["container_style"],
    }
    records.append(item_record)

# 2. Local & GDrive sync directories
os.makedirs(local_dir, exist_ok=True)
if os.path.exists(r"G:\My Drive"):
    os.makedirs(gdrive_sync_dir, exist_ok=True)

json_path = os.path.join(local_dir, "favorites.json")
tsv_path = os.path.join(local_dir, "favorites.tsv")

print(f"Writing local JSON: {json_path}")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print(f"Writing local TSV: {tsv_path}")
headers = ["index", "title", "subtitle", "asset_id", "link", "data_bgsrc", "data_ia", "style", "container_style"]
with open(tsv_path, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=headers, delimiter="\t")
    writer.writeheader()
    for r in records:
        writer.writerow({k: ("" if r[k] is None else str(r[k])) for k in headers})

if os.path.exists(gdrive_sync_dir):
    print(f"Copying to local GDrive sync folder: {gdrive_sync_dir}")
    shutil.copy2(json_path, os.path.join(gdrive_sync_dir, "favorites.json"))
    shutil.copy2(tsv_path, os.path.join(gdrive_sync_dir, "favorites.tsv"))

# 3. Google Drive / Sheets API with retries
def get_token():
    return subprocess.check_output('gcloud auth print-access-token', shell=True, text=True).strip()

token = get_token()

def api_request(url, method='GET', data=None, content_type='application/json', retries=5):
    global token
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8') if data is not None else None,
                headers={
                    'Authorization': f'Bearer {token}',
                    'Content-Type': content_type
                },
                method=method
            )
            with urllib.request.urlopen(req) as resp:
                body = resp.read().decode()
                return json.loads(body) if body else {}
        except Exception as e:
            print(f"API attempt {attempt+1}/{retries} failed ({e}), retrying in {2**attempt}s...")
            time.sleep(2**attempt)
            token = get_token()
    raise Exception(f"Failed API request to {url} after {retries} attempts.")

print("\nEnsuring 'Google Arts & Culture' folder on Google Drive...")
query = urllib.parse.quote("name = 'Google Arts & Culture' and mimeType = 'application/vnd.google-apps.folder' and trashed = false")
search_res = api_request(f"https://www.googleapis.com/drive/v3/files?q={query}")

folder_id = None
if search_res.get("files"):
    folder_id = search_res["files"][0]["id"]
    print(f"Found existing folder: ID={folder_id}")
else:
    folder_res = api_request("https://www.googleapis.com/drive/v3/files", method="POST", data={
        "name": "Google Arts & Culture",
        "mimeType": "application/vnd.google-apps.folder"
    })
    folder_id = folder_res["id"]
    print(f"Created new folder: ID={folder_id}")

# Check if spreadsheet already exists in folder
sheet_query = urllib.parse.quote(f"name = 'Google Arts & Culture - Favorites' and '{folder_id}' in parents and trashed = false")
# spreadsheet_id, once known, should generally match paths.SHEET_ID
sheet_search = api_request(f"https://www.googleapis.com/drive/v3/files?q={sheet_query}")

spreadsheet_id = None
if sheet_search.get("files"):
    spreadsheet_id = sheet_search["files"][0]["id"]
    print(f"Found existing Google Sheet in folder: ID={spreadsheet_id}")
else:
    # Create via Drive API inside folder directly
    create_drive_file = {
        "name": "Google Arts & Culture - Favorites",
        "mimeType": "application/vnd.google-apps.spreadsheet",
        "parents": [folder_id]
    }
    file_res = api_request("https://www.googleapis.com/drive/v3/files", method="POST", data=create_drive_file)
    spreadsheet_id = file_res["id"]
    print(f"Created Google Sheet in folder: ID={spreadsheet_id}")

spreadsheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit"
print(f"Spreadsheet URL: {spreadsheet_url}")

# Fetch sheet metadata
sheet_meta = api_request(f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}")
sheet_obj = sheet_meta["sheets"][0]
sheet_id = sheet_obj["properties"]["sheetId"]
sheet_title = sheet_obj["properties"]["title"]

# Populate data
print("Writing rows to Google Sheet...")
rows_data = [headers]
for r in records:
    rows_data.append([
        r["index"],
        r["title"] or "",
        r["subtitle"] or "",
        r["asset_id"] or "",
        r["link"] or "",
        r["data_bgsrc"] or "",
        r["data_ia"] or "",
        r["style"] or "",
        r["container_style"] or "",
    ])

val_body = {
    "range": f"'{sheet_title}'!A1:I{len(rows_data)}",
    "majorDimension": "ROWS",
    "values": rows_data
}

# Update values
req = urllib.request.Request(
    f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/'{urllib.parse.quote(sheet_title)}'!A1?valueInputOption=USER_ENTERED",
    data=json.dumps(val_body).encode("utf-8"),
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    },
    method="PUT"
)
with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode())
    print(f"Populated {res.get('updatedRows')} rows.")

# Format Sheet: freeze top row, bold header with styling, auto-resize
print("Styling Google Sheet...")
format_requests = [
    # Freeze row 1
    {
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "gridProperties": {
                    "frozenRowCount": 1
                }
            },
            "fields": "gridProperties.frozenRowCount"
        }
    },
    # Header format
    {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": 0,
                "endRowIndex": 1,
                "startColumnIndex": 0,
                "endColumnIndex": len(headers)
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                        "red": 0.12,
                        "green": 0.35,
                        "blue": 0.75
                    },
                    "textFormat": {
                        "foregroundColor": {
                            "red": 1.0,
                            "green": 1.0,
                            "blue": 1.0
                        },
                        "bold": True,
                        "fontSize": 11
                    },
                    "horizontalAlignment": "CENTER",
                    "verticalAlignment": "MIDDLE"
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
        }
    },
    # Auto-resize columns
    {
        "autoResizeDimensions": {
            "dimensions": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": 0,
                "endIndex": len(headers)
            }
        }
    }
]

fmt_req = urllib.request.Request(
    f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate",
    data=json.dumps({"requests": format_requests}).encode("utf-8"),
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    },
    method="POST"
)
with urllib.request.urlopen(fmt_req) as resp:
    print("Formatting applied successfully!")

print("\n--- COMPLETE ---")
print(f"Local Folder: {local_dir}")
print(f"  - favorites.json ({len(records)} records)")
print(f"  - favorites.tsv ({len(records)} records)")
print(f"Google Drive Sync Folder: {gdrive_sync_dir}")
print(f"Native Google Sheet: {spreadsheet_url}")
