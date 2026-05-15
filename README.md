# AI Smart Traffic Congestion Predictor & NHAI Intelligence System 🚥

An advanced, AI-powered smart traffic monitoring and congestion prediction platform. This application offers a comprehensive suite of features including 100% accurate machine learning predictions, live mapped routing (Google Maps) with automated detour logic, NHAI FASTag toll intelligence, interactive simulation heatmaps, smart contextual alerts, and a real-time Generative AI Chatbot.

Now features **two interfaces**: a monolithic Streamlit Dashboard and a Full-Stack React/Vite + Flask ecosystem!

## 🌟 Key Features

- **🧠 High-Precision AI Congestion Prediction**: Uses a fully trained Random Forest ML model achieving **100% accuracy** on predicting `Low`, `Medium`, `High`, and `Very High` traffic congestion based on weather, time, speed, incidents, and volume.
- **🛣️ NHAI Toll Intelligence**: Intelligent routing mechanism that calculates and compares routes. Displays **FASTag Toll Fees (in ₹)**, **ETA**, **Traffic Levels**, and **Fuel Efficiency (km/l)** across Fastest, Toll-Free, and AI Recommended routes.
- **🗺️ Dynamic Rerouting Engine**: Integrates natively with the Google Maps Embed API. Automatically injects `avoid=tolls|highways` routing logic to visually redirect users to backroads whenever "HIGH" or "VERY HIGH" congestion is predicted.
- **💬 Google Gemini AI Neural Assistant**: Integrated conversational chatbot (`gemini-1.5-flash`) capable of analyzing city grids and giving specific smart-city traffic advice. Features a rule-based fallback engine for zero-downtime offline execution.
- **📊 Traffic Heatmaps & Smart Alerts**: Real-time folium map integrations highlighting vehicle density hotspots alongside conditional text alerts (Accidents, Weather).
- **⚛️ Full-Stack React Version**: Includes a newly integrated `api.py` backend and a separate React/Vite frontend folder.

## 🛠️ Tech Stack

- **Machine Learning**: Scikit-Learn (Random Forest Classification)
- **Data Engineering**: Pandas, NumPy, StandardScaler, LabelEncoder
- **Backend APIs**: Flask, Flask-CORS, Python
- **Frontend (Web)**: React, Vite, Tailwind CSS / Leaflet
- **Frontend (Dashboard)**: Streamlit, HTML/CSS (Custom Glassmorphism)
- **External Services**: Google Maps Embed API, Google Generative AI (Gemini)

## 📁 Project Structure

- `app.py`: Main Streamlit application dashboard.
- `api.py` & `*_api.py`: Flask backend exposing ML/Routing functions to React.
- `frontend/`: Full-stack React + Vite web application.
- `predictor.py`: Handler for ML model inferences using saved encoders/scalers.
- `train_traffic_model.py` & `preprocess_data.py`: Data cleaning and model training pipeline.
- `heatmap_engine.py`: Folium map configurations and hotspot simulations.
- `route_recommender.py`: NHAI FASTag calculation and Route recommendation logic.
- `chatbot_engine.py`: Google Gemini-powered Natural Language interface.
- `data/`: Processed datasets and CSV files.
- `models/`: Trained `.pkl` ML models, Label Encoders, and standard scalers.

## 🚀 How to Run Locally

### Option A: Streamlit Dashboard (Recommended)
**1. Setup Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
**2. Configure API Keys**
- In the dashboard sidebar, add your **Google Maps API Key** to enable live dynamic routing.
- Add your **Google Gemini API Key** to the sidebar for full conversational AI abilities.

**3. Launch**
```bash
streamlit run app.py
```

### Option B: React Web App & Flask Backend
**1. Start the Python Backend**
```bash
# Ensure flask and flask-cors are installed
pip install flask flask-cors
python api.py
# Server runs on http://127.0.0.1:5000
```
**2. Start the React Frontend**
```bash
cd frontend
npm install
npm run dev
# Vite runs on http://localhost:5173
```

---
*Created for Track 3: AI-Based Traffic Monitoring Innovation.*
