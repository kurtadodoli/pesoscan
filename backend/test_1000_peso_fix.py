#!/usr/bin/env python3
"""Simple test to check our denomination detection fix via HTTP API"""

import requests
import base64
import cv2
import numpy as np
import time

def create_mock_1000_peso_image():
    """Create a mock image representing a 1000 peso bill"""
    # Create image with brown/gold color (1000 peso characteristics)
    img = np.zeros((400, 800, 3), dtype=np.uint8)
    
    # Use the actual colors similar to 1000 peso bills
    img[:] = (20, 69, 139)  # Blue/brown mix
    
    # Add some text to simulate features
    cv2.putText(img, 'BANGKO SENTRAL', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, 'NG PILIPINAS', (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(img, '1000', (300, 250), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 0), 4)
    cv2.putText(img, 'PISO', (450, 250), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 0), 3)
    
    return img

def test_denomination_detection():
    """Test if our 1000 peso detection fix works"""
    print("🧪 Testing 1000 Peso Denomination Detection Fix")
    print("=" * 60)
    
    # Wait a moment for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    # Test API connectivity first
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print("✅ Backend server is responding")
    except:
        print("❌ Backend server is not responding. Please check if it's running.")
        return
    
    # Create test image
    print("🖼️ Creating mock 1000 peso bill image...")
    image = create_mock_1000_peso_image()
    
    # Convert to base64
    _, buffer = cv2.imencode('.jpg', image)
    image_base64 = base64.b64encode(buffer).decode('utf-8')
    
    # Test comprehensive scan
    url = "http://localhost:8000/api/comprehensive-scan"
    
    # Convert image to file-like object
    files = {"file": ("test_1000.jpg", buffer, "image/jpeg")}
    
    print("📤 Sending test image to comprehensive scan API...")
    
    try:
        response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n✅ SUCCESS! API Response received")
            print("=" * 40)
            
            denomination = result.get('denomination', 'Unknown')
            confidence = result.get('confidence', 0)
            authentic = result.get('authentic', False)
            
            print(f"💰 DETECTED DENOMINATION: ₱{denomination}")
            print(f"🎯 CONFIDENCE: {confidence:.1f}%")
            print(f"✅ AUTHENTIC: {authentic}")
            
            # Check if our fix worked
            if denomination == "1000":
                print("\n🎉 SUCCESS! 1000 peso correctly detected as 1000")
                print("✅ Denomination detection fix is working!")
            elif denomination == "20":
                print("\n❌ PROBLEM STILL EXISTS!")
                print("❌ 1000 peso still being detected as 20 peso")
                print("🔧 Need to investigate further...")
            else:
                print(f"\n🤔 Unexpected result: detected as ₱{denomination}")
                print("🔍 May need to check denomination mapping logic")
            
            # Show detected features
            detections = result.get('detections', [])
            if detections:
                print(f"\n🔍 Security Features Detected ({len(detections)}):")
                for i, det in enumerate(detections[:5]):
                    class_name = det.get('class_name', 'unknown')
                    det_confidence = det.get('confidence', 0)
                    print(f"   {i+1}. {class_name} ({det_confidence:.3f})")
            
            return denomination == "1000"
            
        else:
            print(f"❌ API Error: Status {response.status_code}")
            try:
                error_info = response.json()
                print(f"   Error: {error_info}")
            except:
                print(f"   Raw response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Cannot reach the API")
        print("   Make sure the backend server is running")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    success = test_denomination_detection()
    
    if success:
        print("\n🏆 TEST PASSED: Denomination detection is working correctly!")
    else:
        print("\n❌ TEST FAILED: Issues found with denomination detection")
        print("   Please check the backend logs for more details")