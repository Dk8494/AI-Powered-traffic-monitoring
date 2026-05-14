import os
import joblib
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
MODEL_PATH = os.path.join("models", "traffic_model.pkl")

# Mappings
WEATHER_MAPPING = {"Clear": 0, "Rain": 1, "Snow": 2, "Fog": 3, "Cloudy": 4, "Heavy Rain": 5}
ACCIDENT_MAPPING = {"No": 0, "Yes": 1}
EVENT_MAPPING = {"None": 0, "No": 0, "Concert": 1, "Sports Game": 2, "Festival": 3, "Yes": 4}
CONGESTION_LEVELS = {0: "LOW", 1: "MEDIUM", 2: "HIGH"}

def load_model():
    """Loads the trained RandomForest model."""
    if not os.path.exists(MODEL_PATH):
        logger.warning(f"Model not found at {MODEL_PATH}.")
        return None
    try:
        return joblib.load(MODEL_PATH)
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return None

def predict_congestion(lat, lng, time_of_day, weather, vehicle_volume, avg_speed, rain_mm, accident, event, public_transport_density):
    """
    Predicts the traffic congestion level based on inputs.
    
    Args:
        latitude (float): Location latitude
        longitude (float): Location longitude
        time_of_day (int): Hour of the day (0-23)
        weather_condition (str): Weather description ('Clear', 'Rain', 'Snow', 'Fog')
        
    Returns:
        str: 'LOW', 'MEDIUM', or 'HIGH'
    """
    try:
        # Validate and preprocess input
        if not isinstance(time_of_day, (int, float)) or not (0 <= time_of_day <= 23):
            raise ValueError(f"Invalid time_of_day: {time_of_day}. Must be between 0 and 23.")
            
        hour = int(time_of_day)
        
        if weather not in WEATHER_MAPPING:
            logger.warning(f"Unknown weather condition '{weather}'. Defaulting to 'Clear'.")
            
        weather_encoded = WEATHER_MAPPING.get(weather, 0)
        accident_encoded = ACCIDENT_MAPPING.get(accident, 0)
        event_encoded = EVENT_MAPPING.get(event, 0)
        
        # Prepare features for the model (matching dummy timestamp/location to bypass dimension errors)
        # Expected shape matches the dataset features: [Timestamp, Location, Latitude, Longitude, Traffic Volume, Avg Speed, Weather, Rain, Accident, Event, Public Transport]
        features = np.array([[hour, 0, lat, lng, vehicle_volume, avg_speed, weather_encoded, rain_mm, accident_encoded, event_encoded, public_transport_density]])
        
        # Load Model
        model = load_model()
        
        if model is not None:
            # Predict using the ML model
            prediction_idx = model.predict(features)[0]
            prediction_text = CONGESTION_LEVELS.get(prediction_idx, "LOW")
            return prediction_text
        else:
            # Fallback heuristic if the model is not trained yet
            return get_heuristic_prediction(hour, weather)

    except Exception as e:
        # Handle invalid inputs safely with a default return
        logger.error(f"Prediction failed: {str(e)}. Returning default LOW.")
        return "LOW"

def get_heuristic_prediction(hour, weather):
    """Fallback rule-based heuristic prediction."""
    if hour in [8, 9, 17, 18]:
        return "HIGH"
    elif hour in [7, 10, 16, 19] or weather in ["Rain", "Snow"]:
        return "MEDIUM"
    else:
        return "LOW"
