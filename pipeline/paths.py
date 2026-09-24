"""Repo-relative paths and IDs shared by the pipeline scripts.

Kept deliberately tiny: constants and three lazy ID lookups, no logic. Import
this as `import paths` (or `from paths import ...`). Each script that
needs it inserts its own directory's parent onto sys.path first, so it
works whether you run `python pipeline/<script>.py` from the repo root
or the script lives one level deeper, in pipeline/recovery/ or
pipeline/audit/.
"""
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA = REPO_ROOT / "data"
CATALOGUE = REPO_ROOT / "catalogue"
CLUSTERS = REPO_ROOT / "clusters"

# The Sheet is view-only once public; the ID itself isn't sensitive.
SHEET_ID = os.environ.get("GAC_SHEET_ID", "1Tznbdor6-JFLkGNtuN5StasMSopnLkhdqzgbq7NWdAU")


def drive_folder_id():
    """Return the private Google Drive folder ID from the environment.

    Not hardcoded here: the folder is personal and private. Set
    GAC_DRIVE_FOLDER_ID before running a script that needs it, e.g.:
        GAC_DRIVE_FOLDER_ID=... python pipeline/download_and_link_images.py
    """
    try:
        return os.environ["GAC_DRIVE_FOLDER_ID"]
    except KeyError as exc:
        raise RuntimeError(
            "GAC_DRIVE_FOLDER_ID is not set. Export it before running this "
            "script; see pipeline/README.md."
        ) from exc


def drive_images_folder_id():
    """Return the private Google Drive 'images' subfolder ID.

    A second, distinct private ID from drive_folder_id(); also not
    hardcoded. Set GAC_DRIVE_IMAGES_FOLDER_ID before running a script
    that needs it.
    """
    try:
        return os.environ["GAC_DRIVE_IMAGES_FOLDER_ID"]
    except KeyError as exc:
        raise RuntimeError(
            "GAC_DRIVE_IMAGES_FOLDER_ID is not set. Export it before "
            "running this script; see pipeline/README.md."
        ) from exc


def gcp_project_id():
    """Return the GCP/Vertex AI project ID from the environment.

    Not hardcoded here: the project ID identifies a specific billing
    account. Set GCP_PROJECT before running a script that needs it, e.g.:
        GCP_PROJECT=your-project python pipeline/run_full_vision_pipeline.py
    """
    try:
        return os.environ["GCP_PROJECT"]
    except KeyError as exc:
        raise RuntimeError(
            "GCP_PROJECT is not set. Export it before running this "
            "script; see pipeline/README.md."
        ) from exc
