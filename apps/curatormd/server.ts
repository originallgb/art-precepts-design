import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import dotenv from 'dotenv';
import { GoogleGenAI, Type } from '@google/genai';
import { createServer as createViteServer } from 'vite';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;

app.use(express.json({ limit: '15mb' }));

// Lazy Gemini client helper
function getGeminiClient(): GoogleGenAI | null {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) {
    return null;
  }
  return new GoogleGenAI({
    apiKey,
    httpOptions: {
      headers: {
        'User-Agent': 'aistudio-build',
      },
    },
  });
}

// 1. Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    hasApiKey: Boolean(process.env.GEMINI_API_KEY),
  });
});

// 2. Import Google Sheet or CSV data
app.post('/api/import-sheet', async (req, res) => {
  try {
    const { sheetUrl, rawCsv } = req.body;
    let csvData = rawCsv || '';

    if (sheetUrl && !rawCsv) {
      // Extract Google Sheet ID if possible
      const match = sheetUrl.match(/\/spreadsheets\/d\/([a-zA-Z0-9-_]+)/);
      if (match && match[1]) {
        const sheetId = match[1];
        const exportUrl = `https://docs.google.com/spreadsheets/d/${sheetId}/export?format=csv`;
        try {
          const fetchRes = await fetch(exportUrl);
          if (fetchRes.ok) {
            csvData = await fetchRes.text();
          } else {
            // try gviz url
            const gvizUrl = `https://docs.google.com/spreadsheets/d/${sheetId}/gviz/tq?tqx=out:csv`;
            const gvizRes = await fetch(gvizUrl);
            if (gvizRes.ok) {
              csvData = await gvizRes.text();
            }
          }
        } catch (fetchErr) {
          console.warn('Direct fetch of sheet failed, attempting text parse', fetchErr);
        }
      }
    }

    if (!csvData) {
      return res.status(400).json({ error: 'No spreadsheet content could be read. Make sure the Google Sheet is shared with "Anyone with the link can view", or paste CSV/TSV content directly.' });
    }

    // Parse CSV lines
    const lines = csvData.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
    if (lines.length === 0) {
      return res.status(400).json({ error: 'The spreadsheet appears to be empty.' });
    }

    // Helper to parse CSV row
    const parseRow = (line: string): string[] => {
      const result: string[] = [];
      let cur = '';
      let inQuotes = false;
      for (let i = 0; i < line.length; i++) {
        const char = line[i];
        if (char === '"') {
          inQuotes = !inQuotes;
        } else if ((char === ',' || char === '\t') && !inQuotes) {
          result.push(cur.trim());
          cur = '';
        } else {
          cur += char;
        }
      }
      result.push(cur.trim());
      return result.map(s => s.replace(/^"|"$/g, '').trim());
    };

    const header = parseRow(lines[0]).map(h => h.toLowerCase());
    const titleIdx = header.findIndex(h => h.includes('title') || h.includes('artwork') || h.includes('name') || h.includes('piece'));
    const artistIdx = header.findIndex(h => h.includes('artist') || h.includes('creator') || h.includes('painter'));
    const urlIdx = header.findIndex(h => h.includes('url') || h.includes('link') || h.includes('arts') || h.includes('google'));
    const imgIdx = header.findIndex(h => h.includes('image') || h.includes('img') || h.includes('photo') || h.includes('pic'));
    const yearIdx = header.findIndex(h => h.includes('year') || h.includes('date') || h.includes('period'));
    const notesIdx = header.findIndex(h => h.includes('note') || h.includes('comment') || h.includes('fav') || h.includes('tag'));

    const items: any[] = [];
    for (let i = 1; i < lines.length; i++) {
      const row = parseRow(lines[i]);
      if (row.length === 0 || row.every(cell => !cell)) continue;

      let sourceUrl = (urlIdx !== -1 ? row[urlIdx] : '') || row.find(c => c.startsWith('http')) || '';
      let title = (titleIdx !== -1 ? row[titleIdx] : '') || row[0] || 'Untitled Artwork';
      let artist = (artistIdx !== -1 ? row[artistIdx] : '') || row[1] || 'Unknown Artist';
      let imageUrl = (imgIdx !== -1 ? row[imgIdx] : '') || row.find(c => c.match(/\.(jpeg|jpg|png|webp)/i)) || '';
      let year = yearIdx !== -1 ? row[yearIdx] : '';
      let userNotes = notesIdx !== -1 ? row[notesIdx] : '';

      // If source is a Google Arts link and no image, provide a smart default or placeholder
      if (sourceUrl && !imageUrl) {
        imageUrl = `https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1200&q=80`;
      }

      items.push({
        id: `imported-${Date.now()}-${i}`,
        title,
        artist,
        year,
        sourceUrl,
        imageUrl: imageUrl || 'https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1200&q=80',
        userNotes,
        isFavorite: true,
        userRating: 5
      });
    }

    res.json({ success: true, count: items.length, artworks: items });
  } catch (error: any) {
    console.error('Error importing sheet:', error);
    res.status(500).json({ error: error?.message || 'Failed to process Google Sheet' });
  }
});

