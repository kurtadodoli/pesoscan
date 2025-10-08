#!/usr/bin/env python3
"""
Download and Train Roboflow Counterfeit Money Detector v5
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from ultralytics import YOLO
import torch


def install_roboflow():
    """Install roboflow package if not already installed"""
    try:
        import roboflow
        print("✅ Roboflow already installed")
        return True
    except ImportError:
        print("📦 Installing roboflow package...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "roboflow"])
            print("✅ Roboflow installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install roboflow: {e}")
            return False


def download_roboflow_dataset():
    """Download the specific Roboflow dataset"""
    
    print("🔽 Downloading Roboflow Counterfeit Money Detector v5...")
    
    try:
        from roboflow import Roboflow
        
        # Initialize Roboflow with API key
        rf = Roboflow(api_key="gZGoQuvlmBgBLq1Ev4Ar")
        project = rf.workspace("aileen-crpev").project("counterfeit-money-detector")
        version = project.version(5)
        
        # Download dataset in YOLOv8 format
        dataset = version.download("yolov8")
        
        print(f"✅ Dataset downloaded successfully!")
        print(f"📁 Dataset location: {dataset.location}")
        
        return dataset.location
        
    except Exception as e:
        print(f"❌ Failed to download dataset: {e}")
        return None


def analyze_dataset(dataset_path):
    """Analyze the downloaded dataset structure"""
    
    dataset_path = Path(dataset_path)
    print(f"\n📊 Analyzing dataset: {dataset_path}")
    
    # Check data.yaml
    data_yaml = dataset_path / "data.yaml"
    if data_yaml.exists():
        print(f"✅ Found data.yaml")
        
        with open(data_yaml, 'r') as f:
            content = f.read()
            print("📋 Dataset configuration:")
            print(content[:500] + "..." if len(content) > 500 else content)
    
    # Check splits
    for split in ['train', 'valid', 'test']:
        split_dir = dataset_path / split
        if split_dir.exists():
            images_dir = split_dir / 'images'
            labels_dir = split_dir / 'labels'
            
            if images_dir.exists():
                image_count = len(list(images_dir.glob('*.jpg'))) + len(list(images_dir.glob('*.png')))
                print(f"📸 {split} images: {image_count}")
            
            if labels_dir.exists():
                label_count = len(list(labels_dir.glob('*.txt')))
                print(f"🏷️  {split} labels: {label_count}")
    
    return str(data_yaml)


def create_training_config(data_yaml_path, output_name="roboflow_counterfeit_v5"):
    """Create training configuration"""
    
    config = {
        'data': data_yaml_path,
        'epochs': 20,  # More epochs for better training
        'imgsz': 640,  # Standard YOLO image size
        'batch': 4,    # Reasonable batch size for CPU
        'device': 'cuda' if torch.cuda.is_available() else 'cpu',
        'project': './roboflow_runs',
        'name': output_name,
        'save': True,
        'patience': 10,
        'verbose': True,
        'plots': True,
        'cache': False,  # Disable cache to save memory
        'workers': 2,    # Reduce workers for CPU
    }
    
    return config


def train_roboflow_model(data_yaml_path):
    """Train YOLOv8 model on Roboflow dataset"""
    
    print("\n🚀 Starting training on Roboflow Counterfeit Money Detector v5...")
    print("=" * 70)
    
    # Check device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🔧 Using device: {device}")
    
    if device == "cpu":
        print("⚠️  Training on CPU - this will be slower but should work")
    
    try:
        # Load YOLOv8 model
        print("🤖 Loading YOLOv8 nano model...")
        model = YOLO('yolov8n.pt')
        
        # Get training configuration
        config = create_training_config(data_yaml_path)
        
        print("\n📋 Training Configuration:")
        for key, value in config.items():
            print(f"  {key}: {value}")
        
        print(f"\n🏃‍♂️ Starting training...")
        print("=" * 50)
        
        # Start training
        results = model.train(**config)
        
        print("=" * 50)
        print("✅ Training completed!")
        
        # Get model paths
        best_model = Path(f"./roboflow_runs/{config['name']}/weights/best.pt")
        
        if best_model.exists():
            # Copy to main backend directory with descriptive name
            target_path = Path("./roboflow_counterfeit_v5_model.pt")
            shutil.copy2(best_model, target_path)
            print(f"✓ Trained model saved to: {target_path.absolute()}")
            
            # Test the model
            print("\n🧪 Testing the trained model...")
            test_dataset_path = Path(data_yaml_path).parent
            test_images = list((test_dataset_path / 'test' / 'images').glob('*.jpg'))
            
            if not test_images:
                test_images = list((test_dataset_path / 'valid' / 'images').glob('*.jpg'))
            
            if test_images:
                test_img = test_images[0]
                results = model.predict(
                    source=str(test_img), 
                    save=True, 
                    project="./roboflow_runs", 
                    name="test_predictions"
                )
                print(f"✓ Test prediction completed for: {test_img}")
                
                # Show detection results
                if results and len(results) > 0:
                    result = results[0]
                    if result.boxes is not None and len(result.boxes) > 0:
                        print(f"🎯 Detected {len(result.boxes)} objects in test image")
                        for i, box in enumerate(result.boxes[:3]):  # Show first 3
                            conf = float(box.conf[0])
                            cls = int(box.cls[0])
                            print(f"  Detection {i+1}: Class {cls}, Confidence: {conf:.3f}")
                    else:
                        print("📝 No objects detected in test image")
        
        print("\n🎉 Roboflow training completed successfully!")
        print(f"📊 Model ready for integration into PesoScan!")
        
        return True
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 70)
    print("🚀 Roboflow Counterfeit Money Detector v5 - Download & Train")
    print("=" * 70)
    
    # Install roboflow
    if not install_roboflow():
        print("❌ Cannot proceed without roboflow package")
        return
    
    # Download dataset
    dataset_location = download_roboflow_dataset()
    if not dataset_location:
        print("❌ Failed to download dataset")
        return
    
    # Analyze dataset
    data_yaml_path = analyze_dataset(dataset_location)
    
    # Train model
    success = train_roboflow_model(data_yaml_path)
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 Complete! Roboflow Counterfeit Money Detector v5 trained successfully!")
        print("✅ Model file: roboflow_counterfeit_v5_model.pt")
        print("📁 Training results: ./roboflow_runs/")
        print("🔧 Ready to integrate into PesoScan backend!")
    else:
        print("❌ Training failed. Check the logs above for details.")
    print("=" * 70)


if __name__ == "__main__":
    main()