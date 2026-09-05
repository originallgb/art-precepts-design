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
