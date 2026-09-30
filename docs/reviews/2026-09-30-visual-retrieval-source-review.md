# Visual retrieval: source review and bounded experiment

Date: 2026-09-30. Status: research recommendation, not an accepted implementation decision.

## Recommendation

Test whether retrieving references helps turn the collection into usable design precepts. Grant has selected **composition and spatial structure** as the first experiment's criterion: seek formal similarities across different subjects and include counterexamples with similar subjects but different arrangements. Palette and texture are secondary. Begin with catalogue tags and a contact-sheet baseline, then compare one small image/text retrieval index on the same permitted sample. Keep the embedding model **unselected** until compatibility, asset availability and relevance can be checked. Defer style transfer: transforming an image is a different task from finding evidence for a design choice.

This is a source review of the recovered research request. No model was installed, no weights were downloaded, no retrieval run was performed, and no aesthetic usefulness has been demonstrated. Public primary sources were inspected on the review date; their moving main-branch URLs are inspection references, not pinned experiment dependencies.

## Project fit and evidence limits

The [current brief](../../README.md) aims to produce `design.md` playbooks for interfaces, interiors and a broader design language from personally selected works. The [original guide](../process/curatormd_original_brief.md) connects non-obvious curatorial collections to those playbooks. Search is useful only if it helps select and compare references for that work.

The existing clustering implementation combines palette/categorical attributes with TF-IDF/SVD features built from titles, creators and generated analysis. It is not a direct image-embedding retrieval index. [ADR 001](../decisions/001-latent-clustering-methodology.md) remains PROPOSED; its correction note and the README caution against treating the groups as established aesthetic relationships. See the actual [feature construction](../../pipeline/generate_phase2a_clustering.py). Existing generated labels are candidate filters and hypotheses, not human relevance ground truth.

The research handoff establishes a direct project connection for the llm-clip inspiration. It does not establish AesFA as a project requirement. Its archive repository reference is a discovery lead, not proof of archive contents or authority over this checkout. Nearby creative interests do not establish additional project scope. Private source identifiers and personal activity details are deliberately absent from this public-facing review.

The repository [excludes artwork images](../../README.md), and its [pipeline notes](../../pipeline/README.md) describe historical image paths and machine dependencies. Catalogue notes alone support query design, but cannot establish visually judged retrieval quality. Grant subsequently identified the private Drive File Stream source. The coordinator found 800 JPEG filenames mapping uniquely to catalogue IDs in each of two image directories, including the proposed seed works. All four selected seed files were then read and hashed successfully; complete corpus hydration has not been checked. See the [handoff review](2026-09-30-art-precepts-handoff-review.md) for source availability and the distinction between file listing and confirmed byte access.

## What the primary sources establish

