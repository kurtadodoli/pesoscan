#!/usr/bin/env python3
"""
Test script to verify real AI detection with bounding boxes
"""
import requests
import os
import json

def test_real_detection():
    """Test the actual AI detection with a real peso image"""
    
    # Test the comprehensive scan endpoint
    url = "http://localhost:8000/api/comprehensive-scan"
    
    # Try to find a test peso image
    test_images = [
        r"C:\pesoscan\backend\Philippine-Money-1\test\images",
        r"C:\pesoscan\backend\test_images",
        r"C:\pesoscan\backend"
    ]
    
    peso_image = None
    for test_dir in test_images:
        if os.path.exists(test_dir):
            for file in os.listdir(test_dir):
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    peso_image = os.path.join(test_dir, file)
                    break
            if peso_image:
                break
    
    if not peso_image:
        print("❌ No test peso image found. Please upload a peso image manually.")
        return
    
    print(f"🖼️  Testing with image: {peso_image}")
    
    try:
        with open(peso_image, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ API Response received!")
            print(f"📊 Processing time: {result.get('processing_time', 'N/A')}s")
            
            # Check peso detections
            peso_scan = result.get('peso_scan', {})
            peso_detections = peso_scan.get('result', {}).get('detections', [])
            print(f"🏆 Peso model detections: {len(peso_detections)}")
            
            # Check counterfeit detections
            counterfeit_analysis = result.get('counterfeit_analysis', {})
            counterfeit_detections = counterfeit_analysis.get('detected_features', [])
            print(f"🔍 Counterfeit model detections: {len(counterfeit_detections)}")
            
            # Check combined detections (this is what frontend uses)
            combined_detections = result.get('combined_detections', {})
            peso_features = combined_detections.get('peso_features', [])
            security_features = combined_detections.get('security_features', [])
            
            print(f"\n🎯 COMBINED DETECTIONS:")
            print(f"   Peso features: {len(peso_features)}")
            print(f"   Security features: {len(security_features)}")
            
            # Show actual bounding boxes
            if peso_features:
                print(f"\n💰 PESO FEATURES WITH BOUNDING BOXES:")
                for i, feature in enumerate(peso_features[:3]):
                    bbox = feature.get('bbox', {})
                    print(f"   {i+1}. {feature.get('feature_name', 'Unknown')}")
                    print(f"      Confidence: {feature.get('confidence', 0):.3f}")
                    print(f"      Bbox: x={bbox.get('x', 0):.3f}, y={bbox.get('y', 0):.3f}, w={bbox.get('width', 0):.3f}, h={bbox.get('height', 0):.3f}")
            
            if security_features:
                print(f"\n🔒 SECURITY FEATURES WITH BOUNDING BOXES:")
                for i, feature in enumerate(security_features[:3]):
                    bbox = feature.get('bbox', {})
                    print(f"   {i+1}. {feature.get('feature_name', 'Unknown')}")
                    print(f"      Confidence: {feature.get('confidence', 0):.3f}")
                    print(f"      Bbox: x={bbox.get('x', 0):.3f}, y={bbox.get('y', 0):.3f}, w={bbox.get('width', 0):.3f}, h={bbox.get('height', 0):.3f}")
            
            if not peso_features and not security_features:
                print("❌ NO BOUNDING BOXES DETECTED!")
                print("   This means the AI models aren't detecting anything.")
                print("   The bounding boxes you see in the frontend are just decorative.")
            else:
                print("✅ REAL AI DETECTION WITH BOUNDING BOXES WORKING!")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error testing detection: {e}")

if __name__ == "__main__":
    test_real_detection()