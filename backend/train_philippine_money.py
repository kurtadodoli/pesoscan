#!/usr/bin/env python3
"""
Train YOLOv8 model on Philippine Money dataset
"""

from ultralytics import YOLO
import time
from pathlib import Path

def train_philippine_money_model():
    """Train the complete Philippine Money detection model"""
    print("🚀 Starting YOLOv8 training on Philippine Money dataset...")
    print("📊 Dataset: 4,089 training images, 1,167 validation images")  
    print("🎯 Classes: 9 Philippine peso denominations")
    print("=" * 60)
    
    # Load YOLOv8 nano model (pre-trained)
    model = YOLO("yolov8n.pt")
    
    # Start training
    start_time = time.time()
    
    try:
        results = model.train(
            data="philippine_money_corrected.yaml",
            epochs=50,  # Reduced for faster training
            imgsz=640,
            batch=16,
            device='cpu',
            project="runs/detect", 
            name="philippine_money_complete",
            exist_ok=True,
            patience=15,
            save=True,
            plots=True,
            verbose=True
        )
        
        training_time = time.time() - start_time
        print(f"\n⏱️ Training completed in {training_time/3600:.2f} hours")
        
        # Copy the best model to trained_models directory
        best_model = Path("runs/detect/philippine_money_complete/weights/best.pt")
        if best_model.exists():
            import shutil
            trained_models_dir = Path("trained_models")
            trained_models_dir.mkdir(exist_ok=True)
            
            shutil.copy2(best_model, trained_models_dir / "philippine_money_complete_best.pt")
            print(f"✅ Best model saved to: trained_models/philippine_money_complete_best.pt")
            
            # Validate the model
            print("\n🔍 Validating trained model...")
            val_results = model.val()
            print(f"📈 Validation mAP50: {val_results.box.map50:.3f}")
            print(f"📈 Validation mAP50-95: {val_results.box.map:.3f}")
        
        print("\n🎉 Training completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False

if __name__ == "__main__":
    success = train_philippine_money_model()
    if success:
        print("✅ Philippine Money model training complete!")
    else:
        print("❌ Training failed!")