#!/usr/bin/env python3
"""Diagnostic test to see what's happening during peso detection"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import cv2
import numpy as np
import asyncio
from app.services.enhanced_detection_service import EnhancedDetectionService

async def diagnostic_test():
    """Test the enhanced detection service directly"""
    print("🔧 DIAGNOSTIC TEST - Enhanced Detection Service")
    print("=" * 60)
    
    # Initialize the service
    print("🔄 Initializing Enhanced Detection Service...")
    service = EnhancedDetectionService()
    await service.initialize()
    
    print("✅ Service initialized successfully")
    
    # Create a simple test image
    print("🖼️ Creating test image...")
    image = np.ones((400, 600, 3), dtype=np.uint8) * 128  # Gray image
    
    # Add some simple features
    cv2.rectangle(image, (50, 50), (550, 350), (139, 69, 19), -1)  # Brown rectangle
    cv2.putText(image, '1000', (200, 220), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 4)
    
    print("📊 Testing peso bill detection...")
    
    # Test the detect_peso_bill method
    detections = await service.detect_peso_bill(image)
    print(f"🔍 Raw detections: {len(detections)} found")
    
    for i, detection in enumerate(detections):
        print(f"   Detection {i+1}:")
        print(f"      Class: {detection.class_name}")
        print(f"      Confidence: {detection.confidence:.4f}")
        print(f"      Box: {detection.bbox}")
    
    # Test the full process_image method
    print("\n📊 Testing full image processing...")
    response = await service.process_image(image)
    
    print(f"✅ Response status: {response.status}")
    if response.result:
        print(f"💰 Denomination: {response.result.denomination}")
        print(f"🎯 Confidence: {response.result.confidence:.2f}%")
        print(f"✅ Authentic: {response.result.authentic}")
        print(f"⏱️ Processing time: {response.result.processing_time:.2f}s")
        
        if hasattr(response.result, 'detections'):
            print(f"🔍 All detections: {len(response.result.detections)}")
            for i, det in enumerate(response.result.detections[:5]):
                print(f"   {i+1}. {det.class_name} ({det.confidence:.4f})")
    else:
        print("❌ No result returned")
    
    # Test the denomination determination logic
    print("\n📊 Testing denomination determination logic...")
    if detections:
        final_denomination = service.determine_final_denomination(detections)
        print(f"🎯 Final denomination: {final_denomination}")
    
    return True

if __name__ == "__main__":
    asyncio.run(diagnostic_test())