| Source | Observed capability | Consequence for this project |
|---|---|---|
| [Willison's September 2023 article](https://simonwillison.net/2023/Sep/12/llm-clip-and-chat/) | Demonstrates image embeddings stored in SQLite and text queries returning ranked IDs and scores. | Useful original inspiration and a compact architecture, not evidence of current model superiority. |
| [Current llm-clip code](https://raw.githubusercontent.com/simonw/llm-clip/main/llm_clip.py) and [package metadata](https://raw.githubusercontent.com/simonw/llm-clip/main/pyproject.toml) | Registers text and binary-image support; lazily creates `SentenceTransformer("clip-ViT-B-32")`; opens image bytes through PIL and calls `encode`. Metadata declares version `0.1`, `llm>=0.10` and `sentence-transformers`. | The inspected wrapper hardcodes its model and has no model-revision option. Pinning the package alone would not record all model/preprocessing provenance. Local dependency compatibility and runtime remain untested. |
| [LLM embedding CLI documentation](https://llm.datasette.io/en/stable/embeddings/cli.html) | Collections associate unique IDs with embeddings from one model; SQLite can be placed in a separate database. | A disposable local index can remain separate from catalogue data and the master Sheet. Record revisions and preprocessing in an additional manifest. |
| [AesFA paper, version 3](https://arxiv.org/abs/2312.05928v3) | Proposes frequency decomposition and contrastive training for neural style transfer. | Its task is stylization. It does not validate semantic retrieval or design-precept extraction for this corpus. |
| [AesFA project page](https://aesfa-nst.github.io/AesFA/) | Separates fine textures/brushstrokes from broader structures/tones; reports limitations including excessive patterns and line artifacts. | Useful vocabulary for independent visual judgments, not a reason to add transformation to this experiment. |
| [AesFA repository](https://github.com/Sooyyoungg/AesFA) and [test implementation](https://raw.githubusercontent.com/Sooyyoungg/AesFA/main/test.py) | Documents Python 3.7/PyTorch 1.13.1 and checkpoint-based testing. The test path loads content/style images, resizes and center-crops, runs the model, and saves stylized files. | Even the supplied demo requires distinct inputs, dependencies and output review. It is not a drop-in retrieval tool. No local execution or performance claim follows from inspection. |

## Comparison to run, not results

| Approach | Smallest useful form | Failure to inspect |
|---|---|---|
| Tags and contact sheet | Filter existing catalogue fields and text, then inspect permitted thumbnails with source IDs and links. Keep generated labels visibly separate from Grant's judgments. | Vocabulary matches can reflect repeated model prose; useful unlabelled relationships may be missed. |
| Image/text retrieval | Embed the same images once; compare short text queries and selected image queries against the stored vectors. Export ranked IDs and scores to the same review surface. | Subject, artist or medium similarity may dominate the requested composition, palette, texture or conceptual relation. |

Neither approach establishes a design rule. A useful match becomes a candidate for an applied design example, followed by judgment of whether that example works.

## Representative tasks from actual catalogue records

These are proposed queries grounded in generated notes, not completed visual assessments. Composition and spatial structure are the selected criterion; the other dimensions distinguish controls and possible confounds. Grant should judge useful references before their labels are used for evaluation.

| Dimension | Proposed task and anchor | Deliberate failure case |
|---|---|---|
| Subject matter | Find angel imagery using [Arcángel](../../catalogue/0100_arc-ngel_NgHYVFO9OGwDSA.md) as a simple control. | Treating success on angels as success on visual hierarchy. |
| Composition | Find a dominant foreground form against a repeating background, starting with the Arcángel note. | Same subject with no matching foreground/background relationship. |
| Palette | Find warm, muted references, starting with the [Buddhist Map](../../catalogue/0771_buddhist-map-of-the-world-outline-map-of-all-count_pQHZVGGNlR3gLg.md) note. | Similar map subject with an unsuitable palette; generated colour labels mistaken for measured pixels. |
| Texture | Compare visible paper/mark texture using the map and [Worktable](../../catalogue/0407_worktable_QgGF20uJIwXlLg.md) notes. | Text matching the medium while the thumbnail does not show the texture at useful resolution. |
| Style | Find systematic technical drawing references around Worktable. | Artist-name proximity mistaken for the visual convention being sought. |
| Conceptual precept | Compare a central anchor with dense annotations against systematic multi-view layout for an information interface. | “Information architecture” language matching without a visible arrangement that supports the proposed use. |

## Reversible experiment contract

Proposed initial scope: a deliberately varied sample of 30–50 permitted images and six queries centred on composition and spatial structure: foreground/background hierarchy, central anchoring, density, layering, directional flow and systematic multi-view layout. These are experiment sizes, not measured results or an adequacy guarantee. Include same-subject/different-structure and different-subject/same-structure examples; do not sample only from existing cluster winners. Use palette/texture observations to identify confounds rather than redefine success.

1. Create an additive sample manifest: asset ID, source URL, permitted local file reference, image hash, dimensions, provenance/usage basis and inclusion reason. Keep private paths and images outside public outputs. Preserve originals.
2. Build the baseline and one retrieval candidate over exactly that manifest. Record package and model revisions, preprocessing/crop policy, vector normalization, similarity function, environment and index hash. Do not infer model settings from the generic alias `clip`.
3. Use one review surface with query, ordered thumbnails, asset IDs, source links and scores where relevant. Record false positives and useful references missing from the top results. Separate human comments from model-generated descriptions. Scores and captions are not causal explanations of ranking.
4. Capture useful matches among the first five results, time to find a usable reference, important misses and the property that made each judgment relevant. Compare both approaches under the same query and image set. Repeated timing can be affected by familiarity; alternate method order and report that limitation.
5. Have Grant review a small contrasting set and take a chosen reference into one design-precept example. Retain retrieval only if it improves the creative task enough to justify the additional setup. If tags/contact sheets suffice, stop there. Set any numerical success threshold with Grant before treating the trial as an acceptance test.

The next decision is to select a reproducible candidate and expand the readable seed sample from the identified private source for the selected composition/spatial-structure criterion. That enables a bounded baseline-versus-retrieval trial; it does not authorize rewriting clusters, running historical Sheet writers, acquiring new images, or building a style-transfer application.
