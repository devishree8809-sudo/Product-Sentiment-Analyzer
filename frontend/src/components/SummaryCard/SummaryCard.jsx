import React from 'react';
import './SummaryCard.css';

export default function SummaryCard({ title, value, percentage, type, icon: Icon }) {
  const getCardClass = () => {
    switch (type) {
      case 'positive': return 'card-positive';
      case 'neutral': return 'card-neutral';
      case 'negative': return 'card-negative';
      default: return 'card-total';
    }
  };

  return (
    <div className={`summary-card glass-panel ${getCardClass()}`}>
      <div className="card-header">
        <span className="card-title">{title}</span>
        <div className="card-icon-wrapper">
          {Icon && <Icon className="card-icon" size={20} />}
        </div>
      </div>
      <div className="card-body">
        <h2 className="card-value">{(value ?? 0).toLocaleString()}</h2>
        {percentage !== undefined && (
          <div className="card-percentage">
            <span className="pct-num">{percentage}%</span>
            <span className="pct-label">of reviews</span>
          </div>
        )}
      </div>
    </div>
  );
}
