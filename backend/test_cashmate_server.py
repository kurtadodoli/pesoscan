#!/usr/bin/env python3
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
