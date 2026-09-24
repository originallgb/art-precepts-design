# 2026-09-24: recovering the pipeline, then going public

Two separate pieces of work landed on the same day.

## Recovering the pipeline

The scripts in `pipeline/` (extraction, enrichment, the vision pass, the
Phase 2a clustering, the recovery scripts, the audit scripts) existed only
as working files in Antigravity session scratch directories on OPTILAB. The
session that produced them was gone. I found them again by going through
the scratch directories of three separate agy sessions and pulling out
everything that mattered, then committing it as `pipeline/` in one recovery
commit.

They weren't written for portability. Most of them hardcode a Windows path
(`%USERPROFILE%\...`), a Google Drive Desktop mirror path (`<drive-mirror>\...`),
or a cwd-relative `"Google Arts & Culture/..."` path that assumed the old
nested layout. Some hardcode the private Drive folder ID. None of that was a
problem while the repo was private and lived on one machine. It became a
problem the moment I decided to publish.

## Going public

Four things needed handling before this could be a public repo:

**Images.** 800 of them, third-party, on loan from museums via Google Arts &
Culture, at least 150 carrying an explicit copyright notice. I dropped them
entirely. Every catalogue note now links to its GAC source page instead of
embedding the image.

**The Drive folder ID.** It was in the README and in a couple of scripts. I
pulled it out of both. Scripts that need it now read `GAC_DRIVE_FOLDER_ID`
from the environment, via `pipeline/paths.py`, and fail with a clear message
if it's not set, rather than falling back to a hardcoded value.

**Layout.** Everything sat under `Google Arts & Culture/`, whose spaces and
ampersand made every path reference awkward. I flattened it by role:
`data/`, `catalogue/`, `clusters/`, `pipeline/`, `docs/`, using `git mv` so
history follows each file.

**The README.** The old one still had an unstarted roadmap for phases that
were, in fact, already done. Rewritten from scratch, in the open, as what
this actually is: a learning project, not a finished product, with the
mistakes left in.

None of this touched the analysis itself. The 801 catalogue notes, their
precept critiques, and the cluster assignments are untouched. What changed
is where things live and what's honest about how they got made.
