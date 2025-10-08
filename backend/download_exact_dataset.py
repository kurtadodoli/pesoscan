"""
Download the exact Roboflow dataset specified by the user
"""

from roboflow import Roboflow
import os
import sys

def download_philippine_money_dataset():
    """Download the specific Philippine money dataset from Roboflow"""
    
    print("Downloading Philippine Money dataset from Roboflow...")
    
    try:
        # Initialize Roboflow with the provided API key
        rf = Roboflow(api_key="gZGoQuvlmBgBLq1Ev4Ar")
        
        # Access the specific project
        project = rf.workspace("philippine-money-jczbl").project("philippine-money-hjn3v")
        
        # Get version 1 of the dataset
        version = project.version(1)
        
        # Download in YOLOv8 format
        print("Downloading dataset in YOLOv8 format...")
        dataset = version.download("yolov8")
        
        print(f"Dataset downloaded successfully!")
        print(f"Dataset location: {dataset.location}")
        
        # List the contents to understand the structure
        dataset_path = dataset.location
        print(f"\nDataset structure:")
        for root, dirs, files in os.walk(dataset_path):
            level = root.replace(dataset_path, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # Show first 5 files
                print(f"{subindent}{file}")
            if len(files) > 5:
                print(f"{subindent}... and {len(files)-5} more files")
        
        # Check if data.yaml exists and show its content
        data_yaml_path = os.path.join(dataset_path, "data.yaml")
        if os.path.exists(data_yaml_path):
            print(f"\ndata.yaml content:")
            with open(data_yaml_path, 'r') as f:
                print(f.read())
        
        return dataset_path
        
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        return None

if __name__ == "__main__":
    dataset_path = download_philippine_money_dataset()
    if dataset_path:
        print(f"\n✅ Success! Dataset downloaded to: {dataset_path}")
    else:
        print("❌ Failed to download dataset")