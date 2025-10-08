#!/usr/bin/env python3
"""
Complete Philippine Money Detection Training
Train YOLOv8 model on the full Philippine Money dataset
"""

import os
import sys
import time
import shutil
from pathlib import Path
from ultralytics import YOLO

def train_complete_philippine_money():
    """Train complete Philippine Money detection model"""
    print("=" * 70)
    print("🏦 COMPLETE PHILIPPINE MONEY DETECTION TRAINING")
    print("📊 Training on full dataset: 4,089 training + 1,167 validation images")
    print("🎯 Target: 9 Philippine peso denominations")
    print("=" * 70)
    
    # Check dataset availability
    data_yaml = Path("philippine_money_corrected.yaml")
    if not data_yaml.exists():
        print("❌ Dataset configuration not found!")
        return False
    
    dataset_dir = Path("Philippine-Money-1")
    if not dataset_dir.exists():
        print("❌ Philippine Money dataset not found!")
        return False
    
    print(f"✅ Dataset found: {dataset_dir}")
    print(f"✅ Configuration: {data_yaml}")
    
    try:
        # Load YOLOv8 model (using small version for better accuracy)
        print("\n🤖 Loading YOLOv8 Small model for better accuracy...")
        model = YOLO("yolov8s.pt")  # Small version instead of nano
        
        # Training configuration
        training_params = {
            'data': str(data_yaml),
            'epochs': 100,  # Full training epochs
            'imgsz': 640,   # Full resolution
            'batch': 8,     # Moderate batch size for CPU
            'device': 'cpu',
            'workers': 4,   # More workers for faster data loading
            'project': 'runs/detect',
            'name': 'philippine_money_complete_training',
            'exist_ok': True,
            'patience': 20,  # Early stopping patience
            'save': True,
            'plots': True,
            'verbose': True,
            'cache': False,  # Don't cache to save memory
            'amp': False,    # Disable AMP for CPU
            'optimizer': 'AdamW',
            'lr0': 0.001,    # Learning rate
            'momentum': 0.937,
            'weight_decay': 0.0005,
            'warmup_epochs': 3,
            'cos_lr': True,  # Cosine learning rate scheduler
        }
        
        print("\n📋 Training Configuration:")
        for key, value in training_params.items():
            print(f"   {key}: {value}")
        
        print(f"\n🚀 Starting complete model training...")
        print("⏱️ This will take several hours on CPU...")
        print("💡 Consider using GPU for faster training if available")
        print("=" * 50)
        
        # Start training
        start_time = time.time()
        results = model.train(**training_params)
        training_time = time.time() - start_time
        
        print("=" * 50)
        print(f"⏱️ Training completed in {training_time/3600:.2f} hours!")
        
        # Get paths to trained models
        run_dir = Path("runs/detect/philippine_money_complete_training")
        best_model = run_dir / "weights/best.pt"
        last_model = run_dir / "weights/last.pt"
        
        if best_model.exists():
            # Create trained_models directory if it doesn't exist
            trained_models_dir = Path("trained_models")
            trained_models_dir.mkdir(exist_ok=True)
            
            # Copy models to easily accessible location
            shutil.copy2(best_model, trained_models_dir / "philippine_money_complete_best.pt")
            shutil.copy2(last_model, trained_models_dir / "philippine_money_complete_last.pt")
            
            print(f"✅ Best model saved to: trained_models/philippine_money_complete_best.pt")
            print(f"✅ Last model saved to: trained_models/philippine_money_complete_last.pt")
            
            # Validate the trained model
            print("\n🔍 Validating trained model...")
            model_best = YOLO(str(best_model))
            val_results = model_best.val()
            
            print(f"\n📈 Final Validation Results:")
            print(f"   mAP50: {val_results.box.map50:.3f}")
            print(f"   mAP50-95: {val_results.box.map:.3f}")
            print(f"   Precision: {val_results.box.mp:.3f}")
            print(f"   Recall: {val_results.box.mr:.3f}")
            
            # Test on sample images
            print("\n🧪 Testing on sample images...")
            test_images_dir = Path("Philippine-Money-1/test/images")
            if test_images_dir.exists():
                test_images = list(test_images_dir.glob("*.jpg"))[:5]  # Test on 5 images
                
                for i, img_path in enumerate(test_images, 1):
                    print(f"📸 Testing image {i}: {img_path.name}")
                    results = model_best(str(img_path))
                    
                    for result in results:
                        boxes = result.boxes
                        if boxes is not None and len(boxes) > 0:
                            print(f"   ✅ Detected {len(boxes)} peso bills:")
                            for box in boxes:
                                class_id = int(box.cls[0])
                                confidence = float(box.conf[0])
                                class_name = model_best.names[class_id]
                                print(f"      - {class_name} peso: {confidence:.3f}")
                        else:
                            print(f"   ⚠️ No peso bills detected")
            
            print("\n" + "=" * 70)
            print("🎉 COMPLETE TRAINING SUCCESSFUL!")
            print("✅ Philippine Money detection model fully trained")
            print("✅ Ready for integration into PesoScan website")
            print("✅ Model can detect 9 peso denominations")
            print("=" * 70)
            
            return True
        
        else:
            print("❌ Training failed - no model weights found!")
            return False
    
    except Exception as e:
        print(f"❌ Training failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main training function"""
    print("🚀 Starting complete Philippine Money model training...")
    
    # Change to backend directory
    os.chdir(Path(__file__).parent)
    
    success = train_complete_philippine_money()
    
    if success:
        print("\n🎊 Training pipeline completed successfully!")
        print("\n📋 Next steps:")
        print("1. Update PesoScan detection service to use the new model")
        print("2. Test the model with real peso images")
        print("3. Deploy to production")
    else:
        print("\n❌ Training failed! Check error messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)