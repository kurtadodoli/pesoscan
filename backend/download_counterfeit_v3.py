#!/usr/bin/env python3
"""
Download Counterfeit Money Detection Dataset using Roboflow API - New Version
"""
import os
import sys

def install_roboflow():
    """Install roboflow package if not available"""
    try:
        import roboflow
        print("✅ Roboflow already installed")
        return True
    except ImportError:
        print("📦 Installing roboflow package...")
        import subprocess
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "roboflow"])
            print("✅ Roboflow installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install roboflow: {e}")
            return False

def download_counterfeit_dataset():
    """Download the counterfeit money detection dataset"""
    print("🚀 Starting Counterfeit Money Detection Dataset Download")
    print("="*60)
    
    # Set working directory
    os.chdir(r"c:\pesoscan\backend")
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Install roboflow if needed
    if not install_roboflow():
        return False
    
    try:
        from roboflow import Roboflow
        
        # Initialize Roboflow with API key
        print("🔑 Initializing Roboflow with API key...")
        rf = Roboflow(api_key="gZGoQuvlmBgBLq1Ev4Ar")
        
        # Access the project
        print("📂 Accessing project: counterfeit-money-detector")
        project = rf.workspace("aileen-crpev").project("counterfeit-money-detector")
        
        # Get version 5
        print("📋 Getting version 5 of the dataset...")
        version = project.version(5)
        
        # Download dataset in YOLOv8 format
        print("⬇️ Downloading dataset in YOLOv8 format...")
        print("This may take several minutes depending on dataset size...")
        
        dataset = version.download("yolov8")
        
        print(f"✅ Dataset downloaded successfully!")
        print(f"📁 Dataset location: {dataset.location}")
        
        # Check dataset structure
        dataset_path = dataset.location
        if os.path.exists(dataset_path):
            print(f"\n📊 Dataset Structure:")
            print(f"   📁 Dataset path: {dataset_path}")
            
            # Check for train, valid, test folders
            for split in ['train', 'valid', 'test']:
                split_path = os.path.join(dataset_path, split)
                if os.path.exists(split_path):
                    # Count images
                    images_path = os.path.join(split_path, 'images')
                    labels_path = os.path.join(split_path, 'labels')
                    
                    if os.path.exists(images_path):
                        image_count = len([f for f in os.listdir(images_path) if f.endswith(('.jpg', '.jpeg', '.png'))])
                        print(f"   📸 {split} images: {image_count}")
                    
                    if os.path.exists(labels_path):
                        label_count = len([f for f in os.listdir(labels_path) if f.endswith('.txt')])
                        print(f"   🏷️ {split} labels: {label_count}")
            
            # Check data.yaml
            data_yaml_path = os.path.join(dataset_path, 'data.yaml')
            if os.path.exists(data_yaml_path):
                print(f"\n📋 Data configuration found: data.yaml")
                try:
                    with open(data_yaml_path, 'r') as f:
                        content = f.read()
                        print("📄 Data.yaml content:")
                        print(content)
                except Exception as e:
                    print(f"⚠️ Could not read data.yaml: {e}")
            else:
                print("⚠️ data.yaml not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Download failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = download_counterfeit_dataset()
    if success:
        print("\n🎉 SUCCESS! Counterfeit dataset downloaded and ready for training!")
    else:
        print("\n❌ FAILED! Dataset download encountered errors.")
    sys.exit(0 if success else 1)