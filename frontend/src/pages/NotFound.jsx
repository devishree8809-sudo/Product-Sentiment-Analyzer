import React from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { AlertCircle, ArrowLeft } from 'lucide-react';
import './Pages.css';

export default function NotFound() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const productName = searchParams.get('product') || 'the specified product';

  return (
    <div className="page-container search-page animate-fade-in">
      <div className="search-hero glass-panel" style={{ maxWidth: '650px', padding: '40px 32px' }}>
        <div className="search-logo-wrapper" style={{ background: 'rgba(239, 68, 68, 0.1)', borderColor: 'rgba(239, 68, 68, 0.25)', color: 'var(--danger)' }}>
          <AlertCircle size={32} style={{ filter: 'drop-shadow(0 0 8px rgba(239, 68, 68, 0.5))' }} />
        </div>

        <h2 className="search-title" style={{ marginTop: '12px' }}>Product Not Found</h2>

        <p className="search-subtitle" style={{ fontSize: '1.05rem', margin: '8px 0 20px 0', maxWidth: '100%' }}>
          We couldn't find any sentiment records or reviews for <strong style={{ color: 'var(--text-primary)' }}>"{productName}"</strong> in our database.
        </p>

        <div className="search-info-card glass-panel" style={{ background: 'rgba(255,255,255,0.01)', border: '1px solid rgba(255,255,255,0.05)', textAlign: 'left', width: '100%', padding: '18px' }}>
          <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '8px' }}>Suggestions:</h4>
          <ul style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', paddingLeft: '20px', lineHeight: '1.6' }}>
            <li>Verify the spelling of your query and try again.</li>
            <li>Try searching for partial matches like <strong>"Apple"</strong>, <strong>"iPhone"</strong>, or <strong>"Motorola"</strong>.</li>
            <li>Ensure the MongoDB database has been seeded using the database script.</li>
          </ul>
        </div>

        <button
          className="cta-button"
          onClick={() => navigate('/search')}
          style={{ marginTop: '24px', padding: '12px 28px', fontSize: '0.95rem' }}
        >
          <ArrowLeft size={16} /> Back to Search
        </button>
      </div>
    </div>
  );
}
