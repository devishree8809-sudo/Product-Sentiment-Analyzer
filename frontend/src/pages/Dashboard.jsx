import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useProduct } from '../context/ProductContext';
import SummaryCard from '../components/SummaryCard/SummaryCard';
import { MessageSquare, ThumbsUp, ThumbsDown, HelpCircle, Star, BarChart3, ArrowRight, Activity } from 'lucide-react';
import './Pages.css';

export default function Dashboard() {
  const { productData } = useProduct();
  const navigate = useNavigate();

  if (!productData) {
    return (
      <div className="page-container dashboard-loading animate-fade-in">
        <div className="glass-panel" style={{ textAlign: 'center', padding: '48px 32px', maxWidth: '600px', margin: '40px auto', width: '100%' }}>
          <Activity size={48} className="text-gradient" style={{ marginBottom: '16px', display: 'inline-block' }} />
          <h2 style={{ fontFamily: 'var(--font-display)', marginBottom: '12px', fontSize: '1.75rem', fontWeight: 700 }}>No Product Analyzed</h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '24px', fontSize: '0.95rem' }}>
            You haven't searched for or analyzed any product yet. Search for a product to view the dashboard metrics.
          </p>
          <button className="cta-button" onClick={() => navigate('/search')} style={{ display: 'inline-flex', padding: '12px 28px', marginTop: 0 }}>
            Analyze a Product
          </button>
        </div>
      </div>
    );
  }

  const { product_name, summary, reviews } = productData;

  // Star generator helper for rating
  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalf = rating % 1 !== 0;

    for (let i = 1; i <= 5; i++) {
      if (i <= fullStars) {
        stars.push(<Star key={i} size={16} fill="var(--warning)" stroke="var(--warning)" />);
      } else if (i === fullStars + 1 && hasHalf) {
        stars.push(
          <div key={i} style={{ position: 'relative', display: 'inline-block' }}>
            <Star size={16} stroke="var(--text-muted)" />
            <div style={{ position: 'absolute', top: 0, left: 0, width: '50%', overflow: 'hidden' }}>
              <Star size={16} fill="var(--warning)" stroke="var(--warning)" />
            </div>
          </div>
        );
      } else {
        stars.push(<Star key={i} size={16} stroke="var(--text-muted)" />);
      }
    }
    return stars;
  };

  return (
    <div className="page-container dashboard-page animate-fade-in">
      {/* Product Banner */}
      <div className="dashboard-banner glass-panel">
        <div className="banner-details">
          <span className="banner-sub">Analysis Results for</span>
          <h1 className="banner-title text-gradient">{product_name}</h1>
        </div>
        <div className="rating-badge-container">
          <div className="rating-stars">
            {renderStars(summary.average_rating)}
          </div>
          <div className="rating-score">
            <span className="score-big">{summary.average_rating}</span>
            <span className="score-total">/ 5.0</span>
          </div>
        </div>
      </div>

      {/* Grid Metrics */}
      <div className="metrics-grid">
        <SummaryCard
          title="Total Reviews"
          value={summary.total_reviews}
          type="total"
          icon={MessageSquare}
        />
        <SummaryCard
          title="Positive Feedback"
          value={summary.positive}
          percentage={summary.positive_pct}
          type="positive"
          icon={ThumbsUp}
        />
        <SummaryCard
          title="Neutral Feedback"
          value={summary.neutral}
          percentage={summary.neutral_pct}
          type="neutral"
          icon={Activity}
        />
        <SummaryCard
          title="Negative Feedback"
          value={summary.negative}
          percentage={summary.negative_pct}
          type="negative"
          icon={ThumbsDown}
        />
      </div>

      {/* Navigation shortcuts */}
      <div className="shortcuts-grid">
        <div className="shortcut-card glass-panel" onClick={() => navigate('/reviews')}>
          <div className="shortcut-header">
            <h3>Recent Customer Feedback</h3>
            <ArrowRight size={18} className="shortcut-arrow" />
          </div>
          <p>Read what verified buyers are saying. Search, sort and filter reviews by sentiment badges.</p>
          <div className="recent-reviews-snippet">
            {reviews.slice(0, 2).map(r => (
              <div key={r.id} className="snippet-row">
                <span className={`badge ${r.sentiment.toLowerCase() === 'positive' ? 'badge-positive' : r.sentiment.toLowerCase() === 'neutral' ? 'badge-neutral' : 'badge-negative'}`}>
                  {r.sentiment}
                </span>
                <p className="snippet-text">"{r.text.substring(0, 60)}..."</p>
              </div>
            ))}
          </div>
        </div>

        <div className="shortcut-card glass-panel" onClick={() => navigate('/charts')}>
          <div className="shortcut-header">
            <h3>Explore Chart Visualizations</h3>
            <BarChart3 size={24} className="shortcut-chart-icon" />
          </div>
          <p>Analyze trends, distributions, and review counts using interactive visual charting elements.</p>
          <div className="chart-preview-bars">
            <div className="preview-bar positive" style={{ width: `${summary.positive_pct}%` }}></div>
            <div className="preview-bar neutral" style={{ width: `${summary.neutral_pct}%` }}></div>
            <div className="preview-bar negative" style={{ width: `${summary.negative_pct}%` }}></div>
          </div>
          <button className="shortcut-btn" onClick={(e) => { e.stopPropagation(); navigate('/charts'); }}>
            View Detailed Charts <ArrowRight size={14} style={{ marginLeft: 6 }} />
          </button>
        </div>
      </div>
    </div>
  );
}
