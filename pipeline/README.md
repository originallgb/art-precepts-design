# Scripts

Recovered from Google Antigravity (agy) session scratch directories on OPTILAB on
2026-09-24. These were working scratch scripts, not designed for portability, and
most are historical: they assume the old `%USERPROFILE%\...` / `<drive-mirror>\...`
Windows/OPTILAB machine, or predate the repo layout below, and won't run again
without that machine and its Drive Desktop mirror.

## Paths and environment

`paths.py` holds the shared, repo-relative constants (`REPO_ROOT`, `DATA`,
`CATALOGUE`, `CLUSTERS`) plus the three IDs scripts need:

- `SHEET_ID`: defaults to the project's Google Sheet ID. Override with the
  `GAC_SHEET_ID` environment variable if you're pointing at a different sheet.
- `drive_folder_id()` and `drive_images_folder_id()`: each reads its own
  environment variable (`GAC_DRIVE_FOLDER_ID`, `GAC_DRIVE_IMAGES_FOLDER_ID`)
  and raises a clear error if it's unset. Both Drive folders are private, so
  neither ID is hardcoded here; export them yourself before running a script
  that needs one:
  ```
  GAC_DRIVE_IMAGES_FOLDER_ID=... python pipeline/download_and_link_images.py
  ```
- `gcp_project_id()`: reads the `GCP_PROJECT` environment variable and
  raises a clear error if it's unset. The GCP/Vertex AI project ID isn't
  hardcoded here either; export it before running a script that needs it:
  ```
  GCP_PROJECT=your-project python pipeline/run_full_vision_pipeline.py
  ```

Scripts directly under `pipeline/` do `import paths` as-is. Scripts one level
deeper, in `pipeline/recovery/` and `pipeline/audit/`, add their parent
directory to `sys.path` first so the same import works when run as
`python pipeline/recovery/<script>.py` or `python pipeline/audit/<script>.py`.

Genuinely machine-local paths (the agy brain-scratch SQLite caches, the
OPTILAB Google Drive Desktop mirror, the original MHTML download under
`%USERPROFILE%\Downloads\`) are left as hardcoded Windows paths, marked
`# historical` in a comment. They have no repo-relative equivalent.

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

**Historical / won't run as-is**: `extract_and_upload_v2.py` (needs a saved
MHTML snapshot at a Windows Downloads path, one-time initial extraction),
`download_and_link_images.py` and `run_full_vision_pipeline.py` (both assume
`images/`, which was dropped from this repo for copyright reasons before it
went public). The rest run against repo-relative paths via `paths.py`, but
still need a live `gcloud` token and network access to the Sheet.

## Recovery scripts (recovered from session `agy-session-addd`)

| Script | Purpose |
|---|---|
| `recovery/restore_and_build_sheets.py` | Rebuilds the Google Sheet from a prior Drive revision (`revision_115.xlsx`) plus the local analyzed/enriched JSON files, after an apparent data-loss incident. |
| `recovery/verify_sheets.py` | Verifies Sheet metadata and content against expectations post-recovery via the Sheets API. |
| `recovery/verify_specs.py` | Defines/checks the expected column spec (list of 47 field names) for the master Sheet. |

**Historical**: `recovery/restore_and_build_sheets.py` needs
`revision_115.xlsx`, a specific Drive revision export that only existed on
OPTILAB during the recovery incident. Kept for the record.

## Audit scripts (recovered from session `agy-session-912e`)

| Script | Purpose |
|---|---|
| `audit/audit_script.py` | Audits the multimodal analysis SQLite cache (`analysis_cache` table) — row counts, output size, basic sanity checks. |
| `audit/verify_and_report.py` | Deeper verification/report pass over the analysis DB and enriched JSON — timing, hashing, statistics — likely feeding a written audit report. |

**Historical**: both need the agy brain-scratch SQLite cache and, for
`verify_and_report.py`, a specific task log, neither of which exist outside
OPTILAB. `audit_script.py` also reads local image files that no longer exist
in this repo.
