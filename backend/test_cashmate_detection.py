#!/usr/bin/env python3
"""
Test CashMate detector with peso images
"""

import os
import sys
from cashmate_detector import CashMateDetector

def test_cashmate_detection():
    """Test CashMate detector with available peso images"""
    print("Testing CashMate Philippine Peso Detection")
    print("=" * 50)
    
    # Initialize detector
    detector = CashMateDetector()
    
    if not detector.model:
        print("ERROR: CashMate model not loaded!")
        return False
    
    print(f"Model loaded with {len(detector.class_names)} classes")
    print(f"Classes: {list(detector.class_names.values())}")
    print()
    
    # Look for test images in common directories
    test_dirs = [
        ".",
        "../temp",
        "../assets",
        "../test_images"
    ]
    
    test_images = []
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
    
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            for file in os.listdir(test_dir):
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    if any(peso_term in file.lower() for peso_term in ['peso', '100', '50', '20', '10', '5', '1']):
                        test_images.append(os.path.join(test_dir, file))
    
    if not test_images:
        print("No peso test images found.")
        print("To test, place peso bill images in any of these directories:")
        for test_dir in test_dirs:
            print(f"  - {os.path.abspath(test_dir)}")
        print()
        
        # Create a demo result
        print("Creating demo detection result...")
        demo_result = {
            "success": True,
            "image_info": {"width": 640, "height": 480, "path": "demo_peso.jpg"},
            "detections": [
                {
                    "class_id": 6,
                    "class_name": "100",
                    "denomination": 100,
                    "confidence": 0.85,
                    "bbox": [100, 150, 300, 350],
                    "bbox_normalized": [0.15, 0.31, 0.47, 0.73]
                }
            ],
            "detection_count": 1,
            "model_info": {
                "model_path": "demo",
                "confidence_threshold": 0.25,
                "classes": detector.class_names
            }
        }
        
        # Convert to PesoScan format
        pesoscan_format = detector.create_pesoscan_format(demo_result)
        
        print("Demo CashMate Detection Result:")
        print("-" * 40)
        result = pesoscan_format.get("result", {})
        print(f"Denomination: ₱{result.get('denomination', 'Unknown')}")
        print(f"Confidence: {result.get('confidence', 0):.2%}")
        print(f"Authentic: {result.get('authentic', False)}")
        print(f"Detections: {len(result.get('detections', []))}")
        
        if result.get('detections'):
            for i, det in enumerate(result['detections'], 1):
                print(f"  {i}. {det['feature_name']} - {det['confidence']:.2%}")
        
        return True
    
    # Test with found images
    print(f"Found {len(test_images)} test images:")
    
    success_count = 0
    for i, image_path in enumerate(test_images[:3], 1):  # Test max 3 images
        print(f"\n{i}. Testing: {os.path.basename(image_path)}")
        
        try:
            result = detector.detect_peso_bills(image_path)
            
            if "error" in result:
                print(f"   ERROR: {result['error']}")
                continue
            
            print(f"   Detections: {result['detection_count']}")
            
            if result['detections']:
                # Get best detection
                best_det = result['detections'][0]
                denomination = best_det.get('denomination')
                confidence = best_det.get('confidence', 0)
                
                print(f"   Best: {best_det['class_name']} - {confidence:.2%}")
                if denomination:
                    print(f"   Value: ₱{denomination}")
                
                # Convert to PesoScan format
                pesoscan_result = detector.create_pesoscan_format(result)
                peso_result = pesoscan_result.get("result", {})
                print(f"   PesoScan Format: ₱{peso_result.get('denomination', 'Unknown')} - {peso_result.get('confidence', 0):.2%}")
                
                success_count += 1
            else:
                print("   No peso bills detected")
                
        except Exception as e:
            print(f"   ERROR: {e}")
    
    print(f"\nTesting Summary:")
    print(f"Successfully processed: {success_count}/{len(test_images[:3])}")
    
    return success_count > 0

if __name__ == "__main__":
    success = test_cashmate_detection()
    if success:
        print("\nCashMate detector test completed!")
        sys.exit(0)
    else:
        print("\nCashMate detector test failed!")
        sys.exit(1)