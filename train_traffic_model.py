import pandas as pd
import numpy as np
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

def train_pipeline(data_path="data/processed_traffic_data.csv", target_col="Congestion Level"):
    """
    Machine Learning Training Pipeline for Traffic Congestion Prediction.
    Trains a Random Forest model, evaluates it, and saves the trained model.
    """
    print("--- Starting Machine Learning Training Pipeline ---")
    
    # 1. Load the preprocessed dataset
    if not os.path.exists(data_path):
        print(f"Error: Processed dataset not found at '{data_path}'.")
        print("Please ensure the preprocessing step has been completed.")
        return
        
    df = pd.read_csv(data_path)
    
    # Ensure target column exists
    if target_col not in df.columns:
        print(f"Error: Target column '{target_col}' not found in the dataset.")
        return
        
    print(f"Successfully loaded dataset with {len(df)} records.")
    
    # Separate features (X) and target (y)
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # 2. Split dataset into training and testing sets (80% train, 20% test)
    print("\nSplitting dataset into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Testing set: {X_test.shape[0]} samples")
    
    # 3. Initialize and train the RandomForestClassifier
    print("\nTraining RandomForestClassifier...")
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    
    # Generate predictions on the test set
    y_pred = rf_model.predict(X_test)
    
    # 4. Show accuracy score
    print("\n--- Model Evaluation ---")
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy Score: {accuracy * 100:.2f}%")
    
    # 5. Show confusion matrix
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    # 6. Show feature importance
    print("\nFeature Importance:")
    importances = rf_model.feature_importances_
    
    # Create a DataFrame to display feature importance cleanly
    feature_importance_df = pd.DataFrame({
        'Feature': X.columns,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    
    print(feature_importance_df.to_string(index=False))
    
    # 7. Save the trained model using joblib
    print("\nSaving the trained model...")
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "traffic_model.pkl")
    joblib.dump(rf_model, model_path)
    print(f"Model successfully saved to '{model_path}'")

if __name__ == "__main__":
    # Execute the training pipeline
    # Note: Assumes feature data is stored in 'data/processed_traffic_data.csv' 
    # and the target column is 'Congestion Level'
    train_pipeline(data_path="data/processed_traffic_data.csv", target_col="Congestion Level")