// 3. Multimodal / Visual & Compositional Analysis
app.post('/api/analyze-artwork', async (req, res) => {
  try {
    const { artwork } = req.body;
    if (!artwork || !artwork.title) {
      return res.status(400).json({ error: 'Artwork title or details are required' });
    }

    const ai = getGeminiClient();
    if (!ai) {
      // Return smart programmatic fallback if no API key configured yet
      return res.json({
        analysis: generateFallbackAnalysis(artwork)
      });
    }

    const prompt = `You are a world-renowned art historian, visual composition analyst, and master design system architect.
Perform an exhaustive visual, chromatic, and compositional analysis for the following Google Arts & Culture artwork:

Artwork Details:
- Title: ${artwork.title}
- Artist: ${artwork.artist || 'Unknown'}
- Year/Period: ${artwork.year || 'Historical'}
- Medium: ${artwork.medium || 'Fine Art'}
- Museum: ${artwork.museum || 'Fine Art Museum'}
- Source Link: ${artwork.sourceUrl || 'Google Arts & Culture'}
- User Notes: ${artwork.userNotes || 'None'}

Return a precise JSON object according to the exact schema:
1. "palette": Array of exactly 5 color swatches with { hex (format #RRGGBB), name (evocative artistic name), percentage (integer summing to 100), role ("dominant" | "secondary" | "accent" | "neutral" | "surface"), rgb ([r, g, b]) }.
2. "dominantMood": Evocative 1-2 sentence aesthetic mood.
3. "compositionType": Detailed compositional structure (e.g. "Dynamic Diagonal & Caravaggesque Chiaroscuro", "Golden Ratio Triangle with Asymmetric Counterweight", "Orthogonal Matrix", "All-Over Field with Horizonless Depth").
4. "visualWeight": Distribution of weight, focal anchoring, and gravitational flow.
5. "colorTemperature": "warm" | "cool" | "balanced" | "polarizing".
6. "contrastLevel": "high" | "medium" | "low" | "dramatic-chiaroscuro".
7. "textureFeel": Physical and optical surface texture (impasto, sfumato glaze, woodblock keyblock, smooth enamel).
8. "spatialRhythm": Visual cadence and pacing across the visual plane.
9. "designTakeaways": 3-4 actionable, high-level design system principles derived from this piece for modern web UI/UX.
10. "typographicResonance": {
      "fontPairingSuggestion": "Display + Sans pairing",
      "weightCadence": "Description of heading vs body contrast",
      "suggestedSerif": "Serif font name",
      "suggestedSans": "Sans-serif font name",
      "trackingPreference": "e.g. +0.05em wide tracking for headers"
    }
11. "focalPoints": 2-3 key compositional anchors with { "x": percentage (0-100), "y": percentage (0-100), "label": string, "importance": "primary" | "secondary" | "counter-balance" }.

Ensure exact JSON format.`;

    const response = await ai.models.generateContent({
      model: 'gemini-3.7-flash',
      contents: prompt,
      config: {
        responseMimeType: 'application/json',
      },
    });

    const text = response.text || '';
    const parsed = JSON.parse(text);
    res.json({ analysis: parsed });
  } catch (error: any) {
    console.error('Error analyzing artwork:', error);
    res.status(500).json({ error: error?.message || 'Failed to analyze artwork with Gemini' });
  }
});

