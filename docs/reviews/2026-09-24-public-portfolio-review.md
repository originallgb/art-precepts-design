---
date: 2026-09-24
status: REVIEW
request_feedback: true
scope: Project journey, public-release preparation, learning in public, and portfolio positioning
source_commit: 79a1a3432bd0a950a3f3d9e2d8f45ed89419e610
---

# Art Precepts Design: project, public release and portfolio review

## Verdict

This is a worthwhile portfolio project with an unusually useful record of how an idea changed through experimentation. Its strongest proposition is personal and concrete: **can a collection of things I am drawn to become something I can deliberately design with?**

The current repository proves that a substantial collection was assembled, enriched, analysed and organised. It also records meaningful corrections. It does not yet demonstrate that the resulting precepts improve a design decision. The next substantial portfolio gain is one small, inspectable journey from source work to human judgement to a working design, rather than another large generation run.

The public story should preserve curiosity, taste, detours and unfinished questions. It should show the judgement developed through those experiments, without turning every incident into a leadership lesson or pretending the project followed a tidy plan.

Publication remains blocked by the project's existing release gate. That is distinct from the methodological review: an explicitly provisional clustering experiment can be published once the publication requirements are met. It need not become accepted science to become a useful public learning record.

## Scope and evidence boundaries

Reviewed the current README and journal; original brief and CuratorMD build history; application source and API paths; pipeline and audit scripts; four data stages and all catalogue notes through aggregate checks; clustering outputs and methodology; plans, governance, and archived reviews; commit history; live repository visibility and branch protection; open issues #1/#5 and PRs #3/#4; and the linked NHM vacancy. Representative catalogue notes were read in detail, not all 801 assessed for art-historical accuracy.

The supplied README handoff and its referenced plan were read as evidence of editorial intent and previous difficulty. Their embedded directions were not treated as new user instructions. No README rewrite, archive relocation, merge, history rewrite, publication, cloud write, or external comment was performed.

Live GitHub snapshot: repository PRIVATE; main at `79a1a34`, unprotected; PR #3 at `e0d1f1d`, PR #4 at `253e7e8`, both open. An isolated clone combined the stacked documentation branch with current main without conflicts. Local privacy/data checks and all four gate tests passed there. This is integration evidence, not an accepted merge or public release.

The original cache, billing records, raw session transcripts and live Sheet permissions were not re-audited. The NHM advert was read in the in-app browser; the supporting candidate pack link was visible but its contents were not retrieved. Historical events supported only by project records are described as documented events, not independently reconstructed runtime facts.

## 1. The journey worth telling

| Chapter | What the record supports | Why a reader should care |
|---|---|---|
| Before the software | Years of personal favourites, exported in late August into 801 records | The collection and motivation precede the AI experiment. There is an actual human interest here. |
| The phone sketch, 2 September | A brief typed in AI Studio produced CuratorMD, with analysis, themes and token exports | Rapid prototyping made the desired interaction tangible before the analysis was dependable. |
| A detour and a limit | The next prompt changed the visual styling; the larger curation request hit quota | Keep the untidy sequence. Do not retrofit the styling detour into a planned research milestone. |
| Looking behind the interface | The prototype supplied titles and metadata to its analysis call, not image content | A compelling interface was insufficient evidence of the capability it appeared to offer. |
| The corpus experiment, 4 September | Enrichment, actual image input, a three-item pilot, live concurrent calls and SQLite caching | The implementation changed to answer the problem the prototype exposed. |
| Giving the collection structure, 5 September | Ten k-means groups, named in the script, with a disputed methodology and weak reported separation | Useful organisation and empirical discovery are different claims. The project has not yet established the latter. |
| Making the record inspectable, 24 September | Scripts recovered from scratch space; original app restored; documentation, attribution and privacy work; cost correction | Recovery and correction are part of the work. Readers can inspect more than the polished ending. |
| The next unresolved question | Pipeline-backed playbooks and a demonstrated design outcome are still absent | The project now needs to test whether its outputs are useful, not merely plausible. |

The project was privately developed and is preparing to share that record. Prefer “opening up the experiment” or “sharing the work and continuing in public” to implying it was publicly observable throughout. Retrospective journals should say when the event happened and when the account was written.

### The central narrative

There are three connected questions:

