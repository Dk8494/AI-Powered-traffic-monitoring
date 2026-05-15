import React from 'react';

/* ═══════ SIGNAL TIMING PANEL ═══════ */
const SIGNALS = [
  { name:'Signal A — Atta Market Crossing', green:45, red:30, cycle:75, status:'green' },
  { name:'Signal B — DND Entry Junction', green:30, red:45, cycle:75, status:'red' },
  { name:'Signal C — Maharani Bagh', green:40, red:35, cycle:75, status:'green' },
  { name:'Signal D — Ashram Chowk', green:25, red:50, cycle:75, status:'red' },
  { name:'Signal E — Ring Road Junction', green:50, red:25, cycle:75, status:'green' },
  { name:'Signal F — Chilla Regulator', green:35, red:40, cycle:75, status:'red' },
];

export function SignalPanel() {
  return (
    <>
      <div className="panel-section" style={{ animation:'fadeInUp .3s ease-out' }}>
        <div className="section-label">🚦 Signal Timing Optimization</div>
        <p style={{ fontSize:'.78rem', color:'var(--text-secondary)', marginBottom:14, lineHeight:1.5 }}>
          AI-optimized signal timings based on current traffic density. Click markers on the map for details.
        </p>
        <div className="signal-list">
          {SIGNALS.map((s, i) => (
            <div className="signal-row" key={i} style={{ animationDelay:`${i*0.06}s` }}>
              <div style={{ display:'flex', alignItems:'center', gap:10, flex:1 }}>
                <div className={`signal-dot ${s.status}`} />
                <div>
                  <div className="signal-name">{s.name}</div>
                  <div className="signal-meta">Cycle: {s.cycle}s</div>
                </div>
              </div>
              <div style={{ display:'flex', gap:6 }}>
                <span className="signal-time green">🟢 {s.green}s</span>
                <span className="signal-time red">🔴 {s.red}s</span>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="panel-section">
        <div className="section-label">Optimization Summary</div>
        <div className="kpi-grid">
          <div className="kpi-card"><div className="kpi-icon">🟢</div><div className="kpi-val">3</div><div className="kpi-lbl">Green Active</div></div>
          <div className="kpi-card"><div className="kpi-icon">🔴</div><div className="kpi-val">3</div><div className="kpi-lbl">Red Active</div></div>
          <div className="kpi-card"><div className="kpi-icon">⏱️</div><div className="kpi-val">75s</div><div className="kpi-lbl">Avg Cycle</div></div>
          <div className="kpi-card"><div className="kpi-icon">📊</div><div className="kpi-val">82%</div><div className="kpi-lbl">Efficiency</div></div>
        </div>
      </div>
    </>
  );
}

/* ═══════ EMERGENCY PANEL ═══════ */
export function EmergencyPanel() {
  return (
    <>
      <div className="panel-section" style={{ animation:'fadeInUp .3s ease-out' }}>
        <div className="section-label">🚨 Emergency Route Control</div>
        <div className="emergency-banner">
          <div className="emergency-icon">🚑</div>
          <div>
            <div className="emergency-title">Emergency Priority Active</div>
            <div className="emergency-sub">All tolls exempted · Signal clearing in progress</div>
          </div>
        </div>
      </div>
      <div className="panel-section">
        <div className="section-label">Priority Routes</div>
        <div className="route-list">
          <div className="route-card selected" style={{ borderColor:'rgba(255,77,106,.4)', background:'rgba(255,77,106,.06)' }}>
            <div style={{ display:'flex', alignItems:'center', gap:8, flex:1 }}>
              <div className="route-color-dot" style={{ background:'#FF4D6A' }} />
              <div>
                <div className="route-name">🚨 Emergency Priority</div>
                <div className="route-meta">Lanes clearing · Toll: Exempt</div>
                <div className="route-tag" style={{ background:'rgba(255,77,106,.15)', color:'var(--neon-red)' }}>Priority</div>
              </div>
            </div>
            <div className="route-eta">28 min</div>
          </div>
          <div className="route-card">
            <div style={{ display:'flex', alignItems:'center', gap:8, flex:1 }}>
              <div className="route-color-dot" style={{ background:'#FFAA33' }} />
              <div>
                <div className="route-name">Backup Route ⚡</div>
                <div className="route-meta">Moderate traffic · Toll: Exempt</div>
              </div>
            </div>
            <div className="route-eta">32 min</div>
          </div>
        </div>
      </div>
      <div className="panel-section">
        <div className="section-label">Emergency Services</div>
        <div className="kpi-grid">
          <div className="kpi-card"><div className="kpi-icon">🚑</div><div className="kpi-val">2</div><div className="kpi-lbl">Ambulances</div></div>
          <div className="kpi-card"><div className="kpi-icon">🚒</div><div className="kpi-val">1</div><div className="kpi-lbl">Fire Trucks</div></div>
          <div className="kpi-card"><div className="kpi-icon">🚔</div><div className="kpi-val">3</div><div className="kpi-lbl">Police Units</div></div>
          <div className="kpi-card"><div className="kpi-icon">🏥</div><div className="kpi-val">4.2km</div><div className="kpi-lbl">Nearest Hospital</div></div>
        </div>
      </div>
    </>
  );
}

/* ═══════ HEATMAP INFO PANEL ═══════ */
export function HeatmapPanel({ hotspots }) {
  const highCount = hotspots?.filter(p => p[2] > 0.7).length || 0;
  const medCount = hotspots?.filter(p => p[2] > 0.45 && p[2] <= 0.7).length || 0;
  const lowCount = hotspots?.filter(p => p[2] <= 0.45).length || 0;

  return (
    <>
      <div className="panel-section" style={{ animation:'fadeInUp .3s ease-out' }}>
        <div className="section-label">🔥 Congestion Heatmap</div>
        <p style={{ fontSize:'.78rem', color:'var(--text-secondary)', marginBottom:14, lineHeight:1.5 }}>
          AI-detected traffic density zones. Red indicates severe congestion, green shows clear corridors.
        </p>
        <div className="kpi-grid">
          <div className="kpi-card" style={{ borderColor:'rgba(255,77,106,.2)' }}>
            <div className="kpi-icon">🔴</div><div className="kpi-val" style={{ color:'var(--neon-red)' }}>{highCount}</div><div className="kpi-lbl">High Zones</div>
          </div>
          <div className="kpi-card" style={{ borderColor:'rgba(255,170,51,.2)' }}>
            <div className="kpi-icon">🟠</div><div className="kpi-val" style={{ color:'var(--neon-orange)' }}>{medCount}</div><div className="kpi-lbl">Medium Zones</div>
          </div>
          <div className="kpi-card" style={{ borderColor:'rgba(74,222,128,.2)' }}>
            <div className="kpi-icon">🟢</div><div className="kpi-val" style={{ color:'var(--neon-green)' }}>{lowCount}</div><div className="kpi-lbl">Clear Zones</div>
          </div>
          <div className="kpi-card">
            <div className="kpi-icon">📍</div><div className="kpi-val">{hotspots?.length || 0}</div><div className="kpi-lbl">Total Points</div>
          </div>
        </div>
      </div>
      <div className="panel-section">
        <div className="section-label">Density Legend</div>
        <div className="legend-list">
          <div className="legend-item"><div className="legend-dot" style={{ background:'#FF4D6A' }} /><span>High Density (70-100%)</span></div>
          <div className="legend-item"><div className="legend-dot" style={{ background:'#FFAA33' }} /><span>Medium Density (45-70%)</span></div>
          <div className="legend-item"><div className="legend-dot" style={{ background:'#4ADE80' }} /><span>Low Density (0-45%)</span></div>
        </div>
      </div>
    </>
  );
}

/* ═══════ ALERTS FULL PANEL ═══════ */
export function AlertsFullPanel({ alerts }) {
  const items = alerts?.alerts || [];
  return (
    <>
      <div className="panel-section" style={{ animation:'fadeInUp .3s ease-out' }}>
        <div className="section-label">🔔 Live Alerts & Notifications</div>
        {items.length > 0 ? (
          <div className="alert-list">
            {items.map((a, i) => (
              <div className={`alert-row ${a.type}`} key={i} style={{ animationDelay:`${i*0.08}s` }}>
                <span className="alert-icon">{a.icon}</span>
                <span>{a.text}</span>
              </div>
            ))}
          </div>
        ) : (
          <div style={{ textAlign:'center', padding:24, color:'var(--text-muted)', fontSize:'.82rem' }}>
            <div style={{ fontSize:'2rem', marginBottom:8 }}>✅</div>
            No active alerts. Run a prediction to generate alerts.
          </div>
        )}
      </div>
      <div className="panel-section">
        <div className="section-label">Alert Summary</div>
        <div className="kpi-grid">
          <div className="kpi-card"><div className="kpi-icon">🛑</div><div className="kpi-val">{items.filter(a=>a.type==='danger').length}</div><div className="kpi-lbl">Critical</div></div>
          <div className="kpi-card"><div className="kpi-icon">⚠️</div><div className="kpi-val">{items.filter(a=>a.type==='warning').length}</div><div className="kpi-lbl">Warnings</div></div>
          <div className="kpi-card"><div className="kpi-icon">ℹ️</div><div className="kpi-val">{items.filter(a=>a.type==='info').length}</div><div className="kpi-lbl">Info</div></div>
          <div className="kpi-card"><div className="kpi-icon">✅</div><div className="kpi-val">{items.filter(a=>a.type==='success').length}</div><div className="kpi-lbl">Clear</div></div>
        </div>
      </div>
    </>
  );
}

/* ═══════ ROUTES PANEL (dedicated tab view) ═══════ */
export function RoutesPanel({ routes, selectedRoute, onRouteSelect }) {
  const routeColors = ['#FF4D6A', '#4ADE80', '#FFAA33'];
  const items = routes?.routes || [];

  return (
    <>
      <div className="panel-section" style={{ animation:'fadeInUp .3s ease-out' }}>
        <div className="section-label">🛣️ Alternative Routes — Click to highlight on map</div>
        {items.length > 0 ? (
          <div className="route-list">
            {items.map((r, i) => (
              <div
                className={`route-card ${r.recommended ? 'best' : ''} ${selectedRoute === i ? 'selected' : ''}`}
                key={i}
                onClick={() => onRouteSelect(selectedRoute === i ? null : i)}
              >
                <div style={{ display:'flex', alignItems:'center', gap:8, flex:1 }}>
                  <div className="route-color-dot" style={{ background: routeColors[i] || '#00C9FF' }} />
                  <div>
                    <div className="route-name">{r.name}</div>
                    <div className="route-meta">{r.traffic} traffic · Toll: {r.toll} · Fuel: {r.fuel_efficiency}</div>
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
        ) : (
          <div style={{ textAlign:'center', padding:24, color:'var(--text-muted)', fontSize:'.82rem' }}>
            <div style={{ fontSize:'2rem', marginBottom:8 }}>🛣️</div>
            Run a prediction first to see route suggestions.
          </div>
        )}
      </div>
      <div className="panel-section">
        <div className="section-label">Route Comparison</div>
        <div className="legend-list">
          {items.map((r, i) => (
            <div className="legend-item" key={i}>
              <div className="legend-dot" style={{ background: routeColors[i] }} />
              <span>{r.name} — {r.eta}</span>
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
