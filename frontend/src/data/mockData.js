// ─── Prediction Data ───
export const predictionData = {
  percentage: 78,
  level: 'High',
  subtitle: 'Congestion Risk Next 45 mins',
};

// ─── High Risk Zones ───
export const riskZones = [
  { id: 1, name: 'MG Road', risk: 'high' },
  { id: 2, name: 'Ring Road', risk: 'high' },
  { id: 3, name: 'Central Avenue', risk: 'medium' },
  { id: 4, name: 'Station Road', risk: 'medium' },
  { id: 5, name: 'Lake Drive', risk: 'low' },
];

// ─── KPI Cards ───
export const kpiData = [
  { icon: '🚗', value: '1,240', label: 'Vehicles/hr' },
  { icon: '⏱️', value: '18:00', label: 'Peak Hour' },
  { icon: '🌧️', value: 'Rain', label: 'Weather' },
  { icon: '⚡', value: 'Online', label: 'System' },
];

// ─── Route Options ───
export const routeOptions = [
  { id: 1, name: 'Fastest Route', eta: '35 min', traffic: 'Heavy', toll: '$8.50', recommended: false },
  { id: 2, name: 'AI Recommended', eta: '40 min', traffic: 'Light', toll: '$2.50', recommended: true },
  { id: 3, name: 'Cheapest Route', eta: '55 min', traffic: 'Moderate', toll: 'Free', recommended: false },
];

// ─── Alerts ───
export const alertsData = [
  { id: 1, type: 'danger', icon: '🛑', text: 'Heavy congestion on MG Road. Expect 25 min delay.' },
  { id: 2, type: 'warning', icon: '🌧️', text: 'Wet roads ahead. Reduce speed and increase following distance.' },
  { id: 3, type: 'danger', icon: '💥', text: 'Accident reported on Ring Road. Emergency services en route.' },
  { id: 4, type: 'success', icon: '✅', text: 'Lake Drive corridor is clear. Optimal driving conditions.' },
];

// ─── Chat Messages ───
export const initialChatMessages = [
  { id: 1, role: 'assistant', content: '👋 Hello! I\'m your AI Traffic Assistant. Ask me about congestion, routes, or live conditions.' },
];

// ─── Heatmap Points (lat, lng, intensity) ───
export function generateHeatmapPoints(baseLat = 28.5706, baseLng = 77.3240, count = 120) {
  const points = [];
  const seed = 42;
  // Simple seeded random for reproducibility
  let s = seed;
  const rand = () => { s = (s * 16807 + 0) % 2147483647; return (s - 1) / 2147483646; };
  for (let i = 0; i < count; i++) {
    const lat = baseLat + (rand() - 0.5) * 0.12;
    const lng = baseLng + (rand() - 0.5) * 0.12;
    const intensity = 0.3 + rand() * 0.7;
    points.push([lat, lng, intensity]);
  }
  return points;
}

// ─── Map Markers ───
export const incidentMarkers = [
  { position: [28.5706, 77.3240], label: 'Heavy Congestion Zone', type: 'congestion' },
  { position: [28.5850, 77.3150], label: 'Accident Reported', type: 'accident' },
  { position: [28.5600, 77.3350], label: 'Construction Delay', type: 'construction' },
  { position: [28.5780, 77.3050], label: 'Signal Malfunction', type: 'signal' },
];

// ─── Chatbot Responses ───
export function getBotResponse(query) {
  const q = query.toLowerCase();
  if (q.includes('congestion') || q.includes('traffic')) {
    return 'Heavy congestion expected on MG Road in the next 45 mins. Consider alternate route via Lake Drive.';
  }
  if (q.includes('route') || q.includes('fastest') || q.includes('alternative')) {
    return 'I recommend the AI Recommended route via Lake Drive. It saves 12 minutes and avoids the Ring Road bottleneck.';
  }
  if (q.includes('accident') || q.includes('crash')) {
    return '⚠️ An accident was reported on Ring Road 15 minutes ago. Emergency services are active. Routes have been auto-adjusted.';
  }
  if (q.includes('weather')) {
    return '🌧️ Light rain expected for the next 2 hours. Road surfaces may be wet — reduce speed.';
  }
  if (q.includes('emergency') || q.includes('ambulance')) {
    return '🚨 Emergency priority lanes are active. Fastest routes are locked for emergency vehicles.';
  }
  return 'I can help with congestion forecasts, route suggestions, accident reports, and weather updates. What would you like to know?';
}
