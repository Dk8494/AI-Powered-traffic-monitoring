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

# --- CONSTANTS ---
# Replace this with your actual Google Maps API Key
GOOGLE_MAPS_API_KEY = "AIzaSyBE9GpUrBD2eO_W2ACBKZ_ckTB4Kas8Rlc" \
""

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
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Global Cyberpunk Dark Theme */
    html, body, [class*="css"] { 
        font-family: 'Space Grotesk', sans-serif; 
    }
    .stApp { background: radial-gradient(circle at top center, #121218 0%, #050505 100%) !important; color: #E0E0E0; }
    
    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(10, 10, 12, 0.6) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(0, 240, 255, 0.15);
    }
    
    /* Futuristic glowing buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #00F0FF 0%, #8A2BE2 100%);
        color: #FFFFFF !important;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 0 25px rgba(138, 43, 226, 0.6);
        border: 1px solid #00F0FF;
    }
    
    /* Palantir-style KPI Cards */
    .kpi-card {
        background: rgba(20, 20, 25, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 240, 255, 0.15);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    
    /* Animated Radar scanning effect on hover */
    .kpi-card::before {
        content: ''; position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
        background: linear-gradient(to right, transparent, rgba(0, 240, 255, 0.1), transparent);
        transform: skewX(-25deg); opacity: 0; transition: opacity 0.3s ease;
    }
    .kpi-card:hover::before { opacity: 1; animation: scan 1.5s infinite; }
    @keyframes scan { 0% { left: -100%; } 100% { left: 200%; } }
    
    .kpi-card:hover { 
        transform: translateY(-5px); 
        border-color: #00F0FF; 
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
    }
    .kpi-title { font-size: 0.85rem; color: #8892B0; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 2px; }
    .kpi-value { font-family: 'JetBrains Mono', monospace; font-size: 2.2rem; font-weight: 700; color: #00F0FF; text-shadow: 0 0 10px rgba(0,240,255,0.4); }
    
    /* Dynamic AI Alerts */
    .alert-banner { padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 20px; animation: glowPulse 2s infinite alternate; backdrop-filter: blur(10px); }
    .alert-low { background: rgba(0, 255, 102, 0.05); border: 1px solid #00FF66; color: #00FF66; text-shadow: 0 0 10px rgba(0,255,102,0.4); }
    .alert-medium { background: rgba(255, 152, 0, 0.05); border: 1px solid #FF9800; color: #FF9800; text-shadow: 0 0 10px rgba(255,152,0,0.4); }
    .alert-high { background: rgba(255, 0, 60, 0.05); border: 1px solid #FF003C; color: #FF003C; text-shadow: 0 0 10px rgba(255,0,60,0.4); }
    
    @keyframes glowPulse { 
        0% { box-shadow: inset 0 0 10px rgba(255,255,255,0.02); } 
        100% { box-shadow: inset 0 0 20px rgba(255,255,255,0.05); } 
    }
    
    /* Typography Overrides */
    h1, h2, h3 { color: #FFFFFF !important; font-family: 'Space Grotesk', sans-serif !important; }
    hr { border-color: rgba(0, 240, 255, 0.2) !important; }
    
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
        with st.expander("🔑 API Integrations", expanded=False):
            gemini_key = st.text_input("Gemini API Key", type="password", help="Add key to enable live AI Chatbot. Leave blank to use safe fallback mode.")
        with st.expander("�📍 Location & Routing", expanded=True):
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
        
        if predict_btn:
            st.session_state.dashboard_active = True
            
    # Try to keep dashboard open permanently if it was ever opened
    if 'dashboard_active' not in st.session_state:
        st.session_state.dashboard_active = False

    # --- 5. Main Dashboard Architecture ---
    if st.session_state.dashboard_active:
        try:
            with st.spinner('Synchronizing modules & running neural network...'):
                if predict_btn: # Only delay on the initial click
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
                
                # Check UI option to show alternate routes
                show_alternate = st.checkbox("Show Alternate Detour Route (Avoid Tolls & Highways)", value=False)
                
                if GOOGLE_MAPS_API_KEY and GOOGLE_MAPS_API_KEY != "YOUR_GOOGLE_MAPS_API_KEY_HERE":
                    origin_encoded = urllib.parse.quote(source)
                    dest_encoded = urllib.parse.quote(destination)
                    
                    if show_alternate or prediction in ["HIGH", "VERY HIGH"]:
                        st.info("🔄 Congestion active. Displaying alternative avoidance route.")
                        # Force alternate route by avoiding tolls/highways in Maps Embed API
                        map_url = f"https://www.google.com/maps/embed/v1/directions?key={GOOGLE_MAPS_API_KEY}&origin={origin_encoded}&destination={dest_encoded}&mode=driving&avoid=tolls|highways"
                    else:
                        map_url = f"https://www.google.com/maps/embed/v1/directions?key={GOOGLE_MAPS_API_KEY}&origin={origin_encoded}&destination={dest_encoded}&mode=driving"
                        
                    st.markdown(f'<iframe width="100%" height="450" style="border:1px solid #333; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.5);" loading="lazy" allowfullscreen src="{map_url}"></iframe>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Please configure the GOOGLE_MAPS_API_KEY constant in app.py to enable live tracking.")
                    
            with col_heat:
                display_heatmap()
            st.divider()

            # Module 7: AI Chatbot
            import os
            if gemini_key:
                os.environ["GEMINI_API_KEY"] = gemini_key
            else:
                os.environ.pop("GEMINI_API_KEY", None)
                
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
