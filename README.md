# Art Precepts Design

Years of saved favourites on Google Arts & Culture, turned into a corpus I
can reference and translate into `design.md` specs for UX work, interiors,
and design language. Each of the 801 pieces is read by a Gemini vision
pipeline from five design perspectives, then the set is clustered into
aesthetic families. Built in the open, mistakes included.

## What this is for

I've been saving art I respond to on Google Arts & Culture for years. The
collection says something about my taste that I couldn't articulate or use.
The goal is a semantic translation of those selections: a structured,
amendable corpus I can query when making real design decisions, and from
which to seed `design.md` playbooks (colour tokens, layout rules, material
cues, do's and don'ts) for UX projects, interior design, and wider design
language work.

## The name

The repo started life on 2026-09-02 as `art-to-deisng`, typo included,
created by AI Studio from its app template. It became `art-to-design` two
days later. When I recreated it on 2026-09-05 to shed that template
lineage, I renamed it `art-precepts-design`. Art and Design sit on the flanks, and
Precepts, the rules the pipeline extracts, hold the middle as the bridge
between them. The agent read that as a chiasmus. I'd call it a synchysis:
art and design aren't mirrored, they're interlocked, with the precepts
woven through both. It also made me do a double take. English expects
`art-design-precepts`, a flat compound. Putting precepts in the middle
inverts that into a sequence, art to precepts to design, which is the
pipeline in three words. That small bit of syntactic friction is the
point, and I've since written it into my naming rules.

## Why in public

Along the way I leaned into every stage: scraping the favourites out of
GAC, enriching them from museum metadata and Wikidata, the multimodal
analysis, clustering. Each was a chance to try a different tool, process,
or model, sketch an idea, and iterate. This repo keeps that record,
including the parts that went wrong. `GEMINI.md` is the rule set I wrote
for the workspace after the first Google Sheet got overwritten in place,
and `docs/process/engineering_learnings_and_governance.md` documents why.
`.agents/skills/self-audit/` is the check that's meant to run before any
phase gets called done.

## Where it stands

Using the phase numbering from the original plan:

- **Phase 0, extraction**: 801 favourites pulled from GAC, parsed, and
  pushed to a Google Sheet. Done, 2026-08-30 to 31; first committed
  2026-09-04.
- **Phase 1, metadata enrichment**: curatorial fields, Wikidata links,
  physical dimensions, aspect ratios. Done.
- **Phase 2, visual asset caching**: 800 images collected and synced. Done
  at the time; the images have since been dropped from this repo for
  copyright reasons ahead of going public.
- **Phase 3, architecture planning**: Draft Plan 1 committed, then an
  advisory pass that designed the five-perspective analysis (below).
