#!/usr/bin/env python3
"""
Direct test of the YOLO model to see if it can detect peso features
"""
import sys
import os
sys.path.append(os.getcwd())

def test_yolo_directly():
    """Test YOLO model directly"""
    try:
        from ultralytics import YOLO
        import cv2
        import numpy as np
        
        # Load the trained model
        model_path = r"C:\pesoscan\backend\trained_models\philippine_money_final_best.pt"
        
        if not os.path.exists(model_path):
            print(f"❌ Model not found: {model_path}")
            return
            
        print(f"🏆 Loading model: {model_path}")
        model = YOLO(model_path)
        
        print(f"📋 Model classes: {model.names}")
        print(f"📊 Number of classes: {len(model.names)}")
        
        # Find a test image
        test_images = [
            r"C:\pesoscan\backend\Philippine-Money-1\test\images",
            r"C:\pesoscan\backend\test_images"
        ]
        
        test_image = None
        for test_dir in test_images:
            if os.path.exists(test_dir):
                for file in os.listdir(test_dir)[:5]:  # Check first 5 files
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        test_image = os.path.join(test_dir, file)
                        break
                if test_image:
                    break
        
        if not test_image:
            print("❌ No test image found")
            return
            
        print(f"🖼️  Testing with: {test_image}")
        
        # Run detection
        results = model(test_image, verbose=True, conf=0.01)  # Very low confidence
        
        print(f"\n🔍 DETECTION RESULTS:")
        for i, result in enumerate(results):
            print(f"Result {i+1}:")
            print(f"  Number of detections: {len(result.boxes) if result.boxes is not None else 0}")
            
            if result.boxes is not None and len(result.boxes) > 0:
                print("  🎯 DETECTIONS FOUND!")
                for j, box in enumerate(result.boxes):
                    conf = float(box.conf.cpu().numpy()[0])
                    cls_id = int(box.cls.cpu().numpy()[0])
                    bbox = box.xywhn.cpu().numpy()[0]  # normalized
                    
                    class_name = model.names.get(cls_id, f"class_{cls_id}")
                    print(f"    Detection {j+1}: {class_name} (conf: {conf:.3f})")
                    print(f"    Bbox: {bbox}")
            else:
                print("  ❌ No detections")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_yolo_directly()