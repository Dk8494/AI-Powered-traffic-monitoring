import React from 'react';

export default function ControlSidebar({ params, setParams, onPredict, loading }) {
  const update = (key, val) => setParams(p => ({ ...p, [key]: val }));

  return (
    <aside className="control-sidebar">
      <div className="sidebar-header">
        <h2>🚦 Mission Control</h2>
      </div>

      {/* Location */}
      <div className="sidebar-group">
        <div className="group-title">📍 Location & Routing</div>
        <div className="form-field">
          <label className="form-label">Source</label>
          <input className="form-input" value={params.source} onChange={e => update('source', e.target.value)} />
        </div>
        <div className="form-field">
          <label className="form-label">Destination</label>
          <input className="form-input" value={params.destination} onChange={e => update('destination', e.target.value)} />
        </div>
        <div className="form-field">
          <label className="form-label">Latitude</label>
          <input className="form-input" type="number" step="0.0001" value={params.lat} onChange={e => update('lat', parseFloat(e.target.value))} />
        </div>
        <div className="form-field">
          <label className="form-label">Longitude</label>
          <input className="form-input" type="number" step="0.0001" value={params.lng} onChange={e => update('lng', parseFloat(e.target.value))} />
        </div>
      </div>

      {/* AI Context Variables */}
      <div className="sidebar-group">
        <div className="group-title">⚙️ AI Context Variables</div>
        <div className="form-field">
          <label className="form-label">Time of Day</label>
          <div className="range-row">
            <input type="range" min="0" max="23" value={params.time_of_day} onChange={e => update('time_of_day', parseInt(e.target.value))} />
            <span className="range-value">{params.time_of_day}:00</span>
          </div>
        </div>
        <div className="form-field">
          <label className="form-label">Vehicles/hr</label>
          <input className="form-input" type="number" min="0" max="10000" step="50" value={params.vehicle_volume} onChange={e => update('vehicle_volume', parseInt(e.target.value))} />
        </div>
        <div className="form-field">
          <label className="form-label">Avg Speed (km/h)</label>
          <input className="form-input" type="number" min="0" max="200" step="5" value={params.avg_speed} onChange={e => update('avg_speed', parseInt(e.target.value))} />
        </div>
        <div className="form-field">
          <label className="form-label">Weather</label>
          <select className="form-select" value={params.weather} onChange={e => update('weather', e.target.value)}>
            {['Clear','Rain','Snow','Fog','Cloudy','Heavy Rain'].map(w => <option key={w} value={w}>{w}</option>)}
          </select>
        </div>
        <div className="form-field">
          <label className="form-label">Rain (mm)</label>
          <input className="form-input" type="number" min="0" max="100" step="1" value={params.rain_mm} onChange={e => update('rain_mm', parseFloat(e.target.value))} />
        </div>
        <div className="form-field">
          <label className="form-label">Accident Nearby?</label>
          <select className="form-select" value={params.accident} onChange={e => update('accident', e.target.value)}>
            <option value="No">No</option>
            <option value="Yes">Yes</option>
          </select>
        </div>
        <div className="form-field">
          <label className="form-label">Special Event</label>
          <select className="form-select" value={params.event} onChange={e => update('event', e.target.value)}>
            {['None','Concert','Sports Game','Festival'].map(e => <option key={e} value={e}>{e}</option>)}
          </select>
        </div>
        <div className="form-field">
          <label className="form-label">Public Transport Density</label>
          <div className="range-row">
            <input type="range" min="0" max="100" step="5" value={params.public_transport_density} onChange={e => update('public_transport_density', parseInt(e.target.value))} />
            <span className="range-value">{params.public_transport_density}</span>
          </div>
        </div>
      </div>

      {/* Vehicle Type */}
      <div className="sidebar-group">
        <div className="group-title">🚑 Vehicle Type</div>
        <div className="form-field">
          <select className="form-select" value={params.vehicle_type} onChange={e => update('vehicle_type', e.target.value)}>
            <option value="Normal">Normal</option>
            <option value="Ambulance">Ambulance</option>
            <option value="Fire Truck">Fire Truck</option>
          </select>
        </div>
        <button className="predict-btn" onClick={onPredict} disabled={loading}>
          {loading ? <><span className="spinner"></span>Processing...</> : '🚀 Initiate AI Prediction'}
        </button>
      </div>
    </aside>
  );
}
