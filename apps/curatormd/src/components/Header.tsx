import React from 'react';
import { Palette, Sparkles, FileText, Layers, FolderPlus, Compass, BookOpen, Share2 } from 'lucide-react';

interface HeaderProps {
  activeTab: 'artworks' | 'curation' | 'design-md' | 'sandbox';
  setActiveTab: (tab: 'artworks' | 'curation' | 'design-md' | 'sandbox') => void;
  artworksCount: number;
  analyzedCount: number;
  themesCount: number;
  hasDesignSystem: boolean;
  onOpenImporter: () => void;
  onCurateThemes: () => void;
  onGenerateDesignSystem: () => void;
  isCurating?: boolean;
  isGenerating?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  activeTab,
  setActiveTab,
  artworksCount,
  analyzedCount,
  themesCount,
  hasDesignSystem,
  onOpenImporter,
  onCurateThemes,
  onGenerateDesignSystem,
  isCurating,
  isGenerating
}) => {
  return (
    <header className="sticky top-0 z-40 bg-[#FDFBF7]/95 backdrop-blur-md border-b-2 border-[#1A1A1A]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between py-4 sm:py-5">
          {/* Logo and Brand */}
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 bg-[#1A1A1A] text-[#FDFBF7] flex items-center justify-center border border-[#1A1A1A] shadow-sm">
              <Compass className="w-5 h-5 text-[#D4AF37]" />
            </div>
            <div>
              <p className="text-[9px] uppercase tracking-[0.3em] font-sans text-[#888] hidden sm:block">
                Automated Art Intelligence &bull; Google Arts &amp; Culture
              </p>
              <div className="flex items-baseline gap-2.5">
                <h1 className="font-serif text-2xl sm:text-3xl font-light tracking-tight italic text-[#1A1A1A]">
                  Curator<span className="font-serif font-bold text-[#D4AF37] not-italic">MD</span>
                </h1>
                <span className="px-2 py-0.5 text-[9px] uppercase font-sans font-bold tracking-widest bg-[#1A1A1A] text-[#FDFBF7]">
                  v1.0.4
                </span>
              </div>
            </div>
          </div>

          {/* Navigation Tabs (Editorial style) */}
          <nav className="hidden md:flex items-center space-x-6 border-x border-[#EBE8E0] px-6">
            <button
              id="tab-artworks-nav"
              onClick={() => setActiveTab('artworks')}
              className={`flex items-center gap-2 py-1 text-[10px] uppercase font-sans tracking-[0.25em] transition-all cursor-pointer ${
                activeTab === 'artworks'
                  ? 'text-[#1A1A1A] font-bold border-b-2 border-[#1A1A1A]'
                  : 'text-[#888] hover:text-[#1A1A1A]'
              }`}
            >
              <Palette className="w-3.5 h-3.5" />
              <span>01 / Artworks</span>
              <span className={`text-[9px] px-1.5 py-0.2 font-mono ${activeTab === 'artworks' ? 'bg-[#1A1A1A] text-[#FDFBF7]' : 'bg-[#EBE8E0] text-[#555]'}`}>
                {artworksCount}
              </span>
            </button>

            <button
              id="tab-curation-nav"
              onClick={() => setActiveTab('curation')}
              className={`flex items-center gap-2 py-1 text-[10px] uppercase font-sans tracking-[0.25em] transition-all cursor-pointer ${
                activeTab === 'curation'
                  ? 'text-[#1A1A1A] font-bold border-b-2 border-[#1A1A1A]'
                  : 'text-[#888] hover:text-[#1A1A1A]'
              }`}
            >
              <Layers className="w-3.5 h-3.5" />
              <span>02 / Curation</span>
              <span className={`text-[9px] px-1.5 py-0.2 font-mono ${activeTab === 'curation' ? 'bg-[#1A1A1A] text-[#FDFBF7]' : 'bg-[#EBE8E0] text-[#555]'}`}>
                {themesCount}
              </span>
            </button>

            <button
              id="tab-designmd-nav"
              onClick={() => setActiveTab('design-md')}
              className={`flex items-center gap-2 py-1 text-[10px] uppercase font-sans tracking-[0.25em] transition-all cursor-pointer ${
                activeTab === 'design-md'
                  ? 'text-[#1A1A1A] font-bold border-b-2 border-[#1A1A1A]'
                  : 'text-[#888] hover:text-[#1A1A1A]'
              }`}
            >
              <FileText className="w-3.5 h-3.5" />
              <span>03 / design.md</span>
              {hasDesignSystem && (
                <span className="w-1.5 h-1.5 rounded-full bg-[#D4AF37]"></span>
              )}
            </button>

            <button
              id="tab-sandbox-nav"
              onClick={() => setActiveTab('sandbox')}
              className={`flex items-center gap-2 py-1 text-[10px] uppercase font-sans tracking-[0.25em] transition-all cursor-pointer ${
                activeTab === 'sandbox'
                  ? 'text-[#1A1A1A] font-bold border-b-2 border-[#1A1A1A]'
                  : 'text-[#888] hover:text-[#1A1A1A]'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>04 / Sandbox</span>
            </button>
          </nav>

          {/* Quick Actions */}
          <div className="flex items-center gap-3">
            <button
              id="btn-import-sheet"
              onClick={onOpenImporter}
              className="flex items-center gap-2 px-4 py-2 border border-[#1A1A1A] text-[#1A1A1A] text-[10px] uppercase tracking-[0.25em] font-sans hover:bg-[#F0EEE6] transition-colors cursor-pointer"
            >
              <FolderPlus className="w-3.5 h-3.5 text-[#1A1A1A]" />
              <span className="hidden sm:inline">Sync Sheet</span>
              <span className="sm:hidden">Sync</span>
            </button>

            {activeTab === 'artworks' && (
              <button
                id="btn-curate-themes-header"
                onClick={onCurateThemes}
                disabled={artworksCount === 0 || isCurating}
                className="flex items-center gap-2 px-5 py-2 bg-[#1A1A1A] text-[#FDFBF7] text-[10px] uppercase tracking-[0.25em] font-sans hover:bg-[#333] disabled:opacity-50 transition-colors shadow-sm cursor-pointer"
              >
                <Sparkles className={`w-3.5 h-3.5 text-[#D4AF37] ${isCurating ? 'animate-spin' : ''}`} />
                <span>{isCurating ? 'Curating...' : 'Curate Themes'}</span>
              </button>
            )}

            {(activeTab === 'curation' || activeTab === 'design-md' || activeTab === 'sandbox') && (
              <button
                id="btn-generate-designmd-header"
                onClick={onGenerateDesignSystem}
                disabled={artworksCount === 0 || isGenerating}
                className="flex items-center gap-2 px-5 py-2 bg-[#1A1A1A] text-[#FDFBF7] text-[10px] uppercase tracking-[0.25em] font-sans hover:bg-[#333] disabled:opacity-50 transition-colors shadow-sm cursor-pointer"
              >
                <Sparkles className={`w-3.5 h-3.5 text-[#D4AF37] ${isGenerating ? 'animate-spin' : ''}`} />
                <span>{isGenerating ? 'Synthesizing...' : 'Generate design.md'}</span>
              </button>
            )}
          </div>
        </div>

        {/* Mobile Navigation bar */}
        <div className="flex md:hidden items-center justify-around py-2.5 border-t border-[#EBE8E0]">
          <button
            onClick={() => setActiveTab('artworks')}
            className={`flex flex-col items-center gap-1 text-[10px] font-sans tracking-wider uppercase ${activeTab === 'artworks' ? 'text-[#1A1A1A] font-bold border-b border-[#1A1A1A]' : 'text-[#888]'}`}
          >
            <span>01 / Artworks ({artworksCount})</span>
          </button>
          <button
            onClick={() => setActiveTab('curation')}
            className={`flex flex-col items-center gap-1 text-[10px] font-sans tracking-wider uppercase ${activeTab === 'curation' ? 'text-[#1A1A1A] font-bold border-b border-[#1A1A1A]' : 'text-[#888]'}`}
          >
            <span>02 / Curation ({themesCount})</span>
          </button>
          <button
            onClick={() => setActiveTab('design-md')}
            className={`flex flex-col items-center gap-1 text-[10px] font-sans tracking-wider uppercase ${activeTab === 'design-md' ? 'text-[#1A1A1A] font-bold border-b border-[#1A1A1A]' : 'text-[#888]'}`}
          >
            <span>03 / design.md</span>
          </button>
          <button
            onClick={() => setActiveTab('sandbox')}
            className={`flex flex-col items-center gap-1 text-[10px] font-sans tracking-wider uppercase ${activeTab === 'sandbox' ? 'text-[#1A1A1A] font-bold border-b border-[#1A1A1A]' : 'text-[#888]'}`}
          >
            <span>04 / Sandbox</span>
          </button>
        </div>
      </div>
    </header>
  );
};
