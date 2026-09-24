export interface PaletteSwatch {
  hex: string;
  name: string;
  percentage: number;
  role: 'dominant' | 'secondary' | 'accent' | 'neutral' | 'surface';
  rgb: [number, number, number];
}

export interface CompositionAnalysis {
  palette: PaletteSwatch[];
  dominantMood: string;
  compositionType: string;
  visualWeight: string;
  colorTemperature: 'warm' | 'cool' | 'balanced' | 'polarizing';
  contrastLevel: 'high' | 'medium' | 'low' | 'dramatic-chiaroscuro';
  textureFeel: string;
  spatialRhythm: string;
  designTakeaways: string[];
  typographicResonance: {
    fontPairingSuggestion: string;
    weightCadence: string;
    suggestedSerif: string;
    suggestedSans: string;
    trackingPreference: string;
  };
  focalPoints: {
    x: number; // percentage 0-100
    y: number; // percentage 0-100
    label: string;
    importance: 'primary' | 'secondary' | 'counter-balance';
  }[];
}

export interface Artwork {
  id: string;
  title: string;
  artist: string;
  year?: string;
  medium?: string;
  movement?: string;
  museum?: string;
  sourceUrl: string;
  imageUrl: string;
  userNotes?: string;
  isFavorite?: boolean;
  userRating?: number; // 1-5
  compositionAnalysis?: CompositionAnalysis;
  analyzing?: boolean;
  error?: string;
}

export interface CuratorialTheme {
  id: string;
  title: string;
  subtitle: string;
  curatorialEssay: string;
  aestheticPhilosophy: string;
  artworkIds: string[];
  keywords: string[];
  designTranslation: {
    visualTone: string;
    recommendedUseCases: string[];
    keyColors: string[];
    layoutStyle: string;
    interactionPacing: string;
  };
}

export interface DesignTokens {
  colors: {
    brandPrimary: string;
    brandSecondary: string;
    brandAccent: string;
    surfaceBase: string;
    surfaceElevated: string;
    surfaceOverlay: string;
    textPrimary: string;
    textSecondary: string;
    textMuted: string;
    borderSubtle: string;
    borderFocus: string;
  };
  paletteVariants: {
    name: string;
    hex: string;
    tokenName: string;
    usage: string;
    wcagContrastRatio?: number;
  }[];
  typography: {
    displayFont: string;
    bodyFont: string;
    monoFont: string;
    baseFontSize: string;
    scaleRatio: number;
    headingLineHeight: string;
    bodyLineHeight: string;
  };
  spacing: {
    scale: { name: string; rem: string; px: number }[];
    containerPadding: string;
    sectionGap: string;
  };
  radii: {
    buttonRadius: string;
    cardRadius: string;
    tagRadius: string;
  };
  elevation: {
    cardShadow: string;
    dropdownShadow: string;
    modalShadow: string;
  };
  rules: {
    dos: string[];
    donts: string[];
  };
}

export interface DesignSystemGuideline {
  title: string;
  subtitle: string;
  curatorialInspiration: string;
  generatedAt: string;
  markdownContent: string;
  tokens: DesignTokens;
}

export type GeneratedDesignSystem = DesignSystemGuideline;

export interface PresetCollection {
  id: string;
  name: string;
  description: string;
  badge: string;
  artworks: Artwork[];
}
