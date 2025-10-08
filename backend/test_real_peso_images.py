#!/usr/bin/env python3
"""Test with actual peso bill images from the dataset"""

import requests
import os
import glob

def test_with_real_peso_images():
    """Test comprehensive scan with real peso bill images"""
    print("🧪 Testing with Real Peso Bill Images")
    print("=" * 60)
    
    # Find actual peso images
    image_patterns = [
        r"C:\pesoscan\backend\Counterfeit-Money-Detector-5\test\images\*.jpg",
        r"C:\pesoscan\backend\Counterfeit-Money-Detector-5\train\images\*.jpg"
    ]
    
    images_found = []
    for pattern in image_patterns:
        images_found.extend(glob.glob(pattern))
    
    print(f"🔍 Found {len(images_found)} peso bill images")
    
    if not images_found:
        print("❌ No peso bill images found")
        return False
    
    # Test with first few images
    api_url = "http://localhost:8000/api/comprehensive-scan"
    success_count = 0
    
    for i, image_path in enumerate(images_found[:3]):  # Test first 3 images
        print(f"\n📸 Testing image {i+1}: {os.path.basename(image_path)}")
        
        try:
            # Upload the actual image file
            with open(image_path, 'rb') as img_file:
                files = {"file": ("test_peso.jpg", img_file, "image/jpeg")}
                response = requests.post(api_url, files=files, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                
                denomination = result.get('denomination', 'Unknown')
                confidence = result.get('confidence', 0)
                authentic = result.get('authentic', False)
                processing_time = result.get('processing_time', 0)
                
                print(f"   💰 DENOMINATION: ₱{denomination}")
                print(f"   🎯 CONFIDENCE: {confidence:.1f}%")
                print(f"   ✅ AUTHENTIC: {authentic}")
                print(f"   ⏱️ TIME: {processing_time:.2f}s")
                
                # Show some detected features
                detections = result.get('detections', [])
                if detections:
                    print(f"   🔍 Features: {len(detections)} detected")
                    for j, det in enumerate(detections[:3]):
                        feature = det.get('class_name', 'unknown')
                        feat_conf = det.get('confidence', 0)
                        print(f"      - {feature} ({feat_conf:.3f})")
                
                if denomination != "Unknown":
                    success_count += 1
                    print(f"   ✅ SUCCESS: Detected as ₱{denomination}")
                else:
                    print(f"   ⚠️ WARNING: No denomination detected")
                
            else:
                print(f"   ❌ API Error: {response.status_code}")
                try:
                    error_info = response.json()
                    print(f"      Error: {error_info.get('detail', 'Unknown error')}")
                except:
                    print(f"      Raw error: {response.text[:100]}...")
        
        except Exception as e:
            print(f"   ❌ Error processing image: {e}")
    
    print(f"\n📊 SUMMARY:")
    print(f"   ✅ Successful detections: {success_count}/3")
    print(f"   📈 Success rate: {(success_count/3)*100:.1f}%")
    
    return success_count > 0

if __name__ == "__main__":
    success = test_with_real_peso_images()
    
    if success:
        print("\n🏆 REAL IMAGE TEST PASSED!")
        print("   The system can detect actual peso bill features")
    else:
        print("\n❌ REAL IMAGE TEST FAILED!")
        print("   Issues detected with real peso bill recognition")