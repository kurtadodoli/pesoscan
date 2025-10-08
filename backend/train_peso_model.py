"""
Train YOLOv8 model specifically for Philippine peso detection using the Roboflow dataset
"""

import os
import yaml
from ultralytics import YOLO
import torch

def train_peso_detection_model():
    """Train YOLOv8 model on the exact Roboflow dataset"""
    
    print("🚀 Training YOLOv8 model on Philippine peso dataset...")
    
    # Check if dataset exists
    dataset_path = "Philippine-Money-1"
    data_yaml = os.path.join(dataset_path, "data.yaml")
    
    if not os.path.exists(data_yaml):
        print("❌ Roboflow dataset not found!")
        return None
    
    # Read the data.yaml configuration
    with open(data_yaml, 'r') as f:
        config = yaml.safe_load(f)
    
    print(f"📊 Dataset info:")
    print(f"  Classes: {config['names']}")
    print(f"  Number of classes: {config['nc']}")
    
    # Update paths to be absolute
    config['train'] = os.path.abspath(os.path.join(dataset_path, "train", "images"))
    config['val'] = os.path.abspath(os.path.join(dataset_path, "valid", "images"))
    config['test'] = os.path.abspath(os.path.join(dataset_path, "test", "images"))
    
    # Save updated config
    updated_yaml = "peso_detection_config.yaml"
    with open(updated_yaml, 'w') as f:
        yaml.dump(config, f)
    
    print(f"💾 Updated config saved to: {updated_yaml}")
    
    try:
        # Initialize YOLOv8 model
        model = YOLO('yolov8n.pt')  # Start with pre-trained model
        
        # Train the model
        print("🏋️ Starting training...")
        results = model.train(
            data=updated_yaml,
            epochs=50,  # Reduced for faster training
            imgsz=640,
            batch=16,
            patience=10,
            save=True,
            project="runs/detect",
            name="peso_detection"
        )
        
        # Save the trained model
        model_save_path = "trained_peso_model.pt"
        model.save(model_save_path)
        print(f"✅ Model saved to: {model_save_path}")
        
        # Validate the model
        print("🧪 Validating model...")
        val_results = model.val()
        
        print(f"📈 Validation results:")
        print(f"  mAP50: {val_results.box.map50:.3f}")
        print(f"  mAP50-95: {val_results.box.map:.3f}")
        
        return model_save_path
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return None

if __name__ == "__main__":
    model_path = train_peso_detection_model()
    if model_path:
        print(f"🎉 Training completed! Model saved at: {model_path}")
    else:
        print("❌ Training failed!")