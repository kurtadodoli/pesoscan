#!/usr/bin/env python3
"""
Test API with a real Philippine money image
"""

import requests
from pathlib import Path
import json

def test_api_with_real_image():
    """Test the API with a real image from the dataset"""
    
    # Find a real image from the dataset
    dataset_path = Path("Philippine-Money-1/test/images")
    image_files = list(dataset_path.glob("*.jpg"))
    
    if not image_files:
        print("❌ No test images found")
        return
        
    test_image = image_files[0]
    print(f"🖼️ Testing with image: {test_image.name}")
    
    # Test health endpoint first
    try:
        health_response = requests.get("http://localhost:8000/api/health", timeout=5)
        print(f"🏥 Health check: {health_response.status_code}")
        
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"   Status: {health_data.get('status')}")
            print(f"   Models: {health_data.get('models_loaded', {})}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Backend server not running")
        return
    
    # Test scan endpoint
    try:
        with open(test_image, 'rb') as f:
            files = {'file': (test_image.name, f, 'image/jpeg')}
            scan_response = requests.post("http://localhost:8000/api/scan", files=files, timeout=30)
        
        print(f"🔍 Scan request: {scan_response.status_code}")
        
        if scan_response.status_code == 200:
            scan_data = scan_response.json()
            print("✅ Scan successful!")
            print(f"   Scan ID: {scan_data.get('id')}")
            print(f"   Processing Time: {scan_data.get('processing_time', 0):.2f}s")
            
            if 'result' in scan_data:
                result = scan_data['result']
                
                # Detection info
                if 'detection' in result and result['detection']:
                    detection = result['detection']
                    print(f"   Detection Confidence: {detection.get('confidence', 0):.1f}%")
                    print(f"   Class: {detection.get('class_name', 'N/A')}")
                
                # Classification info
                if 'result' in result and result['result']:
                    classification = result['result']
                    authentic = classification.get('authentic', False)
                    confidence = classification.get('confidence', 0)
                    denomination = classification.get('denomination', 'N/A')
                    
                    print(f"   Authentic: {'✅ Yes' if authentic else '❌ No'}")
                    print(f"   Confidence: {confidence:.1f}%")
                    print(f"   Denomination: {denomination} peso")
                    
                    # Security features
                    if 'features' in classification:
                        features = classification['features']
                        print("   Security Features:")
                        for feature, present in features.items():
                            status = "✅" if present else "❌"
                            print(f"     {feature.replace('_', ' ').title()}: {status}")
        else:
            print(f"❌ Scan failed: {scan_response.text}")
            
    except Exception as e:
        print(f"❌ Error testing scan: {e}")

if __name__ == "__main__":
    print("🧪 Testing PesoScan API with Real Philippine Money Image")
    print("=" * 60)
    test_api_with_real_image()
    print("\n🏁 API testing completed!")