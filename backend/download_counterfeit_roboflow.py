#!/usr/bin/env python3
"""
Download Counterfeit Money Detector dataset from Roboflow
"""

import os
import sys
from roboflow import Roboflow


def download_counterfeit_dataset():
    """Download the counterfeit money detection dataset from Roboflow"""
    
    print("Starting download of Counterfeit Money Detector dataset...")
    
    try:
        # Initialize Roboflow with API key
        rf = Roboflow(api_key="gZGoQuvlmBgBLq1Ev4Ar")
        print("✓ Connected to Roboflow successfully")
        
        # Access the project
        project = rf.workspace("aileen-crpev").project("counterfeit-money-detector")
        print("✓ Accessed project: counterfeit-money-detector")
        
        # Get version 5 of the dataset
        version = project.version(5)
        print("✓ Retrieved dataset version 5")
        
        # Set download location to the backend directory
        download_location = os.path.join(os.path.dirname(__file__), "Counterfeit-Money-Detector-v5")
        
        # Download the dataset in YOLOv8 format
        print(f"📥 Downloading dataset to: {download_location}")
        dataset = version.download("yolov8", location=download_location)
        
        print("✅ Dataset download completed successfully!")
        print(f"📁 Dataset location: {download_location}")
        
        # Check if the download was successful
        if os.path.exists(download_location):
            # List the contents
            contents = os.listdir(download_location)
            print(f"📂 Dataset contents: {contents}")
            
            # Check for expected directories
            expected_dirs = ['train', 'valid', 'test']
            for dir_name in expected_dirs:
                dir_path = os.path.join(download_location, dir_name)
                if os.path.exists(dir_path):
                    file_count = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
                    print(f"  ✓ {dir_name}/ directory found with {file_count} files")
                else:
                    print(f"  ⚠️ {dir_name}/ directory not found")
            
            # Check for data.yaml file
            data_yaml_path = os.path.join(download_location, "data.yaml")
            if os.path.exists(data_yaml_path):
                print("  ✓ data.yaml configuration file found")
                # Read and display the data.yaml content
                with open(data_yaml_path, 'r') as f:
                    yaml_content = f.read()
                    print(f"📄 data.yaml content:\n{yaml_content}")
            else:
                print("  ⚠️ data.yaml configuration file not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Counterfeit Money Detector Dataset Download")
    print("=" * 60)
    
    success = download_counterfeit_dataset()
    
    if success:
        print("\n🎉 Download completed successfully!")
        print("You can now use this dataset for training your counterfeit detection model.")
    else:
        print("\n💥 Download failed!")
        sys.exit(1)