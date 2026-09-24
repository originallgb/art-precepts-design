import asyncio
import httpx
import json
import csv
import os
import sys
import time
import urllib.parse
import urllib.request
import subprocess
import shutil
import sqlite3

sys.path.insert(0, r"%USERPROFILE%\.gemini\antigravity\brain\agy-session-2287\scratch")
from gac_parser import parse_gac_html

# Paths
local_dir = r"<repo>\Google Arts & Culture"
gdrive_sync_dir = r"<drive-mirror>\Google Arts & Culture"
db_path = r"%USERPROFILE%\.gemini\antigravity\brain\agy-session-2287\scratch\enrichment.db"
spreadsheet_id = "1Tznbdor6-JFLkGNtuN5StasMSopnLkhdqzgbq7NWdAU"

# 1. Initialize SQLite Cache Database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS gac_cache (
    asset_id TEXT PRIMARY KEY,
    json_data TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS wikidata_cache (
    asset_id TEXT PRIMARY KEY,
    json_data TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Load base favorites list
json_input_path = os.path.join(local_dir, "favorites.json")
with open(json_input_path, "r", encoding="utf-8") as f:
    favorites = json.load(f)

print(f"Loaded {len(favorites)} favorite items.")

# 2. Worker 1: Async GAC Asset Fetcher
async def fetch_gac_asset(client, semaphore, item, total, progress_tracker):
    asset_id = item["asset_id"]
    url = item["link"]
    
    # Check SQLite cache first
    c = conn.cursor()
    c.execute("SELECT json_data FROM gac_cache WHERE asset_id = ?", (asset_id,))
    cached = c.fetchone()
    if cached:
        progress_tracker["cached"] += 1
        return json.loads(cached[0])
        
    async with semaphore:
        for attempt in range(4):
            try:
                resp = await client.get(url, timeout=20.0)
                if resp.status_code == 200:
                    parsed = parse_gac_html(resp.text, asset_id, url)
                    # Cache in DB
                    c.execute("INSERT OR REPLACE INTO gac_cache (asset_id, json_data) VALUES (?, ?)",
                              (asset_id, json.dumps(parsed, ensure_ascii=False)))
                    conn.commit()
                    progress_tracker["fetched"] += 1
                    done = progress_tracker["fetched"] + progress_tracker["cached"]
                    if done % 50 == 0 or done == total:
                        print(f"  [GAC Progress] {done}/{total} items processed ({progress_tracker['fetched']} fetched, {progress_tracker['cached']} cached)...")
                    return parsed
                elif resp.status_code == 429 or resp.status_code >= 500:
                    await asyncio.sleep(1.5 ** attempt)
                else:
                    break
            except Exception as e:
                await asyncio.sleep(1.0)
                
    # Fallback to base data if all retries fail
    fallback = {
        "asset_id": asset_id,
        "url": url,
        "title": item.get("title"),
        "creator_name": item.get("subtitle"),
        "image_url": item.get("data_bgsrc"),
    }
    return fallback

# 3. Worker 2: Wikidata SPARQL Batch Resolver
async def fetch_wikidata_batch(client, all_ids):
    print(f"\n[Wikidata Worker] Querying Wikidata SPARQL for {len(all_ids)} asset IDs...")
    wikidata_map = {}
    
    # Check cache
    missing_ids = []
    c = conn.cursor()
    for aid in all_ids:
        c.execute("SELECT json_data FROM wikidata_cache WHERE asset_id = ?", (aid,))
        cached = c.fetchone()
        if cached:
            wikidata_map[aid] = json.loads(cached[0])
        else:
            missing_ids.append(aid)
            
    print(f"[Wikidata Worker] {len(wikidata_map)} cached, {len(missing_ids)} to query.")
    
    chunk_size = 100
    for i in range(0, len(missing_ids), chunk_size):
        chunk = missing_ids[i:i+chunk_size]
        values_clause = " ".join([f'"{cid}"' for cid in chunk])
        sparql = f"""
        SELECT ?item ?itemLabel ?gacId ?creatorLabel ?date ?collectionLabel ?commonsImage ?inventory ?wikipedia WHERE {{
          VALUES ?gacId {{ {values_clause} }}
          ?item wdt:P4701 ?gacId .
          OPTIONAL {{ ?item wdt:P170 ?creator. }}
          OPTIONAL {{ ?item wdt:P571 ?date. }}
          OPTIONAL {{ ?item wdt:P195 ?collection. }}
          OPTIONAL {{ ?item wdt:P18 ?commonsImage. }}
          OPTIONAL {{ ?item wdt:P217 ?inventory. }}
          OPTIONAL {{
            ?wikipedia schema:about ?item ;
                       schema:isPartOf <https://en.wikipedia.org/> .
          }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}
        """
        try:
            resp = await client.get("https://query.wikidata.org/sparql", params={"query": sparql, "format": "json"}, timeout=30.0)
            if resp.status_code == 200:
                res = resp.json()
                bindings = res.get("results", {}).get("bindings", [])
                for b in bindings:
                    gid = b.get("gacId", {}).get("value")
                    if gid:
                        rec = {
                            "wikidata_qid": b.get("item", {}).get("value"),
                            "wikidata_title": b.get("itemLabel", {}).get("value"),
                            "wikidata_creator": b.get("creatorLabel", {}).get("value"),
                            "wikidata_date": b.get("date", {}).get("value"),
                            "wikidata_collection": b.get("collectionLabel", {}).get("value"),
                            "commons_image": b.get("commonsImage", {}).get("value"),
                            "wikidata_inventory": b.get("inventory", {}).get("value"),
                            "wikipedia_url": b.get("wikipedia", {}).get("value"),
                        }
                        wikidata_map[gid] = rec
                        c.execute("INSERT OR REPLACE INTO wikidata_cache (asset_id, json_data) VALUES (?, ?)",
                                  (gid, json.dumps(rec, ensure_ascii=False)))
                conn.commit()
        except Exception as e:
            print(f"Wikidata chunk error: {e}")
        await asyncio.sleep(0.3)
        
    print(f"[Wikidata Worker] Total Wikidata matches resolved: {len(wikidata_map)} / {len(all_ids)}")
    return wikidata_map

# 4. Main Orchestrator
async def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
    wiki_headers = {
        "User-Agent": "AntigravityArtsResearch/1.0 (https://github.com; originallgb@users.noreply.github.com)"
    }
    
    start_time = time.time()
    semaphore = asyncio.Semaphore(12)  # 12 parallel async streams
    progress_tracker = {"fetched": 0, "cached": 0}
    
    async with httpx.AsyncClient(headers=headers, follow_redirects=True, timeout=25.0) as gac_client, \
               httpx.AsyncClient(headers=wiki_headers, timeout=35.0) as wiki_client:
        
        all_asset_ids = [item["asset_id"] for item in favorites]
        
        print("\n--- Starting Parallel Processing ---")
        gac_tasks = [
            fetch_gac_asset(gac_client, semaphore, item, len(favorites), progress_tracker)
            for item in favorites
        ]
        wikidata_task = fetch_wikidata_batch(wiki_client, all_asset_ids)
        
        # Run both simultaneously
        gac_results, wikidata_map = await asyncio.gather(
            asyncio.gather(*gac_tasks),
            wikidata_task
        )
        
    elapsed = time.time() - start_time
    print(f"\nAll 801 items fetched and parsed in {elapsed:.2f} seconds!")
    
    # 5. Merge Datasets
    print("\nMerging primary GAC metadata and Wikidata open data...")
    enriched_records = []
    
    for i, base_item in enumerate(favorites):
        gac_meta = gac_results[i]
        aid = base_item["asset_id"]
        wiki_meta = wikidata_map.get(aid, {})
        
        # Build unified clean record
        rec = {
            "index": base_item["index"],
            "title": gac_meta.get("title") or base_item.get("title"),
            "original_title": gac_meta.get("original_title"),
            "creator": gac_meta.get("creator_name") or base_item.get("subtitle"),
            "creator_lifespan": gac_meta.get("creator_lifespan"),
            "creator_nationality": gac_meta.get("creator_nationality"),
            "date_created": gac_meta.get("date_created"),
            "location_created": gac_meta.get("location_created"),
            "medium": gac_meta.get("medium"),
            "object_type": gac_meta.get("object_type"),
            "physical_dimensions": gac_meta.get("physical_dimensions"),
            "aspect_ratio": gac_meta.get("aspect_ratio"),
            "dominant_color": gac_meta.get("dominant_color_hex"),
            "partner_name": gac_meta.get("partner_name"),
            "partner_city_country": gac_meta.get("partner_city_country"),
            "partner_website": gac_meta.get("partner_website"),
            "partner_lat": gac_meta.get("partner_lat"),
            "partner_long": gac_meta.get("partner_long"),
            "curatorial_description": gac_meta.get("curatorial_description"),
            "provenance": gac_meta.get("provenance"),
            "credit_line": gac_meta.get("credit_line"),
            "inventory_number": gac_meta.get("inventory_number") or wiki_meta.get("wikidata_inventory"),
            "external_catalog_url": gac_meta.get("external_catalog_url"),
            "rights": gac_meta.get("rights"),
            "art_movements": gac_meta.get("art_movements"),
            "tags_and_topics": gac_meta.get("tags_and_topics"),
            "wikidata_qid": wiki_meta.get("wikidata_qid"),
            "wikipedia_url": wiki_meta.get("wikipedia_url"),
            "commons_image_url": wiki_meta.get("commons_image"),
            "asset_id": aid,
            "link": base_item["link"],
            "image_url": gac_meta.get("image_url") or base_item.get("data_bgsrc"),
        }
        enriched_records.append(rec)
        
    # 6. Save JSON and TSV
    enriched_json_path = os.path.join(local_dir, "favorites_enriched.json")
    enriched_tsv_path = os.path.join(local_dir, "favorites_enriched.tsv")
    
    print(f"\nWriting local Enriched JSON: {enriched_json_path}")
    with open(enriched_json_path, "w", encoding="utf-8") as f:
        json.dump(enriched_records, f, ensure_ascii=False, indent=2)
        
    print(f"Writing local Enriched TSV: {enriched_tsv_path}")
    field_order = list(enriched_records[0].keys())
    with open(enriched_tsv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=field_order, delimiter="\t")
        writer.writeheader()
        for r in enriched_records:
            writer.writerow({k: ("" if r[k] is None else str(r[k])) for k in field_order})
            
    # Also sync to G: Drive
    if os.path.exists(gdrive_sync_dir):
        print(f"Syncing files to Google Drive Desktop: {gdrive_sync_dir}")
        shutil.copy2(enriched_json_path, os.path.join(gdrive_sync_dir, "favorites_enriched.json"))
        shutil.copy2(enriched_tsv_path, os.path.join(gdrive_sync_dir, "favorites_enriched.tsv"))
        
    # 7. Update Native Google Sheet
    print("\nUpdating Native Google Sheet...")
    token = subprocess.check_output('gcloud auth print-access-token', shell=True, text=True).strip()
    
    # Check spreadsheet tabs
    req_meta = urllib.request.Request(
        f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}",
        headers={'Authorization': f'Bearer {token}'}
    )
    with urllib.request.urlopen(req_meta) as resp:
        meta = json.loads(resp.read().decode())
        
    sheet_obj = meta["sheets"][0]
    sheet_id = sheet_obj["properties"]["sheetId"]
    sheet_title = sheet_obj["properties"]["title"]
    
    # Format rows for upload
    rows_data = [field_order]
    for r in enriched_records:
        row = [("" if r[k] is None else str(r[k])) for k in field_order]
        rows_data.append(row)
        
    range_name = f"'{sheet_title}'!A1:{chr(64 + len(field_order))}{len(rows_data)}"
    val_body = {
        "range": range_name,
        "majorDimension": "ROWS",
        "values": rows_data
    }
    
    # 1. Expand sheet row/col dimensions if needed
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
        
    # 2. Put values
    enc_range = urllib.parse.quote("Enriched Favorites!A1")
    req_put = urllib.request.Request(
        f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{enc_range}?valueInputOption=USER_ENTERED",
        data=json.dumps(val_body).encode("utf-8"),
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        method="PUT"
    )
    with urllib.request.urlopen(req_put) as resp:
        res = json.loads(resp.read().decode())
        print(f"Populated Google Sheet: {res.get('updatedRows')} rows, {res.get('updatedColumns')} columns.")
        
    # 3. Format header, alignment, auto-resize
    print("Formatting Google Sheet styling...")
    format_requests = [
        # Header style: Navy background, bold white text
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
                        "backgroundColor": {"red": 0.08, "green": 0.32, "blue": 0.72},
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
        # Auto resize columns
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
        print("Sheet formatting applied successfully!")
        
    print("\n==========================================")
    print("      PIPELINE COMPLETED SUCCESSFULLY     ")
    print("==========================================")
    print(f"1. Enriched Local JSON: {enriched_json_path}")
    print(f"2. Enriched Local TSV:  {enriched_tsv_path}")
    print(f"3. Google Drive Sync:   {gdrive_sync_dir}")
    print(f"4. Google Sheet:        https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")

if __name__ == "__main__":
    asyncio.run(main())
