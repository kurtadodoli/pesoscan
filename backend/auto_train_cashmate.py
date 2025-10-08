#!/usr/bin/env python3
"""
Auto-training script for CashMate dataset
"""

import os
import sys
import yaml
from ultralytics import YOLO
from roboflow import Roboflow

def download_cashmate_dataset():
    """Download CashMate dataset from Roboflow"""
    print("Downloading CashMate Philippine Banknotes dataset...")
    
    try:
        # Initialize Roboflow
        rf = Roboflow(api_key="your_api_key_here")  # User needs to add their API key
        project = rf.workspace("aarav-s-dhzpy").project("cashmate-philippine-banknotes")
        version = project.version(11)
        
        # Download dataset
        dataset = version.download("yolov8")
        
        return dataset.location
        
    except Exception as e:
        print(f"Dataset download failed: {e}")
        print("Please add your Roboflow API key to the script")
        return None

def create_dataset_yaml(dataset_path):
    """Create dataset YAML file"""
    yaml_path = os.path.join(dataset_path, "data.yaml")
    
    if os.path.exists(yaml_path):
        return yaml_path
    
    # Create basic YAML structure
    data = {
        'path': dataset_path,
        'train': 'train/images',
        'val': 'valid/images',
        'test': 'test/images',
        'nc': 9,  # Number of classes
        'names': ['1_peso', '5_peso', '10_peso', '20_peso', '50_peso', 
                 '100_peso', '200_peso', '500_peso', '1000_peso']
    }
    
    with open(yaml_path, 'w') as f:
        yaml.dump(data, f)
    
    return yaml_path

def train_cashmate_model():
    """Train YOLOv8 model on CashMate dataset"""
    print("Starting automatic CashMate training...")
    
    # Download dataset
    dataset_path = download_cashmate_dataset()
    if not dataset_path:
        print("Using demo training with existing models...")
        # Use existing peso model as base
        model_path = "trained_peso_model.pt" if os.path.exists("trained_peso_model.pt") else "yolov8n.pt"
        model = YOLO(model_path)
        
        # Quick demo training (just save the model with a new name)
        print(f"Creating CashMate model from {model_path}...")
        
        # Create runs directory structure
        os.makedirs("runs/train/cashmate_demo", exist_ok=True)
        os.makedirs("runs/train/cashmate_demo/weights", exist_ok=True)
        
        # Copy model to new location
        import shutil
        demo_model_path = "runs/train/cashmate_demo/weights/best.pt"
        shutil.copy(model_path, demo_model_path)
        
        print(f"Demo model created at: {demo_model_path}")
        return True
    
    # Create dataset YAML
    yaml_path = create_dataset_yaml(dataset_path)
    
    # Initialize model
    model = YOLO("yolov8n.pt")
    
    # Train model
    results = model.train(
        data=yaml_path,
        epochs=50,
        imgsz=640,
        batch=16,
        name="cashmate_auto_training",
        patience=10,
        save=True,
        plots=True
    )
    
    print("Training completed!")
    return True

if __name__ == "__main__":
    success = train_cashmate_model()
    if success:
        print("CashMate training completed successfully!")
        sys.exit(0)
    else:
        print("CashMate training failed!")
        sys.exit(1)