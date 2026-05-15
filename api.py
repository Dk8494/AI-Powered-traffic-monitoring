"""
Flask API backend — wraps existing Python modules for the React frontend.
"""
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

from predictor import predict_congestion
from route_recommender import get_route_options, calculate_ai_score
from alert_engine_api import generate_alerts
from chatbot_engine import get_ai_response
from heatmap_engine_api import get_heatmap_data

app = Flask(__name__)
CORS(app)


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """Run ML prediction with the given parameters."""
    data = request.json
    try:
        prediction = predict_congestion(
            lat=float(data.get("lat", 28.5706)),
            lng=float(data.get("lng", 77.3240)),
            time_of_day=int(data.get("time_of_day", datetime.datetime.now().hour)),
            weather=data.get("weather", "Clear"),
            vehicle_volume=int(data.get("vehicle_volume", 500)),
            avg_speed=int(data.get("avg_speed", 40)),
            rain_mm=float(data.get("rain_mm", 0.0)),
            accident=data.get("accident", "No"),
            event=data.get("event", "None"),
            public_transport_density=int(data.get("public_transport_density", 40)),
        )

        # Map prediction to a percentage for the frontend
        pct_map = {"LOW": 28, "MEDIUM": 55, "HIGH": 78}
        percentage = pct_map.get(prediction, 50)

        return jsonify({
            "prediction": prediction,
            "percentage": percentage,
            "level": prediction.capitalize() if prediction != "LOW" else "Low",
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/routes", methods=["POST"])
def api_routes():
    """Get route recommendations."""
    data = request.json
    source = data.get("source", "Sector 18 Noida")
    destination = data.get("destination", "Akshardham")
    vehicle_type = data.get("vehicle_type", "Normal")
    is_emergency = vehicle_type in ["Ambulance", "Fire Truck"]

    routes = get_route_options(source, destination, is_emergency)
    best = min(routes, key=calculate_ai_score)

    result = []
    for r in routes:
        result.append({
            "name": r["type"],
            "eta": r["eta"],
            "eta_mins": r["eta_mins"],
            "toll": r["toll"],
            "traffic": r["traffic"],
            "fuel_efficiency": r["fuel_efficiency"],
            "recommended": r == best,
        })
    return jsonify({"routes": result, "is_emergency": is_emergency})


@app.route("/api/alerts", methods=["POST"])
def api_alerts():
    """Generate contextual alerts."""
    data = request.json
    alerts = generate_alerts(
        prediction=data.get("prediction", "LOW"),
        weather=data.get("weather", "Clear"),
        accident=data.get("accident", "No"),
        event=data.get("event", "None"),
    )
    return jsonify({"alerts": alerts})


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """AI chatbot response."""
    data = request.json
    query = data.get("query", "")
    response = get_ai_response(query)
    return jsonify({"response": response})


@app.route("/api/heatmap", methods=["GET"])
def api_heatmap():
    """Get heatmap data points."""
    lat = float(request.args.get("lat", 28.5706))
    lng = float(request.args.get("lng", 77.3240))
    data = get_heatmap_data(lat, lng)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
