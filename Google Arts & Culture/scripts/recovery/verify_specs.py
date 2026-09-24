import json

cols = [
    "thumbnail_preview", "index", "title", "original_title", "creator", "creator_lifespan",
    "creator_nationality", "date_created", "location_created", "medium", "object_type",
    "aspect_ratio", "aspect_ratio_standard", "orientation", "master_width_px", "master_height_px",
    "megapixels", "focal_anchors_count", "physical_dimensions_raw", "parsed_height_cm",
    "parsed_width_cm", "parsed_depth_cm", "resolution_density_dpi", "partner_name",
    "partner_city_country", "partner_website", "partner_lat", "partner_long",
    "curatorial_description", "provenance", "credit_line", "inventory_number",
    "external_catalog_url", "rights", "art_movements", "tags_and_topics", "dominant_color",
    "wikidata_qid", "wikipedia_url", "commons_image_url", "asset_id", "link",
    "image_url", "max_preview_url", "local_image_file", "gdrive_file_id", "gdrive_image_url",
    "precept_critique", "design_heuristics", "extracted_palette", "chromatic_temperature",
    "light_profile", "contrast_level", "focal_flow", "framing_density", "spatial_depth"
]

# Widths tailored strictly according to requirements:
# - index, aspect_ratio, orientation, dates: 70-95px, centered.
# - title, creator, medium, partner_name: 200-240px, left-aligned.
# - precept_critique: 480px, left-aligned, vertical alignment TOP, wrapStrategy = "WRAP".
# - design_heuristics: 520px, left-aligned, vertical alignment TOP, wrapStrategy = "WRAP".
# - extracted_palette: 220px, font Roboto Mono / monospace.
# - other short attributes (chromatic_temperature, light_profile, contrast_level, framing_density, spatial_depth): 110-140px, centered.

col_specs = {
    "thumbnail_preview": {"width": 85, "align": "CENTER"},
    "index": {"width": 75, "align": "CENTER"},
    "title": {"width": 240, "align": "LEFT"},
    "original_title": {"width": 200, "align": "LEFT"},
    "creator": {"width": 220, "align": "LEFT"},
    "creator_lifespan": {"width": 110, "align": "CENTER"},
    "creator_nationality": {"width": 120, "align": "CENTER"},
    "date_created": {"width": 90, "align": "CENTER"},
    "location_created": {"width": 160, "align": "LEFT"},
    "medium": {"width": 200, "align": "LEFT"},
    "object_type": {"width": 160, "align": "LEFT"},
    "aspect_ratio": {"width": 85, "align": "CENTER"},
    "aspect_ratio_standard": {"width": 95, "align": "CENTER"},
    "orientation": {"width": 90, "align": "CENTER"},
    "master_width_px": {"width": 85, "align": "CENTER"},
    "master_height_px": {"width": 85, "align": "CENTER"},
    "megapixels": {"width": 85, "align": "CENTER"},
    "focal_anchors_count": {"width": 85, "align": "CENTER"},
    "physical_dimensions_raw": {"width": 160, "align": "LEFT"},
    "parsed_height_cm": {"width": 85, "align": "CENTER"},
    "parsed_width_cm": {"width": 85, "align": "CENTER"},
    "parsed_depth_cm": {"width": 85, "align": "CENTER"},
    "resolution_density_dpi": {"width": 95, "align": "CENTER"},
    "partner_name": {"width": 220, "align": "LEFT"},
    "partner_city_country": {"width": 150, "align": "LEFT"},
    "partner_website": {"width": 160, "align": "LEFT"},
    "partner_lat": {"width": 85, "align": "CENTER"},
    "partner_long": {"width": 85, "align": "CENTER"},
    "curatorial_description": {"width": 360, "align": "LEFT", "wrap": True},
    "provenance": {"width": 240, "align": "LEFT", "wrap": True},
    "credit_line": {"width": 200, "align": "LEFT", "wrap": True},
    "inventory_number": {"width": 110, "align": "CENTER"},
    "external_catalog_url": {"width": 150, "align": "LEFT"},
    "rights": {"width": 180, "align": "LEFT"},
    "art_movements": {"width": 160, "align": "LEFT"},
    "tags_and_topics": {"width": 240, "align": "LEFT", "wrap": True},
    "dominant_color": {"width": 110, "align": "CENTER", "mono": True},
    "wikidata_qid": {"width": 95, "align": "CENTER"},
    "wikipedia_url": {"width": 160, "align": "LEFT"},
    "commons_image_url": {"width": 160, "align": "LEFT"},
    "asset_id": {"width": 120, "align": "CENTER"},
    "link": {"width": 160, "align": "LEFT"},
    "image_url": {"width": 160, "align": "LEFT"},
    "max_preview_url": {"width": 160, "align": "LEFT"},
    "local_image_file": {"width": 200, "align": "LEFT"},
    "gdrive_file_id": {"width": 140, "align": "CENTER"},
    "gdrive_image_url": {"width": 160, "align": "LEFT"},
    "precept_critique": {"width": 480, "align": "LEFT", "wrap": True},
    "design_heuristics": {"width": 520, "align": "LEFT", "wrap": True},
    "extracted_palette": {"width": 220, "align": "LEFT", "mono": True},
    "chromatic_temperature": {"width": 130, "align": "CENTER"},
    "light_profile": {"width": 120, "align": "CENTER"},
    "contrast_level": {"width": 110, "align": "CENTER"},
    "focal_flow": {"width": 360, "align": "LEFT", "wrap": True},
    "framing_density": {"width": 120, "align": "CENTER"},
    "spatial_depth": {"width": 130, "align": "CENTER"}
}

print(f"Total cols: {len(cols)}, total specs: {len(col_specs)}")
assert len(cols) == len(col_specs)
for i, c in enumerate(cols):
    assert c in col_specs, f"Missing {c}"
print("All 56 columns mapped successfully!")
