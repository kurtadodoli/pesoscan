#!/usr/bin/env python3
"""Simple test to check if API is responding"""

import requests
import json

def test_api_health():
    """Test if the API is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running successfully!")
            print(f"   Status: {response.json()}")
        else:
            print(f"❌ API returned status code: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API - server may not be running")
        print("   Please start the backend server first")
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    print("🔍 Testing PesoScan API Health...")
    test_api_health()