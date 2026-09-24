# Security, privacy and data integrity CI gate

This document describes the automated gate implemented for issue #1. It covers
what each check does, the thresholds and allowlists it uses, how to run the
checks locally, how to fix a failure, and the recommended branch protection
settings for `main`.

The repo stays private until the PR that adds this gate (`ci/security-privacy-gate`)
is merged and green. That is issue #1's hard gate: no public visibility change
and no release tag before then.

## What runs, and when

`.github/workflows/security-privacy-ci.yml` runs on:

- every pull request into `main`
- every push to any branch
- every push of a tag matching `v*`
- manual trigger (`workflow_dispatch`)

It has six jobs: `secrets`, `privacy`, `data-integrity`, `pipeline-syntax`,
`tests`, and `release-gate` (tag pushes only, gates the release on the other
five).

## The checks

### secrets

Runs [gitleaks](https://github.com/gitleaks/gitleaks) via the official
`gitleaks/gitleaks-action@v2`, scanning the full git history
(`fetch-depth: 0`), not just the working tree. Configuration is in
`.gitleaks.toml` at the repo root, which extends gitleaks' default rule set
and adds an allowlist for:

- the project's public Google Sheet id and Google's public sample sheet id
- this repo's own redaction placeholders (`REDACTED_DRIVE_FOLDER_ID`,
  `<agy-session>`, `<repo>`, `<workspace>`, `<drive-mirror>`, `<user>`,
  `<gcp-project>`, and the `agy-session-xxxx` pseudonyms)
- (no fixture paths: the tests synthesise their deliberately leaky samples
  at run time from string fragments, so no leak-shaped text is ever committed)

`gitleaks-action` only needs a `GITLEAKS_LICENSE` secret for GitHub
Organisation accounts. This repo is on a personal account, so the free tier
applies and no licence key is configured. On a pull request the job also
needs `pull-requests: read` so gitleaks-action can read the PR's commit list.

### privacy