- **Phase 4, multimodal analysis**: all 800 image-bearing items analysed by
  Gemini 2.5 Flash on Vertex AI. Done, 2026-09-04. See
  [The analysis pipeline](#the-analysis-pipeline).
- **Phase 5, latent clustering**: done, 2026-09-05, but not as planned. The
  plan called for UMAP/HDBSCAN; what actually ran was k-means over a
  59-dimension feature vector (CIELAB colour, spatial/categorical
  attributes, TF-IDF semantic text). ADR 001 documents the method and is
  still `PROPOSED`, not accepted: Grok's review said not to accept it as
  written, because the document overstated its empirical validation and
  didn't account for the change of algorithm.
- **Phase 6, catalogue notes**: the 801 markdown notes in `catalogue/`. 800
  of them carry the generated critique and heuristics; one (index 0602, an
  interactive tour card with no static image) has none because it was never
  analysed. Done.
- **Phase 7, the design playbook**: not started. `design.md` standards per
  cluster.

Later documents (the ADR, the reviews, `generate_phase2a_clustering.py`)
call the clustering work "Phase 2a" rather than Phase 5. That's a second,
narrower numbering: `docs/process/implementation_plan.md` bundles Phases
5-7 above into its own "Phase 2", with sub-phases 2a (clustering and the
ADR), 2b (catalogue notes), 2c/2d (playbooks). This README keeps the
original 0-7 numbering throughout.

## The first attempt: CuratorMD

Before the pipeline in this repo, there was an app. On 2026-09-02, with
the favourites already in a Google Sheet, I opened Google AI Studio's
Build mode and gave Gemini 3.7 Flash one rough prompt: an app that reads
my GAC links from a sheet, runs visual and compositional analysis,
curates the pieces into non-obvious themes, and writes `design.md`
guidelines. Five minutes later it had built CuratorMD, a full-stack
React and Express app. The code is in `apps/curatormd/`, exported
unchanged, with the build conversation in `BUILD_HISTORY.md`.

CuratorMD split the work across three Gemini calls, each playing a
different expert:

1. An art historian and composition analyst, once per artwork: palette
   with roles, composition type, visual weight, focal points, type
   pairing.
2. A museum curator, once over the whole set: two to four cross-cutting
   themes with a short essay each.
3. A design-systems author: the `design.md` and a set of tokens, with a
   live sandbox and exports to CSS, Tailwind, and Figma tokens.

It ran on my AI Studio API key. Two things sent me elsewhere. The
per-artwork "visual" analysis never saw the images: the app sends Gemini
the title, artist, date, medium, and museum, and the model works from
what it already knows about the piece. And my third prompt, which asked
for manual curation tools, mood boards, and style tagging across the
whole Sheet, died on "Quota exceeded". Two days later I picked the work
back up in Antigravity, and the questions CuratorMD raised shaped what
came next: send the actual images, run all 800, and cache every result.
CuratorMD is still open in AI Studio, stuck at that quota error.

## The analysis pipeline

**The brief.** With the corpus enriched, I asked for the images and
metadata to be batch-loaded through a multimodal analysis that would
describe and critique each piece, and asked for a higher-reasoning advisor
agent to plan it and propose "board members". That advisor session is in
the Antigravity history for 2026-09-04.

**The advisory board.** The advisor proposed five personas, each reading
the work from a different angle:

| Persona | Became Angle | What it looks at |
|---|---|---|
| The Formalist (curator, art historian) | 1. Composition & Lineage | geometry, focal flow, balance, historical lineage |
| The Industrial & UX Designer | 2. Utility & Ergonomics | affordances and structural rules if the work were an interface, product or space |
| The Cultural Semiotician | 3. Visual Language & Semiotics | symbols, narrative, emotional valence |
| The Spatial Materialist | 4. Light, Space & Materiality | light and shadow, negative space, depth, surface |
| The Colorist & Typographer | 5. Color & Typography | palette (as hex), contrast, temperature, letterform weight |

**From five personas to one call.** The advisor recommended prompting the
model to adopt the personas as lenses. What shipped is one Gemini call per
image, with a system prompt naming the five Angles and a strict JSON
response schema with seven parts: one object per Angle, plus a
three-sentence `precept_critique` and three to five `design_heuristics`.
The schema is what keeps the perspectives separate; the prompt also bans a
list of art-critic clichés by name.

**Platform and batch versus live.** Before running anything at scale I
had the pipeline compared against a pure GCP build and a Cloudflare Workers
AI build, weighing model quality and speed to try it over cost. After a
three-image pilot on 2.5 Flash, agy priced the Gemini Batch API (a flat 50%
discount) against live calls and offered three options: live parallel
Flash, batch Flash, or batch Pro. I picked live Flash, and asked for the
2.5 Pro batch requirements and a survey of other vision models to be
written up anyway. That write-up is
`docs/process/batch_and_vision_models_guide.md`. No batch job ran. The
estimates in that exchange ($0.30 live, $0.15 batch for Flash) had the same
pricing error as the audit below.

**The run.** `pipeline/run_full_vision_pipeline.py`, 2026-09-04, 12:38 to
13:04 UTC. Three items were done first as a pilot, then the remaining 797
ran through ten concurrent workers (`asyncio` with a semaphore of 10),
each result cached to SQLite so a crash wouldn't lose work. 800 of 801
items processed, every result passed the schema, median latency about 19
seconds per image. Outputs: `data/favorites_analyzed.json`/`.tsv` and the
catalogue notes.

**The audit, and what it got wrong.** A separate Gemini session then wrote
`docs/process/telemetry_audit_report.md`, reconstructing the run from the
cache database and log. The timings and schema checks hold up. The cost
doesn't: it priced 2.5 Flash at a small fraction of its actual list rate
and arrived at $0.077. Its per-token rates appear to be Gemini 1.5
Flash's old per-1,000-character prices applied to 2.5 Flash tokens. At
Google's published 2.5 Flash rates ($0.30 per million tokens in, $2.50 per
million out, thinking tokens included), the audit's own counts (about 1.52M
in, 648K out) come to roughly **$2.08**. That's a floor: the script set no
thinking budget, and thinking tokens bill as output but don't appear in the
JSON the audit measured. The report is kept as written with a correction
note at the top.

