import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowRight, BarChart3, MessageSquare, ShieldAlert, Sparkles } from 'lucide-react';
import './Pages.css';

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="page-container home-page animate-fade-in">
      <section className="hero-section">
        <div className="hero-badge">
          <Sparkles size={14} className="badge-sparkle-icon" />
          <span>AI-Powered Review Analysis</span>
        </div>
        <h1 className="hero-title">
          Product Sentiment <br />
          <span className="text-gradient">Analyzer & Dashboard</span>
        </h1>
        <p className="hero-subtitle">
          Instantly transform customer reviews into actionable insights. Understand what your customers are saying through advanced sentiment analysis and interactive visual metrics.
        </p>
        <button className="cta-button" onClick={() => navigate('/search')}>
          Analyze a Product <ArrowRight size={18} />
        </button>
      </section>

      <section className="features-section">
        <h2 className="section-title">Core Capabilities</h2>
        <div className="features-grid">
          <div className="feature-card glass-panel">
            <div className="feature-icon-wrapper pos">
              <Sparkles size={20} />
            </div>
            <h3>Sentiment Scoring</h3>
            <p>Analyze and categorize customer feedback into Positive, Neutral, and Negative segments automatically.</p>
          </div>

          <div className="feature-card glass-panel">
            <div className="feature-icon-wrapper bar">
              <BarChart3 size={20} />
            </div>
            <h3>Visual Insights</h3>
            <p>Explore sentiment trends, share distribution, and volumes with interactive Recharts diagrams.</p>
          </div>

          <div className="feature-card glass-panel">
            <div className="feature-icon-wrapper msg">
              <MessageSquare size={20} />
            </div>
            <h3>Review Explorer</h3>
            <p>Browse through filtered reviews, search key phrases, and analyze specific feedback badges.</p>
          </div>
        </div>
      </section>
    </div>
  );
}
