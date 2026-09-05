# Art-to-Design Workspace Rules

## Git Discipline
- **Never push directly to `main`**. All changes — including documentation-only commits — must go through a feature branch and Pull Request.
- **Complete the PR lifecycle before starting new work**. A fix or feature is not "done" until its PR is merged, its tracking issue is closed, and local `main` is fast-forwarded. Do not begin downstream phases from unmerged branches.
- **Non-destructive additive enrichment**: No script may overwrite or mutate extant project artifacts (datasets, catalogue notes, Google Sheet tabs) without verifiable evidence, automated backup, and explicit user approval. Derived outputs must be written to new, additive files.

## Claims & Declarations
- **No unsubstantiated quantified claims**. Every number (cost, runtime, accuracy, score) must cite its evidentiary source (log file, database query, hash). Prefer "no claim" over an unverified one.
- **Honest metric context**: When reporting statistical measures (e.g. silhouette scores, accuracy), state the value AND its interpretive context (what constitutes strong/weak for that metric). Do not present weak scores as "validated."
- **Status fields track reality, not aspiration**: Documents (ADRs, plans, reports) must not be marked `ACCEPTED`, `COMPLETE`, or `VERIFIED` until the corresponding gate or review has been explicitly approved by the user.

## Vocabulary
- **Banned terms**: "Genome", "Living" (in project naming context), "tapestry", "juxtaposition", "dance of light and shadow", "evocative", and generic art-school clichés.
- **Approved vocabulary**: The Catalogue, Catalogue Notes, The 5 Angles, Design Precepts & Heuristics, The Design Playbook, Standards & Theories, Jury, Angles.
