import React, { useState, useRef, useCallback } from "react";
import ProbabilityBars from "../../components/ProbabilityBars";
import JobMatchCard from "../../components/JobMatchCard";

const CATEGORY_ICONS = {
  "Business": "💼",
  "Cloud & Infrastructure": "☁️",
  "Data & AI": "🤖",
  "Design": "🎨",
  "Marketing": "📢",
  "Product & Management": "📋",
  "Software Engineering": "💻",
};

export default function ResumePage() {
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const inputRef = useRef(null);

  const handleFile = useCallback((f) => {
    if (!f) return;
    if (!f.name.toLowerCase().endsWith(".pdf")) {
      setError("Please select a PDF file.");
      setFile(null);
      return;
    }
    setError("");
    setResult(null);
    setFile(f);
  }, []);

  function handleDrop(e) {
    e.preventDefault();
    setDragActive(false);
    const f = e.dataTransfer?.files?.[0];
    handleFile(f);
  }

  function handleDragOver(e) {
    e.preventDefault();
    setDragActive(true);
  }

  function handleDragLeave(e) {
    e.preventDefault();
    setDragActive(false);
  }

  function removeFile() {
    setFile(null);
    setResult(null);
    setError("");
    if (inputRef.current) inputRef.current.value = "";
  }

  async function handleAnalyze() {
    if (!file) {
      setError("Please choose a PDF resume to analyze.");
      return;
    }

    setError("");
    setResult(null);
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("/analyze-resume", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || "Analysis failed.");
      if (!data.all_probabilities || typeof data.all_probabilities !== "object") {
        throw new Error("Invalid response from server.");
      }
      if (!Array.isArray(data.job_analysis)) {
        throw new Error("Resume response missing role skill matches.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  const category = result?.prediction_category;
  const confidence = result ? (result.confidence * 100).toFixed(2) : 0;

  return (
    <div className="animate-fade-in">
      {/* Hero */}
      <section className="relative overflow-hidden py-20 px-6">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-[var(--color-pink)]/8 rounded-full blur-[120px] pointer-events-none" />

        <div className="relative max-w-3xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-[var(--color-pink)]/20 bg-[var(--color-pink)]/5 text-[var(--color-pink)] text-xs font-bold uppercase tracking-wider mb-6">
            <span className="w-1.5 h-1.5 rounded-full bg-[var(--color-pink)] dot-pulse" />
            PDF Resume Analysis
          </div>

          <h1 className="font-[var(--font-heading)] text-5xl md:text-6xl font-bold leading-[1.1] mb-5">
            Upload your resume,{" "}
            <em className="text-[var(--color-pink)] not-italic bg-gradient-to-r from-[var(--color-pink)] to-[var(--color-orange)] bg-clip-text text-transparent">
              see where you fit.
            </em>
          </h1>

          <p className="text-[var(--color-text-secondary)] text-lg leading-relaxed max-w-xl mx-auto">
            Drop a PDF resume and get an AI-powered breakdown: detected job title,
            extracted skills, predicted career category, and a ranked comparison across multiple roles.
          </p>
        </div>
      </section>

      {/* Card */}
      <section className="px-6 pb-16 -mt-4">
        <div className="max-w-2xl mx-auto">
          <div className="glass-card p-7 md:p-9">

            {/* Header */}
            <div className="flex items-start gap-4 mb-7">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[var(--color-pink)]/20 to-[var(--color-pink)]/5 border border-[var(--color-pink)]/15 flex items-center justify-center shrink-0">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--color-pink)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                  <polyline points="17 8 12 3 7 8"/>
                  <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
              </div>
              <div>
                <h2 className="text-xl font-bold text-[var(--color-text-primary)]">Resume Analysis</h2>
                <p className="text-sm text-[var(--color-text-secondary)] mt-1">
                  Upload a PDF resume to extract skills and match against job roles.
                </p>
              </div>
            </div>

            {/* Drop zone */}
            {!file && (
              <div
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onClick={() => inputRef.current?.click()}
                className={`relative rounded-xl border-2 border-dashed p-10 text-center cursor-pointer transition-all duration-300 ${
                  dragActive
                    ? "drag-active border-[var(--color-accent)] bg-[var(--color-accent-glow)]"
                    : "border-[var(--color-border)] hover:border-white/15 hover:bg-white/[0.02]"
                }`}
              >
                <input
                  ref={inputRef}
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={(e) => handleFile(e.target.files?.[0])}
                  className="hidden"
                />
                <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-[var(--color-accent)]/10 to-transparent border border-[var(--color-accent)]/10 flex items-center justify-center">
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="var(--color-accent-light)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="17 8 12 3 7 8"/>
                    <line x1="12" y1="3" x2="12" y2="15"/>
                  </svg>
                </div>
                <p className="text-sm font-semibold text-[var(--color-text-primary)] mb-1">
                  Drag & drop your PDF resume here
                </p>
                <p className="text-xs text-[var(--color-text-muted)]">
                  or click to browse files
                </p>
              </div>
            )}

            {/* File selected */}
            {file && (
              <div className="flex items-center justify-between gap-3 px-4 py-3 rounded-xl border border-[var(--color-accent)]/20 bg-[var(--color-accent)]/5 animate-fade-in">
                <div className="flex items-center gap-3 min-w-0">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--color-accent-light)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                  </svg>
                  <span className="text-sm font-medium text-[var(--color-text-primary)] truncate">{file.name}</span>
                  <span className="text-xs text-[var(--color-text-muted)] shrink-0">
                    {(file.size / 1024).toFixed(0)} KB
                  </span>
                </div>
                <button
                  onClick={removeFile}
                  className="w-7 h-7 rounded-lg hover:bg-white/10 flex items-center justify-center transition-colors cursor-pointer shrink-0"
                  title="Remove file"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--color-text-muted)" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
            )}

            {/* Analyze button */}
            <div className="mt-5 flex justify-end">
              <button
                onClick={handleAnalyze}
                disabled={loading || !file}
                className="btn-glow inline-flex items-center gap-2.5 px-6 py-3 rounded-xl bg-gradient-to-r from-[var(--color-pink)] to-[var(--color-accent-dark)] text-white text-sm font-bold shadow-lg shadow-[var(--color-pink)]/20 hover:shadow-[var(--color-pink)]/35 hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 transition-all duration-200 cursor-pointer"
              >
                {loading ? (
                  <>
                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-[spin_0.6s_linear_infinite]" />
                    Analyzing…
                  </>
                ) : (
                  <>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
                    Analyze Resume
                  </>
                )}
              </button>
            </div>

            {/* Error */}
            {error && (
              <div className="mt-5 flex items-center gap-3 px-4 py-3 rounded-xl border border-[var(--color-danger-border)] bg-[var(--color-danger-bg)] text-[var(--color-danger)] text-sm animate-fade-in">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
                {error}
              </div>
            )}

            {/* Result */}
            {result && (
              <div className="mt-8 pt-7 border-t border-[var(--color-border)] animate-fade-in-up">

                <div className="flex items-center justify-between mb-5">
                  <h3 className="text-lg font-bold text-[var(--color-text-primary)]">Analysis Result</h3>
                  <span className="text-[10px] font-bold uppercase tracking-wider px-3 py-1 rounded-full border border-[var(--color-pink)]/20 bg-[var(--color-pink)]/5 text-[var(--color-pink)]">
                    Resume Analysis
                  </span>
                </div>

                {/* Prediction card */}
                <div className="flex items-center gap-5 p-5 rounded-xl border border-[var(--color-border)] bg-white/[0.02]">
                  <div className="w-14 h-14 rounded-xl bg-[var(--color-pink)]/10 border border-[var(--color-pink)]/15 flex items-center justify-center text-2xl shrink-0">
                    {CATEGORY_ICONS[category] || "📄"}
                  </div>
                  <div className="flex-1 min-w-0">
                    <span className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider font-semibold">Predicted Category</span>
                    <h2 className="text-2xl font-bold text-[var(--color-text-primary)] mt-1 font-[var(--font-heading)]">{category}</h2>
                  </div>
                  <div className="text-right pl-5 border-l border-[var(--color-border)]">
                    <span className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider font-semibold">Confidence</span>
                    <p className="text-2xl font-extrabold text-[var(--color-pink)] mt-1 font-mono tabular-nums">{confidence}%</p>
                  </div>
                </div>

                {/* Resume details */}
                <div className="mt-6 p-5 rounded-xl border border-[var(--color-border)] bg-white/[0.015]">
                  <div className="flex flex-wrap gap-8 mb-5">
                    <div>
                      <span className="text-[11px] font-bold uppercase tracking-wider text-[var(--color-text-muted)]">Detected Job Title</span>
                      <p className="text-sm font-bold text-[var(--color-text-primary)] mt-1">{result.job_title || "Not detected"}</p>
                    </div>
                    <div>
                      <span className="text-[11px] font-bold uppercase tracking-wider text-[var(--color-text-muted)]">Skills Found</span>
                      <p className="text-sm font-bold text-[var(--color-text-primary)] mt-1">{result.skills?.length || 0}</p>
                    </div>
                  </div>

                  {/* Skill chips */}
                  {result.skills && result.skills.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {result.skills.map((skill) => (
                        <span key={skill} className="px-3 py-1.5 rounded-lg text-xs font-medium bg-[var(--color-accent)]/10 text-[var(--color-accent-light)] border border-[var(--color-accent)]/15">
                          {skill}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {/* Job Matches */}
                {result.job_analysis && result.job_analysis.length > 0 && (
                  <div className="mt-7">
                    <div className="mb-4">
                      <h4 className="text-sm font-bold text-[var(--color-text-primary)]">Role Skill Matches</h4>
                      <p className="text-xs text-[var(--color-text-secondary)] mt-1">Ranked by the share of required skills found in this resume.</p>
                    </div>
                    <div className="space-y-3">
                      {result.job_analysis.map((match, i) => (
                        <JobMatchCard key={match.role} match={match} defaultOpen={i === 0} />
                      ))}
                    </div>
                  </div>
                )}

                {/* Probabilities */}
                <div className="mt-7">
                  <h4 className="text-sm font-bold text-[var(--color-text-primary)] mb-4">Category Probabilities</h4>
                  <ProbabilityBars probabilities={result.all_probabilities} />
                </div>
              </div>
            )}
          </div>
        </div>
      </section>
    </div>
  );
}
