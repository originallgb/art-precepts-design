import { PresetCollection } from '../types';

export const PRESET_COLLECTIONS: PresetCollection[] = [
  {
    id: 'chiaroscuro-mystics',
    name: 'The Luminous Threshold',
    description: 'Chiaroscuro, deep tenebrism, and golden candlelight transitions that translate into cinematic, high-contrast dark interfaces.',
    badge: 'Chiaroscuro & Lighting',
    artworks: [
      {
        id: 'art-1',
        title: 'The Night Watch',
        artist: 'Rembrandt van Rijn',
        year: '1642',
        medium: 'Oil on canvas',
        movement: 'Dutch Golden Age',
        museum: 'Rijksmuseum, Amsterdam',
        sourceUrl: 'https://artsandculture.google.com/asset/the-night-watch/eQEbPflDpAhQqQ',
        imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/The_Night_Watch_-_HD.jpg/1280px-The_Night_Watch_-_HD.jpg',
        userNotes: 'Masterclass in dynamic composition, atmospheric amber lighting, and deep tenebrist depth.',
        isFavorite: true,
        userRating: 5,
        compositionAnalysis: {
          palette: [
            { hex: '#111215', name: 'Abyssal Umber', percentage: 40, role: 'surface', rgb: [17, 18, 21] },
            { hex: '#c59b27', name: 'Gilded Cadmium', percentage: 20, role: 'accent', rgb: [197, 155, 39] },
            { hex: '#8a4b28', name: 'Burnt Sienna', percentage: 15, role: 'secondary', rgb: [138, 75, 40] },
            { hex: '#3c3b37', name: 'Smoked Charcoal', percentage: 15, role: 'dominant', rgb: [60, 59, 55] },
            { hex: '#d9cbab', name: 'Aged Parchment', percentage: 10, role: 'neutral', rgb: [217, 203, 171] }
          ],
          dominantMood: 'Monumental, dramatic, electric theatricality with focused focal illumination.',
          compositionType: 'Dynamic Diagonal & Caravaggesque Chiaroscuro',
          visualWeight: 'Bottom-heavy with central luminous piercing spotlight on the lieutenant and captain.',
          colorTemperature: 'warm',
          contrastLevel: 'dramatic-chiaroscuro',
          textureFeel: 'Heavy textural glaze with luminous impasto highlights on gold brocade.',
          spatialRhythm: 'Polyrhythmic, multi-layered diagonals creating expansive atmospheric depth.',
          designTakeaways: [
            'Use deep charcoal-black background layers with pinpoint warm amber-gold focal highlights.',
            'Maintain a 60% shadow, 30% ambient midtones, 10% luminous highlight ratio for high-end cinematic density.',
            'Apply deliberate directional gradients to guide user eye flow through hierarchically prioritized action areas.'
          ],
          typographicResonance: {
            fontPairingSuggestion: 'Cinzel Decorative Display with Plus Jakarta Sans Body',
            weightCadence: 'Stark contrast between heavy bold display headings and ultra-clean light body copy',
            suggestedSerif: 'Cinzel / Playfair Display',
            suggestedSans: 'Plus Jakarta Sans',
            trackingPreference: 'Slightly tracked display (+0.05em) and crisp neutral body'
          },
          focalPoints: [
            { x: 42, y: 55, label: 'Captain Frans Banninck Cocq', importance: 'primary' },
            { x: 55, y: 52, label: 'Lieutenant in Radiant Gold', importance: 'primary' },
            { x: 30, y: 62, label: 'Illuminated Girl with Golden Rooster', importance: 'secondary' }
          ]
        }
      },
      {
        id: 'art-2',
        title: 'The Calling of Saint Matthew',
        artist: 'Caravaggio',
        year: '1600',
        medium: 'Oil on canvas',
        movement: 'Baroque',
        museum: 'San Luigi dei Francesi, Rome',
        sourceUrl: 'https://artsandculture.google.com/asset/the-calling-of-st-matthew/DwF1s8KzX4lWvw',
        imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Caravaggio_-_The_Calling_of_Saint_Matthew.jpg/1280px-Caravaggio_-_The_Calling_of_Saint_Matthew.jpg',
        userNotes: 'A beam of piercing light slicing diagonally across shadowy tavern interior.',
        isFavorite: true,
        userRating: 5,
        compositionAnalysis: {
          palette: [
            { hex: '#0f0e0d', name: 'Tenebrous Obsidian', percentage: 45, role: 'surface', rgb: [15, 14, 13] },
            { hex: '#d4a359', name: 'Shaft of Revelation Gold', percentage: 22, role: 'accent', rgb: [212, 163, 89] },
            { hex: '#7a2222', name: 'Crimson Velveteen', percentage: 14, role: 'secondary', rgb: [122, 34, 34] },
            { hex: '#483a2e', name: 'Raw Umber', percentage: 12, role: 'dominant', rgb: [72, 58, 46] },
            { hex: '#eae3d2', name: 'Warm Alabaster', percentage: 7, role: 'neutral', rgb: [234, 227, 210] }
          ],
          dominantMood: 'Sublime, intense spiritual tension, sharp theatrical revelation.',
          compositionType: 'Single Diagonal Light Vector (Right-to-Left)',
          visualWeight: 'Asymmetrical: Upper right empty shadow balanced by intense left cluster of figures.',
          colorTemperature: 'warm',
          contrastLevel: 'dramatic-chiaroscuro',
          textureFeel: 'Smooth dark surfaces punctuated by rich textiles, feathers, and illuminated flesh.',
          spatialRhythm: 'Linear light beam directing gaze directly across interactive focal groups.',
          designTakeaways: [
            'Use single-source lighting gradients across modal sheets and card headers.',
            'Pair intense crimson accents with warm antique gold for high-urgency or premium actions.',
            'Leverage negative dark space to allow key focal cards to emerge naturally.'
          ],
          typographicResonance: {
            fontPairingSuggestion: 'Playfair Display Italic headings with JetBrains Mono numbers',
            weightCadence: 'High contrast editorial typography with sharp serifs',
            suggestedSerif: 'Playfair Display',
            suggestedSans: 'Plus Jakarta Sans',
            trackingPreference: 'Tight heading tracking with generous line height (1.6)'
          },
          focalPoints: [
            { x: 38, y: 58, label: 'Matthew Questioning Gestures', importance: 'primary' },
            { x: 86, y: 48, label: 'Christ’s Pointing Hand', importance: 'primary' },
            { x: 70, y: 22, label: 'Diagonal Window Beam Light Source', importance: 'secondary' }
          ]
        }
      },
      {
        id: 'art-3',
        title: 'Girl with a Pearl Earring',
        artist: 'Johannes Vermeer',
        year: '1665',
        medium: 'Oil on canvas',
        movement: 'Dutch Golden Age',
        museum: 'Mauritshuis, The Hague',
        sourceUrl: 'https://artsandculture.google.com/asset/girl-with-a-pearl-earring/3QFHLJgXIIftiA',
        imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/1665_Girl_with_a_Pearl_Earring.jpg/1024px-1665_Girl_with_a_Pearl_Earring.jpg',
        userNotes: 'Sublime lapis lazuli ultramarine paired with ochre and a luminous pearl highlight.',
        isFavorite: true,
        userRating: 5,
        compositionAnalysis: {
          palette: [
            { hex: '#16191b', name: 'Glazed Indigo Black', percentage: 48, role: 'surface', rgb: [22, 25, 27] },
            { hex: '#2b5876', name: 'Lapis Lazuli Blue', percentage: 20, role: 'accent', rgb: [43, 88, 118] },
            { hex: '#d9a74a', name: 'Ochre Turban', percentage: 16, role: 'secondary', rgb: [217, 167, 74] },
            { hex: '#f4ebd9', name: 'Pearl Luminescence', percentage: 10, role: 'neutral', rgb: [244, 235, 217] },
            { hex: '#c85a53', name: 'Moist Coral Glaze', percentage: 6, role: 'dominant', rgb: [200, 90, 83] }
          ],
          dominantMood: 'Intimate, enigmatic, exquisitely poised, soft optical purity.',
          compositionType: 'Centered Triangular Portrait with Soft Sfumato Edges',
          visualWeight: 'Perfect central balance with shimmering micro-anchor at the earlobe.',
          colorTemperature: 'balanced',
          contrastLevel: 'high',
          textureFeel: 'Enamelled, vitreous smoothness with soft optical blur and pure specular highlights.',
          spatialRhythm: 'Singular, quiet contemplative focus against infinite dark backdrop.',
          designTakeaways: [
            'Contrast a deep slate-navy surface with pure ultramarine secondary buttons and pearl highlights.',
            'Use subtle rounded micro-elements (pill badges) that catch light like the pearl.',
            'Minimalist layout: let single key focal visual breath inside expansive dark canvas.'
          ],
          typographicResonance: {
            fontPairingSuggestion: 'Cormorant Garamond / Playfair with Inter / Plus Jakarta Sans',
            weightCadence: 'Delicate, refined medium weights with ample whitespace',
            suggestedSerif: 'Playfair Display',
            suggestedSans: 'Plus Jakarta Sans',
            trackingPreference: 'Airy tracking for tags, intimate line spacing for quotes'
          },
          focalPoints: [
            { x: 52, y: 52, label: 'Luminous Pearl Earring Specular Dot', importance: 'primary' },
            { x: 50, y: 38, label: 'Turned Gaze and Sfumato Eyes', importance: 'primary' },
            { x: 44, y: 22, label: 'Ultramarine Blue Headscarf Fold', importance: 'secondary' }
          ]
        }
      },
      {
        id: 'art-4',
        title: 'Joseph the Carpenter',
        artist: 'Georges de La Tour',
        year: '1642',
        medium: 'Oil on canvas',
        movement: 'Baroque / Tenebrism',
        museum: 'Musée du Louvre, Paris',
        sourceUrl: 'https://artsandculture.google.com/asset/joseph-the-carpenter/ZwEp7d_Z43pP3Q',
        imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Georges_de_La_Tour_042.jpg/1024px-Georges_de_La_Tour_042.jpg',
        userNotes: 'A solitary candle illuminating translucent skin, timber grains, and warm intimacy.',
        isFavorite: true,
        userRating: 4,
        compositionAnalysis: {
          palette: [
            { hex: '#140c08', name: 'Charred Timber Umber', percentage: 50, role: 'surface', rgb: [20, 12, 8] },
            { hex: '#e87b28', name: 'Candle Flame Amber', percentage: 22, role: 'accent', rgb: [232, 123, 40] },
            { hex: '#944b1d', name: 'Carved Oak Sienna', percentage: 14, role: 'secondary', rgb: [148, 75, 29] },
            { hex: '#ffd89b', name: 'Translucent Flesh Tint', percentage: 10, role: 'neutral', rgb: [255, 216, 155] },
            { hex: '#402419', name: 'Deep Mahogany', percentage: 4, role: 'dominant', rgb: [64, 36, 25] }
          ],
          dominantMood: 'Meditative serenity, solemn craftsmanship, warm sacred glow.',
          compositionType: 'Radial Candlelight Dispersion with Vertical Interlocking Figures',
          visualWeight: 'Bottom-weighted along the woodworker’s drill and upward illuminated hand.',
          colorTemperature: 'warm',
          contrastLevel: 'dramatic-chiaroscuro',
          textureFeel: 'Raw wood grain, rough wool, and glowing translucent fingertips.',
          spatialRhythm: 'Intimate focal pool fading into total atmospheric darkness.',
          designTakeaways: [
            'Warm amber (#e87b28) as a primary action color against ultra-deep warm espresso (#140c08).',
            'Subtle radial gradient backdrops behind primary metric cards.',
            'Soft border glow transitions (1px amber border with 8px blur at 20% opacity).'
          ],
          typographicResonance: {
            fontPairingSuggestion: 'Cinzel Display with JetBrains Mono code tags',
            weightCadence: 'Grounded, rhythmic, tactile weights',
            suggestedSerif: 'Cinzel',
            suggestedSans: 'Plus Jakarta Sans',
            trackingPreference: 'Generous uppercase kerning for section dividers'
          },
          focalPoints: [
            { x: 62, y: 55, label: 'Child Christ Holding Candle', importance: 'primary' },
            { x: 42, y: 72, label: 'Wood Auger Drilling Timber', importance: 'secondary' },
            { x: 60, y: 48, label: 'Translucent Light Passing Through Fingers', importance: 'primary' }
          ]
        }
      }
    ]
  },
  {
    id: 'ukiyo-e-space',
    name: 'Sublime Solitude & Ukiyo-e Space',
    description: 'Mastery of negative space (Ma), asymmetric balance, indigo gradations (bokashi), and tranquil contemplative rhythm.',
    badge: 'Negative Space & Asymmetry',
    artworks: [
      {
        id: 'art-5',
        title: 'The Great Wave off Kanagawa',
        artist: 'Katsushika Hokusai',
        year: '1831',
        medium: 'Woodblock print; ink and color on paper',
        movement: 'Ukiyo-e / Edo Period',
        museum: 'Tokyo National Museum / Metropolitan Museum of Art',
        sourceUrl: 'https://artsandculture.google.com/asset/the-great-wave-off-kanagawa/fAFjhP81wbgMhQ',
        imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Great_Wave_off_Kanagawa2.jpg/1280px-Great_Wave_off_Kanagawa2.jpg',
        userNotes: 'Dynamic fractal claw curve of Prussian blue framing serene distant Mount Fuji.',
        isFavorite: true,
        userRating: 5,
        compositionAnalysis: {
          palette: [
            { hex: '#1b3b6f', name: 'Prussian Indigo', percentage: 35, role: 'dominant', rgb: [27, 59, 111] },
            { hex: '#e8dcba', name: 'Washi Paper Ecru', percentage: 30, role: 'surface', rgb: [232, 220, 186] },
            { hex: '#4990a4', name: 'Seafoam Bokashi', percentage: 18, role: 'secondary', rgb: [73, 144, 164] },
            { hex: '#fdfaf2', name: 'Crest Spray White', percentage: 12, role: 'neutral', rgb: [253, 250, 242] },
            { hex: '#96704b', name: 'Cedar Boat Ochre', percentage: 5, role: 'accent', rgb: [150, 112, 75] }
          ],
          dominantMood: 'Dynamic majesty, cyclical force of nature versus stoic calm.',
          compositionType: 'Fibonacci Spiral with Yin-Yang Wave Equilibrium',
          visualWeight: 'Left-heavy surging wave encircling centered miniature Mount Fuji.',
          colorTemperature: 'cool',
          contrastLevel: 'high',
          textureFeel: 'Crisp woodblock lineart, wood grain ink absorption, and fine stipple droplets.',
          spatialRhythm: 'Surging dynamic curve terminating into absolute stillness in the background.',
          designTakeaways: [
            'Use asymmetric layout grids: 70% dynamic asymmetric hero container balanced by 30% calm sidebar.',
            'Incorporate Prussian Blue (#1b3b6f) as an authoritative primary brand color with soft washi parchment backgrounds.',
            'Maintain crisp 1px borders inspired by ukiyo-e keyblock lines.'
          ],
          typographicResonance: {
            fontPairingSuggestion: 'Cinzel display paired with Plus Jakarta Sans body',
            weightCadence: 'Bold sculptural titles with ultra-refined body text',
            suggestedSerif: 'Cinzel',
            suggestedSans: 'Plus Jakarta Sans',
            trackingPreference: 'Clean modern tracking with strict mathematical baseline grid'
          },
          focalPoints: [
            { x: 30, y: 40, label: 'Clawing Wave Crest Vortex', importance: 'primary' },
            { x: 52, y: 68, label: 'Mount Fuji Horizon Anchor', importance: 'primary' },
            { x: 62, y: 76, label: 'Slender Oar Boat Cutting Through Trough', importance: 'secondary' }
          ]
        }
      },
      {
        id: 'art-6',
        title: 'Wanderer above the Sea of Fog',
        artist: 'Caspar David Friedrich',
        year: '1818',
        medium: 'Oil on canvas',
        movement: 'Romanticism',
        museum: 'Hamburger Kunsthalle',
        sourceUrl: 'https://artsandculture.google.com/asset/wanderer-above-the-sea-of-fog/bQG1_tF4c8-35g',
        imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Caspar_David_Friedrich_-_Wanderer_above_the_sea_of_fog.jpg/1024px-Caspar_David_Friedrich_-_Wanderer_above_the_sea_of_fog.jpg',
        userNotes: 'Rückenfigur perspective overlooking majestic mountain mist.',
        isFavorite: true,
        userRating: 5,
        compositionAnalysis: {
          palette: [
            { hex: '#1c2226', name: 'Basalt Silhouette Slate', percentage: 32, role: 'dominant', rgb: [28, 34, 38] },
            { hex: '#b5c6d0', name: 'Glacial Fog Azure', percentage: 30, role: 'surface', rgb: [181, 198, 208] },
            { hex: '#637a88', name: 'Alpine Ridge Heather', percentage: 20, role: 'secondary', rgb: [99, 122, 136] },
            { hex: '#e8edf0', name: 'Vapor Mist White', percentage: 12, role: 'neutral', rgb: [232, 237, 240] },
            { hex: '#9b7653', name: 'Lichen Earth Ochre', percentage: 6, role: 'accent', rgb: [155, 118, 83] }
          ],
          dominantMood: 'Sublime existential contemplation, vast scale, introspective solitude.',
          compositionType: 'Central Triangular Figure with Symmetrical V-Valley Horizon',
          visualWeight: 'Anchored central foreground rock tapering into boundless mist.',
          colorTemperature: 'cool',
          contrastLevel: 'high',
          textureFeel: 'Sharp crystalline rock contours contrasting with soft vaporous atmospheric haze.',
          spatialRhythm: 'Expansive breathing space with deep atmospheric perspective planes.',
          designTakeaways: [
            'Embrace expansive negative space and oversized margins for meditative breathing room.',
            'Cool muted slate and fog blues create calm, distraction-free analytical interfaces.',
            'Strong central hero alignment for primary statements, framed by subtle misty borders.'
          ],
          typographicResonance: {
            fontPairingSuggestion: 'Playfair Display Serif with Plus Jakarta Sans Clean Sans',
            weightCadence: 'Philosophical, elegant cadence with generous line spacing',
            suggestedSerif: 'Playfair Display',
            suggestedSans: 'Plus Jakarta Sans',
            trackingPreference: 'Slightly wide letter-spacing for uppercase badges'
          },
          focalPoints: [
            { x: 50, y: 50, label: 'Rückenfigur Traveler Spine & Stance', importance: 'primary' },
            { x: 50, y: 78, label: 'Apex of the Basalt Crag', importance: 'secondary' },
            { x: 74, y: 44, label: 'Distant Jagged Peak Breaking Fog', importance: 'secondary' }
          ]
        }
      },
      {
        id: 'art-7',
        title: 'Zōjōji Temple in Shiba (Snow Scene)',
        artist: 'Hasui Kawase',
        year: '1925',
        medium: 'Woodblock print (Shin-hanga)',
        museum: 'Art Institute of Chicago',
        sourceUrl: 'https://artsandculture.google.com/asset/shiba-zojoji-hasui-kawase/8AFvW81j3kP4kg',
        imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Hasui_Kawase_-_Shiba_Zojoji_1925.jpg/1024px-Hasui_Kawase_-_Shiba_Zojoji_1925.jpg',
        userNotes: 'Vivid vermilion temple gate standing proud against heavy diagonal white blizzard.',
        isFavorite: true,
        userRating: 5,
        compositionAnalysis: {
          palette: [
            { hex: '#c83424', name: 'Vermilion Lacquer Red', percentage: 28, role: 'accent', rgb: [200, 52, 36] },
            { hex: '#222831', name: 'Nocturne Winter Slate', percentage: 32, role: 'surface', rgb: [34, 40, 49] },
            { hex: '#dee4e7', name: 'Fresh Powder Snow', percentage: 24, role: 'neutral', rgb: [222, 228, 231] },
            { hex: '#4b5d67', name: 'Pine Frost Gray', percentage: 12, role: 'secondary', rgb: [75, 93, 103] },
            { hex: '#16191c', name: 'Keyblock Black', percentage: 4, role: 'dominant', rgb: [22, 25, 28] }
          ],
          dominantMood: 'Serene solitude, crisp winter stillness, poignant architectural sanctuary.',
          compositionType: 'Strong Vertical Gate Post Asymmetry with Diagonal Snow Velocity',
          visualWeight: 'Right-skewed monumental vermilion structure grounding floating snow dots.',
          colorTemperature: 'polarizing',
          contrastLevel: 'high',
          textureFeel: 'Matte pigment on hand-pressed mulberry paper with speckled gouache snowflake resist.',
          spatialRhythm: 'Steady rhythmic snowfall creating depth layers in front of structural geometry.',
          designTakeaways: [
            'Use Vermilion Red (#c83424) strictly for high-priority CTA moments against charcoal-slate.',
            'Maintain high contrast ratio (minimum 8:1) between text elements and dark card surfaces.',
            'Subtle dot-matrix or stipple micro-textures on hero banners.'
          ],
          typographicResonance: {
            fontPairingSuggestion: 'Cinzel / Plus Jakarta Sans pairing with geometric precision',
            weightCadence: 'Structured, architectural hierarchy with clean tabular numbers',
            suggestedSerif: 'Cinzel',
            suggestedSans: 'Plus Jakarta Sans',
            trackingPreference: 'Tight numeric spacing with crisp tabular alignment'
          },
          focalPoints: [
            { x: 62, y: 48, label: 'Monumental Crimson Temple Gate', importance: 'primary' },
            { x: 34, y: 78, label: 'Lone Figure with Umbrella in Snow', importance: 'primary' },
            { x: 22, y: 35, label: 'Frosted Evergreen Pine Boughs', importance: 'secondary' }
          ]
        }
      }
    ]
  },
  {
    id: 'bauhaus-modernism',
    name: 'Radical Modernist Geometry & De Stijl',
    description: 'Primary color reduction, asymmetric grid tension, orthogonal harmony, and functional structural purity.',
    badge: 'Geometric Constructivism',
    artworks: [
      {
        id: 'art-8',
        title: 'Composition with Red, Blue and Yellow',
        artist: 'Piet Mondrian',
        year: '1930',
        medium: 'Oil on canvas',
        movement: 'De Stijl / Neoplasticism',
        museum: 'Kunsthaus Zürich',
        sourceUrl: 'https://artsandculture.google.com/asset/composition-with-red-blue-and-yellow/qQE7Q1L31PZowg',
        imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Piet_Mondriaan%2C_1930_-_Mondrian_Composition_II_in_Red%2C_Blue%2C_and_Yellow.jpg/1024px-Piet_Mondriaan%2C_1930_-_Mondrian_Composition_II_in_Red%2C_Blue%2C_and_Yellow.jpg',
        userNotes: 'Dynamic equilibrium: oversized pure red rectangle counterbalanced by tiny intense blue & yellow blocks.',
        isFavorite: true,
        userRating: 5,
        compositionAnalysis: {
          palette: [
            { hex: '#df2929', name: 'Neoplastic Crimson Red', percentage: 38, role: 'accent', rgb: [223, 41, 41] },
            { hex: '#f7f6f2', name: 'Architectural Zinc White', percentage: 36, role: 'surface', rgb: [247, 246, 242] },
            { hex: '#1c285c', name: 'Primary Cobalt Blue', percentage: 10, role: 'secondary', rgb: [28, 40, 92] },
            { hex: '#f3c72b', name: 'Cadmium Lemon Yellow', percentage: 8, role: 'accent', rgb: [243, 199, 43] },
            { hex: '#111111', name: 'Grid Coordinate Black', percentage: 8, role: 'dominant', rgb: [17, 17, 17] }
          ],
          dominantMood: 'Rational equilibrium, rigorous clarity, energetic asymmetric tension.',
          compositionType: 'Orthogonal Asymmetric Grid Matrix',
          visualWeight: 'Upper-right massive red block counterbalanced by bottom-left heavy blue anchor.',
          colorTemperature: 'polarizing',
          contrastLevel: 'high',
          textureFeel: 'Ultra-flat oil matte planes bounded by thick, intentional black vector grid lines.',
          spatialRhythm: 'Precision cadence governed by fractional ratios (golden rectangle variations).',
          designTakeaways: [
            'Strict orthogonal layout: use crisp borders (2px solid #111) without rounded corners (radius: 0px).',
            'Limit color usage to pure functional accents: 1 primary accent per screen to indicate direct interaction.',
            'Asymmetric bento grid layouts where varying card proportions achieve visual harmony.'
          ],
          typographicResonance: {
            fontPairingSuggestion: 'Plus Jakarta Sans Bold display paired with JetBrains Mono data tables',
            weightCadence: 'Geometric, sans-serif dominance with high weight contrasts (800 for headers, 400 for text)',
            suggestedSerif: 'Cinzel (for rare classical counters)',
            suggestedSans: 'Plus Jakarta Sans',
            trackingPreference: 'Zero tracking on headers, strict uppercase section badges'
          },
          focalPoints: [
            { x: 65, y: 35, label: 'Dominant Red Quadrant Block', importance: 'primary' },
            { x: 18, y: 88, label: 'Bottom Blue Counterweight', importance: 'primary' },
            { x: 92, y: 88, label: 'Bottom Right Yellow Accent Pill', importance: 'secondary' }
          ]
        }
      },
      {
        id: 'art-9',
        title: 'Composition VIII',
        artist: 'Wassily Kandinsky',
        year: '1923',
        medium: 'Oil on canvas',
        movement: 'Bauhaus / Abstract Expressionism',
        museum: 'Solomon R. Guggenheim Museum, New York',
        sourceUrl: 'https://artsandculture.google.com/asset/composition-8/ngF8u-w_Fj7yTw',
        imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Vassily_Kandinsky%2C_1923_-_Composition_8%2C_huile_sur_toile%2C_140_x_201_cm%2C_Mus%C3%A9e_Guggenheim%2C_New_York.jpg/1280px-Vassily_Kandinsky%2C_1923_-_Composition_8%2C_huile_sur_toile%2C_140_x_201_cm%2C_Mus%C3%A9e_Guggenheim%2C_New_York.jpg',
        userNotes: 'Synesthetic visual symphony: circles, intersecting diagonals, and cosmic color harmony.',
        isFavorite: true,
        userRating: 5,
        compositionAnalysis: {
          palette: [
            { hex: '#f0ede1', name: 'Cream Canvas Base', percentage: 40, role: 'surface', rgb: [240, 237, 225] },
            { hex: '#222226', name: 'Cosmic Eclipse Black', percentage: 22, role: 'dominant', rgb: [34, 34, 38] },
            { hex: '#d83a2b', name: 'Resonant Solar Scarlet', percentage: 15, role: 'accent', rgb: [216, 58, 43] },
            { hex: '#3168a8', name: 'Harmonic Cobalt', percentage: 13, role: 'secondary', rgb: [49, 104, 168] },
            { hex: '#e2ab32', name: 'Solar Flare Gold', percentage: 10, role: 'accent', rgb: [226, 171, 50] }
          ],
          dominantMood: 'Musical, electric, synesthetic geometry in joyful centrifugal motion.',
          compositionType: 'Centrifugal Multi-Focal Polyphony with Diagonal Vectors',
          visualWeight: 'Upper-left black circle with purple halo commanding gravitational pull.',
          colorTemperature: 'balanced',
          contrastLevel: 'high',
          textureFeel: 'Sharp geometric vector precision interacting with soft atmospheric color halos.',
          spatialRhythm: 'Staccato bursts of circles and sharp chevron needles traversing calm open space.',
          designTakeaways: [
            'Use floating circular status badges and intersecting grid lines for interactive state changes.',
            'Pair structured card frames with whimsical circular micro-interactions (pulse, ripple, glow).',
            'Adopt a musical pacing for UI transitions (snappy 180ms ease-out for hover, smooth 300ms for drawers).'
          ],
          typographicResonance: {
            fontPairingSuggestion: 'Plus Jakarta Sans with JetBrains Mono',
            weightCadence: 'Dynamic, modern, typographic scale with clear mathematical step ratio (1.25)',
            suggestedSerif: 'Playfair Display',
            suggestedSans: 'Plus Jakarta Sans',
            trackingPreference: 'Slightly open letter spacing on numbers and metadata tags'
          },
          focalPoints: [
            { x: 22, y: 28, label: 'Primary Black Sun Circle with Violet Aura', importance: 'primary' },
            { x: 68, y: 42, label: 'Intersecting Diagonal Acute Needle Angles', importance: 'primary' },
            { x: 78, y: 78, label: 'Checkered Chessboard Grid Matrix', importance: 'secondary' }
          ]
        }
      }
    ]
  },
  {
    id: 'impressionist-chroma',
    name: 'Impressionist Chroma & Fleeting Light',
    description: 'Vibrant optical color mixing, broken brushwork, pastel luminosity, and impressionistic atmosphere.',
    badge: 'Chroma & Optical Mixing',
    artworks: [
      {
        id: 'art-10',
        title: 'Water Lilies (Nymphéas)',
        artist: 'Claude Monet',
        year: '1916',
        medium: 'Oil on canvas',
        movement: 'Impressionism',
        museum: 'Musée de l’Orangerie / Musée d’Orsay',
        sourceUrl: 'https://artsandculture.google.com/asset/water-lilies/wAEW8Z1pP4gMwA',
        imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Claude_Monet_-_Water_Lilies_-_Google_Art_Project.jpg/1280px-Claude_Monet_-_Water_Lilies_-_Google_Art_Project.jpg',
        userNotes: 'Boundless reflections of weeping willows, violet skies, and pink blossom clusters in water.',
        isFavorite: true,
        userRating: 5,
        compositionAnalysis: {
          palette: [
            { hex: '#2e4a42', name: 'Reflected Willow Emerald', percentage: 32, role: 'surface', rgb: [46, 74, 66] },
            { hex: '#485675', name: 'Twilight Water Violet', percentage: 28, role: 'dominant', rgb: [72, 86, 117] },
            { hex: '#d98b9e', name: 'Floating Nénuphar Rose', percentage: 18, role: 'accent', rgb: [217, 139, 158] },
            { hex: '#779986', name: 'Sage Lily Pad', percentage: 14, role: 'secondary', rgb: [119, 153, 134] },
            { hex: '#f0d38d', name: 'Dappled Sunlight Butter', percentage: 8, role: 'neutral', rgb: [240, 211, 141] }
          ],
          dominantMood: 'Immersive, tranquil, boundless meditative fluidity without horizon line.',
          compositionType: 'All-Over Field (Horizonless Reflective Surface)',
          visualWeight: 'Evenly dispersed organic clusters floating on fluid color shifts.',
          colorTemperature: 'cool',
          contrastLevel: 'medium',
          textureFeel: 'Layered impasto scumbling, tactile dry-brush crust over glazed wet-in-wet tones.',
          spatialRhythm: 'Gentle horizontal ripples punctuated by floating organic blossom islands.',
          designTakeaways: [
            'Create subtle chromatic gradient backdrops blending deep sage emerald into twilight violet.',
            'Soft blur glassmorphism with delicate pastel rose accent borders (1px border-rose-300/30).',
            'Fluid container layouts with soft generous radii (16px) and gentle hover scale physics.'
          ],
          typographicResonance: {
            fontPairingSuggestion: 'Playfair Display Serif with Plus Jakarta Sans body',
            weightCadence: 'Lyrical, poetic editorial typography with italicized accents',
            suggestedSerif: 'Playfair Display',
            suggestedSans: 'Plus Jakarta Sans',
            trackingPreference: 'Relaxed letter-spacing and generous line-heights (1.7)'
          },
          focalPoints: [
            { x: 35, y: 62, label: 'Luminous Pink Water Lily Island', importance: 'primary' },
            { x: 72, y: 38, label: 'Willow Branch Reflection Depth', importance: 'primary' },
            { x: 55, y: 82, label: 'Sunlight Glint on Deep Pond Basin', importance: 'secondary' }
          ]
        }
      },
      {
        id: 'art-11',
        title: 'Mont Sainte-Victoire',
        artist: 'Paul Cézanne',
        year: '1904',
        medium: 'Oil on canvas',
        movement: 'Post-Impressionism / Proto-Cubism',
        museum: 'Philadelphia Museum of Art',
        sourceUrl: 'https://artsandculture.google.com/asset/mont-sainte-victoire/XgFQ4k0949Q',
        imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Paul_C%C3%A9zanne_-_Mont_Sainte-Victoire_-_Google_Art_Project.jpg/1280px-Paul_C%C3%A9zanne_-_Mont_Sainte-Victoire_-_Google_Art_Project.jpg',
        userNotes: 'Constructed landscape using rhythmic color facets (taches) translating nature into geometric order.',
        isFavorite: true,
        userRating: 4,
        compositionAnalysis: {
          palette: [
            { hex: '#4f6d7a', name: 'Provençal Sky Slate', percentage: 34, role: 'surface', rgb: [79, 109, 122] },
            { hex: '#8a9b68', name: 'Olive Grove Ochre Green', percentage: 26, role: 'dominant', rgb: [138, 155, 104] },
            { hex: '#c88a42', name: 'Terracotta Earth', percentage: 18, role: 'secondary', rgb: [200, 138, 66] },
            { hex: '#dbe3ea', name: 'Limestone Mountain Shimmer', percentage: 14, role: 'neutral', rgb: [219, 227, 234] },
            { hex: '#263b3f', name: 'Pine Shadow Charcoal', percentage: 8, role: 'accent', rgb: [38, 59, 63] }
          ],
          dominantMood: 'Architectonic majesty, structural permanence, reasoned tectonic calm.',
          compositionType: 'Horizontal Tiered Facets with Central Mountain Apex',
          visualWeight: 'Grounded horizontal foreground bands rising to triangular limestone peak.',
          colorTemperature: 'balanced',
          contrastLevel: 'medium',
          textureFeel: 'Blocky, modular brushstroke facets creating structural spatial depth.',
          spatialRhythm: 'Rhythmic repetition of rectangular brush patches building a solid spatial matrix.',
          designTakeaways: [
            'Use modular facet cards with subtle muted border dividers.',
            'Muted olive and terracotta provide an earthy, organic yet highly disciplined color foundation.',
            'Clear horizontal section tiers for complex data displays and dashboards.'
          ],
          typographicResonance: {
            fontPairingSuggestion: 'Playfair Display Serif with JetBrains Mono metrics',
            weightCadence: 'Sturdy, tectonic hierarchy with grounded medium-bold headings',
            suggestedSerif: 'Playfair Display',
            suggestedSans: 'Plus Jakarta Sans',
            trackingPreference: 'Standard clean tracking with strict baseline rhythm'
          },
          focalPoints: [
            { x: 50, y: 35, label: 'Limestone Ridge of Mont Sainte-Victoire', importance: 'primary' },
            { x: 38, y: 72, label: 'Terracotta Farmhouse Geometry', importance: 'secondary' },
            { x: 68, y: 84, label: 'Olive Valley Patchwork Facets', importance: 'secondary' }
          ]
        }
      }
    ]
  },
  {
    id: 'symbolism-gold',
    name: 'Organic Vitalism & Golden Symbolism',
    description: 'Gold leaf ornamentation, organic sinuous curves, sensual symbolism, and lush decorative complexity.',
    badge: 'Art Nouveau & Gold Leaf',
    artworks: [
      {
        id: 'art-12',
        title: 'The Kiss (Lovers)',
        artist: 'Gustav Klimt',
        year: '1908',
        medium: 'Oil and gold leaf on canvas',
        movement: 'Vienna Secession / Art Nouveau',
        museum: 'Österreichische Galerie Belvedere, Vienna',
        sourceUrl: 'https://artsandculture.google.com/asset/the-kiss/HQE4qZ7m0_M7lg',
        imageUrl: 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/The_Kiss_-_Gustav_Klimt_-_Google_Cultural_Institute.jpg/1024px-The_Kiss_-_Gustav_Klimt_-_Google_Cultural_Institute.jpg',
        userNotes: 'A golden aura cloaking two figures on a floral cliff edge with geometric gold patterns.',
        isFavorite: true,
        userRating: 5,
        compositionAnalysis: {
          palette: [
            { hex: '#d4af37', name: 'Florentine Gold Leaf', percentage: 42, role: 'accent', rgb: [212, 175, 55] },
            { hex: '#262015', name: 'Gilded Espresso Dark', percentage: 26, role: 'surface', rgb: [38, 32, 21] },
            { hex: '#e8cb75', name: 'Luminous Foil Amber', percentage: 16, role: 'secondary', rgb: [232, 203, 117] },
            { hex: '#486851', name: 'Meadow Moss Green', percentage: 10, role: 'neutral', rgb: [72, 104, 81] },
            { hex: '#8a2be2', name: 'Secessionist Violet', percentage: 6, role: 'dominant', rgb: [138, 43, 226] }
          ],
          dominantMood: 'Ecstatic transcendence, luxurious intimacy, timeless golden splendor.',
          compositionType: 'Vertical Monolithic Totem on Sinuous Floral Shelf',
          visualWeight: 'Centered shimmering gold mass contrasted against ethereal dark background.',
          colorTemperature: 'warm',
          contrastLevel: 'high',
          textureFeel: 'Embossed gold leaf, spiraling filigree, and tessellated black-and-white rectangle inlays.',
          spatialRhythm: 'Intricate decorative micro-patterns contained within a bold, iconic macro-silhouette.',
          designTakeaways: [
            'Gold Leaf (#d4af37) as a signature luxury highlight, button borders, and premium accents.',
            'Deep warm espresso surfaces (#1a150e) accented by glowing 1px gold borders.',
            'Micro-ornamentation: small geometric badges and pill tags with metallic sheen.'
          ],
          typographicResonance: {
            fontPairingSuggestion: 'Cinzel Decorative Display with Plus Jakarta Sans body',
            weightCadence: 'Opulent, regal display titles with refined modern readability',
            suggestedSerif: 'Cinzel / Playfair Display',
            suggestedSans: 'Plus Jakarta Sans',
            trackingPreference: 'Generous letter-spacing (+0.08em) on all uppercase headers'
          },
          focalPoints: [
            { x: 52, y: 32, label: 'Embracing Lovers Face & Golden Crown', importance: 'primary' },
            { x: 44, y: 55, label: 'Rectangular Geometric Robe Patterns (Masculine)', importance: 'secondary' },
            { x: 58, y: 65, label: 'Concentric Spiral & Floral Tessellations (Feminine)', importance: 'secondary' }
          ]
        }
      }
    ]
  }
];

