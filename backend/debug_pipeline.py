#!/usr/bin/env python3
"""Debug the denomination detection pipeline step by step"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import cv2
import numpy as np
import asyncio
from app.services.enhanced_detection_service import EnhancedDetectionService

async def debug_denomination_pipeline():
    """Debug each step of the denomination detection pipeline"""
    print("🔍 DEBUGGING DENOMINATION DETECTION PIPELINE")
    print("=" * 60)
    
    # Initialize service
    service = EnhancedDetectionService()
    await service.initialize()
    
    # Create test image (same as before)
    image = np.ones((400, 600, 3), dtype=np.uint8) * 128
    cv2.rectangle(image, (50, 50), (550, 350), (139, 69, 19), -1)
    cv2.putText(image, '1000', (200, 220), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 4)
    
    print("STEP 1: Raw Model Detection")
    print("-" * 30)
    detections = await service.detect_peso_bill(image)
    print(f"Number of detections: {len(detections)}")
    
    for i, det in enumerate(detections):
        print(f"  Detection {i+1}:")
        print(f"    Class: '{det.class_name}' (type: {type(det.class_name)})")
        print(f"    Confidence: {det.confidence}")
    
    if detections:
        print(f"\nSTEP 2: Final Denomination Determination")
        print("-" * 40)
        final_denom = service.determine_final_denomination(detections)
        print(f"Final denomination: '{final_denom}' (type: {type(final_denom)})")
        
        print(f"\nSTEP 3: Classification Process")
        print("-" * 30)
        
        # Test the classify_authenticity function directly
        classification = service.classify_authenticity(image, detections)
        print(f"Classification result:")
        print(f"  Denomination: '{classification.denomination}'")
        print(f"  Confidence: {classification.confidence}")
        print(f"  Authentic: {classification.authentic}")
        
        print(f"\nSTEP 4: Full Pipeline Test")
        print("-" * 25)
        
        # Test the full process_image method
        response = await service.process_image(image)
        print(f"Full pipeline result:")
        print(f"  Response type: {type(response)}")
        if hasattr(response, 'result') and response.result:
            scan_result = response.result
            print(f"  ScanResult type: {type(scan_result)}")
            
            if hasattr(scan_result, 'result') and scan_result.result:
                classification = scan_result.result
                print(f"  Status: Success")
                print(f"  Denomination: '{classification.denomination}'")
                print(f"  Confidence: {classification.confidence}%")
                print(f"  Authentic: {classification.authentic}")
            else:
                print(f"  Status: Failed - no classification result")
        else:
            print(f"  Status: Failed - no result")
            if hasattr(response, '__dict__'):
                print(f"  Response attributes: {list(response.__dict__.keys())}")
    
    return True

if __name__ == "__main__":
    asyncio.run(debug_denomination_pipeline())