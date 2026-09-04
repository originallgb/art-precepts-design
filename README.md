# Art to Design: Personal Taste Genome & Generative Design Systems

> An opinionated, amendable personal corpus of art, style, and visual design synthesized from 801 curated Google Arts & Culture favorites, engineered to seed operational `design.md` design systems.

---

## Overview

**Art to Design** bridges historical art curation and contemporary visual/system design. By combining dense curatorial metadata, Wikimedia/Wikidata open semantic data, and high-resolution visual assets with multimodal AI perception, this project extracts the latent principles governing a personal visual taste profile.

The ultimate deliverable is a suite of **seeded `design.md` manifestos** (covering color design tokens, spatial typography, component affordances, layout geometry, and visual philosophies) rooted directly in ancestral art lineages.

---

## Repository Structure

```
art-to-design/
├── README.md                                             # Project overview & roadmap
└── Google Arts & Culture/
    ├── plans/
    │   └── draft_plan_1_personal_taste_genome.md        # Committed Draft Plan 1 Packet & Critique Prompts
    ├── favorites.json                                    # Raw favorites baseline (801 items)
    ├── favorites.tsv                                     # Raw favorites TSV
    ├── favorites_enriched.json                           # Enriched dataset (47 columns, derived dimensions, Wikidata)
    ├── favorites_enriched.tsv                            # Enriched TSV table
    └── images/                                           # 800 high-resolution preview images (=s1200)
```

---

## Key Artifacts & Links

* **Committed Architectural Plan**: [`Google Arts & Culture/plans/draft_plan_1_personal_taste_genome.md`](Google%20Arts%20&%20Culture/plans/draft_plan_1_personal_taste_genome.md)
* **Master Google Sheet**: [Google Arts & Culture - Favorites](https://docs.google.com/spreadsheets/d/1Tznbdor6-JFLkGNtuN5StasMSopnLkhdqzgbq7NWdAU/edit)
  - 802 rows × 47 columns with live `=IMAGE(...)` visual preview gallery.
* **Google Drive Sync Folder**: `Google Arts & Culture` (ID: `REDACTED_DRIVE_FOLDER_ID`)

---

## The Advisory Council Framework ("The Board Members")

The next phase of multimodal analysis evaluates the corpus through 5 distinct intellectual lenses:
1. **The Formalist**: Compositional geometry, technique, visual rhythm, and art-historical lineage.
2. **The Industrial & UX Designer**: Physical affordances, surface tension, spatial ergonomics, and functional aesthetics.
3. **The Cultural Semiotician**: Cultural signifiers, symbolic encoding, narrative subtext, and emotional valence.
4. **The Spatial Materialist**: Light/void balance, negative space, tactile materiality, and spatial perspective.
5. **The Colorist & Typographer**: Chromatic temperature, tonal contrast profiles, and typographic/calligraphic weight.

---

## Status & Roadmap

- [x] **Phase 0: Extraction & Purification** — 801 cultural assets filtered and chronologically indexed.
- [x] **Phase 1: Metadata Enrichment** — 25+ curatorial fields, Wikidata QIDs, metric physical dimensions, and aspect ratios.
- [x] **Phase 2: Visual Asset Caching** — 800 high-res image files collected and synced.
- [x] **Phase 3: Architecture Planning** — Draft Plan 1 committed with multi-lens critique prompts.
- [ ] **Phase 4: Multimodal Analysis** — Batch structured JSON extraction across all 800 images.
- [ ] **Phase 5: Latent Clustering** — Multimodal vector embeddings + UMAP / HDBSCAN taxonomy.
- [ ] **Phase 6: Taste Genome Dossier** — 800 individual Obsidian-compatible Markdown files.
- [ ] **Phase 7: Generative `design.md` Files** — Operational design system manifestos per cluster.
