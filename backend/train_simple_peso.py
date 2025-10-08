#!/usr/bin/env python3
"""
Simple YOLOv8 training script for Philippine Money dataset
"""

def train_simple():
    """Simple training approach"""
    try:
        from ultralytics import YOLO
        print("🚀 Starting simplified YOLOv8 training...")
        
        # Load YOLOv8n model
        model = YOLO("yolov8n.pt")
        
        # Train with minimal settings
        results = model.train(
            data="philippine_money_corrected.yaml",
            epochs=20,  # Reduced epochs
            imgsz=416,  # Smaller image size
            batch=8,    # Smaller batch
            device='cpu',
            workers=2,  # Fewer workers
            project="runs/detect",
            name="peso_simple",
            exist_ok=True,
            patience=10,
            amp=False,  # Disable mixed precision
            plots=False,  # Disable plots
            verbose=False  # Less verbose
        )
        
        print("✅ Training completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    train_simple()