// 4. Curate Non-Obvious Curatorial Themes & Collections
app.post('/api/curate-collections', async (req, res) => {
  try {
    const { artworks } = req.body;
    if (!artworks || !Array.isArray(artworks) || artworks.length === 0) {
      return res.status(400).json({ error: 'At least one artwork is required' });
    }

    const ai = getGeminiClient();
    if (!ai) {
      return res.json({
        themes: generateFallbackThemes(artworks)
      });
    }

    const artworksSummary = artworks.map((a, idx) => ({
      id: a.id,
      index: idx + 1,
      title: a.title,
      artist: a.artist,
      year: a.year,
      movement: a.movement,
      mood: a.compositionAnalysis?.dominantMood || a.userNotes || '',
      composition: a.compositionAnalysis?.compositionType || '',
      palette: a.compositionAnalysis?.palette?.map((p: any) => p.hex) || [],
      userNotes: a.userNotes || ''
    }));

    const prompt = `You are an avant-garde senior museum curator at Google Arts & Culture and a principal design systems director.
Your mission is to curate the following set of artworks into 2 to 4 NON-OBVIOUS, cross-cutting curatorial themes.

DO NOT group simply by basic chronological epoch or single artist (e.g. avoid banal themes like "17th Century Art" or "Impressionist Paintings").
INSTEAD, construct deep conceptual, visual, emotional, and structural dialogues between disparate pieces (e.g., "The Architecture of Solitude: Tenebrist Thresholds & Japanese Negative Space", "Chromatic Dissonance & Kinetic Geometry", "Liminal Horizons & Sacred Materiality").

Artworks Collection:
${JSON.stringify(artworksSummary, null, 2)}

Return a JSON array of Curatorial Themes where each theme contains:
- "id": string (unique slug, e.g. "theme-architecture-of-solitude")
- "title": Evocative, sophisticated theme title
- "subtitle": Brief curatorial premise (1 sentence)
- "curatorialEssay": A rich, intellectual 2-3 paragraph curatorial essay explaining how these specific artworks dialogue with one another, their hidden visual synergies, and their tension.
- "aestheticPhilosophy": The core aesthetic law or thesis governing this collection.
- "artworkIds": Array of artwork IDs from the input that belong to this theme (each artwork can belong to 1 or more themes).
- "keywords": 4-6 curated aesthetic tags (e.g. ["Tenebrism", "Asymmetric Ma", "Golden Luster", "Tactile Sfumato"])
- "designTranslation": {
    "visualTone": "Atmospheric tone description for digital products",
    "recommendedUseCases": ["Fintech luxury portal", "Editorial magazine", "Data visualization suite"],
    "keyColors": ["#hex1", "#hex2", "#hex3", "#hex4"],
    "layoutStyle": "Layout and spatial cadence recommendation",
    "interactionPacing": "Transition physics and micro-interaction feel"
  }
`;

    const response = await ai.models.generateContent({
      model: 'gemini-3.7-flash',
      contents: prompt,
      config: {
        responseMimeType: 'application/json',
      },
    });

    const text = response.text || '';
    const parsed = JSON.parse(text);
    const themes = Array.isArray(parsed) ? parsed : (parsed.themes || [parsed]);
    res.json({ themes });
  } catch (error: any) {
    console.error('Error curating themes:', error);
    res.status(500).json({ error: error?.message || 'Failed to curate themes' });
  }
});

