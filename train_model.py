import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

def create_synthetic_data(num_samples=1000):
    np.random.seed(42)
    # Features: hour of day, weather condition (0=Clear, 1=Rain, 2=Snow, 3=Fog)
    hours = np.random.randint(0, 24, num_samples)
    weather = np.random.choice([0, 1, 2, 3], num_samples, p=[0.7, 0.2, 0.05, 0.05])
    
    # Target: 0=Low, 1=Moderate, 2=High
    congestion = []
    for h, w in zip(hours, weather):
        score = 0
        if h in [8, 9, 17, 18]: score += 2 # Rush hour
        elif h in [7, 10, 16, 19]: score += 1
        
        if w in [1, 3]: score += 1 # Rain or fog
        elif w == 2: score += 2 # Snow
        
        if score >= 3: congestion.append(2)
        elif score >= 1: congestion.append(1)
        else: congestion.append(0)
        
    return pd.DataFrame({'time_of_day': hours, 'weather': weather, 'congestion_level': congestion})

def train():
    print("Generating synthetic data...")
    df = create_synthetic_data(5000)
    
    X = df[['time_of_day', 'weather']]
    y = df['congestion_level']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training RandomForest model...")
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"Model Accuracy on Test Set: {accuracy:.2f}")
    
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/rf_model.pkl')
    print("Model saved to models/rf_model.pkl")

if __name__ == "__main__":
    train()
