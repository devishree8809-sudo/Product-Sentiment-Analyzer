import React from 'react';
import { useNavigate } from 'react-router-dom';
import SearchBar from '../components/SearchBar/SearchBar';
import { Sparkles, HelpCircle } from 'lucide-react';
import './Pages.css';

export default function Search() {
  const navigate = useNavigate();

  const handleSearchSubmit = (productName) => {
    navigate(`/loading?product=${encodeURIComponent(productName)}`);
  };

  return (
    <div className="page-container search-page animate-fade-in">
      <div className="search-hero glass-panel">
        <div className="search-logo-wrapper">
          <Sparkles className="search-glow-icon" size={32} />
        </div>
        <h2 className="search-title">Start Sentiment Analysis</h2>
        <p className="search-subtitle">
          Type any product name below to fetch mock reviews and analyze customer satisfaction metrics.
        </p>

        <SearchBar onSearch={handleSearchSubmit} />
      </div>

      <div className="search-info-card glass-panel">
        <div className="info-item">
          <HelpCircle size={18} className="info-icon" />
          <div>
            <h4>How it works</h4>
            <p>Our analyzer fetches customer reviews from retail databases and uses sentiment analysis to score feedback, providing actionable summaries.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
