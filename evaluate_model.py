import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, classification_report
import os

data_path = 'data/processed_traffic_data.csv'
model_path = 'models/traffic_model.pkl'
encoders_path = 'models/label_encoders.pkl'

if os.path.exists(data_path) and os.path.exists(model_path):
    # Load data
    df = pd.read_csv(data_path)
    X = df.drop(columns=['Congestion Level'])
    y_true = df['Congestion Level']
    
    # Load model and encoders
    model = joblib.load(model_path)
    encoders = joblib.load(encoders_path)
    
    # Predict
    y_pred = model.predict(X)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_true, y_pred)
    
    # Map encoded targets back to original labels for a readable report
    target_names = encoders['target'].classes_
    
    # Print results
    print(f"Overall Model Accuracy: {accuracy * 100:.2f}%\n")
    print("Classification Report:")
    print(classification_report(y_true, y_pred, target_names=target_names))
else:
    print("Required files not found.")
