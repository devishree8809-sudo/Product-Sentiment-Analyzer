import React, { useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner';
import { useProduct } from '../context/ProductContext';
import './Pages.css';

export default function Loading() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { analyzeProduct } = useProduct();
  const productName = searchParams.get('product');

  useEffect(() => {
    if (!productName) {
      navigate('/search');
      return;
    }

    const startAnalysis = async () => {
      const timerPromise = new Promise(resolve => setTimeout(resolve, 1800));
      const apiPromise = analyzeProduct(productName);

      try {
        await Promise.all([timerPromise, apiPromise]);
        navigate('/dashboard');
      } catch (err) {
        console.error("Analysis failed:", err);
        navigate(`/not-found?product=${encodeURIComponent(productName)}`);
      }
    };

    startAnalysis();
  }, [productName, analyzeProduct, navigate]);

  return (
    <div className="page-container loading-page animate-fade-in">
      <div className="loading-card glass-panel">
        <LoadingSpinner />
      </div>
    </div>
  );
}
