#!/usr/bin/env python3
"""
Test script to verify comprehensive scan functionality
"""

import sys
import os
import asyncio
import logging
import numpy as np
import cv2

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_comprehensive_scan():
    """Test the comprehensive scan functionality"""
    try:
        # Import the services
        from app.services.counterfeit_detection_service import CounterfeitDetectionService
        from app.services.detection_service import DetectionService
        
        logger.info("=" * 60)
        logger.info("COMPREHENSIVE SCAN TEST")
        logger.info("=" * 60)
        
        # Initialize both services
        logger.info("Initializing services...")
        counterfeit_service = CounterfeitDetectionService()
        peso_service = DetectionService()
        
        await counterfeit_service.initialize()
        await peso_service.initialize()
        
        # Create a dummy test image (you can replace this with an actual peso image)
        logger.info("Creating test image...")
        test_image = np.ones((480, 640, 3), dtype=np.uint8) * 128  # Gray test image
        
        # Test peso detection
        logger.info("Testing peso detection...")
        peso_results = await peso_service.detect_peso_denomination(test_image)
        logger.info(f"Peso detection result: {peso_results.get('status', 'unknown')}")
        
        # Test counterfeit analysis
        logger.info("Testing counterfeit analysis...")
        if counterfeit_service.model_loaded:
            counterfeit_results = await counterfeit_service.analyze_counterfeit_features(
                test_image, 
                peso_denomination="1000"  # Test with 1000 peso bill
            )
            logger.info(f"Counterfeit analysis result: {counterfeit_results.get('status', 'unknown')}")
            logger.info(f"Authenticity score: {counterfeit_results.get('authenticity_score', 0)}")
            logger.info(f"Detected features: {len(counterfeit_results.get('detected_features', []))}")
            
            # Simulate comprehensive scan result
            logger.info("\n" + "=" * 40)
            logger.info("COMPREHENSIVE SCAN RESULT")
            logger.info("=" * 40)
            
            comprehensive_result = {
                "status": "completed",
                "scan_type": "comprehensive",
                "peso_detection": peso_results,
                "counterfeit_analysis": counterfeit_results,
                "final_verdict": {
                    "is_authentic": counterfeit_results.get('authenticity_score', 0) > 0.7,
                    "confidence": min(
                        peso_results.get('confidence_score', 0),
                        counterfeit_results.get('authenticity_score', 0)
                    ),
                    "detected_denomination": peso_results.get('denomination', 'unknown'),
                    "security_features_passed": len([
                        f for f in counterfeit_results.get('detected_features', [])
                        if f.get('confidence', 0) > 0.5
                    ])
                }
            }
            
            logger.info(f"✅ Final Verdict: {'AUTHENTIC' if comprehensive_result['final_verdict']['is_authentic'] else 'SUSPICIOUS'}")
            logger.info(f"✅ Denomination: {comprehensive_result['final_verdict']['detected_denomination']}")
            logger.info(f"✅ Security Features: {comprehensive_result['final_verdict']['security_features_passed']}")
            logger.info(f"✅ Overall Confidence: {comprehensive_result['final_verdict']['confidence']:.2f}")
            
            return True
        else:
            logger.error("❌ Counterfeit service not properly loaded")
            return False
            
    except Exception as e:
        logger.error(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_comprehensive_scan())