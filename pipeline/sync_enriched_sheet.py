import subprocess
import urllib.request
import urllib.parse
import json
import csv
import os

import paths

token = subprocess.check_output('gcloud auth print-access-token', shell=True, text=True).strip()
spreadsheet_id = paths.SHEET_ID

tsv_path = str(paths.DATA / "favorites_enriched.tsv")
with open(tsv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f, delimiter="\t")
    rows = list(reader)

print(f"Read {len(rows)} rows, {len(rows[0])} columns from enriched TSV.")

# 1. Fetch spreadsheet metadata
req_meta = urllib.request.Request(
    f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}",
    headers={'Authorization': f'Bearer {token}'}
)
with urllib.request.urlopen(req_meta) as resp:
    meta = json.loads(resp.read().decode())

sheet_obj = meta["sheets"][0]
sheet_id = sheet_obj["properties"]["sheetId"]
sheet_title = sheet_obj["properties"]["title"]
print(f"Current sheet title: '{sheet_title}', sheet ID: {sheet_id}")

# 2. Resize sheet to fit all rows and columns
expand_body = {
    "requests": [
        {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "title": "Enriched Favorites",
                    "gridProperties": {
                        "rowCount": len(rows) + 20,
                        "columnCount": len(rows[0]) + 5,
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
try:
    with urllib.request.urlopen(req_expand) as resp:
        print("Sheet dimensions expanded successfully.")
except urllib.error.HTTPError as e:
    print("Expand error:", e.code, e.read().decode())

# 3. Put values using batchUpdate or value update
val_body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {
            "range": f"'Enriched Favorites'!A1",
            "majorDimension": "ROWS",
            "values": rows
        }
    ]
}

url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values:batchUpdate"
req = urllib.request.Request(
    url,
    data=json.dumps(val_body).encode("utf-8"),
    headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
    method="POST"
)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode())
        print(f"Values populated: {res.get('totalUpdatedRows')} rows, {res.get('totalUpdatedColumns')} cols, {res.get('totalUpdatedCells')} cells.")
except urllib.error.HTTPError as e:
    print("Values error:", e.code, e.read().decode())
    exit(1)

# 4. Apply styling: Navy Header, bold white text, center index, auto-resize columns
headers = rows[0]
format_requests = [
    # Header format: Navy blue (#154360), bold white text, centered
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
                    "backgroundColor": {"red": 0.08, "green": 0.26, "blue": 0.55},
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
                "endRowIndex": len(rows),
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
                "endIndex": len(headers)
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

try:
    with urllib.request.urlopen(fmt_req) as resp:
        print("Styling applied successfully!")
except urllib.error.HTTPError as e:
    print("Styling Error:", e.code, e.read().decode())

print(f"\nSpreadsheet URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")
