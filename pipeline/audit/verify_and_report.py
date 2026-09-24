import sqlite3
import json
import os
import sys
import hashlib
from datetime import datetime, timedelta
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paths

# Connect to database
db_path = r'%USERPROFILE%\.gemini\antigravity\brain\agy-session-2287\scratch\multimodal_analysis.db'  # historical, Windows/OPTILAB-only
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Get DB file metadata
db_stat = os.stat(db_path)
db_size = db_stat.st_size
with open(db_path, 'rb') as f:
    db_sha256 = hashlib.sha256(f.read()).hexdigest()

log_path = r'%USERPROFILE%\.gemini\antigravity\brain\agy-session-2287\.system_generated\tasks\task-1232.log'  # historical, Windows/OPTILAB-only
log_stat = os.stat(log_path)
with open(log_path, 'rb') as f:
    log_sha256 = hashlib.sha256(f.read()).hexdigest()

print(f"DB Path: {db_path}")
print(f"DB Size: {db_size} bytes ({db_size / (1024*1024):.2f} MB)")
print(f"DB SHA256: {db_sha256}")
print(f"Log Path: {log_path}")
print(f"Log Size: {log_stat.st_size} bytes")
print(f"Log SHA256: {log_sha256}")

# Schema check
cur.execute("SELECT index_num, asset_id, title, created_at, length(json_result), json_result FROM analysis_cache ORDER BY index_num")
all_rows = cur.fetchall()

expected_fields = [
    "visual_composition",
    "color_and_light",
    "texture_and_materiality",
    "semiotics_and_emotion",
    "design_vernacular",
    "precept_critique",
    "design_heuristics"
]

subfield_checks = {
    "visual_composition": ["focal_flow", "geometric_structure", "symmetry_balance", "framing_density"],
    "color_and_light": ["palette_hex", "chromatic_temperature", "light_source_profile", "contrast_level"],
    "texture_and_materiality": ["perceived_surface", "material_honesty", "spatial_depth_handling"],
    "semiotics_and_emotion": ["core_symbols", "emotional_valence", "narrative_themes"],
    "design_vernacular": ["historical_lineage", "structural_motifs", "typographic_cues"]
}

valid_count = 0
invalid_json = 0
missing_field_count = 0
missing_subfield_count = 0

for r in all_rows:
    try:
        data = json.loads(r[5])
        valid_count += 1
        for fld in expected_fields:
            if fld not in data or data[fld] is None or data[fld] == "" or data[fld] == []:
                missing_field_count += 1
        for fld, subflds in subfield_checks.items():
            sub_obj = data.get(fld, {})
            for sf in subflds:
                if sf not in sub_obj or sub_obj[sf] is None or sub_obj[sf] == "" or sub_obj[sf] == []:
                    missing_subfield_count += 1
    except Exception:
        invalid_json += 1

print(f"\nTotal DB rows: {len(all_rows)}")
print(f"Valid JSON rows: {valid_count} / {len(all_rows)}")
print(f"Missing top-level fields: {missing_field_count}")
print(f"Missing subfields: {missing_subfield_count}")

# Timestamps & Runtime
cur.execute("SELECT index_num, created_at FROM analysis_cache WHERE created_at = '2026-09-04 12:38:36'")
pilot_items = cur.fetchall()

cur.execute("SELECT index_num, created_at, length(json_result) FROM analysis_cache WHERE created_at > '2026-09-04 12:38:36' ORDER BY created_at, index_num DESC")
live_items = cur.fetchall()

print(f"\nPilot cached items count: {len(pilot_items)}")
print(f"Live analyzed items count: {len(live_items)}")

# Queue Simulation for exact latency
t_start = datetime.strptime("2026-09-04 12:38:37.87", "%Y-%m-%d %H:%M:%S.%f")
fav_path = str(paths.DATA / 'favorites_enriched.json')
with open(fav_path, 'r', encoding='utf-8') as f:
    favs = json.load(f)

bypassed = {801, 794, 720, 602}
dispatched_order = [f['index'] for f in favs if f['index'] not in bypassed]

sorted_completions = sorted(live_items, key=lambda r: (r[1], -r[0]))
start_times = {}
end_times = {}

for idx in dispatched_order[:10]:
    start_times[idx] = t_start

next_dispatch_idx = 10
for r in sorted_completions:
    idx = r[0]
    t_finish = datetime.strptime(r[1], "%Y-%m-%d %H:%M:%S")
    end_times[idx] = t_finish
    if next_dispatch_idx < len(dispatched_order):
        next_item = dispatched_order[next_dispatch_idx]
        start_times[next_item] = t_finish
        next_dispatch_idx += 1

latencies = [(et - start_times[idx]).total_seconds() for idx, et in end_times.items()]
lat_vals = sorted(latencies)

def percentile(data, p):
    k = (len(data) - 1) * (p / 100.0)
    f = int(k)
    c = f + 1
    if c >= len(data):
        return data[f]
    return data[f] * (c - k) + data[c] * (k - f)

p_min = min(lat_vals)
p25 = percentile(lat_vals, 25)
p50 = percentile(lat_vals, 50)
p75 = percentile(lat_vals, 75)
p90 = percentile(lat_vals, 90)
p95 = percentile(lat_vals, 95)
p99 = percentile(lat_vals, 99)
p_max = max(lat_vals)
p_mean = statistics.mean(lat_vals)
agg_runtime = sum(lat_vals)
wall_clock = 1536.13

print(f"\n--- Runtime & Concurrency ---")
print(f"Wall-clock runtime: {wall_clock:.2f} s ({wall_clock/60:.2f} min)")
print(f"Aggregate request runtime: {agg_runtime:.2f} s ({agg_runtime/60:.2f} min = {agg_runtime/3600:.2f} hours)")
print(f"Effective concurrency: {agg_runtime/wall_clock:.2f}x (out of 10.0x maximum)")

print(f"\n--- Latency Percentiles ---")
print(f"Min:  {p_min:.2f} s")
print(f"p25:  {p25:.2f} s")
print(f"p50:  {p50:.2f} s")
print(f"p75:  {p75:.2f} s")
print(f"p90:  {p90:.2f} s")
print(f"p95:  {p95:.2f} s")
print(f"p99:  {p99:.2f} s")
print(f"Max:  {p_max:.2f} s")
print(f"Mean: {p_mean:.2f} s")

# 60-second window throughput
rolling_windows = {}
start_win = datetime.strptime("2026-09-04 12:38:38", "%Y-%m-%d %H:%M:%S")
for r in live_items:
    ts = datetime.strptime(r[1], "%Y-%m-%d %H:%M:%S")
    sec_offset = int((ts - start_win).total_seconds())
    w_idx = max(0, sec_offset // 60)
    rolling_windows[w_idx] = rolling_windows.get(w_idx, 0) + 1

print(f"\n--- 60-Second Rolling Windows ({len(rolling_windows)} windows) ---")
for w_idx in sorted(rolling_windows.keys()):
    w_start = start_win + timedelta(seconds=w_idx * 60)
    w_end = w_start + timedelta(seconds=59)
    print(f"Window {w_idx+1:02d} [{w_start.strftime('%H:%M:%S')} - {w_end.strftime('%H:%M:%S')} UTC]: {rolling_windows[w_idx]} items")

conn.close()
