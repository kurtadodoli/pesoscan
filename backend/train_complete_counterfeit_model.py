#!/usr/bin/env python3
"""
🚀 COMPLETE COUNTERFEIT DETECTION MODEL TRAINING
🎯 Train the entire YOLOv8 model from scratch using Roboflow dataset
📊 Full training with validation, monitoring, and model optimization
"""

import os
import yaml
import time
import shutil
from pathlib import Path
from ultralytics import YOLO
import torch
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CounterfeitModelTrainer:
    def __init__(self):
        self.dataset_path = "Counterfeit-Money-Detector-v5"
        self.output_dir = "complete_counterfeit_training"
        self.model_size = "yolov8n"  # Start with nano for faster training, can upgrade to 's', 'm', 'l', 'x'
        
    def setup_training_environment(self):
        """Setup the training environment and directories"""
        logger.info("🔧 Setting up training environment...")
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Check dataset exists
        if not os.path.exists(self.dataset_path):
            logger.error(f"❌ Dataset not found at {self.dataset_path}")
            return False
            
        # Check data.yaml exists
        data_yaml_path = os.path.join(self.dataset_path, "data.yaml")
        if not os.path.exists(data_yaml_path):
            logger.error(f"❌ data.yaml not found at {data_yaml_path}")
            return False
            
        logger.info(f"✅ Dataset found: {self.dataset_path}")
        logger.info(f"✅ Training output: {self.output_dir}")
        
        return True
    
    def verify_dataset(self):
        """Verify the dataset structure and classes"""
        logger.info("🔍 Verifying dataset structure...")
        
        data_yaml_path = os.path.join(self.dataset_path, "data.yaml")
        
        with open(data_yaml_path, 'r') as f:
            data_config = yaml.safe_load(f)
        
        logger.info(f"📊 Dataset configuration:")
        logger.info(f"   - Classes: {data_config.get('nc', 'Unknown')}")
        logger.info(f"   - Names: {len(data_config.get('names', []))} classes")
        
        # Check directories
        for split in ['train', 'valid', 'test']:
            split_dir = os.path.join(self.dataset_path, split)
            if os.path.exists(split_dir):
                images_dir = os.path.join(split_dir, 'images')
                labels_dir = os.path.join(split_dir, 'labels')
                
                if os.path.exists(images_dir):
                    image_count = len([f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.jpeg', '.png'))])
                    logger.info(f"   - {split}: {image_count} images")
                    
                if os.path.exists(labels_dir):
                    label_count = len([f for f in os.listdir(labels_dir) if f.endswith('.txt')])
                    logger.info(f"   - {split}: {label_count} labels")
        
        return data_config
    
    def train_model(self, epochs=100, imgsz=640, batch_size=16):
        """Train the complete counterfeit detection model"""
        logger.info("🚀 Starting complete model training...")
        logger.info(f"📋 Training parameters:")
        logger.info(f"   - Model: {self.model_size}")
        logger.info(f"   - Epochs: {epochs}")
        logger.info(f"   - Image size: {imgsz}")
        logger.info(f"   - Batch size: {batch_size}")
        
        try:
            # Load a pre-trained YOLOv8 model
            model = YOLO(f'{self.model_size}.pt')
            logger.info(f"✅ Loaded pre-trained {self.model_size} model")
            
            # Prepare data path
            data_yaml_path = os.path.join(self.dataset_path, "data.yaml")
            
            # Configure training parameters
            training_args = {
                'data': data_yaml_path,
                'epochs': epochs,
                'imgsz': imgsz,
                'batch': batch_size,
                'name': 'counterfeit_detection_complete',
                'project': self.output_dir,
                'save': True,
                'save_period': 10,  # Save every 10 epochs
                'cache': False,  # Don't cache images to save memory
                'device': 'cpu',  # Use CPU for compatibility, can change to 'cuda' if GPU available
                'workers': 4,
                'patience': 50,  # Early stopping patience
                'optimizer': 'AdamW',
                'lr0': 0.01,
                'lrf': 0.1,
                'momentum': 0.937,
                'weight_decay': 0.0005,
                'warmup_epochs': 3,
                'warmup_momentum': 0.8,
                'warmup_bias_lr': 0.1,
                'box': 7.5,
                'cls': 0.5,
                'dfl': 1.5,
                'pose': 12.0,
                'kobj': 1.0,
                'label_smoothing': 0.0,
                'nbs': 64,
                'hsv_h': 0.015,
                'hsv_s': 0.7,
                'hsv_v': 0.4,
                'degrees': 0.0,
                'translate': 0.1,
                'scale': 0.5,
                'shear': 0.0,
                'perspective': 0.0,
                'flipud': 0.0,
                'fliplr': 0.5,
                'mosaic': 1.0,
                'mixup': 0.0,
                'copy_paste': 0.0,
                'val': True,
                'plots': True,
                'verbose': True
            }
            
            logger.info("🏋️ Starting training process...")
            start_time = time.time()
            
            # Train the model
            results = model.train(**training_args)
            
            training_time = time.time() - start_time
            logger.info(f"✅ Training completed in {training_time/60:.1f} minutes")
            
            # Get the path to the best model
            best_model_path = os.path.join(self.output_dir, 'counterfeit_detection_complete', 'weights', 'best.pt')
            last_model_path = os.path.join(self.output_dir, 'counterfeit_detection_complete', 'weights', 'last.pt')
            
            if os.path.exists(best_model_path):
                logger.info(f"✅ Best model saved: {best_model_path}")
                
                # Copy to main directory for easy access
                main_model_path = "counterfeit_detection_complete_best.pt"
                shutil.copy2(best_model_path, main_model_path)
                logger.info(f"✅ Model copied to: {main_model_path}")
                
            if os.path.exists(last_model_path):
                logger.info(f"✅ Last model saved: {last_model_path}")
            
            return results, best_model_path
            
        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            return None, None
    
    def validate_model(self, model_path):
        """Validate the trained model"""
        logger.info("🧪 Validating trained model...")
        
        try:
            # Load the trained model
            model = YOLO(model_path)
            
            # Run validation
            data_yaml_path = os.path.join(self.dataset_path, "data.yaml")
            results = model.val(data=data_yaml_path)
            
            logger.info("📊 Validation Results:")
            if hasattr(results, 'box'):
                logger.info(f"   - mAP50: {results.box.map50:.3f}")
                logger.info(f"   - mAP50-95: {results.box.map:.3f}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Validation failed: {e}")
            return None
    
    def test_model_inference(self, model_path):
        """Test the model with sample images"""
        logger.info("🎯 Testing model inference...")
        
        try:
            model = YOLO(model_path)
            
            # Find test images
            test_images_dir = os.path.join(self.dataset_path, "test", "images")
            if not os.path.exists(test_images_dir):
                test_images_dir = os.path.join(self.dataset_path, "valid", "images")
            
            if os.path.exists(test_images_dir):
                test_images = [f for f in os.listdir(test_images_dir) 
                             if f.endswith(('.jpg', '.jpeg', '.png'))][:5]  # Test with 5 images
                
                logger.info(f"🖼️ Testing with {len(test_images)} sample images...")
                
                for img_file in test_images:
                    img_path = os.path.join(test_images_dir, img_file)
                    
                    # Run inference
                    results = model(img_path, verbose=False)
                    
                    if results and len(results) > 0:
                        detections = len(results[0].boxes) if results[0].boxes is not None else 0
                        logger.info(f"   - {img_file}: {detections} detections")
                    else:
                        logger.info(f"   - {img_file}: No detections")
                
                logger.info("✅ Model inference test completed")
                return True
            else:
                logger.warning("⚠️ No test images found")
                return False
                
        except Exception as e:
            logger.error(f"❌ Inference test failed: {e}")
            return False

def main():
    """Main training function"""
    print("=" * 80)
    print("🚀 COMPLETE COUNTERFEIT DETECTION MODEL TRAINING")
    print("🎯 Training YOLOv8 from scratch with Roboflow dataset")
    print("=" * 80)
    
    trainer = CounterfeitModelTrainer()
    
    # Setup environment
    if not trainer.setup_training_environment():
        print("❌ Environment setup failed")
        return
    
    # Verify dataset
    data_config = trainer.verify_dataset()
    if not data_config:
        print("❌ Dataset verification failed")
        return
    
    print(f"\n📊 Dataset Summary:")
    print(f"   - Total classes: {data_config.get('nc', 'Unknown')}")
    print(f"   - Class names: {data_config.get('names', [])[:10]}...")  # Show first 10
    
    # Ask user for training parameters
    print(f"\n🏋️ Training Configuration:")
    print(f"   - Model: YOLOv8 nano (fastest training)")
    print(f"   - Epochs: 100 (can adjust based on results)")
    print(f"   - Device: CPU (compatible with all systems)")
    
    # Start training
    results, model_path = trainer.train_model(
        epochs=100,  # Can adjust based on performance
        imgsz=640,
        batch_size=8  # Smaller batch for CPU training
    )
    
    if results and model_path:
        print("\n🎉 TRAINING COMPLETED SUCCESSFULLY!")
        print(f"✅ Best model: {model_path}")
        
        # Validate the model
        validation_results = trainer.validate_model(model_path)
        
        # Test inference
        trainer.test_model_inference(model_path)
        
        print("\n🌟 COMPLETE COUNTERFEIT DETECTION MODEL READY!")
        print("📁 Model files:")
        print(f"   - Best: counterfeit_detection_complete_best.pt")
        print(f"   - Training folder: {trainer.output_dir}")
        
    else:
        print("❌ Training failed")

if __name__ == "__main__":
    main()