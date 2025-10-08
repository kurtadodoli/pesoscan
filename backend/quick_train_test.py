#!/usr/bin/env python3
"""
Quick CashMate training test with fixed dataset
"""

from ultralytics import YOLO
import os

def quick_train_test():
    """Quick training test with 10 epochs"""
    print("🚀 Quick CashMate Training Test")
    print("=" * 40)
    
    dataset_path = "backend/CASHMATE-PH-BANKNOTES-11/data.yaml"
    
    if not os.path.exists(dataset_path):
        print("❌ Dataset not found!")
        return False
    
    try:
        # Initialize model
        model = YOLO("yolov8n.pt")
        
        # Quick training test
        print("🎯 Starting 10-epoch test training...")
        results = model.train(
            data=dataset_path,
            epochs=10,
            imgsz=640,
            batch=8,
            name="cashmate_test",
            patience=5,
            save=True,
            plots=True
        )
        
        print("✅ Quick training test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False

if __name__ == "__main__":
    success = quick_train_test()
    if success:
        print("🎉 Ready for full training!")
    else:
        print("❌ Fix issues before full training")