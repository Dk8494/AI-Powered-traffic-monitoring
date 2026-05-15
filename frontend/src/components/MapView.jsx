import React, { useEffect } from 'react';
import { MapContainer, TileLayer, CircleMarker, Polyline, Popup, Tooltip, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// Start: Sector 18 Noida  (28.5696, 77.3219)
// End:   Akshardham Delhi  (28.6127, 77.2773)

// ─── Route 1: Fastest — via DND Flyway (toll road, crosses Yamuna directly) ───
// Sector 18 → Sector 15A → DND Flyway entry → across Yamuna → Maharani Bagh → Ring Road → Akshardham
const ROUTE_1 = [
  [28.5696, 77.3219],  // Sector 18, Noida
  [28.5720, 77.3180],  // Atta Market area
  [28.5758, 77.3125],  // Sector 15 Noida
  [28.5790, 77.3080],  // DND Flyway Noida entry
  [28.5830, 77.3020],  // DND Flyway on-ramp
  [28.5870, 77.2960],  // DND over Yamuna (east bank)
  [28.5920, 77.2890],  // DND mid-river crossing
  [28.5960, 77.2830],  // DND west bank approach
  [28.5990, 77.2790],  // Maharani Bagh exit
  [28.6030, 77.2770],  // Ring Road junction
  [28.6070, 77.2760],  // NH-24 approach
  [28.6127, 77.2773],  // Akshardham
];

// ─── Route 2: AI Recommended — via Mayur Vihar / NH-24 (balanced) ───
// Sector 18 → Sector 14 → Chilla Regulator → Mayur Vihar Ph-1 → NH-24 → Akshardham
const ROUTE_2 = [
  [28.5696, 77.3219],  // Sector 18, Noida
  [28.5730, 77.3160],  // Sector 16 Noida
  [28.5770, 77.3100],  // Sector 14A
  [28.5810, 77.3050],  // Film City Road
  [28.5860, 77.3010],  // Chilla Regulator approach
  [28.5910, 77.2970],  // Chilla border crossing
  [28.5960, 77.2940],  // Mayur Vihar Extension
  [28.6000, 77.2900],  // Mayur Vihar Phase 1
  [28.6040, 77.2860],  // Akshardham flyover approach
  [28.6080, 77.2820],  // NH-24 merge
  [28.6110, 77.2790],  // Akshardham east gate
  [28.6127, 77.2773],  // Akshardham
];

// ─── Route 3: Cheapest — via Kalindi Kunj (no toll, longer southern route) ───
// Sector 18 → Sector 37 → Kalindi Kunj bridge → Sarita Vihar → Ashram → Ring Road → Akshardham
const ROUTE_3 = [
  [28.5696, 77.3219],  // Sector 18, Noida
  [28.5650, 77.3200],  // Sector 18 south exit
  [28.5590, 77.3170],  // Sector 37 Noida
  [28.5530, 77.3130],  // Amity University area
  [28.5480, 77.3060],  // Kalindi Kunj approach (Noida side)
  [28.5460, 77.2980],  // Kalindi Kunj Bridge
  [28.5480, 77.2900],  // Kalindi Kunj (Delhi side)
  [28.5530, 77.2850],  // Sarita Vihar
  [28.5610, 77.2810],  // Jasola
  [28.5700, 77.2780],  // Ashram Chowk
  [28.5810, 77.2760],  // Nizamuddin
  [28.5920, 77.2750],  // Pragati Maidan area
  [28.6030, 77.2760],  // Ring Road
  [28.6127, 77.2773],  // Akshardham
];

export const ROUTE_PATHS = [
  { id: 0, label: 'Fastest Route ⚡ (DND Flyway)', color: '#FF4D6A', positions: ROUTE_1 },
  { id: 1, label: 'AI Recommended ✨ (via Mayur Vihar)', color: '#4ADE80', positions: ROUTE_2 },
  { id: 2, label: 'Cheapest Route 💰 (Kalindi Kunj)', color: '#FFAA33', positions: ROUTE_3 },
];

// ─── Emergency: DND Flyway direct + NH-24 backup ───
const EMERGENCY_PATHS = [
  { label: '🚨 Emergency Priority (DND)', color: '#FF4D6A', positions: ROUTE_1 },
  { label: 'Backup (Mayur Vihar)', color: '#FFAA33', positions: ROUTE_2 },
];

// ─── Signal timing markers — placed at real intersections along routes ───
const SIGNALS = [
  { pos:[28.5720, 77.3180], name:'Signal A — Atta Market Crossing', green:45, red:30, status:'green' },
  { pos:[28.5790, 77.3080], name:'Signal B — DND Entry Junction', green:30, red:45, status:'red' },
  { pos:[28.5990, 77.2790], name:'Signal C — Maharani Bagh', green:40, red:35, status:'green' },
  { pos:[28.5700, 77.2780], name:'Signal D — Ashram Chowk', green:25, red:50, status:'red' },
  { pos:[28.6030, 77.2770], name:'Signal E — Ring Road Junction', green:50, red:25, status:'green' },
  { pos:[28.5860, 77.3010], name:'Signal F — Chilla Regulator', green:35, red:40, status:'red' },
];

// ─── Start & End points ───
const START_POS = [28.5696, 77.3219];
const END_POS = [28.6127, 77.2773];

// ─── Sub-components ───

function HeatmapDots({ hotspots }) {
  if (!hotspots?.length) return null;
  return hotspots.map((p, i) => (
    <CircleMarker key={`h${i}`} center={[p[0], p[1]]}
      radius={6 + p[2] * 10}
      pathOptions={{ fillColor: p[2]>.7?'#FF4D6A':p[2]>.45?'#FFAA33':'#4ADE80', fillOpacity:.2+p[2]*.25, stroke:false }}
    />
  ));
}

function IncidentMarkers({ incidents }) {
  if (!incidents?.length) return null;
  const c = { congestion:'#FF4D6A', accident:'#FFAA33', construction:'#FFD600', signal:'#00C9FF' };
  return incidents.map((m, i) => (
    <CircleMarker key={`i${i}`} center={m.position} radius={7}
      pathOptions={{ fillColor:c[m.type]||'#FF4D6A', fillOpacity:.9, color:c[m.type]||'#FF4D6A', weight:2 }}>
      <Popup><div style={{ color:'#0A1128', fontWeight:600, fontSize:'.82rem' }}>⚠️ {m.label}</div></Popup>
    </CircleMarker>
  ));
}

function StartEndMarkers() {
  return (
    <>
      <CircleMarker center={START_POS} radius={9}
        pathOptions={{ fillColor:'#4ADE80', fillOpacity:1, color:'#fff', weight:3 }}>
        <Tooltip permanent direction="right" offset={[12,0]} className="route-tooltip">
          📍 Sector 18, Noida
        </Tooltip>
      </CircleMarker>
      <CircleMarker center={END_POS} radius={9}
        pathOptions={{ fillColor:'#FF4D6A', fillOpacity:1, color:'#fff', weight:3 }}>
        <Tooltip permanent direction="right" offset={[12,0]} className="route-tooltip">
          🏁 Akshardham, Delhi
        </Tooltip>
      </CircleMarker>
    </>
  );
}

function AllRoutePaths({ selectedRoute }) {
  return ROUTE_PATHS.map((r) => {
    const isSelected = selectedRoute === r.id;
    const isNone = selectedRoute === null;
    return (
      <Polyline key={`r${r.id}`} positions={r.positions}
        pathOptions={{
          color: r.color,
          weight: isSelected ? 6 : 3,
          opacity: isNone ? 0.4 : isSelected ? 0.95 : 0.12,
          dashArray: r.id === 1 ? '10,6' : undefined,
        }}
      >
        {isSelected && (
          <Tooltip permanent direction="center" className="route-tooltip">
            {r.label}
          </Tooltip>
        )}
      </Polyline>
    );
  });
}

function EmergencyRoutes() {
  return EMERGENCY_PATHS.map((r, i) => (
    <Polyline key={`e${i}`} positions={r.positions}
      pathOptions={{ color:r.color, weight:i===0?6:3, opacity:i===0?.9:.5, dashArray:i===0?'12,8':undefined }}>
      <Tooltip permanent={i===0} direction="center" className="route-tooltip">{r.label}</Tooltip>
    </Polyline>
  ));
}

function SignalMarkers() {
  return SIGNALS.map((s, i) => (
    <CircleMarker key={`s${i}`} center={s.pos} radius={10}
      pathOptions={{
        fillColor: s.status==='green'?'#4ADE80':'#FF4D6A',
        fillOpacity:.85, color:'#fff', weight:2,
      }}>
      <Popup>
        <div style={{ color:'#0A1128', fontSize:'.8rem', minWidth:140 }}>
          <div style={{ fontWeight:700, marginBottom:4 }}>🚦 {s.name}</div>
          <div>🟢 Green: {s.green}s</div>
          <div>🔴 Red: {s.red}s</div>
          <div style={{ marginTop:4, fontWeight:600, color:s.status==='green'?'#16a34a':'#dc2626' }}>
            Currently: {s.status.toUpperCase()}
          </div>
        </div>
      </Popup>
      <Tooltip direction="top" offset={[0,-10]}>
        <span style={{ fontSize:'.7rem' }}>{s.name.split('—')[0]}</span>
      </Tooltip>
    </CircleMarker>
  ));
}

// ─── Helper: Recenter map on mount ───
function RecenterMap({ center, zoom }) {
  const map = useMap();
  useEffect(() => {
    map.setView(center, zoom);
  }, []);
  return null;
}

// ─── Main MapView ───

export default function MapView({ center, hotspots, incidents, activeTab, selectedRoute }) {
  // Center between Sector 18 Noida and Akshardham for best view
  const mapCenter = [28.5900, 77.2990];

  return (
    <MapContainer center={mapCenter} zoom={13} style={{ width:'100%', height:'100%' }} zoomControl={false} attributionControl={false}>
      <RecenterMap center={mapCenter} zoom={13} />
      <TileLayer url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png" />

      {/* Heatmap — show on heatmap tab or alerts */}
      {(activeTab === 'heatmap' || activeTab === 'alerts') && <HeatmapDots hotspots={hotspots} />}

      {/* Incidents — always visible */}
      <IncidentMarkers incidents={incidents} />

      {/* Start & End markers — show on routes, heatmap, emergency */}
      {(activeTab === 'routes' || activeTab === 'heatmap' || activeTab === 'emergency') && <StartEndMarkers />}

      {/* Routes — show on routes tab or heatmap */}
      {(activeTab === 'routes' || activeTab === 'heatmap') && (
        <AllRoutePaths selectedRoute={selectedRoute} />
      )}

      {/* Signal timing markers */}
      {activeTab === 'signal' && <><SignalMarkers /><StartEndMarkers /></>}

      {/* Emergency routes */}
      {activeTab === 'emergency' && <EmergencyRoutes />}

      {/* Alert markers */}
      {activeTab === 'alerts' && <IncidentMarkers incidents={incidents} />}
    </MapContainer>
  );
}
