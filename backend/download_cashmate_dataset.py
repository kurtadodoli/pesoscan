#!/usr/bin/env python3
"""
Download CashMate Philippine Banknotes dataset from Roboflow
"""

import os
import sys
from roboflow import Roboflow

def download_cashmate_dataset():
    """Download the actual CashMate dataset from Roboflow"""
    print("🔄 Downloading CashMate Philippine Banknotes Dataset")
    print("=" * 60)
    
    # Get API key from user
    api_key = input("Enter your Roboflow API key: ").strip()
    
    if not api_key or api_key == "":
        print("❌ API key is required!")
        print("\n📝 To get your API key:")
        print("1. Go to https://roboflow.com")
        print("2. Sign up/Login to your account")
        print("3. Go to Account > Roboflow API")
        print("4. Copy your API key")
        return None
    
    try:
        print(f"🔗 Connecting to Roboflow with API key: {api_key[:8]}...")
        
        # Initialize Roboflow
        rf = Roboflow(api_key=api_key)
        
        # Access the CashMate project
        print("📂 Accessing CashMate Philippine Banknotes project...")
        project = rf.workspace("aarav-s-dhzpy").project("cashmate-philippine-banknotes")
        
        # Get version 11 (latest)
        print("🔢 Getting dataset version 11...")
        version = project.version(11)
        
        # Download in YOLOv8 format
        print("⬇️ Downloading dataset (this may take a few minutes)...")
        dataset = version.download("yolov8")
        
        print(f"✅ Dataset downloaded successfully!")
        print(f"📁 Location: {dataset.location}")
        print(f"📊 Dataset structure:")
        
        # Check dataset structure
        dataset_path = dataset.location
        for root, dirs, files in os.walk(dataset_path):
            level = root.replace(dataset_path, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files[:5]:  # Show first 5 files
                print(f"{subindent}{file}")
            if len(files) > 5:
                print(f"{subindent}... and {len(files) - 5} more files")
        
        return dataset.location
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        print("\n🔍 Troubleshooting:")
        print("1. Check your API key is correct")
        print("2. Ensure you have access to the CashMate project")
        print("3. Check your internet connection")
        return None

def create_training_config(dataset_path):
    """Create training configuration for the downloaded dataset"""
    if not dataset_path:
        return None
    
    config_file = os.path.join(dataset_path, "data.yaml")
    
    if os.path.exists(config_file):
        print(f"✅ Found existing config: {config_file}")
        return config_file
    
    print("📝 Creating training configuration...")
    
    # Read the downloaded data.yaml or create one
    import yaml
    
    config = {
        'path': dataset_path,
        'train': 'train/images',
        'val': 'valid/images', 
        'test': 'test/images',
        'nc': 9,  # Number of classes for Philippine peso
        'names': ['1_peso', '5_peso', '10_peso', '20_peso', '50_peso', 
                 '100_peso', '200_peso', '500_peso', '1000_peso']
    }
    
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print(f"✅ Config created: {config_file}")
    return config_file

def main():
    """Main download function"""
    print("🪙 CashMate Dataset Downloader")
    print("=" * 50)
    
    # Download dataset
    dataset_path = download_cashmate_dataset()
    
    if dataset_path:
        # Create training config
        config_file = create_training_config(dataset_path)
        
        print("\n🎉 Download Complete!")
        print("=" * 30)
        print(f"📁 Dataset: {dataset_path}")
        print(f"⚙️ Config: {config_file}")
        print("\n🚀 Next Steps:")
        print("1. Run training with the downloaded dataset:")
        print(f"   python train_roboflow_cashmate.py")
        print("2. Or use the enhanced training script:")
        print(f"   python train_cashmate_enhanced.py")
        
        # Update training scripts to use the downloaded dataset
        update_training_scripts(dataset_path, config_file)
        
    else:
        print("\n❌ Download failed!")
        print("Please check your API key and try again.")

def update_training_scripts(dataset_path, config_file):
    """Update training scripts to use the downloaded dataset"""
    scripts_to_update = [
        "train_roboflow_cashmate.py",
        "train_cashmate_enhanced.py", 
        "auto_train_cashmate.py"
    ]
    
    print("\n🔧 Updating training scripts...")
    
    for script in scripts_to_update:
        if os.path.exists(script):
            try:
                with open(script, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace dataset path references
                content = content.replace(
                    'data=yaml_path',
                    f'data="{config_file}"'
                )
                content = content.replace(
                    'your_api_key_here',
                    f'# Dataset already downloaded to {dataset_path}'
                )
                
                with open(script, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"   ✅ Updated {script}")
                
            except Exception as e:
                print(f"   ⚠️ Could not update {script}: {e}")

if __name__ == "__main__":
    main()