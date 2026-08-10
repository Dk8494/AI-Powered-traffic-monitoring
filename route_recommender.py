"""Route recommender logic without Streamlit dependency.
Provides `get_route_options` and `calculate_ai_score` for API use.
"""

def get_route_options(source, destination, is_emergency=False):
    """
    Simulates fetching route options with toll, ETA, traffic, and fuel metrics.
    Includes NHAI FASTag intelligence.
    """
    if is_emergency:
        routes = [
            {
                "type": "🚨 Emergency Priority Route",
                "eta": "28 mins (Priority)",
                "eta_mins": 28,
                "toll": "₹0 (FASTag Exempt)",
                "toll_cost": 0.0,
                "traffic": "Clearing lanes...",
                "fuel_efficiency": "N/A",
                "fuel_score": 0
            },
            {
                "type": "Alternative Backup ⚡",
                "eta": "32 mins",
                "eta_mins": 32,
                "toll": "₹0 (FASTag Exempt)",
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
                "toll": "₹150 (NHAI Highway)",
                "toll_cost": 150.0,
                "traffic": "Flowing / High Speed",
                "fuel_efficiency": "14 km/l",
                "fuel_score": 14
            },
            {
                "type": "Toll-Free Alternative 💰",
                "eta": "55 mins",
                "eta_mins": 55,
                "toll": "₹0",
                "toll_cost": 0.0,
                "traffic": "Heavy (City Roads)",
                "fuel_efficiency": "10 km/l",
                "fuel_score": 10
            },
            {
                "type": "Lowest Toll Route 🎫",
                "eta": "45 mins",
                "eta_mins": 45,
                "toll": "₹45 (State Highway)",
                "toll_cost": 45.0,
                "traffic": "Moderate",
                "fuel_efficiency": "12 km/l",
                "fuel_score": 12
            },
            {
                "type": "AI Recommended ✨",
                "eta": "40 mins",
                "eta_mins": 40,
                "toll": "₹65 (Smart Route)",
                "toll_cost": 65.0,
                "traffic": "Light / Bypassing Bottlenecks",
                "fuel_efficiency": "16 km/l",
                "fuel_score": 16
            }
        ]
    return routes

def calculate_ai_score(route):
    """
    Custom AI recommendation logic (lower score is better).
    Normalizes and weights ETA, Toll, and Fuel Efficiency.
    Note: Toll is scaled down so it's comparable with minutes.
    """
    score = (route["eta_mins"] * 1.5) + (route["toll_cost"] * 0.1) - (route["fuel_score"] * 1.2)
    return score

def display_route_recommendations(source, destination, vehicle_type="Normal"):
    """Return route recommendation payload usable by a frontend.

    Returns a dict with routes and the best route flagged.
    """
    is_emergency = vehicle_type in ["Ambulance", "Fire Truck"]
    routes = get_route_options(source, destination, is_emergency)
    best_route = min(routes, key=calculate_ai_score)

    result = {
        "is_emergency": is_emergency,
        "routes": [],
    }
    for r in routes:
        rr = r.copy()
        rr["recommended"] = (r == best_route)
        result["routes"].append(rr)

    return result
