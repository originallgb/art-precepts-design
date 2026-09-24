# The original guide: CuratorMD's first build (2026-09-02)

This is Gemini 3.7 Flash's summary of what it built from my first prompt
in Google AI Studio, reproduced verbatim. It was the clearest statement
of what the project is for, written before I got distracted polishing the
app's UX. Everything since, the vision pipeline, the clustering, and the
playbooks still to come, is working towards it.

My prompt, typed on my phone as a one-shot sketch, verbatim:

> an app that hcreates design.md andguideelines from a users favirorited art on google arts adn culture. the app analyzes list of google arts and culture links from a google sheet, runs visual and compositional . curates images into non obvois curatorial themes and collections.

---

I have built CuratorMD, a full-stack design system synthesis platform that analyzes favorited art from Google Arts & Culture, discovers non-obvious curatorial themes, and generates production-ready design.md guidelines with live design token sandboxes.

## Key Capabilities & Visual Design

* **Google Arts & Culture & Sheets Integration:**
   * Direct import from Google Sheets URLs (with support for public view links, CSV, and TSV exports).
   * Bulk link pasting for Google Arts & Culture assets with automatic metadata extraction.
   * Curated Masterpiece Packs spanning Chiaroscuro & Tenebrism, Ukiyo-e Negative Space (Ma), Bauhaus & De Stijl, Impressionist Chroma, and Symbolism & Gold Leaf.
* **Multimodal Visual & Compositional Analysis (Gemini API):**
   * Chromatic Decomposition: Generates 5-color harmonic palettes with exact hex codes, RGB values, percentage distribution, and semantic UI roles (dominant, secondary, accent, surface, neutral).
   * Interactive Composition Overlays: Live toggleable Rule of Thirds 3×3 Grid, Golden Ratio Spiral, and AI-detected Focal Anchor Points with coordinate tooltips.
   * Visual Laws Breakdown: Analyzes visual weight gravity, color temperature, chiaroscuro contrast, surface texture grain, spatial rhythm cadence, and typographic resonance.
* **Non-Obvious Curatorial Collections:**
   * Synthesizes unexpected cross-cutting themes with curatorial essays, aesthetic philosophies, and digital product translation blueprints.
* **design.md Generation & Token Studio:**
   * Complete, structured markdown document generation with execution philosophies, CSS custom properties (:root), typography step ratios (1.25), spacing scale, radii, component blueprints, and curatorial Dos & Don'ts.
   * Live UI Sandbox: Interactive preview rendering buttons, inputs, metrics cards, and badges dynamically driven by the active design tokens.
   * Export Formats: One-click download of design.md, copyable CSS variables, Tailwind CSS @theme directives, and Figma Tokens JSON.

---

## Where each part stands (2026-09-24)

| Guide | Status in this repo |
|---|---|
| Sheet import | Done. The Sheet is the master record; `data/` holds each stage. |
| Chromatic decomposition | Mostly. The vision pass extracts a 5-hex palette per image, without the percentages or UI roles. |
| Composition and visual laws | Done, from the images themselves, as the 5 Angles in `catalogue/`. |
| Non-obvious curatorial collections | Partly. Ten k-means clusters with names and philosophies in `clusters/`; ADR 001 still `PROPOSED`, and no curatorial essays yet. |
| design.md and tokens | Not started. This is Phase 7, the playbooks. |
| Live sandbox and exports | Only in CuratorMD (`apps/curatormd/`), not wired to the pipeline's output. |
