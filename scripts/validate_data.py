#!/usr/bin/env python3
"""Data integrity checks for the favourites dataset and catalogue.

Stdlib only. Exits 1 and prints every failure found (not just the first)
if any check fails; exits 0 and prints a short summary otherwise.

Checks:
  1. data/favorites.json, favorites_enriched.json, favorites_analyzed.json
     and favorites_clustered.json are each a JSON list of exactly 801
     objects.
  2. `index` and `asset_id` are present in every record of every stage,
     unique within each stage, and map to the same asset_id for a given
     index across all four stages (no reordering/relinking between
     stages).
  3. Enrichment is additive from favorites_enriched.json onward: every key
     present in favorites_enriched.json is present in favorites_analyzed
     .json, and every key present in favorites_analyzed.json is present
     in favorites_clustered.json. (favorites.json itself is the raw
     scrape and is intentionally re-keyed once by enrichment: its
     identifying fields -- index, asset_id, link, title -- must still
     carry through, but its scrape-only fields do not.)
  4. Every analyzed record carries the 7 analysis modules, except the one
     known image-less item (index 602): 800 of 801 records must have all
     7 populated.
  5. Every clustered record carries a cluster id.
  6. catalogue/ has exactly 801 .md files, each with frontmatter
     containing asset_id, and none of them link to ../images/.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA = REPO_ROOT / "data"
CATALOGUE = REPO_ROOT / "catalogue"

EXPECTED_COUNT = 801
IMAGELESS_INDEX = 602

STAGE_FILES = [
    "favorites.json",
    "favorites_enriched.json",
    "favorites_analyzed.json",
    "favorites_clustered.json",
]

# The keys added between favorites_enriched.json and favorites_analyzed
# .json (derived from the actual files: set(analyzed[0]) - set(enriched[0])).
# These 9 stored fields are the flattened leaves of the 7 top-level
# `required` keys in the vision model's response_schema in
# pipeline/run_full_vision_pipeline.py (visual_composition, color_and_light,
# texture_and_materiality, semiotics_and_emotion, design_vernacular,
# precept_critique, design_heuristics -- the first 5 are objects that
# flatten to one or more of the fields below). Every one of these 9 fields
# is populated together or left blank together per record, so checking
# all 9 gives the same 800/801 result as checking the 7 schema modules.
ANALYSIS_MODULE_KEYS = [
    "chromatic_temperature",
    "contrast_level",
    "design_heuristics",
    "extracted_palette",
    "focal_flow",
    "framing_density",
    "light_profile",
    "precept_critique",
    "spatial_depth",
]


def fail(errors: List[str], msg: str) -> None:
    errors.append(msg)


def load_stage(name: str, errors: List[str]):
    path = DATA / name
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"{name}: could not read/parse ({exc})")
        return None
    if not isinstance(data, list):
        fail(errors, f"{name}: expected a JSON list, got {type(data).__name__}")
        return None
    if len(data) != EXPECTED_COUNT:
        fail(errors, f"{name}: expected {EXPECTED_COUNT} records, found {len(data)}")
    return data


def check_index_asset_id(name: str, records, errors: List[str]):
    indices = []
    asset_ids = []
    for i, r in enumerate(records):
        if "index" not in r:
            fail(errors, f"{name}: record at position {i} missing 'index'")
        else:
            indices.append(r["index"])
        if "asset_id" not in r:
            fail(errors, f"{name}: record at position {i} missing 'asset_id'")
        else:
            asset_ids.append(r["asset_id"])
    if len(set(indices)) != len(indices):
        fail(errors, f"{name}: 'index' values are not unique")
    if len(set(asset_ids)) != len(asset_ids):
        fail(errors, f"{name}: 'asset_id' values are not unique")


def check_index_asset_id_consistency(stages, errors: List[str]):
    base_name = STAGE_FILES[0]
    base = stages.get(base_name)
    if base is None:
        return
    base_map = {r["index"]: r["asset_id"] for r in base if "index" in r and "asset_id" in r}
    for name in STAGE_FILES[1:]:
        records = stages.get(name)
        if records is None:
            continue
        this_map = {r["index"]: r["asset_id"] for r in records if "index" in r and "asset_id" in r}
        mismatched = [i for i, aid in base_map.items() if this_map.get(i) != aid]
        if mismatched:
            fail(errors, f"{name}: {len(mismatched)} index(es) map to a different asset_id "
                          f"than in {base_name}, e.g. {mismatched[:5]}")
        missing = set(base_map) - set(this_map)
        if missing:
            fail(errors, f"{name}: missing {len(missing)} index(es) present in {base_name}, "
                          f"e.g. {sorted(missing)[:5]}")


# The only keys favorites.json -> favorites_enriched.json is allowed to
# drop: raw HTML-scrape artefacts with no derived equivalent. Any other
# key disappearing at this transition is a real integrity failure, not
# expected re-keying.
ALLOWED_DROPPED_KEYS = {"data_bgsrc", "style", "subtitle", "data_ia", "container_style"}


def _keys_by_index(records):
    return {r["index"]: set(r.keys()) for r in records if "index" in r}


def check_additive_keys(stages, errors: List[str]):
    # favorites.json -> favorites_enriched.json: every dropped key must be
    # in ALLOWED_DROPPED_KEYS, checked per record (not just record 0).
    fav = stages.get("favorites.json")
    enr = stages.get("favorites_enriched.json")
    if fav and enr:
        fav_by_idx = _keys_by_index(fav)
        enr_by_idx = _keys_by_index(enr)
        bad = {}
        for idx, fav_keys in fav_by_idx.items():
            enr_keys = enr_by_idx.get(idx)
            if enr_keys is None:
                continue  # reported separately by check_index_asset_id_consistency
            unexpectedly_dropped = (fav_keys - enr_keys) - ALLOWED_DROPPED_KEYS
            if unexpectedly_dropped:
                bad[idx] = sorted(unexpectedly_dropped)
        if bad:
            sample = dict(list(bad.items())[:5])
            fail(errors, f"favorites_enriched.json: {len(bad)} record(s) dropped a key from "
                          f"favorites.json that is not in the allowed scrape-artefact set "
                          f"{sorted(ALLOWED_DROPPED_KEYS)}, e.g. {sample}")

    # From favorites_enriched.json onward, enrichment must be additive-only,
    # checked per record (matched by index), not just record 0.
    chain = ["favorites_enriched.json", "favorites_analyzed.json", "favorites_clustered.json"]
    for prev_name, next_name in zip(chain, chain[1:]):
        prev = stages.get(prev_name)
        nxt = stages.get(next_name)
        if not prev or not nxt:
            continue
        prev_by_idx = _keys_by_index(prev)
        next_by_idx = _keys_by_index(nxt)
        bad = {}
        for idx, prev_keys in prev_by_idx.items():
            next_keys = next_by_idx.get(idx)
            if next_keys is None:
                continue
            missing = prev_keys - next_keys
            if missing:
                bad[idx] = sorted(missing)
        if bad:
            sample = dict(list(bad.items())[:5])
            fail(errors, f"{next_name}: {len(bad)} record(s) are missing key(s) present in "
                          f"{prev_name}, e.g. {sample}")


def check_analysis_modules(stages, errors: List[str]):
    analyzed = stages.get("favorites_analyzed.json")
    if not analyzed:
        return
    complete = 0
    incomplete_indices = []
    for r in analyzed:
        modules_present = all(r.get(k) not in (None, "", []) for k in ANALYSIS_MODULE_KEYS)
        if modules_present:
            complete += 1
        else:
            incomplete_indices.append(r.get("index"))

    expected_complete = EXPECTED_COUNT - 1  # index 602 is the known image-less item
    if complete != expected_complete:
        fail(errors, f"favorites_analyzed.json: expected {expected_complete} records with all "
                      f"{len(ANALYSIS_MODULE_KEYS)} analysis modules populated, found {complete} "
                      f"(incomplete indices: {incomplete_indices})")
    elif incomplete_indices != [IMAGELESS_INDEX]:
        fail(errors, f"favorites_analyzed.json: the one incomplete record should be index "
                      f"{IMAGELESS_INDEX} (the known image-less item), found "
                      f"{incomplete_indices} instead")


def check_cluster_ids(stages, errors: List[str]):
    clustered = stages.get("favorites_clustered.json")
    if not clustered:
        return
    missing = [r.get("index") for r in clustered if r.get("cluster_id") in (None, "")]
    if missing:
        fail(errors, f"favorites_clustered.json: {len(missing)} record(s) missing cluster_id: "
                      f"{missing[:10]}")


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
ASSET_ID_RE = re.compile(r'^asset_id:\s*"?([^"\n]+)"?\s*$', re.MULTILINE)
IMAGES_LINK_RE = re.compile(r"\]\(\.\./images/")


def check_catalogue(errors: List[str]):
    if not CATALOGUE.is_dir():
        fail(errors, "catalogue/ directory not found")
        return
    md_files = sorted(CATALOGUE.glob("*.md"))
    if len(md_files) != EXPECTED_COUNT:
        fail(errors, f"catalogue/: expected {EXPECTED_COUNT} .md files, found {len(md_files)}")

    missing_asset_id = []
    bad_image_links = []
    for f in md_files:
        text = f.read_text(encoding="utf-8")
        fm_match = FRONTMATTER_RE.match(text)
        if not fm_match or not ASSET_ID_RE.search(fm_match.group(1)):
            missing_asset_id.append(f.name)
        if IMAGES_LINK_RE.search(text):
            bad_image_links.append(f.name)

    if missing_asset_id:
        fail(errors, f"catalogue/: {len(missing_asset_id)} file(s) missing asset_id in "
                      f"frontmatter: {missing_asset_id[:10]}")
    if bad_image_links:
        fail(errors, f"catalogue/: {len(bad_image_links)} file(s) contain a "
                      f"'](../images/' link: {bad_image_links[:10]}")


def main() -> int:
    errors: List[str] = []
    stages = {}
    for name in STAGE_FILES:
        records = load_stage(name, errors)
        stages[name] = records
        if records:
            check_index_asset_id(name, records, errors)

    check_index_asset_id_consistency(stages, errors)
    check_additive_keys(stages, errors)
    check_analysis_modules(stages, errors)
    check_cluster_ids(stages, errors)
    check_catalogue(errors)

    if errors:
        print(f"{len(errors)} data integrity failure(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("Data integrity OK: 4 stages x 801 records, additive enrichment, "
          "800/801 analysis modules, cluster ids present, 801 catalogue notes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
