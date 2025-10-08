#!/usr/bin/env python3
"""
Simple and Robust Counterfeit Detection Model Training
"""

import os
import sys
import torch
from pathlib import Path
from ultralytics import YOLO
import time
from datetime import datetime


def main():
    print("=" * 60)
    print("🎯 Training Counterfeit Detection Model")
    print("=" * 60)
    
    # Check device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🔧 Using device: {device}")
    
    # Set working directory to the dataset directory
    dataset_dir = Path("Counterfeit-Money-Detector-v5")
    if not dataset_dir.exists():
        print("❌ Dataset directory not found!")
        sys.exit(1)
    
    # Change to dataset directory
    os.chdir(dataset_dir)
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Verify data.yaml exists
    data_yaml = Path("data.yaml")
    if not data_yaml.exists():
        print("❌ data.yaml not found!")
        sys.exit(1)
    
    print("✓ Dataset structure validated")
    
    try:
        # Load YOLOv8 model
        print("🚀 Loading YOLOv8 model...")
        model = YOLO('yolov8n.pt')
        
        # Create training directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = f"../counterfeit_detection_runs/train_{timestamp}"
        
        # Training parameters
        params = {
            'data': 'data.yaml',
            'epochs': 30,  # Reduced for faster training
            'imgsz': 640,
            'batch': 4 if device == "cpu" else 16,
            'device': device,
            'project': project_dir,
            'name': 'counterfeit_model',
            'save': True,
            'patience': 10,
            'verbose': True,
            'plots': True,
        }
        
        print("\n📋 Training Configuration:")
        for key, value in params.items():
            print(f"  {key}: {value}")
        
        print(f"\n🏃‍♂️ Starting training...")
        print("=" * 50)
        
        # Start training
        results = model.train(**params)
        
        print("=" * 50)
        print("✅ Training completed!")
        
        # Get model paths
        best_model = Path(project_dir) / "counterfeit_model" / "weights" / "best.pt"
        
        if best_model.exists():
            # Copy to main backend directory
            import shutil
            target_path = Path("../counterfeit_detection_model.pt")
            shutil.copy2(best_model, target_path)
            print(f"✓ Model saved to: {target_path.absolute()}")
        
        print("\n🎉 Training completed successfully!")
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()