> **Correction note (2026-09-24).** This is the 2026-09-04 governance protocol written after the Sheet-overwrite incident during the README's Phase 1 (enrichment). Its rules were later folded into `GEMINI.md` at the repo root. The repository link below points to `originallgb/art-to-design`, which is now a private archive. The $0.30 cost figure at §"Incident" below was itself one of the unverified claims being described; see `docs/process/telemetry_audit_report.md` for the corrected figure of at least $2.08.

# Engineering Learnings & Governance Protocol

**Repository**: [originallgb/art-to-design](https://github.com/originallgb/art-to-design)  
**Document Version**: 1.0.0  
**Effective Date**: September 4, 2026  

---

## 1. Upstream Invariant: The Non-Destructive Rule

> ### **CARDINAL RULE**
> **No script, tool, or autonomous agent may destructively overwrite or mutate extant project artifacts without verifiable supporting evidence, automated backup, and explicit review approval.**

### Applications Across Project Layers:
1. **Tabular & Curatorial Datasets**: Existing baseline datasets (`favorites.json`, `favorites_enriched.json`, `favorites_analyzed.json`) are immutable foundations. Derived transformations must produce separate, additive files (`favorites_clustered.json`) rather than modifying upstream sources in place.
2. **Master Google Sheet**: Automated sync tools must never target or overwrite existing tabs (e.g. `sheetId: 0` or `sheetId: 98234710`). Any new perspective or data representation must be provisioned via an additive `AddSheetRequest` with distinct naming and styling.
3. **Catalogue Notes**: The 801 individual Markdown files in `Google Arts & Culture/catalogue/` represent enriched intellectual assets. Any subsequent phase (such as clustering enrichment) must perform an **additive merge**: updating frontmatter keys and appending affinity sections while preserving 100% of existing critique text, heuristics, and user manual annotations (`## User Notes & Project Overrides`).

---

## 2. Root Cause Analysis: Phase 1 Failures & Corrective Learnings

### Failure Example 1: In-Place Sheet Overwrite & Cosmetic Collapse
* **Incident**: An automated export utility updated `sheetId: 0` in-place, renaming the user's primary curated gallery (`Enriched Favorites`) to `Catalogue Precepts`, wiping `=IMAGE` preview formulas, and dumping raw TSV without text wrapping or column width rules.
* **Root Cause**: The script targeted an existing index rather than provisioning a new sheet, and lacked visual QA prior to declaring completion.
* **Corrective Learning**: Visual and structural deliverables cannot be verified solely by API return codes (`200 OK`). Visual inspection (via headless browser screenshots or direct link audits) is mandatory before marking tasks complete.

### Failure Example 2: Delayed PR Closure & State Divergence
* **Incident**: Following the remediation in PR #2, the fix was verified and reported, but the PR remained unmerged while work moved directly toward planning Phase 2. `main` remained stale at `cf194c5`, creating a divergence between the working branch and the trunk.
* **Root Cause**: An agent assumed that producing verification proof was synonymous with closing the delivery lifecycle.
* **Corrective Learning**: A fix lifecycle is only complete when the PR is merged into `main`, the tracking issue is closed, and local `main` is fast-forwarded. Work on subsequent phases must never commence from a stale trunk or an unmerged fix branch.

### Failure Example 3: Unsubstantiated Telemetry Assertions
* **Incident**: Early progress reports quoted estimated cost ($\sim \$0.30$) and runtime without citing event logs, timestamps, or raw billing formulas.
* **Root Cause**: Reliance on informal heuristics rather than querying persistent execution state.
* **Corrective Learning**: Quantified claims are strictly prohibited unless accompanied by verifiable evidentiary artifacts (SQLite timestamps, log file hashes, exact token counts).

---

## 3. Git & Branching Governance for Subsequent Phases

1. **Branch Isolation**: Every new feature or analytical phase operates on a dedicated branch branched directly from updated `main` (`feat/phase-2-clustering-and-playbooks`).
2. **Atomic Milestones**: Commits must correspond to verified sub-phase milestones with descriptive commit messages and evidence summaries.
3. **Pull Request Gate**: Merges to `main` require a formal Pull Request documenting what was changed, what was verified, and referencing relevant tracking issues.
4. **Pragmatic Hardening**: Operational safeguards should be right-sized: enforce non-destructive invariants and local schema tests without creating bureaucratic friction that stalls feature progress.
