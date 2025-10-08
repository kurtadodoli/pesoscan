#!/usr/bin/env python3
"""
🇵🇭 Final integration test for CashMate trained model
"""

import os
import sys
from pathlib import Path
import json

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our updated detector
from cashmate_detector import CashMateDetector

def test_with_validation_image():
    """Test the detector with a validation image"""
    print("🇵🇭 CashMate Integration Test")
    print("=" * 50)
    
    # Initialize detector
    detector = CashMateDetector()
    
    if not detector.model:
        print("❌ Model failed to load!")
        return False
    
    print(f"✅ Model loaded: {detector.model_path or 'auto-detected'}")
    print(f"📊 Classes: {list(detector.class_names.values())}")
    
    # Find a validation image to test with
    test_image_dir = Path("backend/CASHMATE-PH-BANKNOTES-11/valid/images")
    
    if not test_image_dir.exists():
        print(f"❌ Test image directory not found: {test_image_dir}")
        return False
    
    # Get first available image
    image_files = list(test_image_dir.glob("*.jpg"))
    
    if not image_files:
        print("❌ No test images found!")
        return False
    
    test_image = str(image_files[0])
    print(f"🖼️ Testing with: {Path(test_image).name}")
    
    # Run detection
    result = detector.detect_peso_bills(test_image, confidence_threshold=0.25)
    
    if "error" in result:
        print(f"❌ Detection failed: {result['error']}")
        return False
    
    # Display results
    print(f"\n🎯 Detection Results:")
    print(f"📸 Image: {result['image_info']['width']}x{result['image_info']['height']}")
    print(f"🔢 Detections found: {result['detection_count']}")
    
    if result['detection_count'] > 0:
        print(f"\n📋 Detections:")
        for i, det in enumerate(result['detections'], 1):
            denomination = det.get('denomination')
            denom_text = f"₱{denomination}" if denomination else "N/A"
            print(f"  {i}. Class: {det['class_name']} | Denomination: {denom_text} | Confidence: {det['confidence']:.3f}")
            
        # Test PesoScan format conversion
        pesoscan_result = detector.create_pesoscan_format(result)
        print(f"\n💰 Primary Denomination: ₱{pesoscan_result['result']['denomination']}")
        print(f"🎯 Primary Confidence: {pesoscan_result['result']['confidence']:.3f}")
        
    print(f"\n✅ Integration test completed successfully!")
    return True

def main():
    """Main function"""
    success = test_with_validation_image()
    
    if success:
        print(f"\n🎉 CashMate Model Ready for Production!")
        print(f"🚀 You can now:")
        print(f"   1. Start the API: python backend/main.py")
        print(f"   2. Run frontend: Open frontend/index.html")
        print(f"   3. Test with your own images")
    else:
        print(f"\n❌ Integration test failed!")

if __name__ == "__main__":
    main()