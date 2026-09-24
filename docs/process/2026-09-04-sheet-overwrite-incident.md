# 2026-09-04 Sheet Overwrite Incident

> **Note (2026-09-24).** This is the original incident record from `originallgb/art-to-design`, the first repository, now a private archive. It is reproduced verbatim below: the bug report as issue #1, and the fix as pull request #2. Lessons drawn from this incident are documented in `docs/process/engineering_learnings_and_governance.md`. Paths referred to in the text below use the old `Google Arts & Culture/...` layout, since flattened to `data/`, `catalogue/`, `clusters/`, `pipeline/`, `docs/`.

## Issue #1: [BUG] Google Sheet tab overwrite, layout malformation, and unverified telemetry claims

**Opened**: 2026-09-04T15:52:59Z  
**Closed**: 2026-09-04T21:53:53Z

## Executive Summary

During an operational execution to synchronize the 800 analyzed artworks and their 5-Angle precepts into the master Google Sheet, an automation defect resulted in data loss, sheet malformation, and unverifiable telemetry reporting:
1. **Primary Tab Overwrite:** The script targeted `sheetId: 0` (holding the canonical **Enriched Favorites** dataset) and renamed it to **Catalogue Precepts**, completely overwriting the historical favorite records and formatting in place rather than creating a new dedicated tab.
2. **Layout Malformation:** The raw TSV dataset (`favorites_analyzed.tsv`) was streamed into the sheet without formatting rules. Crucial attributes—including lengthy multi-sentence precepts, heuristics, descriptions, and tags across 21 columns—were inserted without text wrapping (`WRAP`), without customized column pixel widths, and without frozen headers, resulting in an unreadable presentation.
3. **Unverified Telemetry Claims:** Claims regarding pipeline execution, batch completion, costs, and token usage were posted without supporting forensic execution telemetry or verifiable visual proof of sheet status.

---

## Root Cause Analysis (RCA)

- **Sheet ID 0 Mutated In-Place:** The ingestion routine did not invoke `AddSheetRequest` to create a dedicated tab with an isolated `sheetId`. Instead, it issued an update request against the default sheet (`sheetId: 0`), altering its title from "Enriched Favorites" to "Catalogue Precepts" and executing a destructive range update with the 800 analyzed records.
- **Unformatted Value Injection:** The Google Sheets API integration executed a plain `spreadsheets.values.update` / raw TSV paste without executing companion batch requests (`batchUpdate`):
  - No `RepeatCellRequest` setting `wrapStrategy: "WRAP"` on narrative/text columns.
  - No `UpdateDimensionPropertiesRequest` to configure proportional column widths.
  - No frozen header row properties or header row cell formatting (bold, background fill, vertical alignment).
- **Absence of Audit & Verification Pipeline:** Automated validation stages were skipped prior to declaring pipeline completion:
  - Telemetry logs (timestamped API calls, token counts, batch run IDs) were not preserved or forensic-audited.
  - No visual validation or automated snapshot capture was performed against the published sheet to confirm readability and multi-tab structure.

---

## Reproduction Steps

1. Open the target Google Sheet (`Personal Taste Genome / Art to Design Master`).
2. Run the legacy sync script with `favorites_analyzed.tsv`.
3. Inspect sheet tabs: Observe that the original "Enriched Favorites" tab has vanished; only "Catalogue Precepts" exists at `sheetId: 0`.
4. Inspect cell contents: Observe columns with extensive narrative content (e.g. `precept_1`, `heuristic_1`, `formal_analysis`) stretching horizontally across adjacent cells with text clipping or overflow due to missing wrap strategy.
5. Attempt to locate audit telemetry or visual verification proofs: None exist in execution logs.

---

## Remediation Checklist

- [ ] **1. Tab Restoration**
  - [ ] Access Google Sheet version history and restore the canonical "Enriched Favorites" tab data and structure from **revision 115 (`rev 115`)** onto `sheetId: 0`.
  - [ ] Verify all 800 original rows and columns are intact and verified against `favorites_enriched.tsv`.

- [ ] **2. Tab Isolation & Ingestion**
  - [ ] Issue an `AddSheetRequest` to create a new, distinct tab named **"Catalogue Precepts"** with a dedicated `sheetId`.
  - [ ] Populate the tab with all 800 analyzed artwork records from `favorites_analyzed.tsv`.

