#!/usr/bin/env python3
"""
Integration script to use trained CashMate model in PesoScan
"""

import os
import sys
import torch
import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path
import json
import logging
from typing import List, Dict, Tuple, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CashMateDetector:
    """Philippine Peso Bill Detector using trained CashMate model"""
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.model_path = model_path
        self.class_names = {}
        self.confidence_threshold = 0.25
        self.load_model()
    
    def find_best_model(self) -> Optional[str]:
        """Find the best trained model automatically"""
        # Priority order: Latest trained CashMate production model first
        model_paths = [
            "runs/detect/cashmate_production/weights/best.pt",  # Latest trained model
            "runs/train/cashmate_real/weights/best.pt",        # Previous real dataset model
            "trained_models/cashmate_best.pt",                 # Backup location
        ]
        
        for model_path in model_paths:
            if os.path.exists(model_path):
                logger.info(f"Found trained model: {model_path}")
                return model_path
        
        # Fallback: Look in runs/train and runs/detect directories
        for runs_dir_name in ["runs/detect", "runs/train"]:
            runs_dir = Path(runs_dir_name)
            if not runs_dir.exists():
                continue
                
            best_model = None
            best_priority = 0
            best_map = 0
            
            for run_dir in runs_dir.iterdir():
                if run_dir.is_dir() and "cashmate" in run_dir.name.lower():
                    weights_dir = run_dir / "weights"
                    best_pt = weights_dir / "best.pt"
                    
                    if best_pt.exists():
                        # Prioritize production models, then real dataset models
                        priority = 3 if "production" in run_dir.name.lower() else (2 if "real" in run_dir.name.lower() else 1)
                        
                        # Try to get mAP from results
                        current_map = 0
                        results_csv = run_dir / "results.csv"
                        if results_csv.exists():
                            try:
                                import pandas as pd
                                df = pd.read_csv(results_csv)
                                current_map = df['metrics/mAP50(B)'].iloc[-1] if 'metrics/mAP50(B)' in df.columns else 0
                            except:
                                pass
                        
                        # Select best model based on priority and mAP
                        if priority > best_priority or (priority == best_priority and current_map > best_map):
                            best_priority = priority
                            best_map = current_map
                            best_model = str(best_pt)
            
            if best_model:
                return best_model
        
        logger.warning("No trained CashMate models found")
        return None
    
    def load_model(self):
        """Load the trained YOLOv8 model"""
        try:
            # Use provided model path or find best model
            if self.model_path and os.path.exists(self.model_path):
                model_path = self.model_path
            else:
                model_path = self.find_best_model()
            
            if not model_path:
                logger.error("No trained model found!")
                return False
            
            logger.info(f"Loading model from: {model_path}")
            self.model = YOLO(model_path)
            
            # Get class names from the trained CashMate model
            if hasattr(self.model.model, 'names'):
                self.class_names = self.model.model.names
            else:
                # CashMate Philippine peso classes (matching the trained model)
                self.class_names = {
                    0: '100',    # ₱100
                    1: '1000',   # ₱1000  
                    2: '20',     # ₱20
                    3: '200',    # ₱200
                    4: '50',     # ₱50
                    5: '500'     # ₱500
                }
            
            logger.info(f"Model loaded successfully with {len(self.class_names)} classes")
            logger.info(f"Classes: {list(self.class_names.values())}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def detect_peso_bills(self, image_path: str, confidence_threshold: float = None) -> Dict:
        """
        Detect Philippine peso bills in an image
        
        Args:
            image_path: Path to the image file
            confidence_threshold: Minimum confidence threshold (default: 0.25)
            
        Returns:
            Dictionary with detection results
        """
        if not self.model:
            return {"error": "Model not loaded"}
        
        try:
            # Set confidence threshold
            conf_threshold = confidence_threshold or self.confidence_threshold
            
            # Run inference
            results = self.model(image_path, conf=conf_threshold, verbose=False)
            
            # Process results
            detections = []
            image_info = {}
            
            if results and len(results) > 0:
                result = results[0]
                
                # Image info
                image_info = {
                    "width": result.orig_shape[1],
                    "height": result.orig_shape[0],
                    "path": image_path
                }
                
                # Process detections
                if result.boxes is not None and len(result.boxes) > 0:
                    boxes = result.boxes.xyxy.cpu().numpy()  # Bounding boxes
                    confidences = result.boxes.conf.cpu().numpy()  # Confidence scores
                    classes = result.boxes.cls.cpu().numpy().astype(int)  # Class indices
                    
                    for i in range(len(boxes)):
                        x1, y1, x2, y2 = boxes[i]
                        confidence = float(confidences[i])
                        class_id = classes[i]
                        class_name = self.class_names.get(class_id, f"class_{class_id}")
                        
                        # Extract denomination from class name
                        denomination = self.extract_denomination(class_name)
                        
                        detection = {
                            "class_id": int(class_id),
                            "class_name": class_name,
                            "denomination": denomination,
                            "confidence": confidence,
                            "bbox": [float(x1), float(y1), float(x2), float(y2)],
                            "bbox_normalized": [
                                float(x1) / image_info["width"],
                                float(y1) / image_info["height"],
                                float(x2) / image_info["width"],
                                float(y2) / image_info["height"]
                            ]
                        }
                        detections.append(detection)
            
            # Sort detections by confidence
            detections.sort(key=lambda x: x["confidence"], reverse=True)
            
            return {
                "success": True,
                "image_info": image_info,
                "detections": detections,
                "detection_count": len(detections),
                "model_info": {
                    "model_path": self.model_path or "auto-detected",
                    "confidence_threshold": conf_threshold,
                    "classes": self.class_names
                }
            }
            
        except Exception as e:
            logger.error(f"Detection failed: {e}")
            return {"error": str(e)}
    
    def extract_denomination(self, class_name: str) -> Optional[int]:
        """Extract peso denomination from class name"""
        try:
            # Look for numbers in class name
            import re
            numbers = re.findall(r'\d+', class_name)
            
            if numbers:
                value = int(numbers[0])
                # Validate it's a valid peso denomination
                valid_denominations = [1, 5, 10, 20, 50, 100, 200, 500, 1000]
                if value in valid_denominations:
                    return value
            
            return None
            
        except:
            return None
    
    def get_highest_confidence_denomination(self, detections: List[Dict]) -> Optional[int]:
        """Get the denomination with highest confidence"""
        if not detections:
            return None
        
        # Sort by confidence and return first valid denomination
        for detection in sorted(detections, key=lambda x: x["confidence"], reverse=True):
            if detection.get("denomination"):
                return detection["denomination"]
        
        return None
    
    def create_pesoscan_format(self, detection_result: Dict) -> Dict:
        """Convert detection result to PesoScan format"""
        if "error" in detection_result:
            return {"error": detection_result["error"]}
        
        detections = detection_result.get("detections", [])
        
        # Get primary denomination
        primary_denomination = self.get_highest_confidence_denomination(detections)
        
        # Format for PesoScan
        pesoscan_result = {
            "result": {
                "authentic": True,  # Assume authentic if detected
                "confidence": detections[0]["confidence"] if detections else 0,
                "denomination": primary_denomination,
                "detections": [
                    {
                        "class_name": det["class_name"],
                        "feature_name": f"₱{det['denomination']}" if det.get("denomination") else det["class_name"],
                        "confidence": det["confidence"],
                        "bbox": det["bbox_normalized"]
                    }
                    for det in detections
                ]
            },
            "processing_time": 0.5,  # Placeholder
            "model_info": {
                "name": "CashMate Philippine Banknotes",
                "version": "v11",
                "mAP50": "Training dependent"
            }
        }
        
        return pesoscan_result

def test_detector():
    """Test the detector with sample images"""
    detector = CashMateDetector()
    
    if not detector.model:
        print("❌ No trained model available. Please train a model first.")
        return
    
    print("🔍 CashMate Detector Test")
    print("=" * 50)
    
    # Test with sample image (if available)
    test_images = [
        "test_images/peso_sample.jpg",
        "test_images/100_peso.jpg",
        "test_images/500_peso.jpg"
    ]
    
    found_test_image = False
    for test_image in test_images:
        if os.path.exists(test_image):
            print(f"Testing with: {test_image}")
            
            result = detector.detect_peso_bills(test_image)
            
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Found {result['detection_count']} detections")
                for i, det in enumerate(result['detections']):
                    print(f"  {i+1}. {det['class_name']} - {det['confidence']:.2f} confidence")
                    if det.get('denomination'):
                        print(f"      Denomination: ₱{det['denomination']}")
            
            print()
            found_test_image = True
    
    if not found_test_image:
        print("No test images found. Place test images in 'test_images/' directory.")

def main():
    """Main function for testing"""
    if len(sys.argv) > 1:
        # Test with provided image
        image_path = sys.argv[1]
        if os.path.exists(image_path):
            detector = CashMateDetector()
            result = detector.detect_peso_bills(image_path)
            print(json.dumps(result, indent=2))
        else:
            print(f"Image not found: {image_path}")
    else:
        # Run test
        test_detector()

if __name__ == "__main__":
    main()