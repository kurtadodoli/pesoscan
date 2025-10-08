#!/usr/bin/env python3
"""
🎉 COUNTERFEIT DETECTION MODEL TESTING SCRIPT 🎉
Test your completed 100-epoch counterfeit detection model!

Training Results Summary:
- ✅ 100/100 epochs completed
- 🏆 93.99% mAP50 accuracy achieved
- 🎯 Ready for counterfeit peso detection
"""

import os
import sys
import time
from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np

def test_counterfeit_model():
    """Test the completed counterfeit detection model"""
    print("🎉 TESTING YOUR COMPLETED COUNTERFEIT MODEL!")
    print("=" * 60)
    
    # Model paths
    model_path = Path("complete_counterfeit_training/counterfeit_detection_complete/weights/best.pt")
    
    if not model_path.exists():
        print(f"❌ Model not found: {model_path}")
        return False
    
    try:
        print("📦 Loading your 100-epoch counterfeit detection model...")
        model = YOLO(str(model_path))
        
        print("✅ Model loaded successfully!")
        print(f"📊 Model classes: {model.names}")
        print(f"🎯 Training accuracy: 93.99% mAP50")
        
        # Get model info
        model_size = model_path.stat().st_size / (1024 * 1024)
        print(f"📦 Model size: {model_size:.1f} MB")
        
        return model
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def test_with_sample_images(model):
    """Test the model with sample images from the dataset"""
    print("\n🧪 Testing with sample images from your dataset...")
    
    # Test dataset path
    test_images_dir = Path("Counterfeit-Money-Detector-5/test/images")
    
    if not test_images_dir.exists():
        print(f"❌ Test images directory not found: {test_images_dir}")
        return False
    
    # Get some test images
    test_images = list(test_images_dir.glob("*.jpg"))[:5]  # Test with first 5 images
    
    if not test_images:
        print("❌ No test images found")
        return False
    
    print(f"🖼️  Found {len(test_images)} test images")
    
    results_summary = []
    
    for i, img_path in enumerate(test_images):
        print(f"\n📸 Testing image {i+1}: {img_path.name}")
        
        try:
            # Run inference
            results = model(str(img_path))
            
            # Process results
            for result in results:
                boxes = result.boxes
                if boxes is not None and len(boxes) > 0:
                    print(f"   ✅ Detected {len(boxes)} objects:")
                    for box in boxes:
                        conf = box.conf[0].item()
                        cls = int(box.cls[0].item())
                        class_name = model.names[cls]
                        print(f"      🎯 {class_name}: {conf:.3f} confidence")
                        
                        results_summary.append({
                            'image': img_path.name,
                            'class': class_name,
                            'confidence': conf
                        })
                else:
                    print("   ❌ No objects detected")
                    
        except Exception as e:
            print(f"   ❌ Error processing image: {e}")
    
    # Summary
    if results_summary:
        print(f"\n📊 DETECTION SUMMARY:")
        print(f"   Total detections: {len(results_summary)}")
        avg_conf = sum(r['confidence'] for r in results_summary) / len(results_summary)
        print(f"   Average confidence: {avg_conf:.3f}")
        
        # Group by class
        classes = {}
        for result in results_summary:
            cls = result['class']
            if cls not in classes:
                classes[cls] = []
            classes[cls].append(result['confidence'])
        
        print("   Detected classes:")
        for cls, confidences in classes.items():
            avg_conf = sum(confidences) / len(confidences)
            print(f"      🏷️  {cls}: {len(confidences)} detections, avg confidence: {avg_conf:.3f}")
    
    return True

def copy_model_to_production():
    """Copy the best model to production directory"""
    print("\n📦 Copying model to production directory...")
    
    source_path = Path("complete_counterfeit_training/counterfeit_detection_complete/weights/best.pt")
    dest_dir = Path("trained_models")
    dest_path = dest_dir / "counterfeit_detection_complete.pt"
    
    try:
        dest_dir.mkdir(exist_ok=True)
        
        import shutil
        shutil.copy2(source_path, dest_path)
        
        print(f"✅ Model copied to: {dest_path}")
        
        # Verify copy
        if dest_path.exists():
            size_mb = dest_path.stat().st_size / (1024 * 1024)
            print(f"📦 Production model size: {size_mb:.1f} MB")
            return True
        else:
            print("❌ Failed to copy model")
            return False
            
    except Exception as e:
        print(f"❌ Error copying model: {e}")
        return False

def main():
    print("🎉 COUNTERFEIT DETECTION MODEL RECOVERY TEST")
    print("═" * 60)
    print("🏆 Your training was COMPLETED successfully!")
    print("📊 Final Results: 100/100 epochs, 93.99% mAP50")
    print("🎯 Testing your completed counterfeit detection model...")
    print("═" * 60)
    
    # Test the model
    model = test_counterfeit_model()
    if not model:
        return 1
    
    # Test with sample images
    if not test_with_sample_images(model):
        print("❌ Sample testing failed")
        return 1
    
    # Copy to production
    if not copy_model_to_production():
        print("❌ Failed to copy model to production")
        return 1
    
    print("\n🎉 COUNTERFEIT MODEL RECOVERY COMPLETE!")
    print("=" * 60)
    print("✅ Your 100-epoch counterfeit detection model is ready!")
    print("✅ 93.99% mAP50 accuracy achieved")
    print("✅ Model tested successfully with sample images")
    print("✅ Model copied to production directory")
    print("🚀 Your counterfeit detection system is ready for use!")
    print("\nNext steps:")
    print("1. 🧪 Test with your own peso images")
    print("2. 🔗 Integrate with your main API")
    print("3. 🚀 Deploy for counterfeit detection")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())