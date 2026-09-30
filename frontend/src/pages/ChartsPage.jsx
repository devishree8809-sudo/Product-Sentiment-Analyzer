import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useProduct } from '../context/ProductContext';
import SentimentPieChart from '../components/Charts/SentimentPieChart';
import SentimentBarChart from '../components/Charts/SentimentBarChart';
import SentimentLineChart from '../components/Charts/SentimentLineChart';
import { BarChart3 } from 'lucide-react';
import './Pages.css';
import '../components/Charts/Charts.css';

export default function ChartsPage() {
  const { productData } = useProduct();
  const navigate = useNavigate();

  if (!productData) {
    return (
      <div className="page-container charts-loading animate-fade-in">
        <div className="glass-panel" style={{ textAlign: 'center', padding: '48px 32px', maxWidth: '600px', margin: '40px auto', width: '100%' }}>
          <BarChart3 size={48} className="text-gradient" style={{ marginBottom: '16px', display: 'inline-block' }} />
          <h2 style={{ fontFamily: 'var(--font-display)', marginBottom: '12px', fontSize: '1.75rem', fontWeight: 700 }}>No Sentiment Charts</h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '24px', fontSize: '0.95rem' }}>
            You haven't searched for or analyzed any product yet. Search for a product to view the charts and statistics.
          </p>
          <button className="cta-button" onClick={() => navigate('/search')} style={{ display: 'inline-flex', padding: '12px 28px', marginTop: 0 }}>
            Analyze a Product
          </button>
        </div>
      </div>
    );
  }

  const { product_name, charts_data } = productData;

  return (
    <div className="page-container charts-page animate-fade-in">
      <div className="charts-page-header glass-panel">
        <span className="header-subtitle">Analytics Charts</span>
        <h1 className="header-title text-gradient">{product_name} Sentiment Analysis</h1>
        <p className="header-desc">
          Interactive distribution sharing and historic sentiment tracking trends.
        </p>
      </div>

      <div className="charts-grid-layout">
        <div className="charts-row">
          <SentimentPieChart data={charts_data.distribution} />
          <SentimentBarChart data={charts_data.distribution} />
        </div>
        <div className="full-width-chart">
          <SentimentLineChart data={charts_data.timeline} />
        </div>
      </div>
    </div>
  );
}
