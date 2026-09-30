import React, { useState, useEffect } from 'react';
import './LoadingSpinner.css';

export default function LoadingSpinner() {
  const [stage, setStage] = useState(0);
  const stages = [
    "Searching product databases...",
    "Fetching customer reviews...",
    "Analyzing sentiments with AI models...",
    "Compiling dashboard statistics..."
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      setStage((prevStage) => (prevStage < stages.length - 1 ? prevStage + 1 : prevStage));
    }, 450);

    return () => clearInterval(timer);
  }, []);

  return (
    <div className="loading-spinner-container">
      <div className="spinner-wrapper">
        <div className="outer-ring"></div>
        <div className="inner-ring"></div>
        <div className="center-dot"></div>
      </div>
      <div className="loading-text-wrapper">
        <h3 className="loading-title">Processing</h3>
        <p className="loading-subtitle">{stages[stage]}</p>
        <div className="loading-progress-bar">
          <div className="loading-progress-fill" style={{ width: `${(stage + 1) * 25}%` }}></div>
        </div>
      </div>
    </div>
  );
}
