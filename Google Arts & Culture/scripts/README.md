# Scripts

Recovered from Google Antigravity (agy) session scratch directories on OPTILAB on
2026-09-24. These were working scratch scripts, not designed for portability: most
contain hardcoded Windows paths (`%USERPROFILE%\...`, brain scratch dirs) and a
hardcoded Google Sheet ID. Paths will need adjusting before any of these can run
again — see the security/hygiene notes in the recovery PR/commit for specifics.

## Pipeline scripts (recovered from session `agy-session-2287`)

| Script | Purpose |
|---|---|
| `gac_parser.py` | Parses Google Arts & Culture asset HTML (`window.INIT_data` payload) into structured metadata records (title, creator, dimensions, etc.). Imported as a shared helper by `run_full_enrichment_pipeline.py`. |
| `extract_and_upload_v2.py` | Extracts favorited items from a saved GAC MHTML snapshot, parses each with BeautifulSoup, and uploads/creates the master Google Sheet. |
| `download_and_link_images.py` | Async (httpx) bulk downloader for high-resolution preview images, with Google Drive upload/linking and Sheet updates. |
| `run_full_vision_pipeline.py` | Orchestrates the multimodal (Gemini/Vertex AI) vision analysis pass across all catalogued items, caching results in a local SQLite DB, and pushes precept critiques back to the Sheet. |
| `run_full_enrichment_pipeline.py` | Async enrichment pipeline that re-parses GAC pages (via `gac_parser`) and enriches records with additional metadata (Wikidata, dimensions, etc.), caching to SQLite. |
| `generate_phase2a_clustering.py` | Builds latent visual/design clusters from the enriched dataset using TF-IDF, SVD/PCA, and KMeans (scikit-learn), including CIELAB color-space conversion. |
| `generate_derived_entities.py` | Derives secondary entities/fields from the enriched JSON/TSV dataset and writes them back out. |
| `finish_catalogue_and_sheet.py` | Finalizes the local catalogue (markdown notes) and syncs it into the master Google Sheet. |
| `sync_enriched_sheet.py` | Pushes an enriched TSV's contents into the Google Sheet via the Sheets API (using a `gcloud` access token). |
| `update_sheet_precepts.py` | Updates the Sheet's precept/heuristic columns from a locally analyzed TSV. |

## Recovery scripts (recovered from session `agy-session-addd`)

| Script | Purpose |
|---|---|
| `recovery/restore_and_build_sheets.py` | Rebuilds the Google Sheet from a prior Drive revision (`revision_115.xlsx`) plus the local analyzed/enriched JSON files, after an apparent data-loss incident. |
| `recovery/verify_sheets.py` | Verifies Sheet metadata and content against expectations post-recovery via the Sheets API. |
| `recovery/verify_specs.py` | Defines/checks the expected column spec (list of 47 field names) for the master Sheet. |

## Audit scripts (recovered from session `agy-session-912e`)

| Script | Purpose |
|---|---|
| `audit/audit_script.py` | Audits the multimodal analysis SQLite cache (`analysis_cache` table) — row counts, output size, basic sanity checks. |
| `audit/verify_and_report.py` | Deeper verification/report pass over the analysis DB and enriched JSON — timing, hashing, statistics — likely feeding a written audit report. |