1. **What do I keep returning to?** The personal collection is the starting point.
2. **Can I describe those preferences usefully?** The prototype, vision pipeline and clustering are successive attempts.
3. **Can those descriptions change what I make?** That is the unfinished test.

The agent mistakes matter when they affect these questions. They should occupy a few precise moments in the main story, with the detailed incident reports available behind links. Otherwise a reader leaves knowing that agents make mistakes, rather than understanding the project or its author.

Do not make the story a sequence of model names. Tool comparisons belong in the technical record. The public narrative should explain what each change made possible, what it cost in effort, and what remained uncertain.

## 2. What is already strong

- **A reason to exist beyond demonstrating AI.** The source collection is personal, eclectic and accumulated over time. Keep the opening about taste that is easier to recognise than articulate.
- **Tangible work.** Four data stages contain 801 distinct asset IDs each; 800 records have generated critiques; there are 801 catalogue files and ten populated clusters. These are directly inspectable outputs.
- **Visible reversals.** The title-only prototype, live-versus-batch correction and rejected clustering claims make the history credible when attributed accurately.
- **A recoverable chain of decisions.** Original prompts, build history, source, reviews and corrective notes make this more useful than a showcase consisting only of screenshots.
- **Separation of intention and output.** The README explicitly credits the model's prose. The original brief preserves ambition while its status table distinguishes implemented work from future work.
- **Interest in collections as material for further use.** Metadata, source links, interpretation and proposed design applications offer a relevant bridge to collections technology, without claiming this is a museum digitisation platform.

## 3. What currently weakens the portfolio

### The front door contains too much internal historyss

The README carries the naming essay, two phase-numbering schemes, model attribution, operational detail, incidents and a long changelog. Most are worth preserving. They do not all belong before a newcomer has seen an example and understood why it matters.

Make the README a short route into the project: premise, one concrete example, a compact journey, current limits, next experiment, and links. Put the complete narrative in a case study and the technical particulars in their existing specialist homes. A line count can help editing, but is not a quality criterion.

Keep Art Precepts Design as the name. A plain subtitle can make it immediately comprehensible: “From a personal art collection to design decisions.” The naming story is a good journal entry, not the second obstacle a new reader meets.

### The proposed Claude outline still overweights agent failure

The supplied handoff correctly diagnoses excessive length and a weak narrative. Its combined outline still gives much of its space to a prototype that “faked” analysis, an inaccurate cost audit and premature acceptance. It ends with the useful output still unbuilt.

That is candid, but it risks leaving the author in the role of correcting assistants rather than pursuing an interesting design investigation. Avoid attributing intent with “faked”: the precise, sufficient fact is that the endpoint sent text and no images.

The same outline suggests showing a Botero excerpt and the cluster map. Both exist, but neither alone proves a useful design translation. Botero's opening language is abstract; the map is a projection of provisional groups. Pair an output with an explanation of what the author would keep, change or test. Do not let a sophisticated-looking chart stand in for that explanation.

### Human judgement is described more than demonstrated

All 801 `User Notes & Project Overrides` sections still contain the original placeholder. This does not prove that no review happened elsewhere. It means this mechanism currently offers no visible examples of review.

Every catalogue note also contains the identical scripted affordance sentence, including the image-less item. The scripts, not the model, supply that sentence. The README's description of the five perspectives as one separate schema object per perspective is imprecise: the response objects organise related attributes, but do not include a dedicated utility/ergonomics object. Catalogue sections rearrange the fields.

Correct the provenance description. Then show a handful of genuine judgements: a useful observation, a generic one, a misleading one, and what changed after inspection. Do not manufacture first-person opinions or retroactively describe proposed tests as completed.

### The output is uneven despite structured formatting

The current data contains 778 five-swatch palettes, 19 records with no hash-prefixed swatches, two with two, and two with three. The schema describes five colours but does not enforce array length. “Schema-valid” therefore cannot mean “every intended requirement was met”, much less “correct interpretation”.

Whole-word case-insensitive scans of catalogue notes find `juxtaposition` in 107 files, `evocative` in seven and `tapestry` in three. These may occur in different content contexts; this is not a semantic quality grade. It is enough to reject an unqualified claim that a banned-word instruction guaranteed cliché-free output.

