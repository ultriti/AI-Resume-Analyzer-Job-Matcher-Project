import React from "react";

/**
 * Renders a list of category probability bars.
 * @param {{ probabilities: Record<string, number> }} props
 */
export default function ProbabilityBars({ probabilities }) {
  if (!probabilities || Object.keys(probabilities).length === 0) return null;

  const sorted = Object.entries(probabilities).sort(([, a], [, b]) => b - a);
  const maxVal = sorted[0]?.[1] ?? 1;

  const barColors = [
    "from-[var(--color-accent)] to-[var(--color-accent-light)]",
    "from-cyan-500 to-cyan-400",
    "from-pink-500 to-pink-400",
    "from-emerald-500 to-emerald-400",
    "from-amber-500 to-amber-400",
    "from-orange-500 to-orange-400",
    "from-indigo-400 to-purple-400",
  ];

  return (
    <div className="space-y-3">
      {sorted.map(([label, value], i) => {
        const pct = (value * 100).toFixed(2);
        const widthPct = Math.max(1, (value / Math.max(maxVal, 0.01)) * 100);
        const isTop = i === 0;

        return (
          <div key={label} className="group">
            <div className="flex items-center justify-between mb-1.5">
              <span className={`text-sm ${isTop ? "text-[var(--color-text-primary)] font-semibold" : "text-[var(--color-text-secondary)]"}`}>
                {label}
              </span>
              <span className={`text-sm font-mono tabular-nums ${isTop ? "text-[var(--color-accent-light)] font-bold" : "text-[var(--color-text-muted)]"}`}>
                {pct}%
              </span>
            </div>
            <div className="h-2 rounded-full bg-white/[0.04] overflow-hidden">
              <div
                className={`h-full rounded-full bg-gradient-to-r ${barColors[i % barColors.length]} animate-bar-grow`}
                style={{ width: `${widthPct}%`, animationDelay: `${i * 80}ms` }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}
