import React, { useState } from "react";

/**
 * Expandable job match card.
 * @param {{ match: { role: string, score: number, matched_skills: string[], missing_skills: string[] }, defaultOpen?: boolean }} props
 */
export default function JobMatchCard({ match, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen);
  const score = Number(match.score);

  return (
    <div
      className={`rounded-xl border transition-all duration-300 overflow-hidden ${
        open
          ? "border-[var(--color-accent)]/30 bg-[var(--color-accent)]/[0.03] shadow-lg shadow-[var(--color-accent)]/5"
          : "border-[var(--color-border)] bg-white/[0.02] hover:border-white/10"
      }`}
    >
      {/* Summary row */}
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between gap-4 px-5 py-4 cursor-pointer text-left"
      >
        <span className="text-sm font-bold text-[var(--color-text-primary)]">
          {match.role}
        </span>
        <div className="flex items-center gap-3">
          <span className="text-sm font-extrabold font-mono tabular-nums text-[var(--color-accent-light)]">
            {score.toFixed(1)}%
          </span>
          <svg
            width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
            strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"
            className={`text-[var(--color-text-muted)] transition-transform duration-300 ${open ? "rotate-180" : ""}`}
          >
            <polyline points="6 9 12 15 18 9" />
          </svg>
        </div>
      </button>

      {/* Progress bar */}
      <div className="px-5 pb-1">
        <div className="h-1.5 rounded-full bg-white/[0.04] overflow-hidden">
          <div
            className="h-full rounded-full bg-gradient-to-r from-[var(--color-accent)] to-[var(--color-accent-light)] animate-bar-grow"
            style={{ width: `${Math.max(0, Math.min(100, score))}%` }}
          />
        </div>
      </div>

      {/* Expanded details */}
      {open && (
        <div className="px-5 pt-4 pb-5 animate-fade-in">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {/* Matched */}
            <div>
              <h5 className="text-[11px] font-bold uppercase tracking-wider text-[var(--color-success)] mb-3">
                ✓ Matched Skills
              </h5>
              <div className="flex flex-wrap gap-2">
                {match.matched_skills.length === 0 ? (
                  <span className="text-xs text-[var(--color-text-muted)] italic">No matches yet</span>
                ) : (
                  match.matched_skills.map((s) => (
                    <span key={s} className="px-2.5 py-1 rounded-lg text-xs font-medium bg-[var(--color-success)]/10 text-[var(--color-success)] border border-[var(--color-success)]/15">
                      {s}
                    </span>
                  ))
                )}
              </div>
            </div>
            {/* Missing */}
            <div>
              <h5 className="text-[11px] font-bold uppercase tracking-wider text-[var(--color-orange)] mb-3">
                ↗ Skills to Build
              </h5>
              <div className="flex flex-wrap gap-2">
                {match.missing_skills.length === 0 ? (
                  <span className="text-xs text-[var(--color-text-muted)] italic">All listed skills matched!</span>
                ) : (
                  match.missing_skills.map((s) => (
                    <span key={s} className="px-2.5 py-1 rounded-lg text-xs font-medium bg-[var(--color-orange)]/10 text-[var(--color-orange)] border border-[var(--color-orange)]/15">
                      {s}
                    </span>
                  ))
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
