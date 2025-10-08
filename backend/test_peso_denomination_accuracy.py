#!/usr/bin/env python3
"""
🎯 ACCURATE 1000 PESO DETECTION TEST
Test the Philippine-Money-1 dataset model for correct denomination detection
"""

import cv2
import numpy as np
import os
import sys
from pathlib import Path
from ultralytics import YOLO

def test_1000_peso_detection():
    """Test accurate 1000 peso bill detection using the correct model"""
    print("🎯 TESTING ACCURATE 1000 PESO DETECTION")
    print("=" * 60)
    
    # Use the Philippine-Money-1 dataset model (NOT the counterfeit model)
    peso_model_path = Path("trained_models/philippine_money_final_best.pt")
    
    if not peso_model_path.exists():
        print(f"❌ Philippine peso model not found: {peso_model_path}")
        return False
    
    try:
        print("📦 Loading Philippine-Money-1 dataset model...")
        model = YOLO(str(peso_model_path))
        
        print(f"✅ Model loaded successfully!")
        print(f"📋 Model classes: {model.names}")
        
        # Test with 1000 peso images from the dataset
        test_image_dir = Path("Philippine-Money-1/test/images")
        if not test_image_dir.exists():
            print(f"❌ Test images not found: {test_image_dir}")
            return False
        
        # Find 1000 peso images in the dataset
        test_images = list(test_image_dir.glob("*.jpg"))
        print(f"📸 Found {len(test_images)} test images")
        
        # Test with first few images
        results_summary = []
        
        for i, img_path in enumerate(test_images[:10]):
            print(f"\n🔍 Testing image {i+1}: {img_path.name}")
            
            try:
                # Run inference
                results = model(str(img_path))
                
                # Process results
                for result in results:
                    boxes = result.boxes
                    if boxes is not None and len(boxes) > 0:
                        for box in boxes:
                            conf = box.conf[0].item()
                            cls = int(box.cls[0].item())
                            
                            # Get class name
                            if cls in model.names:
                                class_name = model.names[cls]
                            else:
                                class_name = f"class_{cls}"
                            
                            print(f"   🎯 Detected: {class_name} (confidence: {conf:.3f})")
                            
                            results_summary.append({
                                'image': img_path.name,
                                'class': class_name,
                                'confidence': conf,
                                'class_id': cls
                            })
                    else:
                        print("   ❌ No detections")
                        
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Summary
        if results_summary:
            print(f"\n📊 DETECTION RESULTS SUMMARY:")
            print(f"   Total detections: {len(results_summary)}")
            
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
            
            # Check for 1000 peso detections
            peso_1000_detections = [r for r in results_summary if r['class'] == '1000']
            if peso_1000_detections:
                print(f"\n🎉 FOUND {len(peso_1000_detections)} 1000 PESO DETECTIONS!")
                for detection in peso_1000_detections:
                    print(f"   ✅ {detection['image']}: confidence {detection['confidence']:.3f}")
            else:
                print(f"\n❌ NO 1000 PESO DETECTIONS FOUND")
                print("   Available classes in results:", list(classes.keys()))
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🏆 PHILIPPINE PESO DENOMINATION ACCURACY TEST")
    print("Testing with the correct Philippine-Money-1 dataset model")
    print("=" * 70)
    
    if not test_1000_peso_detection():
        print("\n❌ Test failed!")
        return 1
    
    print("\n🎉 TEST COMPLETED!")
    print("Check the results above to see if 1000 peso bills are correctly detected")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())