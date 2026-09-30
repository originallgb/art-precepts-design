# Art Precepts: two exploratory research threads

Date: 30 September 2026. Status: corrected research brief; no technology or
implementation selected. request_feedback: true

## Correction and authority

This note supersedes the intent, scope and sequencing conclusions in the
[earlier handoff review](2026-09-30-art-precepts-handoff-review.md) and
[earlier source review](2026-09-30-visual-retrieval-source-review.md).
Those reports remain byte-for-byte unchanged as the record of the initial
interpretation. This correction is additive. Their source observations and
image inventory can still be useful; their retrieval
experiment is an optional proposal, not the governing research brief.

The correction comes directly from Grant's subsequent clarification in this
conversation. It takes precedence over the consolidated Drive handoff and
the assistant's interpretation of browsing evidence.

Grant was considering **two distinct, tangentially related ideas** for Art
Precepts. He does not yet know fully what the methods do, how they might be
incorporated, or whether they are suitable. Both are legitimate interests
to explore. Either or both could prove wrong for the project.

## Thread A: Image Toolbox and model capabilities

**Origin of interest:** Grant encountered AesFA through the Android FOSS app
Image Toolbox. While trying to understand the different models available,
he realised some of those models might have utility for Art Precepts.

**Research question:** What do those models actually do, what goes in and
comes out, how do they differ, and could any capability help this project?

Begin with a plain explanation of the app's relevant capabilities and the
models behind them. Distinguish the app, model architecture, trained weights
and any preset; similar names do not establish equivalent capabilities.
Establish the installed app version and model names only if needed to match
the exact options Grant saw. Do not infer them from current upstream docs.

AesFA's published task is neural style transfer: producing a stylised image
from content and style references. That describes its documented function;
it does not determine which use, if any, Grant wants for Art Precepts.
See the [AesFA paper](https://arxiv.org/abs/2312.05928v3) and the
[Image Toolbox source context](2026-09-30-image-toolbox-model-context.md).

Possible project uses should emerge from understanding the capabilities.
They may include creative experimentation or transformations, or none may
be worthwhile. There is no dependency on first completing an image-search
experiment. No transformation workflow has been selected.

## Thread B: embeddings as part of the pipeline

**Origin of interest:** Simon Willison's llm-clip example looked like a way to
embed data as part of the Art Precepts pipeline.

**Research question:** What does an embedding add to this pipeline, which
data might be represented, what useful operations become possible, and what
information or distinctions might be lost?

An embedding is a numerical representation produced by a model. The model
and input determine which similarities those numbers capture. In the
[llm-clip example](https://simonwillison.net/2023/Sep/12/llm-clip-and-chat/),
images and text can be represented in a compatible space, and similarity
search demonstrates one use. The pipeline interest is broader than building
a search interface or adopting that exact package.

Investigate image, text and compatible cross-modal representations as
separate possibilities. Search, neighbour comparison, grouping or exploratory
maps are candidate uses, not agreed requirements. Compare any proposal with
the pipeline's existing palette, categorical and TF-IDF/SVD features in
[ADR 001](../decisions/001-latent-clustering-methodology.md) and the
[clustering implementation](../../pipeline/generate_phase2a_clustering.py).

Embedding generated critiques could be a valid text experiment, provided it
is labelled as such. It cannot establish what a model learned directly from
image pixels. Likewise, proximity between image embeddings does not by
itself establish a useful aesthetic relationship or design rule.

## What changes from the first review

| Earlier interpretation | Corrected treatment |
|---|---|
| One retrieval project with style transfer deferred | Two independent research threads with open outcomes |
| AesFA's connection was only inferred from nearby browsing | Grant explicitly confirmed the interest and its Image Toolbox origin |
| llm-clip implied a visual retrieval product | It suggested embedding data within the existing pipeline; retrieval is one example |
| Composition and spatial structure defined the whole branch | Grant chose that answer within an assistant-proposed retrieval question; retain it as a useful preference for a possible comparison, not a decision to narrow both threads |
| The next action was to select a retrieval model and implement | First explain capabilities, inputs, outputs, limits and possible project fit in each thread |
| A prototype was the inevitable next deliverable | A small trial becomes useful once there is a question it can answer; rejecting a poor fit is also a valid outcome |

## Research approach

For each thread, produce an understandable capability note with:

1. The question or curiosity that prompted it, in Grant's terms.
2. What each method takes as input and produces as output, with an example.
3. What it can plausibly help with, what evidence supports that, and what it
   cannot establish.
4. Potential connections to Art Precepts, clearly marked as hypotheses.
5. The smallest demonstration or comparison that would resolve a useful
   uncertainty, if a demonstration is warranted.
6. A conclusion that may be pursue, investigate further, or set aside.

Keep the two findings independently understandable. Combine them only if
later evidence reveals a useful relationship. Neither research thread has
priority or an implementation deadline imposed by this correction.

## Existing project evidence to reuse

The [project brief](../../README.md), catalogue, generated analysis and
provisional clustering remain the starting context. The private image source
has already been located: two directories each listed 800 filenames matching
catalogue IDs, and four seed images were read and hashed. This supports the
feasibility of later private examples; it does not demonstrate model utility.

Preserve source identity, input modality, model/version, processing settings
and outputs in any later experiment. Keep originals intact. Existing privacy
and publication boundaries remain in force. No image, model, private source
record or pipeline implementation is introduced by this correction.

## Verification and limits

The governing evidence for intent is Grant's clarification, not a technical
paper or inferred browsing sequence. The source review can establish what a
method does; it cannot decide Grant's intended use. The exact Image Toolbox
version and options he encountered remain unspecified.

The correction is complete when an appended review-index entry points here,
both interests are represented without an imposed priority, and the research
branch preserves both original reports byte-for-byte while directing future
work to this brief. Model suitability and project benefit remain unevaluated.

### Preservation and requirement checks

| Requirement | Evidence | Result |
|---|---|---|
| Preserve previous reports | Exact byte comparison with commit `9bb6e56` for both original reports | Passed |
| Preserve previous index content | Original index is an unchanged prefix; correction section appended | Passed |
| Capture both interests and uncertainty | Separate threads above, no imposed priority, no adopted model or product | Passed against Grant's clarification |
| Keep project data intact | Changes limited to new research notes and the index addition | Passed |
| Validate local references | 15 local Markdown links across new notes and index resolve | Passed; repository link-validator script remains absent |
| Check privacy and whitespace | Repository privacy scanner on changed/new files; Git diff check | Passed |

No model performance or creative benefit has been tested. The new Image
Toolbox context cites a source revision; it does not establish the version
or models installed on Grant's phone.
