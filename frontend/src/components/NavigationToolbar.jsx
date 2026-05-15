import React from 'react';
import { FaFireAlt, FaRoute, FaTrafficLight, FaTruck, FaBell } from 'react-icons/fa';

const navItems = [
  { id: 'heatmap', label: 'Heatmap', icon: <FaFireAlt />, colorClass: 'heatmap' },
  { id: 'routes', label: 'Alternative Routes', icon: <FaRoute />, colorClass: 'routes' },
  { id: 'signal', label: 'Signal Timing', icon: <FaTrafficLight />, colorClass: 'signal' },
  { id: 'emergency', label: 'Emergency Route', icon: <FaTruck />, colorClass: 'emergency' },
  { id: 'alerts', label: 'Live Alerts', icon: <FaBell />, colorClass: 'alerts' },
];

export default function NavigationToolbar({ activeTab, onTabChange }) {
  return (
    <nav className="nav-toolbar">
      {navItems.map((item) => (
        <button
          key={item.id}
          className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
          onClick={() => onTabChange(item.id)}
          aria-label={item.label}
        >
          <div className={`nav-icon-wrapper ${item.colorClass}`}>
            {item.icon}
          </div>
          <span className="nav-label">{item.label}</span>
        </button>
      ))}
    </nav>
  );
}
