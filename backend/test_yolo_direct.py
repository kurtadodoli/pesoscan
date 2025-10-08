#!/usr/bin/env python3
"""
Test the YOLOv8 model directly to see all detections
"""

import cv2
import numpy as np
import sys
import os
import glob

# Add the app directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_yolo_directly():
    """Test YOLOv8 model directly to see all raw detections"""
    
    try:
        from ultralytics import YOLO
        
        # Load the excellent model
        model_path = "trained_models/counterfeit_detection_final_best.pt"
        if not os.path.exists(model_path):
            model_path = "../trained_models/counterfeit_detection_final_best.pt"
        
        if not os.path.exists(model_path):
            print("❌ Model not found!")
            return
            
        print(f"🔥 Loading excellent model: {model_path}")
        model = YOLO(model_path)
        
        print(f"📊 Model classes: {len(model.names)} classes")
        for class_id, class_name in model.names.items():
            print(f"  {class_id}: {class_name}")
        
        # Test with real peso images
        test_dirs = [
            "../Philippine-Money-1/test/images",
            "../Philippine-Money-1/valid/images", 
            "../Philippine-Money-1/train/images"
        ]
        
        for test_dir in test_dirs:
            full_path = os.path.join(os.path.dirname(__file__), test_dir)
            if os.path.exists(full_path):
                image_files = glob.glob(os.path.join(full_path, "*.jpg"))[:3]  # Test first 3 images
                
                for img_path in image_files:
                    print(f"\n🖼️  TESTING: {os.path.basename(img_path)}")
                    print("-" * 60)
                    
                    image = cv2.imread(img_path)
                    if image is None:
                        continue
                        
                    # Run inference with lower confidence to see more detections
                    results = model(image, verbose=False, conf=0.10)  # Very low confidence
                    
                    for result in results:
                        if len(result.boxes) > 0:
                            print(f"🎯 FOUND {len(result.boxes)} DETECTIONS!")
                            
                            for i, box in enumerate(result.boxes):
                                confidence = float(box.conf.cpu().numpy()[0])
                                class_id = int(box.cls.cpu().numpy()[0])
                                bbox = box.xywhn.cpu().numpy()[0]  # normalized
                                
                                class_name = model.names.get(class_id, f"class_{class_id}")
                                
                                print(f"  Detection {i+1}:")
                                print(f"    Class ID: {class_id}")
                                print(f"    Class Name: {class_name}")
                                print(f"    Confidence: {confidence:.3f} ({confidence*100:.1f}%)")
                                print(f"    BBox: [{bbox[0]:.3f}, {bbox[1]:.3f}, {bbox[2]:.3f}, {bbox[3]:.3f}]")
                        else:
                            print("❌ No detections found")
                            
                        print()
                break  # Only test from first available directory
                
    except ImportError:
        print("❌ Ultralytics not available")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔍 Testing YOLOv8 Model Directly...")
    test_yolo_directly()