import sys
from predictor import predict_congestion

print("Testing Traffic Congestion Predictor")
print("-" * 40)

tests = [
    {"name": "Low Traffic (Midnight, Clear)", "params": {"lat": 28.57, "lng": 77.32, "time_of_day": 2, "weather": "Clear", "vehicle_volume": 50, "avg_speed": 60, "rain_mm": 0, "accident": "No", "event": "None", "public_transport_density": 10}},
    {"name": "Medium Traffic (10 AM, Rain)", "params": {"lat": 28.57, "lng": 77.32, "time_of_day": 10, "weather": "Rain", "vehicle_volume": 400, "avg_speed": 35, "rain_mm": 5, "accident": "No", "event": "None", "public_transport_density": 60}},
    {"name": "High Traffic (6 PM, Accident)", "params": {"lat": 28.59, "lng": 77.30, "time_of_day": 18, "weather": "Clear", "vehicle_volume": 800, "avg_speed": 15, "rain_mm": 0, "accident": "Yes", "event": "Concert", "public_transport_density": 80}},
]

for t in tests:
    print(f"Scenario: {t['name']}")
    res = predict_congestion(**t["params"])
    print(f"Prediction: {res}\n")

