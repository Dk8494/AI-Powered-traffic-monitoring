import os
from predictor import predict_congestion

data = [
    {"lat": 28.5706, "lng": 77.3240, "time_of_day": 8, "weather": "Clear", "vehicle_volume": 420, "avg_speed": 18, "rain_mm": 0, "accident": "No", "event": "No", "public_transport_density": 65, "y_true": "High"},
    {"lat": 28.5942, "lng": 77.3053, "time_of_day": 8, "weather": "Cloudy", "vehicle_volume": 510, "avg_speed": 12, "rain_mm": 0, "accident": "Yes", "event": "No", "public_transport_density": 70, "y_true": "Very High"},
    {"lat": 28.4671, "lng": 77.5030, "time_of_day": 8, "weather": "Clear", "vehicle_volume": 300, "avg_speed": 35, "rain_mm": 0, "accident": "No", "event": "No", "public_transport_density": 40, "y_true": "Medium"},
    {"lat": 28.5636, "lng": 77.3340, "time_of_day": 9, "weather": "Rain", "vehicle_volume": 460, "avg_speed": 15, "rain_mm": 6, "accident": "No", "event": "Yes", "public_transport_density": 80, "y_true": "High"},
    {"lat": 28.6127, "lng": 77.2773, "time_of_day": 9, "weather": "Heavy Rain", "vehicle_volume": 620, "avg_speed": 10, "rain_mm": 14, "accident": "Yes", "event": "Yes", "public_transport_density": 90, "y_true": "Very High"}
]

matches = 0
for i, row in enumerate(data):
    pred = predict_congestion(
        lat=row["lat"], lng=row["lng"], time_of_day=row["time_of_day"], 
        weather=row["weather"], vehicle_volume=row["vehicle_volume"], 
        avg_speed=row["avg_speed"], rain_mm=row["rain_mm"], 
        accident=row["accident"], event=row["event"], 
        public_transport_density=row["public_transport_density"]
    )
    y_true = row["y_true"].upper().strip()
    pred_clean = pred.upper().strip() if pred else "NONE"
    print(f"Row {i+1}: True={y_true}, Pred={pred_clean}")
    if pred_clean == y_true:
        matches += 1

print(f"Match: {matches}/{len(data)} ({(matches/len(data))*100}%)")
