#!/usr/bin/env python3
"""
Quick train YOLOv8 model for demonstration (reduced epochs)
"""

import logging
from pathlib import Path
import yaml

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def quick_train_demo():
    """Quick training for demo with reduced epochs"""
    logger.info("🚀 Quick Training Demo - Philippine Money YOLOv8")
    logger.info("=" * 50)
    
    try:
        from ultralytics import YOLO
        
        # Check for existing model first
        existing_models = [
            Path("models/philippine_money_best.pt"),
            Path("trained_models/philippine_money/weights/best.pt")
        ]
        
        for model_path in existing_models:
            if model_path.exists():
                logger.info(f"✅ Found existing trained model: {model_path}")
                return model_path
        
        # If no existing model, do quick training
        logger.info("🏋️ Starting quick training (10 epochs for demo)...")
        
        # Initialize model
        model = YOLO('yolov8n.pt')
        
        # Create output directory
        output_dir = Path("models")
        output_dir.mkdir(exist_ok=True)
        
        # Quick training with reduced parameters
        results = model.train(
            data="philippine_money_data.yaml",
            epochs=10,  # Reduced for quick demo
            imgsz=416,  # Smaller image size for speed
            batch=4,    # Smaller batch for memory
            name="philippine_money_quick",
            project=str(output_dir),
            save=True,
            verbose=False,  # Less verbose output
            patience=5
        )
        
        # Check for trained model
        trained_model_path = output_dir / "philippine_money_quick" / "weights" / "best.pt"
        if trained_model_path.exists():
            # Copy to expected location
            final_path = output_dir / "philippine_money_best.pt"
            import shutil
            shutil.copy2(trained_model_path, final_path)
            logger.info(f"✅ Quick training completed: {final_path}")
            return final_path
        else:
            logger.warning("⚠️ Training completed but model not found")
            return None
            
    except Exception as e:
        logger.error(f"❌ Training failed: {e}")
        return None

if __name__ == "__main__":
    result = quick_train_demo()
    if result:
        logger.info(f"🎉 Demo model ready: {result}")
    else:
        logger.info("⚠️ Using pre-trained model for demo")