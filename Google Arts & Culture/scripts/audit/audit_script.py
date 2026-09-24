import sqlite3
import json
import os

db_path = r'%USERPROFILE%\.gemini\antigravity\brain\agy-session-2287\scratch\multimodal_analysis.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("SELECT index_num, asset_id, title, json_result, created_at FROM analysis_cache ORDER BY index_num")
rows = cur.fetchall()

print(f"Total rows audited: {len(rows)}")

# Output analysis
total_output_chars = sum(len(r[3]) for r in rows)
total_output_bytes = sum(len(r[3].encode('utf-8')) for r in rows)
output_byte_lengths = [len(r[3].encode('utf-8')) for r in rows]

print("\n--- Output Payloads (json_result) ---")
print(f"Total output characters: {total_output_chars:,}")
print(f"Total output bytes (UTF-8): {total_output_bytes:,} bytes ({total_output_bytes / (1024*1024):.2f} MB)")
print(f"Mean output bytes per item: {sum(output_byte_lengths)/len(rows):.1f} bytes")
print(f"Min output bytes: {min(output_byte_lengths)} bytes")
print(f"Max output bytes: {max(output_byte_lengths)} bytes")

# Input prompt analysis
fav_path = r'<repo>\Google Arts & Culture\favorites_enriched.json'
with open(fav_path, 'r', encoding='utf-8') as f:
    favs = json.load(f)
fav_by_idx = {f['index']: f for f in favs}

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

system_prompt_bytes = len(system_prompt.encode('utf-8'))
system_prompt_chars = len(system_prompt)

img_dir = r"<repo>\Google Arts & Culture\images"
img_files = os.listdir(img_dir)
img_by_prefix = {}
for fn in img_files:
    pfx = fn[:4]
    if pfx.isdigit():
        img_by_prefix[int(pfx)] = os.path.join(img_dir, fn)

total_input_text_chars = 0
total_input_text_bytes = 0
total_img_bytes = 0
total_b64_bytes = 0
img_count = 0

for r in rows:
    idx = r[0]
    item = fav_by_idx.get(idx, {})
    title = item.get("title", "Untitled")
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

    full_text = system_prompt + prompt_text
    total_input_text_chars += len(full_text)
    total_input_text_bytes += len(full_text.encode('utf-8'))

    img_path = img_by_prefix.get(idx)
    if img_path and os.path.exists(img_path):
        sz = os.path.getsize(img_path)
        total_img_bytes += sz
        # base64 encoded size: ceil(sz / 3) * 4
        total_b64_bytes += ((sz + 2) // 3) * 4
        img_count += 1

print("\n--- Input Payloads ---")
print(f"System prompt length: {system_prompt_chars} chars, {system_prompt_bytes} bytes")
print(f"Total input text characters (across 800): {total_input_text_chars:,}")
print(f"Total input text bytes (UTF-8, across 800): {total_input_text_bytes:,} bytes ({total_input_text_bytes/(1024*1024):.2f} MB)")
print(f"Mean input text bytes per item: {total_input_text_bytes/800:.1f} bytes")
print(f"Total raw image files: {img_count} images, {total_img_bytes:,} bytes ({total_img_bytes/(1024*1024):.2f} MB)")
print(f"Mean raw image size: {total_img_bytes/img_count/1024:.1f} KB")
print(f"Total base64 image bytes transferred: {total_b64_bytes:,} bytes ({total_b64_bytes/(1024*1024):.2f} MB)")

# Token Accounting
# Gemini token pricing:
# Input: $0.00001875 per 1,000 tokens ($0.01875 per 1M tokens)
# Output: $0.000075 per 1,000 tokens ($0.075 per 1M tokens)
#
# Gemini token rules:
# Image tokens: Gemini 1.5/2.5 Flash treats standard single image as 258 tokens (or 258 per tile)
# Text tokens: English text is approximately 1 token per 4 characters (or ~0.25 to 0.3 tokens/char for structured text/JSON)
# Let's compute text tokens using standard character/word ratios and exact tokenization heuristics.

conn.close()
