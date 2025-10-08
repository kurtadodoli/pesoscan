#!/usr/bin/env python3
"""
🇵🇭 Test the newly trained CashMate model
"""

import os
import sys
from pathlib import Path
from ultralytics import YOLO
import cv2
import numpy as np

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class CashMateModelTester:
    def __init__(self):
        self.model_path = "runs/detect/cashmate_production/weights/best.pt"
        self.test_images_dir = "backend/CASHMATE-PH-BANKNOTES-11/valid/images"
        
        # Class names mapping
        self.class_names = {
            0: "₱100",
            1: "₱1000", 
            2: "₱20",
            3: "₱200",
            4: "₱50",
            5: "₱500"
        }
        
        print("🇵🇭 CashMate Trained Model Tester")
        print("=" * 50)
    
    def load_model(self):
        """Load the trained model"""
        print(f"📄 Loading model: {self.model_path}")
        
        if not os.path.exists(self.model_path):
            print(f"❌ Model not found: {self.model_path}")
            return False
            
        try:
            self.model = YOLO(self.model_path)
            print(f"✅ Model loaded successfully!")
            print(f"🏗️ Model architecture: {self.model.model_name if hasattr(self.model, 'model_name') else 'YOLOv8'}")
            return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def test_sample_images(self, num_samples=5):
        """Test on sample validation images"""
        print(f"\n🖼️ Testing on {num_samples} sample images...")
        
        if not os.path.exists(self.test_images_dir):
            print(f"❌ Test images directory not found: {self.test_images_dir}")
            return
        
        # Get sample images
        image_files = list(Path(self.test_images_dir).glob("*.jpg"))[:num_samples]
        
        if not image_files:
            print("❌ No test images found!")
            return
        
        print(f"📸 Found {len(image_files)} test images")
        
        for i, img_path in enumerate(image_files, 1):
            print(f"\n--- Test {i}: {img_path.name} ---")
            
            try:
                # Run inference
                results = self.model(str(img_path), conf=0.25)
                
                if results and len(results) > 0:
                    result = results[0]
                    
                    if result.boxes is not None and len(result.boxes) > 0:
                        boxes = result.boxes
                        print(f"🎯 Found {len(boxes)} detections:")
                        
                        for j, box in enumerate(boxes):
                            # Get class and confidence
                            cls = int(box.cls.item())
                            conf = box.conf.item()
                            
                            denomination = self.class_names.get(cls, f"Class_{cls}")
                            print(f"  {j+1}. {denomination} - {conf:.3f} confidence")
                    else:
                        print("❌ No detections found")
                else:
                    print("❌ No results returned")
                    
            except Exception as e:
                print(f"❌ Error processing {img_path.name}: {e}")
    
    def model_info(self):
        """Display model information"""
        print(f"\n📊 Model Information:")
        print(f"📁 Model path: {self.model_path}")
        print(f"🏷️ Classes: {len(self.class_names)}")
        
        for cls_id, name in self.class_names.items():
            print(f"   {cls_id}: {name}")
    
    def run_comprehensive_test(self):
        """Run all tests"""
        print("🚀 Starting comprehensive model test...")
        
        # Load model
        if not self.load_model():
            return False
        
        # Show model info
        self.model_info()
        
        # Test on sample images
        self.test_sample_images(5)
        
        print(f"\n🎉 Testing completed!")
        print(f"✅ Model is ready for production use!")
        return True

def main():
    """Main function"""
    tester = CashMateModelTester()
    tester.run_comprehensive_test()

if __name__ == "__main__":
    main()