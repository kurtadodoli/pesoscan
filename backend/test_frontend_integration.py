#!/usr/bin/env python3
"""
🧪 Frontend-Backend Integration Test for Counterfeit Detection
Test the comprehensive scan endpoint that the frontend will use
"""

import requests
import json
import os
import sys
from pathlib import Path

def test_counterfeit_api():
    """Test the counterfeit detection API endpoint"""
    print("🧪 Testing Counterfeit Detection API Integration")
    print("=" * 60)
    
    # API endpoint
    api_url = "http://localhost:8000/api/comprehensive-scan"
    
    # Test image path
    test_image_dir = Path("Counterfeit-Money-Detector-5/test/images")
    if not test_image_dir.exists():
        print(f"❌ Test image directory not found: {test_image_dir}")
        return False
    
    # Get a test image
    test_images = list(test_image_dir.glob("*.jpg"))
    if not test_images:
        print("❌ No test images found")
        return False
    
    test_image = test_images[0]
    print(f"📸 Testing with image: {test_image.name}")
    
    try:
        # Test if API server is running
        health_response = requests.get("http://localhost:8000/api/health", timeout=5)
        if health_response.status_code != 200:
            print("❌ API server is not running or unhealthy")
            print("   Start the server with: python main.py")
            return False
        
        print("✅ API server is healthy")
        
        # Test comprehensive scan
        with open(test_image, 'rb') as f:
            files = {'file': (test_image.name, f, 'image/jpeg')}
            
            print("🔍 Sending comprehensive scan request...")
            response = requests.post(api_url, files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Comprehensive scan successful!")
            
            # Print results summary
            print("\n📊 SCAN RESULTS SUMMARY:")
            print("-" * 40)
            
            # Overall assessment
            overall = result.get('overall_assessment', {})
            print(f"Peso Detected: {overall.get('peso_detected', False)}")
            print(f"Denomination: {overall.get('denomination', 'Unknown')}")
            print(f"Authenticity Score: {overall.get('authenticity_score', 0):.3f}")
            print(f"Counterfeit Probability: {overall.get('counterfeit_probability', 1):.3f}")
            print(f"Recommendation: {overall.get('recommendation', 'N/A')}")
            
            # Counterfeit analysis
            counterfeit = result.get('counterfeit_analysis', {})
            if counterfeit:
                detected_features = counterfeit.get('detected_features', [])
                print(f"\n🎯 Detected Features: {len(detected_features)}")
                for i, feature in enumerate(detected_features[:5]):
                    conf = feature.get('confidence', 0) * 100
                    print(f"   {i+1}. {feature.get('feature', 'Unknown')} ({conf:.1f}%)")
                if len(detected_features) > 5:
                    print(f"   ... and {len(detected_features) - 5} more")
            
            # Processing time
            proc_time = result.get('processing_time', 0)
            print(f"\n⏱️  Processing Time: {proc_time:.2f}s")
            
            print("\n🎉 Integration test PASSED!")
            print("Frontend can successfully communicate with the counterfeit detection model")
            return True
            
        else:
            print(f"❌ API request failed with status {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API server")
        print("   Make sure the backend is running: python main.py")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out - analysis taking too long")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_model_status():
    """Test the model status endpoint"""
    try:
        print("\n🔍 Checking model status...")
        response = requests.get("http://localhost:8000/api/counterfeit-model-status", timeout=5)
        
        if response.status_code == 200:
            status = response.json()
            print("✅ Model status retrieved successfully:")
            
            counterfeit_status = status.get('counterfeit_detection', {})
            print(f"   Counterfeit Model Loaded: {counterfeit_status.get('counterfeit_model_loaded', False)}")
            print(f"   Model Path: {counterfeit_status.get('model_path', 'N/A')}")
            print(f"   Classes: {counterfeit_status.get('classes', 0)}")
            
            peso_status = status.get('peso_detection', {})
            print(f"   Peso Detection Model: {peso_status.get('yolo_loaded', False)}")
            
            return True
        else:
            print(f"❌ Model status check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Model status check error: {e}")
        return False

def main():
    print("🚀 COUNTERFEIT DETECTION API INTEGRATION TEST")
    print("Testing frontend-backend communication for counterfeit detection")
    print("=" * 70)
    
    # Test model status first
    if not test_model_status():
        print("\n❌ Model status test failed")
        return 1
    
    # Test the main API
    if not test_counterfeit_api():
        print("\n❌ API integration test failed")
        return 1
    
    print("\n🎉 ALL TESTS PASSED!")
    print("=" * 70)
    print("✅ Backend counterfeit detection is ready")
    print("✅ Frontend can communicate with the API") 
    print("✅ Comprehensive scan endpoint is working")
    print("🚀 Your counterfeit detection system is ready for use!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())