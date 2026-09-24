import React, { useState } from 'react';
import Markdown from 'react-markdown';
import { Download, Copy, Check, FileText, Code2, Sparkles, Palette, Layers, Sliders, ExternalLink, ShieldCheck, FileCode } from 'lucide-react';
import { GeneratedDesignSystem } from '../types';

interface DesignSystemStudioProps {
  designSystem: GeneratedDesignSystem;
  onRegenerate: () => void;
  isGenerating?: boolean;
}

export const DesignSystemStudio: React.FC<DesignSystemStudioProps> = ({
  designSystem,
  onRegenerate,
  isGenerating
}) => {
  const [activeSubTab, setActiveSubTab] = useState<'markdown' | 'tokens' | 'export'>('markdown');
  const [viewRawMarkdown, setViewRawMarkdown] = useState(false);
  const [copiedState, setCopiedState] = useState<string | null>(null);

  const handleCopy = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    setCopiedState(label);
    setTimeout(() => setCopiedState(null), 2500);
  };

  const handleDownloadMarkdown = () => {
    const blob = new Blob([designSystem.markdownContent], { type: 'text/markdown;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'design.md';
    link.click();
    URL.revokeObjectURL(url);
  };

  const cssVariablesSnippet = `:root {
  /* Surface Tokens */
  --surface-base: ${designSystem.tokens?.colors?.surfaceBase || '#0d0f12'};
  --surface-elevated: ${designSystem.tokens?.colors?.surfaceElevated || '#161a20'};
  --surface-overlay: ${designSystem.tokens?.colors?.surfaceOverlay || '#1e242c'};

  /* Brand Tokens */
  --brand-primary: ${designSystem.tokens?.colors?.brandPrimary || '#d4af37'};
  --brand-secondary: ${designSystem.tokens?.colors?.brandSecondary || '#2b5876'};
  --brand-accent: ${designSystem.tokens?.colors?.brandAccent || '#c83424'};

  /* Typography Tokens */
  --text-primary: ${designSystem.tokens?.colors?.textPrimary || '#f2f4f8'};
  --text-secondary: ${designSystem.tokens?.colors?.textSecondary || '#9ea8b6'};
  --text-muted: ${designSystem.tokens?.colors?.textMuted || '#5e6878'};

  /* Stroke Tokens */
  --border-subtle: ${designSystem.tokens?.colors?.borderSubtle || 'rgba(212, 175, 55, 0.15)'};
  --border-focus: ${designSystem.tokens?.colors?.borderFocus || '#d4af37'};

  /* Radii */
  --radius-button: ${designSystem.tokens?.radii?.buttonRadius || '8px'};
  --radius-card: ${designSystem.tokens?.radii?.cardRadius || '12px'};
}`;

  const tailwindThemeSnippet = `@theme {
  --color-brand-primary: ${designSystem.tokens?.colors?.brandPrimary || '#d4af37'};
  --color-brand-secondary: ${designSystem.tokens?.colors?.brandSecondary || '#2b5876'};
  --color-brand-accent: ${designSystem.tokens?.colors?.brandAccent || '#c83424'};
  --color-surface-base: ${designSystem.tokens?.colors?.surfaceBase || '#0d0f12'};
  --color-surface-elevated: ${designSystem.tokens?.colors?.surfaceElevated || '#161a20'};
  --font-display: ${designSystem.tokens?.typography?.displayFont || 'Cinzel, serif'};
  --font-sans: ${designSystem.tokens?.typography?.bodyFont || 'Plus Jakarta Sans, sans-serif'};
}`;

  const figmaTokensJson = JSON.stringify(designSystem.tokens, null, 2);

  return (
    <div className="space-y-6">
      {/* Studio Header Bar */}
      <div className="bg-[#FFFFFF] border-2 border-[#1A1A1A] p-6 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <span className="text-[10px] uppercase tracking-[0.3em] font-sans font-semibold text-[#1A1A1A] border-l-4 border-[#D4AF37] pl-3">
              Generated Artifact &bull; Master Specification
            </span>
            <span className="text-[10px] uppercase font-mono tracking-widest bg-[#F9F8F4] border border-[#EBE8E0] px-2 py-0.5 text-[#555]">
              design.md &bull; {new Date(designSystem.generatedAt).toLocaleDateString()}
            </span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-light tracking-tight italic text-[#1A1A1A]">
            {designSystem.title}
          </h1>
          <p className="text-xs font-serif italic text-[#555] max-w-2xl mt-1 leading-relaxed">
            {designSystem.subtitle}
          </p>
        </div>

        {/* Header Action Buttons */}
        <div className="flex flex-wrap items-center gap-2.5 shrink-0">
          <button
            id="btn-download-designmd"
            onClick={handleDownloadMarkdown}
            className="flex items-center gap-2 px-5 py-2.5 bg-[#1A1A1A] text-[#FDFBF7] text-[10px] uppercase tracking-[0.25em] font-sans hover:bg-[#333] transition-colors shadow-xs cursor-pointer"
          >
            <Download className="w-3.5 h-3.5 text-[#D4AF37]" />
            <span>Download design.md</span>
          </button>

          <button
            id="btn-copy-designmd"
            onClick={() => handleCopy(designSystem.markdownContent, 'markdown')}
            className="flex items-center gap-2 px-4 py-2.5 border border-[#1A1A1A] text-[#1A1A1A] text-[10px] uppercase tracking-[0.25em] font-sans hover:bg-[#F0EEE6] transition-colors cursor-pointer"
          >
            {copiedState === 'markdown' ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5 text-[#D4AF37]" />}
            <span>{copiedState === 'markdown' ? 'Copied' : 'Copy Markdown'}</span>
          </button>

          <button
            id="btn-regenerate-system"
            onClick={onRegenerate}
            disabled={isGenerating}
            className="flex items-center gap-2 px-4 py-2.5 border border-[#EBE8E0] text-[#777] hover:text-[#1A1A1A] hover:border-[#1A1A1A] text-[10px] uppercase tracking-[0.25em] font-sans transition-colors cursor-pointer disabled:opacity-50"
          >
            <Sparkles className={`w-3.5 h-3.5 ${isGenerating ? 'animate-spin' : ''}`} />
            <span>{isGenerating ? 'Synthesizing...' : 'Re-Generate'}</span>
          </button>
        </div>
      </div>

      {/* Sub-tab Switcher */}
      <div className="flex border-b-2 border-[#1A1A1A] bg-[#FFFFFF] px-4">
        <button
          id="subtab-markdown-doc"
          onClick={() => setActiveSubTab('markdown')}
          className={`py-3 px-5 text-[10px] uppercase font-sans tracking-[0.25em] border-b-2 flex items-center gap-2 transition-all ${
            activeSubTab === 'markdown'
              ? 'border-[#1A1A1A] text-[#1A1A1A] font-bold -mb-[2px]'
              : 'border-transparent text-[#888] hover:text-[#1A1A1A]'
          }`}
        >
          <FileText className="w-3.5 h-3.5" />
          design.md Document
        </button>

        <button
          id="subtab-tokens-view"
          onClick={() => setActiveSubTab('tokens')}
          className={`py-3 px-5 text-[10px] uppercase font-sans tracking-[0.25em] border-b-2 flex items-center gap-2 transition-all ${
            activeSubTab === 'tokens'
              ? 'border-[#1A1A1A] text-[#1A1A1A] font-bold -mb-[2px]'
              : 'border-transparent text-[#888] hover:text-[#1A1A1A]'
          }`}
        >
          <Palette className="w-3.5 h-3.5" />
          Token Architecture
        </button>

        <button
          id="subtab-export-code"
          onClick={() => setActiveSubTab('export')}
          className={`py-3 px-5 text-[10px] uppercase font-sans tracking-[0.25em] border-b-2 flex items-center gap-2 transition-all ${
            activeSubTab === 'export'
              ? 'border-[#1A1A1A] text-[#1A1A1A] font-bold -mb-[2px]'
              : 'border-transparent text-[#888] hover:text-[#1A1A1A]'
          }`}
        >
          <Code2 className="w-3.5 h-3.5" />
          Export Code Snippets
        </button>
      </div>

      {/* SUBTAB 1: MARKDOWN DOCUMENT */}
      {activeSubTab === 'markdown' && (
        <div className="bg-[#FFFFFF] border border-[#1A1A1A] overflow-hidden shadow-xs">
          <div className="flex items-center justify-between px-6 py-3 border-b border-[#EBE8E0] bg-[#F9F8F4]">
            <span className="text-[10px] font-mono uppercase tracking-widest text-[#555]">
              design.md &bull; Markdown Output
            </span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setViewRawMarkdown(!viewRawMarkdown)}
                className="text-[10px] uppercase tracking-wider font-sans px-3 py-1 bg-[#FFFFFF] text-[#1A1A1A] border border-[#1A1A1A] hover:bg-[#1A1A1A] hover:text-[#FDFBF7] transition-colors"
              >
                {viewRawMarkdown ? 'Formatted Reader' : 'Raw Markdown'}
              </button>
            </div>
          </div>

          <div className="p-6 sm:p-12">
            {viewRawMarkdown ? (
              <pre className="font-mono text-xs text-[#FDFBF7] bg-[#1A1A1A] p-6 overflow-x-auto whitespace-pre-wrap leading-relaxed border border-[#1A1A1A]">
                {designSystem.markdownContent}
              </pre>
            ) : (
              <div className="prose max-w-none text-xs sm:text-sm text-[#333] leading-relaxed space-y-6">
                <Markdown
                  components={{
                    h1: ({ children }) => (
                      <h1 className="text-3xl sm:text-4xl font-serif font-light italic text-[#1A1A1A] border-b-2 border-[#1A1A1A] pb-4 mt-6 mb-6 tracking-tight">
                        {children}
                      </h1>
                    ),
                    h2: ({ children }) => (
                      <h2 className="text-xl sm:text-2xl font-serif font-light italic text-[#1A1A1A] text-[#D4AF37] mt-10 mb-4 flex items-center gap-2 border-l-4 border-[#D4AF37] pl-3">
                        {children}
                      </h2>
                    ),
                    h3: ({ children }) => (
                      <h3 className="text-base font-serif font-bold text-[#1A1A1A] mt-6 mb-2">
                        {children}
                      </h3>
                    ),
                    p: ({ children }) => (
                      <p className="text-xs sm:text-sm font-serif text-[#333] leading-relaxed my-3">
                        {children}
                      </p>
                    ),
                    ul: ({ children }) => (
                      <ul className="list-disc pl-6 space-y-1.5 text-xs sm:text-sm font-serif text-[#333] my-3">
                        {children}
                      </ul>
                    ),
                    blockquote: ({ children }) => (
                      <blockquote className="p-5 bg-[#F9F8F4] border-l-4 border-[#D4AF37] text-xs sm:text-sm font-serif italic text-[#1A1A1A] my-4">
                        {children}
                      </blockquote>
                    ),
                    table: ({ children }) => (
                      <div className="overflow-x-auto my-6 border border-[#1A1A1A] bg-[#FFFFFF]">
                        <table className="w-full text-left text-xs border-collapse">
                          {children}
                        </table>
                      </div>
                    ),
                    th: ({ children }) => (
                      <th className="p-3 font-sans text-[10px] uppercase tracking-widest text-[#FDFBF7] bg-[#1A1A1A] border-b border-[#1A1A1A]">
                        {children}
                      </th>
                    ),
                    td: ({ children }) => (
                      <td className="p-3 text-xs font-serif text-[#1A1A1A] border-b border-[#EBE8E0]">
                        {children}
                      </td>
                    ),
                    code: ({ children, className }) => {
                      const isBlock = className?.includes('language-');
                      if (isBlock) {
                        return (
                          <div className="my-4 overflow-hidden border border-[#1A1A1A] bg-[#1A1A1A]">
                            <div className="flex items-center justify-between px-4 py-2 bg-[#262626] border-b border-[#333] text-[10px] font-mono uppercase tracking-wider text-[#D4AF37]">
                              <span>Code Snippet</span>
                              <button
                                onClick={() => handleCopy(String(children), 'code-block')}
                                className="text-[#FDFBF7] hover:underline cursor-pointer"
                              >
                                Copy
                              </button>
                            </div>
                            <pre className="p-4 font-mono text-xs text-[#D4AF37] overflow-x-auto">
                              <code>{children}</code>
                            </pre>
                          </div>
                        );
                      }
                      return (
                        <code className="px-1.5 py-0.5 bg-[#F4F1EA] text-[#1A1A1A] font-mono text-xs border border-[#EBE8E0]">
                          {children}
                        </code>
                      );
                    }
                  }}
                >
                  {designSystem.markdownContent}
                </Markdown>
              </div>
            )}
          </div>
        </div>
      )}

      {/* SUBTAB 2: TOKENS ARCHITECTURE */}
      {activeSubTab === 'tokens' && (
        <div className="space-y-6">
          {/* Color Tokens Matrix */}
          <div className="bg-[#FFFFFF] border border-[#1A1A1A] p-6 space-y-4 shadow-sm">
            <div className="flex items-center justify-between border-b border-[#EBE8E0] pb-3">
              <div>
                <h3 className="font-serif text-2xl font-light italic text-[#1A1A1A]">
                  Chromatic Token Matrix
                </h3>
                <p className="text-xs font-serif italic text-[#777]">
                  Standard semantic color tokens derived from master art compositions.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {Object.entries(designSystem.tokens?.colors || {}).map(([tokenKey, value]) => {
                const hexVal = String(value);
                return (
                  <div
                    key={tokenKey}
                    className="p-4 bg-[#F9F8F4] border border-[#EBE8E0] hover:border-[#1A1A1A] flex items-center justify-between gap-3 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className="w-10 h-10 border border-[#1A1A1A] shadow-xs shrink-0"
                        style={{ backgroundColor: hexVal }}
                      />
                      <div>
                        <p className="font-mono text-xs font-bold text-[#1A1A1A]">
                          --{tokenKey.replace(/([A-Z])/g, '-$1').toLowerCase()}
                        </p>
                        <p className="font-mono text-[11px] text-[#777]">
                          {hexVal}
                        </p>
                      </div>
                    </div>

                    <button
                      onClick={() => handleCopy(hexVal, tokenKey)}
                      className="p-1.5 text-[#777] hover:text-[#1A1A1A] transition-colors"
                      title="Copy HEX"
                    >
                      {copiedState === tokenKey ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4" />}
                    </button>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Typography and Spacing Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Typography */}
            <div className="bg-[#FFFFFF] border border-[#1A1A1A] p-6 space-y-4 shadow-sm">
              <h3 className="font-serif text-xl font-light italic text-[#1A1A1A] border-b border-[#EBE8E0] pb-2">
                Typography Architecture
              </h3>
              <div className="space-y-3 text-xs">
                <div className="p-3 bg-[#F9F8F4] border border-[#EBE8E0]">
                  <span className="text-[9px] text-[#777] uppercase font-sans tracking-widest font-bold">Display Font:</span>
                  <p className="font-serif text-base italic text-[#1A1A1A] mt-0.5">
                    {designSystem.tokens?.typography?.displayFont || 'Cinzel, Playfair Display'}
                  </p>
                </div>
                <div className="p-3 bg-[#F9F8F4] border border-[#EBE8E0]">
                  <span className="text-[9px] text-[#777] uppercase font-sans tracking-widest font-bold">Body Font:</span>
                  <p className="font-sans text-sm font-semibold text-[#1A1A1A] mt-0.5">
                    {designSystem.tokens?.typography?.bodyFont || 'Plus Jakarta Sans'}
                  </p>
                </div>
                <div className="p-3 bg-[#F9F8F4] border border-[#EBE8E0]">
                  <span className="text-[9px] text-[#777] uppercase font-sans tracking-widest font-bold">Monospace / Data:</span>
                  <p className="font-mono text-xs font-semibold text-[#1A1A1A] mt-0.5">
                    {designSystem.tokens?.typography?.monoFont || 'JetBrains Mono'}
                  </p>
                </div>
              </div>
            </div>

            {/* Curatorial Rules & Laws */}
            <div className="bg-[#FFFFFF] border border-[#1A1A1A] p-6 space-y-4 shadow-sm">
              <h3 className="font-serif text-xl font-light italic text-[#1A1A1A] border-b border-[#EBE8E0] pb-2">
                Curatorial Directives
              </h3>
              <div className="space-y-2.5 text-xs">
                {designSystem.tokens?.rules?.dos?.slice(0, 3).map((rule, rIdx) => (
                  <div key={rIdx} className="flex items-start gap-2 p-2.5 bg-emerald-50 border border-emerald-300 text-emerald-900">
                    <Check className="w-3.5 h-3.5 text-emerald-700 shrink-0 mt-0.5" />
                    <span className="font-serif">{rule}</span>
                  </div>
                ))}
                {designSystem.tokens?.rules?.donts?.slice(0, 3).map((rule, rIdx) => (
                  <div key={rIdx} className="flex items-start gap-2 p-2.5 bg-rose-50 border border-rose-300 text-rose-900">
                    <ShieldCheck className="w-3.5 h-3.5 text-rose-700 shrink-0 mt-0.5" />
                    <span className="font-serif">{rule}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* SUBTAB 3: EXPORT CODE SNIPPETS */}
      {activeSubTab === 'export' && (
        <div className="space-y-6">
          {/* CSS Variables */}
          <div className="bg-[#FFFFFF] border border-[#1A1A1A] p-6 space-y-3 shadow-sm">
            <div className="flex items-center justify-between border-b border-[#EBE8E0] pb-3">
              <div>
                <h3 className="font-serif text-xl font-light italic text-[#1A1A1A]">
                  CSS Custom Properties (`:root`)
                </h3>
                <p className="text-xs font-serif italic text-[#777]">
                  Paste into your global `src/index.css` or stylesheet.
                </p>
              </div>
              <button
                onClick={() => handleCopy(cssVariablesSnippet, 'css-vars')}
                className="flex items-center gap-1.5 px-4 py-2 text-[10px] uppercase tracking-wider font-sans font-bold text-[#FDFBF7] bg-[#1A1A1A] hover:bg-[#333] transition-colors cursor-pointer"
              >
                {copiedState === 'css-vars' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-[#D4AF37]" />}
                <span>{copiedState === 'css-vars' ? 'Copied' : 'Copy CSS'}</span>
              </button>
            </div>
            <pre className="font-mono text-xs text-[#D4AF37] bg-[#1A1A1A] p-4 overflow-x-auto border border-[#1A1A1A]">
              {cssVariablesSnippet}
            </pre>
          </div>

          {/* Tailwind CSS @theme */}
          <div className="bg-[#FFFFFF] border border-[#1A1A1A] p-6 space-y-3 shadow-sm">
            <div className="flex items-center justify-between border-b border-[#EBE8E0] pb-3">
              <div>
                <h3 className="font-serif text-xl font-light italic text-[#1A1A1A]">
                  Tailwind CSS v4 `@theme` Config
                </h3>
                <p className="text-xs font-serif italic text-[#777]">
                  Modern Tailwind directive for CSS tokens.
                </p>
              </div>
              <button
                onClick={() => handleCopy(tailwindThemeSnippet, 'tailwind-theme')}
                className="flex items-center gap-1.5 px-4 py-2 text-[10px] uppercase tracking-wider font-sans font-bold text-[#FDFBF7] bg-[#1A1A1A] hover:bg-[#333] transition-colors cursor-pointer"
              >
                {copiedState === 'tailwind-theme' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-[#D4AF37]" />}
                <span>{copiedState === 'tailwind-theme' ? 'Copied' : 'Copy Tailwind Config'}</span>
              </button>
            </div>
            <pre className="font-mono text-xs text-[#D4AF37] bg-[#1A1A1A] p-4 overflow-x-auto border border-[#1A1A1A]">
              {tailwindThemeSnippet}
            </pre>
          </div>

          {/* Figma Design Tokens JSON */}
          <div className="bg-[#FFFFFF] border border-[#1A1A1A] p-6 space-y-3 shadow-sm">
            <div className="flex items-center justify-between border-b border-[#EBE8E0] pb-3">
              <div>
                <h3 className="font-serif text-xl font-light italic text-[#1A1A1A]">
                  Figma Tokens / Tokens Studio JSON
                </h3>
                <p className="text-xs font-serif italic text-[#777]">
                  Standard structured JSON for importing into Figma or design token tools.
                </p>
              </div>
              <button
                onClick={() => handleCopy(figmaTokensJson, 'figma-tokens')}
                className="flex items-center gap-1.5 px-4 py-2 text-[10px] uppercase tracking-wider font-sans font-bold text-[#FDFBF7] bg-[#1A1A1A] hover:bg-[#333] transition-colors cursor-pointer"
              >
                {copiedState === 'figma-tokens' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-[#D4AF37]" />}
                <span>{copiedState === 'figma-tokens' ? 'Copied' : 'Copy JSON'}</span>
              </button>
            </div>
            <pre className="font-mono text-xs text-[#D4AF37] bg-[#1A1A1A] p-4 overflow-x-auto max-h-64 border border-[#1A1A1A]">
              {figmaTokensJson}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};
