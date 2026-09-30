import React from 'react';
import { BarChart3 } from 'lucide-react';
import './Footer.css';

export default function Footer() {
  return (
    <footer className="footer glass-panel">
      <div className="footer-container">
        <div className="footer-brand">
          <div className="footer-logo">
            <BarChart3 className="logo-icon" size={20} />
            <span className="logo-text">Sentima<span className="logo-dot">.</span></span>
          </div>
          <p className="footer-tagline">AI-driven Product Sentiment Analysis & Reviews Insights</p>
        </div>
        <div className="footer-meta">
          <div className="footer-links">
            <a href="#" className="footer-link">Terms</a>
            <a href="#" className="footer-link">Privacy</a>
            <a href="#" className="footer-link">API docs</a>
          </div>
          <p className="footer-copy">&copy; {new Date().getFullYear()} Sentima. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
