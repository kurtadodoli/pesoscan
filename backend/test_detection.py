import requests
import json
import os

# Test with an image from the Roboflow dataset
test_img_path = 'Philippine-Money-1/test/images/IMG_20240829_143721_jpg.rf.624351226440fec0768aee40197ee7eb.jpg'
if os.path.exists(test_img_path):
    print(f'🔍 Testing with Roboflow dataset image: {os.path.basename(test_img_path)}')
    with open(test_img_path, 'rb') as f:
        files = {'file': f}
        try:
            response = requests.post('http://localhost:8000/api/scan', files=files, timeout=30)
            if response.status_code == 200:
                result = response.json()
                print('\n✅ PESO DETECTION SUCCESS!')
                print(f"💰 Denomination: ₱{result['result']['result']['denomination']} peso")
                print(f"📊 Confidence: {result['result']['result']['confidence']:.1f}%")
                print(f"🏛️ Series: {result['result']['result'].get('series_year', 'Unknown')}")
                print(f"✅ Peso detected: {result['result']['result']['authentic']}")
                if result['result']['detection']:
                    print(f"🔍 Detection confidence: {result['result']['detection']['confidence']:.1f}%")
                print(f"⏱️ Processing time: {result.get('processing_time', 0):.2f}s")
            else:
                print(f'❌ Error: {response.status_code} - {response.text}')
        except Exception as e:
            print(f'❌ Request failed: {e}')
else:
    print(f'❌ Image not found: {test_img_path}')