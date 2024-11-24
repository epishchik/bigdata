from sklearn.datasets import fetch_california_housing
import pandas as pd

def save_california_housing_as_csv(output_file="california_housing.csv"):
    # Fetch the California Housing dataset
    data = fetch_california_housing(as_frame=True)
    
    # Get features and target
    features = data.data
    target = data.target
    
    # Combine features and target into a single DataFrame
    housing_data = features.copy()
    housing_data["MedHouseValue"] = target  # Add the target as a column
    
    # Save to CSV
    housing_data.to_csv(output_file, index=False)
    print(f"California housing dataset saved as '{output_file}'.")

if __name__ == "__main__":
    save_california_housing_as_csv()