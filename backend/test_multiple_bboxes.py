#!/usr/bin/env python3
"""
Test multiple bounding boxes detection with a real peso image
"""

import cv2
import numpy as np
import asyncio
import sys
import os
import glob
import json

# Add the app directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

async def test_multiple_bounding_boxes():
    """Test multiple bounding boxes with real peso images"""
    
    # Import after adding to path
    from backend.app.services.enhanced_detection_service import enhanced_detection_service
    
    # Initialize the service
    await enhanced_detection_service.initialize()
    
    # Find a real peso image to test
    test_dirs = [
        "../Philippine-Money-1/test/images",
        "../Philippine-Money-1/valid/images", 
        "../Philippine-Money-1/train/images"
    ]
    
    real_image_path = None
    for test_dir in test_dirs:
        full_path = os.path.join(os.path.dirname(__file__), test_dir)
        if os.path.exists(full_path):
            image_files = glob.glob(os.path.join(full_path, "*.jpg"))
            if image_files:
                real_image_path = image_files[0]  # Use first available image
                break
    
    if not real_image_path:
        print("❌ No test peso images found")
        return
    
    print(f"🖼️  Testing with real peso image: {os.path.basename(real_image_path)}")
    
    # Load the image
    image = cv2.imread(real_image_path)
    if image is None:
        print("❌ Could not load image")
        return
    
    print(f"📐 Image size: {image.shape}")
    
    # Process with enhanced detection service
    print("🔍 Processing image for multiple detections...")
    response = await enhanced_detection_service.process_image(image)
    
    print("\n" + "="*80)
    print("🎯 MULTIPLE BOUNDING BOXES TEST RESULTS")
    print("="*80)
    
    # Check response structure
    print(f"📊 Processing Time: {response.processing_time:.3f}s")
    print(f"📝 Message: {response.message}")
    
    # Check for multiple detections
    if response.result and hasattr(response.result, 'detections') and response.result.detections:
        print(f"\n🏆 FOUND {len(response.result.detections)} BOUNDING BOXES!")
        print("-" * 60)
        
        for i, detection in enumerate(response.result.detections, 1):
            print(f"Bounding Box {i}:")
            print(f"  🎯 Class: ₱{detection.class_name}")
            if hasattr(detection, 'feature_name') and detection.feature_name:
                print(f"  🔍 Feature: {detection.feature_name}")
            print(f"  📈 Confidence: {detection.confidence:.3f} ({detection.confidence*100:.1f}%)")
            print(f"  📍 BBox: [{detection.bbox[0]:.3f}, {detection.bbox[1]:.3f}, {detection.bbox[2]:.3f}, {detection.bbox[3]:.3f}]")
            
            # Convert normalized coordinates to pixel coordinates for visualization
            height, width = image.shape[:2]
            x1 = int(detection.bbox[0] * width)
            y1 = int(detection.bbox[1] * height)
            x2 = int(detection.bbox[2] * width)
            y2 = int(detection.bbox[3] * height)
            print(f"  📐 Pixel BBox: [{x1}, {y1}, {x2}, {y2}]")
            print()
        
        # Also check primary detection for compatibility
        if response.result.detection:
            print(f"🥇 PRIMARY DETECTION: ₱{response.result.detection.class_name}")
            print(f"   Confidence: {response.result.detection.confidence:.3f}")
            
        # Create a test response that mimics what the frontend expects
        test_response = {
            "result": {
                "detections": []
            }
        }
        
        for detection in response.result.detections:
            test_response["result"]["detections"].append({
                "bbox": detection.bbox,
                "confidence": detection.confidence,
                "class_name": detection.class_name,
                "feature_name": getattr(detection, 'feature_name', None)
            })
        
        print(f"\n📤 JSON Response for Frontend:")
        print(json.dumps(test_response, indent=2))
        
    else:
        print("\n❌ NO MULTIPLE DETECTIONS FOUND!")
        print("🔍 Checking single detection...")
        
        if response.result and response.result.detection:
            print(f"✅ Single detection found: ₱{response.result.detection.class_name}")
            print(f"   Confidence: {response.result.detection.confidence:.3f}")
        else:
            print("❌ No detections at all!")
    
    print(f"\n✅ Test completed!")

if __name__ == "__main__":
    print("🚀 Starting Multiple Bounding Boxes Test...")
    asyncio.run(test_multiple_bounding_boxes())