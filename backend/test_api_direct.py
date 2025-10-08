#!/usr/bin/env python3
"""Test the API endpoint directly to confirm results"""

import requests
import cv2
import base64
import numpy as np
import time

def test_api_endpoint():
    """Test API endpoint to see if results match internal testing"""
    print("🌐 TESTING API ENDPOINT DIRECTLY")
    print("=" * 50)
    
    # Create the same test image as internal test
    image = np.ones((400, 600, 3), dtype=np.uint8) * 128
    cv2.rectangle(image, (50, 50), (550, 350), (139, 69, 19), -1)  # Brown rectangle
    cv2.putText(image, '1000', (200, 220), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 4)
    
    # Convert to file format for API
    _, buffer = cv2.imencode('.jpg', image)
    files = {"file": ("test_1000.jpg", buffer, "image/jpeg")}
    
    # Test comprehensive scan endpoint
    url = "http://localhost:8000/api/comprehensive-scan"
    
    print("📤 Sending request to API...")
    try:
        response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ API Response received!")
            print("📊 FULL RESPONSE STRUCTURE:")
            
            # Check overall_assessment for denomination
            overall = result.get('overall_assessment', {})
            peso_scan = result.get('peso_scan', {})
            
            print(f"   💰 Overall Assessment Denomination: {overall.get('denomination', 'NOT_FOUND')}")
            print(f"   📊 Peso Detected: {overall.get('peso_detected', 'NOT_FOUND')}")
            print(f"   🎯 Authenticity Score: {overall.get('authenticity_score', 'NOT_FOUND')}")
            print(f"   ⏱️ Processing Time: {result.get('processing_time', 'NOT_FOUND')}s")
            
            print(f"\n🔍 Overall Assessment Keys: {list(overall.keys())}")
            print(f"🔍 Peso Scan Keys: {list(peso_scan.keys())}")
            
            # Try to find the denomination anywhere in the response
            api_denom = overall.get('denomination', 'Unknown')
            if api_denom == 'Unknown' and 'result' in peso_scan:
                peso_result = peso_scan['result']
                if 'result' in peso_result:
                    classification = peso_result['result']
                    api_denom = classification.get('denomination', 'Unknown')
                    print(f"🔍 Found denomination in peso_scan.result.result: {api_denom}")
            
            # Compare with internal test results
            print(f"\n🔄 COMPARISON:")
            print(f"   Internal Test: 20 peso, 87.5% confidence, True authentic")
            api_conf = overall.get('authenticity_score', 0) * 100  # Convert to percentage
            api_auth = overall.get('peso_detected', False)
            print(f"   API Result:    {api_denom} peso, {api_conf}% confidence, {api_auth} authentic")
            
            if api_denom == "20":
                print(f"   ✅ MATCH: Both internal and API return 20 peso")
                print(f"   🚨 PROBLEM CONFIRMED: Model predicts 20 peso for 1000 peso features")
            elif api_denom == "Unknown":
                print(f"   ⚠️ DISCREPANCY: Internal says 20, API says Unknown")
                print(f"   🔍 Need to investigate API vs internal difference")
            else:
                print(f"   🤔 UNEXPECTED: API returned {api_denom}, internal returned 20")
            
            return result
            
        else:
            print(f"❌ API Error: Status {response.status_code}")
            print(f"   Error: {response.text}")
            return None
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: API server not responding")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    test_api_endpoint()