import React, { useState, useMemo } from 'react';
import { Search, Filter, Sparkles, Heart, ExternalLink, Eye, Plus, CheckCircle2, SlidersHorizontal, RefreshCw, Layers } from 'lucide-react';
import { Artwork } from '../types';

interface ArtworkGalleryProps {
  artworks: Artwork[];
  onSelectArtwork: (artwork: Artwork) => void;
  onAnalyzeArtwork: (artwork: Artwork) => void;
  onToggleFavorite: (artworkId: string) => void;
  onAnalyzeAll: () => void;
  onOpenImporter: () => void;
  isAnalyzingAll?: boolean;
}

export const ArtworkGallery: React.FC<ArtworkGalleryProps> = ({
  artworks,
  onSelectArtwork,
  onAnalyzeArtwork,
  onToggleFavorite,
  onAnalyzeAll,
  onOpenImporter,
  isAnalyzingAll
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterTemp, setFilterTemp] = useState<string>('all');
  const [onlyFavorites, setOnlyFavorites] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'compact'>('grid');

  const filteredArtworks = useMemo(() => {
    return artworks.filter((art) => {
      const matchesSearch =
        art.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        art.artist.toLowerCase().includes(searchQuery.toLowerCase()) ||
        (art.movement && art.movement.toLowerCase().includes(searchQuery.toLowerCase())) ||
        (art.compositionAnalysis?.dominantMood && art.compositionAnalysis.dominantMood.toLowerCase().includes(searchQuery.toLowerCase()));

      const matchesTemp =
        filterTemp === 'all' ||
        (art.compositionAnalysis && art.compositionAnalysis.colorTemperature === filterTemp);

      const matchesFav = !onlyFavorites || Boolean(art.isFavorite);

      return matchesSearch && matchesTemp && matchesFav;
    });
  }, [artworks, searchQuery, filterTemp, onlyFavorites]);

  const unanalyzedCount = artworks.filter(a => !a.compositionAnalysis).length;

  return (
    <div className="space-y-6">
      {/* Top Banner / Collection Stats Bar */}
      <div className="bg-[#FFFFFF] border-2 border-[#1A1A1A] p-6 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <span className="text-[10px] uppercase tracking-[0.3em] font-sans font-semibold text-[#1A1A1A] border-l-4 border-[#D4AF37] pl-3">
              Analysis Matrix &bull; Active Catalog
            </span>
            <span className="text-[10px] uppercase font-mono tracking-widest bg-[#F9F8F4] border border-[#EBE8E0] px-2 py-0.5 text-[#555]">
              {artworks.length} LINKED &bull; {artworks.length - unanalyzedCount} ANALYZED
            </span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-light tracking-tight italic text-[#1A1A1A]">
            Google Arts &amp; Culture Library
          </h1>
          <p className="text-xs font-serif italic text-[#555] max-w-2xl mt-1 leading-relaxed">
            Every piece is scrutinized through chromatic frequency, spatial vectors, tonal gravity, and optical lighting to derive mathematically grounded design tokens.
          </p>
        </div>

        <div className="flex items-center gap-3 shrink-0 w-full md:w-auto">
          {unanalyzedCount > 0 && (
            <button
              id="btn-analyze-all"
              onClick={onAnalyzeAll}
              disabled={isAnalyzingAll}
              className="flex-1 md:flex-initial flex items-center justify-center gap-2 px-6 py-3 bg-[#1A1A1A] text-[#FDFBF7] text-[10px] uppercase tracking-[0.3em] font-sans hover:bg-[#333] disabled:opacity-50 transition-colors shadow-sm cursor-pointer"
            >
              <Sparkles className={`w-3.5 h-3.5 text-[#D4AF37] ${isAnalyzingAll ? 'animate-spin' : ''}`} />
              <span>{isAnalyzingAll ? 'Analyzing Pieces...' : `Analyze All (${unanalyzedCount})`}</span>
            </button>
          )}

          <button
            id="btn-add-more-artworks"
            onClick={onOpenImporter}
            className="flex items-center justify-center gap-2 px-5 py-3 border border-[#1A1A1A] text-[#1A1A1A] text-[10px] uppercase tracking-[0.3em] font-sans hover:bg-[#F0EEE6] transition-colors cursor-pointer"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Add Pieces</span>
          </button>
        </div>
      </div>

      {/* Filter and Search Toolbar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 bg-[#FFFFFF] p-3 border border-[#EBE8E0]">
        {/* Search input */}
        <div className="relative w-full sm:w-80">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#888]" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search title, artist, movement, or mood..."
            className="w-full pl-9 pr-3 py-1.5 bg-[#FDFBF7] border border-[#EBE8E0] focus:border-[#1A1A1A] text-xs text-[#1A1A1A] placeholder-[#888] focus:outline-none"
          />
        </div>

        {/* Filter Badges */}
        <div className="flex items-center gap-2 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
          <div className="flex items-center gap-1 bg-[#FDFBF7] p-1 border border-[#EBE8E0]">
            <button
              onClick={() => setFilterTemp('all')}
              className={`px-3 py-1 text-[10px] uppercase font-sans tracking-wider transition-colors ${
                filterTemp === 'all' ? 'bg-[#1A1A1A] text-[#FDFBF7] font-bold' : 'text-[#777] hover:text-[#1A1A1A]'
              }`}
            >
              All Temps
            </button>
            <button
              onClick={() => setFilterTemp('warm')}
              className={`px-3 py-1 text-[10px] uppercase font-sans tracking-wider transition-colors ${
                filterTemp === 'warm' ? 'bg-[#D4AF37] text-white font-bold' : 'text-[#777] hover:text-[#1A1A1A]'
              }`}
            >
              Warm
            </button>
            <button
              onClick={() => setFilterTemp('cool')}
              className={`px-3 py-1 text-[10px] uppercase font-sans tracking-wider transition-colors ${
                filterTemp === 'cool' ? 'bg-[#1A1A1A] text-sky-200 font-bold' : 'text-[#777] hover:text-[#1A1A1A]'
              }`}
            >
              Cool
            </button>
            <button
              onClick={() => setFilterTemp('balanced')}
              className={`px-3 py-1 text-[10px] uppercase font-sans tracking-wider transition-colors ${
                filterTemp === 'balanced' ? 'bg-[#1A1A1A] text-emerald-200 font-bold' : 'text-[#777] hover:text-[#1A1A1A]'
              }`}
            >
              Balanced
            </button>
          </div>

          <button
            onClick={() => setOnlyFavorites(!onlyFavorites)}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-[10px] uppercase tracking-wider font-sans border transition-colors ${
              onlyFavorites
                ? 'bg-[#1A1A1A] border-[#1A1A1A] text-rose-300'
                : 'bg-[#FDFBF7] border-[#EBE8E0] text-[#777] hover:text-[#1A1A1A]'
            }`}
          >
            <Heart className={`w-3.5 h-3.5 ${onlyFavorites ? 'fill-rose-400 text-rose-400' : ''}`} />
            <span>Favorites</span>
          </button>
        </div>
      </div>

      {/* Empty State */}
      {filteredArtworks.length === 0 && (
        <div className="bg-[#FFFFFF] border border-[#EBE8E0] p-12 text-center space-y-3">
          <div className="w-12 h-12 bg-[#F9F8F4] border border-[#1A1A1A] flex items-center justify-center text-[#1A1A1A] mx-auto">
            <Search className="w-5 h-5" />
          </div>
          <h3 className="font-serif text-lg font-bold text-[#1A1A1A]">
            No artworks match your query
          </h3>
          <p className="text-xs text-[#777] max-w-md mx-auto italic font-serif">
            Try adjusting your search criteria, or import new artworks from your Google Sheets or curated preset packs.
          </p>
          <button
            onClick={onOpenImporter}
            className="inline-flex items-center gap-2 px-6 py-2.5 bg-[#1A1A1A] text-[#FDFBF7] text-[10px] uppercase tracking-[0.3em] font-sans hover:bg-[#333] transition-colors mt-2"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Import Artworks</span>
          </button>
        </div>
      )}

      {/* Artworks Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredArtworks.map((artwork) => {
          const isAnalyzed = Boolean(artwork.compositionAnalysis);
          return (
            <div
              key={artwork.id}
              className="group bg-[#FFFFFF] border border-[#EBE8E0] hover:border-[#1A1A1A] transition-all duration-200 flex flex-col justify-between shadow-xs"
            >
              {/* Artwork Media Area */}
              <div className="relative aspect-[4/3] bg-[#EBE8E0] overflow-hidden border-b border-[#EBE8E0]">
                <img
                  src={artwork.imageUrl}
                  alt={artwork.title}
                  className="w-full h-full object-cover group-hover:scale-102 transition-transform duration-500"
                  loading="lazy"
                  referrerPolicy="no-referrer"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-black/10 opacity-70" />

                {/* Top Overlay Badges */}
                <div className="absolute top-3 left-3 right-3 flex items-center justify-between">
                  <span className="px-2.5 py-1 text-[9px] font-mono tracking-widest uppercase bg-white/95 text-[#1A1A1A] border border-[#1A1A1A] shadow-xs">
                    {artwork.movement || artwork.year || 'Historical'}
                  </span>

                  <div className="flex items-center gap-1.5">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onToggleFavorite(artwork.id);
                      }}
                      className="p-1.5 bg-white/95 text-[#1A1A1A] hover:text-rose-600 border border-[#1A1A1A] transition-colors"
                    >
                      <Heart className={`w-3.5 h-3.5 ${artwork.isFavorite ? 'fill-rose-600 text-rose-600' : ''}`} />
                    </button>

                    {artwork.sourceUrl && (
                      <a
                        href={artwork.sourceUrl}
                        target="_blank"
                        rel="noreferrer"
                        onClick={(e) => e.stopPropagation()}
                        title="View on Google Arts & Culture"
                        className="p-1.5 bg-white/95 text-[#1A1A1A] hover:text-[#D4AF37] border border-[#1A1A1A] transition-colors"
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                      </a>
                    )}
                  </div>
                </div>

                {/* Color Swatch Strip (if analyzed) */}
                {isAnalyzed && artwork.compositionAnalysis?.palette && (
                  <div className="absolute bottom-2 left-3 right-3 flex items-center h-2 overflow-hidden border border-black/50 shadow-xs">
                    {artwork.compositionAnalysis.palette.map((swatch, sIdx) => (
                      <div
                        key={sIdx}
                        className="h-full"
                        style={{
                          width: `${swatch.percentage}%`,
                          backgroundColor: swatch.hex
                        }}
                        title={`${swatch.name} (${swatch.hex}) - ${swatch.percentage}%`}
                      />
                    ))}
                  </div>
                )}
              </div>

              {/* Artwork Metadata & Analysis Info */}
              <div className="p-5 flex-1 flex flex-col justify-between space-y-4">
                <div>
                  <div className="flex items-start justify-between gap-2 border-b border-[#EBE8E0] pb-3">
                    <div>
                      <h3 className="font-serif text-base font-bold text-[#1A1A1A] group-hover:text-[#D4AF37] transition-colors line-clamp-1">
                        {artwork.title}
                      </h3>
                      <p className="text-xs text-[#777] mt-0.5 font-serif italic">
                        {artwork.artist} {artwork.year ? `• ${artwork.year}` : ''}
                      </p>
                    </div>

                    {isAnalyzed ? (
                      <span className="shrink-0 bg-[#D4AF37] text-white text-[9px] px-2 py-0.5 tracking-widest font-sans font-bold uppercase">
                        STABLE
                      </span>
                    ) : (
                      <span className="shrink-0 border border-[#1A1A1A] text-[#1A1A1A] text-[9px] px-2 py-0.5 font-mono uppercase tracking-widest">
                        PENDING
                      </span>
                    )}
                  </div>

                  {/* Composition / Mood Snippet */}
                  {isAnalyzed && artwork.compositionAnalysis ? (
                    <div className="mt-3 space-y-1.5">
                      <div className="flex items-center gap-2">
                        <span className="text-[10px] uppercase font-sans tracking-widest font-bold text-[#1A1A1A]">
                          Structure:
                        </span>
                        <span className="text-xs text-[#333] font-serif italic truncate">
                          {artwork.compositionAnalysis.compositionType}
                        </span>
                      </div>
                      <p className="text-xs text-[#555] line-clamp-2 leading-relaxed font-serif italic">
                        "{artwork.compositionAnalysis.dominantMood}"
                      </p>
                    </div>
                  ) : (
                    <p className="mt-2 text-xs text-[#888] italic font-serif">
                      {artwork.userNotes || 'Awaiting compositional and chromatic analysis by Gemini...'}
                    </p>
                  )}
                </div>

                {/* Card Actions */}
                <div className="pt-3 border-t border-[#EBE8E0] flex items-center justify-between gap-2">
                  <button
                    onClick={() => onSelectArtwork(artwork)}
                    className="flex-1 flex items-center justify-center gap-1.5 px-3 py-2 text-[10px] uppercase tracking-[0.2em] font-sans font-bold text-[#1A1A1A] border border-[#1A1A1A] hover:bg-[#1A1A1A] hover:text-[#FDFBF7] transition-colors cursor-pointer"
                  >
                    <Eye className="w-3.5 h-3.5" />
                    <span>Inspect</span>
                  </button>

                  <button
                    onClick={() => onAnalyzeArtwork(artwork)}
                    disabled={artwork.analyzing}
                    title="Run Gemini Visual Analysis"
                    className="p-2 border border-[#1A1A1A] bg-[#FDFBF7] text-[#1A1A1A] hover:bg-[#1A1A1A] hover:text-[#D4AF37] transition-colors cursor-pointer disabled:opacity-50"
                  >
                    <Sparkles className={`w-3.5 h-3.5 ${artwork.analyzing ? 'animate-spin' : ''}`} />
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