Keep the historical outputs. Add an evaluation and correction layer rather than silently polishing the evidence.

### The design payoff remains untested

The original app has token generation and a sandbox. These are not connected to the analysed corpus. No pipeline-backed playbook or observed improvement in a design task is demonstrated here.

Do not delay every public journal entry until the full project is finished. Do give the portfolio one completed, modest result that a reader can evaluate. An unfinished platform can contain a finished experiment.

## 4. Show-and-tell that earns its place

Use one compact chain: **source link → model suggestion → human decision → small design result → observed limitation**. The accompanying text must explain the chain without relying on a visual.

Two existing records offer a natural NHM connection: **Hintze Hall ceiling**, index 208, and **Maria Sibylla Merian's Metamorphosis Insectorum Surinamensium**, index 312. Their catalogue metadata names the Natural History Museum. They were in the committed collection before this review. Use them because they make a good example, not to imply collaboration or endorsement.

A proposed Merian experiment:

- The model suggests showing successive states within one visual field.
- Translate that suggestion into a small record view which presents related life stages together while retaining individual labels and provenance.
- Compare it with a straightforward baseline showing independent cards. Keep information and task constant.
- Ask readers to locate a stage, understand its relationship to the others, and find the source of a statement. Record confusion and disagreement as well as success.
- Report who tried it and what was observed. A small qualitative pilot is useful; it is not evidence of general effectiveness.

This is a proposed design exercise, not a claim about biological correctness or suitability for NHM systems. Validate the interpretation against the source and, if it becomes scientific content, appropriate domain expertise.

A second, contrasting example could use Botero to explore visual weight. But reject any implied rule that rounded, oversized forms universally improve interfaces. A transfer from an artwork is a design hypothesis. Accessibility, task demands and context still determine whether it helps.

The existing SVG can remain linked as an exploratory artefact. If embedded, caption it as a two-dimensional PCA view of tentative k-means assignments, not proof that ten natural aesthetic families exist. Use cleared source images only if rights are established; the currently available alternatives are source links, original interface diagrams and your own design output.

## 5. A concrete narrative direction

The following is a proposed passage, not a rewrite of the README and not evidence of new work:

> I've been saving things I like on Google Arts & Culture for years: paintings, maps, furniture, architectural drawings. I wanted to find out whether that collection could tell me something useful about my taste, and whether I could turn it into guidance for things I make.
>
> Art Precepts Design is that experiment. The aim is a set of `design.md` playbooks for interfaces, interiors and a wider design language, grounded in the works I keep returning to.
>
> The first attempt was a sketch typed into AI Studio on my phone. It produced CuratorMD, an app with artwork analysis, curatorial themes and a design-token sandbox. My next prompt restyled it. Looking back at the code later, I found a more basic problem: the analysis had been given the artwork's title and metadata, but not the image. A later attempt to extend the app hit the model quota.
>
> I picked the idea up again as a pipeline. This time the model received the images. The collection became 801 records, with generated analysis for the 800 that had a static image, and a catalogue I could inspect and amend.
>
> Organising that catalogue raised another question. The clustering produced ten groups, but the review found that some of the apparent connections could be explained by artist names and the language of the generated critiques. I have kept the result and the criticism together. The groups are provisional.
>
> The next step is to take a few of these observations through to an actual design: decide which are useful, reject those that are generic, and show what changes. That is the part I want to test now. The code, catalogue and working notes document how I got here, including the attempts that did not do what I expected.

This leaves room for a short show-and-tell example immediately after the opening, once a human interpretation has actually been supplied. The cost correction is valuable journal material, but does not need to carry the central narrative.

## 6. NHM relevance and its limits

