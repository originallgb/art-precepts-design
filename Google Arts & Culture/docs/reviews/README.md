# Reviews & Audits

Archive of project reviews and forensic audits. Naming:

```
{YYYYMMDDTHHMMZ}_{authoring-model}_{report-name}.md
```

Timestamps are UTC from artifact metadata or the writing turn. The model slug is the **authoring** model (who wrote the report), recovered from Antigravity `USER_SETTINGS_CHANGE` events, subagent `Model=` fields, and thinking traces — not the model that the report is about.

Originals are left in place. Each archived copy has YAML provenance at the top.

## Catalog

| File | When (UTC) | Authoring model | Git | Original |
|---|---|---|---|---|
| [20260904T1558Z_gemini-3.8-flash-high_telemetry-audit.md](./20260904T1558Z_gemini-3.8-flash-high_telemetry-audit.md) | 2026-09-04 15:58 | **Gemini 3.8 Flash (High)** via `telemetry_auditor` subagent (`Model=inherit`) | committed `bb719e9` (PR #2) | `docs/telemetry_audit_report.md` |
| [20260904T2113Z_claude-opus-4.6_phase2-critical-review.md](./20260904T2113Z_claude-opus-4.6_phase2-critical-review.md) | 2026-09-04 21:13 | **Claude Opus 4.6 (Thinking)** | uncommitted (brain only) | `~/.gemini/antigravity/brain/agy-session-2287/phase2_critical_review.md` |
| [20260905T0820Z_claude-opus-4.6_phase2a-self-audit.md](./20260905T0820Z_claude-opus-4.6_phase2a-self-audit.md) | 2026-09-05 08:20 | **Claude Opus 4.6 (Thinking)** | uncommitted (brain only) | `~/.gemini/antigravity/brain/agy-session-2287/phase2a_self_audit.md` |
| [20260905T0846Z_grok-4.6_adr-001-latent-clustering-methodology.md](./20260905T0846Z_grok-4.6_adr-001-latent-clustering-methodology.md) | 2026-09-05 08:46 | **Grok 4.6** | uncommitted (this folder) | written in this Grok Build session |

## How models were identified

Parent conversation: Antigravity brain `agy-session-2287`.

`USER_SETTINGS_CHANGE` timeline from `.system_generated/logs/transcript.jsonl`:

| Time (UTC) | Model Selection |
|---|---|
| 2026-08-30 22:57 | None → Gemini 3.7 Flash (High) |
| 2026-09-04 10:14 | → Gemini 3.8 Flash (Medium) |
| 2026-09-04 10:48 | → Gemini 3.8 Flash (High) |
| 2026-09-04 21:07 | → **Claude Opus 4.6 (Thinking)** |
| 2026-09-04 21:53 | → Gemini 3.8 Flash (Medium) |
| 2026-09-05 08:15 | → **Claude Opus 4.6 (Thinking)** |

- **Telemetry audit**: written at 15:58 on 2026-09-04, while the parent was still Gemini 3.8 Flash (High). The `telemetry_auditor` subagent was invoked with `Model=inherit`. Its own transcript has no independent model switch. Thinking traces are Gemini planner steps.
- **Phase 2 critical review**: requested and written in the 21:07 Opus turn (`"Let me compile the critical review."`). Metadata `updatedAt` 21:13:06Z.
- **Phase 2a self-audit**: requested and written in the 08:15 Opus turn (`"Now let me write the honest audit report."`). Metadata `updatedAt` 08:20:48Z.
- **ADR 001 review**: this Grok 4.6 session.

Do not confuse authoring model with subject model. The telemetry report audits a Vertex AI `gemini-2.5-flash` vision pipeline; that is the pipeline under test, not who wrote the report.

## Related documents not copied here

These are not reviews/audits (plans, governance, or GitHub objects):

| Document | Why excluded |
|---|---|
| `docs/adr_001_latent_clustering_methodology.md` | Decision record, not a review. Subject of the Grok review above. |
| `docs/engineering_learnings_and_governance.md` | Governance protocol produced after the Phase 2 critical review. Authored 2026-09-04 21:54 under Gemini 3.8 Flash (Medium). Committed `4b5518f` on `main`. |
| `plans/draft_plan_1_design_precepts.md` | Plan packet. Advisor subagent used Antigravity `Model=pro` at 2026-09-04 10:14. |
| [GitHub Issue #1](https://github.com/originallgb/art-to-design/issues/1) | Incident ticket, not a markdown audit. |
| [GitHub PR #2](https://github.com/originallgb/art-to-design/pull/2) | Merge vehicle for the telemetry audit. |
