import React from 'react';

export default function AlertsPanel({ alerts }) {
  return (
    <div className="sidebar-section animate-fade-in" style={{ animationDelay: '0.3s' }}>
      <div className="section-label">Live Alerts</div>
      <div className="alerts-list">
        {alerts.map((alert, i) => (
          <div
            className={`alert-item ${alert.type}`}
            key={alert.id}
            style={{ animationDelay: `${i * 0.1}s` }}
          >
            <span className="alert-icon">{alert.icon}</span>
            <span>{alert.text}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