The [linked vacancy](https://jobs.nhm.ac.uk/Job/JobDetail?JobId=953) is **DiSSCo UK Head of the Technical Innovation Centre**. It combines technical experimentation with leading a team, developing usable services, cross-institution adoption and partnerships. The advert also says shortlisting is anonymised and panels do not view CVs. A public portfolio is supporting evidence and a visibility asset; do not assume it will be consulted during shortlisting.

| Capability relevant to that audience | What this project supports | What needs separate evidence |
|---|---|---|
| Practical AI/data experimentation | Prototyping, metadata handling, image analysis, caching and structured outputs | Production quality and operational reliability |
| Assessing whether an experiment deserves further investment | Rejected methodology, documented trade-offs, explicit unfinished work | A repeatable evaluation and a real user outcome |
| Stewardship of collections-derived information | Source fields, staged data, preservation intent and publication review | Resolved reuse basis, dependable provenance and tested safeguards |
| Communicating complex work | Potentially a clear case study with inspectable artefacts | A concise public explanation that works for non-specialists |
| Leading multidisciplinary people and programmes | This solo project illustrates decisions at a small scale | Actual team leadership, institutional delivery, budgets and stakeholder outcomes |
| Partnerships, adoption and sustainable services | Useful questions to address in the next experiment | Evidence from real collaborations, adoption or commercial/investment work |

Do not equate coordinating AI personas with leading a multidisciplinary human team. Do not reshape this personal art project into a claim about robotics, specimen digitisation throughput or national infrastructure. Use it as one example of hands-on judgement alongside separate professional case studies.

## 7. Public-release preparation: findings and priorities

### Blocking: complete the existing release gate on the final integrated tree

[Issue #1](https://github.com/originallgb/art-precepts-design/issues/1) remains open and explicitly blocks publication. [Issue #5](https://github.com/originallgb/art-precepts-design/issues/5) records the outstanding sequence. [PR #3](https://github.com/originallgb/art-precepts-design/pull/3) supplies security/privacy/data checks; [PR #4](https://github.com/originallgb/art-precepts-design/pull/4) supplies historical caveats, link repairs and catalogue identifier removal. Both are still proposals awaiting merge.

Their reported GitHub checks are green, but the tag-only release-gate job is skipped on the reviewed PR runs. Local integration checks pass. Neither is evidence that all issue acceptance requirements have been implemented or that publication is approved.

### Blocking under the stated privacy goal: scanner self-exclusion

PR #3 excludes `scripts/sanitize.py` from its default scan. That file contains the original session UUIDs, username and project identifier that the publication policy aims to remove. An explicit in-memory scan of the file finds those rule matches. Excluding a pattern definition from scanning may avoid self-triggering, but it does not remove the literal identifier from the public source.

Decide which identifiers genuinely need removal, then design the rules accordingly: generic context patterns, externally supplied private values, or fingerprint comparison where suitable. Do not claim identifiers are purged while retaining them in an excluded rule table. Preserve the real private evidence separately, with redacted public copies clearly labelled.

The full-history check also needs to distinguish deliberately synthetic fixtures and scanner patterns from actual historical disclosures. A zero-output promise for `git log -p --all` is not credible while the history intentionally includes matching test material and the scanner's original literals.

### High: the checks cover less than the hard-gate wording implies

The destructive-change guard inspects PR changes under `data/`. It does not prevent a Python script overwriting a live Sheet tab, regenerating catalogue notes, or rewriting existing local outputs. Existing historical scripts still have those operations. Document them as historical/unsafe to rerun without isolation; add meaningful runtime or negative-test safeguards before claiming that destructive operations are prevented.

The release-gate job aggregates checks on a tag. It does not itself stop an owner changing repository visibility or gate an unrelated deployment. Branch protection is currently absent. Treat publication as a controlled owner action after verification; describe precisely what CI enforces.

The data validator checks useful counts, keys and selected populated fields. In an in-memory negative test, replacing an inherited critique and setting a cluster ID to 999 produces no errors from its additive-key and cluster-ID checks. It therefore does not prove unchanged values or valid cluster membership. The current data does preserve analysed values into the clustered records; the weakness is in future regression detection.

The four tests demonstrate a dirty privacy fixture and a clean dataset. They do not test every failure mode promised by issue #1. In particular, the fake-secret fixture is excluded from repository-wide gitleaks and is not separately exercised by these unit tests through gitleaks.

### High: rights and private references need an explicit publication decision

Removal of raster images is supported by the reachable local Git object path inventory: no `.png`, `.jpg`, `.jpeg`, `.webp` or `.gif` paths were found. This is a bounded filename check, not a byte-level forensic scan of every hosted ref or embedded payload.

The licence excludes museum text from the project's content licence, but the repository still redistributes that text. Attribution and licence exclusion do not, by themselves, document a basis for publishing the copied material. Resolve that basis, or produce a rights-reviewed public export retaining identifiers and source links with only material suitable for redistribution. This is an unresolved publication-evidence question, not a legal conclusion about any individual record.

PR #4 removes Drive file IDs from catalogue frontmatter but deliberately leaves `data/` unchanged. Drive image IDs and URLs remain in data. An ID is not a permission grant, but publication should reflect an explicit decision about exposing those references and a fresh permission check. The README and checklist disagree about whether the Sheet is already shared; that status was not verified here.

### Medium: historical evidence and present claims need clearer separation

The ADR remains `PROPOSED`, correctly. Its body still contains claims challenged by the archived review. PR #4's top notes help, but the reader should not need to reconcile contradictory documents unaided. Add a short current decision summary with links to the preserved evidence.

Several scripts depend on an unavailable SQLite cache, including clustering and catalogue finalisation. `pipeline/README.md` understates these dependencies when it suggests the remaining scripts simply use repo-relative data. Recovered source is valuable; it is not yet a reproducible checkout. Publish an honest run-status table before adding a broad “run this” invitation.

CuratorMD arrived after the security PR's checks and is outside its Python syntax check. Its README instructs `.env.local`, while server initialisation uses plain `dotenv.config()`. The app also returns programmatic fallback analysis when no key exists, without provenance in the response, and the UI can announce Gemini analysis completion. Keep it as a labelled historical prototype; verify configuration, fallback labelling, build and exposure controls before promoting it as a live service.

### Medium: quantify only what can be traced

The published cost correction improves the old figure, but the token ledger still needs reconciliation. Its input total equals contextual text plus image tokens, apparently excluding the separately listed 290 system tokens per request. Its output count is extrapolated from a sampled character/token ratio. The recovered audit scripts do not establish an actual billing total.

Describe the roughly $2.08 number as the existing reconstruction under stated assumptions, not an invoiced cost or a rigorously established lower bound. Do not replace the old overconfident number with a new headline until provider usage/billing evidence is available. Timings and schema completeness likewise remain historical claims where the original raw evidence was not re-run in this review.

## 8. A publication and visibility strategy

### First: make a good destination

Create three levels of reading:

1. **README:** a short introduction, one sample with provenance, current state, and three useful paths: see an example, read the journey, inspect the method.
2. **Case study:** the complete arc, decisions, rejected approaches, contribution boundaries and one completed design experiment.
3. **Technical record:** scripts, data, dated journals, original reviews and corrections. Keep it complete and navigable.

Use an accurate contribution statement. For example: “I selected the collection, set the brief and direction, chose between approaches and reviewed the results. AI tools generated much of the code and analysis; the repository records those contributions and the changes made after review.” Confirm that wording against the actual work. Avoid implying either sole manual authorship or that the author's contribution was merely pressing a button.

### Then: publish episodes with a specific question

| Episode | Useful public question | Evidence to show |
|---|---|---|
| The beginning | What can years of favourites tell me about my taste? | The collection's variety and original brief |
| The prototype | What did a working interface conceal about the analysis? | A short request-payload comparison: metadata only, then image input |
| The corpus | What changes when an experiment has to handle the whole collection? | Coverage, the missing-image case, caching and a representative result |
| The grouping | Did I discover a pattern, or introduce one through the features? | Artist-name concentration, provisional map, proposed ablation |
| The use | Does a generated observation actually help me design? | A baseline, a change, a human decision and a small evaluation |

Date retrospective episodes honestly. Publish when there is an observation worth sharing, not to sustain an arbitrary daily cadence. Use one durable case-study URL and link short posts back to the relevant evidence. LinkedIn can reach professional contacts; GitHub holds the inspectable work. No messages or posts are authorised by this review.

Ask peers one answerable question tied to the artefact, such as whether a proposed grouping is useful or whether a provenance distinction is clear. Avoid generic announcements about building an AI platform. Track substantive feedback, independent use and conversations alongside page views; those are closer to the visibility the project needs.

### Recommended order

1. Resolve the publication blockers against the integrated tree and intended public history. Preserve private originals.
2. Shorten the front door by moving detail, not discarding it. Keep the complete case study and journal.
3. Add several genuine human annotations and one bounded design example. Select examples for explanatory value, not employer flattery.
4. Publish the repository and case study only after the existing owner gate is satisfied.
5. Share the original question and the first inspected result. Continue with the experiments as they happen.

Do not make a vector database, interactive cluster explorer, or ten generated playbooks a prerequisite for a convincing portfolio. Those may become useful later. The next discriminating evidence is whether one translation helps someone do something.

## A. Automated verification results

Machine-readable counts and dataset fingerprints are in [the verification record](2026-09-24-portfolio-verification.json). Checks are read-only except for these new review artefacts.

| Check | Result | Boundary |
|---|---|---|
| Four stages, each 801 records and 801 unique asset IDs | PASS | Current committed JSON |
| 801 catalogue notes, 800 non-empty critiques | PASS | Counts, not correctness |
| Analysed fields preserved in clustered rows | PASS | Value comparison by index |
| Ten clusters; counts sum to 801 | PASS | Does not establish useful separation |
| Exactly five hash-prefixed palette swatches per record | FAIL | 778/801; expected image-less exception alone does not explain the remainder |
| Individual affordance statements | FAIL | Identical scripted sentence in all 801 notes |
| Visible personal overrides | NOT DEMONSTRATED | All 801 placeholders untouched |
| Cluster metadata in catalogue notes | NOT DELIVERED | Zero notes with `cluster_id`; appropriately pending methodology gate |
| Banned terminology absent across generated notes | FAIL | Term counts above; contextual review still needed |
| Reachable raster file paths | PASS, LIMITED | Filename extensions in local reachable objects only |
| Isolated integrated privacy/data checks and unit tests | PASS | Four tests; limited enforcement described above |
| Validator rejects invalid cluster membership/inherited value edits | FAIL | In-memory negative tests not caught by relevant checks |
| Original tracked contents untouched by verification | PASS | SHA-256 before/after plus no tracked content diff |

## B. Requirements cross-reference

| Requirement and source | Delivered state | Assessment |
|---|---|---|
| Original brief: turn collection into design guidance | Corpus exists, final pipeline-backed playbook absent | PARTIAL |
| Implementation plan, lines 8–16: upstream invariant | Current analysed-to-clustered values preserved | PASS for inspected data; runtime protection incomplete |
| Implementation plan, line 60: Gate 2a | ADR proposed; no current acceptance found | OPEN |
| Implementation plan, lines 63–75: Gate 2b | Catalogue cluster metadata/affinities absent | PENDING, not a premature failure |
| Implementation plan, lines 79–110: Gates 2c/2d | Pipeline-backed playbooks absent | PENDING |
| GEMINI.md, lines 9–11: claims, context and status | Cost correction exists; historical audit and ADR still overstate parts | PARTIAL |
| GEMINI.md, line 14: no banned terms | Multiple catalogue hits | FAIL for blanket absence claim |
| Issue #1: publication hard gate | PR open, no main enforcement yet | BLOCKED |
| Issue #1: negative tests and integrity protection | Useful starter checks, important uncovered failure modes | PARTIAL |
| Issue #5: final history/privacy and permission checks | Outstanding | OPEN |
| Supplied session protocol: document-link validation | Prescribed script absent; targeted fallback validation used for review artefacts | PARTIAL for whole repository |
| Supplied session protocol: GitHub cross-links | Relevant issue/PR URLs in this local report | No external comments posted; task did not authorise messaging |

## C. Non-conformances and remediation summary

| Priority | Finding | Next action |
|---|---|---|
| Blocking | Existing publication gate open | Complete owner review, integration and final checks |
| Blocking under privacy goal | Excluded scanner source retains private literals | Redesign matching and public-history verification |
| High | CI claims exceed runtime/release enforcement | Narrow claims and cover critical destructive pathways |
| High | Rights basis and remaining private references unresolved | Decide public export scope and verify permissions |
| Medium | Provisional methodology described too strongly | Current decision summary, exact evaluation/production alignment |
| Medium | Five-angle/provenance and palette claims imprecise | Separate model fields, script text and human interpretation |
| Medium | No visible human decisions or demonstrated design payoff | Annotate examples and complete one bounded test |
| Medium | Recovered scripts/prototype not a verified portable service | Accurate run-status documentation; test before live promotion |
| Medium | Cost reconstruction still uncertain | Trace provider usage/billing or retain explicit uncertainty |

## D. Scorecard and close-out

This review does not convert the open gates into approval. Of the 13 automated checks above, seven pass (including one explicitly limited), four fail, and two are not demonstrated or not delivered as labelled. The narrative recommendation is to proceed with a concise, evidence-backed case study; public release remains blocked under the repository's own rules.

No existing data, catalogue note, application, README, historical report or release setting was changed. The review and verification record are new, local, uncommitted artefacts on `codex/portfolio-narrative-review`. The next editorial action is concrete: select a representative output and document the author's actual response to it. The next release action is separate: resolve the scanner and acceptance gaps before the existing publish checklist is treated as complete.

## Evidence reading trail

Paths below refer to source commit `79a1a34` unless a PR head is specified. Line references identify the material inspected, not an instruction to modify it.

- `apps/curatormd/BUILD_HISTORY.md`, prompts 1–3: initial intent, styling detour and quota stop.
- `apps/curatormd/server.ts`, lines 149–221: text-only analysis input and fallback branch.
- `pipeline/run_full_vision_pipeline.py`, lines 58–150 and 213–222: prompt, schema and actual image payload; line 415: scripted affordance sentence.
- `pipeline/finish_catalogue_and_sheet.py`, lines 25–76: external cache dependency and flattened output construction; line 168: the repeated sentence.
- `pipeline/generate_phase2a_clustering.py`, lines 52–139: cache dependency, missing-value defaults, creator/title/medium text features, fixed k-means and curated labels.
- `docs/decisions/001-latent-clustering-methodology.md` and `docs/reviews/20260905T0846Z_grok-4.6_adr-001-latent-clustering-methodology.md`: proposed methodology and reasons not to accept it. The review's evaluation-versus-production discrepancy remains historical evidence because its evaluation script is not in this checkout.
- `docs/process/telemetry_audit_report.md`, lines 180–205: reconstructed token ledger and sampled token ratio.
- PR #3 head `e0d1f1d`: `scripts/sanitize.py` exclusions and literal rules; `scripts/validate_data.py` additive-key and cluster checks; `tests/test_gates.py`; `.github/workflows/security-privacy-ci.yml`.
- PR #4 head `253e7e8`: historical context notes, catalogue identifier removal and recovered Sheet incident record.
- README handoff supplied in this conversation and its referenced outline: editorial context only. Neither was copied into the repository.

## Follow-up: publication-first editorial delivery, 24 September 2026

The owner clarified that the NHM vacancy was an example of the broader reason
for making work visible, not the intended audience for this project. The public
README and new journal entry are consequently written for interested peers and
potential collaborators or employers generally.

The owner also prioritised a secure public work in progress today. This
supersedes any suggested sequencing above that would put a completed design
example, polished case study or improved clustering before publication. Those
are continuation work. Actual privacy, source-rights and release-gate questions
remain separate from editorial completeness.

### A. Verification

The new README is 74 lines and 509 words. The five publication-facing documents
passed 19 local link/anchor checks with zero errors and the existing privacy
scanner in stdin mode with no findings. The archived README body matches the
previous README exactly after reversing relative-link relocation. All eight
recorded dataset fingerprints remain unchanged. No application, pipeline or
catalogue content changed, so no application tests were run.

### B. Requirements

| Requirement | Result | Evidence |
|---|---|---|
| Minimal public introduction in the agreed voice | PASS | README: premise, journey, one sample, WIP state, continuation and licence |
| Preserve the longer working record | PASS | Historical README body comparison |
| Lightweight continuation scaffold | PASS | Journal index, opening entry and one next experiment |
| No role-specific positioning | PASS | General audience; no NHM reference in new public-facing prose |
| Publication before optional polish | PASS | Next experiment explicitly not a release prerequisite |
| Secure-publication status remains honest | PASS | Repository still private; unchecked release tasks remain visible |

### C. Remaining boundary

This is the requested draft and scaffold, not a completed security remediation
or publication. No commits, pushes, merges, external messages, permission changes
or visibility changes were made. The release checklist identifies what remains
before changing visibility; it does not introduce a new product-completeness gate.

### D. Scorecard

Six editorial requirements pass; nineteen local links/anchors pass. No new
editorial blocker was found. Publication remains dependent on the existing
security gate and the final public data/history scope.
