#!/usr/bin/env python3
"""
Test script to verify counterfeit model loading
"""

import os
import sys
import asyncio
import logging

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_counterfeit_model_loading():
    """Test loading the counterfeit detection model"""
    try:
        # Import the counterfeit detection service
        from app.services.counterfeit_detection_service import CounterfeitDetectionService
        
        logger.info("Creating CounterfeitDetectionService instance...")
        service = CounterfeitDetectionService()
        
        logger.info("Initializing counterfeit detection service...")
        await service.initialize()
        
        if service.model_loaded and service.counterfeit_model:
            logger.info("✅ SUCCESS: Counterfeit model loaded successfully!")
            logger.info(f"Model classes: {len(service.counterfeit_class_mapping)}")
            logger.info(f"Sample classes: {list(service.counterfeit_class_mapping.values())[:10]}")
            return True
        else:
            logger.error("❌ FAILED: Counterfeit model not loaded")
            return False
            
    except Exception as e:
        logger.error(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

async def check_model_files():
    """Check which model files exist"""
    logger.info("Checking for available model files...")
    
    model_paths = [
        "counterfeit_detection_runs/counterfeit_yolov8_final/weights/best.pt",
        "counterfeit_detection_runs/counterfeit_yolov8_train/weights/best.pt", 
        "counterfeit_detection_runs/counterfeit_resilient/weights/best.pt",
        "counterfeit_demo_model.pt"
    ]
    
    found_models = []
    for model_path in model_paths:
        full_path = os.path.join(os.path.dirname(__file__), model_path)
        if os.path.exists(full_path):
            size_mb = os.path.getsize(full_path) / (1024 * 1024)
            logger.info(f"✅ Found: {model_path} ({size_mb:.1f} MB)")
            found_models.append(full_path)
        else:
            logger.info(f"❌ Missing: {model_path}")
    
    return found_models

if __name__ == "__main__":
    async def main():
        logger.info("=" * 60)
        logger.info("COUNTERFEIT MODEL LOADING TEST")
        logger.info("=" * 60)
        
        # First check which model files exist
        found_models = await check_model_files()
        logger.info(f"Found {len(found_models)} model files")
        
        # Then test loading the service
        success = await test_counterfeit_model_loading()
        
        if success:
            logger.info("✅ RESULT: Counterfeit detection is working!")
        else:
            logger.info("❌ RESULT: Counterfeit detection needs fixing")
    
    asyncio.run(main())