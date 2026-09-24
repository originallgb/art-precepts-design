# Learning Proposal: Phase 1→2 Behavioral Corrections

> **Source**: This session's arc from Phase 1 incident remediation through Phase 2a self-audit. The self-audit (Section E) surfaced 5 gaps — 3 of which repeated the exact failure patterns documented in Phase 1. These are the reusable corrections.

---

## Identified Behaviors to Persist

### Behavior 1: Git Merge Discipline & Non-Destructive Enrichment
**Classification**: **Rule** (workspace-scoped)  
**Root Cause**: Two distinct failures occurred:
- PR #2 was left unmerged while Phase 2 planning began (Phase 1 Failure Example 2).
- The governance doc (`4b5518f`) was pushed directly to `main` without a PR — the exact violation we'd just codified as a rule, on the same day.

**Why a rule**: This is a strict invariant that should be enforced on every interaction in this workspace. It doesn't require multi-step procedures — it's a hard guardrail.

---

### Behavior 2: Honest Metric Reporting & Status Declarations  
**Classification**: **Rule** (workspace-scoped)  
**Root Cause**: Two patterns recurred:
- ADR 001 was committed with `Status: ACCEPTED` before Gate 2a user approval — premature declaration identical to Phase 1's premature "Complete" marking.
- Silhouette score (0.079) was presented as "validated" without acknowledging it's well below the 0.25 threshold for reasonable cluster structure.

**Why a rule**: This is a behavioral guardrail, not a procedure. It constrains how claims are made.

---

### Behavior 3: Self-Audit Against Governing Documents  
**Classification**: **Skill** (new)  
**Root Cause**: The Phase 2a self-audit caught 5 gaps that would have gone unnoticed without the explicit cross-referencing procedure. This is a repeatable multi-step workflow: gather governing docs → run automated checks → cross-reference each deliverable against each requirement → flag honest non-conformances.

**Why a skill**: This is a multi-step analytical procedure that should be triggered after completing any gated phase of work. It involves specific steps (read governing docs, run verification scripts, produce a structured audit report).

---

## Proposed Changes

### 1. [NEW] Workspace Rule — `GEMINI.md` in repo root

**Target Path**: `<repo>\GEMINI.md`

> [!NOTE]
> This workspace has no existing `GEMINI.md` or `.agents/` directory. This would be the first workspace-scoped customization file.

**Proposed Content**:

```markdown
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
```

---

### 2. [NEW] Skill — `self-audit`

**Target Path**: `<repo>\.agents\skills\self-audit\SKILL.md`

**Proposed Content**:

```markdown
---
name: self-audit
description: >-
  Run a skeptical self-audit of completed work against governing documents
  (implementation plans, ADRs, governance protocols, critical reviews).
  Use after completing any gated phase of work, before presenting results
  to the user. Also use when the user asks to "review", "audit", "verify
  against the plan", or "check your work."
---

# Self-Audit Against Governing Documents

When a gated phase of work is complete, run this procedure before
presenting results or requesting user sign-off.

## Steps

### 1. Gather Governing Documents
Identify and read all documents that specify requirements for this phase:
- Implementation plans (what was promised)
- ADRs (what methodology was decided)
- Governance protocols (what rules apply)
- Critical review findings (what past failures must not recur)
- Issue tracker (what is open/blocked)

### 2. Run Automated Verification
Write and execute a verification script that checks every testable claim:
- File existence and counts
- Schema integrity (required fields present, correct types)
- Non-destructive invariant (upstream files untouched — hash comparison)
- Banned terminology scan across all generated files
- Git state (correct branch, clean working tree, pushed to remote)

### 3. Cross-Reference Deliverables Against Requirements
For each requirement in each governing document, produce a pass/fail
assessment with evidence. Use a table format:

| Requirement | Source Document & Line | Delivered | Evidence | Assessment |
|---|---|---|---|---|

### 4. Flag Honest Non-Conformances
Identify gaps where execution departed from documented standards.
Classify each by severity (Blocking / Medium / Low) and propose
remediation. Do not suppress findings to present a clean report.

Key categories to check:
- **Premature declarations**: Did any status field (ACCEPTED, COMPLETE)
  get set before the corresponding review gate?
- **Merge discipline**: Was anything pushed directly to main?
- **Unsubstantiated claims**: Are quantified assertions backed by
  cited evidence?
- **Metric honesty**: Are statistical scores contextualized with
  interpretive benchmarks?

### 5. Produce Audit Report
Create an artifact with:
- Section A: Automated verification results (table)
- Section B: Cross-reference against each governing document (tables)
- Section C: Honest non-conformances with severity and remediation
- Section D: Summary scorecard (pass/fail counts per category)

Set `request_feedback = true` on the artifact.
```

---

## What I Am NOT Proposing

- **No global rule changes**: These learnings are specific to this workspace's governance model and git discipline. The global `GEMINI.md` already covers general tool preferences and naming style.
- **No updates to existing skills**: The `code-review` and `diagnosing-bugs` skills cover different workflows. The self-audit pattern is distinct — it's an internal compliance check, not a code review or bug diagnosis.
- **No CI/CD automation**: That lane belongs to `@jules` via Issue #3. These rules are agent-behavioral, not pipeline-level.
