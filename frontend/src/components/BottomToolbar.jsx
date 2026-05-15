import React from 'react';
import { FaFireAlt, FaRoute, FaTrafficLight, FaTruck, FaBell } from 'react-icons/fa';

const items = [
  { id:'heatmap', label:'Heatmap', icon:<FaFireAlt/>, c:'c1' },
  { id:'routes', label:'Alt Routes', icon:<FaRoute/>, c:'c2' },
  { id:'signal', label:'Signal Timing', icon:<FaTrafficLight/>, c:'c3' },
  { id:'emergency', label:'Emergency', icon:<FaTruck/>, c:'c4' },
  { id:'alerts', label:'Live Alerts', icon:<FaBell/>, c:'c5' },
];

export default function BottomToolbar({ active, onChange }) {
  return (
    <nav className="bottom-bar">
      {items.map(it => (
        <button key={it.id} className={`nav-btn ${active===it.id?'on':''}`} onClick={() => onChange(it.id)}>
          <div className={`nav-icon-box ${it.c}`}>{it.icon}</div>
          <span className="nav-lbl">{it.label}</span>
        </button>
      ))}
    </nav>
  );
}
