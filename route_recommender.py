import streamlit as st
import pandas as pd

def get_route_options(source, destination, is_emergency=False):
    """
    Simulates fetching route options with toll, ETA, traffic, and fuel metrics.
    """
    if is_emergency:
        routes = [
            {
                "type": "🚨 Emergency Priority Route",
                "eta": "28 mins (Priority)",
                "eta_mins": 28,
                "toll": "₹0 (Exempt)",
                "toll_cost": 0.0,
                "traffic": "Clearing lanes...",
                "fuel_efficiency": "N/A",
                "fuel_score": 0
            },
            {
                "type": "Alternative Backup ⚡",
                "eta": "32 mins",
                "eta_mins": 32,
                "toll": "₹0 (Exempt)",
                "toll_cost": 0.0,
                "traffic": "Moderate",
                "fuel_efficiency": "N/A",
                "fuel_score": 0
            }
        ]
    else:
        routes = [
            {
                "type": "Fastest Route ⚡",
                "eta": "35 mins",
                "eta_mins": 35,
                "toll": "₹150",
                "toll_cost": 8.50,
                "traffic": "Heavy",
                "fuel_efficiency": "22 MPG",
                "fuel_score": 22
            },
            {
                "type": "AI Recommended ✨",
                "eta": "40 mins",
                "eta_mins": 40,
                "toll": "₹45",
                "toll_cost": 2.50,
                "traffic": "Light",
                "fuel_efficiency": "32 MPG",
                "fuel_score": 32
            },
            {
                "type": "Cheapest Route 💰",
                "eta": "55 mins",
                "eta_mins": 55,
                "toll": "₹0",
                "toll_cost": 0.0,
                "traffic": "Moderate",
                "fuel_efficiency": "28 MPG",
                "fuel_score": 28
            }
        ]
    return routes

def calculate_ai_score(route):
    """
    Custom AI recommendation logic (lower score is better).
    Normalizes and weights ETA, Toll, and Fuel Efficiency.
    """
    score = (route["eta_mins"] * 1.0) + (route["toll_cost"] * 1.5) - (route["fuel_score"] * 0.5)
    return score

def display_route_recommendations(source, destination, vehicle_type="Normal"):
    """
    Renders the toll-aware route recommendation module in Streamlit.
    Reacts to Emergency Vehicle context.
    """
    is_emergency = vehicle_type in ["Ambulance", "Fire Truck"]
    routes = get_route_options(source, destination, is_emergency)
    
    st.subheader("🛣️ Smart Route Recommendations")
    
    if is_emergency:
        st.error(f"🚨 **EMERGENCY MODE ACTIVE ({vehicle_type}):** Tolls exempted. Prioritizing absolute shortest ETA and traffic clearing.")
    else:
        st.markdown("AI-analyzed routes factoring in **Tolls**, **Time**, and **Fuel Efficiency**.")
    
    cols = st.columns(len(routes))
    
    # Sort or mark the best AI route based on the logic
    best_route = min(routes, key=calculate_ai_score)
    
    for idx, route in enumerate(routes):
        with cols[idx]:
            # Highlight the AI Recommended/Emergency route
            is_best = (route == best_route)
            
            if is_emergency and is_best:
                card_color = "#B71C1C" # Deep red for emergency
                border_css = "border: 2px solid #FF5252;"
            else:
                card_color = "#2E7D32" if is_best else "#2D2D2D"
                border_css = "border: 2px solid #4CAF50;" if is_best else "border: 1px solid #444;"
            
            html = f"""
            <div style="background-color: {card_color}; padding: 15px; border-radius: 10px; {border_css} margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                <h4 style="margin-top: 0; color: #FFF;">{route['type']}</h4>
                <hr style="border-color: #555; margin: 10px 0;">
                <p style="margin: 5px 0;">⏱️ <b>ETA:</b> {route['eta']}</p>
                <p style="margin: 5px 0;">💵 <b>Toll Fee:</b> {route['toll']}</p>
                <p style="margin: 5px 0;">🚗 <b>Traffic:</b> {route['traffic']}</p>
                <p style="margin: 5px 0;">🌱 <b>Fuel Efficiency:</b> {route['fuel_efficiency']}</p>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)
