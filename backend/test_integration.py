#!/usr/bin/env python3
"""
Test the complete integration of counterfeit detection
"""

import requests
import base64
from pathlib import Path


def test_comprehensive_scan():
    """Test the comprehensive scan endpoint"""
    
    # Use a sample image from our demo dataset
    image_path = Path("CounterfeitDemo/valid/images/IMG20241109201559_jpg.rf.13d581388fd0b6c2a15fcd0d6f8ff6e6.jpg")
    
    if not image_path.exists():
        print(f"❌ Test image not found: {image_path}")
        return False
    
    # Read image data
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    # Test the comprehensive scan endpoint
    url = "http://localhost:8000/api/comprehensive-scan"
    
    files = {'file': (image_path.name, image_data, 'image/jpeg')}
    
    print("🔍 Testing comprehensive scan...")
    print(f"📁 Image: {image_path.name}")
    print(f"📏 Image size: {len(image_data)} bytes")
    
    try:
        response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Comprehensive scan successful!")
            print(f"🎯 Status: {result.get('status', 'unknown')}")
            
            # Print peso detection results
            peso_detection = result.get('peso_detection', {})
            if peso_detection:
                print(f"💰 Peso detected: {peso_detection.get('detected', False)}")
                if peso_detection.get('detected'):
                    print(f"💵 Denomination: {peso_detection.get('denomination', 'unknown')}")
                    print(f"🎯 Confidence: {peso_detection.get('confidence', 0):.2f}")
            
            # Print counterfeit detection results
            counterfeit_detection = result.get('counterfeit_detection', {})
            if counterfeit_detection:
                print(f"🔒 Authenticity: {counterfeit_detection.get('authenticity', 'unknown')}")
                print(f"🎯 Confidence: {counterfeit_detection.get('confidence', 0):.2f}")
                
                detections = counterfeit_detection.get('detections', [])
                if detections:
                    print(f"🔍 Found {len(detections)} security features:")
                    for i, detection in enumerate(detections[:3]):  # Show first 3
                        print(f"  {i+1}. {detection.get('class', 'unknown')} ({detection.get('confidence', 0):.2f})")
            
            return True
            
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"📝 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def test_health():
    """Test the health endpoint"""
    
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Health check passed!")
            print(f"📊 Status: {result.get('status', 'unknown')}")
            print(f"🤖 Models loaded: {result.get('models_loaded', {})}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def main():
    print("=" * 60)
    print("🧪 PesoScan Integration Test")
    print("=" * 60)
    
    # Test health endpoint
    print("\n1. Testing API Health...")
    health_ok = test_health()
    
    if not health_ok:
        print("❌ Health check failed, stopping tests")
        return
    
    # Test comprehensive scan
    print("\n2. Testing Comprehensive Scan...")
    scan_ok = test_comprehensive_scan()
    
    print("\n" + "=" * 60)
    if health_ok and scan_ok:
        print("🎉 All integration tests passed!")
        print("✅ Backend API is working correctly")
        print("✅ Counterfeit detection is functional")
        print("🚀 PesoScan is ready for use!")
    else:
        print("❌ Some tests failed")
        print("🔧 Please check the backend logs for errors")
    print("=" * 60)


if __name__ == "__main__":
    main()