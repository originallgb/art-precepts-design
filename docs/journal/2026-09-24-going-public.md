# 2026-09-24: going public

The aim of this project hasn't changed. I want to turn years of saved Google
Arts & Culture favourites into a corpus I can reference, and translate into
`design.md` specs for UX work, interiors, and design language. Getting
there, I'd used the project to try a lot of tools and processes. The repo
had the results. It didn't yet explain how they were made, and it wasn't
safe to publish. Going public meant fixing both.

## Recovering the pipeline

The scripts behind every stage (extraction, enrichment, the vision pass,
the clustering, the Sheet recovery, the audits) had only ever existed as
working files in Antigravity session scratch directories on another
machine. None of it had been committed. I went through those directories,
pulled out everything that mattered, and committed it as `pipeline/`.

They weren't written for portability. Most hardcoded Windows paths, a
Google Drive mirror path, or paths that assumed the old nested layout.
`pipeline/paths.py` now resolves everything from the repo root, and the
private Drive folder IDs come from environment variables.

## Making it safe to publish

**Images.** 800 of them, third-party, held by museums and shown via Google
Arts & Culture, at least 150 with an explicit copyright notice. I dropped
them, and every catalogue note now links to its GAC source page instead.
The analysis text in each note is untouched.

**History.** Removing the images from the current tree wasn't enough, since
they'd still sit in every earlier commit. I rewrote the history to strip
the images, the two private Drive folder IDs, and my personal email, then
pushed it to a fresh repo. The original stays private as an archive,
along with its pull requests.

**Layout.** Everything sat under a `Google Arts & Culture/` folder, whose
spaces and ampersand made every path awkward. It's now flat by role:
`data/`, `catalogue/`, `clusters/`, `pipeline/`, `docs/`.

## Writing it up

The old README had a roadmap for phases that were already done. Rewriting
it meant retracing how the analysis actually happened, from the Antigravity
session history for 2026-09-04.

The story starts earlier than the repo's first real commit. On
2026-09-02 I built CuratorMD in Google AI Studio from a one-line prompt.
It read the favourites Sheet and ran three Gemini roles in turn: an
analyst per artwork, a curator over the set, and a design-systems author
for the `design.md`. Going back through it for this write-up, two things
stood out. Its analysis never sent the images, only titles and metadata.
And the prompt that would have scaled it to the whole Sheet died on a
quota error. The app is now in `apps/curatormd/`, exported as it stands.

Gemini's summary of that first build turned out to be the real guide for
the whole project, before I got distracted restyling the app. It's now
kept verbatim in `docs/process/curatormd_original_brief.md`.

Two days later, back in Antigravity, I asked for an advisor agent to plan
the analysis and propose "board members". It came back with five personas: a Formalist, an Industrial & UX
Designer, a Cultural Semiotician, a Spatial Materialist, and a Colorist &
Typographer. Those became the 5 Angles of a single structured prompt, one
Gemini call per image, rather than five separate agents. After a
three-image pilot I was offered live parallel Flash, batch Flash, or batch
Pro, and picked live Flash, while asking for the Pro batch requirements to
be written up. I'd remembered batch as the route taken. The session history
says otherwise, which is a good argument for keeping it.

Retracing it also turned up a bad number. The telemetry audit put the whole
run at $0.077, using per-token rates far below Gemini 2.5 Flash's published
price. Recomputed from the audit's own token counts at list price, the run
cost at least $2.08, more once thinking tokens are counted. The pricing
estimate I was given before the run had the same error. The audit stays as
written, with a correction note at the top.

## Still to do

The scripts, docs, and reviews still carry machine-specific details:
Windows paths, a username, Antigravity session IDs, the GCP project name.
Rather than hand-edit them once, I'll add a CI workflow that sanitises
them and fails the build if new ones creep in.
