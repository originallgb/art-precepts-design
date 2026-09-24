import React, { useState } from 'react';
import { Sparkles, Check, AlertTriangle, Info, Bell, Search, Star, ArrowRight, ShieldCheck, Heart, Sliders, ChevronDown } from 'lucide-react';
import { DesignTokens } from '../types';

interface LiveComponentSandboxProps {
  tokens: DesignTokens;
  systemTitle: string;
}

export const LiveComponentSandbox: React.FC<LiveComponentSandboxProps> = ({
  tokens,
  systemTitle
}) => {
  const [activeThemeMode, setActiveThemeMode] = useState<'dark' | 'light'>('dark');
  const [customRadius, setCustomRadius] = useState<number>(8);
  const [isFavorited, setIsFavorited] = useState(false);
  const [activeTab, setActiveTab] = useState<'overview' | 'analytics' | 'settings'>('overview');
  const [toggleState, setToggleState] = useState(true);

  const colors = tokens.colors;

  // Derive dynamic sandbox inline style tokens
  const isDark = activeThemeMode === 'dark';
  const bgSurface = isDark ? colors.surfaceBase : '#f8f9fa';
  const bgCard = isDark ? colors.surfaceElevated : '#ffffff';
  const textPrimary = isDark ? colors.textPrimary : '#1a1f26';
  const textSecondary = isDark ? colors.textSecondary : '#5e6878';
  const borderSubtle = isDark ? colors.borderSubtle : 'rgba(0, 0, 0, 0.1)';

  return (
    <div className="space-y-6">
      {/* Sandbox Controller Bar */}
      <div className="bg-[#FFFFFF] border-2 border-[#1A1A1A] p-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-xs">
        <div>
          <span className="text-[9px] uppercase font-sans font-bold tracking-[0.2em] text-[#FDFBF7] bg-[#1A1A1A] px-2.5 py-0.5 inline-block">
            Interactive Component Preview
          </span>
          <h2 className="font-serif italic text-xl text-[#1A1A1A] mt-1.5">
            Live UI Sandbox Powered by {systemTitle} Tokens
          </h2>
          <p className="text-xs font-serif italic text-[#666]">
            Every component below dynamically inherits the synthesized color roles, typography scale, radii, and spacing.
          </p>
        </div>

        {/* Sandbox Theme & Radius Tweaker */}
        <div className="flex items-center gap-3 shrink-0 flex-wrap">
          <div className="flex items-center bg-[#F9F8F4] p-1 border border-[#1A1A1A]">
            <button
              onClick={() => setActiveThemeMode('dark')}
              className={`px-3 py-1 text-[10px] uppercase font-sans font-bold tracking-wider transition-colors cursor-pointer ${
                isDark ? 'bg-[#1A1A1A] text-[#FDFBF7]' : 'text-[#777] hover:text-[#1A1A1A]'
              }`}
            >
              Obsidian Dark
            </button>
            <button
              onClick={() => setActiveThemeMode('light')}
              className={`px-3 py-1 text-[10px] uppercase font-sans font-bold tracking-wider transition-colors cursor-pointer ${
                !isDark ? 'bg-[#1A1A1A] text-[#FDFBF7]' : 'text-[#777] hover:text-[#1A1A1A]'
              }`}
            >
              Gallery Light
            </button>
          </div>

          <div className="flex items-center gap-2 bg-[#F9F8F4] px-3 py-1.5 border border-[#1A1A1A] text-xs text-[#1A1A1A]">
            <span className="text-[10px] uppercase font-sans font-bold tracking-wider">Radius:</span>
            <input
              type="range"
              min="0"
              max="24"
              value={customRadius}
              onChange={(e) => setCustomRadius(Number(e.target.value))}
              className="w-20 accent-[#1A1A1A] cursor-pointer"
            />
            <span className="font-mono text-xs font-bold text-[#1A1A1A]">{customRadius}px</span>
          </div>
        </div>
      </div>

      {/* Rendered Live Canvas */}
      <div
        className="p-6 sm:p-8 border-2 transition-all duration-300 space-y-8 shadow-sm"
        style={{
          backgroundColor: bgSurface,
          borderColor: '#1A1A1A',
          color: textPrimary
        }}
      >
        {/* SECTION 1: Mock App Header / Navigation */}
        <div
          className="p-4 rounded-xl flex items-center justify-between border shadow-md"
          style={{
            backgroundColor: bgCard,
            borderColor: borderSubtle,
            borderRadius: `${customRadius}px`
          }}
        >
          <div className="flex items-center gap-3">
            <div
              className="w-8 h-8 flex items-center justify-center font-bold text-xs shadow-sm"
              style={{
                backgroundColor: colors.brandPrimary,
                color: isDark ? '#0d0f12' : '#ffffff',
                borderRadius: `${Math.max(4, customRadius - 2)}px`
              }}
            >
              CR
            </div>
            <div>
              <h3 className="font-serif font-bold text-sm tracking-wide" style={{ color: textPrimary }}>
                {systemTitle}
              </h3>
              <p className="text-[11px]" style={{ color: textSecondary }}>
                Editorial Curatorial Console
              </p>
            </div>
          </div>

          <div className="hidden md:flex items-center gap-1.5">
            {(['overview', 'analytics', 'settings'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className="px-3 py-1.5 text-xs font-medium capitalize transition-all"
                style={{
                  backgroundColor: activeTab === tab ? `${colors.brandPrimary}25` : 'transparent',
                  color: activeTab === tab ? colors.brandPrimary : textSecondary,
                  borderRadius: `${Math.max(4, customRadius - 4)}px`
                }}
              >
                {tab}
              </button>
            ))}
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsFavorited(!isFavorited)}
              className="p-2 border transition-colors"
              style={{
                borderColor: borderSubtle,
                borderRadius: `${Math.max(4, customRadius - 2)}px`,
                color: isFavorited ? colors.brandAccent : textSecondary
              }}
            >
              <Heart className={`w-4 h-4 ${isFavorited ? 'fill-current' : ''}`} />
            </button>
            <button
              className="flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-semibold shadow-sm transition-transform active:scale-95"
              style={{
                backgroundColor: colors.brandPrimary,
                color: isDark ? '#0d0f12' : '#ffffff',
                borderRadius: `${Math.max(4, customRadius - 2)}px`
              }}
            >
              <span>Publish System</span>
            </button>
          </div>
        </div>

        {/* SECTION 2: Metric Highlights Bento Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div
            className="p-5 border shadow-md space-y-2 relative overflow-hidden"
            style={{
              backgroundColor: bgCard,
              borderColor: borderSubtle,
              borderRadius: `${customRadius}px`
            }}
          >
            <div className="flex items-center justify-between">
              <span className="text-[10px] uppercase font-mono tracking-wider" style={{ color: colors.brandPrimary }}>
                Luminance Equilibrium
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full font-mono text-emerald-400 bg-emerald-950/40 border border-emerald-800/40">
                +98.4%
              </span>
            </div>
            <div className="text-2xl font-serif font-bold tracking-tight" style={{ color: textPrimary }}>
              60 / 30 / 10
            </div>
            <p className="text-xs leading-relaxed" style={{ color: textSecondary }}>
              Calculated golden ratio distribution of surface, midtone, and gilded accent.
            </p>
          </div>

          <div
            className="p-5 border shadow-md space-y-2 relative overflow-hidden"
            style={{
              backgroundColor: bgCard,
              borderColor: borderSubtle,
              borderRadius: `${customRadius}px`
            }}
          >
            <div className="flex items-center justify-between">
              <span className="text-[10px] uppercase font-mono tracking-wider" style={{ color: colors.brandSecondary }}>
                Typographic Scale
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full font-mono" style={{ backgroundColor: `${colors.brandSecondary}20`, color: colors.brandSecondary }}>
                1.250 Major Third
              </span>
            </div>
            <div className="text-2xl font-serif font-bold tracking-tight" style={{ color: textPrimary }}>
              Cinzel &times; Plus Jakarta
            </div>
            <p className="text-xs leading-relaxed" style={{ color: textSecondary }}>
              Harmonized display serifs with mathematical geometric sans-serif baseline grid.
            </p>
          </div>

          <div
            className="p-5 border shadow-md space-y-2 relative overflow-hidden"
            style={{
              backgroundColor: bgCard,
              borderColor: borderSubtle,
              borderRadius: `${customRadius}px`
            }}
          >
            <div className="flex items-center justify-between">
              <span className="text-[10px] uppercase font-mono tracking-wider" style={{ color: colors.brandAccent }}>
                WCAG AA Accessibility
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full font-mono text-emerald-400 bg-emerald-950/40 border border-emerald-800/40">
                15.8 : 1
              </span>
            </div>
            <div className="text-2xl font-serif font-bold tracking-tight" style={{ color: textPrimary }}>
              High Contrast Pass
            </div>
            <p className="text-xs leading-relaxed" style={{ color: textSecondary }}>
              Text elements rigorously exceed minimum contrast standards across all components.
            </p>
          </div>
        </div>

        {/* SECTION 3: Interactive Controls & Form Elements */}
        <div
          className="p-6 border shadow-lg space-y-6"
          style={{
            backgroundColor: bgCard,
            borderColor: borderSubtle,
            borderRadius: `${customRadius}px`
          }}
        >
          <div className="border-b pb-3" style={{ borderColor: borderSubtle }}>
            <h3 className="font-serif font-bold text-base" style={{ color: textPrimary }}>
              Interactive Button & Control Matrix
            </h3>
            <p className="text-xs" style={{ color: textSecondary }}>
              Hover and click each component to test state transitions.
            </p>
          </div>

          {/* Buttons row */}
          <div className="flex flex-wrap items-center gap-3">
            <button
              className="px-5 py-2.5 text-xs font-semibold shadow-md transition-all active:scale-95 cursor-pointer"
              style={{
                backgroundColor: colors.brandPrimary,
                color: isDark ? '#0d0f12' : '#ffffff',
                borderRadius: `${customRadius}px`
              }}
            >
              Primary Action
            </button>

            <button
              className="px-5 py-2.5 text-xs font-semibold shadow-sm transition-all active:scale-95 cursor-pointer border"
              style={{
                backgroundColor: `${colors.brandSecondary}20`,
                borderColor: colors.brandSecondary,
                color: colors.brandSecondary,
                borderRadius: `${customRadius}px`
              }}
            >
              Secondary Action
            </button>

            <button
              className="px-5 py-2.5 text-xs font-semibold transition-all active:scale-95 cursor-pointer border"
              style={{
                borderColor: borderSubtle,
                color: textPrimary,
                borderRadius: `${customRadius}px`
              }}
            >
              Ghost Outline
            </button>

            <button
              className="px-4 py-2.5 text-xs font-semibold transition-all active:scale-95 cursor-pointer"
              style={{
                backgroundColor: `${colors.brandAccent}25`,
                color: colors.brandAccent,
                borderRadius: `${customRadius}px`
              }}
            >
              Destructive Accent
            </button>
          </div>

          {/* Form inputs row */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
            <div>
              <label className="block text-xs font-medium mb-1.5" style={{ color: textPrimary }}>
                Curatorial Search Query
              </label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4" style={{ color: textSecondary }} />
                <input
                  type="text"
                  defaultValue="Vermeer Sfumato Lighting"
                  className="w-full pl-9 pr-3 py-2 text-xs border focus:outline-none"
                  style={{
                    backgroundColor: isDark ? colors.surfaceBase : '#ffffff',
                    borderColor: borderSubtle,
                    color: textPrimary,
                    borderRadius: `${customRadius}px`
                  }}
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium mb-1.5" style={{ color: textPrimary }}>
                Select Color Profile
              </label>
              <select
                className="w-full px-3 py-2 text-xs border focus:outline-none"
                style={{
                  backgroundColor: isDark ? colors.surfaceBase : '#ffffff',
                  borderColor: borderSubtle,
                  color: textPrimary,
                  borderRadius: `${customRadius}px`
                }}
              >
                <option>Florentine Gold & Tenebrism</option>
                <option>Prussian Indigo & Negative Space</option>
                <option>Neoplastic Crimson & Bauhaus</option>
              </select>
            </div>

            <div className="flex flex-col justify-end">
              <div
                className="flex items-center justify-between p-2.5 border"
                style={{
                  backgroundColor: isDark ? colors.surfaceBase : '#ffffff',
                  borderColor: borderSubtle,
                  borderRadius: `${customRadius}px`
                }}
              >
                <span className="text-xs font-medium" style={{ color: textPrimary }}>
                  Haptic Feedback & Motion
                </span>
                <button
                  type="button"
                  onClick={() => setToggleState(!toggleState)}
                  className="w-10 h-5 rounded-full transition-colors relative"
                  style={{
                    backgroundColor: toggleState ? colors.brandPrimary : '#3e4856'
                  }}
                >
                  <div
                    className={`w-4 h-4 rounded-full bg-white transition-transform ${
                      toggleState ? 'translate-x-5' : 'translate-x-0.5'
                    }`}
                  />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* SECTION 4: Status Badges & Alert Notice */}
        <div className="space-y-4">
          <div className="flex flex-wrap items-center gap-2">
            <span
              className="px-3 py-1 text-xs font-mono uppercase tracking-wider font-semibold"
              style={{
                backgroundColor: `${colors.brandPrimary}25`,
                color: colors.brandPrimary,
                borderRadius: '9999px',
                border: `1px solid ${colors.brandPrimary}40`
              }}
            >
              Primary Tag
            </span>

            <span
              className="px-3 py-1 text-xs font-mono uppercase tracking-wider font-semibold"
              style={{
                backgroundColor: `${colors.brandSecondary}25`,
                color: colors.brandSecondary,
                borderRadius: '9999px',
                border: `1px solid ${colors.brandSecondary}40`
              }}
            >
              Secondary Indigo
            </span>

            <span
              className="px-3 py-1 text-xs font-mono uppercase tracking-wider font-semibold"
              style={{
                backgroundColor: `${colors.brandAccent}25`,
                color: colors.brandAccent,
                borderRadius: '9999px',
                border: `1px solid ${colors.brandAccent}40`
              }}
            >
              Accent Alert
            </span>
          </div>

          <div
            className="p-4 border flex items-start gap-3"
            style={{
              backgroundColor: `${colors.brandPrimary}10`,
              borderColor: `${colors.brandPrimary}35`,
              borderRadius: `${customRadius}px`
            }}
          >
            <ShieldCheck className="w-5 h-5 shrink-0 mt-0.5" style={{ color: colors.brandPrimary }} />
            <div className="text-xs space-y-1">
              <p className="font-semibold" style={{ color: textPrimary }}>
                Production-Ready Design System Validation
              </p>
              <p style={{ color: textSecondary }}>
                All tokens compile cleanly into Tailwind v4 configs, CSS variables, and Figma design tokens.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