export const SAMPLE_DESIGN_SYSTEM = {
  title: 'The Luminous Threshold Design System',
  subtitle: 'Synthesized from Compositional & Chromatic Analysis of Google Arts & Culture Masterpieces',
  curatorialInspiration: 'Baroque Chiaroscuro & Tenebrist Luminance',
  generatedAt: new Date().toISOString(),
  markdownContent: `# The Luminous Threshold Design System
> **Curatorial Genesis:** Synthesized from compositional, chromatic, and structural analysis of Google Arts & Culture masterpieces including *The Night Watch* (Rembrandt), *The Calling of St. Matthew* (Caravaggio), *Girl with a Pearl Earring* (Vermeer), and *Joseph the Carpenter* (Georges de La Tour).

---

## 1. Executive Philosophy & Thematic Manifesto

The **Luminous Threshold** design system is founded upon the timeless visual principles of classical European tenebrism, chiaroscuro, and radiant specular focal points:

- **The Law of the Threshold:** 60% deep obsidian canvas, 30% structural midtones, and 10% luminous golden focal points.
- **Asymmetric Gravity:** Layouts leverage calculated asymmetric focal weights to direct user attention naturally without visual friction.
- **Directional Light Vectors:** Every shadow and highlight represents an intentional physical light vector that establishes spatial hierarchy.

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

## 5. Curatorial Laws: Dos and Don'ts

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
        { name: 'sm', rem: '0.5rem', px: 8 },
        { name: 'md', rem: '1rem', px: 16 },
        { name: 'lg', rem: '1.5rem', px: 24 },
        { name: 'xl', rem: '2rem', px: 32 },
        { name: '2xl', rem: '3rem', px: 48 },
        { name: '3xl', rem: '4rem', px: 64 }
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
