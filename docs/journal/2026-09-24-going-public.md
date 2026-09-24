# 2026-09-24: recovering the pipeline, then going public

Two separate pieces of work landed on the same day.

## Recovering the pipeline

The scripts in `pipeline/` (extraction, enrichment, the vision pass, the
Phase 5 clustering, the recovery scripts, the audit scripts) had only ever
existed as working files in Antigravity session scratch directories on
OPTILAB, across three separate agy sessions. None of it had been committed.
I went through those scratch directories, pulled out everything that
mattered, and committed it as `pipeline/` in one recovery commit.

They weren't written for portability. Most of them hardcode a Windows path
(`%USERPROFILE%\...`), a Google Drive Desktop mirror path (`<drive-mirror>\...`),
or a cwd-relative `"Google Arts & Culture/..."` path that assumed the old
nested layout. One script also hardcoded the private Drive folder ID. None
of that was a problem while the repo was private and lived on one machine.
It became a problem the moment I decided to publish.

## Going public

Four things needed handling before this could be a public repo:

**Images.** 800 of them, third-party, on loan from museums via Google Arts &
Culture, at least 150 carrying an explicit copyright notice. I dropped them
entirely. Every catalogue note now links to its GAC source page instead of
embedding the image. The analysis text in each note is untouched.

**The Drive folder ID.** It was in the README and in one script, which
never actually used it (dead code left over from an earlier version). I
pulled the ID out of both places and moved the lookup into
`pipeline/paths.drive_folder_id()`, which reads `GAC_DRIVE_FOLDER_ID` from
the environment and fails with a clear message if it's not set, for
whatever later needs it. A second, separate private Drive folder ID (for
the images subfolder, this one genuinely in use) turned up in the same
audit and got the same treatment, as `drive_images_folder_id()` /
`GAC_DRIVE_IMAGES_FOLDER_ID`.

**Layout.** Everything sat under `Google Arts & Culture/`, whose spaces and
ampersand made every path reference awkward. I flattened it by role:
`data/`, `catalogue/`, `clusters/`, `pipeline/`, `docs/`, using `git mv` so
history follows each file.

**The README.** The old one still had an unstarted roadmap for phases that
were, in fact, already done by 2026-09-05. Rewritten from scratch as what
this actually is: a learning project, with the mistakes left in rather than
smoothed over.

The clustering, the catalogue notes, and their generated analysis are
otherwise unchanged by any of this.
