#!/usr/bin/env python3
"""
Test script to verify multiple security feature detection
"""

import cv2
import numpy as np
import asyncio
import sys
import os
import json

# Add the app directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

async def test_multiple_detections():
    """Test the enhanced detection service with multiple bounding boxes"""
    
    # Import after adding to path
    from backend.app.services.enhanced_detection_service import enhanced_detection_service
    
    # Initialize the service
    await enhanced_detection_service.initialize()
    
    # Test with a sample image (create a dummy peso-like image)
    print("🧪 Creating test peso image...")
    
    # Create a test image (simulating a peso bill)
    test_image = np.ones((480, 640, 3), dtype=np.uint8) * 200  # Light background
    
    # Add some colored rectangles to simulate peso features
    cv2.rectangle(test_image, (50, 50), (150, 100), (100, 150, 200), -1)  # Blue region
    cv2.rectangle(test_image, (200, 150), (300, 200), (150, 200, 100), -1)  # Green region
    cv2.rectangle(test_image, (400, 200), (500, 250), (200, 150, 100), -1)  # Orange region
    cv2.rectangle(test_image, (100, 300), (200, 350), (150, 100, 200), -1)  # Purple region
    
    # Add some text-like features
    cv2.putText(test_image, "100", (300, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 3)
    cv2.putText(test_image, "PISO", (450, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    
    print("🔍 Processing image with enhanced detection service...")
    
    # Process the image
    response = await enhanced_detection_service.process_image(test_image)
    
    # Display results
    print("\n" + "="*60)
    print("🎯 DETECTION RESULTS")
    print("="*60)
    
    print(f"📊 Processing Time: {response.processing_time:.3f}s")
    print(f"📝 Message: {response.message}")
    
    if response.result and response.result.detections:
        print(f"\n🏆 FOUND {len(response.result.detections)} SECURITY FEATURES!")
        print("-" * 40)
        
        for i, detection in enumerate(response.result.detections, 1):
            print(f"Feature {i}:")
            print(f"  🎯 Class: ₱{detection.class_name}")
            if hasattr(detection, 'feature_name') and detection.feature_name:
                print(f"  🔍 Feature: {detection.feature_name}")
            print(f"  📈 Confidence: {detection.confidence:.3f} ({detection.confidence*100:.1f}%)")
            print(f"  📍 BBox: [{detection.bbox[0]:.3f}, {detection.bbox[1]:.3f}, {detection.bbox[2]:.3f}, {detection.bbox[3]:.3f}]")
            print()
    else:
        print("\n❌ No detections found")
    
    if response.result and response.result.detection:
        print(f"🥇 PRIMARY DETECTION: ₱{response.result.detection.class_name}")
        print(f"   Confidence: {response.result.detection.confidence:.3f}")
    
    print("\n" + "="*60)
    print("🔧 MODEL STATUS")
    print("="*60)
    
    status = enhanced_detection_service.get_model_status()
    print(f"YOLOv8 Loaded: {'✅' if status['yolo_loaded'] else '❌'}")
    print(f"CNN Loaded: {'✅' if status['cnn_loaded'] else '❌'}")
    print(f"Dataset Loaded: {'✅' if status['dataset_loaded'] else '❌'}")
    print(f"Reference Images: {status['reference_images']}")
    print(f"Using Excellent Model: {'✅' if enhanced_detection_service.using_excellent_model else '❌'}")
    
    # Test with a real peso image if available
    peso_test_images = [
        "../Philippine-Money-1/test/images",
        "../Philippine-Money-1/valid/images", 
        "../Philippine-Money-1/train/images"
    ]
    
    for test_dir in peso_test_images:
        full_path = os.path.join(os.path.dirname(__file__), test_dir)
        if os.path.exists(full_path):
            import glob
            image_files = glob.glob(os.path.join(full_path, "*.jpg"))[:2]  # Test first 2 images
            
            for img_path in image_files:
                print(f"\n🖼️  TESTING REAL PESO IMAGE: {os.path.basename(img_path)}")
                print("-" * 50)
                
                real_image = cv2.imread(img_path)
                if real_image is not None:
                    real_response = await enhanced_detection_service.process_image(real_image)
                    
                    if real_response.result and real_response.result.detections:
                        print(f"🎉 REAL IMAGE: Found {len(real_response.result.detections)} features!")
                        for i, det in enumerate(real_response.result.detections[:5], 1):  # Show first 5
                            feature_name = det.feature_name if hasattr(det, 'feature_name') and det.feature_name else f"₱{det.class_name}"
                            print(f"  {i}. {feature_name} ({det.confidence*100:.1f}%)")
                    else:
                        print("❌ No features detected in real image")
            break  # Only test from first available directory
    
    print(f"\n✅ Test completed! Service uptime: {enhanced_detection_service.get_uptime():.1f}s")

if __name__ == "__main__":
    print("🚀 Starting Multiple Detections Test...")
    asyncio.run(test_multiple_detections())