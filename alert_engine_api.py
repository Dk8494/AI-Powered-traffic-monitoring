"""
Alert engine adapted for API use (no Streamlit dependency).
"""

def generate_alerts(prediction, weather, accident, event):
    """Returns a list of alert dicts based on current conditions."""
    alerts = []

    if prediction == "HIGH":
        alerts.append({
            "type": "danger",
            "icon": "🛑",
            "text": "HIGH CONGESTION: Expect severe delays. Alternative routes are strongly advised."
        })
    elif prediction in ["MEDIUM", "Moderate"]:
        alerts.append({
            "type": "warning",
            "icon": "⚠️",
            "text": "MODERATE CONGESTION: Traffic is building up in this zone. Allow extra travel time."
        })

    if accident == "Yes":
        alerts.append({
            "type": "danger",
            "icon": "💥",
            "text": "ACCIDENT REPORTED: An accident has been reported nearby. Emergency services may be en route."
        })

    if weather == "Rain":
        alerts.append({
            "type": "warning",
            "icon": "🌧️",
            "text": "WEATHER ALERT (Rain): Wet roads and potential hydroplaning. Reduce speed."
        })
    elif weather == "Snow":
        alerts.append({
            "type": "danger",
            "icon": "❄️",
            "text": "WEATHER ALERT (Snow): Icy roads detected. Only travel if necessary."
        })
    elif weather == "Fog":
        alerts.append({
            "type": "warning",
            "icon": "🌫️",
            "text": "WEATHER ALERT (Fog): Severely reduced visibility. Keep low-beam headlights on."
        })
    elif weather == "Heavy Rain":
        alerts.append({
            "type": "danger",
            "icon": "⛈️",
            "text": "WEATHER ALERT (Heavy Rain): Flooding risk. Avoid low-lying areas."
        })

    if event not in ["None", "No"]:
        alerts.append({
            "type": "info",
            "icon": "🎉",
            "text": f"SPECIAL EVENT ({event}): Increased pedestrian crossings and road closures expected."
        })

    if not alerts:
        alerts.append({
            "type": "success",
            "icon": "✅",
            "text": "ALL CLEAR: No active weather, accident, or congestion alerts. Safe travels!"
        })

    return alerts
