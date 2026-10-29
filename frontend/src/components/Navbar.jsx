import React, { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";

export default function Navbar() {
  const [health, setHealth] = useState(null); // null = loading, true = ok, false = down

  useEffect(() => {
    let cancelled = false;
    async function check() {
      try {
        const res = await fetch("/health");
        const data = await res.json();
        if (!cancelled) setHealth(data.model_loaded === true);
      } catch {
        if (!cancelled) setHealth(false);
      }
    }
    check();
    const id = setInterval(check, 30_000);
    return () => { cancelled = true; clearInterval(id); };
  }, []);

  const linkClass = ({ isActive }) =>
    `flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold transition-all duration-200 ${
      isActive
        ? "bg-[var(--color-accent)]/15 text-[var(--color-accent-light)] shadow-[0_0_12px_rgba(108,92,231,0.15)]"
        : "text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-white/[0.04]"
    }`;

  return (
    <nav className="sticky top-0 z-50 border-b border-[var(--color-border)] bg-[var(--color-bg-primary)]/80 backdrop-blur-xl">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <NavLink to="/" className="flex items-center gap-3 group">
          <span className="w-9 h-9 rounded-xl bg-gradient-to-br from-[var(--color-accent)] to-[var(--color-accent-dark)] flex items-center justify-center shadow-lg shadow-[var(--color-accent)]/20 group-hover:shadow-[var(--color-accent)]/40 transition-shadow duration-300">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
              <line x1="16" y1="13" x2="8" y2="13" />
              <line x1="16" y1="17" x2="8" y2="17" />
            </svg>
          </span>
          <span className="text-lg font-bold text-[var(--color-text-primary)]">
            Resume<span className="text-[var(--color-accent-light)]">AI</span>
          </span>
        </NavLink>

        {/* Links */}
        <div className="flex items-center gap-2">
          <NavLink to="/predict" end className={linkClass}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>
            Text Predict
          </NavLink>
          <NavLink to="/resume" className={linkClass}>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            Resume Analyze
          </NavLink>

          {/* Health dot */}
          <div className="ml-3 flex items-center gap-2 px-3 py-1.5 rounded-full border text-xs font-bold"
            style={{
              borderColor: health === true ? "var(--color-success-border)" : health === false ? "var(--color-danger-border)" : "var(--color-border)",
              background: health === true ? "var(--color-success-bg)" : health === false ? "var(--color-danger-bg)" : "transparent",
              color: health === true ? "var(--color-success)" : health === false ? "var(--color-danger)" : "var(--color-text-muted)",
            }}
          >
            <span
              className={`w-2 h-2 rounded-full ${health === null ? "dot-pulse" : ""}`}
              style={{
                background: health === true ? "var(--color-success)" : health === false ? "var(--color-danger)" : "var(--color-text-muted)",
                boxShadow: health === true ? "0 0 8px rgba(52,211,153,0.4)" : "none",
              }}
            />
            {health === null ? "Checking…" : health ? "Model Ready" : "Offline"}
          </div>
        </div>
      </div>
    </nav>
  );
}
