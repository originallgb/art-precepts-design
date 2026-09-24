import subprocess
import urllib.request
import json

spreadsheet_id = "1Tznbdor6-JFLkGNtuN5StasMSopnLkhdqzgbq7NWdAU"
token = subprocess.check_output('gcloud auth print-access-token', shell=True, text=True).strip()

def api_get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

print("=== VERIFICATION 1: SPREADSHEET METADATA ===")
meta = api_get(
    f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}"
    "?fields=properties,sheets(properties,bandedRanges)"
)
print(f"Spreadsheet Title: {meta['properties']['title']}")
sheets = meta['sheets']
print(f"Total Sheets: {len(sheets)}")
for s in sheets:
    p = s['properties']
    print(f"\nSheet Title: '{p['title']}', Sheet ID: {p['sheetId']}, Index: {p.get('index')}")
    print(f"  GridProperties: {p.get('gridProperties')}")
    bandings = s.get('bandedRanges', [])
    print(f"  Banded Ranges: {len(bandings)}")
    for b in bandings:
        print(f"    Banding ID {b['bandedRangeId']}: range={b['range']}")

print("\n=== VERIFICATION 2: ENRICHED FAVORITES (Sheet ID 0) ===")
# Fetch first 5 rows and last 5 rows of Enriched Favorites
vals_ef = api_get(
    f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/'Enriched%20Favorites'!A1:AW822"
    "?valueRenderOption=FORMULA"
)
rows_ef = vals_ef.get('values', [])
print(f"Total rows retrieved from Enriched Favorites: {len(rows_ef)}")
print(f"Total columns in header: {len(rows_ef[0])}")
print(f"First 10 headers: {rows_ef[0][:10]}")
print(f"Last 5 headers: {rows_ef[0][-5:]}")

# Verify Column A has =IMAGE(...) formula in rows 2..802
image_formulas_ef = 0
for r_idx in range(1, 802):
    row = rows_ef[r_idx]
    if row and str(row[0]).startswith("=IMAGE"):
        image_formulas_ef += 1
print(f"Valid =IMAGE formulas in Column A (rows 2..802): {image_formulas_ef} / 801")
print(f"Sample Col A Row 2: {rows_ef[1][0]}")
print(f"Sample Col A Row 802: {rows_ef[801][0]}")
print(f"Sample Row 2 Index: {rows_ef[1][1]}, Title: {rows_ef[1][2]}, Creator: {rows_ef[1][4]}")
print(f"Sample Row 802 Index: {rows_ef[801][1]}, Title: {rows_ef[801][2]}, Creator: {rows_ef[801][4]}")

print("\n=== VERIFICATION 3: CATALOGUE PRECEPTS (Sheet ID 98234710) ===")
vals_cp = api_get(
    f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/'Catalogue%20Precepts'!A1:BD802"
    "?valueRenderOption=FORMULA"
)
rows_cp = vals_cp.get('values', [])
print(f"Total rows retrieved from Catalogue Precepts: {len(rows_cp)}")
print(f"Total columns in header: {len(rows_cp[0])}")
print(f"First 5 headers: {rows_cp[0][:5]}")
print(f"Last 10 headers: {rows_cp[0][-10:]}")

# Verify Column A has =IMAGE(...) formula in rows 2..802
image_formulas_cp = 0
for r_idx in range(1, len(rows_cp)):
    row = rows_cp[r_idx]
    if row and str(row[0]).startswith("=IMAGE"):
        image_formulas_cp += 1
print(f"Valid =IMAGE formulas in Column A (rows 2..802): {image_formulas_cp} / 801")
print(f"Sample Col A Row 2: {rows_cp[1][0]}")
print(f"Sample Col A Row 802: {rows_cp[801][0]}")

# Precept critique and heuristics samples
print(f"Sample Row 2 Precept Critique (first 80 chars): {rows_cp[1][47][:80]}...")
print(f"Sample Row 2 Design Heuristics (first 80 chars): {rows_cp[1][48][:80]}...")
print(f"Sample Row 2 Extracted Palette: {rows_cp[1][49]}")

