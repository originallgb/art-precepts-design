import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { Header } from './components/Header';
import { ArtworkGallery } from './components/ArtworkGallery';
import { ArtworkInspectorModal } from './components/ArtworkInspectorModal';
import { SheetImporterModal } from './components/SheetImporterModal';
import { CuratorialThemesView } from './components/CuratorialThemesView';
import { DesignSystemStudio } from './components/DesignSystemStudio';
import { LiveComponentSandbox } from './components/LiveComponentSandbox';
import { Artwork, CuratorialTheme, GeneratedDesignSystem, PresetCollection } from './types';
import { PRESET_COLLECTIONS, SAMPLE_DESIGN_SYSTEM } from './data/presets';
import { Sparkles, Check, AlertCircle, Info } from 'lucide-react';

export function App() {
  // Initialize with the first curated preset
  const defaultPreset = PRESET_COLLECTIONS[0];
  const [artworks, setArtworks] = useState<Artwork[]>(defaultPreset.artworks);
  const [themes, setThemes] = useState<CuratorialTheme[]>([]);
  const [selectedTheme, setSelectedTheme] = useState<CuratorialTheme | null>(null);
  const [designSystem, setDesignSystem] = useState<GeneratedDesignSystem | null>(SAMPLE_DESIGN_SYSTEM);

  // Navigation and Modals
  const [activeTab, setActiveTab] = useState<'artworks' | 'curation' | 'design-md' | 'sandbox'>('artworks');
  const [selectedArtwork, setSelectedArtwork] = useState<Artwork | null>(null);
  const [isImporterOpen, setIsImporterOpen] = useState(false);

  // Loading states
  const [isCurating, setIsCurating] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isAnalyzingAll, setIsAnalyzingAll] = useState(false);

  // Toast notifications
  const [toast, setToast] = useState<{ message: string; type: 'success' | 'info' | 'error' } | null>(null);

  const showToast = (message: string, type: 'success' | 'info' | 'error' = 'success') => {
    setToast({ message, type });
    setTimeout(() => {
      setToast(null);
    }, 3500);
  };

  // Initial curate if preset has artworks
  useEffect(() => {
    // Generate initial curatorial themes from default preset
    if (themes.length === 0 && artworks.length > 0) {
      handleCurateThemes(false);
    }
  }, []);

  // 1. Single artwork analysis
  const handleAnalyzeArtwork = async (artwork: Artwork) => {
    // Update artwork analyzing status
    setArtworks(prev => prev.map(a => a.id === artwork.id ? { ...a, analyzing: true } : a));
    if (selectedArtwork?.id === artwork.id) {
      setSelectedArtwork(prev => prev ? { ...prev, analyzing: true } : null);
    }

    try {
      const res = await fetch('/api/analyze-artwork', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ artwork }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to analyze artwork');

      if (data.analysis) {
        setArtworks(prev => prev.map(a => a.id === artwork.id ? { ...a, compositionAnalysis: data.analysis, analyzing: false } : a));
        if (selectedArtwork?.id === artwork.id) {
          setSelectedArtwork(prev => prev ? { ...prev, compositionAnalysis: data.analysis, analyzing: false } : null);
        }
        showToast(`Analyzed "${artwork.title}" visual composition`, 'success');
      }
    } catch (err: any) {
      console.error('Analysis error:', err);
      showToast(err.message || 'Error analyzing artwork', 'error');
      setArtworks(prev => prev.map(a => a.id === artwork.id ? { ...a, analyzing: false } : a));
      if (selectedArtwork?.id === artwork.id) {
        setSelectedArtwork(prev => prev ? { ...prev, analyzing: false } : null);
      }
    }
  };

  // 2. Batch analyze all unanalyzed artworks
  const handleAnalyzeAll = async () => {
    const unanalyzed = artworks.filter(a => !a.compositionAnalysis);
    if (unanalyzed.length === 0) {
      showToast('All artworks are already analyzed!', 'info');
      return;
    }

    setIsAnalyzingAll(true);
    showToast(`Analyzing ${unanalyzed.length} artworks with Gemini...`, 'info');

    for (const art of unanalyzed) {
      await handleAnalyzeArtwork(art);
    }

    setIsAnalyzingAll(false);
    showToast('Batch visual analysis complete!', 'success');
  };

  // 3. Curate non-obvious collections
  const handleCurateThemes = async (switchTab = true) => {
    if (artworks.length === 0) {
      showToast('Add artworks first to curate collections.', 'error');
      return;
    }

    setIsCurating(true);
    try {
      const res = await fetch('/api/curate-collections', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ artworks }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to curate themes');

      if (data.themes && data.themes.length > 0) {
        setThemes(data.themes);
        if (switchTab) {
          setActiveTab('curation');
          showToast(`Curated ${data.themes.length} non-obvious thematic collections!`, 'success');
        }
      }
    } catch (err: any) {
      console.error('Curation error:', err);
      showToast(err.message || 'Error curating themes', 'error');
    } finally {
      setIsCurating(false);
    }
  };

  // 4. Generate design.md and design tokens
  const handleGenerateDesignSystem = async (theme?: CuratorialTheme) => {
    if (artworks.length === 0) {
      showToast('Add artworks first before synthesizing design.md.', 'error');
      return;
    }

    setIsGenerating(true);
    const targetTheme = theme || selectedTheme || themes[0];
    const systemName = targetTheme ? `${targetTheme.title.split(':')[0]} Design System` : 'CuratorMD Design System';

    try {
      const res = await fetch('/api/generate-design-system', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          artworks,
          selectedTheme: targetTheme,
          systemName,
          projectContext: 'Production web application & editorial design tokens'
        }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Failed to generate design system');

      if (data.designSystem) {
        setDesignSystem(data.designSystem);
        setActiveTab('design-md');
        showToast(`Synthesized ${data.designSystem.title}!`, 'success');

        // Confetti celebration
        try {
          confetti({
            particleCount: 80,
            spread: 70,
            origin: { y: 0.6 },
            colors: ['#d4af37', '#8a4b28', '#f2f4f8', '#2b5876']
          });
        } catch {
          // ignore if canvas unavailable
        }
      }
    } catch (err: any) {
      console.error('Generation error:', err);
      showToast(err.message || 'Error synthesizing design system', 'error');
    } finally {
      setIsGenerating(false);
    }
  };

  // 5. Toggle favorite
  const handleToggleFavorite = (id: string) => {
    setArtworks(prev => prev.map(a => a.id === id ? { ...a, isFavorite: !a.isFavorite } : a));
  };

  // 6. Import custom artworks
  const handleImportArtworks = (newArtworks: Artwork[], collectionName = 'Imported Collection') => {
    setArtworks(prev => {
      const existingIds = new Set(prev.map(a => a.id));
      const fresh = newArtworks.filter(a => !existingIds.has(a.id));
      return [...fresh, ...prev];
    });
    showToast(`Added ${newArtworks.length} pieces from ${collectionName}!`, 'success');
  };

  // 7. Load preset pack
  const handleSelectPreset = (preset: PresetCollection) => {
    setArtworks(preset.artworks);
    showToast(`Loaded ${preset.name} (${preset.artworks.length} pieces)`, 'success');
    // Re-curate themes for the new preset
    setTimeout(() => {
      handleCurateThemes(false);
    }, 200);
  };

  const analyzedCount = artworks.filter(a => Boolean(a.compositionAnalysis)).length;

  return (
    <div className="min-h-screen bg-[#FDFBF7] text-[#1A1A1A] flex flex-col font-serif selection:bg-[#D4AF37]/30 selection:text-[#1A1A1A]">
      {/* App Navigation Header */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        artworksCount={artworks.length}
        analyzedCount={analyzedCount}
        themesCount={themes.length}
        hasDesignSystem={Boolean(designSystem)}
        onOpenImporter={() => setIsImporterOpen(true)}
        onCurateThemes={() => handleCurateThemes(true)}
        onGenerateDesignSystem={() => handleGenerateDesignSystem()}
        isCurating={isCurating}
        isGenerating={isGenerating}
      />

      {/* Main App Canvas */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* TAB 1: ARTWORKS GALLERY */}
        {activeTab === 'artworks' && (
          <ArtworkGallery
            artworks={artworks}
            onSelectArtwork={(art) => setSelectedArtwork(art)}
            onAnalyzeArtwork={handleAnalyzeArtwork}
            onToggleFavorite={handleToggleFavorite}
            onAnalyzeAll={handleAnalyzeAll}
            onOpenImporter={() => setIsImporterOpen(true)}
            isAnalyzingAll={isAnalyzingAll}
          />
        )}

        {/* TAB 2: CURATORIAL THEMES */}
        {activeTab === 'curation' && (
          <CuratorialThemesView
            themes={themes}
            artworks={artworks}
            onSelectThemeForDesign={(theme) => {
              setSelectedTheme(theme);
              handleGenerateDesignSystem(theme);
            }}
            onReCurate={() => handleCurateThemes(true)}
            isCurating={isCurating}
          />
        )}

        {/* TAB 3: DESIGN.MD STUDIO */}
        {activeTab === 'design-md' && designSystem && (
          <DesignSystemStudio
            designSystem={designSystem}
            onRegenerate={() => handleGenerateDesignSystem()}
            isGenerating={isGenerating}
          />
        )}

        {/* TAB 4: LIVE UI SANDBOX */}
        {activeTab === 'sandbox' && designSystem?.tokens && (
          <LiveComponentSandbox
            tokens={designSystem.tokens}
            systemTitle={designSystem.title}
          />
        )}
      </main>

      {/* Footer */}
      <footer className="border-t-2 border-[#1A1A1A] bg-[#FDFBF7] py-6 text-center text-xs text-[#555]">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="font-serif italic text-sm text-[#1A1A1A]">
            CuratorMD <span className="font-sans font-normal not-italic text-xs text-[#888]">&bull; Translating Google Arts &amp; Culture into production-ready </span>
            <code className="bg-[#1A1A1A] text-[#FDFBF7] px-1.5 py-0.5 rounded-xs font-mono text-[11px]">design.md</code>
          </p>
          <div className="flex items-center space-x-4">
            <span className="text-[10px] uppercase tracking-[0.2em] font-sans text-[#888]">Curation Engine v.1.0.4</span>
            <span className="text-[10px] uppercase tracking-[0.3em] font-sans font-bold text-[#1A1A1A] border-b border-[#1A1A1A]">Multimodal Intelligence</span>
          </div>
        </div>
      </footer>

      {/* MODAL: Artwork Inspector */}
      {selectedArtwork && (
        <ArtworkInspectorModal
          artwork={selectedArtwork}
          onClose={() => setSelectedArtwork(null)}
          onAnalyze={handleAnalyzeArtwork}
          isAnalyzing={selectedArtwork.analyzing}
        />
      )}

      {/* MODAL: Sheet & Arts Link Importer */}
      <SheetImporterModal
        isOpen={isImporterOpen}
        onClose={() => setIsImporterOpen(false)}
        onImportArtworks={handleImportArtworks}
        onSelectPreset={handleSelectPreset}
      />

      {/* TOAST NOTIFICATION */}
      {toast && (
        <div className="fixed bottom-6 right-6 z-50 animate-in slide-in-from-bottom-5 duration-200">
          <div className={`flex items-center gap-2.5 px-5 py-3 shadow-xl border text-xs font-sans tracking-wide ${
            toast.type === 'error'
              ? 'bg-[#1A1A1A] border-red-700 text-red-200'
              : toast.type === 'info'
              ? 'bg-[#FFFFFF] border-[#1A1A1A] text-[#1A1A1A]'
              : 'bg-[#1A1A1A] border-[#D4AF37] text-[#FDFBF7]'
          }`}>
            {toast.type === 'error' ? (
              <AlertCircle className="w-4 h-4 text-red-400 shrink-0" />
            ) : toast.type === 'info' ? (
              <Info className="w-4 h-4 text-[#D4AF37] shrink-0" />
            ) : (
              <div className="w-2 h-2 rounded-full bg-[#D4AF37] shrink-0" />
            )}
            <span className="font-medium">{toast.message}</span>
          </div>
        </div>
      )}
    </div>
  );
}
export default App;
