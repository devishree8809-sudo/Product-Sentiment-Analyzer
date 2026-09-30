import React, { useState, useMemo } from 'react';
import { Search, ChevronLeft, ChevronRight, Calendar, MessageSquare } from 'lucide-react';
import './ReviewTable.css';

export default function ReviewTable({ reviews = [] }) {
  const [filter, setFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  const filteredReviews = useMemo(() => {
    return reviews.filter(review => {
      const sentiment = review.sentiment || 'Neutral';
      const text = review.text || '';
      const matchesSentiment = filter === 'all' || sentiment.toLowerCase() === filter;
      const matchesSearch = text.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesSentiment && matchesSearch;
    });
  }, [reviews, filter, searchQuery]);

  const totalPages = Math.ceil(filteredReviews.length / itemsPerPage) || 1;
  const paginatedReviews = useMemo(() => {
    const startIdx = (currentPage - 1) * itemsPerPage;
    return filteredReviews.slice(startIdx, startIdx + itemsPerPage);
  }, [filteredReviews, currentPage]);

  const handleFilterChange = (newFilter) => {
    setFilter(newFilter);
    setCurrentPage(1);
  };

  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
    setCurrentPage(1);
  };

  const getSentimentBadgeClass = (sentiment) => {
    const clean = (sentiment || 'neutral').toLowerCase();
    if (clean === 'positive') return 'badge badge-positive';
    if (clean === 'neutral') return 'badge badge-neutral';
    return 'badge badge-negative';
  };

  return (
    <div className="review-table-container glass-panel">
      <div className="table-header-controls">
        <div className="sentiment-tabs">
          <button
            className={`tab-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => handleFilterChange('all')}
          >
            All ({reviews.length})
          </button>
          <button
            className={`tab-btn positive ${filter === 'positive' ? 'active' : ''}`}
            onClick={() => handleFilterChange('positive')}
          >
            Positive ({reviews.filter(r => (r.sentiment || '').toLowerCase() === 'positive').length})
          </button>
          <button
            className={`tab-btn neutral ${filter === 'neutral' ? 'active' : ''}`}
            onClick={() => handleFilterChange('neutral')}
          >
            Neutral ({reviews.filter(r => (r.sentiment || '').toLowerCase() === 'neutral').length})
          </button>
          <button
            className={`tab-btn negative ${filter === 'negative' ? 'active' : ''}`}
            onClick={() => handleFilterChange('negative')}
          >
            Negative ({reviews.filter(r => (r.sentiment || '').toLowerCase() === 'negative').length})
          </button>
        </div>

        <div className="table-search-wrapper">
          <Search size={16} className="table-search-icon" />
          <input
            type="text"
            placeholder="Search reviews..."
            value={searchQuery}
            onChange={handleSearchChange}
            className="table-search-input"
          />
        </div>
      </div>

      <div className="reviews-list">
        {paginatedReviews.length > 0 ? (
          paginatedReviews.map((review) => (
            <div key={review.id} className="review-row">
              <div className="review-meta-row">
                <div className="review-date-wrapper">
                  <Calendar size={14} className="date-icon" />
                  <span className="review-date">{review.date}</span>
                </div>
                <span className={getSentimentBadgeClass(review.sentiment)}>
                  {review.sentiment}
                </span>
              </div>
              <p className="review-text">"{review.text}"</p>
            </div>
          ))
        ) : (
          <div className="empty-reviews-state">
            <MessageSquare size={48} className="empty-icon" />
            <p className="empty-title">No reviews found</p>
            <p className="empty-subtitle">Try refining your search terms or filter selection.</p>
          </div>
        )}
      </div>

      {totalPages > 1 && (
        <div className="table-pagination">
          <button
            className="pagination-btn"
            disabled={currentPage === 1}
            onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
          >
            <ChevronLeft size={16} /> Prev
          </button>
          <span className="pagination-info">
            Page {currentPage} of {totalPages}
          </span>
          <button
            className="pagination-btn"
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
          >
            Next <ChevronRight size={16} />
          </button>
        </div>
      )}
    </div>
  );
}
