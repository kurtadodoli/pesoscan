#!/usr/bin/env python3
"""
Test YOLOv8 model directly for multiple detections with lower confidence
"""

import cv2
import numpy as np
import sys
import os

# Add the app directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_yolo_multiple_detections():
    """Test YOLOv8 model directly with lower confidence to get multiple detections"""
    
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
        
        # Create a synthetic peso-like test image with multiple features
        print("🎨 Creating synthetic peso bill image...")
        height, width = 480, 640
        image = np.ones((height, width, 3), dtype=np.uint8) * 240  # Light background
        
        # Add multiple colored regions to simulate different peso features
        features = [
            ((50, 50, 150, 100), (100, 150, 200)),    # Blue region (watermark area)
            ((200, 80, 320, 130), (150, 200, 100)),   # Green region (security thread)
            ((400, 60, 520, 110), (200, 150, 100)),   # Orange region (denomination)
            ((100, 200, 200, 280), (150, 100, 200)),  # Purple region (portrait)
            ((350, 180, 450, 260), (200, 100, 150)),  # Pink region (serial number)
            ((150, 320, 280, 380), (100, 200, 150)),  # Cyan region (ornamental)
            ((380, 300, 500, 360), (180, 180, 100)),  # Yellow region (value)
        ]
        
        for (x1, y1, x2, y2), color in features:
            cv2.rectangle(image, (x1, y1), (x2, y2), color, -1)
            # Add some text-like features
            cv2.putText(image, "PESO", (x1+10, y1+30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
        
        # Add main denomination
        cv2.putText(image, "100", (250, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 4)
        cv2.putText(image, "PISO", (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)
        
        # Test with VERY low confidence to capture multiple features
        print("🔍 Running inference with low confidence...")
        for conf_threshold in [0.05, 0.1, 0.15, 0.2]:
            print(f"\n📊 Testing with confidence threshold: {conf_threshold}")
            results = model(image, verbose=False, conf=conf_threshold)
            
            total_detections = 0
            for result in results:
                total_detections += len(result.boxes)
                
                if len(result.boxes) > 0:
                    print(f"🎯 FOUND {len(result.boxes)} DETECTIONS at {conf_threshold} confidence!")
                    
                    for i, box in enumerate(result.boxes):
                        confidence = float(box.conf.cpu().numpy()[0])
                        class_id = int(box.cls.cpu().numpy()[0])
                        bbox = box.xywhn.cpu().numpy()[0]  # normalized
                        
                        class_name = model.names.get(class_id, f"class_{class_id}")
                        
                        print(f"  Detection {i+1}:")
                        print(f"    Feature: {class_name}")
                        print(f"    Confidence: {confidence:.3f} ({confidence*100:.1f}%)")
                        print(f"    BBox: [{bbox[0]:.3f}, {bbox[1]:.3f}, {bbox[2]:.3f}, {bbox[3]:.3f}]")
                else:
                    print(f"❌ No detections at {conf_threshold} confidence")
            
            if total_detections >= 3:  # If we get multiple detections, break
                print(f"✅ SUCCESS: Found {total_detections} detections!")
                break
        
        # Test what the enhanced detection service would return
        print(f"\n🧪 Testing Enhanced Detection Service...")
        
        # Import detection service
        from app.services.enhanced_detection_service import enhanced_detection_service
        
        # Mock initialization for testing
        enhanced_detection_service.yolo_model = model
        enhanced_detection_service.using_excellent_model = True
        enhanced_detection_service.counterfeit_model_mapping = {
            0: "1000", 1: "1000", 2: "100", 3: "100", 4: "10", 5: "10", 6: "10", 7: "10",
            8: "1", 9: "1", 10: "1", 11: "1", 12: "200", 13: "200", 14: "20", 15: "20",
            16: "20", 17: "20", 18: "0.25", 19: "0.25", 20: "0.25", 21: "0.25",
            22: "500", 23: "500", 24: "50", 25: "50", 26: "5", 27: "5", 28: "5", 29: "5",
            30: "100", 31: "20", 32: "500", 33: "1000", 34: "5", 35: "100", 36: "50",
            37: "200", 38: "20", 39: "100", 40: "1000"
        }
        
        # Test the detection function
        import asyncio
        async def test_detection():
            detections = await enhanced_detection_service.detect_peso_bill(image)
            print(f"🏆 Enhanced Detection Service returned: {len(detections) if detections else 0} detections")
            if detections:
                for i, detection in enumerate(detections, 1):
                    print(f"  Detection {i}: ₱{detection.class_name} ({detection.confidence:.3f})")
        
        asyncio.run(test_detection())
                
    except ImportError:
        print("❌ Ultralytics not available")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🔍 Testing Multiple Detections with YOLOv8...")
    test_yolo_multiple_detections()