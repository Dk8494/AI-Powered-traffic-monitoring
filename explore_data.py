import pandas as pd
import os

def explore_dataset(file_path):
    print(f"--- Loading Dataset: {file_path} ---")
    
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        print("Please ensure the Excel file is placed in the correct location.")
        return
        
    try:
        # Load the dataset
        df = pd.read_excel(file_path)
        
        # 1. Print dataset shape
        print("\n=== 1. Dataset Shape ===")
        print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
        
        # 2. Print column names
        print("\n=== 2. Column Names ===")
        print(df.columns.tolist())
        
        # 3. Show first 5 rows
        print("\n=== 3. First 5 Rows ===")
        print(df.head())
        
        # 4. Detect missing values
        print("\n=== 4. Missing Values ===")
        missing_values = df.isnull().sum()
        print(missing_values[missing_values > 0] if missing_values.sum() > 0 else "No missing values detected.")
        
        # 5. Detect categorical columns
        print("\n=== 5. Categorical Columns ===")
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        print(cat_cols if cat_cols else "None detected.")
        
        # 6. Detect numerical columns
        print("\n=== 6. Numerical Columns ===")
        num_cols = df.select_dtypes(include=['int64', 'float64', 'int32', 'float32']).columns.tolist()
        print(num_cols if num_cols else "None detected.")
        
        # 7. Create a summary report
        print("\n=== 7. Summary Report ===")
        # Using include='all' gives a summary for both numerical and categorical columns
        print(df.describe(include='all').to_string())
        
    except Exception as e:
        print(f"An error occurred while analyzing the dataset: {e}")

if __name__ == "__main__":
    # Ensure you have 'openpyxl' installed to read .xlsx files (pip install openpyxl)
    file_location = os.path.join("data", "TrafficCongestion_MultiLocation_7000Rows.xlsx")
    explore_dataset(file_location)
