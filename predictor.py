import os
import joblib
import numpy as np
import pandas as pd
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Paths
MODEL_PATH = os.path.join("models", "traffic_model.pkl")
SCALER_PATH = os.path.join("models", "scaler.pkl")
ENCODERS_PATH = os.path.join("models", "label_encoders.pkl")

def load_objects():
    """Loads the trained ML model, scaler, and encoders."""
    try:
        model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
        scaler = joblib.load(SCALER_PATH) if os.path.exists(SCALER_PATH) else None
        encoders = joblib.load(ENCODERS_PATH) if os.path.exists(ENCODERS_PATH) else None
        return model, scaler, encoders
    except Exception as e:
        logger.error(f"Error loading models/transformers: {e}")
        return None, None, None

def get_heuristic_prediction(hour, weather):
    """Fallback rule-based heuristic prediction."""
    if hour in [8, 9, 17, 18]:
        return "HIGH"
    elif hour in [7, 10, 16, 19] or weather in ["Rain", "Snow"]:
        return "MEDIUM"
    else:
        return "LOW"

def predict_congestion(lat, lng, time_of_day, weather, vehicle_volume, avg_speed, rain_mm, accident, event, public_transport_density):
    """
    Predicts the traffic congestion level based on inputs using the trained model and loaded transformers.
    """
    try:
        model, scaler, encoders = load_objects()

        if model is None or scaler is None or encoders is None:
            logger.warning("Missing trained models or transformers. Using fallback.")
            return get_heuristic_prediction(int(time_of_day), weather)

        # 1. Create a DataFrame with a single row of the raw input
        # Note: 'Timestamp' and 'Location' were in the original dataframe. We pass mock data that fits the encoders.
        # Original columns order: 'Timestamp', 'Location', 'Latitude', 'Longitude', 'Traffic Volume', 'Avg Speed (km/h)', 'Weather', 'Rain(mm)', 'Accident', 'Event', 'Public Transport Density'
        
        # We need to map inputs to strings or values expected by the encoders.
        # If 'Timestamp' and 'Location' are not provided, we mock them to the first known class to bypass the transform error.
        timestamp_mock = encoders['Timestamp'].classes_[0] if 'Timestamp' in encoders else "2026-05-14 08:00"
        location_mock = encoders['Location'].classes_[0] if 'Location' in encoders else "Sector 18 Noida"
        weather_val = weather if weather in encoders['Weather'].classes_ else encoders['Weather'].classes_[0]
        accident_val = accident if accident in encoders['Accident'].classes_ else encoders['Accident'].classes_[0]
        event_val = event if event in encoders['Event'].classes_ else encoders['Event'].classes_[0]
        
        raw_data = {
            'Timestamp': [timestamp_mock],
            'Location': [location_mock],
            'Latitude': [float(lat)],
            'Longitude': [float(lng)],
            'Traffic Volume': [int(vehicle_volume)],
            'Avg Speed (km/h)': [float(avg_speed)],
            'Weather': [weather_val],
            'Rain(mm)': [float(rain_mm)],
            'Accident': [accident_val],
            'Event': [event_val],
            'Public Transport Density': [int(public_transport_density)]
        }
        
        df = pd.DataFrame(raw_data)
        
        # 2. Encode categorical columns
        categorical_cols = ['Timestamp', 'Location', 'Weather', 'Accident', 'Event']
        for col in categorical_cols:
            if col in encoders:
                df[col] = encoders[col].transform(df[col])
                
        # 3. Scale numerical columns
        numerical_cols = ['Latitude', 'Longitude', 'Traffic Volume', 'Avg Speed (km/h)', 'Rain(mm)', 'Public Transport Density']
        df[numerical_cols] = scaler.transform(df[numerical_cols])

        # 4. Predict
        prediction_encoded = model.predict(df)[0]
        
        # 5. Decode Target
        if 'target' in encoders:
            prediction_text = encoders['target'].inverse_transform([prediction_encoded])[0]
        else:
            # Fallback if target encoder is somehow missing
            mapping = {0: "High", 1: "Low", 2: "Medium", 3: "Very High"}
            prediction_text = mapping.get(prediction_encoded, "Unknown")

        return prediction_text.upper()

    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}. Returning default LOW.")
        return get_heuristic_prediction(int(time_of_day), weather)

