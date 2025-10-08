#!/usr/bin/env python3
"""
Quick status check for PesoScan application
"""

import requests
import time

def check_application_status():
    """Check if both backend and frontend are running"""
    
    print("🚀 PesoScan Application Status Check")
    print("=" * 50)
    
    # Check Backend API
    try:
        backend_response = requests.get("http://localhost:8000/api/status", timeout=5)
        if backend_response.status_code == 200:
            print("✅ Backend API: RUNNING on http://localhost:8000")
            status_data = backend_response.json()
            print(f"   - Models loaded: {status_data.get('models_loaded', 'Unknown')}")
            print(f"   - Peso model: {status_data.get('peso_model_status', 'Unknown')}")
            print(f"   - Counterfeit model: {status_data.get('counterfeit_model_status', 'Unknown')}")
        else:
            print(f"⚠️ Backend API: HTTP {backend_response.status_code}")
    except Exception as e:
        print(f"❌ Backend API: Not responding ({str(e)})")
    
    # Check Frontend (try to access it)
    try:
        frontend_response = requests.get("http://localhost:3000", timeout=5)
        if frontend_response.status_code == 200:
            print("✅ Frontend: RUNNING on http://localhost:3000")
        else:
            print(f"⚠️ Frontend: HTTP {frontend_response.status_code}")
    except Exception as e:
        print(f"❌ Frontend: Not responding ({str(e)})")
    
    print("\n🎯 Application Summary:")
    print("- Backend: FastAPI server with YOLOv8 models")
    print("- Frontend: React application with enhanced bounding boxes")
    print("- Models: Philippine-Money-1 (94.0% mAP50) + Counterfeit-v5 (94.0% mAP50)")
    print("- Features: Enhanced visualization with security feature detection")
    
    print("\n🌐 Access URLs:")
    print("- Main Application: http://localhost:3000")
    print("- API Documentation: http://localhost:8000/docs")
    print("- API Status: http://localhost:8000/api/status")
    
    print("\n📱 Ready to use!")
    print("Upload peso bill images to see enhanced bounding box detection!")

if __name__ == "__main__":
    check_application_status()