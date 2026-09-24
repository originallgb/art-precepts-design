import React, { useState } from 'react';
import { X, FileSpreadsheet, Sparkles, Link, Plus, Check, AlertCircle, Library, ArrowRight, ExternalLink } from 'lucide-react';
import { Artwork, PresetCollection } from '../types';
import { PRESET_COLLECTIONS } from '../data/presets';

interface SheetImporterModalProps {
  isOpen: boolean;
  onClose: () => void;
  onImportArtworks: (artworks: Artwork[], collectionName?: string) => void;
  onSelectPreset: (preset: PresetCollection) => void;
}

export const SheetImporterModal: React.FC<SheetImporterModalProps> = ({
  isOpen,
  onClose,
  onImportArtworks,
  onSelectPreset
}) => {
  const [activeTab, setActiveTab] = useState<'presets' | 'sheets' | 'paste' | 'manual'>('presets');
  const [sheetUrl, setSheetUrl] = useState('');
  const [rawText, setRawText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Manual form state
  const [manualTitle, setManualTitle] = useState('');
  const [manualArtist, setManualArtist] = useState('');
  const [manualYear, setManualYear] = useState('');
  const [manualUrl, setManualUrl] = useState('');
  const [manualImage, setManualImage] = useState('');
  const [manualNotes, setManualNotes] = useState('');

  if (!isOpen) return null;

  const handleImportSheet = async () => {
    if (!sheetUrl.trim()) {
      setError('Please provide a valid Google Sheet URL.');
      return;
    }
    setError(null);
    setIsLoading(true);

    try {
      const response = await fetch('/api/import-sheet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sheetUrl: sheetUrl.trim() }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch spreadsheet data.');
      }

      if (data.artworks && data.artworks.length > 0) {
        onImportArtworks(data.artworks, 'Imported from Google Sheet');
        onClose();
      } else {
        setError('No valid artwork rows found in the sheet. Ensure column headers include Title/Artwork and Artist/URL.');
      }
    } catch (err: any) {
      setError(err.message || 'Error processing spreadsheet. Ensure it is public or shared via link.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleParsePaste = () => {
    if (!rawText.trim()) {
      setError('Please paste text, CSV, or Google Arts & Culture links.');
      return;
    }
    setError(null);

    const lines = rawText.split('\n').map(l => l.trim()).filter(Boolean);
    const parsedArtworks: Artwork[] = [];

    lines.forEach((line, idx) => {
      // Check if line is a Google Arts & Culture URL
      if (line.includes('artsandculture.google.com')) {
        // Extract title slug from url
        const slugMatch = line.match(/\/asset\/([^/?#]+)/) || line.match(/\/story\/([^/?#]+)/);
        let derivedTitle = slugMatch ? slugMatch[1].replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase()) : `Arts & Culture Artwork #${idx + 1}`;
        
        parsedArtworks.push({
          id: `pasted-link-${Date.now()}-${idx}`,
          title: derivedTitle,
          artist: 'Google Arts & Culture Asset',
          sourceUrl: line,
          imageUrl: 'https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1200&q=80',
          userNotes: 'Imported via Google Arts & Culture URL',
          isFavorite: true,
          userRating: 5
        });
      } else if (line.includes(',') || line.includes('\t')) {
        // CSV row parse
        const parts = line.split(/[,\t]/).map(p => p.replace(/^"|"$/g, '').trim());
        if (parts.length >= 1 && parts[0]) {
          parsedArtworks.push({
            id: `pasted-csv-${Date.now()}-${idx}`,
            title: parts[0] || 'Untitled Artwork',
            artist: parts[1] || 'Unknown Artist',
            year: parts[2] || '',
            sourceUrl: parts.find(p => p.startsWith('http')) || 'https://artsandculture.google.com',
            imageUrl: parts.find(p => p.match(/\.(jpeg|jpg|png|webp)/i)) || 'https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1200&q=80',
            userNotes: parts[3] || 'Imported from CSV row',
            isFavorite: true,
            userRating: 5
          });
        }
      } else {
        // Plain text title
        parsedArtworks.push({
          id: `pasted-title-${Date.now()}-${idx}`,
          title: line,
          artist: 'Masterpiece',
          sourceUrl: 'https://artsandculture.google.com',
          imageUrl: 'https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1200&q=80',
          userNotes: 'Imported from artwork title',
          isFavorite: true,
          userRating: 5
        });
      }
    });

    if (parsedArtworks.length > 0) {
      onImportArtworks(parsedArtworks, 'Imported from Text / Links');
      onClose();
    } else {
      setError('Could not identify any artwork entries in the pasted text.');
    }
  };

  const handleAddManual = (e: React.FormEvent) => {
    e.preventDefault();
    if (!manualTitle.trim()) {
      setError('Artwork title is required.');
      return;
    }

    const newArtwork: Artwork = {
      id: `manual-${Date.now()}`,
      title: manualTitle.trim(),
      artist: manualArtist.trim() || 'Unknown Master',
      year: manualYear.trim(),
      sourceUrl: manualUrl.trim() || 'https://artsandculture.google.com',
      imageUrl: manualImage.trim() || 'https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=1200&q=80',
      userNotes: manualNotes.trim() || 'Manually cataloged artwork',
      isFavorite: true,
      userRating: 5
    };

    onImportArtworks([newArtwork], 'Added Artwork');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-[#1A1A1A]/70 backdrop-blur-sm animate-in fade-in duration-200">
      <div 
        id="modal-sheet-importer"
        className="bg-[#FFFFFF] border-2 border-[#1A1A1A] w-full max-w-3xl overflow-hidden shadow-2xl flex flex-col max-h-[90vh]"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b-2 border-[#1A1A1A] bg-[#FDFBF7]">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-[#1A1A1A] flex items-center justify-center text-[#D4AF37]">
              <FileSpreadsheet className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-xl font-serif italic text-[#1A1A1A]">
                Import Arts &amp; Culture Collection
              </h2>
              <p className="text-xs font-serif italic text-[#666]">
                Sync Google Sheets favorites, Arts &amp; Culture URLs, or explore curated presets
              </p>
            </div>
          </div>
          <button
            id="btn-close-importer"
            onClick={onClose}
            className="p-1.5 text-[#777] hover:text-[#1A1A1A] hover:bg-[#F0EEE6] transition-colors cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab selection */}
        <div className="flex border-b border-[#1A1A1A] bg-[#F9F8F4] px-6">
          <button
            id="tab-importer-presets"
            onClick={() => { setActiveTab('presets'); setError(null); }}
            className={`py-3 px-4 text-[10px] uppercase font-sans tracking-[0.2em] border-b-2 flex items-center gap-2 transition-all ${
              activeTab === 'presets'
                ? 'border-[#1A1A1A] text-[#1A1A1A] font-bold -mb-[1px]'
                : 'border-transparent text-[#777] hover:text-[#1A1A1A]'
            }`}
          >
            <Library className="w-3.5 h-3.5" />
            Curated Masterpiece Packs
          </button>

          <button
            id="tab-importer-sheets"
            onClick={() => { setActiveTab('sheets'); setError(null); }}
            className={`py-3 px-4 text-[10px] uppercase font-sans tracking-[0.2em] border-b-2 flex items-center gap-2 transition-all ${
              activeTab === 'sheets'
                ? 'border-[#1A1A1A] text-[#1A1A1A] font-bold -mb-[1px]'
                : 'border-transparent text-[#777] hover:text-[#1A1A1A]'
            }`}
          >
            <FileSpreadsheet className="w-3.5 h-3.5" />
            Google Sheet URL
          </button>

          <button
            id="tab-importer-paste"
            onClick={() => { setActiveTab('paste'); setError(null); }}
            className={`py-3 px-4 text-[10px] uppercase font-sans tracking-[0.2em] border-b-2 flex items-center gap-2 transition-all ${
              activeTab === 'paste'
                ? 'border-[#1A1A1A] text-[#1A1A1A] font-bold -mb-[1px]'
                : 'border-transparent text-[#777] hover:text-[#1A1A1A]'
            }`}
          >
            <Link className="w-3.5 h-3.5" />
            Paste Links / CSV
          </button>

          <button
            id="tab-importer-manual"
            onClick={() => { setActiveTab('manual'); setError(null); }}
            className={`py-3 px-4 text-[10px] uppercase font-sans tracking-[0.2em] border-b-2 flex items-center gap-2 transition-all ${
              activeTab === 'manual'
                ? 'border-[#1A1A1A] text-[#1A1A1A] font-bold -mb-[1px]'
                : 'border-transparent text-[#777] hover:text-[#1A1A1A]'
            }`}
          >
            <Plus className="w-3.5 h-3.5" />
            Manual Entry
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto flex-1 bg-[#FFFFFF]">
          {error && (
            <div className="mb-4 p-3.5 bg-rose-50 border border-rose-300 flex items-start gap-3 text-xs text-rose-900">
              <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
              <div>
                <p className="font-bold font-serif">Import Note</p>
                <p className="font-serif">{error}</p>
              </div>
            </div>
          )}

          {/* TAB 1: PRESETS */}
          {activeTab === 'presets' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <p className="text-xs font-serif italic text-[#666]">
                  Select from verified, museum-grade collections from Google Arts &amp; Culture:
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {PRESET_COLLECTIONS.map((preset) => (
                  <div
                    key={preset.id}
                    onClick={() => {
                      onSelectPreset(preset);
                      onClose();
                    }}
                    className="group bg-[#F9F8F4] hover:bg-[#F0EEE6] border border-[#1A1A1A] p-5 cursor-pointer transition-all duration-200 shadow-2xs hover:shadow-md flex flex-col justify-between"
                  >
                    <div>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-[9px] uppercase tracking-widest px-2 py-0.5 font-sans font-bold bg-[#1A1A1A] text-[#FDFBF7]">
                          {preset.badge}
                        </span>
                        <span className="text-[10px] text-[#777] font-sans font-semibold uppercase tracking-wider">
                          {preset.artworks.length} pieces
                        </span>
                      </div>
                      <h3 className="font-serif italic text-lg text-[#1A1A1A] group-hover:text-[#D4AF37] transition-colors">
                        {preset.name}
                      </h3>
                      <p className="text-xs font-serif text-[#555] mt-1 line-clamp-2 leading-relaxed">
                        {preset.description}
                      </p>
                    </div>

                    {/* Preview thumbs */}
                    <div className="mt-4 pt-3 border-t border-[#EBE8E0] flex items-center justify-between">
                      <div className="flex -space-x-2">
                        {preset.artworks.map((art) => (
                          <img
                            key={art.id}
                            src={art.imageUrl}
                            alt={art.title}
                            className="w-7 h-7 object-cover border border-[#1A1A1A]"
                          />
                        ))}
                      </div>
                      <span className="text-[10px] uppercase font-sans font-bold tracking-widest text-[#1A1A1A] flex items-center gap-1 group-hover:translate-x-0.5 transition-transform">
                        Load Pack <ArrowRight className="w-3 h-3 text-[#D4AF37]" />
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 2: GOOGLE SHEETS */}
          {activeTab === 'sheets' && (
            <div className="space-y-4">
              <div className="p-4 bg-[#F9F8F4] border border-[#1A1A1A] space-y-2">
                <h4 className="text-xs font-sans uppercase tracking-widest font-bold text-[#1A1A1A] flex items-center gap-2">
                  <FileSpreadsheet className="w-4 h-4 text-[#D4AF37]" />
                  Google Sheet Setup Instructions
                </h4>
                <p className="text-xs font-serif text-[#555] leading-relaxed">
                  1. In Google Sheets, click <strong className="text-[#1A1A1A]">Share &rarr; Anyone with the link (Viewer)</strong>.<br />
                  2. Ensure your sheet has columns such as: <code className="font-mono text-[#1A1A1A] bg-[#EBE8E0] px-1">Title</code>, <code className="font-mono text-[#1A1A1A] bg-[#EBE8E0] px-1">Artist</code>, <code className="font-mono text-[#1A1A1A] bg-[#EBE8E0] px-1">Google Arts URL</code>, <code className="font-mono text-[#1A1A1A] bg-[#EBE8E0] px-1">Image URL</code>, <code className="font-mono text-[#1A1A1A] bg-[#EBE8E0] px-1">Notes</code>.<br />
                  3. Paste the browser URL of the Google Sheet below.
                </p>
              </div>

              <div>
                <label className="block text-[10px] font-sans uppercase tracking-wider font-bold text-[#1A1A1A] mb-1.5">
                  Google Sheet URL
                </label>
                <input
                  type="url"
                  value={sheetUrl}
                  onChange={(e) => setSheetUrl(e.target.value)}
                  placeholder="https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit"
                  className="w-full px-3.5 py-2.5 bg-[#FFFFFF] border border-[#1A1A1A] focus:border-[#D4AF37] focus:outline-hidden text-xs text-[#1A1A1A] placeholder-[#999]"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={onClose}
                  className="px-4 py-2 text-[10px] uppercase font-sans tracking-wider text-[#777] hover:text-[#1A1A1A]"
                >
                  Cancel
                </button>
                <button
                  id="btn-submit-sheet-import"
                  type="button"
                  onClick={handleImportSheet}
                  disabled={isLoading || !sheetUrl.trim()}
                  className="flex items-center gap-2 px-5 py-2.5 text-[10px] uppercase font-sans font-bold tracking-[0.2em] text-[#FDFBF7] bg-[#1A1A1A] hover:bg-[#333] disabled:opacity-50 transition-colors shadow-xs cursor-pointer"
                >
                  {isLoading ? <Sparkles className="w-3.5 h-3.5 text-[#D4AF37] animate-spin" /> : <Check className="w-3.5 h-3.5 text-[#D4AF37]" />}
                  <span>{isLoading ? 'Reading Google Sheet...' : 'Import from Sheet'}</span>
                </button>
              </div>
            </div>
          )}

          {/* TAB 3: PASTE LINKS / CSV */}
          {activeTab === 'paste' && (
            <div className="space-y-4">
              <div>
                <label className="block text-[10px] font-sans uppercase tracking-wider font-bold text-[#1A1A1A] mb-1.5">
                  Paste Google Arts &amp; Culture Links, CSV, or Artwork Titles
                </label>
                <textarea
                  rows={8}
                  value={rawText}
                  onChange={(e) => setRawText(e.target.value)}
                  placeholder={`https://artsandculture.google.com/asset/the-starry-night/bgEuwDxel93-Pg\nhttps://artsandculture.google.com/asset/the-great-wave-off-kanagawa/fAFjhP81wbgMhQ\n"The Night Watch", "Rembrandt", "1642", "Dramatic chiaroscuro"\n"Composition VIII", "Wassily Kandinsky", "1923"`}
                  className="w-full p-3.5 bg-[#FFFFFF] border border-[#1A1A1A] focus:border-[#D4AF37] focus:outline-hidden text-xs font-mono text-[#1A1A1A] placeholder-[#999] leading-relaxed"
                />
                <p className="text-[11px] font-serif italic text-[#777] mt-1.5">
                  Supports one link/row per line. Links to Google Arts &amp; Culture assets are automatically enriched.
                </p>
              </div>

              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={onClose}
                  className="px-4 py-2 text-[10px] uppercase font-sans tracking-wider text-[#777] hover:text-[#1A1A1A]"
                >
                  Cancel
                </button>
                <button
                  id="btn-submit-paste-import"
                  type="button"
                  onClick={handleParsePaste}
                  disabled={!rawText.trim()}
                  className="flex items-center gap-2 px-5 py-2.5 text-[10px] uppercase font-sans font-bold tracking-[0.2em] text-[#FDFBF7] bg-[#1A1A1A] hover:bg-[#333] disabled:opacity-50 transition-colors shadow-xs cursor-pointer"
                >
                  <Sparkles className="w-3.5 h-3.5 text-[#D4AF37]" />
                  <span>Parse &amp; Import</span>
                </button>
              </div>
            </div>
          )}

          {/* TAB 4: MANUAL ENTRY */}
          {activeTab === 'manual' && (
            <form onSubmit={handleAddManual} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                <div>
                  <label className="block text-[10px] font-sans uppercase tracking-wider font-bold text-[#1A1A1A] mb-1">
                    Artwork Title *
                  </label>
                  <input
                    type="text"
                    required
                    value={manualTitle}
                    onChange={(e) => setManualTitle(e.target.value)}
                    placeholder="e.g. Impression, Sunrise"
                    className="w-full px-3 py-2 bg-[#FFFFFF] border border-[#1A1A1A] focus:border-[#D4AF37] text-xs text-[#1A1A1A]"
                  />
                </div>
                <div>
                  <label className="block text-[10px] font-sans uppercase tracking-wider font-bold text-[#1A1A1A] mb-1">
                    Artist / Creator
                  </label>
                  <input
                    type="text"
                    value={manualArtist}
                    onChange={(e) => setManualArtist(e.target.value)}
                    placeholder="e.g. Claude Monet"
                    className="w-full px-3 py-2 bg-[#FFFFFF] border border-[#1A1A1A] focus:border-[#D4AF37] text-xs text-[#1A1A1A]"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                <div>
                  <label className="block text-[10px] font-sans uppercase tracking-wider font-bold text-[#1A1A1A] mb-1">
                    Year / Period
                  </label>
                  <input
                    type="text"
                    value={manualYear}
                    onChange={(e) => setManualYear(e.target.value)}
                    placeholder="e.g. 1872"
                    className="w-full px-3 py-2 bg-[#FFFFFF] border border-[#1A1A1A] focus:border-[#D4AF37] text-xs text-[#1A1A1A]"
                  />
                </div>
                <div>
                  <label className="block text-[10px] font-sans uppercase tracking-wider font-bold text-[#1A1A1A] mb-1">
                    Google Arts &amp; Culture URL
                  </label>
                  <input
                    type="url"
                    value={manualUrl}
                    onChange={(e) => setManualUrl(e.target.value)}
                    placeholder="https://artsandculture.google.com/asset/..."
                    className="w-full px-3 py-2 bg-[#FFFFFF] border border-[#1A1A1A] focus:border-[#D4AF37] text-xs text-[#1A1A1A]"
                  />
                </div>
              </div>

              <div>
                <label className="block text-[10px] font-sans uppercase tracking-wider font-bold text-[#1A1A1A] mb-1">
                  Image URL (High-res preview)
                </label>
                <input
                  type="url"
                  value={manualImage}
                  onChange={(e) => setManualImage(e.target.value)}
                  placeholder="https://... image link"
                  className="w-full px-3 py-2 bg-[#FFFFFF] border border-[#1A1A1A] focus:border-[#D4AF37] text-xs text-[#1A1A1A]"
                />
              </div>

              <div>
                <label className="block text-[10px] font-sans uppercase tracking-wider font-bold text-[#1A1A1A] mb-1">
                  User Notes / Curatorial Impressions
                </label>
                <textarea
                  rows={3}
                  value={manualNotes}
                  onChange={(e) => setManualNotes(e.target.value)}
                  placeholder="Why do you love this piece? (e.g. Vibrant solar disc contrasting against misty twilight water)"
                  className="w-full p-2.5 bg-[#FFFFFF] border border-[#1A1A1A] focus:border-[#D4AF37] text-xs text-[#1A1A1A]"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={onClose}
                  className="px-4 py-2 text-[10px] uppercase font-sans tracking-wider text-[#777] hover:text-[#1A1A1A]"
                >
                  Cancel
                </button>
                <button
                  id="btn-submit-manual-art"
                  type="submit"
                  className="flex items-center gap-2 px-5 py-2.5 text-[10px] uppercase font-sans font-bold tracking-[0.2em] text-[#FDFBF7] bg-[#1A1A1A] hover:bg-[#333] transition-colors shadow-xs cursor-pointer"
                >
                  <Plus className="w-3.5 h-3.5 text-[#D4AF37]" />
                  <span>Add Artwork</span>
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