// 5. Generate Comprehensive Design.md and Design Tokens
app.post('/api/generate-design-system', async (req, res) => {
  try {
    const { artworks, selectedTheme, systemName, projectContext } = req.body;
    if (!artworks || artworks.length === 0) {
      return res.status(400).json({ error: 'Artworks are required to generate design.md' });
    }

    const ai = getGeminiClient();
    if (!ai) {
      return res.json({
        designSystem: generateFallbackDesignSystem(artworks, selectedTheme, systemName)
      });
    }

    const prompt = `You are the Principal Design Systems Architect.
Generate a comprehensive, production-grade \`design.md\` guideline document and design token architecture derived directly from the user's favorited Google Arts & Culture collection.

Artworks Analyzed:
${artworks.map((a: any) => `- "${a.title}" by ${a.artist} (${a.year || 'Historical'}). Composition: ${a.compositionAnalysis?.compositionType || 'Rich visual composition'}. Mood: ${a.compositionAnalysis?.dominantMood || 'Sublime'}`).join('\n')}

Curatorial Theme Context:
${selectedTheme ? `Theme: "${selectedTheme.title}" - ${selectedTheme.subtitle}\nPhilosophy: ${selectedTheme.aestheticPhilosophy}\nKey Colors: ${selectedTheme.designTranslation?.keyColors?.join(', ')}` : 'Comprehensive Synthesis of Artworks'}

Additional Context: ${projectContext || 'General Modern Web Application & High-Craft Digital Interfaces'}
Desired System Name: ${systemName || 'Aura & Cadence Design System'}

You MUST generate a JSON object with:
1. "title": String (e.g. "${systemName || 'Aura & Cadence'} Design System")
2. "subtitle": String (e.g. "Derived from Google Arts & Culture Masterpiece Analysis")
3. "curatorialInspiration": String (High-level summary of the aesthetic foundation)
4. "generatedAt": ISO timestamp string
5. "markdownContent": A rich, comprehensive, fully formatted \`design.md\` string (complete with H1, H2, H3, code blocks for Tailwind CSS, CSS variables, typography hierarchies, component blueprints, spacing math, elevation, and Dos and Don'ts).
6. "tokens": Exact structured tokens object:
   - "colors": {
       "brandPrimary": "#HEX",
       "brandSecondary": "#HEX",
       "brandAccent": "#HEX",
       "surfaceBase": "#HEX",
       "surfaceElevated": "#HEX",
       "surfaceOverlay": "#HEX",
       "textPrimary": "#HEX",
       "textSecondary": "#HEX",
       "textMuted": "#HEX",
       "borderSubtle": "#HEX",
       "borderFocus": "#HEX"
     }
   - "paletteVariants": Array of { "name": string, "hex": string, "tokenName": string, "usage": string, "wcagContrastRatio": number }
   - "typography": {
       "displayFont": string,
       "bodyFont": string,
       "monoFont": string,
       "baseFontSize": "16px",
       "scaleRatio": 1.25,
       "headingLineHeight": "1.2",
       "bodyLineHeight": "1.6"
     }
   - "spacing": {
       "scale": [
         { "name": "xs", "rem": "0.25rem", "px": 4 },
         { "name": "sm", "rem": "0.5rem", "px": 8 },
         { "name": "md", "rem": "1rem", "px": 16 },
         { "name": "lg", "rem": "1.5rem", "px": 24 },
         { "name": "xl", "rem": "2rem", "px": 32 },
         { "name": "2xl", "rem": "3rem", "px": 48 },
         { "name": "3xl", "rem": "4rem", "px": 64 }
       ],
       "containerPadding": "24px",
       "sectionGap": "48px"
     }
   - "radii": {
       "buttonRadius": "8px",
       "cardRadius": "12px",
       "tagRadius": "9999px"
     }
   - "elevation": {
       "cardShadow": "0 4px 20px -2px rgba(0, 0, 0, 0.4)",
       "dropdownShadow": "0 10px 30px -4px rgba(0, 0, 0, 0.5)",
       "modalShadow": "0 20px 50px -8px rgba(0, 0, 0, 0.7)"
     }
   - "rules": {
       "dos": ["Array of 4-6 specific actionable rules"],
       "donts": ["Array of 4-6 specific banned anti-patterns"]
     }

Make sure the markdown content is impeccably formatted and deeply grounded in the visual laws extracted from the artworks.`;

    const response = await ai.models.generateContent({
      model: 'gemini-3.7-flash',
      contents: prompt,
      config: {
        responseMimeType: 'application/json',
      },
    });

    const text = response.text || '';
    const parsed = JSON.parse(text);
    res.json({ designSystem: parsed });
  } catch (error: any) {
    console.error('Error generating design system:', error);
    res.status(500).json({ error: error?.message || 'Failed to generate design system' });
  }
});

