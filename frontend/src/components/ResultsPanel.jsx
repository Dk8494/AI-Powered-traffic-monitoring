import React from 'react';

export default function ResultsPanel({ prediction, routes, alerts, params, selectedRoute, onRouteSelect }) {
  if (!prediction) return null;

  const lvl = prediction.prediction?.toLowerCase() || 'low';
  const riskZones = [
    { id:1, name:'MG Road', risk: lvl==='high'?'high':'medium' },
    { id:2, name:'Ring Road', risk: lvl==='high'?'high':'medium' },
    { id:3, name:'Central Avenue', risk: lvl==='high'?'medium':'low' },
    { id:4, name:'Station Road', risk:'medium' },
    { id:5, name:'Lake Drive', risk:'low' },
  ];

  const routeColors = ['#FF4D6A', '#4ADE80', '#FFAA33'];

  return (
    <>
      {/* Prediction Hero */}
      <div className="panel-section prediction-hero" style={{ animation:'fadeInUp .4s ease-out' }}>
        <div className="section-label">Congestion Prediction</div>
        <div className={`prediction-pct ${lvl}`}>{prediction.percentage}%</div>
        <div className="prediction-label" style={{ color: lvl==='high'?'var(--neon-red)':lvl==='medium'?'var(--neon-orange)':'var(--neon-green)' }}>
          {prediction.prediction}
        </div>
        <div className="prediction-sub">Congestion Risk Next 45 mins</div>
      </div>

      {/* Risk Zones */}
      <div className="panel-section" style={{ animation:'fadeInUp .5s ease-out' }}>
        <div className="section-label">High Risk Zones</div>
        <div className="zone-list">
          {riskZones.map(z => (
            <div className="zone-row" key={z.id}>
              <div className="zone-info">
                <span className="zone-rank">{z.id}.</span>
                <span className="zone-name">{z.name}</span>
              </div>
              <span className={`badge ${z.risk}`}>{z.risk}</span>
            </div>
          ))}
        </div>
      </div>

      {/* KPI */}
      <div className="panel-section" style={{ animation:'fadeInUp .6s ease-out' }}>
        <div className="section-label">Live Telemetry</div>
        <div className="kpi-grid">
          <div className="kpi-card"><div className="kpi-icon">🚗</div><div className="kpi-val">{params.vehicle_volume}/hr</div><div className="kpi-lbl">Vehicle Load</div></div>
          <div className="kpi-card"><div className="kpi-icon">🕒</div><div className="kpi-val">{params.time_of_day}:00</div><div className="kpi-lbl">Local Time</div></div>
          <div className="kpi-card"><div className="kpi-icon">⛈️</div><div className="kpi-val">{params.weather}</div><div className="kpi-lbl">Weather</div></div>
          <div className="kpi-card"><div className="kpi-icon">⚡</div><div className="kpi-val">Online</div><div className="kpi-lbl">System</div></div>
        </div>
      </div>

      {/* Routes — clickable */}
      {routes?.routes?.length > 0 && (
        <div className="panel-section" style={{ animation:'fadeInUp .7s ease-out' }}>
          <div className="section-label">
            {routes.is_emergency ? '🚨 Emergency Routes' : '🛣️ Click a route to view on map'}
          </div>
          <div className="route-list">
            {routes.routes.map((r, i) => (
              <div
                className={`route-card ${r.recommended ? 'best' : ''} ${selectedRoute === i ? 'selected' : ''}`}
                key={i}
                onClick={() => onRouteSelect(selectedRoute === i ? null : i)}
              >
                <div style={{ display:'flex', alignItems:'center', gap:8, flex:1 }}>
                  <div className="route-color-dot" style={{ background: routeColors[i] || '#00C9FF' }} />
                  <div>
                    <div className="route-name">{r.name}</div>
                    <div className="route-meta">{r.traffic} traffic · Toll: {r.toll}</div>
                    {r.recommended && <div className="route-tag">AI Pick</div>}
                  </div>
                </div>
                <div style={{ textAlign:'right' }}>
                  <div className="route-eta">{r.eta}</div>
                  {selectedRoute === i && <div className="route-active-tag">On Map</div>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Alerts */}
      {alerts?.alerts?.length > 0 && (
        <div className="panel-section" style={{ animation:'fadeInUp .8s ease-out' }}>
          <div className="section-label">Live Alerts</div>
          <div className="alert-list">
            {alerts.alerts.map((a, i) => (
              <div className={`alert-row ${a.type}`} key={i}>
                <span className="alert-icon">{a.icon}</span>
                <span>{a.text}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}
