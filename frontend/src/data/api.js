const API = 'http://127.0.0.1:5000/api';

export async function fetchPrediction(params) {
  const res = await fetch(`${API}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  });
  return res.json();
}

export async function fetchRoutes(params) {
  const res = await fetch(`${API}/routes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  });
  return res.json();
}

export async function fetchAlerts(params) {
  const res = await fetch(`${API}/alerts`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  });
  return res.json();
}

export async function fetchChat(query) {
  const res = await fetch(`${API}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  return res.json();
}

export async function fetchHeatmap(lat, lng) {
  const res = await fetch(`${API}/heatmap?lat=${lat}&lng=${lng}`);
  return res.json();
}