// Fallback generators for offline/instant mode
function generateFallbackAnalysis(artwork: any) {
  return {
    palette: [
      { hex: '#121418', name: 'Museum Obsidian', percentage: 38, role: 'surface', rgb: [18, 20, 24] },
      { hex: '#d4af37', name: 'Gilded Cadmium', percentage: 24, role: 'accent', rgb: [212, 175, 55] },
      { hex: '#8c593b', name: 'Raw Sienna Earth', percentage: 18, role: 'secondary', rgb: [140, 89, 59] },
      { hex: '#425164', name: 'Atmospheric Slate', percentage: 12, role: 'dominant', rgb: [66, 81, 100] },
      { hex: '#f0ece1', name: 'Linen Parchment', percentage: 8, role: 'neutral', rgb: [240, 236, 225] }
    ],
    dominantMood: `Atmospheric, meditative poise with deep chromatic resonance and classical visual cadence.`,
    compositionType: 'Dynamic Diagonal & Tenebrist Focal Luster',
    visualWeight: 'Asymmetric anchor with radiant golden focal counterpoint',
    colorTemperature: 'warm',
    contrastLevel: 'high',
    textureFeel: 'Textured glaze with tactile brushwork highlights against velvety deep surfaces',
    spatialRhythm: 'Rhythmic hierarchy directing gaze through luminous focal thresholds',
    designTakeaways: [
      'Establish a 60-30-10 color balance using deep obsidian surfaces, slate midtones, and gilded accents.',
      'Maintain generous negative space around hero elements to evoke museum-grade contemplative focus.',
      'Employ high-contrast typography pairings (ornamental serif display with ultra-clean modern sans).'
    ],
    typographicResonance: {
      fontPairingSuggestion: 'Cinzel / Playfair Display Display with Plus Jakarta Sans Body',
      weightCadence: 'Stark contrast between sculptural bold titles and airy light body copy',
      suggestedSerif: 'Cinzel',
      suggestedSans: 'Plus Jakarta Sans',
      trackingPreference: '+0.05em wide uppercase tracking for section labels'
    },
    focalPoints: [
      { x: 50, y: 45, label: 'Primary Luminous Focal Mass', importance: 'primary' },
      { x: 70, y: 65, label: 'Secondary Accent Anchor', importance: 'secondary' }
    ]
  };
}

function generateFallbackThemes(artworks: any[]) {
  return [
    {
      id: 'theme-luminous-tension',
      title: 'The Luminous Threshold & Silent Void',
      subtitle: 'A cross-examination of high-contrast tenebrism and boundless contemplative negative space.',
      curatorialEssay: `This curation pairs the dramatic illumination of classical European chiaroscuro with the boundless, meditative spatial restraint of Eastern aesthetics. Rather than merely presenting historical artifacts, this collection interrogates how light defines matter out of dark obscurity.\n\nThe deep shadows do not serve as empty background; rather, they act as active spatial chambers that give the gilded highlights their transcendent weight. In digital design, this translates into high-craft dark mode systems where glowing focal points command supreme clarity.`,
      aestheticPhilosophy: 'Light derives its sacred authority strictly from the depth and discipline of the surrounding darkness.',
      artworkIds: artworks.map(a => a.id),
      keywords: ['Chiaroscuro', 'Negative Space', 'Specular Highlights', 'Architectural Void', 'Gilded Cadmium'],
      designTranslation: {
        visualTone: 'Sublime, high-contrast, editorial luxury with cinematic focal radiance.',
        recommendedUseCases: ['Executive Analytics', 'Curated Art Portfolios', 'Architectural Showcase', 'High-End SaaS'],
        keyColors: ['#0d0f12', '#d4af37', '#8a4b28', '#f2f4f8'],
        layoutStyle: 'Spacious asymmetrical grid with deep dark surfaces and single-source illumination accents.',
        interactionPacing: 'Deliberate, velvety ease-out curves (250ms) with subtle luminous border shines.'
      }
    }
  ];
}

