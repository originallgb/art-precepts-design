import json
import csv
import os
import subprocess
import urllib.request

import paths

spreadsheet_id = paths.SHEET_ID
tsv_path = str(paths.DATA / "favorites_analyzed.tsv")

def get_token():
    return subprocess.check_output('gcloud auth print-access-token', shell=True, text=True).strip()

def update_sheet():
    if not os.path.exists(tsv_path):
        print(f"File not found: {tsv_path}")
        return

    rows_data = []
    with open(tsv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            rows_data.append(row)

    print(f"Loaded {len(rows_data)} rows from {tsv_path}")
    token = get_token()

    # Get metadata
    req_meta = urllib.request.Request(
        f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}",
        headers={'Authorization': f'Bearer {token}'}
    )
    with urllib.request.urlopen(req_meta) as resp:
        meta = json.loads(resp.read().decode())

    sheet_id = meta["sheets"][0]["properties"]["sheetId"]

    # Ensure sheet size
    field_count = len(rows_data[0]) if rows_data else 50
    expand_body = {
        "requests": [
            {
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": sheet_id,
                        "title": "Catalogue Precepts",
                        "gridProperties": {
                            "rowCount": len(rows_data) + 20,
                            "columnCount": field_count + 5,
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
        print(f"Successfully updated Google Sheet: {res.get('totalUpdatedRows')} rows, {res.get('totalUpdatedColumns')} columns, {res.get('totalUpdatedCells')} cells.")

if __name__ == "__main__":
    update_sheet()
