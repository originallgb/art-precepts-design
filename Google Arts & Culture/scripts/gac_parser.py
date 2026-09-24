import re
import json
from bs4 import BeautifulSoup

def parse_gac_html(html, asset_id, url):
    """Extract structured metadata from GAC asset HTML using window.INIT_data and fallbacks."""
    record = {
        "asset_id": asset_id,
        "url": url,
        "title": None,
        "original_title": None,
        "creator_name": None,
        "creator_lifespan": None,
        "creator_nationality": None,
        "creator_kg_mid": None,
        "date_created": None,
        "location_created": None,
        "medium": None,
        "object_type": None,
        "physical_dimensions": None,
        "aspect_ratio": None,
        "dominant_color_hex": None,
        "partner_name": None,
        "partner_city_country": None,
        "partner_address": None,
        "partner_website": None,
        "partner_maps_url": None,
        "partner_lat": None,
        "partner_long": None,
        "curatorial_description": None,
        "provenance": None,
        "credit_line": None,
        "inventory_number": None,
        "external_catalog_url": None,
        "rights": None,
        "art_movements": None,
        "tags_and_topics": None,
        "image_url": None,
    }
    
    match = re.search(r"window\.INIT_data\[['\"]Asset:[^'\"]+['\"]\]\s*=\s*(\[.+?\]);(?:\s*window|\s*var|\s*<)", html)
    if match:
        try:
            raw_tree = json.loads(match.group(1))
            asset = raw_tree[2] if len(raw_tree) > 2 else {}
            
            # Title
            if len(asset) > 2 and asset[2]:
                record["title"] = asset[2]
                
            # Date
            if len(asset) > 3 and asset[3]:
                record["date_created"] = str(asset[3])
                
            # Image URL
            if len(asset) > 4 and asset[4]:
                img = asset[4]
                record["image_url"] = ("https:" + img) if img.startswith("//") else img
                
            # Curatorial Description
            if len(asset) > 5 and asset[5] and len(asset[5]) > 1:
                desc_html = asset[5][1]
                if desc_html:
                    soup_desc = BeautifulSoup(desc_html, "html.parser")
                    record["curatorial_description"] = soup_desc.get_text(separator=" ", strip=True)
                    
            # Creator
            if len(asset) > 6 and asset[6]:
                creator_block = asset[6]
                if len(creator_block) > 0 and creator_block[0]:
                    record["creator_name"] = creator_block[0]
                if len(creator_block) > 1 and creator_block[1] and len(creator_block[1]) > 0:
                    first_c = creator_block[1][0]
                    if len(first_c) > 21 and first_c[21] and len(first_c[21]) > 1:
                        record["creator_kg_mid"] = first_c[21][1]
                        
            # Partner / Museum
            if len(asset) > 7 and asset[7] and isinstance(asset[7], list):
                p_block = asset[7]
                if len(p_block) > 1 and isinstance(p_block[1], str):
                    record["partner_name"] = p_block[1]
                if len(p_block) > 14 and p_block[14] and isinstance(p_block[14], list):
                    loc = p_block[14]
                    if len(loc) > 2 and loc[2]:
                        record["partner_maps_url"] = loc[2]
                    if len(loc) > 3 and loc[3]:
                        record["partner_website"] = loc[3]
                    if len(loc) > 4 and loc[4]:
                        record["partner_address"] = loc[4].replace("\n", ", ")
                    if len(loc) > 5 and isinstance(loc[5], (int, float)):
                        record["partner_lat"] = round(float(loc[5]), 6)
                    if len(loc) > 6 and isinstance(loc[6], (int, float)):
                        record["partner_long"] = round(float(loc[6]), 6)
                    if len(loc) > 7 and loc[7]:
                        record["partner_city_country"] = loc[7]
                        
            # Aspect ratio & Dominant color
            if len(asset) > 10 and asset[10] is not None:
                record["aspect_ratio"] = round(float(asset[10]), 4)
            if len(asset) > 25 and asset[25] and isinstance(asset[25], str):
                record["dominant_color_hex"] = "#" + asset[25].lstrip("#")
                
            # Curatorial Metadata table in asset[12]
            if len(asset) > 12 and isinstance(asset[12], list):
                for meta_entry in asset[12]:
                    if not isinstance(meta_entry, list) or len(meta_entry) < 2:
                        continue
                    label = str(meta_entry[0]).strip()
                    val_block = meta_entry[1]
                    val_text = None
                    if isinstance(val_block, list) and len(val_block) > 0:
                        if isinstance(val_block[0], list) and len(val_block[0]) > 0:
                            val_text = val_block[0][0]
                        elif isinstance(val_block[0], str):
                            val_text = val_block[0]
                    elif isinstance(val_block, str):
                        val_text = val_block
                        
                    if not val_text or not isinstance(val_text, str):
                        continue
                    val_text = val_text.strip()
                    
                    label_l = label.lower()
                    if label_l == "original title":
                        record["original_title"] = val_text
                    elif label_l in ["medium", "physical medium", "technique"]:
                        record["medium"] = val_text
                    elif label_l in ["type", "object type"]:
                        record["object_type"] = val_text
                    elif label_l in ["physical dimensions", "dimensions", "size"]:
                        record["physical_dimensions"] = val_text
                    elif label_l in ["creator lifespan", "artist lifespan", "lifespan"]:
                        record["creator_lifespan"] = val_text
                    elif label_l in ["creator nationality", "nationality"]:
                        record["creator_nationality"] = val_text
                    elif label_l in ["location created", "place created"]:
                        record["location_created"] = val_text
                    elif label_l in ["provenance", "history"]:
                        record["provenance"] = val_text
                    elif label_l in ["credit line", "credit", "acquisition"]:
                        record["credit_line"] = val_text
                    elif label_l in ["catalogue reference", "inventory number", "accession number", "reference"]:
                        record["inventory_number"] = val_text
                    elif label_l in ["external link", "catalog link"]:
                        record["external_catalog_url"] = val_text
                    elif label_l in ["rights", "copyright", "license"]:
                        record["rights"] = val_text
                        
            # Chips / Taxonomies in asset[21]
            if len(asset) > 21 and isinstance(asset[21], list):
                movements = []
                tags = []
                for chip in asset[21]:
                    if isinstance(chip, list) and len(chip) > 1:
                        c_name = chip[1] if isinstance(chip[1], str) else chip[0]
                        chip_str = json.dumps(chip)
                        if "entity/ART_MOVEMENT" in chip_str:
                            movements.append(c_name)
                        elif "entity/TOPIC" in chip_str or "entity/USER_INTEREST" in chip_str or "entity/ART_MEDIUM" in chip_str or "entity/PLACE" in chip_str:
                            tags.append(c_name)
                if movements:
                    record["art_movements"] = ", ".join(dict.fromkeys(movements))
                if tags:
                    record["tags_and_topics"] = ", ".join(dict.fromkeys(tags))
                    
        except Exception:
            pass
            
    # 2. JSON-LD Fallback
    soup = BeautifulSoup(html, "html.parser")
    json_ld_el = soup.find("script", type="application/ld+json")
    if json_ld_el and json_ld_el.string:
        try:
            ld = json.loads(json_ld_el.string)
            if not record["title"] and "name" in ld:
                record["title"] = ld["name"]
            if not record["curatorial_description"] and "description" in ld:
                record["curatorial_description"] = ld["description"]
            if not record["creator_name"] and "author" in ld:
                author = ld["author"]
                if isinstance(author, dict):
                    record["creator_name"] = author.get("name")
                elif isinstance(author, str):
                    record["creator_name"] = author
            if not record["image_url"] and "image" in ld:
                record["image_url"] = ld["image"]
        except Exception:
            pass
            
    return record
