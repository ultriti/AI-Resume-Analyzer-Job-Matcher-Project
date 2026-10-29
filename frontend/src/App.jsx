import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import PredictPage from "./pages/predict/PredictPage";
import ResumePage from "./pages/resume/ResumePage";

const App = () => {
  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<PredictPage />} />
            <Route path="/predict" element={<PredictPage />} />
            <Route path="/resume" element={<ResumePage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
};

function Footer() {
  return (
    <footer className="border-t border-[var(--color-border)] py-6 text-center">
      <p className="text-[var(--color-text-muted)] text-sm">
        Resume<span className="text-[var(--color-accent)] font-semibold">AI</span>
        {" · "}NLP-powered Job Category Classification · BiGRU Deep Learning
      </p>
    </footer>
  );
}

export default App;
