import React, { useState, useEffect } from 'react';
import ControlSidebar from './components/ControlSidebar';
import MapView from './components/MapView';
import ResultsPanel from './components/ResultsPanel';
import ChatInterface from './components/ChatInterface';
import BottomToolbar from './components/BottomToolbar';
import { SignalPanel, EmergencyPanel, HeatmapPanel, AlertsFullPanel, RoutesPanel } from './components/TabPanels';
import { fetchPrediction, fetchRoutes, fetchAlerts, fetchHeatmap } from './data/api';

const defaultParams = {
  source: 'Sector 18 Noida',
  destination: 'Akshardham',
  lat: 28.5706,
  lng: 77.3240,
  time_of_day: new Date().getHours(),
  vehicle_volume: 500,
  avg_speed: 40,
  weather: 'Clear',
  rain_mm: 0,
  accident: 'No',
  event: 'None',
  public_transport_density: 40,
  vehicle_type: 'Normal',
};

export default function App() {
  const [params, setParams] = useState(defaultParams);
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [routes, setRoutes] = useState(null);
  const [alerts, setAlerts] = useState(null);
  const [heatmap, setHeatmap] = useState({ hotspots: [], incidents: [], center: [28.5706, 77.324] });
  const [activeTab, setActiveTab] = useState('heatmap');
  const [rightView, setRightView] = useState('dashboard'); // 'dashboard' | 'chat'
  const [selectedRoute, setSelectedRoute] = useState(null);

  // Load heatmap on mount
  useEffect(() => {
    fetchHeatmap(params.lat, params.lng).then(setHeatmap).catch(() => {});
  }, []);

  // Reset selected route when switching tabs
  useEffect(() => {
    if (activeTab !== 'routes') setSelectedRoute(null);
  }, [activeTab]);

  const runPrediction = async () => {
    setLoading(true);
    setRightView('dashboard');
    try {
      const [pred, rts, alts, hm] = await Promise.all([
        fetchPrediction(params),
        fetchRoutes({ source: params.source, destination: params.destination, vehicle_type: params.vehicle_type }),
        fetchAlerts({ prediction: 'pending', weather: params.weather, accident: params.accident, event: params.event }),
        fetchHeatmap(params.lat, params.lng),
      ]);
      setPrediction(pred);
      setRoutes(rts);
      setHeatmap(hm);

      // Re-fetch alerts with actual prediction
      const finalAlerts = await fetchAlerts({
        prediction: pred.prediction,
        weather: params.weather,
        accident: params.accident,
        event: params.event,
      });
      setAlerts(finalAlerts);
    } catch (err) {
      console.error('Prediction failed:', err);
    }
    setLoading(false);
  };

  const lvl = prediction?.prediction?.toLowerCase() || '';

  // Determine what to show in the right panel based on activeTab
  const renderRightPanel = () => {
    if (rightView === 'chat') return <ChatInterface />;

    switch (activeTab) {
      case 'heatmap':
        return prediction ? (
          <ResultsPanel prediction={prediction} routes={routes} alerts={alerts} params={params}
            selectedRoute={selectedRoute} onRouteSelect={setSelectedRoute} />
        ) : (
          <HeatmapPanel hotspots={heatmap.hotspots} />
        );
      case 'routes':
        return <RoutesPanel routes={routes} selectedRoute={selectedRoute} onRouteSelect={setSelectedRoute} />;
      case 'signal':
        return <SignalPanel />;
      case 'emergency':
        return <EmergencyPanel />;
      case 'alerts':
        return <AlertsFullPanel alerts={alerts} />;
      default:
        return null;
    }
  };

  // Map banner text
  const bannerText = {
    heatmap: prediction ? `Congestion: ${prediction.prediction}` : 'Heatmap View',
    routes: selectedRoute !== null ? `Showing Route ${selectedRoute + 1} on map` : 'All Routes Displayed',
    signal: 'Signal Timing View — 6 Intersections',
    emergency: '🚨 Emergency Priority Mode',
    alerts: 'Alert Zones Highlighted',
  };

  return (
    <div className="app-layout">
      {/* Header */}
      <header className="app-header">
        <div className="header-brand">
          <div className="logo-box">🚥</div>
          <h1>AI Smart Traffic Predictor</h1>
        </div>
        <div className="header-right">
          <button className={`header-btn ${rightView === 'chat' ? 'active' : ''}`}
            onClick={() => setRightView(v => v === 'chat' ? 'dashboard' : 'chat')}>
            {rightView === 'chat' ? '📊 Dashboard' : '💬 AI Assistant'}
          </button>
          <div className="status-pill">
            <span className="dot" />
            All Systems Online
          </div>
        </div>
      </header>

      {/* Left Sidebar */}
      <ControlSidebar params={params} setParams={setParams} onPredict={runPrediction} loading={loading} />

      {/* Center Map */}
      <main className="map-area">
        <div className={`map-banner ${activeTab === 'emergency' ? 'high' : lvl || 'low'}`}>
          {activeTab === 'emergency' ? '🚨' : activeTab === 'signal' ? '🚦' : activeTab === 'routes' ? '🛣️' : activeTab === 'alerts' ? '🔔' : lvl === 'high' ? '🛑' : lvl === 'medium' ? '⚠️' : '🗺️'}
          <span>{bannerText[activeTab]}</span>
        </div>
        <MapView
          center={heatmap.center}
          hotspots={heatmap.hotspots}
          incidents={heatmap.incidents}
          activeTab={activeTab}
          selectedRoute={selectedRoute}
        />
      </main>

      {/* Right Panel */}
      <aside className="right-panel">
        {renderRightPanel() || (
          <div className="idle-state">
            <div className="idle-icon">🚥</div>
            <h3>System Standby</h3>
            <p>Configure parameters in Mission Control and click <strong>Initiate AI Prediction</strong> to begin.</p>
          </div>
        )}
      </aside>

      {/* Bottom Toolbar */}
      <BottomToolbar active={activeTab} onChange={setActiveTab} />
    </div>
  );
}