function generateFallbackDesignSystem(artworks: any[], selectedTheme: any, systemName: string = 'CuratorMD Design System') {
  return {
    title: systemName,
    subtitle: 'Production Design Tokens & Guidelines Synthesized from Google Arts & Culture Masterpieces',
    curatorialInspiration: selectedTheme ? selectedTheme.title : 'Classical & Modernist Masterpiece Compositional Synthesis',
    generatedAt: new Date().toISOString(),
    markdownContent: `# ${systemName}
> **Curatorial Genesis:** Synthesized from compositional, chromatic, and structural analysis of ${artworks.length} masterpiece artworks from Google Arts & Culture.

---

## 1. Executive Philosophy & Thematic Manifesto

The **${systemName}** is founded upon the timeless visual principles of classical painting, woodblock spatial discipline, and modernist geometric equilibrium.

- **The Law of the Threshold:** 60% deep obsidian canvas, 30% structural midtones, and 10% luminous golden focal points.
- **Asymmetric Gravity:** Layouts leverage calculated asymmetric weights to guide attention naturally without visual friction.
- **Tactile Restraint:** Avoid gratuitous gradients; every shadow and highlight represents a physical light vector.

---

## 2. Color System & Design Tokens

### Primary Palette Tokens
\`\`\`css
:root {
  /* Surface Tokens */
  --surface-base: #0d0f12;
  --surface-elevated: #161a20;
  --surface-overlay: #1e242c;
  
  /* Brand & Chromatic Tokens */
  --brand-primary: #d4af37;
  --brand-secondary: #2b5876;
  --brand-accent: #c83424;
  
  /* Text & Typography Tokens */
  --text-primary: #f2f4f8;
  --text-secondary: #9ea8b6;
  --text-muted: #5e6878;
  
  /* Border & Stroke Tokens */
  --border-subtle: rgba(212, 175, 55, 0.15);
  --border-focus: #d4af37;
}
\`\`\`

---

## 3. Typography Hierarchy & Baseline Grid

| Hierarchy | Font Family | Size | Weight | Line Height | Tracking |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Display H1** | Cinzel / Playfair | 48px (3.0rem) | 700 Bold | 1.15 | +0.02em |
| **Heading H2** | Cinzel / Playfair | 32px (2.0rem) | 600 SemiBold | 1.25 | +0.01em |
| **Heading H3** | Plus Jakarta Sans | 24px (1.5rem) | 600 SemiBold | 1.35 | 0em |
| **Body Large** | Plus Jakarta Sans | 18px (1.125rem) | 400 Regular | 1.60 | 0em |
| **Body Regular**| Plus Jakarta Sans | 16px (1.0rem) | 400 Regular | 1.65 | 0em |
| **Caption / Tag**| Plus Jakarta Sans | 12px (0.75rem) | 600 SemiBold | 1.40 | +0.06em (Uppercase) |
| **Data / Code** | JetBrains Mono | 13px (0.8125rem) | 500 Medium | 1.50 | 0em |

---

## 4. Spacing, Radii & Elevation Rules

### Spatial Scale
- **xs:** 4px (0.25rem) — micro icon gaps
- **sm:** 8px (0.50rem) — pill padding & badge gaps
- **md:** 16px (1.00rem) — inner card padding
- **lg:** 24px (1.50rem) — container outer margins
- **xl:** 32px (2.00rem) — section dividers
- **2xl:** 48px (3.00rem) — major hero gaps

### Border Radii
- **Buttons & Pills:** 8px (or 9999px for status tags)
- **Cards & Containers:** 12px
- **Modals & Dialogs:** 16px

---

## 5. Component Construction Blueprints

### Primary Button
\`\`\`html
<button class="px-5 py-2.5 bg-[#d4af37] hover:bg-[#c59b27] text-[#0d0f12] font-semibold text-sm rounded-lg transition-all shadow-md active:scale-95">
  Curate Collection
</button>
\`\`\`

### Elevated Gallery Card
\`\`\`html
<div class="bg-[#161a20] border border-[#d4af37]/20 rounded-xl p-6 shadow-xl hover:border-[#d4af37]/40 transition-colors">
  <span class="text-xs uppercase font-mono tracking-widest text-[#d4af37]">Composition Anchor</span>
  <h3 class="text-xl font-serif text-[#f2f4f8] mt-2 mb-3">Tenebrist Threshold</h3>
  <p class="text-sm text-[#9ea8b6] leading-relaxed">Deep shadows provide architectural clarity to focal elements.</p>
</div>
\`\`\`

---

## 6. Curatorial Laws: Dos and Don'ts

### ✅ DO
- Keep neutral background saturation below 5% for authentic museum-grade depth.
- Use 1px subtle gold or cobalt hairline borders to frame cards instead of heavy drop shadows.
- Ensure all body typography maintains at least a 7:1 contrast ratio against the dark background.
- Pair classical high-contrast serif headlines with pristine, readable geometric sans body copy.

### ❌ DON'T
- Never use neon purple-to-cyan arbitrary gradients.
- Avoid stacking multiple nested card containers within one another.
- Do not round cards with extreme radii exceeding 16px when using metallic hairline borders.
- Never truncate status labels across multiple lines.
`,
    tokens: {
      colors: {
        brandPrimary: '#d4af37',
        brandSecondary: '#2b5876',
        brandAccent: '#c83424',
        surfaceBase: '#0d0f12',
        surfaceElevated: '#161a20',
        surfaceOverlay: '#1e242c',
        textPrimary: '#f2f4f8',
        textSecondary: '#9ea8b6',
        textMuted: '#5e6878',
        borderSubtle: 'rgba(212, 175, 55, 0.15)',
        borderFocus: '#d4af37'
      },
      paletteVariants: [
        { name: 'Florentine Gold', hex: '#d4af37', tokenName: 'brand.primary', usage: 'Primary action buttons, key metrics, active borders', wcagContrastRatio: 9.8 },
        { name: 'Prussian Indigo', hex: '#2b5876', tokenName: 'brand.secondary', usage: 'Secondary badges, subtle card fills, tags', wcagContrastRatio: 6.4 },
        { name: 'Vermilion Lacquer', hex: '#c83424', tokenName: 'brand.accent', usage: 'Critical alerts, urgent callouts, favorite stars', wcagContrastRatio: 5.2 },
        { name: 'Abyssal Obsidian', hex: '#0d0f12', tokenName: 'surface.base', usage: 'Primary screen background canvas', wcagContrastRatio: 16.5 },
        { name: 'Museum Slate', hex: '#161a20', tokenName: 'surface.elevated', usage: 'Card surfaces, modals, navigation bars', wcagContrastRatio: 14.1 },
        { name: 'Linen Frost', hex: '#f2f4f8', tokenName: 'text.primary', usage: 'Headings, primary readable body copy', wcagContrastRatio: 15.8 }
      ],
      typography: {
        displayFont: 'Cinzel, Playfair Display, serif',
        bodyFont: 'Plus Jakarta Sans, sans-serif',
        monoFont: 'JetBrains Mono, monospace',
        baseFontSize: '16px',
        scaleRatio: 1.25,
        headingLineHeight: '1.2',
        bodyLineHeight: '1.65'
      },
      spacing: {
        scale: [
          { name: 'xs', rem: '0.25rem', px: 4 },
          { name: 'sm', 'rem': '0.5rem', px: 8 },
          { name: 'md', 'rem': '1rem', px: 16 },
          { name: 'lg', 'rem': '1.5rem', px: 24 },
          { name: 'xl', 'rem': '2rem', px: 32 },
          { name: '2xl', 'rem': '3rem', px: 48 },
          { name: '3xl', 'rem': '4rem', px: 64 }
        ],
        containerPadding: '24px',
        sectionGap: '48px'
      },
      radii: {
        buttonRadius: '8px',
        cardRadius: '12px',
        tagRadius: '9999px'
      },
      elevation: {
        cardShadow: '0 4px 20px -2px rgba(0, 0, 0, 0.4)',
        dropdownShadow: '0 10px 30px -4px rgba(0, 0, 0, 0.5)',
        modalShadow: '0 20px 50px -8px rgba(0, 0, 0, 0.7)'
      },
      rules: {
        dos: [
          'Use deep obsidian canvas (#0d0f12) with subtle 1px gold hairline borders for museum elegance.',
          'Enforce strict typography pairing: sculptural classical serifs for display, clean geometric sans for UI.',
          'Structure layouts with golden ratio and rule of thirds asymmetric focal points.',
          'Verify all primary actions pass WCAG AA with high-contrast luminance (minimum 7:1).'
        ],
        donts: [
          'Do not introduce synthetic saturated purple/cyan glow effects.',
          'Never use rounded card radii exceeding 16px with crisp hairline borders.',
          'Do not create overcrowded cards; preserve at least 24px of negative space between visual sections.',
          'Avoid mixing more than 2 accent colors within a single component.'
        ]
      }
    }
  };
}

// 6. Vite middleware integration for development & static serving for production
async function startServer() {
  if (process.env.NODE_ENV !== 'production') {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), 'dist');
    app.use(express.static(distPath));
    app.get('*', (req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on http://localhost:${PORT}`);
  });
}

startServer();
