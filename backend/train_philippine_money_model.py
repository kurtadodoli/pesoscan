#!/usr/bin/env python3
"""
Train YOLOv8 model with the downloaded Philippine money dataset
"""

import os
import logging
from pathlib import Path
import yaml

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def train_philippine_money_model():
    """Train YOLOv8 model with the Philippine money dataset"""
    logger.info("🤖 Training YOLOv8 with Philippine Money Dataset")
    logger.info("=" * 60)
    
    try:
        # Import ultralytics
        from ultralytics import YOLO
        logger.info("✅ Ultralytics imported successfully")
        
        # Check if dataset exists
        dataset_path = Path("Philippine-Money-1")
        if not dataset_path.exists():
            logger.error(f"❌ Dataset not found at: {dataset_path}")
            return None
            
        data_yaml_path = dataset_path / "data.yaml"
        if not data_yaml_path.exists():
            logger.error(f"❌ data.yaml not found at: {data_yaml_path}")
            return None
            
        logger.info(f"📁 Dataset found at: {dataset_path}")
        
        # Read and update data.yaml to use absolute paths
        with open(data_yaml_path, 'r') as f:
            data_config = yaml.safe_load(f)
            
        logger.info("📋 Original dataset configuration:")
        logger.info(f"  Classes: {data_config['nc']}")
        logger.info(f"  Names: {data_config['names']}")
        
        # Update paths to be absolute
        base_path = dataset_path.absolute()
        data_config['train'] = str(base_path / "train" / "images")
        data_config['val'] = str(base_path / "valid" / "images") 
        data_config['test'] = str(base_path / "test" / "images")
        
        # Save updated data.yaml
        updated_yaml_path = "philippine_money_data.yaml"
        with open(updated_yaml_path, 'w') as f:
            yaml.dump(data_config, f)
            
        logger.info(f"✅ Updated data.yaml saved as: {updated_yaml_path}")
        
        # Initialize YOLOv8 model
        logger.info("🚀 Initializing YOLOv8 model...")
        model = YOLO('yolov8n.pt')  # Start with pre-trained weights
        
        # Create output directory
        output_dir = Path("trained_models")
        output_dir.mkdir(exist_ok=True)
        
        # Train the model
        logger.info("🏋️ Starting training...")
        logger.info("Note: This will take some time depending on your hardware")
        
        results = model.train(
            data=updated_yaml_path,
            epochs=50,  # Adjust based on your needs
            imgsz=640,
            batch=8,    # Adjust based on your GPU memory
            name="philippine_money",
            project=str(output_dir),
            save=True,
            verbose=True
        )
        
        logger.info("✅ Training completed!")
        
        # Check for trained model
        trained_model_path = output_dir / "philippine_money" / "weights" / "best.pt"
        if trained_model_path.exists():
            logger.info(f"🎯 Best model saved at: {trained_model_path}")
            
            # Copy to main models directory
            models_dir = Path("models")
            models_dir.mkdir(exist_ok=True)
            
            import shutil
            final_model_path = models_dir / "philippine_money_best.pt"
            shutil.copy2(trained_model_path, final_model_path)
            logger.info(f"📦 Model copied to: {final_model_path}")
            
            return final_model_path
        else:
            logger.warning("⚠️ Trained model not found in expected location")
            return None
            
    except ImportError as e:
        logger.error(f"❌ Failed to import ultralytics: {e}")
        logger.error("Please install ultralytics: pip install ultralytics")
        return None
        
    except Exception as e:
        logger.error(f"❌ Error during training: {e}")
        return None

def validate_model(model_path):
    """Validate the trained model"""
    try:
        from ultralytics import YOLO
        
        logger.info("🔍 Validating trained model...")
        model = YOLO(str(model_path))
        
        # Run validation
        results = model.val(data="philippine_money_data.yaml")
        
        logger.info("✅ Model validation completed")
        logger.info(f"📊 mAP50: {results.box.map50:.3f}")
        logger.info(f"📊 mAP50-95: {results.box.map:.3f}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error validating model: {e}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Starting YOLOv8 training with Philippine money dataset...")
    
    # Train the model
    model_path = train_philippine_money_model()
    
    if model_path:
        logger.info(f"\n🎉 Training completed successfully!")
        logger.info(f"📍 Model saved to: {model_path}")
        
        # Validate the model
        validation_success = validate_model(model_path)
        
        if validation_success:
            logger.info("\n📋 Next steps:")
            logger.info("1. Update detection service to use the trained model")
            logger.info("2. Test the model with real Philippine peso images")
            logger.info("3. Integrate with the web application")
        else:
            logger.warning("⚠️ Model validation failed, but training completed")
            
    else:
        logger.error("\n❌ Training failed!")
        logger.error("Please check the error messages above")