Runs `python3 scripts/sanitize.py --check` over every tracked text file
(see [scripts/sanitize.py](#scriptssanitizepy) below). Fails the job if any
private identifier is found.

### data-integrity

Runs `python3 scripts/validate_data.py` (schema and consistency checks on
the dataset and catalogue), then, on pull requests only, the destructive-change
guard (`scripts/check_no_destructive_data_changes.py`).

### pipeline-syntax

A syntax-only ruff pass over `pipeline/`: `ruff check --select E9,F63,F7,F82
pipeline`. This is not a style check, just a guard against code that will not
parse or run.

### tests

Runs `python3 -m unittest discover tests -v`, which exercises
`scripts/sanitize.py` and `scripts/validate_data.py` directly, including
against leaky samples generated in a temporary directory.

### release-gate

Only runs on `v*` tag pushes. It `needs:` all five other jobs and fails
explicitly (`if: always()` plus a result check) if any of them failed,
whatever GitHub's default fan-in behaviour would otherwise do.

## scripts/sanitize.py

Single source of truth for the private-identifier rules. Stdlib only. The
script is scanned like any other file: it holds no private literals. Known
session UUIDs are stored as salted SHA-256 digests; usernames, the GCP
project id and truncated session prefixes are low-entropy, so they are read
at run time from `$PRIVATE_IDENTIFIERS_JSON`, `$PRIVATE_IDENTIFIERS_FILE` or
`~/.config/art-precepts/private-identifiers.json` (never committed). Without
that source the generic patterns (any Windows/Unix home path, keyword-tagged
UUIDs, Drive folder ids, emails) and the UUID digests still apply. In CI the
optional `PRIVATE_IDENTIFIERS_JSON` repository secret enables the full set on
pushes and same-repository PRs (forks do not receive secrets).

| Rule id | What it catches | Fixable |
|---|---|---|
| `agy-brain-path` | an Antigravity ("agy") session scratch path: the owner's Windows profile directory, then `.gemini\antigravity\brain\<session uuid>\...`, in either slash direction | yes, replaced by a fixed `<agy-session>\...` placeholder |
| `antigravity-repo` | the owner's local checkout path for this project (a specific Windows path under the owner's Documents folder, or a specific drive-letter path) | yes, replaced by `<repo>`; other paths on that same drive letter by `<workspace>\...` |
| `windows-user-path` | the owner's Windows profile path, any drive-letter case, backslash or forward-slash | yes, replaced by `%USERPROFILE%\...` |
| `gdrive-mirror` | the owner's local Google Drive Desktop mirror path | yes, replaced by `<drive-mirror>\...` |
| `unix-home-path` | any macOS/Linux home directory path (under `Users` or `home`) | yes, replaced by `~/` |
| `username-token` | any username listed in the private identifier source, as a standalone, case-sensitive, word-bounded token | yes, replaced by `<user>` |
| `agy-session-uuid` | this project's known Antigravity session ids, always; any other UUID only when its line mentions agy/brain/session/conversation/subagent/sender | yes, replaced by a stable `agy-session-<4 hex>` pseudonym (`sha256(uuid)[:4]`), so the same session reads consistently across docs |
| `gcp-project-id` | the project's hardcoded GCP project id | yes, replaced by `<gcp-project>` in docs (in code, fixed by hand instead: `pipeline/run_full_vision_pipeline.py` now calls `paths.gcp_project_id()`, which reads `GCP_PROJECT` from the environment and raises a clear error if unset) |
| `drive-folder-id` | `drive/folders/<id>` links and `FOLDER_ID = "<id>"` literals | yes, replaced by `REDACTED_DRIVE_FOLDER_ID` |
| `personal-email` | any email address except one ending `@users.noreply.github.com`, or exactly `noreply@anthropic.com` / `noreply@github.com` | no, check only, must be fixed by hand |

Allowlisted and never flagged: the project's Google Sheet id
(public, view-only), Google's own public sample sheet id, per-image Google
Drive file ids in `data/` and `catalogue/` frontmatter (these are not the
private *folder* id, just per-asset references), and the AI Studio app id
used by the CuratorMD sub-project.

Scope: every file tracked by git, except `bun.lock`, and binary files.
Nothing else is excluded.
`data/*.json` and `data/*.tsv` are scanned by `--check` but never rewritten
by `--fix`: a finding there is reported, not silently edited, because the
datasets are immutable by project rule (see `GEMINI.md`).

### Running locally

```sh
python3 scripts/sanitize.py --check
python3 scripts/sanitize.py --fix              # rewrites fixable violations in place
python3 scripts/sanitize.py --check path/to/file   # scan a specific path
git log -p --all | python3 scripts/sanitize.py --check --stdin   # scan history text
```

`python3 scripts/sanitize.py --emit-filter-repo-rules FILE` writes the
`git filter-repo --replace-text` expressions (0600, refuses paths inside the
repo; the file contains the private literals).

Use `--exclude GLOB` (repeatable) to skip a path, for example
`--exclude README.md` when the maintainer is actively editing it and it
should not be touched by an automated `--fix` run.

### Fixing a failure

1. Run `python3 scripts/sanitize.py --check` locally to see exactly which
   rule fired on which file and line.
2. If the rule is fixable, run `python3 scripts/sanitize.py --fix` (add
   `--exclude` for any files you don't want rewritten) and re-run `--check`.
3. If it is the `personal-email` rule, there is no auto-fix: replace the
   address by hand with a suitable placeholder, or with a
   `*@users.noreply.github.com` address if it needs to stay a working
   contact.
4. If the `gcp-project-id` rule fires inside a `pipeline/*.py` file, don't
   just delete the literal. Read the project id from the environment the
   way `pipeline/run_full_vision_pipeline.py` and `pipeline/paths.py` do
   (`paths.gcp_project_id()`, backed by the `GCP_PROJECT` environment
   variable, documented in `pipeline/README.md`).

## scripts/validate_data.py

Stdlib only. Checks, against the actual shape of the files (keys are derived
from the files themselves, not assumed):

- `data/favorites.json`, `favorites_enriched.json`, `favorites_analyzed.json`
  and `favorites_clustered.json` are each a JSON list of exactly 801 objects.
- `index` and `asset_id` are present and unique in every stage, and the
  `index -> asset_id` mapping is identical across all four stages.
- Enrichment is additive from `favorites_enriched.json` onward: every key
  present on a given record in `favorites_enriched.json` is present on the
  matching record (matched by `index`) in `favorites_analyzed.json`, and
  every key there is present on the matching record in
  `favorites_clustered.json`. (`favorites.json` itself is the raw scrape and
  is intentionally re-keyed once by enrichment: its five scrape-only fields
  `data_bgsrc`, `style`, `subtitle`, `data_ia` and `container_style` are
  dropped, and no other field may be dropped between that stage and the
  next. This one exception is expected, not a bug, and is checked
  explicitly rather than assumed away.)
- Analysed records carry all 9 analysis-stage fields added between
  `favorites_enriched.json` and `favorites_analyzed.json`
  (`chromatic_temperature`, `contrast_level`, `design_heuristics`,
  `extracted_palette`, `focal_flow`, `framing_density`, `light_profile`,
  `precept_critique`, `spatial_depth`) for 800 of the 801 records; the sole
  incomplete record must be index 602, the known image-less item. These 9
  stored fields are the flattened leaves of the 7 top-level `required` keys
  in the vision model's `response_schema` in
  `pipeline/run_full_vision_pipeline.py` (`visual_composition`,
  `color_and_light`, `texture_and_materiality`, `semiotics_and_emotion`,
  `design_vernacular`, `precept_critique`, `design_heuristics`).
- Every clustered record has a `cluster_id`.
- `catalogue/` has exactly 801 `.md` files, each with an `asset_id` in its
  frontmatter, and none of them contain a `](../images/` link (images live
  outside the repo, per the current flat layout).

### Running locally

```sh
python3 scripts/validate_data.py
```

## Destructive-change guard

`scripts/check_no_destructive_data_changes.py`, run only in the
`data-integrity` job on pull requests. Compares the PR's base and head SHAs
and fails if any file that already existed under `data/` was modified or
deleted; adding new files under `data/` is always fine. This is enforced in
CI, not by rewriting history or blocking the commit locally. The workflow
re-runs this check when a label is added or removed, not only on push, so
attaching the `data-migration` label after the fact still takes effect.

**To intentionally change an existing file under `data/`**, add the
`data-migration` label to the PR. This is a deliberate manual step: datasets
under `data/` are immutable by project rule (`GEMINI.md`), so a change that
needs the label should get real review, not just a passing check.

## Recommended branch protection for `main`

Not configured by this PR (repo settings changes are out of scope: this PR
only adds the workflow and documents the recommendation). Once merged,
set up branch protection on `main` with:

- Require a pull request before merging.
- Require status checks to pass before merging, with these required checks:
  `secrets`, `privacy`, `data-integrity`, `pipeline-syntax`, `tests`.
- Require branches to be up to date before merging.

**Note on private repos**: enforced branch protection rules need GitHub Pro
(or Team/Enterprise) on a private repository. If this repo stays private
without a paid plan, branch protection can be configured but will not be
enforced. It becomes free to enforce as soon as the repo is made public,
which, per issue #1, should only happen after this gate is merged and green.
