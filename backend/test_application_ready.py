#!/usr/bin/env python3
"""Quick test to verify the full application is working"""

import requests

def test_full_application():
    """Test that both backend and frontend are running"""
    print("🔍 TESTING FULL APPLICATION SETUP")
    print("=" * 50)
    
    # Test backend API
    print("🔧 Testing Backend API (Port 8000)...")
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Backend API is running and responding")
        else:
            print(f"   ⚠️ Backend API returned status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Backend API is not responding")
        return False
    except Exception as e:
        print(f"   ❌ Backend API error: {e}")
        return False
    
    # Test frontend
    print("\n🌐 Testing Frontend Application (Port 3000)...")
    try:
        response = requests.get("http://localhost:3000/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Frontend application is running and responding")
        else:
            print(f"   ⚠️ Frontend returned status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Frontend application is not responding")
        return False
    except Exception as e:
        print(f"   ❌ Frontend error: {e}")
        return False
    
    print("\n🎉 APPLICATION READY!")
    print("=" * 50)
    print("✅ Backend Server: http://localhost:8000")
    print("✅ Frontend App: http://localhost:3000")
    print("🌟 Chrome should now be open with your PesoScan application!")
    print("\n📱 You can now:")
    print("   1. Upload peso bill images to test denomination detection")
    print("   2. Use the comprehensive scan feature")
    print("   3. Test the accuracy improvements we implemented")
    
    return True

if __name__ == "__main__":
    test_full_application()