#!/usr/bin/env python3
"""
YOLOv8 Training Script for Philippine Money Detection
"""

import os
import sys
from pathlib import Path

def train_yolo_model():
    """Train YOLOv8 model on Philippine money dataset"""
    
    print("🚀 Starting YOLOv8 training for Philippine Money Detection")
    print("=" * 60)
    
    try:
        # Try to import ultralytics
        from ultralytics import YOLO
        
        # Load pre-trained YOLOv8 model
        print("📥 Loading pre-trained YOLOv8n model...")
        model = YOLO('yolov8n.pt')
        
        # Check if dataset config exists
        data_yaml = Path("trained_models/philippine_money_data.yaml")
        if not data_yaml.exists():
            print("❌ Dataset configuration not found!")
            print(f"Expected: {data_yaml}")
            print("Please run download_dataset.py first.")
            return False
        
        print(f"✅ Found dataset configuration: {data_yaml}")
        
        # Training parameters
        epochs = 100
        batch_size = 16
        img_size = 640
        
        print("\n📋 Training Configuration:")
        print(f"  - Model: YOLOv8n")
        print(f"  - Epochs: {epochs}")
        print(f"  - Batch Size: {batch_size}")
        print(f"  - Image Size: {img_size}")
        print(f"  - Dataset: {data_yaml}")
        
        # Start training
        print("\n🎯 Starting training...")
        results = model.train(
            data=str(data_yaml),
            epochs=epochs,
            batch=batch_size,
            imgsz=img_size,
            save=True,
            project="trained_models",
            name="philippine_money_detection",
            verbose=True
        )
        
        # Save the best model
        best_model_path = Path("trained_models/philippine_money_detection/weights/best.pt")
        if best_model_path.exists():
            import shutil
            shutil.copy2(best_model_path, "trained_models/philippine_money_best.pt")
            print(f"✅ Best model saved to: trained_models/philippine_money_best.pt")
        
        # Validate the model
        print("\n📊 Validating model...")
        validation_results = model.val()
        
        print("\n🎉 Training completed successfully!")
        print(f"📈 Model performance:")
        if hasattr(validation_results, 'box'):
            print(f"  - mAP50: {validation_results.box.map50:.3f}")
            print(f"  - mAP50-95: {validation_results.box.map:.3f}")
        
        return True
        
    except ImportError:
        print("❌ Ultralytics not installed!")
        print("Please install with: pip install ultralytics")
        return False
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False

def test_model():
    """Test the trained model with sample images"""
    
    print("\n🔍 Testing trained model...")
    
    try:
        from ultralytics import YOLO
        
        # Load trained model
        model_path = Path("trained_models/philippine_money_best.pt")
        if not model_path.exists():
            print("❌ Trained model not found!")
            return False
        
        model = YOLO(str(model_path))
        
        # Test with sample images (if available)
        test_images_dir = Path("datasets/philippine-money-hjn3v-1/test/images")
        if test_images_dir.exists():
            test_images = list(test_images_dir.glob("*.jpg")) + list(test_images_dir.glob("*.png"))
            
            if test_images:
                print(f"🖼️ Found {len(test_images)} test images")
                
                # Run inference on test images
                results = model(test_images[:5])  # Test first 5 images
                
                for i, result in enumerate(results):
                    print(f"  - Image {i+1}: {len(result.boxes) if result.boxes else 0} detections")
                
                print("✅ Model testing completed!")
            else:
                print("⚠️ No test images found")
        else:
            print("⚠️ Test directory not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Testing failed: {e}")
        return False

def create_demo_images():
    """Create demo Philippine peso bill images for testing"""
    
    print("\n🖼️ Creating demo images for testing...")
    
    try:
        import cv2
        import numpy as np
        
        # Create demo images directory
        demo_dir = Path("demo_images")
        demo_dir.mkdir(exist_ok=True)
        
        # Create simple demo images (colored rectangles representing bills)
        denominations = [20, 50, 100, 200, 500, 1000]
        colors = [
            (255, 0, 0),    # Blue for 20
            (0, 255, 0),    # Green for 50
            (0, 0, 255),    # Red for 100
            (255, 255, 0),  # Cyan for 200
            (255, 0, 255),  # Magenta for 500
            (0, 255, 255),  # Yellow for 1000
        ]
        
        for i, (denom, color) in enumerate(zip(denominations, colors)):
            # Create blank image
            img = np.ones((400, 600, 3), dtype=np.uint8) * 240  # Light gray background
            
            # Draw bill rectangle
            cv2.rectangle(img, (50, 100), (550, 300), color, -1)
            cv2.rectangle(img, (50, 100), (550, 300), (0, 0, 0), 3)
            
            # Add text
            cv2.putText(img, f"{denom} PESO", (200, 220), cv2.FONT_HERSHEY_SIMPLEX, 
                       2, (255, 255, 255), 3)
            cv2.putText(img, "DEMO BILL", (180, 260), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (255, 255, 255), 2)
            
            # Save image
            filename = demo_dir / f"demo_peso_{denom}.jpg"
            cv2.imwrite(str(filename), img)
            print(f"  ✅ Created: {filename}")
        
        print(f"📁 Demo images saved to: {demo_dir}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create demo images: {e}")
        return False

def main():
    """Main function"""
    
    print("🏦 Philippine Money YOLOv8 Training System")
    print("=" * 50)
    
    # Change to backend directory
    os.chdir(Path(__file__).parent)
    
    # Create demo images first
    create_demo_images()
    
    # Check if we should train or just show instructions
    try:
        from ultralytics import YOLO
        
        # Train the model
        success = train_yolo_model()
        
        if success:
            # Test the model
            test_model()
        
    except ImportError:
        print("\n⚠️ ULTRALYTICS NOT INSTALLED")
        print("=" * 40)
        print("To train the actual YOLOv8 model:")
        print("1. Install ultralytics: pip install ultralytics")
        print("2. Download real Philippine peso bill images")
        print("3. Label the images with bounding boxes")
        print("4. Update the dataset configuration")
        print("5. Run this training script")
        print("\nFor now, the system will use simulated detection.")
    
    print("\n📋 Next Steps:")
    print("1. Collect real Philippine peso bill images")
    print("2. Use Roboflow or other tools to label the data")
    print("3. Train the YOLOv8 model with actual data")
    print("4. Replace simulated detection with trained model")

if __name__ == "__main__":
    main()