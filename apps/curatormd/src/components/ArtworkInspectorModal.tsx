import React, { useState } from 'react';
import { X, Sparkles, Copy, Check, Grid, Compass, Lightbulb, Type, ExternalLink, Sliders, Layers, Eye } from 'lucide-react';
import { Artwork } from '../types';

interface ArtworkInspectorModalProps {
  artwork: Artwork | null;
  onClose: () => void;
  onAnalyze: (artwork: Artwork) => void;
  isAnalyzing?: boolean;
}

export const ArtworkInspectorModal: React.FC<ArtworkInspectorModalProps> = ({
  artwork,
  onClose,
  onAnalyze,
  isAnalyzing
}) => {
  const [activeOverlay, setActiveOverlay] = useState<'none' | 'thirds' | 'golden' | 'focal'>('thirds');
  const [copiedHex, setCopiedHex] = useState<string | null>(null);

  if (!artwork) return null;

  const analysis = artwork.compositionAnalysis;

  const handleCopyHex = (hex: string) => {
    navigator.clipboard.writeText(hex);
    setCopiedHex(hex);
    setTimeout(() => setCopiedHex(null), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-[#1A1A1A]/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div 
        id="modal-artwork-inspector"
        className="bg-[#FFFFFF] border-2 border-[#1A1A1A] w-full max-w-6xl max-h-[92vh] overflow-hidden shadow-2xl flex flex-col"
      >
        {/* Modal Top Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b-2 border-[#1A1A1A] bg-[#FDFBF7]">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-[#1A1A1A] flex items-center justify-center text-[#D4AF37]">
              <Compass className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-serif italic text-[#1A1A1A]">
                  {artwork.title}
                </h2>
                {artwork.sourceUrl && (
                  <a
                    href={artwork.sourceUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="text-[#777] hover:text-[#D4AF37] text-xs flex items-center gap-1"
                    title="View on Google Arts & Culture"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                )}
              </div>
              <p className="text-xs font-serif italic text-[#666]">
                {artwork.artist} &bull; {artwork.year || 'Historical'} &bull; {artwork.museum || 'Google Arts & Culture Partner'}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              id="btn-reanalyze-artwork"
              onClick={() => onAnalyze(artwork)}
              disabled={isAnalyzing}
              className="flex items-center gap-1.5 px-4 py-2 bg-[#1A1A1A] text-[#FDFBF7] text-[10px] uppercase tracking-[0.25em] font-sans hover:bg-[#333] disabled:opacity-50 transition-colors cursor-pointer"
            >
              <Sparkles className={`w-3.5 h-3.5 text-[#D4AF37] ${isAnalyzing ? 'animate-spin' : ''}`} />
              <span>{isAnalyzing ? 'Analyzing...' : 'Re-Analyze with Gemini'}</span>
            </button>

            <button
              id="btn-close-inspector"
              onClick={onClose}
              className="p-1.5 text-[#777] hover:text-[#1A1A1A] hover:bg-[#F0EEE6] transition-colors cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Modal Main Content (Split view) */}
        <div className="flex-1 overflow-y-auto grid grid-cols-1 lg:grid-cols-12 divide-y lg:divide-y-0 lg:divide-x-2 divide-[#1A1A1A]">
          
          {/* Left / Top: Visual Canvas & Overlay Inspection */}
          <div className="lg:col-span-6 p-6 flex flex-col justify-between space-y-4 bg-[#FDFBF7]">
            {/* Composition Overlay Switcher Bar */}
            <div className="flex items-center justify-between bg-[#FFFFFF] p-2 border border-[#1A1A1A]">
              <span className="text-[10px] uppercase tracking-widest font-sans font-bold text-[#1A1A1A] pl-1">
                Compositional Overlays:
              </span>
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setActiveOverlay('none')}
                  className={`px-2.5 py-1 text-[10px] uppercase font-sans tracking-wider transition-colors ${
                    activeOverlay === 'none' ? 'bg-[#1A1A1A] text-[#FDFBF7]' : 'text-[#777] hover:text-[#1A1A1A]'
                  }`}
                >
                  Clear
                </button>
                <button
                  onClick={() => setActiveOverlay('thirds')}
                  className={`flex items-center gap-1 px-2.5 py-1 text-[10px] uppercase font-sans tracking-wider transition-colors ${
                    activeOverlay === 'thirds' ? 'bg-[#1A1A1A] text-[#D4AF37] font-bold' : 'text-[#777] hover:text-[#1A1A1A]'
                  }`}
                >
                  <Grid className="w-3 h-3" /> Thirds
                </button>
                <button
                  onClick={() => setActiveOverlay('golden')}
                  className={`flex items-center gap-1 px-2.5 py-1 text-[10px] uppercase font-sans tracking-wider transition-colors ${
                    activeOverlay === 'golden' ? 'bg-[#1A1A1A] text-[#D4AF37] font-bold' : 'text-[#777] hover:text-[#1A1A1A]'
                  }`}
                >
                  <Compass className="w-3 h-3" /> Golden Ratio
                </button>
                <button
                  onClick={() => setActiveOverlay('focal')}
                  className={`flex items-center gap-1 px-2.5 py-1 text-[10px] uppercase font-sans tracking-wider transition-colors ${
                    activeOverlay === 'focal' ? 'bg-[#1A1A1A] text-[#D4AF37] font-bold' : 'text-[#777] hover:text-[#1A1A1A]'
                  }`}
                >
                  <Eye className="w-3 h-3" /> Focal
                </button>
              </div>
            </div>

            {/* Interactive Image Frame */}
            <div className="relative border border-[#1A1A1A] bg-[#1A1A1A] shadow-md flex items-center justify-center min-h-[340px] max-h-[460px]">
              <img
                src={artwork.imageUrl}
                alt={artwork.title}
                className="w-full h-full object-contain max-h-[460px]"
                referrerPolicy="no-referrer"
              />

              {/* OVERLAY 1: Rule of Thirds Grid */}
              {activeOverlay === 'thirds' && (
                <div className="absolute inset-0 pointer-events-none grid grid-cols-3 grid-rows-3 border border-[#D4AF37]/50">
                  <div className="border-r border-b border-[#D4AF37]/50 relative">
                    <div className="absolute -bottom-1 -right-1 w-2 h-2 rounded-full bg-[#D4AF37] shadow-[0_0_8px_#D4AF37]" />
                  </div>
                  <div className="border-r border-b border-[#D4AF37]/50 relative">
                    <div className="absolute -bottom-1 -left-1 w-2 h-2 rounded-full bg-[#D4AF37] shadow-[0_0_8px_#D4AF37]" />
                  </div>
                  <div className="border-b border-[#D4AF37]/50" />
                  <div className="border-r border-b border-[#D4AF37]/50 relative">
                    <div className="absolute -bottom-1 -right-1 w-2 h-2 rounded-full bg-[#D4AF37] shadow-[0_0_8px_#D4AF37]" />
                  </div>
                  <div className="border-r border-b border-[#D4AF37]/50 relative">
                    <div className="absolute -bottom-1 -left-1 w-2 h-2 rounded-full bg-[#D4AF37] shadow-[0_0_8px_#D4AF37]" />
                  </div>
                  <div className="border-b border-[#D4AF37]/50" />
                  <div className="border-r border-[#D4AF37]/50" />
                  <div className="border-r border-[#D4AF37]/50" />
                  <div />
                </div>
              )}

              {/* OVERLAY 2: Golden Ratio Spiral SVG */}
              {activeOverlay === 'golden' && (
                <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-90" viewBox="0 0 100 100" preserveAspectRatio="none">
                  {/* Golden rectangle divisions */}
                  <line x1="61.8" y1="0" x2="61.8" y2="100" stroke="#D4AF37" strokeWidth="0.75" strokeDasharray="2,2" />
                  <line x1="61.8" y1="61.8" x2="100" y2="61.8" stroke="#D4AF37" strokeWidth="0.75" strokeDasharray="2,2" />
                  <line x1="76.4" y1="61.8" x2="76.4" y2="100" stroke="#D4AF37" strokeWidth="0.75" strokeDasharray="2,2" />
                  <line x1="76.4" y1="76.4" x2="61.8" y2="76.4" stroke="#D4AF37" strokeWidth="0.75" strokeDasharray="2,2" />
                  {/* Approximated logarithmic golden spiral curve */}
                  <path
                    d="M 0 100 A 61.8 61.8 0 0 1 61.8 0 A 38.2 38.2 0 0 1 100 61.8 A 23.6 23.6 0 0 1 76.4 100 A 14.6 14.6 0 0 1 61.8 76.4 A 9 9 0 0 1 76.4 67.4"
                    fill="none"
                    stroke="#FDFBF7"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                  />
                  <circle cx="73" cy="72" r="2.5" fill="#D4AF37" />
                </svg>
              )}

              {/* OVERLAY 3: AI Detected Focal Points */}
              {activeOverlay === 'focal' && analysis?.focalPoints && (
                <div className="absolute inset-0 pointer-events-none">
                  {analysis.focalPoints.map((pt, pIdx) => (
                    <div
                      key={pIdx}
                      className="absolute -translate-x-1/2 -translate-y-1/2 group/pt pointer-events-auto cursor-pointer"
                      style={{ left: `${pt.x}%`, top: `${pt.y}%` }}
                    >
                      <div className="relative">
                        <span className="w-6 h-6 rounded-full bg-[#1A1A1A] border-2 border-[#D4AF37] flex items-center justify-center text-[10px] font-mono font-bold text-[#D4AF37] shadow-[0_0_12px_#D4AF37] animate-pulse">
                          {pIdx + 1}
                        </span>
                        {/* Tooltip */}
                        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 w-48 p-2.5 bg-[#FFFFFF] border-2 border-[#1A1A1A] text-xs text-[#1A1A1A] shadow-xl z-30 opacity-95 group-hover/pt:opacity-100 transition-opacity">
                          <p className="font-serif italic font-bold text-[#1A1A1A]">{pt.label}</p>
                          <span className="text-[10px] uppercase font-sans tracking-widest text-[#777]">{pt.importance} focus</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Extracted Palette Swatch Strip */}
            {analysis?.palette && (
              <div className="space-y-2">
                <div className="flex items-center justify-between text-xs text-[#555]">
                  <span className="font-sans text-[10px] uppercase tracking-[0.2em] font-bold text-[#1A1A1A]">
                    Harmonic Color Spectrum
                  </span>
                  <span className="font-serif italic text-[11px]">Click swatch to copy HEX</span>
                </div>
                <div className="grid grid-cols-5 gap-2">
                  {analysis.palette.map((swatch, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleCopyHex(swatch.hex)}
                      className="group/swatch relative flex flex-col border border-[#1A1A1A] hover:border-[#D4AF37] transition-all bg-[#FFFFFF] p-2 text-left shadow-2xs"
                    >
                      <div
                        className="h-9 w-full mb-1.5 border border-[#1A1A1A] transition-transform group-hover/swatch:scale-95 flex items-center justify-center"
                        style={{ backgroundColor: swatch.hex }}
                      >
                        {copiedHex === swatch.hex ? (
                          <Check className="w-4 h-4 text-white drop-shadow-md" />
                        ) : (
                          <Copy className="w-3.5 h-3.5 text-white/80 opacity-0 group-hover/swatch:opacity-100 transition-opacity drop-shadow-md" />
                        )}
                      </div>
                      <span className="font-mono text-[10px] text-[#1A1A1A] font-bold truncate">
                        {swatch.hex}
                      </span>
                      <span className="font-serif text-[10px] text-[#555] truncate italic">
                        {swatch.name}
                      </span>
                      <span className="text-[9px] font-sans uppercase tracking-wider text-[#888]">
                        {swatch.percentage}% &bull; {swatch.role}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Right / Bottom: Deep Analytical Dossier */}
          <div className="lg:col-span-6 p-6 space-y-5 bg-[#FFFFFF]">
            {analysis ? (
              <>
                {/* Mood & Composition Header */}
                <div className="p-5 bg-[#F9F8F4] border border-[#1A1A1A] space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] uppercase tracking-[0.25em] font-sans font-bold text-[#1A1A1A] bg-[#FFFFFF] border border-[#1A1A1A] px-2.5 py-0.5">
                      {analysis.compositionType}
                    </span>
                    <span className="text-xs font-serif italic text-[#666]">
                      Temp: <strong className="text-[#1A1A1A] font-bold">{analysis.colorTemperature}</strong> &bull; Contrast: <strong className="text-[#1A1A1A] font-bold">{analysis.contrastLevel}</strong>
                    </span>
                  </div>
                  <h3 className="text-lg font-serif italic text-[#1A1A1A] pt-1">
                    Aesthetic Atmosphere
                  </h3>
                  <p className="text-xs font-serif text-[#444] leading-relaxed italic">
                    "{analysis.dominantMood}"
                  </p>
                </div>

                {/* Compositional Grid Details */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="p-4 bg-[#F9F8F4] border border-[#EBE8E0] space-y-1">
                    <span className="text-[9px] uppercase tracking-widest font-sans font-bold text-[#1A1A1A]">
                      Visual Weight &amp; Gravity
                    </span>
                    <p className="text-xs font-serif text-[#333] leading-relaxed">
                      {analysis.visualWeight}
                    </p>
                  </div>

                  <div className="p-4 bg-[#F9F8F4] border border-[#EBE8E0] space-y-1">
                    <span className="text-[9px] uppercase tracking-widest font-sans font-bold text-[#1A1A1A]">
                      Surface Texture &amp; Grain
                    </span>
                    <p className="text-xs font-serif text-[#333] leading-relaxed">
                      {analysis.textureFeel}
                    </p>
                  </div>

                  <div className="p-4 bg-[#F9F8F4] border border-[#EBE8E0] space-y-1 sm:col-span-2">
                    <span className="text-[9px] uppercase tracking-widest font-sans font-bold text-[#1A1A1A]">
                      Spatial Rhythm &amp; Cadence
                    </span>
                    <p className="text-xs font-serif text-[#333] leading-relaxed">
                      {analysis.spatialRhythm}
                    </p>
                  </div>
                </div>

                {/* Typographic Resonance */}
                {analysis.typographicResonance && (
                  <div className="p-4 bg-[#F9F8F4] border border-[#EBE8E0] space-y-2">
                    <div className="flex items-center gap-2 text-[#1A1A1A]">
                      <Type className="w-4 h-4 text-[#D4AF37]" />
                      <h4 className="text-[10px] font-sans uppercase tracking-[0.25em] font-bold">
                        Typographic Pairing Resonance
                      </h4>
                    </div>
                    <div className="grid grid-cols-2 gap-3 text-xs">
                      <div>
                        <span className="text-[9px] text-[#777] uppercase font-sans tracking-wider font-bold">Suggested Serif:</span>
                        <p className="text-[#1A1A1A] font-serif italic text-sm">{analysis.typographicResonance.suggestedSerif}</p>
                      </div>
                      <div>
                        <span className="text-[9px] text-[#777] uppercase font-sans tracking-wider font-bold">Suggested Sans:</span>
                        <p className="text-[#1A1A1A] font-sans font-medium text-xs">{analysis.typographicResonance.suggestedSans}</p>
                      </div>
                    </div>
                    <p className="text-xs font-serif italic text-[#555] pt-2 border-t border-[#EBE8E0]">
                      <strong className="text-[#1A1A1A]">Cadence:</strong> {analysis.typographicResonance.weightCadence} ({analysis.typographicResonance.trackingPreference})
                    </p>
                  </div>
                )}

                {/* UI/UX Design System Takeaways */}
                <div className="p-5 bg-[#FFFFFF] border-2 border-[#1A1A1A] space-y-3 shadow-xs">
                  <div className="flex items-center gap-2 text-[#1A1A1A]">
                    <Lightbulb className="w-4 h-4 text-[#D4AF37]" />
                    <h4 className="text-[10px] font-sans uppercase tracking-[0.25em] font-bold">
                      Actionable Design System Directives
                    </h4>
                  </div>
                  <ul className="space-y-2.5">
                    {analysis.designTakeaways.map((takeaway, tIdx) => (
                      <li key={tIdx} className="flex items-start gap-2.5 text-xs font-serif text-[#1A1A1A] leading-relaxed">
                        <span className="w-1.5 h-1.5 bg-[#D4AF37] border border-[#1A1A1A] shrink-0 mt-1.5" />
                        <span>{takeaway}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </>
            ) : (
              <div className="p-8 text-center space-y-3 bg-[#F9F8F4] border border-[#1A1A1A]">
                <Sparkles className="w-8 h-8 text-[#D4AF37] mx-auto animate-pulse" />
                <h3 className="font-serif italic text-xl text-[#1A1A1A]">
                  Compositional Analysis Pending
                </h3>
                <p className="text-xs font-serif text-[#666] max-w-sm mx-auto leading-relaxed">
                  Run Gemini multimodal analysis on this piece to extract its harmonic palette, focal anchor points, and UI design directives.
                </p>
                <button
                  onClick={() => onAnalyze(artwork)}
                  disabled={isAnalyzing}
                  className="inline-flex items-center gap-2 px-6 py-2.5 bg-[#1A1A1A] text-[#FDFBF7] text-[10px] uppercase tracking-[0.25em] font-sans hover:bg-[#333] transition-colors cursor-pointer mt-2"
                >
                  <Sparkles className="w-3.5 h-3.5 text-[#D4AF37]" />
                  <span>Analyze with Gemini</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
