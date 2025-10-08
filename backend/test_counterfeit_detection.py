#!/usr/bin/env python3
"""
Test Enhanced Counterfeit Detection with Roboflow Model
"""

import requests
import base64
from pathlib import Path


def test_counterfeit_detection():
    """Test the enhanced counterfeit detection with Roboflow model"""
    
    # Test with a sample image from the Roboflow dataset
    image_path = Path("Counterfeit-Money-Detector-v5/valid/images")
    
    # Get the first valid image
    if image_path.exists():
        test_images = list(image_path.glob("*.jpg"))
        if test_images:
            test_image = test_images[0]
        else:
            print("❌ No test images found in Roboflow dataset")
            return False
    else:
        print("❌ Roboflow dataset not found")
        return False
    
    print(f"🔍 Testing counterfeit detection with: {test_image.name}")
    
    # Read image data
    with open(test_image, 'rb') as f:
        image_data = f.read()
    
    # Test the comprehensive scan endpoint
    url = "http://localhost:8000/api/comprehensive-scan"
    files = {'file': (test_image.name, image_data, 'image/jpeg')}
    
    try:
        print("📡 Sending request to API...")
        response = requests.post(url, files=files, timeout=60)  # Longer timeout for comprehensive analysis
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Enhanced counterfeit detection successful!")
            
            # Display comprehensive results
            overall_assessment = result.get('overall_assessment', {})
            counterfeit_analysis = result.get('counterfeit_analysis', {})
            
            print(f"\n📊 COUNTERFEIT DETECTION RESULTS:")
            print(f"🎯 Authenticity Score: {overall_assessment.get('authenticity_score', 0):.3f}")
            print(f"⚠️ Counterfeit Probability: {overall_assessment.get('counterfeit_probability', 0):.3f}")
            print(f"💰 Denomination: {overall_assessment.get('denomination', 'Unknown')}")
            print(f"🔍 Recommendation: {overall_assessment.get('recommendation', 'No recommendation')}")
            
            # Show detected features
            detected_features = counterfeit_analysis.get('detected_features', [])
            if detected_features:
                print(f"\n🔍 DETECTED SECURITY FEATURES ({len(detected_features)} total):")
                for i, feature in enumerate(detected_features[:5]):  # Show top 5
                    print(f"  {i+1}. {feature.get('feature', 'Unknown')} - {feature.get('confidence', 0):.3f} confidence")
            
            # Show recommendations
            recommendations = counterfeit_analysis.get('recommendations', [])
            if recommendations:
                print(f"\n💡 RECOMMENDATIONS:")
                for rec in recommendations[:3]:  # Show top 3
                    print(f"  • {rec}")
            
            # Determine if it's authentic or counterfeit
            auth_score = overall_assessment.get('authenticity_score', 0)
            if auth_score >= 0.75:
                print(f"\n✅ VERDICT: AUTHENTIC BILL (High confidence)")
            elif auth_score >= 0.55:
                print(f"\n⚠️ VERDICT: LIKELY AUTHENTIC (Verify manually)")
            elif auth_score >= 0.35:
                print(f"\n⚠️ VERDICT: SUSPICIOUS (Professional verification needed)")
            else:
                print(f"\n❌ VERDICT: LIKELY COUNTERFEIT (Do not accept)")
            
            return True
            
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"📝 Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main():
    print("=" * 70)
    print("🚀 ENHANCED COUNTERFEIT DETECTION TEST")
    print("🤖 Using Roboflow Trained Model")
    print("=" * 70)
    
    success = test_counterfeit_detection()
    
    print("\n" + "=" * 70)
    if success:
        print("🎉 Enhanced counterfeit detection is working!")
        print("✅ Roboflow model integration successful")
        print("🌐 Website ready for counterfeit detection")
    else:
        print("❌ Counterfeit detection test failed")
        print("🔧 Check server logs and model loading")
    print("=" * 70)


if __name__ == "__main__":
    main()