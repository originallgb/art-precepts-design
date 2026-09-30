# Art Precepts visual retrieval: handoff review

Date: 30 September 2026. Status: research proposal; no retrieval system evaluated.
Branch: `codex/art-precepts-handoff-research`.
Baseline: public `main`, commit `49545dbe5b3ac20128ca04e3431f8461b83173b0`.
request_feedback: true

## Decision

Investigate whether a small visual retrieval experiment helps select references
for design precepts. Grant selected **composition and spatial structure** as
the first retrieval distinction on 30 September. Start with the existing
collection and compare a simple metadata/contact-sheet baseline against one
image/text embedding candidate. A model, package and success threshold have
not been selected. Style transfer is outside this first experiment.

This branch reviews the recovered request and prepares the experiment. It
does not claim to have implemented or validated image retrieval.

## Recovered request and source selection

The personal Drive folder named `2026-09-27 Research Context and Handoffs`
contains the Art Precepts handoff, an overview reviewed on 29 September,
a critical review, and a private evidence snapshot. Two Download copies of
the Art Precepts handoff are identical to each other but differ from this
reviewed version. The reviewed version is the basis for this review because
it restores the exact intent evidence, project discovery lead, source links
and limits on inference described by the critical review.

The reviewed handoff connects the project explicitly to Simon Willison's
[llm-clip article](https://simonwillison.net/2023/Sep/12/llm-clip-and-chat/).
It treats the association with AesFA as a hypothesis, not a decision to
transform images. It asks for real project tasks, a simple comparison,
preserved provenance, inspectable failures and direct creative judgment.

Private source copies, Drive metadata and SHA-256 fingerprints were retained
outside this public checkout. Private browsing history, account identifiers
and evidence URLs have not been copied into this report. The source record
can be retrieved through the named personal Drive folder. The source reports
the original Reader annotation; that Reader record was not independently
re-fetched during this review.

## Fit with the actual project

| Evidence | Implication for this research |
|---|---|
| [README](../../README.md) aims for design playbooks grounded in collected works | Retrieval is a way to find useful references, not the project outcome itself |
| [Journal](../journal/README.md) calls for one note taken through a design example | Connect any successful retrieval to a concrete design choice and comparison |
| `data/favorites.json`, `favorites_analyzed.json`, and `favorites_clustered.json` each contain 801 records in the reviewed baseline | Reuse stable `asset_id` values; do not create a disconnected collection |
| [ADR 001](../decisions/001-latent-clustering-methodology.md) remains PROPOSED; clustering uses generated text and artist/title fields | Existing clusters are candidate browsing aids, not relevance ground truth |
| [Pipeline notes](../../pipeline/README.md) document removal of artwork images | Metadata is available; an image retrieval experiment needs a separately available private image sample |
| [Workspace rules](../../GEMINI.md) require additive work and PRs | Preserve datasets and catalogue notes; do not write research results into them |

The historical archive discovery lead was confirmed accessible and private
through repository metadata. Its contents were not imported. The current
public brief and corpus provide sufficient context for this review; older
private Git history must not be merged into this branch.

## Proposed evaluation tasks

These are test candidates derived from generated catalogue observations,
not claims that the art has been personally judged to satisfy them. The
selected focus is user-confirmed; the individual queries and relevance
labels still need visual judgment.

| Task and query | Real seed | Relevant distinction | Deliberate failure case |
|---|---|---|---|
| Find a dominant foreground form against a repeating background | Botero, *Arcángel*, `NgHYVFO9OGwDSA` | Foreground hierarchy and background repetition across subjects | Another angel without that arrangement |
| Find overlapping flat shapes that imply shallow depth | Popova, *Composition*, `UgEKpgTnRQeJkw` | Occlusion, spatial ordering and useful negative space | Similar colours with no overlap |
| Find an off-centre focal mass balanced by a smaller complex form | Kandinsky, *Composition*, `2AGLIiSAmxZHGg` | Asymmetric visual weight and directed attention | Same artist but a different spatial structure |
| Find a central anchor interrupted by directional lines | Rodchenko, *Composition*, `oAE5NZNpXb7aOg` | Focal anchor and directional relationships | A similar circular subject with unrelated structure |

Source observations are in [analysed data](../../data/favorites_analyzed.json),
keyed by the listed IDs. The Botero example is also linked from the README.
For image-to-image queries, exclude the seed image from scored results.

## Smallest useful experiment

1. Build a private, additive sample manifest from existing assets. Choose
   seeds and hard negatives across different subjects. Sample size should
   follow available images and review effort, not a claim of statistical power.
2. Compare the same sample under three conditions: manual contact sheet;
   transparent tag/field filtering; and one image/text retrieval candidate.
   Label tags and descriptions as generated where applicable. Do not compare
   a curated baseline with a different embedding corpus.
3. Save each exact query and ranked result list. A review surface should show
   asset identity, image, source, rank, score type, and separate human
   relevance notes. Generated descriptions are candidate evidence to inspect,
   never proof of why a vector model assigned a rank.
4. Have Grant mark useful references, important misses and plausible false
   positives. Record time to first useful reference and top-k relevance using
   a fixed k chosen before evaluation. Alternate condition order to reduce
   familiarity effects. An unjudged result is unjudged, not irrelevant.
5. Use one accepted reference in a small interface or spatial design study.
   Record the original design, the change, the intended benefit and whether
   the comparison supports that benefit. Retrieval relevance alone does not
   validate a design precept.

The retrieval candidate must improve the chosen task enough to justify its
setup and review effort. If it mostly retrieves subject matter or artist
identity, retain the simpler baseline or revise the representation. No
adoption decision follows from similarity scores alone.

## Proposed artifact contract

All image paths and image-derived outputs stay in a private experiment
directory until their publication scope is deliberately reviewed.

| Artifact | Required contents |
|---|---|
| Sample manifest | Asset ID; private image locator; image hash; source; rights/access note; inclusion reason |
| Run manifest | Model and checkpoint revision; package versions; image preprocessing; embedding dimension and normalisation; distance metric; corpus hash; run timestamp |
| Query/result record | Query ID; exact text or seed asset; requested visual property; candidate set; ordered asset IDs; scores; explicit score semantics |
| Human judgment | Query/result identity; useful/not useful/unjudged; visual-property reason; important misses; evaluator; time recorded |
| Review output | Same queries under each condition; ranked examples; false positives; unresolved disagreements; next decision |

Do not substitute generated critique embeddings for image embeddings and
call the result visual retrieval. That would repeat the original app's
metadata-versus-image problem in a different form.

## Boundaries and remaining input

No model installation, transformation, deployment, dataset mutation or remote
publication was part of this request review. The public checkout has no
`images/` directory. A private Drive File Stream location was supplied by Grant
and inspected separately; it must not be copied wholesale into the public tree.

The private `images` and `images (1)` directories each enumerate 800 JPEGs.
Filename suffix matching maps 800 distinct catalogue IDs with no ambiguous
matches in either directory. The unmatched record is `xQEoZI5yehd96g`,
*Welcome to Mapperton House & Gardens!*. All four proposed seed works are
present by filename. The two directories have not been compared byte-for-byte.
The initially delayed sample read subsequently completed: all four seed files
were read in full, checked for JPEG signatures and SHA-256 hashed. This verifies
byte access for those seeds, not full-corpus hydration or visual decoding.
The private source location is recorded outside the public tree.

The remaining implementation steps are to select a reproducible retrieval
candidate, expand and decode the sample, and implement the comparison.
No further source-location request is needed. The experiment can remain
entirely local/private without changing the public image policy.

## Handoff disposition

| Requested outcome | This review delivers | Remaining work |
|---|---|---|
| Recover project and intent | Current brief, corpus, methodology status and user-selected focus | Individual relevance labels |
| Primary-source recommendation | [Visual retrieval source review](2026-09-30-visual-retrieval-source-review.md) | Runtime compatibility and candidate selection |
| Representative tasks | Four corpus-grounded query candidates and confounders | Grant's visual judgments |
| Working sample and visual comparison | Implementation contract and evaluation design | Expanded sample, implementation and measured runs |
| Concrete next decision | Test retrieval for composition/spatial structure before considering transformation | Choose the retrieval candidate and sample |

This is a completed request review, not completion of the handoff's future
prototype and evaluation work.

## Verification and self-audit

### A. Automated checks

| Check | Result |
|---|---|
| Local links in the two new reports | 17 checked, zero missing targets; no local fragment links |
| Privacy scanner on both reports and review index | No findings |
| Git whitespace check | Passed |
| Data, catalogue and pipeline tracked diff | Empty |
| Prescribed `scripts/validate-doc-links.py` | Absent; focused link check substituted |
| Seed image bytes | Four readable JPEG signatures and private SHA-256 records |

### B. Requirements

The handoff disposition table above distinguishes delivered review work from
unperformed prototype work. Personal identity was selected through
`google-identity`; `gws` passed the health gate and was used at Grant's request.
Composition and spatial structure supersede the provisional focus. The later
image-source correction is incorporated in the inventory and next steps.

### C. Honest limitations

No image decoding, embeddings, ranked-result comparison, relevance judgment
or usefulness measurement was performed. The image directories were not
deduplicated. The original Reader annotation was not independently retrieved.
No GitHub issue comment was posted: this request authorised a local research
review, not external communication. Private evidence remains outside Git.

### D. Disposition

Request review: delivered. Privacy and focused link checks: passed. Required
repository link-validator script: unavailable. Prototype/evaluation: not run.
No image data or private source records are included in this branch.
