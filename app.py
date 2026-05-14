import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import datetime
import urllib.parse
import time
import logging

# Configure basic logging for error handling
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Modular Imports ---
# Wrapping imports in try-except ensures the app loads even if a library fails
try:
    from predictor import predict_congestion
    from route_recommender import display_route_recommendations
    from heatmap_engine import display_heatmap
    from alert_engine import display_alerts
    from chatbot_engine import display_chatbot
    MODULES_LOADED = True
except Exception as e:
    logger.error(f"Failed to load modules: {e}")
    MODULES_LOADED = False

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Traffic Congestion Predictor",
    page_icon="🚥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Enhanced CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #121212; color: #E0E0E0; }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #121212 !important;
        font-weight: 800;
        border-radius: 12px;
        padding: 12px;
        border: none;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 15px rgba(0, 201, 255, 0.4);
    }
    
    .kpi-card {
        background: #1E1E1E; border: 1px solid #333; padding: 20px; border-radius: 15px;
        text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.5); transition: transform 0.3s ease; margin-bottom: 20px;
    }
    .kpi-card:hover { transform: translateY(-5px); border-color: #00C9FF; }
    .kpi-title { font-size: 1rem; color: #A0A0A0; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }
    .kpi-value { font-size: 2rem; font-weight: 800; color: #FFFFFF; }
    
    .alert-banner { padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 20px; animation: fadeIn 0.5s ease-in-out; }
    .alert-low { background: rgba(76, 175, 80, 0.1); border: 2px solid #4CAF50; color: #4CAF50; }
    .alert-medium { background: rgba(255, 152, 0, 0.1); border: 2px solid #FF9800; color: #FF9800; }
    .alert-high { background: rgba(244, 67, 54, 0.1); border: 2px solid #F44336; color: #F44336; }
    @keyframes fadeIn { 0% { opacity: 0; transform: translateY(-10px); } 100% { opacity: 1; transform: translateY(0); } }
    </style>
""", unsafe_allow_html=True)

def main():
    if not MODULES_LOADED:
        st.error("Critical modules failed to load. Please check terminal logs and ensure dependencies are installed.")
        return

    # --- 3. Header ---
    st.markdown("<h1 style='text-align: center; font-weight: 800; background: -webkit-linear-gradient(#00C9FF, #92FE9D); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🚥 AI Smart Traffic Congestion Predictor</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A0A0A0; font-size: 1.2rem;'>Integrated Machine Learning, Live Mapping, and Emergency Routing Dashboard</p>", unsafe_allow_html=True)
    st.divider()

    # --- 4. Sidebar Inputs (Modular Configuration) ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2830/2830305.png", width=80)
        st.header("🚦 Mission Control")
        
        with st.expander("📍 Location & Routing", expanded=True):
            api_key = st.text_input("🔑 Google Maps API Key", type="password", help="Required for live directions iframe")
            source = st.text_input("🟢 Source", value="Sector 18 Noida")
            destination = st.text_input("🔴 Destination", value="Akshardham")
            lat = st.number_input("🗺️ Latitude", value=28.5706, format="%.4f")
            lng = st.number_input("🗺️ Longitude", value=77.3240, format="%.4f")

        with st.expander("⚙️ AI Context Variables", expanded=True):
            time_of_day = st.slider("🕒 Time of Day", 0, 23, datetime.datetime.now().hour, format="%d:00")
            vehicle_count = st.number_input("🚗 Vehicles/hr", min_value=0, max_value=10000, value=500, step=50)
            avg_speed = st.number_input("⏱️ Avg Speed (km/h)", min_value=0, max_value=200, value=40, step=5)
            weather_condition = st.selectbox("☁️ Weather", ["Clear", "Rain", "Snow", "Fog", "Cloudy", "Heavy Rain"])
            rain_mm = st.number_input("🌧️ Rain (mm)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
            accident = st.selectbox("⚠️ Accident Nearby?", ["No", "Yes"])
            event = st.selectbox("🎉 Special Event?", ["None", "Concert", "Sports Game", "Festival", "Yes", "No"])
            public_transport_density = st.number_input("🚌 Public Transport Density", min_value=0, max_value=100, value=40, step=5)

        st.markdown("---")
        vehicle_type = st.selectbox("🚑 Vehicle Type", ["Normal", "Ambulance", "Fire Truck"])
        
        st.markdown("---")
        predict_btn = st.button("🚀 INITIATE AI PREDICTION")

    # --- 5. Main Dashboard Architecture ---
    if predict_btn:
        try:
            with st.spinner('Synchronizing modules & running neural network...'):
                time.sleep(0.8) # Sleek UI delay
                # Module 1: ML Prediction
                prediction = predict_congestion(
                    lat=lat, lng=lng, time_of_day=time_of_day, weather=weather_condition, 
                    vehicle_volume=vehicle_count, avg_speed=avg_speed, 
                    rain_mm=rain_mm, accident=accident, 
                    event=event, public_transport_density=public_transport_density
                )
                
            if prediction == "LOW" and vehicle_type == "Normal":
                st.balloons()
                
            # KPI Telemetry
            st.markdown("### 📈 Live Telemetry")
            k1, k2, k3, k4 = st.columns(4)
            k1.markdown(f"<div class='kpi-card'><div class='kpi-title'>Vehicle Load</div><div class='kpi-value'>🚗 {vehicle_count}/hr</div></div>", unsafe_allow_html=True)
            k2.markdown(f"<div class='kpi-card'><div class='kpi-title'>Local Time</div><div class='kpi-value'>🕒 {time_of_day}:00</div></div>", unsafe_allow_html=True)
            k3.markdown(f"<div class='kpi-card'><div class='kpi-title'>Weather</div><div class='kpi-value'>⛈️ {weather_condition}</div></div>", unsafe_allow_html=True)
            k4.markdown(f"<div class='kpi-card'><div class='kpi-title'>Status</div><div class='kpi-value'>⚡ Online</div></div>", unsafe_allow_html=True)

            # Master Output Banner
            if prediction == "LOW":
                st.markdown('<div class="alert-banner alert-low"><h1>✅ CONGESTION: LOW</h1><p>Traffic is flowing smoothly. Optimal driving conditions detected.</p></div>', unsafe_allow_html=True)
            elif prediction in ["MEDIUM", "Moderate"]:
                st.markdown('<div class="alert-banner alert-medium"><h1>⚠️ CONGESTION: MODERATE</h1><p>Traffic is building up. Minor delays expected. Drive safely.</p></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="alert-banner alert-high"><h1>🛑 CONGESTION: HIGH</h1><p>Severe gridlock detected. Seek alternate routes immediately.</p></div>', unsafe_allow_html=True)
            st.divider()

            # Module 2: Smart Alerts Engine
            display_alerts(prediction, weather_condition, accident, event)
            st.divider()

            # Module 3 & 4: Route Recommender + Toll & Emergency Engine
            display_route_recommendations(source, destination, vehicle_type)
            st.divider()

            # Module 5 & 6: Google Maps iframe + Folium Heatmap
            col_map, col_heat = st.columns([1.2, 1])
            with col_map:
                st.subheader("🗺️ Live Directions Mapping")
                if api_key:
                    origin_encoded = urllib.parse.quote(source)
                    dest_encoded = urllib.parse.quote(destination)
                    map_url = f"https://www.google.com/maps/embed/v1/directions?key={api_key}&origin={origin_encoded}&destination={dest_encoded}&mode=driving"
                    st.markdown(f'<iframe width="100%" height="450" style="border:1px solid #333; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.5);" loading="lazy" allowfullscreen src="{map_url}"></iframe>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Enter Google Maps API Key in sidebar configuring routing iframe.")
                    
            with col_heat:
                display_heatmap()
            st.divider()
            
            # Module 7: AI Chatbot
            display_chatbot()

        except Exception as e:
            st.error(f"An unexpected error occurred during prediction generation: {str(e)}")
            logger.error(f"Runtime error: {e}")
            
    else:
        # Idle State
        st.info("👈 System Standby: Configure parameters in the Mission Control panel and click **Initiate AI Prediction**.")
        c1, c2, c3 = st.columns(3)
        c1.markdown("<div class='kpi-card'><div class='kpi-title'>Modules Integrated</div><div class='kpi-value'>🟢 7/7 Active</div></div>", unsafe_allow_html=True)
        c2.markdown("<div class='kpi-card'><div class='kpi-title'>ML Model Status</div><div class='kpi-value'>🟢 Ready</div></div>", unsafe_allow_html=True)
        c3.markdown("<div class='kpi-card'><div class='kpi-title'>UI Architecture</div><div class='kpi-value'>⚡ Modular</div></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
