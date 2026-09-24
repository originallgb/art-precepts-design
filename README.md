# Design precepts from 801 favourites

A personal catalogue of 801 Google Arts & Culture favourites, run through a
Gemini vision pipeline that reads each image from five design perspectives,
then clustered into aesthetic families. The end goal is a set of `design.md`
playbooks I can use to make real design decisions. Built in the open,
mistakes included.

## Why in public

I wanted to learn agentic AI development on a project with no commercial
pressure, so I could get the failure modes wrong safely and write them down.
This repo is that log. `GEMINI.md` is the rule set I wrote for the workspace
after the first Google Sheet got overwritten in place, and
`docs/process/engineering_learnings_and_governance.md` documents why.
`.agents/skills/self-audit/` is the check that's meant to run before any
phase gets called done.

## Where it stands

Using the phase numbering from the original plan:

- **Phase 0, extraction**: 801 favourites pulled from a saved GAC page,
  parsed, and pushed to a Google Sheet. Done, 2026-09-04.
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

## The analysis pipeline

This is the core of the project, so it gets its own section.

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

**From five agents to one call.** The advisor's own recommendation was to
prompt a single model to adopt all five lenses rather than run five
separate agents per image, and that's what shipped. Each image gets one
Gemini call with a system prompt naming the five Angles and a strict JSON
response schema with seven parts: one object per Angle, plus a
three-sentence `precept_critique` and three to five `design_heuristics`.
The schema is what keeps the perspectives separate; the prompt also bans a
list of art-critic clichés by name.

**Batch versus live.** Before running, I costed the Gemini Batch API (a
flat 50% discount, results within 24 hours) against live calls, and
compared Gemini 2.5 Pro and Flash with other vision models. The comparison
is `docs/process/batch_and_vision_models_guide.md`. At this scale the
absolute cost was small either way, so I took live calls on 2.5 Flash for
the speed and the ability to watch it run. No batch job was ever
submitted.

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
and arrived at $0.077. Using the audit's own token counts (about 1.52M in,
648K out) at the list prices I understand to apply ($0.30 per million in,
$2.50 per million out), the run cost roughly **$2**, more if thinking
tokens were billed. The report is kept as written with a correction note
at the top. The lesson I take from it is in the next section.

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
cost figure is off by more than twenty times. Confident formatting is not
verification. Numbers that matter get checked against a primary source,
here the provider's price list, before they're repeated.

## How it's built

The per-artwork analysis in `catalogue/` (the precept critique, the design
heuristics, the 5 Angles) was generated by the Gemini API from each image.
It isn't hand-written. I wrote the brief, chose the approach, and reviewed
the output, but the words in each note are the model's. Where I disagree
with an analysis I add to the note's own user-override section rather than
edit the generated text, so the record of what the model produced stays
intact.

The pipeline was built mainly in Google Antigravity with Gemini. Four
reviews and audits are archived in `docs/reviews/`, unedited, including
the ones that pushed back: Claude Opus 4.6 reviewed the Phase 2 plan
critically, then separately ran a self-audit against the governing
documents after Phase 2a; Grok 4.6 reviewed ADR 001 and recommended against
accepting it as written; Gemini 3.8 Flash wrote the telemetry audit, which
makes it closer to a self-check than an independent review. Each archived
copy notes the model that wrote it.

The scripts in `pipeline/` only ever lived in Antigravity scratch
directories until I recovered them on 2026-09-24. Paths are now
repo-relative via `pipeline/paths.py`; private IDs come from environment
variables. Some scripts are historical (the MHTML parser, the Windows-only
Drive mirror steps) and are kept for the record rather than for reuse.
`pipeline/README.md` says which.

## Repo map

```
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

- **2026-09-24, going public**: images dropped for copyright, layout
  flattened by role instead of nested under `Google Arts & Culture/`,
  history rewritten to remove the private Drive folder IDs and my personal
  email, the Sheet shared view-only, museum text kept with credit.
- **2026-09-24, cost correction**: rechecked the telemetry audit's $0.077
  against Gemini 2.5 Flash list pricing; the real figure is roughly $2.
  Correction noted on the report rather than editing it.
- **2026-09-24, pipeline recovery**: the extraction, enrichment, vision,
  clustering, recovery and audit scripts, which had only ever lived in
  Antigravity scratch directories, recovered and committed for the first
  time.
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
- **2026-09-04, live calls over batch**: costed the Gemini Batch API
  against live calls and compared vision models. Chose live 2.5 Flash for
  speed and visibility, since the cost difference was small at this scale.
- **2026-09-04, five perspectives, one call**: an advisor agent proposed a
  five-persona board (Formalist, UX Designer, Semiotician, Spatial
  Materialist, Colorist & Typographer). Rather than five agents per image,
  the personas became the 5 Angles of a single structured prompt.
- **2026-09-04, vocabulary change**: replaced "genome" with "design
  precepts" across the plan and docs, and banned a list of art-critic
  clichés.
- **2026-09-04, initial extraction**: 801 favourites pulled from a saved
  GAC page and pushed to a Google Sheet, alongside 800 preview images and
  Draft Plan 1.