print("\n=== VERIFICATION 4: DETAILED FORMATTING AUDIT ===")
detail = api_get(
    f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}"
    "?fields=sheets(properties,data(columnMetadata,rowMetadata,rowData(values(userEnteredFormat))))"
    "&ranges='Enriched%20Favorites'!A1:AW2&ranges='Catalogue%20Precepts'!A1:BD2"
)

# 1. Enriched Favorites formatting
ef_sheet = detail['sheets'][0]
ef_col_meta = ef_sheet['data'][0].get('columnMetadata', [])
ef_row_meta = ef_sheet['data'][0].get('rowMetadata', [])
print(f"Enriched Favorites Column A width: {ef_col_meta[0].get('pixelSize')}px (Target: 85px)")
if len(ef_row_meta) > 1:
    print(f"Enriched Favorites Data Row 2 height: {ef_row_meta[1].get('pixelSize')}px (Target: 55px)")
ef_header_cell = ef_sheet['data'][0]['rowData'][0]['values'][0]['userEnteredFormat']
print(f"Enriched Favorites Header BgColor: {ef_header_cell.get('backgroundColor')}")
print(f"Enriched Favorites Header TextFormat: {ef_header_cell.get('textFormat')}")

# 2. Catalogue Precepts formatting
cp_sheet = detail['sheets'][1]
cp_col_meta = cp_sheet['data'][0].get('columnMetadata', [])
cp_row_meta = cp_sheet['data'][0].get('rowMetadata', [])
print(f"\nCatalogue Precepts Header Row height: {cp_row_meta[0].get('pixelSize')}px (Target: 36px)")
cp_header_cell = cp_sheet['data'][0]['rowData'][0]['values'][0]['userEnteredFormat']
print(f"Catalogue Precepts Header BgColor: {cp_header_cell.get('backgroundColor')}")
print(f"Catalogue Precepts Header TextFormat: {cp_header_cell.get('textFormat')}")

# Check key column widths
headers_cp = rows_cp[0]
target_checks = [
    ("thumbnail_preview", 85),
    ("index", 75),
    ("title", 240),
    ("creator", 220),
    ("precept_critique", 480),
    ("design_heuristics", 520),
    ("extracted_palette", 220),
    ("chromatic_temperature", 130),
    ("contrast_level", 110)
]
print("\nCatalogue Precepts Column Width Checks:")
for name, target in target_checks:
    idx = headers_cp.index(name)
    actual = cp_col_meta[idx].get('pixelSize')
    print(f"  {name:<22}: actual={actual}px | target={target}px -> {'OK' if actual == target else 'DIFF'}")

# Check cell formatting for precept_critique (col 47), design_heuristics (col 48), extracted_palette (col 49)
idx_critique = headers_cp.index("precept_critique")
idx_heuristics = headers_cp.index("design_heuristics")
idx_palette = headers_cp.index("extracted_palette")

critique_fmt = cp_sheet['data'][0]['rowData'][1]['values'][idx_critique].get('userEnteredFormat', {})
heuristics_fmt = cp_sheet['data'][0]['rowData'][1]['values'][idx_heuristics].get('userEnteredFormat', {})
palette_fmt = cp_sheet['data'][0]['rowData'][1]['values'][idx_palette].get('userEnteredFormat', {})

print(f"\nprecept_critique cell format: wrapStrategy={critique_fmt.get('wrapStrategy')}, verticalAlignment={critique_fmt.get('verticalAlignment')}, align={critique_fmt.get('horizontalAlignment')}")
print(f"design_heuristics cell format: wrapStrategy={heuristics_fmt.get('wrapStrategy')}, verticalAlignment={heuristics_fmt.get('verticalAlignment')}, align={heuristics_fmt.get('horizontalAlignment')}")
print(f"extracted_palette cell format: font={palette_fmt.get('textFormat', {}).get('fontFamily')}, verticalAlignment={palette_fmt.get('verticalAlignment')}")

print("\n=== VERIFICATION COMPLETE ===")
