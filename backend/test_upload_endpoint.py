import requests
import os

# Test the upload endpoint with a real image
def test_upload():
    url = "http://localhost:8000/api/upload"
    
    # Look for any image in the datasets directory
    image_path = None
    datasets_dir = "datasets"
    if os.path.exists(datasets_dir):
        for root, dirs, files in os.walk(datasets_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(root, file)
                    break
            if image_path:
                break
    
    if not image_path:
        # Use a sample image from the Roboflow dataset
        sample_dirs = ["Philippine-Money-1", "trained_models"]
        for sample_dir in sample_dirs:
            if os.path.exists(sample_dir):
                for root, dirs, files in os.walk(sample_dir):
                    for file in files:
                        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                            image_path = os.path.join(root, file)
                            break
                    if image_path:
                        break
    
    if not image_path:
        print("No image found for testing")
        return
        
    print(f"Testing upload with: {image_path}")
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files, timeout=30)
            
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Upload successful!")
            result = response.json()
            print(f"Response: {result}")
        else:
            print(f"❌ Upload failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_upload()