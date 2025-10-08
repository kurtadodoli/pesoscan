#!/usr/bin/env python3
"""
Test script to verify enhanced bounding box functionality
"""

import requests
import json
import os

def test_enhanced_bboxes():
    """Test the enhanced bounding box API endpoint"""
    
    # API endpoint
    url = "http://localhost:8000/api/comprehensive-scan"
    
    # Find a test image
    test_image_paths = [
        "C:/pesoscan/backend/tests/test_images/1000_peso.jpg",
        "C:/pesoscan/backend/tests/test_images/peso_sample.jpg",
        "C:/pesoscan/assets/test_1000_peso.jpg",
        "C:/pesoscan/temp/sample_peso.jpg"
    ]
    
    test_image_path = None
    for path in test_image_paths:
        if os.path.exists(path):
            test_image_path = path
            break
    
    if not test_image_path:
        print("❌ No test image found. Creating a test image request...")
        # Try with a sample from the roboflow dataset
        dataset_path = "C:/pesoscan/backend/Philippine-Money-1/test/images"
        if os.path.exists(dataset_path):
            for file in os.listdir(dataset_path):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    test_image_path = os.path.join(dataset_path, file)
                    break
    
    if not test_image_path:
        print("❌ No test images available")
        return False
    
    print(f"📷 Testing with image: {test_image_path}")
    
    try:
        # Upload image for comprehensive scan
        with open(test_image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Response successful!")
            
            # Check if enhanced bounding box data is present
            print("\n📊 API Response Structure:")
            print(f"- Status: {result.get('status', 'N/A')}")
            print(f"- Message: {result.get('message', 'N/A')}")
            
            # Check combined detections structure
            combined_detections = result.get('combined_detections', {})
            if combined_detections:
                print("✅ Combined detections found!")
                
                # Check peso features
                peso_features = combined_detections.get('peso_features', [])
                print(f"💰 Peso Features: {len(peso_features)} detected")
                for i, feature in enumerate(peso_features[:3]):  # Show first 3
                    print(f"  - Feature {i+1}: {feature.get('feature_name', 'Unknown')}")
                    print(f"    Confidence: {feature.get('confidence', 0):.2f}")
                    bbox = feature.get('bbox', {})
                    if bbox:
                        print(f"    BBox: x={bbox.get('x', 0):.1f}, y={bbox.get('y', 0):.1f}, w={bbox.get('width', 0):.1f}, h={bbox.get('height', 0):.1f}")
                
                # Check security features
                security_features = combined_detections.get('security_features', [])
                print(f"🔒 Security Features: {len(security_features)} detected")
                for i, feature in enumerate(security_features[:3]):  # Show first 3
                    print(f"  - Feature {i+1}: {feature.get('feature_name', 'Unknown')}")
                    print(f"    Confidence: {feature.get('confidence', 0):.2f}")
                    bbox = feature.get('bbox', {})
                    if bbox:
                        print(f"    BBox: x={bbox.get('x', 0):.1f}, y={bbox.get('y', 0):.1f}, w={bbox.get('width', 0):.1f}, h={bbox.get('height', 0):.1f}")
                
                # Check model info
                model_info = combined_detections.get('model_info', {})
                if model_info:
                    print("🤖 Model Information:")
                    print(f"  - Peso Model: {model_info.get('peso_model', 'N/A')}")
                    print(f"  - Security Model: {model_info.get('security_model', 'N/A')}")
                
                print("✅ Enhanced bounding box data structure is correct!")
                return True
            else:
                print("❌ No combined detections found in response")
                return False
        
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Enhanced Bounding Box API...")
    success = test_enhanced_bboxes()
    
    if success:
        print("\n✅ Enhanced bounding box test PASSED!")
        print("🎯 You can now upload images to see enhanced visualization!")
    else:
        print("\n❌ Enhanced bounding box test FAILED!")
        print("💡 Check the API server and try again.")