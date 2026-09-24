#!/usr/bin/env python3
"""Destructive-change guard for data/ (PR context only).

Fails if a pull request modifies or deletes any file that already existed
under data/ on the PR's base branch, unless the PR carries the
`data-migration` label. Adding new files under data/ is always fine.

Stdlib only, driven entirely by environment variables set by the calling
GitHub Actions step (see .github/workflows/security-privacy-ci.yml):

    BASE_SHA        - base commit of the PR
    HEAD_SHA        - head commit of the PR
    PR_LABELS       - comma-separated label names on the PR

Run locally against two refs for a dry run:
    BASE_SHA=origin/main HEAD_SHA=HEAD PR_LABELS= python3 \
        scripts/check_no_destructive_data_changes.py
"""
from __future__ import annotations

import os
import subprocess
import sys

DATA_MIGRATION_LABEL = "data-migration"


def git_diff_status(base: str, head: str):
    result = subprocess.run(
        ["git", "diff", "--name-status", f"{base}...{head}", "--", "data/"],
        capture_output=True, text=True, check=True,
    )
    return [line for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    base = os.environ.get("BASE_SHA")
    head = os.environ.get("HEAD_SHA", "HEAD")
    labels_raw = os.environ.get("PR_LABELS", "")
    labels = {l.strip() for l in labels_raw.split(",") if l.strip()}

    if not base:
        print("BASE_SHA not set; nothing to compare (not a PR context). Skipping.")
        return 0

    changes = git_diff_status(base, head)
    if not changes:
        print("No changes under data/.")
        return 0

    offending = []
    added = []
    for line in changes:
        parts = line.split("\t")
        status = parts[0]
        if status.startswith("A"):
            added.append(parts[-1])
            continue
        # M (modified), D (deleted), R (renamed), C (copied over an
        # existing path) all touch an existing file.
        offending.append(line)

    if added:
        print(f"{len(added)} new file(s) added under data/ (fine): {added}")

    if not offending:
        print("No existing data/ files were modified or deleted.")
        return 0

    if DATA_MIGRATION_LABEL in labels:
        print(f"'{DATA_MIGRATION_LABEL}' label present; allowing "
              f"{len(offending)} change(s) to existing data/ file(s):")
        for line in offending:
            print(f"  {line}")
        return 0

    print(f"BLOCKED: {len(offending)} existing file(s) under data/ were modified or "
          f"deleted, and this PR does not carry the '{DATA_MIGRATION_LABEL}' label:",
          file=sys.stderr)
    for line in offending:
        print(f"  {line}", file=sys.stderr)
    print("\nDatasets under data/ are immutable by project rule (see GEMINI.md). "
          "If this change is a deliberate, reviewed migration, add the "
          f"'{DATA_MIGRATION_LABEL}' label to the PR.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
