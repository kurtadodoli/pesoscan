"""
Simple test script to verify the trained YOLOv8 model can detect peso bills
"""
import os
import sys
import requests
import glob
from pathlib import Path

def test_trained_model():
    """Test the trained model with sample images from the dataset"""
    
    # API endpoint
    api_url = "http://localhost:8000/api/upload"
    
    # Get some test images from the dataset
    dataset_path = Path("Philippine-Money-1/test/images")
    
    if not dataset_path.exists():
        print("❌ Dataset not found. Looking for images in other locations...")
        # Try alternative paths
        for alt_path in ["./Philippine-Money-1/valid/images", "./Philippine-Money-1/train/images"]:
            alt_dataset = Path(alt_path)
            if alt_dataset.exists():
                dataset_path = alt_dataset
                print(f"✅ Found images in: {dataset_path}")
                break
    
    if not dataset_path.exists():
        print("❌ No dataset images found. Please check the dataset location.")
        return
    
    # Get first few images for testing
    image_files = list(dataset_path.glob("*.jpg"))[:5]  # Test with first 5 images
    
    if not image_files:
        print("❌ No JPG images found in dataset")
        return
    
    print(f"🧪 Testing trained model with {len(image_files)} images...")
    print("=" * 60)
    
    for i, image_path in enumerate(image_files, 1):
        print(f"\n📸 Test {i}/{len(image_files)}: {image_path.name}")
        
        try:
            # Read image file
            with open(image_path, 'rb') as f:
                files = {'file': (image_path.name, f, 'image/jpeg')}
                
                # Send to API
                response = requests.post(api_url, files=files, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Extract detection info
                    detection = result.get('result', {}).get('detection')
                    bill_result = result.get('result', {}).get('result', {})
                    
                    if detection:
                        denomination = detection.get('class_name', 'Unknown')
                        confidence = detection.get('confidence', 0) * 100
                        print(f"✅ DETECTED: ₱{denomination} peso (Confidence: {confidence:.1f}%)")
                    else:
                        print("❌ No detection found")
                    
                    # Show bill analysis
                    if bill_result:
                        detected_denom = bill_result.get('denomination', 'Unknown')
                        bill_confidence = bill_result.get('confidence', 0) * 100
                        print(f"💰 Bill Analysis: ₱{detected_denom} peso (Overall: {bill_confidence:.1f}%)")
                
                else:
                    print(f"❌ API Error: {response.status_code} - {response.text}")
                    
        except Exception as e:
            print(f"❌ Error testing {image_path.name}: {e}")
        
        print("-" * 40)
    
    print("\n🎯 Test completed!")

if __name__ == "__main__":
    print("🚀 Testing Trained YOLOv8 Model for Peso Detection")
    print("=" * 60)
    
    # Check if API is running
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API is running")
            test_trained_model()
        else:
            print("❌ Backend API is not responding properly")
    except requests.exceptions.RequestException:
        print("❌ Backend API is not running. Please start the backend first:")
        print("   python backend/main.py")