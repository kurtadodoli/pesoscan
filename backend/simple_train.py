#!/usr/bin/env python3
"""
Simple training script for counterfeit detection model
"""
import os
import sys
from ultralytics import YOLO

def main():
    print("🚀 Starting Counterfeit Detection Model Training")
    print("="*50)
    
    # Set working directory
    os.chdir(r"c:\pesoscan\backend")
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Check if dataset exists
    data_yaml = "Counterfeit-Money-Detector-5/data.yaml"
    if not os.path.exists(data_yaml):
        print(f"❌ Dataset not found: {data_yaml}")
        return False
    
    print(f"✅ Dataset found: {data_yaml}")
    
    try:
        # Initialize model
        print("🔧 Initializing YOLOv8 model...")
        model = YOLO('yolov8n.pt')
        
        # Training parameters
        train_params = {
            'data': data_yaml,
            'epochs': 100,
            'imgsz': 640,
            'batch': 8,
            'patience': 50,
            'save': True,
            'project': 'counterfeit_detection_runs',
            'name': 'counterfeit_yolov8_final',
            'exist_ok': True,
            'cache': False,
            'verbose': True,
            'workers': 2
        }
        
        print("⚙️ Training parameters:")
        for key, value in train_params.items():
            print(f"   {key}: {value}")
        
        print("\n🏋️ Starting training...")
        print("This will take a while (approximately 2-3 hours)")
        
        # Start training
        results = model.train(**train_params)
        
        print("\n🎉 Training completed successfully!")
        print(f"📊 Results: {results}")
        
        # Check if model was saved
        model_path = f"counterfeit_detection_runs/counterfeit_yolov8_final/weights/best.pt"
        if os.path.exists(model_path):
            print(f"✅ Model saved at: {model_path}")
        else:
            print("⚠️ Model file not found after training")
        
        return True
        
    except Exception as e:
        print(f"❌ Training failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 SUCCESS! Counterfeit detection model is ready!")
    else:
        print("\n❌ FAILED! Training encountered errors.")
    sys.exit(0 if success else 1)