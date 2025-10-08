#!/usr/bin/env python3
"""
API Integration for CashMate detector in PesoScan backend
"""

import os
import sys
import tempfile
from pathlib import Path
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import logging

# Add backend to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cashmate_detector import CashMateDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CashMateAPI:
    """API wrapper for CashMate detector"""
    
    def __init__(self):
        self.detector = CashMateDetector()
        self.temp_dir = Path(tempfile.gettempdir()) / "pesoscan_uploads"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Allowed file extensions
        self.allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
    
    def is_allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def process_image(self, image_file, confidence_threshold=0.25):
        """Process uploaded image with CashMate detector"""
        try:
            # Save uploaded file temporarily
            if not self.is_allowed_file(image_file.filename):
                return {"error": "Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP, WEBP"}
            
            filename = secure_filename(image_file.filename)
            temp_path = self.temp_dir / filename
            image_file.save(str(temp_path))
            
            # Run detection
            result = self.detector.detect_peso_bills(str(temp_path), confidence_threshold)
            
            # Clean up temp file
            try:
                temp_path.unlink()
            except:
                pass
            
            # Convert to PesoScan format
            if "error" not in result:
                pesoscan_result = self.detector.create_pesoscan_format(result)
                return pesoscan_result
            else:
                return result
                
        except Exception as e:
            logger.error(f"Image processing failed: {e}")
            return {"error": f"Processing failed: {str(e)}"}

# Initialize API
cashmate_api = CashMateAPI()

def create_cashmate_routes(app):
    """Add CashMate routes to Flask app"""
    
    @app.route('/api/cashmate/detect', methods=['POST'])
    def cashmate_detect():
        """CashMate detection endpoint"""
        try:
            # Check if model is loaded
            if not cashmate_api.detector.model:
                return jsonify({
                    "error": "CashMate model not loaded. Please train the model first."
                }), 503
            
            # Check if file is uploaded
            if 'image' not in request.files:
                return jsonify({"error": "No image file provided"}), 400
            
            image_file = request.files['image']
            if image_file.filename == '':
                return jsonify({"error": "No image selected"}), 400
            
            # Get confidence threshold from request
            confidence = float(request.form.get('confidence', 0.25))
            
            # Process image
            result = cashmate_api.process_image(image_file, confidence)
            
            if "error" in result:
                return jsonify(result), 400
            
            return jsonify(result)
            
        except Exception as e:
            logger.error(f"CashMate detection error: {e}")
            return jsonify({"error": str(e)}), 500
    
    @app.route('/api/cashmate/status', methods=['GET'])
    def cashmate_status():
        """Get CashMate model status"""
        try:
            if cashmate_api.detector.model:
                return jsonify({
                    "status": "ready",
                    "model_loaded": True,
                    "classes": cashmate_api.detector.class_names,
                    "class_count": len(cashmate_api.detector.class_names),
                    "model_path": cashmate_api.detector.model_path or "auto-detected"
                })
            else:
                return jsonify({
                    "status": "not_ready",
                    "model_loaded": False,
                    "message": "No trained model available. Please train the model first."
                })
                
        except Exception as e:
            return jsonify({
                "status": "error",
                "error": str(e)
            }), 500
    
    @app.route('/api/cashmate/info', methods=['GET'])
    def cashmate_info():
        """Get CashMate model information"""
        return jsonify({
            "name": "CashMate Philippine Banknotes Detector",
            "version": "v11",
            "description": "YOLOv8-based Philippine peso banknote detection",
            "supported_denominations": [1, 5, 10, 20, 50, 100, 200, 500, 1000],
            "dataset": "CashMate Philippine Banknotes from Roboflow",
            "model_type": "YOLOv8n",
            "confidence_threshold": 0.25,
            "supported_formats": list(cashmate_api.allowed_extensions)
        })

def integrate_with_main_api(main_py_path="main.py"):
    """Integrate CashMate with existing main.py"""
    try:
        if not os.path.exists(main_py_path):
            logger.warning(f"Main API file not found: {main_py_path}")
            return False
        
        # Read existing main.py
        with open(main_py_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check if already integrated
        if "cashmate_detector" in content or "CashMate" in content:
            logger.info("CashMate already integrated with main API")
            return True
        
        # Add integration code
        integration_code = '''
# CashMate Integration
try:
    from cashmate_api import create_cashmate_routes
    create_cashmate_routes(app)
    print("✅ CashMate detector integrated successfully")
except ImportError as e:
    print(f"⚠️ CashMate integration failed: {e}")
except Exception as e:
    print(f"❌ CashMate integration error: {e}")
'''
        
        # Find a good place to add the integration
        if "if __name__ == '__main__':" in content:
            # Add before main block
            content = content.replace(
                "if __name__ == '__main__':",
                integration_code + "\nif __name__ == '__main__':"
            )
        else:
            # Add at the end
            content += integration_code
        
        # Backup original file
        backup_path = f"{main_py_path}.backup"
        with open(backup_path, 'w', encoding='utf-8') as f:
            with open(main_py_path, 'r', encoding='utf-8', errors='ignore') as orig:
                f.write(orig.read())
        
        # Write updated file
        with open(main_py_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"✅ CashMate integrated with {main_py_path}")
        logger.info(f"📁 Backup created: {backup_path}")
        return True
        
    except Exception as e:
        logger.error(f"Integration failed: {e}")
        return False

def test_api_integration():
    """Test the API integration"""
    print("🧪 Testing CashMate API Integration")
    print("=" * 50)
    
    # Test detector initialization
    print("1. Testing detector initialization...")
    if cashmate_api.detector.model:
        print("   ✅ Detector loaded successfully")
        print(f"   📊 Classes: {len(cashmate_api.detector.class_names)}")
    else:
        print("   ❌ Detector not loaded - train model first")
        return
    
    # Test API status
    print("\n2. Testing API status...")
    try:
        from flask import Flask
        test_app = Flask(__name__)
        create_cashmate_routes(test_app)
        print("   ✅ Routes created successfully")
        
        with test_app.test_client() as client:
            response = client.get('/api/cashmate/status')
            print(f"   📡 Status endpoint: {response.status_code}")
            
            response = client.get('/api/cashmate/info')
            print(f"   📝 Info endpoint: {response.status_code}")
        
    except Exception as e:
        print(f"   ❌ API test failed: {e}")
    
    print("\n✅ Integration test completed")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "integrate":
        # Integrate with main API
        integrate_with_main_api()
    elif len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test the integration
        test_api_integration()
    else:
        # Show usage
        print("CashMate API Integration")
        print("Usage:")
        print("  python cashmate_api.py integrate  - Integrate with main.py")
        print("  python cashmate_api.py test       - Test the integration")