## What I've learned so far

The costliest mistake so far was a script that updated the live Sheet in
place: it renamed the primary tab and wiped the image preview formulas. The
fix restored the sheet from a prior Drive revision (pull request #2 in the
original, now archived repo). The review that followed found the fix had
been verified and reported, but the pull request was left unmerged while
planning for the next phase had already started from a branch that hadn't
landed on `main`. Both incidents, with root cause and correction, are
written up in `docs/process/engineering_learnings_and_governance.md`.

The rule that came out of the first incident: no script touches an existing
dataset or sheet tab in place, only additive new files or new tabs. It's
enforced by convention in `GEMINI.md`, not by code. For a solo project at
this size I judged code-level enforcement not worth the friction.

The ADR is the clearest example of a pattern that keeps recurring: a
document marked `ACCEPTED` before the review meant to accept it had
happened. `GEMINI.md` now has a standing rule that status fields track
reality, not aspiration.

The telemetry audit is the same pattern in a different place. It calls
itself "independently verified" and "cryptographically validated", it was
written by the same family of model that did the run, and its headline
cost figure is off by more than twenty-five times. Confident formatting
isn't verification. I've found the fix is dull: numbers that matter get
checked against a primary source, here the provider's price list and the
billing report, before they're repeated.

## How it's built

The per-artwork analysis in `catalogue/` (the precept critique, the design
heuristics, the 5 Angles) was generated by the Gemini API from each image.
It isn't hand-written. I wrote the brief, chose the approach, and reviewed
the output, but the words in each note are the model's. Where I disagree
with an analysis I add to the note's own user-override section rather than
edit the generated text, so the record of what the model produced stays
intact.

The pipeline was built mainly in Google Antigravity with Gemini, with side
trips into other agents and models to compare approaches. Four
reviews and audits are archived in `docs/reviews/`, unedited, including
the ones that pushed back: Claude Opus 4.6 reviewed the Phase 2 plan
critically, then separately ran a self-audit against the governing
documents after Phase 2a; Grok 4.6 reviewed ADR 001 and recommended against
accepting it as written; Gemini 3.8 Flash wrote the telemetry audit, which
makes it closer to a self-check than an independent review. Each archived
copy notes the model that wrote it.

The scripts in `pipeline/`
only ever lived in Antigravity scratch directories until I recovered them
for going public on 2026-09-24. Paths are now
repo-relative via `pipeline/paths.py`; private IDs come from environment
variables. Some scripts are historical (the MHTML parser, the Windows-only
Drive mirror steps) and are kept for the record rather than for reuse.
`pipeline/README.md` says which.

## Repo map

```
apps/curatormd/     the first attempt: a Google AI Studio app (2026-09-02)
catalogue/          801 markdown notes, one per artwork
clusters/           cluster manifest and a 2D latent map (Phase 5)
data/               favourites at each stage (raw, enriched, analysed, clustered)
docs/
  decisions/        ADRs (001, latent clustering, still PROPOSED)
  reviews/          gate reviews, archived with the reviewing model attributed
  process/          plans, learnings, the model comparison, the telemetry audit
  journal/          dated dev-log entries, the long form of the log below
pipeline/           the scripts behind each phase
GEMINI.md           standing workspace rules
.agents/            the self-audit skill
```

