#!/usr/bin/env python3
"""Test script to verify 1000 peso bill detection accuracy"""

import requests
import cv2
import base64
import numpy as np
import json
import glob
import os

def test_1000_peso_images():
    """Test all available 1000 peso images for accurate detection"""
    
    # API endpoint
    url = "http://localhost:8000/api/scan/comprehensive"
    
    # Find 1000 peso images
    test_paths = [
        r"C:\pesoscan\Philippine-Money-1\train\images\*1000*.jpg",
        r"C:\pesoscan\Philippine-Money-1\valid\images\*1000*.jpg", 
        r"C:\pesoscan\Philippine-Money-1\test\images\*1000*.jpg",
        r"C:\pesoscan\backend\*.jpg",  # Any test images
    ]
    
    images_found = []
    for pattern in test_paths:
        images_found.extend(glob.glob(pattern))
    
    print(f"🔍 Found {len(images_found)} potential 1000 peso images")
    
    # Test first few images
    for i, image_path in enumerate(images_found[:5]):  # Test first 5 images
        if "1000" in os.path.basename(image_path):
            print(f"\n🏷️ Testing: {os.path.basename(image_path)}")
            
            try:
                # Read and encode image
                image = cv2.imread(image_path)
                if image is None:
                    print(f"❌ Could not read image: {image_path}")
                    continue
                
                # Convert to base64
                _, buffer = cv2.imencode('.jpg', image)
                image_base64 = base64.b64encode(buffer).decode('utf-8')
                
                # Send request
                payload = {
                    "image": image_base64,
                    "scan_type": "comprehensive"
                }
                
                response = requests.post(url, json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Check denomination
                    denomination = result.get('denomination')
                    confidence = result.get('confidence', 0)
                    authentic = result.get('authentic', False)
                    
                    print(f"📊 RESULT:")
                    print(f"   💰 Detected: ₱{denomination}")
                    print(f"   🎯 Confidence: {confidence:.1f}%")
                    print(f"   ✅ Authentic: {authentic}")
                    
                    # Check if correct
                    if denomination == "1000":
                        print(f"   ✅ CORRECT! 1000 peso detected as 1000")
                    else:
                        print(f"   ❌ WRONG! 1000 peso detected as {denomination}")
                    
                    # Show security features detected
                    if 'detections' in result:
                        print(f"   🔍 Features detected: {len(result['detections'])}")
                        for det in result['detections'][:3]:  # Show first 3
                            print(f"      - {det.get('class_name', 'unknown')} ({det.get('confidence', 0):.2f})")
                    
                else:
                    print(f"❌ Request failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error testing {image_path}: {e}")

if __name__ == "__main__":
    print("🧪 Testing 1000 Peso Bill Detection Accuracy")
    print("=" * 50)
    test_1000_peso_images()