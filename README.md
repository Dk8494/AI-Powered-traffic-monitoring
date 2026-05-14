# AI Smart Traffic Congestion Predictor 🚥

An AI-powered smart traffic monitoring and congestion prediction system. This application offers a comprehensive dashboard with machine learning predictions, live routing mapping using Google Maps, interactive simulation heatmaps, and smart alerts. 

## Features
- **AI Congestion Prediction**: Uses a RandomForest ML model to predict traffic congestion levels based on time of day, weather, vehicle volume, average speed, and incidents.
- **Dynamic Routing**: Integration with Google Maps Embed API for live directions.
- **Traffic Heatmaps**: Interactive Folium-based heatmaps showing simulated high-density zones.
- **Smart Alerts Engine**: Dynamic, real-time contextual alerts depending on traffic events and weather.
- **AI Chatbot Engine**: Built-in chatbot interface for user queries.

## Tech Stack
- **Frontend**: Streamlit, HTML/CSS (Custom Styling)
- **Machine Learning**: Scikit-Learn (Random Forest)
- **Data Processing**: Pandas, NumPy
- **Visualizations**: Folium, Streamlit Folium
- **APIs**: Google Maps Embed API

## Project Structure
- `app.py`: Main Streamlit application dashboard.
- `predictor.py`: Handler for the Machine Learning model inferences. 
- `train_traffic_model.py`: Pipeline for training the ML model.
- `preprocess_data.py`: Data cleaning and Label Encoding pipeline.
- `heatmap_engine.py`: Folium map configurations and hotspot simulations.
- `route_recommender.py`: Recommends routes based on user type (e.g. Normal, Ambulance).
- `alert_engine.py`: Dynamic conditional alerts.
- `chatbot_engine.py`: Integrated chatbot module.
- `data/`: Directory for housing dataset files (`processed_traffic_data.csv`).
- `models/`: Directory housing trained `.pkl` models and encoders.

## How to Run Locally

### 1. Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
*(Make sure streamlit, pandas, scikit-learn, folium, streamlit-folium, and numpy are installed).*

### 3. Run the Application
```bash
streamlit run app.py
```

### 4. Configuration
Once the dashboard opens, go to the **Location & Routing** sidebar and paste your **Google Maps API Key** to enable live routing. Experiment with different **AI Context Variables** to see how the model and the UI adapt to varying traffic conditions!