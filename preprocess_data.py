import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

def preprocess_traffic_data(file_path, target_col='Congestion Level'):
    print(f"Loading data from {file_path}...")
    
    try:
        if file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

    print(f"Initial Dataset Shape: {df.shape}")

    # 1. Remove missing values
    initial_rows = df.shape[0]
    df = df.dropna()
    dropped_rows = initial_rows - df.shape[0]
    print(f"Dropped {dropped_rows} missing values. New Shape: {df.shape}")

    # 2. Separate features and target
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in dataset.")
        
    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Detect categorical and numerical columns
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    numerical_cols = X.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns.tolist()

    os.makedirs('models', exist_ok=True)
    os.makedirs('data', exist_ok=True)

    # 3. Encode categorical columns using LabelEncoder
    encoders = {}
    if categorical_cols:
        for col in categorical_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            encoders[col] = le
        print(f"Encoded categorical features: {categorical_cols}")

    # Encode target variable if it's categorical
    if y.dtype == 'object' or y.dtype.name == 'category':
        target_encoder = LabelEncoder()
        y = target_encoder.fit_transform(y)
        encoders['target'] = target_encoder
        print(f"Encoded target column '{target_col}'. Mapping saved in encoders.")

    # Save LabelEncoders
    if encoders:
        joblib.dump(encoders, 'models/label_encoders.pkl')
        print("Saved LabelEncoders to models/label_encoders.pkl")

    # 4. Scale numerical features
    if numerical_cols:
        scaler = StandardScaler()
        X[numerical_cols] = scaler.fit_transform(X[numerical_cols])
        joblib.dump(scaler, 'models/scaler.pkl')
        print(f"Scaled numerical features: {numerical_cols}")
        print("Saved StandardScaler to models/scaler.pkl")

    # Combine back to save processed version optionally
    processed_df = X.copy()
    processed_df[target_col] = y
    processed_df.to_csv(os.path.join('data', 'processed_traffic_data.csv'), index=False)
    print("Saved fully processed dataset to data/processed_traffic_data.csv")

    # 5. Prepare dataset for machine learning (Split)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Dataset split into Train: {X_train.shape} and Test: {X_test.shape}")
    
    return X_train, X_test, y_train, y_test, encoders

if __name__ == "__main__":
    file_location = os.path.join("data", "TrafficCongestion_MultiLocation_7000Rows.xlsx")
    
    if os.path.exists(file_location):
        result = preprocess_traffic_data(file_location, target_col="Congestion Level")
        if result:
            print("\nPreprocessing pipeline executed successfully. Ready for ML Training!")
    else:
        print(f"Dataset not found at {file_location}.")
        print("Please ensure the file is placed correctly before running preprocessing.")
