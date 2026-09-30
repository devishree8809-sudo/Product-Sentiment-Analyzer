import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useProduct } from '../context/ProductContext';
import ReviewTable from '../components/ReviewTable/ReviewTable';
import { MessageSquare } from 'lucide-react';
import './Pages.css';

export default function Reviews() {
  const { productData } = useProduct();
  const navigate = useNavigate();

  if (!productData) {
    return (
      <div className="page-container reviews-loading animate-fade-in">
        <div className="glass-panel" style={{ textAlign: 'center', padding: '48px 32px', maxWidth: '600px', margin: '40px auto', width: '100%' }}>
          <MessageSquare size={48} className="text-gradient" style={{ marginBottom: '16px', display: 'inline-block' }} />
          <h2 style={{ fontFamily: 'var(--font-display)', marginBottom: '12px', fontSize: '1.75rem', fontWeight: 700 }}>No Reviews Found</h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '24px', fontSize: '0.95rem' }}>
            You haven't searched for or analyzed any product yet. Search for a product to browse customer reviews.
          </p>
          <button className="cta-button" onClick={() => navigate('/search')} style={{ display: 'inline-flex', padding: '12px 28px', marginTop: 0 }}>
            Analyze a Product
          </button>
        </div>
      </div>
    );
  }

  const { product_name, reviews } = productData;

  return (
    <div className="page-container reviews-page animate-fade-in">
      <div className="reviews-page-header glass-panel">
        <span className="header-subtitle">Review Database</span>
        <h1 className="header-title text-gradient">{product_name} Reviews</h1>
        <p className="header-desc">
          Browse individual verified customer feedback. Sort and filter comments by sentiment rating or search specific keywords.
        </p>
      </div>

      <ReviewTable reviews={reviews} />
    </div>
  );
}
