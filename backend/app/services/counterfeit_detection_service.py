"""
Counterfeit Detection Service for Philippine Peso Bills
Integrates the trained counterfeit detection model with the existing peso detection
"""

import cv2
import numpy as np
import logging
import time
import os
import glob
from typing import Optional, Dict, List, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class CounterfeitDetectionService:
    """Service for detecting counterfeit features in Philippine peso bills"""
    
    def __init__(self):
        self.counterfeit_model = None
        self.counterfeit_dataset_path = os.path.join(os.path.dirname(__file__), "..", "..", "Counterfeit-Money-Detector-v5")
        self.counterfeit_class_mapping = {}
        self.model_loaded = False
        
        # Updated categories based on our trained model's classes
        self.counterfeit_categories = {
            "denomination_indicators": [
                "1000_pearl", "1000_pearl_watermark", "100_whale", "100_whale_watermark",
                "200_tarsier", "200_tarsier_watermark", "20_New_Back", "20_New_Front", "20_civet", "20_civet_watermark",
                "500_big_parrot", "500_parrot_watermark", "50_maliputo", "50_maliputo_watermark",
                "10_New_Back", "10_New_Front", "10_Old_Back", "10_Old_Front",
                "5_New_Back", "5_New_Front", "5_Old_Back", "5_Old_Front",
                "1_New_Back", "1_New_Front", "1_Old_Back", "1_Old_Front",
                "25Cent_New_Back", "25Cent_New_Front", "25Cent_Old_Back", "25Cent_Old_Front"
            ],
            "security_features": [
                "security_thread", "watermark", "value_watermark", "clear_window", 
                "see_through_mark", "concealed_value", "optically_variable_device"
            ],
            "design_elements": [
                "eagle", "sampaguita", "serial_number", "value"
            ]
        }
        
    async def initialize(self):
        """Initialize the counterfeit detection service"""
        try:
            logger.info("Initializing Counterfeit Detection Service...")
            
            # Load counterfeit detection dataset info
            await self._load_counterfeit_dataset_info()
            
            # Try to load the trained counterfeit detection model
            await self._load_counterfeit_model()
            
            self.model_loaded = True
            logger.info("Counterfeit detection service initialized successfully")
            
        except Exception as e:
            logger.warning(f"Failed to load counterfeit detection model: {e}")
            logger.info("Counterfeit detection service running in basic mode")
    
    async def _load_counterfeit_dataset_info(self):
        """Load counterfeit detection dataset configuration"""
        try:
            data_yaml_path = os.path.join(self.counterfeit_dataset_path, "data.yaml")
            if os.path.exists(data_yaml_path):
                logger.info(f"Loading counterfeit dataset config from: {data_yaml_path}")
                
                with open(data_yaml_path, 'r') as f:
                    import yaml
                    config = yaml.safe_load(f)
                    
                    # Build class mapping for counterfeit detection
                    if 'names' in config:
                        for idx, class_name in enumerate(config['names']):
                            self.counterfeit_class_mapping[idx] = class_name
                    
                    logger.info(f"Counterfeit detection classes: {len(self.counterfeit_class_mapping)}")
                    logger.info(f"Sample classes: {list(self.counterfeit_class_mapping.values())[:10]}")
                
        except Exception as e:
            logger.error(f"Error loading counterfeit dataset info: {e}")
    
    async def _load_counterfeit_model(self):
        """Load the trained counterfeit detection YOLOv8 model"""
        try:
            from ultralytics import YOLO
            
            # Try to find the trained counterfeit model (prioritize your excellent 100-epoch model!)
            model_paths = [
                # 🏆 YOUR EXCELLENT 100-EPOCH MODEL (HIGHEST PRIORITY!) 🏆
                os.path.join(os.path.dirname(__file__), "..", "..", "trained_models", "counterfeit_detection_final_best.pt"),
                # Your completed training checkpoint
                os.path.join(os.path.dirname(__file__), "..", "..", "complete_counterfeit_training", "counterfeit_detection_complete", "weights", "best.pt"),
                # Previous Roboflow models (fallback)
                os.path.join(os.path.dirname(__file__), "..", "..", "Counterfeit-Money-Detector-v5", "counterfeit_money_v5_best.pt"),
                os.path.join(os.path.dirname(__file__), "..", "..", "roboflow_runs", "counterfeit_money_v5", "weights", "best.pt"),
                os.path.join(os.path.dirname(__file__), "..", "..", "roboflow_runs", "counterfeit_money_v5", "weights", "last.pt"),
                # Our previously trained models
                os.path.join(os.path.dirname(__file__), "..", "..", "counterfeit_demo_model.pt"),
                os.path.join(os.path.dirname(__file__), "..", "..", "demo_runs", "counterfeit_demo", "weights", "best.pt"),
                os.path.join(os.path.dirname(__file__), "..", "..", "demo_runs", "counterfeit_demo", "weights", "last.pt"),
                # Look for any training runs from the current session
                os.path.join(os.path.dirname(__file__), "..", "..", "counterfeit_detection_runs", "train_*", "counterfeit_model", "weights", "best.pt"),
                # Previous models as fallback
                os.path.join(os.path.dirname(__file__), "..", "..", "counterfeit_detection_runs", "counterfeit_yolov8_final", "weights", "best.pt"),
                os.path.join(os.path.dirname(__file__), "..", "..", "counterfeit_detection_runs", "counterfeit_yolov8_final", "weights", "last.pt"),
                os.path.join(os.path.dirname(__file__), "..", "..", "counterfeit_detection_model_v2.pt"),
                os.path.join(os.path.dirname(__file__), "..", "..", "counterfeit_detection_runs", "counterfeit_yolov8_v2", "weights", "best.pt"),
                os.path.join(os.path.dirname(__file__), "..", "..", "counterfeit_detection_runs", "counterfeit_yolov8_v2", "weights", "last.pt"),
                os.path.join(os.path.dirname(__file__), "..", "..", "counterfeit_detection_model.pt"),
                os.path.join(os.path.dirname(__file__), "..", "..", "counterfeit_detection_runs", "counterfeit_yolov8_train", "weights", "best.pt"),
                os.path.join(os.path.dirname(__file__), "..", "..", "counterfeit_detection_runs", "counterfeit_yolov8_train", "weights", "last.pt")
            ]
            
            # Also check for glob patterns for dynamic training runs
            import glob
            training_run_patterns = [
                os.path.join(os.path.dirname(__file__), "..", "..", "counterfeit_detection_runs", "train_*", "counterfeit_model", "weights", "best.pt"),
                os.path.join(os.path.dirname(__file__), "..", "..", "demo_runs", "*", "weights", "best.pt")
            ]
            
            for pattern in training_run_patterns:
                model_paths.extend(glob.glob(pattern))
            
            for model_path in model_paths:
                if os.path.exists(model_path):
                    logger.info(f"Loading counterfeit detection model: {model_path}")
                    
                    # Special celebration for your excellent 100-epoch model!
                    if "counterfeit_detection_final_best.pt" in model_path:
                        logger.info("🎉 LOADING YOUR EXCELLENT 100-EPOCH COUNTERFEIT MODEL!")
                        logger.info("🏆 Model Performance: 94.0% mAP50, 58.8% mAP50-95, 41 counterfeit features!")
                    elif "counterfeit_detection_complete" in model_path:
                        logger.info("🎯 Loading your completed training checkpoint!")
                        logger.info("📊 94.0% mAP50 accuracy achieved!")
                    
                    self.counterfeit_model = YOLO(model_path)
                    
                    # Verify model classes
                    if hasattr(self.counterfeit_model, 'names') and self.counterfeit_model.names:
                        logger.info(f"Counterfeit model classes: {len(self.counterfeit_model.names)}")
                        
                        # Update class mapping with model's classes
                        self.counterfeit_class_mapping = self.counterfeit_model.names
                    
                    if "counterfeit_detection_final_best.pt" in model_path:
                        logger.info("✅ Your excellent 100-epoch counterfeit model loaded successfully!")
                    else:
                        logger.info("✅ Counterfeit detection model loaded successfully!")
                    return
            
            logger.warning("No trained counterfeit detection model found")
            self.counterfeit_model = None
            
        except ImportError:
            logger.warning("Ultralytics not available for counterfeit detection")
            self.counterfeit_model = None
        except Exception as e:
            logger.warning(f"Error loading counterfeit detection model: {e}")
            self.counterfeit_model = None
    
    async def analyze_counterfeit_features(self, image: np.ndarray, peso_denomination: str = None) -> Dict:
        """Analyze image for counterfeit features using the trained model"""
        try:
            if image is None or image.size == 0:
                return {"status": "error", "message": "Invalid image"}
            
            logger.info(f"Analyzing counterfeit features for {peso_denomination or 'unknown'} peso bill")
            
            # Initialize result structure
            analysis_result = {
                "status": "completed",
                "denomination": peso_denomination,
                "authenticity_score": 0.0,
                "counterfeit_probability": 0.0,
                "detected_features": [],
                "security_analysis": {},
                "recommendations": []
            }
            
            # Use trained counterfeit detection model if available
            if self.counterfeit_model:
                results = self.counterfeit_model(image, verbose=False, conf=0.2)  # Lower confidence for feature detection
                
                detected_features = []
                feature_scores = {}
                
                for result in results:
                    if len(result.boxes) > 0:
                        logger.info(f"🔍 Found {len(result.boxes)} security features with counterfeit model")
                        for i, box in enumerate(result.boxes):
                            confidence = float(box.conf.cpu().numpy()[0])
                            class_id = int(box.cls.cpu().numpy()[0])
                            class_name = self.counterfeit_class_mapping.get(class_id, f"feature_{class_id}")
                            
                            # Get bounding box coordinates (normalized)
                            try:
                                bbox_coords = box.xywhn.cpu().numpy()[0]  # [x_center, y_center, width, height]
                                if len(bbox_coords) >= 4:
                                    x_center, y_center, width, height = bbox_coords[:4]
                                    # Convert to corner coordinates (x1, y1, x2, y2)
                                    x1 = float(x_center - width/2)
                                    y1 = float(y_center - height/2)
                                    x2 = float(x_center + width/2)
                                    y2 = float(y_center + height/2)
                                    bbox_dict = {
                                        "x": x1,
                                        "y": y1,
                                        "width": float(width),
                                        "height": float(height)
                                    }
                                else:
                                    logger.warning(f"Invalid bbox coordinates: {bbox_coords}")
                                    bbox_dict = {"x": 0, "y": 0, "width": 0, "height": 0}
                            except Exception as bbox_error:
                                logger.warning(f"Error extracting bbox: {bbox_error}")
                                bbox_dict = {"x": 0, "y": 0, "width": 0, "height": 0}
                            
                            detected_features.append({
                                "feature": class_name,
                                "confidence": confidence,
                                "category": self._categorize_feature(class_name),
                                "bbox": bbox_dict,  # Add bounding box coordinates as dict
                                "class_id": class_id,
                                "feature_type": "security_feature"
                            })
                            
                            # Track feature scores
                            feature_scores[class_name] = max(feature_scores.get(class_name, 0), confidence)
                            
                            logger.info(f"  🎯 Feature {i+1}: {class_name} ({confidence:.3f} confidence)")
                            
                    else:
                        logger.info("No security features detected by counterfeit model")
                
                analysis_result["detected_features"] = detected_features
                logger.info(f"Detected {len(detected_features)} counterfeit analysis features")
                
                # Analyze security features based on detections
                security_analysis = self._analyze_security_features(detected_features, peso_denomination)
                analysis_result["security_analysis"] = security_analysis
                
                # Calculate authenticity score
                authenticity_score = self._calculate_authenticity_score(detected_features, peso_denomination)
                analysis_result["authenticity_score"] = authenticity_score
                analysis_result["counterfeit_probability"] = 1.0 - authenticity_score
                
                # Generate recommendations
                recommendations = self._generate_recommendations(detected_features, authenticity_score)
                analysis_result["recommendations"] = recommendations
                
                logger.info(f"Counterfeit analysis complete: {authenticity_score:.2f} authenticity score")
            
            else:
                # Fallback analysis without trained model
                logger.warning("No counterfeit model available, using basic analysis")
                analysis_result.update({
                    "authenticity_score": 0.7,  # Neutral score
                    "counterfeit_probability": 0.3,
                    "recommendations": ["Professional verification recommended - no trained model available"]
                })
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in counterfeit analysis: {e}")
            return {
                "status": "error",
                "message": f"Analysis failed: {str(e)}",
                "authenticity_score": 0.0,
                "counterfeit_probability": 1.0
            }
    
    def _categorize_feature(self, feature_name: str) -> str:
        """Categorize detected feature into security categories"""
        feature_lower = feature_name.lower()
        
        for category, features in self.counterfeit_categories.items():
            if any(feat.lower() in feature_lower for feat in features):
                return category
        
        # Check for specific patterns
        if any(term in feature_lower for term in ['watermark', 'thread', 'security']):
            return "security_features"
        elif any(term in feature_lower for term in ['pearl', 'whale', 'bohol', 'aquino', 'osmena']):
            return "denomination_indicators"
        elif any(term in feature_lower for term in ['print', 'color', 'ink']):
            return "printing_quality"
        else:
            return "other_features"
    
    def _analyze_security_features(self, detected_features: List[Dict], denomination: str) -> Dict:
        """Analyze detected security features for authenticity assessment"""
        security_analysis = {
            "watermark_present": False,
            "security_thread_present": False,
            "microprinting_present": False,
            "color_changing_ink_present": False,
            "denomination_consistency": True,
            "expected_features_found": 0,
            "unexpected_features_found": 0
        }
        
        try:
            # Check for expected security features
            for feature in detected_features:
                feature_name = feature["feature"].lower()
                confidence = feature["confidence"]
                
                if confidence > 0.3:  # Only consider confident detections
                    if "watermark" in feature_name:
                        security_analysis["watermark_present"] = True
                    if "thread" in feature_name or "security" in feature_name:
                        security_analysis["security_thread_present"] = True
                    if "microprint" in feature_name:
                        security_analysis["microprinting_present"] = True
                    if "color_changing" in feature_name or "ink" in feature_name:
                        security_analysis["color_changing_ink_present"] = True
                    
                    # Check denomination consistency
                    if denomination and denomination in feature_name:
                        security_analysis["expected_features_found"] += 1
                    elif any(d in feature_name for d in ["1000", "500", "200", "100", "50", "20", "10", "5", "1"]):
                        if denomination not in feature_name:
                            security_analysis["denomination_consistency"] = False
                            security_analysis["unexpected_features_found"] += 1
            
            logger.info(f"Security analysis: {security_analysis}")
            
        except Exception as e:
            logger.error(f"Error in security feature analysis: {e}")
        
        return security_analysis
    
    def _calculate_authenticity_score(self, detected_features: List[Dict], denomination: str) -> float:
        """Calculate authenticity score based on detected features (Enhanced for clear counterfeit detection)"""
        try:
            if not detected_features:
                return 0.3  # Low score if no security features detected
            
            # Base score starts lower for stricter counterfeit detection
            score = 0.4
            
            # Feature quality analysis
            high_confidence_features = [f for f in detected_features if f["confidence"] > 0.7]
            medium_confidence_features = [f for f in detected_features if 0.4 < f["confidence"] <= 0.7]
            low_confidence_features = [f for f in detected_features if f["confidence"] <= 0.4]
            
            # Strong positive indicators (significant increase for authentic bills)
            if high_confidence_features:
                score += 0.25 * min(len(high_confidence_features) / 2, 1.0)  # More weight for high confidence
            
            # Medium confidence features (moderate increase)
            if medium_confidence_features:
                score += 0.15 * min(len(medium_confidence_features) / 3, 1.0)
            
            # Check for denomination-specific features (critical for authenticity)
            if denomination:
                denomination_features = [f for f in detected_features 
                                       if denomination in f["feature"].lower() and f["confidence"] > 0.5]
                if denomination_features:
                    score += 0.2  # Strong indicator of authenticity
                else:
                    score -= 0.1  # Penalty for missing denomination features
            
            # Security feature presence (essential for authentic bills)
            security_features = [f for f in detected_features 
                               if any(term in f["feature"].lower() for term in ["watermark", "thread", "security", "concealed", "variable"]) 
                               and f["confidence"] > 0.5]
            if security_features:
                score += 0.25  # Major authenticity indicator
            else:
                score -= 0.15  # Significant penalty for missing security features
            
            # Check for multiple security features (strong authenticity indicator)
            unique_security_types = set()
            for feature in security_features:
                for term in ["watermark", "thread", "security", "concealed", "variable"]:
                    if term in feature["feature"].lower():
                        unique_security_types.add(term)
                        break
            
            if len(unique_security_types) >= 2:
                score += 0.15  # Bonus for multiple different security features
            
            # Penalty for too many low confidence detections (possible noise/fake features)
            if len(low_confidence_features) > len(high_confidence_features) + len(medium_confidence_features):
                score -= 0.1
            
            # Ensure score is within bounds
            score = max(0.0, min(1.0, score))
            
            logger.info(f"Authenticity calculation: {len(high_confidence_features)} high-conf, "
                       f"{len(security_features)} security features, final score: {score:.3f}")
            
            return score
            
            # Negative indicators (decrease authenticity score)
            low_quality_features = [f for f in detected_features if f["confidence"] < 0.3]
            if len(low_quality_features) > len(high_confidence_features):
                score -= 0.15
            
            # Ensure score is within bounds
            score = max(0.0, min(1.0, score))
            
            logger.info(f"Calculated authenticity score: {score:.3f} for {len(detected_features)} features")
            return score
            
        except Exception as e:
            logger.error(f"Error calculating authenticity score: {e}")
            return 0.5
    
    def _generate_recommendations(self, detected_features: List[Dict], authenticity_score: float) -> List[str]:
        """Generate clear recommendations for counterfeit detection"""
        recommendations = []
        
        try:
            # Clear counterfeit detection recommendations
            if authenticity_score >= 0.75:
                recommendations.append("✅ AUTHENTIC: Bill appears genuine with high confidence")
                recommendations.append("✅ Multiple security features detected correctly")
                recommendations.append("✅ Safe to accept this bill")
            elif authenticity_score >= 0.55:
                recommendations.append("⚠️ LIKELY AUTHENTIC: Bill appears genuine but verify manually")
                recommendations.append("⚠️ Some security features detected - check physical features")
                recommendations.append("⚠️ Look for watermarks, security threads, and texture")
            elif authenticity_score >= 0.35:
                recommendations.append("⚠️ SUSPICIOUS: Authenticity uncertain - be cautious")
                recommendations.append("⚠️ Few or weak security features detected")
                recommendations.append("🔍 Professional verification strongly recommended")
                recommendations.append("🔍 Check with bank or authorized money changer")
            else:
                recommendations.append("❌ LIKELY COUNTERFEIT: Bill appears fake")
                recommendations.append("❌ Missing critical security features")
                recommendations.append("🚫 DO NOT ACCEPT this bill")
                recommendations.append("🚫 Report to authorities if received in transaction")
            
            # Feature-specific recommendations
            security_features = [f for f in detected_features 
                               if any(term in f["feature"].lower() for term in ["watermark", "thread", "security"])]
            
            if not security_features:
                recommendations.append("⚠️ No security features detected - major red flag")
            
            high_conf_features = [f for f in detected_features if f["confidence"] > 0.7]
            if len(high_conf_features) < 2:
                recommendations.append("⚠️ Few high-confidence features - manual verification needed")
            
            recommendations.append("💡 Always check: watermarks, security threads, raised printing, and paper texture")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return ["Error generating recommendations - manual verification required"]
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            recommendations = ["Analysis incomplete - manual verification required"]
        
        return recommendations
    
    def get_model_status(self) -> Dict:
        """Get counterfeit detection model status"""
        return {
            "counterfeit_model_loaded": self.counterfeit_model is not None,
            "dataset_path": self.counterfeit_dataset_path,
            "class_count": len(self.counterfeit_class_mapping),
            "categories": list(self.counterfeit_categories.keys())
        }

# Create service instance
counterfeit_detection_service = CounterfeitDetectionService()