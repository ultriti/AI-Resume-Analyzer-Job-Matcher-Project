import React, { useState } from "react";
import ProbabilityBars from "../../components/ProbabilityBars";

const CATEGORY_ICONS = {
  "Business": "💼",
  "Cloud & Infrastructure": "☁️",
  "Data & AI": "🤖",
  "Design": "🎨",
  "Marketing": "📢",
  "Product & Management": "📋",
  "Software Engineering": "💻",
};

export default function PredictPage() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  async function handlePredict() {
    const trimmed = text.trim();
    if (!trimmed) {
      setError("Please enter some job-related text to predict a category.");
      setResult(null);
      return;
    }

    setError("");
    setResult(null);
    setLoading(true);

    try {
      const res = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: trimmed }),
      });
      const data = await res.json();

      if (!res.ok) throw new Error(data.detail || "Prediction failed.");
      if (!data.all_probabilities || typeof data.all_probabilities !== "object") {
        throw new Error("Invalid response from server.");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }

  const category = result?.prediction_emotion || result?.prediction_category;
  const confidence = result ? (result.confidence * 100).toFixed(2) : 0;

  return (
    <div className="animate-fade-in">
      {/* Hero */}
      <section className="relative overflow-hidden py-20 px-6">
        {/* Glow effect */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[300px] bg-[var(--color-accent)]/8 rounded-full blur-[120px] pointer-events-none" />

        <div className="relative max-w-3xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-[var(--color-accent)]/20 bg-[var(--color-accent)]/5 text-[var(--color-accent-light)] text-xs font-bold uppercase tracking-wider mb-6">
            <span className="w-1.5 h-1.5 rounded-full bg-[var(--color-accent-light)] dot-pulse" />
            BiGRU Deep Learning Model
          </div>

          <h1 className="font-[var(--font-heading)] text-5xl md:text-6xl font-bold leading-[1.1] mb-5">
            Predict your{" "}
            <em className="text-[var(--color-accent-light)] not-italic bg-gradient-to-r from-[var(--color-accent-light)] to-[var(--color-cyan)] bg-clip-text text-transparent">
              career category
            </em>{" "}
            from text.
          </h1>

          <p className="text-[var(--color-text-secondary)] text-lg leading-relaxed max-w-xl mx-auto">
            Enter job titles, skills, or a role description. Our trained neural network
            classifies it into one of 7 career categories in real-time.
          </p>
        </div>
      </section>

      {/* Card */}
      <section className="px-6 pb-16 -mt-4">
        <div className="max-w-2xl mx-auto">
          <div className="glass-card p-7 md:p-9">

            {/* Header */}
            <div className="flex items-start gap-4 mb-7">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[var(--color-accent)]/20 to-[var(--color-accent)]/5 border border-[var(--color-accent)]/15 flex items-center justify-center shrink-0">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="var(--color-accent-light)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
                </svg>
              </div>
              <div>
                <h2 className="text-xl font-bold text-[var(--color-text-primary)]">Text Category Prediction</h2>
                <p className="text-sm text-[var(--color-text-secondary)] mt-1">
                  Type a job description, skill set, or career summary below.
                </p>
              </div>
            </div>

            {/* Textarea */}
            <div>
              <label htmlFor="textInput" className="block text-sm font-semibold text-[var(--color-text-primary)] mb-2">
                Your text input
              </label>
              <textarea
                id="textInput"
                value={text}
                onChange={(e) => setText(e.target.value)}
                maxLength={2000}
                rows={5}
                placeholder="Example: Machine learning engineer skilled in Python, PyTorch, TensorFlow, deep learning and SQL."
                className="w-full px-4 py-3.5 rounded-xl border border-[var(--color-border)] bg-[var(--color-bg-input)] text-[var(--color-text-primary)] text-sm leading-relaxed placeholder:text-[var(--color-text-muted)] focus:outline-none focus:border-[var(--color-border-focus)] focus:ring-2 focus:ring-[var(--color-accent)]/15 transition-all duration-200 resize-y"
              />
              <div className="flex items-center justify-between mt-3">
                <span className="text-xs text-[var(--color-text-muted)] font-mono tabular-nums">
                  {text.length} / 2000
                </span>
                <button
                  onClick={handlePredict}
                  disabled={loading}
                  className="btn-glow inline-flex items-center gap-2.5 px-6 py-3 rounded-xl bg-gradient-to-r from-[var(--color-accent)] to-[var(--color-accent-dark)] text-white text-sm font-bold shadow-lg shadow-[var(--color-accent)]/20 hover:shadow-[var(--color-accent)]/35 hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-60 disabled:cursor-wait disabled:hover:translate-y-0 transition-all duration-200 cursor-pointer"
                >
                  {loading ? (
                    <>
                      <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-[spin_0.6s_linear_infinite]" />
                      Predicting…
                    </>
                  ) : (
                    <>
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                      Predict Category
                    </>
                  )}
                </button>
              </div>
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
                  <h3 className="text-lg font-bold text-[var(--color-text-primary)]">Classification Result</h3>
                  <span className="text-[10px] font-bold uppercase tracking-wider px-3 py-1 rounded-full border border-[var(--color-accent)]/20 bg-[var(--color-accent)]/5 text-[var(--color-accent-light)]">
                    Text Prediction
                  </span>
                </div>

                {/* Main result card */}
                <div className="flex items-center gap-5 p-5 rounded-xl border border-[var(--color-border)] bg-white/[0.02]">
                  <div className="w-14 h-14 rounded-xl bg-[var(--color-accent)]/10 border border-[var(--color-accent)]/15 flex items-center justify-center text-2xl shrink-0">
                    {CATEGORY_ICONS[category] || "💼"}
                  </div>
                  <div className="flex-1 min-w-0">
                    <span className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider font-semibold">Detected Category</span>
                    <h2 className="text-2xl font-bold text-[var(--color-text-primary)] mt-1 font-[var(--font-heading)]">{category}</h2>
                  </div>
                  <div className="text-right pl-5 border-l border-[var(--color-border)]">
                    <span className="text-xs text-[var(--color-text-muted)] uppercase tracking-wider font-semibold">Confidence</span>
                    <p className="text-2xl font-extrabold text-[var(--color-accent-light)] mt-1 font-mono tabular-nums">{confidence}%</p>
                  </div>
                </div>

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

      {/* How it works */}
      <section className="px-6 pb-24">
        <div className="max-w-5xl mx-auto grid md:grid-cols-[1fr_1.3fr] gap-16 items-center">
          <div>
            <span className="text-[11px] font-extrabold uppercase tracking-[2px] text-[var(--color-accent-light)]">How it works</span>
            <h2 className="text-3xl font-bold mt-3 mb-4 font-[var(--font-heading)] leading-snug">
              From raw text to a career category in seconds.
            </h2>
            <p className="text-[var(--color-text-secondary)] text-sm leading-relaxed">
              Your input is preprocessed, tokenized and fed into a Bidirectional GRU neural network trained on thousands of career profiles.
            </p>
          </div>
          <div className="grid grid-cols-3 gap-4">
            {[
              { n: "01", title: "Input",   desc: "Enter a job title, skill list, or role description." },
              { n: "02", title: "Process", desc: "Text is cleaned, tokenized, and padded to a fixed length." },
              { n: "03", title: "Predict", desc: "The BiGRU model predicts the most likely job category." },
            ].map((s) => (
              <div key={s.n} className="pt-4 border-t-2 border-[var(--color-accent)]/20 hover:border-[var(--color-accent)]/50 transition-colors duration-300">
                <span className="text-sm font-[var(--font-heading)] text-[var(--color-orange)]">{s.n}</span>
                <h3 className="text-sm font-bold mt-2 mb-1 text-[var(--color-text-primary)]">{s.title}</h3>
                <p className="text-xs text-[var(--color-text-secondary)] leading-relaxed">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
