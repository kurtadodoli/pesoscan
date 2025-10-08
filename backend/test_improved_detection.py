#!/usr/bin/env python3
"""
🔥 QUICK TEST SCRIPT FOR YOUR IMPROVED PESO DETECTION 🔥
Test your excellent 100-epoch model with sample peso images
"""

import requests
import json
import time
from pathlib import Path

def test_peso_detection():
    """Test the improved peso detection API"""
    print("🔥 TESTING YOUR IMPROVED PESO DETECTION!")
    print("=" * 60)
    
    # API endpoint
    api_url = "http://localhost:8000/api/scan"
    
    # Find test images
    test_images_dir = Path("Philippine-Money-1/test/images")
    if test_images_dir.exists():
        test_images = list(test_images_dir.glob("*.jpg"))[:3]  # Test first 3 images
        
        for i, img_path in enumerate(test_images, 1):
            print(f"\n📸 Testing Image {i}: {img_path.name}")
            
            try:
                with open(img_path, 'rb') as f:
                    files = {'file': (img_path.name, f, 'image/jpeg')}
                    response = requests.post(api_url, files=files, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ SUCCESS!")
                    print(f"   Denomination: ₱{result.get('denomination', 'Unknown')}")
                    print(f"   Confidence: {result.get('confidence', 0):.1%}")
                    print(f"   Security Features: {len(result.get('security_features', []))} detected")
                else:
                    print(f"❌ API Error: {response.status_code}")
                    print(f"   Response: {response.text}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
            
            time.sleep(1)  # Small delay between requests
    else:
        print("❌ No test images found")
        print("   Looking for: Philippine-Money-1/test/images/")
    
    print("\n🎯 Test complete! Check the backend logs for detailed detection info.")

if __name__ == "__main__":
    test_peso_detection()