- [ ] **3. Professional Formatting & Layout Standards**
  - [ ] Apply `wrapStrategy: "WRAP"` to all narrative and multi-line columns (`description`, `medium`, `provenance`, 5-Angle precepts, and heuristics).
  - [ ] Configure explicit column widths for readability (compact IDs/indices, mid-width artist/title, wide precept/heuristic columns).
  - [ ] Freeze the header row (Row 1).
  - [ ] Style the header row with dark/contrasting background, bold text, and centered/vertical alignment.
  - [ ] Set vertical alignment to `TOP` for all data rows.

- [ ] **4. Forensic Telemetry Audit**
  - [ ] Generate and publish a comprehensive forensic audit report validating pipeline telemetry (model invocations, batch sizes, latency, token usage, and cost reconciliations).
  - [ ] Commit forensic audit artifact to the repository under `Google Arts & Culture/docs/`.

- [ ] **5. Visual Proof & QA Verification**
  - [ ] Capture visual verification (screenshots / export verification) confirming both "Enriched Favorites" and "Catalogue Precepts" tabs are co-existing with immaculate layout.
  - [ ] Attach visual artifacts to the PR and incident resolution report.

---

## PR #2: fix: restore Enriched Favorites tab, apply professional typography to Catalogue Precepts, and add forensic telemetry audit

**Opened**: 2026-09-04T16:01:47Z  
**Merged**: 2026-09-04T21:53:52Z

Closes #1

## Summary of Changes

This pull request resolves the incident documented in #1 where an automated update overwrote `sheetId: 0` in the master Google Sheet, introduced text overflow and malformation, and lacked auditable telemetry proof.

### Key Remediations:
1. **Enriched Favorites Tab Restoration**:
   - Restored the canonical `Enriched Favorites` tab on `sheetId: 0` from revision 115 (`rev 115`), restoring all 800 historical favorites records, metadata columns, and layout intact.
2. **Dedicated "Catalogue Precepts" Tab Isolation**:
   - Created a separate, isolated tab titled **"Catalogue Precepts"** via `AddSheetRequest`, ensuring non-destructive co-existence with existing catalog data.
   - Populated the tab with the full 800 analyzed records from `favorites_analyzed.tsv`.
3. **Professional Typography & Layout Formatting**:
   - Applied `wrapStrategy: "WRAP"` across all multi-line narrative columns (`description`, `medium`, `provenance`, 5-Angle precepts, and heuristics).
   - Configured custom pixel column widths for optimal reading comfort (compact indices, wide precept and analysis columns).
   - Applied frozen header row with bold text, distinct header fill, and vertical centering.
   - Configured vertical alignment to `TOP` for all data rows.
4. **Forensic Systems & Telemetry Audit**:
   - Added and committed [`telemetry_audit_report.md`](file:///<repo>/Google%20Arts%20&%20Culture/docs/telemetry_audit_report.md) under `Google Arts & Culture/docs/`.
   - Formally details cryptographic signatures (SHA-256) of evidentiary artifacts (`multimodal_analysis.db`, `task-1232.log`), temporal milestone accounting (1,536.13s runtime, 98.82% pool saturation), latency percentiles (p50: 19.0s, p99: 28.0s), token economics (1,496,165 total tokens, $0.6720 actual spend), and schema validation across all 800 analyzed artworks.

---

## Root Cause Analysis (RCA)

- **Root Cause 1 (Tab Overwrite):** The sync utility targeted `sheetId: 0` directly with an `UpdateSheetPropertiesRequest` rather than provisioning a new sheet via `AddSheetRequest`, overwriting the canonical dataset in-place.
- **Root Cause 2 (Formatting Defect):** Value updates were performed via plain TSV streaming without executing companion formatting `batchUpdate` calls (`RepeatCellRequest` with wrap strategies, `UpdateDimensionPropertiesRequest` for column dimensions).
- **Root Cause 3 (Unverified Telemetry Claims):** Completion announcements lacked repository-committed audit trails, cryptographic checksums of raw execution databases, and formal verification logs.

---

## Verification & QA

- [x] **Google Sheet Structure Verification:** Verified both "Enriched Favorites" (`sheetId: 0`) and "Catalogue Precepts" tabs co-exist correctly in the master workbook.
- [x] **Cell Formatting & Layout QA:** Inspected cell wrap strategies, column dimension bounds, and frozen header rows to guarantee high readability without cell truncation or horizontal bleed.
- [x] **Forensic Telemetry Audit:** Verified SQLite cache database (`790b7827...`) and process task log (`fbf3e254...`) with zero schema validation errors across all 800 corpus items.
- [x] **Documentation & Repository Cleanliness:** Committed report adheres strictly to architectural documentation standards.