## Data and rights

The 801 artworks are third-party, held by museums and partner institutions
and shown via Google Arts & Culture. No image is stored or redistributed
here; they were removed from the repo and its history before it went
public. Each catalogue note links to its GAC source page instead.

`curatorial_description` and the other museum-supplied metadata in `data/`
remain the copyright of the partner institutions that supplied them via
Google Arts & Culture. They're kept with each row's `credit_line` and
`link`, for reference and citation.

My own writing, and the AI-generated critiques and heuristics in
`catalogue/`, are licensed CC BY 4.0; see `LICENSE-content.md`. Code is
MIT; see `LICENSE`.

## Links

- [The master Google Sheet](https://docs.google.com/spreadsheets/d/1Tznbdor6-JFLkGNtuN5StasMSopnLkhdqzgbq7NWdAU/edit) (view-only)
- [Journal](docs/journal/)

## Changes and decisions log

Newest first, one or two sentences each. The longer write-ups live in
`docs/journal/`.

- **2026-09-24, going public**: recovered the pipeline scripts from
  Antigravity scratch and committed them for the first time. Dropped the
  images for copyright, flattened the layout by role, rewrote history to
  remove private Drive folder IDs and my personal email, shared the Sheet
  view-only, and kept museum text with credit. Retracing the analysis for
  these docs also corrected the telemetry audit's cost, $0.077 to at least
  $2.08.
- **2026-09-05, renamed to art-precepts-design**: recreated the repo
  without its AI Studio template lineage and renamed it from
  `art-to-design`. The old repo was kept as an archive.
- **2026-09-05, Phase 5 clustering and ADR 001**: k-means over a 59-dim
  feature vector produced 10 clusters, a change from the UMAP/HDBSCAN
  approach in the plan. ADR 001 stays `PROPOSED`; Grok's review found it
  overstated its validation.
- **2026-09-04, Google Sheet restore**: an automated export overwrote the
  primary tab in place and dropped the image previews. Restored from a
  Drive revision, and the non-destructive rule written into `GEMINI.md`.
- **2026-09-04, telemetry audit**: a Gemini session reconstructed the
  vision run from its cache and log. Timings and schema checks sound; the
  cost figure later turned out wrong.
- **2026-09-04, the vision run**: 800 images through Gemini 2.5 Flash on
  Vertex AI in about 25 minutes, ten at a time, every result schema-valid.
- **2026-09-04, live over batch**: after a three-image pilot, chose live
  parallel 2.5 Flash over batch Flash or batch Pro, and had the 2.5 Pro
  batch requirements documented for later.
- **2026-09-04, platform comparison**: compared the local Python and
  Gemini pipeline with a pure GCP build and a Cloudflare Workers AI build.
  Stayed local-first for model quality and speed to try it.
- **2026-09-04, five perspectives, one call**: an advisor agent proposed a
  five-persona board (Formalist, UX Designer, Semiotician, Spatial
  Materialist, Colorist & Typographer). The personas became the 5 Angles
  of a single structured prompt per image.
- **2026-09-04, vocabulary change**: replaced "genome" with "design
  precepts" across the plan and docs, and banned a list of art-critic
  clichés.
- **2026-09-04, first commit**: the favourites dataset, 800 preview
  images, and Draft Plan 1 committed to `art-to-design`.
- **2026-09-02, CuratorMD**: built an AI Studio app that read the Sheet
  and ran three Gemini stages (artwork analysis, curation, `design.md`).
  Its analysis worked from titles, not images, and the next prompt hit the
  quota. The repo was created from its AI Studio template that night.
- **2026-08-30 to 31, extraction**: 801 favourites scraped from GAC into a
  new Google Sheet, and 800 preview images downloaded.
