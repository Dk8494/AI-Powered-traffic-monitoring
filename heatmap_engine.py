import folium
from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import st_folium
import numpy as np

def generate_simulated_hotspots(base_lat, base_lng, num_spots=100):
    """Generates simulated traffic congestion points around a base location."""
    np.random.seed(42) # For reproducible hotspots in demo
    points = []
    for _ in range(num_spots):
        # Slightly offset lat/lng to create a cluster
        lat = base_lat + np.random.normal(0, 0.05)
        lng = base_lng + np.random.normal(0, 0.05)
        intensity = np.random.uniform(0.4, 1.0) # Heat intensity
        points.append([lat, lng, intensity])
    return points
def display_heatmap():
    """
    Renders an interactive Folium HeatMap of traffic congestion in Streamlit.
    """
    st.subheader("🔥 Live Congestion Heatmap (Simulated)")
    st.markdown("Visualizing AI-detected traffic hotspots and high-density zones across the region.")
    
    # Defaulting base map to San Francisco coordinates for the simulation
    base_lat, base_lng = 37.7749, -122.4194
    
    # Create Folium Map with a sleek dark theme
    m = folium.Map(location=[base_lat, base_lng], zoom_start=11, tiles="CartoDB dark_matter")
    
    # Generate data
    hotspots = generate_simulated_hotspots(base_lat, base_lng, num_spots=150)
    
    # Overlay HeatMap
    HeatMap(hotspots, radius=15, blur=15, max_zoom=1).add_to(m)
    
    # Add a few distinct marker popup labels for major incidents
    major_incidents = [
        {"loc": [37.7749, -122.4194], "label": "Downtown Blockage"},
        {"loc": [37.8044, -122.2712], "label": "Bridge Accident"},
        {"loc": [37.7338, -122.4467], "label": "Construction Delay"}
    ]
    
    for incident in major_incidents:
        folium.Marker(
            location=incident["loc"],
            popup=f"⚠️ {incident['label']}",
            tooltip="Click for details",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
        
    # Render map in Streamlit perfectly contained
    st_folium(m, width="100%", height=500, returned_objects=[])
