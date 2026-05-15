import React from 'react';

export default function PredictionPanel({ prediction, riskZones, kpiData }) {
  const levelClass = prediction.level.toLowerCase();

  return (
    <>
      {/* Congestion Prediction */}
      <div className="sidebar-section prediction-card animate-fade-in">
        <div className="section-label">Congestion Prediction</div>
        <div className={`prediction-percentage ${levelClass}`}>
          {prediction.percentage}%
        </div>
        <div className={`prediction-level`} style={{ color: levelClass === 'high' ? 'var(--neon-red)' : levelClass === 'medium' ? 'var(--neon-orange)' : 'var(--neon-green)' }}>
          {prediction.level}
        </div>
        <div className="prediction-subtitle">{prediction.subtitle}</div>
      </div>

      {/* High Risk Zones */}
      <div className="sidebar-section animate-fade-in" style={{ animationDelay: '0.1s' }}>
        <div className="section-label">High Risk Zones</div>
        <div className="risk-zones-list">
          {riskZones.map((zone, i) => (
            <div className="risk-zone-item" key={zone.id} style={{ animationDelay: `${i * 0.08}s` }}>
              <div className="zone-info">
                <span className="zone-rank">{zone.id}.</span>
                <span className="zone-name">{zone.name}</span>
              </div>
              <span className={`risk-badge ${zone.risk}`}>{zone.risk}</span>
            </div>
          ))}
        </div>
      </div>

      {/* KPI Grid */}
      <div className="sidebar-section animate-fade-in" style={{ animationDelay: '0.2s' }}>
        <div className="section-label">Live Telemetry</div>
        <div className="kpi-grid">
          {kpiData.map((kpi, i) => (
            <div className="kpi-card" key={i}>
              <div className="kpi-icon">{kpi.icon}</div>
              <div className="kpi-value">{kpi.value}</div>
              <div className="kpi-label">{kpi.label}</div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
