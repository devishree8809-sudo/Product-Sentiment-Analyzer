import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

export default function SentimentLineChart({ data = [] }) {
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="charts-tooltip glass-panel" style={{ padding: '10px 14px', border: '1px solid var(--border-color)' }}>
          <p className="tooltip-label" style={{ fontWeight: 600, fontSize: '0.85rem', marginBottom: '6px' }}>{label}</p>
          {payload.map((entry, index) => (
            <p key={index} style={{ color: entry.color, fontSize: '0.85rem', fontWeight: 600, margin: '2px 0' }}>
              {entry.name}: {entry.value} Reviews
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="chart-wrapper line-chart-wrapper">
      <h3 className="chart-card-title">Sentiment Trend Over Time</h3>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height={260}>
          <AreaChart
            data={data}
            margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
          >
            <defs>
              <linearGradient id="colorPos" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10B981" stopOpacity={0.2}/>
                <stop offset="95%" stopColor="#10B981" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorNeu" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#F59E0B" stopOpacity={0.2}/>
                <stop offset="95%" stopColor="#F59E0B" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorNeg" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#EF4444" stopOpacity={0.2}/>
                <stop offset="95%" stopColor="#EF4444" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis
              dataKey="date"
              tick={{ fill: 'var(--text-secondary)', fontSize: 11 }}
              axisLine={{ stroke: 'rgba(255,255,255,0.1)' }}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: 'var(--text-secondary)', fontSize: 11 }}
              axisLine={{ stroke: 'rgba(255,255,255,0.1)' }}
              tickLine={false}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              verticalAlign="bottom"
              height={36}
              iconType="circle"
              iconSize={8}
              formatter={(value) => <span className="chart-legend-text">{value}</span>}
            />
            <Area
              type="monotone"
              dataKey="positive"
              name="Positive"
              stroke="#10B981"
              fillOpacity={1}
              fill="url(#colorPos)"
              strokeWidth={2}
            />
            <Area
              type="monotone"
              dataKey="neutral"
              name="Neutral"
              stroke="#F59E0B"
              fillOpacity={1}
              fill="url(#colorNeu)"
              strokeWidth={2}
            />
            <Area
              type="monotone"
              dataKey="negative"
              name="Negative"
              stroke="#EF4444"
              fillOpacity={1}
              fill="url(#colorNeg)"
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
