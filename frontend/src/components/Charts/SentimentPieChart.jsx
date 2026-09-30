import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function SentimentPieChart({ data = [] }) {
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const item = payload[0];
      return (
        <div className="charts-tooltip glass-panel" style={{ padding: '8px 12px', border: '1px solid var(--border-color)' }}>
          <p className="tooltip-label" style={{ fontWeight: 600, fontSize: '0.85rem' }}>{item.name}</p>
          <p className="tooltip-value" style={{ color: item.payload.color || item.color, fontSize: '0.9rem', fontWeight: 700 }}>
            {item.value} Reviews ({((item.value / data.reduce((sum, entry) => sum + entry.value, 0)) * 100).toFixed(1)}%)
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="chart-wrapper">
      <h3 className="chart-card-title">Sentiment Share</h3>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={260}>
          <PieChart>
            <Pie
              data={data}
              cx="50%"
              cy="45%"
              innerRadius={60}
              outerRadius={85}
              paddingAngle={4}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
            <Legend
              verticalAlign="bottom"
              height={36}
              iconType="circle"
              iconSize={8}
              formatter={(value) => <span className="chart-legend-text">{value}</span>}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
