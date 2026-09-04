# Art to Design: Design Precepts & Playbook Pipeline

> An opinionated, amendable personal Catalogue of art, style, and visual design synthesized from 801 curated Google Arts & Culture favorites, engineered to seed operational `design.md` design playbooks and standards.

---

## Overview

**Art to Design** bridges historical art curation and contemporary product/systems design. By combining dense curatorial metadata, Wikimedia/Wikidata semantic links, and high-resolution visual assets with multimodal AI perception, this project extracts the latent principles governing a personal visual taste profile.

The ultimate deliverable is the **Design Playbook**: a collection of operational **`design.md`** files (color tokens, spatial typography, component standards, layout rules, and design theories) rooted directly in ancestral art lineages.

---

## Repository Structure

```
art-to-design/
├── README.md                                             # Project overview & roadmap
└── Google Arts & Culture/
    ├── plans/
    │   └── draft_plan_1_design_precepts.md              # Committed Draft Plan 1 & Critique Prompts
    ├── favorites.json                                    # Raw favorites baseline (801 items)
    ├── favorites.tsv                                     # Raw favorites TSV
    ├── favorites_enriched.json                           # Enriched dataset (47 columns, derived dimensions, Wikidata)
    ├── favorites_enriched.tsv                            # Enriched TSV table
    └── images/                                           # 800 high-resolution preview images (=s1200)
```

---

## Key Artifacts & Links

* **Committed Architectural Plan**: [`Google Arts & Culture/plans/draft_plan_1_design_precepts.md`](Google%20Arts%20&%20Culture/plans/draft_plan_1_design_precepts.md)
* **Master Google Sheet**: [Google Arts & Culture - Favorites](https://docs.google.com/spreadsheets/d/1Tznbdor6-JFLkGNtuN5StasMSopnLkhdqzgbq7NWdAU/edit)
  - 802 rows × 47 columns with live `=IMAGE(...)` visual preview gallery.
* **Google Drive Sync Folder**: `Google Arts & Culture` (ID: `REDACTED_DRIVE_FOLDER_ID`)

---

## The 5 Evaluative Angles

The multimodal analysis examines each work through 5 practical design angles:
1. **Composition & Lineage**: Underlying geometry, visual balance, rhythm, and historical lineage.
2. **Utility & Ergonomics**: Functional aesthetics, focal hierarchy, and interface/tool affordances.
3. **Visual Language & Semiotics**: Visual signifiers, symbolic encoding, and narrative tension.
4. **Light, Space & Materiality**: Light/shadow dynamics, negative space handling, and surface textures.
5. **Color & Typography**: Palette balance, contrast profiles, and typographic/calligraphic weight.

---

## Status & Roadmap

- [x] **Phase 0: Extraction & Purification** — 801 cultural assets filtered and chronologically indexed.
- [x] **Phase 1: Metadata Enrichment** — 25+ curatorial fields, Wikidata QIDs, metric physical dimensions, and aspect ratios.
- [x] **Phase 2: Visual Asset Caching** — 800 high-res image files collected and synced.
- [x] **Phase 3: Architecture Planning** — Draft Plan 1 committed with clean vocabulary and critique prompts.
- [ ] **Phase 4: Multimodal Analysis** — Batch structured JSON extraction across the 5 Angles.
- [ ] **Phase 5: Latent Clustering** — Multimodal vector embeddings + UMAP / HDBSCAN taxonomy.
- [ ] **Phase 6: Catalogue Notes** — 800 individual Obsidian-compatible Markdown files.
- [ ] **Phase 7: The Design Playbook** — Seeded `design.md` standards per cluster.
