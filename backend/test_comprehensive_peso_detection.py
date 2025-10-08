#!/usr/bin/env python3
"""
Test comprehensive peso value detection with actual API endpoints
"""
import os
import sys
import requests
import json

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_api_peso_detection(image_path: str, expected_peso_value: str = None):
    """Test peso detection via API endpoint"""
    print(f"\n🧪 Testing peso detection for: {os.path.basename(image_path)}")
    print("=" * 60)
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return False
    
    try:
        # Test comprehensive scan endpoint for better detection
        url = "http://localhost:8000/api/comprehensive-scan"
        
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/jpeg')}
            
            print(f"📤 Sending request to {url}")
            response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract peso denomination from response
            overall_assessment = result.get('overall_assessment', {})
            peso_denomination = overall_assessment.get('denomination')
            
            # Also check peso_scan for detected denomination
            peso_scan = result.get('peso_scan', {})
            if peso_scan:
                peso_result = peso_scan.get('result', {})
                if peso_result:
                    peso_detection = peso_result.get('result', {})
                    if peso_detection:
                        alt_denomination = peso_detection.get('denomination')
                        if not peso_denomination and alt_denomination:
                            peso_denomination = alt_denomination
            
            # Check combined detections for peso features
            combined_detections = result.get('combined_detections', {})
            peso_features = combined_detections.get('peso_features', [])
            
            print(f"✅ API Response received successfully!")
            print(f"💰 Detected peso denomination: ₱{peso_denomination or 'unknown'}")
            print(f"📊 Total peso features detected: {len(peso_features)}")
            
            if peso_features:
                print(f"🏷️ Detected features:")
                for i, feature in enumerate(peso_features[:5]):  # Show first 5
                    feature_name = feature.get('feature_name', 'unknown')
                    confidence = feature.get('confidence', 0)
                    print(f"   {i+1}. {feature_name} ({confidence*100:.1f}%)")
                
                if len(peso_features) > 5:
                    print(f"   ... and {len(peso_features) - 5} more features")
            
            # Check if expected peso value matches
            if expected_peso_value:
                if peso_denomination == expected_peso_value:
                    print(f"🎯 CORRECT! Expected ₱{expected_peso_value}, got ₱{peso_denomination}")
                    return True
                else:
                    print(f"⚠️ MISMATCH! Expected ₱{expected_peso_value}, got ₱{peso_denomination}")
                    return False
            else:
                return peso_denomination is not None
            
        else:
            print(f"❌ API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing peso detection: {e}")
        return False

def test_peso_detection_comprehensive():
    """Test peso detection with various peso bill images"""
    print("🚀 COMPREHENSIVE PESO VALUE DETECTION TEST")
    print("=" * 80)
    
    # Test cases with expected peso values
    test_cases = [
        # Look for sample images in the dataset
        ("Philippine-Money-1/test/images", None),  # Directory scan
        ("Philippine-Money-1/valid/images", None), # Directory scan
    ]
    
    # Find test images in the dataset directories
    dataset_base = os.path.join(os.path.dirname(__file__), "Philippine-Money-1")
    test_images = []
    
    for subdir in ["test/images", "valid/images", "train/images"]:
        img_dir = os.path.join(dataset_base, subdir)
        if os.path.exists(img_dir):
            for img_file in os.listdir(img_dir)[:3]:  # Test first 3 images
                if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(img_dir, img_file)
                    
                    # Try to extract expected peso value from filename
                    expected_peso = None
                    filename_lower = img_file.lower()
                    
                    if "1000" in filename_lower:
                        expected_peso = "1000"
                    elif "500" in filename_lower:
                        expected_peso = "500"
                    elif "200" in filename_lower:
                        expected_peso = "200"
                    elif "100" in filename_lower:
                        expected_peso = "100"
                    elif "50" in filename_lower:
                        expected_peso = "50"
                    elif "20" in filename_lower and "200" not in filename_lower:
                        expected_peso = "20"
                    elif "10" in filename_lower and "100" not in filename_lower:
                        expected_peso = "10"
                    elif "5" in filename_lower and "50" not in filename_lower:
                        expected_peso = "5"
                    elif "1" in filename_lower and "10" not in filename_lower:
                        expected_peso = "1"
                    
                    test_images.append((img_path, expected_peso))
    
    if not test_images:
        print("❌ No test images found in dataset directories!")
        return False
    
    print(f"🖼️ Found {len(test_images)} test images")
    print("=" * 80)
    
    # Test each image
    successful_tests = 0
    total_tests = 0
    
    for img_path, expected_peso in test_images:
        total_tests += 1
        success = test_api_peso_detection(img_path, expected_peso)
        if success:
            successful_tests += 1
    
    print("\n" + "=" * 80)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 80)
    print(f"✅ Successful detections: {successful_tests}/{total_tests}")
    print(f"📈 Success rate: {(successful_tests/total_tests)*100:.1f}%")
    
    if successful_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Peso value detection is working correctly!")
    elif successful_tests > total_tests * 0.8:
        print("✅ GOOD! Most tests passed. Peso detection is mostly working.")
    elif successful_tests > total_tests * 0.5:
        print("⚠️ PARTIAL SUCCESS. Some peso detection issues need attention.")
    else:
        print("❌ POOR PERFORMANCE. Peso detection needs significant improvement.")
    
    return successful_tests > 0

if __name__ == "__main__":
    print("🔍 Testing enhanced peso value detection...")
    test_peso_detection_comprehensive()