"""
Test Counterfeit Detection Integration
Test the new counterfeit detection functionality with the peso detection
"""

import requests
import os
import glob
from pathlib import Path

def test_counterfeit_detection_endpoints():
    """Test the new counterfeit detection API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Counterfeit Detection Integration")
    print("=" * 60)
    
    # Test model status endpoint
    print("\n📊 Testing Model Status Endpoint...")
    try:
        response = requests.get(f"{base_url}/api/counterfeit-model-status")
        if response.status_code == 200:
            status = response.json()
            print("✅ Model status endpoint working!")
            print(f"   Peso detection loaded: {status.get('peso_detection', {}).get('yolo_loaded', False)}")
            print(f"   Counterfeit model loaded: {status.get('counterfeit_detection', {}).get('counterfeit_model_loaded', False)}")
            print(f"   Status: {status.get('status', 'unknown')}")
        else:
            print(f"❌ Model status endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Model status endpoint error: {e}")
    
    # Test with sample images
    print("\n🖼️ Testing with Sample Images...")
    
    # Look for sample images
    dataset_path = os.path.join(os.path.dirname(__file__), "Philippine-Money-1", "test", "images")
    
    if os.path.exists(dataset_path):
        sample_images = glob.glob(os.path.join(dataset_path, "*.jpg"))[:3]  # Test with 3 images
        
        for img_path in sample_images:
            filename = os.path.basename(img_path)
            print(f"\n🔍 Testing with {filename}...")
            
            try:
                with open(img_path, 'rb') as f:
                    files = {'file': (filename, f, 'image/jpeg')}
                    
                    # Test counterfeit analysis endpoint
                    print("   Testing counterfeit analysis...")
                    response = requests.post(f"{base_url}/api/analyze-counterfeit", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        peso_detection = result.get('peso_detection', {})
                        counterfeit_analysis = result.get('counterfeit_analysis', {})
                        
                        print(f"   ✅ Peso detected: {peso_detection.get('detected', False)}")
                        print(f"   💰 Denomination: ₱{peso_detection.get('denomination', 'unknown')}")
                        print(f"   🔒 Authenticity score: {counterfeit_analysis.get('authenticity_score', 0):.2f}")
                        print(f"   ⚠️ Counterfeit probability: {counterfeit_analysis.get('counterfeit_probability', 0):.2f}")
                        
                        features = counterfeit_analysis.get('detected_features', [])
                        print(f"   🏷️ Features detected: {len(features)}")
                        
                    else:
                        print(f"   ❌ Counterfeit analysis failed: {response.status_code}")
            
            except Exception as e:
                print(f"   ❌ Error testing {filename}: {e}")
        
        # Test comprehensive scan
        print(f"\n🔍 Testing Comprehensive Scan...")
        if sample_images:
            img_path = sample_images[0]
            filename = os.path.basename(img_path)
            
            try:
                with open(img_path, 'rb') as f:
                    files = {'file': (filename, f, 'image/jpeg')}
                    
                    response = requests.post(f"{base_url}/api/comprehensive-scan", files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        overall = result.get('overall_assessment', {})
                        
                        print(f"   ✅ Comprehensive scan successful!")
                        print(f"   💰 Peso detected: {overall.get('peso_detected', False)}")
                        print(f"   💵 Denomination: ₱{overall.get('denomination', 'unknown')}")
                        print(f"   🔒 Authenticity score: {overall.get('authenticity_score', 0):.2f}")
                        print(f"   📋 Recommendation: {overall.get('recommendation', 'N/A')}")
                        print(f"   ⏱️ Processing time: {result.get('processing_time', 0):.2f}s")
                        
                    else:
                        print(f"   ❌ Comprehensive scan failed: {response.status_code}")
            
            except Exception as e:
                print(f"   ❌ Error in comprehensive scan: {e}")
    
    else:
        print("❌ No sample images found for testing")
    
    print("\n" + "=" * 60)
    print("🎯 Counterfeit Detection Integration Test Complete!")

def check_api_health():
    """Check if the API server is running"""
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    if check_api_health():
        print("✅ API server is running")
        test_counterfeit_detection_endpoints()
    else:
        print("❌ API server is not running")
        print("💡 Please start the server first: python main.py")
        print("💡 Or run: uvicorn main:app --reload --host 0.0.0.0 --port 8000")