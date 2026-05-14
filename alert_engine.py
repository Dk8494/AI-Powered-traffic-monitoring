import streamlit as st

def display_alerts(prediction, weather, accident, event):
    """
    Renders smart traffic alerts based on the AI prediction and user inputs.
    """
    st.subheader("🚨 Live Active Alerts")
    
    # Track if any major alerts fired
    alerts_fired = False
    
    # 1. Congestion Alerts
    if prediction == "HIGH":
        st.error("🛑 **HIGH CONGESTION:** Expect severe delays. Alternative routes are strongly advised.")
        alerts_fired = True
    elif prediction in ["MEDIUM", "Moderate"]:
        st.warning("⚠️ **MODERATE CONGESTION:** Traffic is building up in this zone. Allow extra travel time.")
        alerts_fired = True
    
    # 2. Accident Alerts
    if accident == "Yes":
        st.error("💥 **ACCIDENT REPORTED:** An accident has been reported nearby. Emergency services may be on route. Expect sudden stops.")
        alerts_fired = True
        
    # 3. Weather Alerts
    if weather == "Rain":
        st.warning("🌧️ **WEATHER ALERT (Rain):** Wet roads and potential hydroplaning. Reduce speed and increase following distance.")
        alerts_fired = True
    elif weather == "Snow":
        st.error("❄️ **WEATHER ALERT (Snow):** Icy roads detected. Only travel if necessary and use winter tires or chains.")
        alerts_fired = True
    elif weather == "Fog":
        st.warning("🌫️ **WEATHER ALERT (Fog):** Severely reduced visibility. Keep low-beam headlights on.")
        alerts_fired = True
        
    # 4. Event Alerts
    if event != "None":
        st.info(f"🎉 **SPECIAL EVENT ({event}):** Increased pedestrian crossings and event-related road closures expected in the vicinity.")
        alerts_fired = True
        
    # Fallback if conditions are perfect
    if not alerts_fired:
        st.success("✅ **ALL CLEAR:** No active weather, accident, or congestion alerts. Safe travels!")
