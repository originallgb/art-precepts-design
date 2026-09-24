import React from 'react';
import { Layers, Sparkles, BookOpen, ArrowRight, Tag, Palette, CheckCircle2, RefreshCw } from 'lucide-react';
import { CuratorialTheme, Artwork } from '../types';

interface CuratorialThemesViewProps {
  themes: CuratorialTheme[];
  artworks: Artwork[];
  onSelectThemeForDesign: (theme: CuratorialTheme) => void;
  onReCurate: () => void;
  isCurating?: boolean;
}

export const CuratorialThemesView: React.FC<CuratorialThemesViewProps> = ({
  themes,
  artworks,
  onSelectThemeForDesign,
  onReCurate,
  isCurating
}) => {
  // Map artwork id to full artwork object
  const artworkMap = new Map<string, Artwork>(artworks.map(a => [a.id, a]));

  return (
    <div className="space-y-6">
      {/* Curation Introduction Banner */}
      <div className="bg-[#FFFFFF] border-2 border-[#1A1A1A] p-6 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <span className="text-[10px] uppercase tracking-[0.3em] font-sans font-semibold text-[#1A1A1A] border-l-4 border-[#D4AF37] pl-3">
              Curatorial Intelligence &bull; Synthesis
            </span>
            <span className="text-[10px] uppercase font-mono tracking-widest bg-[#F9F8F4] border border-[#EBE8E0] px-2 py-0.5 text-[#555]">
              {themes.length} CROSS-CUTTING COLLECTIONS
            </span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-light tracking-tight italic text-[#1A1A1A]">
            Non-Obvious Curatorial Collections
          </h1>
          <p className="text-xs font-serif italic text-[#555] max-w-2xl mt-1 leading-relaxed">
            Rather than classifying by mere epoch or medium, these collections illuminate unexpected conceptual dialogues, tension, chromatic harmonies, and spatial philosophies across your favorited pieces.
          </p>
        </div>

        <button
          id="btn-recurate-themes"
          onClick={onReCurate}
          disabled={isCurating}
          className="flex items-center justify-center gap-2 px-6 py-3 bg-[#1A1A1A] text-[#FDFBF7] text-[10px] uppercase tracking-[0.3em] font-sans hover:bg-[#333] disabled:opacity-50 transition-colors shadow-sm cursor-pointer shrink-0"
        >
          <Sparkles className={`w-3.5 h-3.5 text-[#D4AF37] ${isCurating ? 'animate-spin' : ''}`} />
          <span>{isCurating ? 'Synthesizing...' : 'Re-Curate Collections'}</span>
        </button>
      </div>

      {/* Empty state */}
      {themes.length === 0 && (
        <div className="bg-[#FFFFFF] border border-[#EBE8E0] p-12 text-center space-y-3">
          <div className="w-12 h-12 bg-[#F9F8F4] border border-[#1A1A1A] flex items-center justify-center text-[#1A1A1A] mx-auto">
            <Layers className="w-5 h-5 text-[#D4AF37]" />
          </div>
          <h3 className="font-serif text-lg font-bold text-[#1A1A1A]">
            No Curatorial Themes Formed Yet
          </h3>
          <p className="text-xs text-[#777] max-w-md mx-auto italic font-serif">
            Click "Curate Themes" to let Gemini discover the hidden structural, emotional, and chromatic synergies among your cataloged artworks.
          </p>
          <button
            onClick={onReCurate}
            disabled={isCurating}
            className="inline-flex items-center gap-2 px-6 py-2.5 bg-[#1A1A1A] text-[#FDFBF7] text-[10px] uppercase tracking-[0.3em] font-sans hover:bg-[#333] transition-colors mt-2"
          >
            <Sparkles className="w-3.5 h-3.5 text-[#D4AF37]" />
            <span>Curate Now</span>
          </button>
        </div>
      )}

      {/* Curatorial Themes Cards */}
      <div className="space-y-6">
        {themes.map((theme, idx) => {
          const matchedArtworks = theme.artworkIds
            .map(id => artworkMap.get(id))
            .filter((a): a is Artwork => Boolean(a));

          return (
            <div
              key={theme.id || idx}
              className="bg-[#FFFFFF] border border-[#1A1A1A] hover:border-[#D4AF37] p-6 shadow-sm transition-colors space-y-6"
            >
              {/* Header */}
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-[#EBE8E0]">
                <div>
                  <div className="flex items-center gap-2 mb-1.5">
                    <span className="text-[9px] uppercase font-mono tracking-widest px-2.5 py-0.5 bg-[#1A1A1A] text-[#FDFBF7]">
                      COLLECTION 0{idx + 1}
                    </span>
                    <span className="text-xs text-[#777] font-serif italic">
                      {matchedArtworks.length} paired compositions
                    </span>
                  </div>
                  <h2 className="font-serif text-2xl font-light italic text-[#1A1A1A]">
                    {theme.title}
                  </h2>
                  <p className="text-xs font-serif italic text-[#D4AF37] font-semibold mt-0.5">
                    {theme.subtitle}
                  </p>
                </div>

                <button
                  id={`btn-generate-from-theme-${idx}`}
                  onClick={() => onSelectThemeForDesign(theme)}
                  className="flex items-center gap-2 px-5 py-2.5 bg-[#1A1A1A] text-[#FDFBF7] text-[10px] uppercase tracking-[0.25em] font-sans hover:bg-[#333] transition-colors shadow-xs cursor-pointer shrink-0"
                >
                  <Sparkles className="w-3.5 h-3.5 text-[#D4AF37]" />
                  <span>Synthesize design.md</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>

              {/* Curatorial Essay and Aesthetic Law */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <div className="lg:col-span-7 space-y-4">
                  <div className="flex items-center gap-2 text-[#1A1A1A] border-b border-[#EBE8E0] pb-1.5">
                    <BookOpen className="w-4 h-4 text-[#D4AF37]" />
                    <h3 className="text-[10px] font-sans uppercase tracking-[0.25em] font-bold text-[#1A1A1A]">
                      Curatorial Essay &amp; Visual Dialogue
                    </h3>
                  </div>
                  <div className="text-xs font-serif text-[#444] leading-relaxed space-y-2 whitespace-pre-line">
                    {theme.curatorialEssay}
                  </div>

                  {/* Philosophy Quote */}
                  <div className="p-4 bg-[#F9F8F4] border-l-4 border-[#D4AF37] text-xs font-serif italic text-[#1A1A1A]">
                    "{theme.aestheticPhilosophy}"
                  </div>
                </div>

                {/* Design Translation Panel */}
                <div className="lg:col-span-5 p-5 bg-[#F9F8F4] border border-[#EBE8E0] space-y-3.5">
                  <div className="flex items-center gap-2 text-[#1A1A1A] border-b border-[#EBE8E0] pb-2">
                    <Palette className="w-4 h-4 text-[#D4AF37]" />
                    <h3 className="text-[10px] font-sans uppercase tracking-[0.25em] font-bold text-[#1A1A1A]">
                      Digital Product Translation
                    </h3>
                  </div>

                  <div className="space-y-3 text-xs">
                    <div>
                      <span className="text-[9px] text-[#777] uppercase font-sans tracking-widest font-bold">Visual Tone:</span>
                      <p className="text-[#1A1A1A] font-serif italic mt-0.5">{theme.designTranslation?.visualTone || 'Sophisticated, high contrast, museum depth'}</p>
                    </div>

                    <div>
                      <span className="text-[9px] text-[#777] uppercase font-sans tracking-widest font-bold">Recommended Use Cases:</span>
                      <div className="flex flex-wrap gap-1.5 mt-1">
                        {theme.designTranslation?.recommendedUseCases?.map((useCase, uIdx) => (
                          <span
                            key={uIdx}
                            className="px-2 py-0.5 text-[9px] uppercase font-mono bg-white border border-[#EBE8E0] text-[#333]"
                          >
                            {useCase}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div>
                      <span className="text-[9px] text-[#777] uppercase font-sans tracking-widest font-bold">Layout &amp; Pacing:</span>
                      <p className="text-[#555] font-serif italic mt-0.5">{theme.designTranslation?.layoutStyle || 'Asymmetrical balance'} • {theme.designTranslation?.interactionPacing || 'Velvety ease-out'}</p>
                    </div>

                    {/* Curated Theme Palette */}
                    {theme.designTranslation?.keyColors && (
                      <div>
                        <span className="text-[9px] text-[#777] uppercase font-sans tracking-widest font-bold">Harmonic Chroma:</span>
                        <div className="flex items-center gap-2 mt-1.5">
                          {theme.designTranslation.keyColors.map((col, cIdx) => (
                            <div
                              key={cIdx}
                              className="w-7 h-7 border border-[#1A1A1A] shadow-xs"
                              style={{ backgroundColor: col }}
                              title={col}
                            />
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Paired Artworks Visual Juxtaposition */}
              <div className="space-y-3 pt-3 border-t border-[#EBE8E0]">
                <h4 className="text-[10px] font-sans uppercase tracking-[0.25em] font-bold text-[#1A1A1A]">
                  Dialoguing Artworks in this Collection
                </h4>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                  {matchedArtworks.map((art) => (
                    <div
                      key={art.id}
                      className="group/art relative overflow-hidden border border-[#EBE8E0] hover:border-[#1A1A1A] bg-[#FDFBF7] aspect-[4/3] transition-colors"
                    >
                      <img
                        src={art.imageUrl}
                        alt={art.title}
                        className="w-full h-full object-cover group-hover/art:scale-102 transition-transform duration-300"
                        referrerPolicy="no-referrer"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-transparent to-transparent p-2.5 flex flex-col justify-end">
                        <p className="text-[11px] font-serif font-bold text-[#FDFBF7] truncate">
                          {art.title}
                        </p>
                        <p className="text-[9px] text-[#D4AF37] font-sans uppercase tracking-wider truncate">
                          {art.artist}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
