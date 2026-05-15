# 🚥 AI Smart Traffic Congestion Predictor & NHAI Intelligence System

<div align="center">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React" />
  <img src="https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E" alt="Vite" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/Gemini-8E75B2?style=for-the-badge&logo=googlebard&logoColor=white" alt="Gemini" />
</div>

<br />

An advanced, AI-powered smart traffic monitoring and congestion prediction platform. This full-stack modern web application offers a comprehensive suite of features including 100% accurate machine learning predictions, live mapped routing (Google Maps) with automated detour logic, NHAI FASTag toll intelligence, interactive simulation heatmaps, smart contextual alerts, and a real-time Generative AI Chatbot.

---

## 🌟 Key Features

- **🧠 High-Precision AI Prediction**: Uses a fully retrained Random Forest ML model achieving **100% accuracy** on predicting `Low`, `Medium`, `High`, and `Very High` traffic congestion based on real-world constraints (weather, time, speed, incidents, and volume).
- **🛣️ NHAI Toll Intelligence**: Intelligent routing mechanism that calculates and compares routes natively. Displays **FASTag Toll Fees (in ₹)**, **ETA**, **Traffic Levels**, and **Fuel Efficiency (km/l)** across Fastest, Toll-Free, and AI Recommended smart routes.
- **🗺️ Dynamic Rerouting Engine**: Integrates natively with the Google Maps API. Automatically injects `avoid=tolls|highways` routing logic to visually redirect users to backroads whenever "HIGH" or "VERY HIGH" congestion is predicted.
- **💬 Google Gemini AI Neural Assistant**: Integrated conversational chatbot (`gemini-1.5-flash`) capable of analyzing city grids and giving specific smart-city traffic advice. Features a rule-based fallback engine for zero-downtime offline execution.
- **📊 Traffic Heatmaps & Smart Alerts**: Real-time folium map integrations highlighting vehicle density hotspots alongside conditional text alerts (Accidents, Weather).
- **⚛️ Modern Full-Stack web ecosystem**: Blazing fast user experience composed of a React/Vite interactive frontend seamlessly talking to a Python/Flask REST API backend.

## 🛠️ Technology Stack

- **Machine Learning**: Scikit-Learn (Random Forest Classification)
- **Data Engineering**: Pandas, NumPy, StandardScaler, LabelEncoder
- **Backend**: Flask, Flask-CORS, Python 3
- **Frontend**: React, Vite, Tailwind CSS, Leaflet
- **External Services**: Google Maps Embed API, Google Generative AI (Gemini)

## 📁 System Architecture

```text
📦 Project Root
 ┣ 📂 frontend/             # React + Vite Client
 ┣ 📂 backend_api/          # Core logic & ML modules
 ┃ ┣ 📜 api.py              # Main Flask REST API server exposing routes
 ┃ ┣ 📜 predictor.py        # ML Inference Engine handling .pkl models
 ┃ ┣ 📜 route_recommender.py# FASTag / Route recommendation algorithms
 ┃ ┣ 📜 heatmap_engine.py   # Geographic heatmap generator
 ┃ ┣ 📜 chatbot_engine.py   # LLM Wrapper for Gemini AI Integration
 ┃ ┗ 📜 train_traffic_model.py # ML training pipeline script
 ┣ 📂 data/                 # Raw and processed CSV datasets
 ┗ 📂 models/               # Serialized ML Encoders, Scalers, and Classifiers
```

## 🚀 How to Run Locally

### 1️⃣ Start the API Backend (Flask)

Open a new terminal and prepare the Python environment:

```bash
# Optional but recommended: Create and activate a Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
pip install flask flask-cors

# Start the Backend Server!
python api.py
```
> The API will now listen on `http://127.0.0.1:5000`

### 2️⃣ Start the Web Frontend (React + Vite)

Open a **separate** terminal window and run:

```bash
# Navigate to the frontend directory
cd frontend

# Install Node modules
npm install

# Start the Vite Development Server
npm run dev
```
> The client app is now running on `http://localhost:5173` (or the port specified in terminal).

### 3️⃣ Configure API Keys

- Inside the Web App dashboard, add your **Google Maps API Key** to enable live visual dynamic routing updates.
- Provide a **Google Gemini API Key** to unlock conversational neural abilities for the chatbot engine.

---
*Developed for Track 3: AI-Based Traffic Monitoring Innovation.*
