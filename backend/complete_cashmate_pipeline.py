#!/usr/bin/env python3
"""
Complete CashMate Training and Integration Pipeline
"""

import os
import sys
import subprocess
import time
from pathlib import Path
import json

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'ultralytics',
        'roboflow',
        'torch',
        'opencv-python',
        'matplotlib',
        'seaborn',
        'pandas'
    ]
    
    print("Checking requirements...")
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   OK {package}")
        except ImportError:
            print(f"   MISSING {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nInstalling missing packages: {', '.join(missing_packages)}")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        return True
    
    return True

def run_training():
    """Execute the training pipeline"""
    print("\nStarting CashMate Training Pipeline")
    print("=" * 60)
    
    # Check if training scripts exist
    training_scripts = [
        "auto_train_cashmate.py",
        "train_cashmate_enhanced.py",
        "train_roboflow_cashmate.py"
    ]
    
    available_script = None
    for script in training_scripts:
        if os.path.exists(script):
            available_script = script
            break
    
    if not available_script:
        print("ERROR: No training scripts found!")
        return False
    
    print(f"Using training script: {available_script}")
    
    # Execute training
    try:
        result = subprocess.run([sys.executable, available_script], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("Training completed successfully!")
            print("\nTraining Output:")
            print(result.stdout)
        else:
            print("Training failed!")
            print("\nError Output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"ERROR: Training execution failed: {e}")
        return False
    
    return True

def setup_integration():
    """Setup the integration with PesoScan"""
    print("\nSetting up CashMate integration...")
    
    # Check if integration files exist
    integration_files = [
        "cashmate_detector.py",
        "cashmate_api.py"
    ]
    
    missing_files = []
    for file in integration_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"   OK {file}")
    
    if missing_files:
        print(f"   ERROR: Missing integration files: {', '.join(missing_files)}")
        return False
    
    # Test detector initialization
    print("\nTesting detector...")
    try:
        from cashmate_detector import CashMateDetector
        detector = CashMateDetector()
        
        if detector.model:
            print("   CashMate detector loaded successfully")
            print(f"   Model classes: {len(detector.class_names)}")
            return True
        else:
            print("   ERROR: Detector failed to load model")
            return False
            
    except Exception as e:
        print(f"   ERROR: Detector test failed: {e}")
        return False

def create_test_endpoint():
    """Create a simple test endpoint"""
    test_script = '''#!/usr/bin/env python3
"""
Simple CashMate Test Server
"""

from flask import Flask, request, jsonify, render_template_string
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cashmate_api import create_cashmate_routes

app = Flask(__name__)
create_cashmate_routes(app)

@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>CashMate Detector Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 600px; margin: 0 auto; }
            .upload-area { border: 2px dashed #ccc; padding: 40px; text-align: center; margin: 20px 0; }
            .result { margin: 20px 0; padding: 20px; background: #f5f5f5; border-radius: 5px; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>CashMate Philippine Peso Detector</h1>
            <p>Upload an image of a Philippine peso bill to test the detector.</p>
            
            <form id="upload-form" enctype="multipart/form-data">
                <div class="upload-area">
                    <input type="file" id="image" name="image" accept="image/*" required>
                    <p>Select an image file (PNG, JPG, JPEG, GIF, BMP, WEBP)</p>
                </div>
                <button type="submit">Detect Peso Bills</button>
            </form>
            
            <div id="result" class="result" style="display: none;">
                <h3>Detection Results:</h3>
                <pre id="result-json"></pre>
            </div>
        </div>
        
        <script>
            document.getElementById('upload-form').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = new FormData();
                const imageFile = document.getElementById('image').files[0];
                formData.append('image', imageFile);
                
                try {
                    const response = await fetch('/api/cashmate/detect', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    document.getElementById('result-json').textContent = JSON.stringify(result, null, 2);
                    document.getElementById('result').style.display = 'block';
                } catch (error) {
                    document.getElementById('result-json').textContent = 'Error: ' + error.message;
                    document.getElementById('result').style.display = 'block';
                }
            });
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    print("Starting CashMate Test Server...")
    print("Server will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    with open("test_cashmate_server.py", "w", encoding='utf-8') as f:
        f.write(test_script)
    
    print("Test server created: test_cashmate_server.py")
    print("   Run with: python test_cashmate_server.py")

def main():
    """Main execution pipeline"""
    print("CashMate Complete Pipeline")
    print("=" * 50)
    
    # Step 1: Check requirements
    if not check_requirements():
        print("ERROR: Requirements check failed")
        return
    
    # Step 2: Check if we should train or if model exists
    model_exists = False
    runs_dir = Path("runs/train")
    
    if runs_dir.exists():
        for run_dir in runs_dir.iterdir():
            if run_dir.is_dir() and "cashmate" in run_dir.name.lower():
                weights_dir = run_dir / "weights"
                if (weights_dir / "best.pt").exists():
                    model_exists = True
                    print(f"Found existing model: {weights_dir / 'best.pt'}")
                    break
    
    if not model_exists:
        print("No trained model found. Starting training...")
        if not run_training():
            print("ERROR: Training failed. Exiting.")
            return
    else:
        print("Using existing trained model")
    
    # Step 3: Setup integration
    if not setup_integration():
        print("ERROR: Integration setup failed")
        return
    
    # Step 4: Create test endpoint
    create_test_endpoint()
    
    print("\nCashMate Pipeline Complete!")
    print("=" * 50)
    print("Model trained and ready")
    print("Integration scripts created")
    print("Test server available")
    print("\nNext Steps:")
    print("1. Run test server: python test_cashmate_server.py")
    print("2. Integrate with main PesoScan: python cashmate_api.py integrate")
    print("3. Test with real peso images")

if __name__ == "__main__":
    main()