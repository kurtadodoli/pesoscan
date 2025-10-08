#!/usr/bin/env python3
"""
Test the PesoScan system with real Philippine money images from the dataset
"""

import os
import cv2
import logging
from pathlib import Path
import random
import asyncio

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

async def test_detection_with_real_images():
    """Test detection service with real Philippine money images"""
    logger.info("🧪 Testing PesoScan with Real Philippine Money Images")
    logger.info("=" * 60)
    
    try:
        # Import the detection service
        import sys
        sys.path.append('.')
        from app.services.detection_service import detection_service
        
        # Initialize the detection service
        logger.info("🔧 Initializing detection service...")
        await detection_service.initialize()
        
        # Find real images from the dataset
        dataset_path = Path("Philippine-Money-1")
        test_images_path = dataset_path / "test" / "images"
        
        if not test_images_path.exists():
            logger.error(f"❌ Test images not found at: {test_images_path}")
            return
            
        # Get some test images
        image_files = list(test_images_path.glob("*.jpg")) + list(test_images_path.glob("*.png"))
        
        if not image_files:
            logger.error("❌ No image files found in test directory")
            return
            
        logger.info(f"📁 Found {len(image_files)} test images")
        
        # Test with 5 random images
        test_images = random.sample(image_files, min(5, len(image_files)))
        
        for i, image_path in enumerate(test_images, 1):
            logger.info(f"\n🖼️ Testing image {i}/{len(test_images)}: {image_path.name}")
            
            try:
                # Load image
                image = cv2.imread(str(image_path))
                if image is None:
                    logger.error(f"❌ Could not load image: {image_path}")
                    continue
                    
                logger.info(f"📐 Image size: {image.shape[1]}x{image.shape[0]}")
                
                # Process with detection service
                result = await detection_service.process_image(image)
                
                # Display results
                logger.info("📊 Detection Results:")
                logger.info(f"  Scan ID: {result.id}")
                logger.info(f"  Processing Time: {result.processing_time:.2f}s")
                logger.info(f"  Message: {result.message}")
                
                if result.result.detection:
                    detection = result.result.detection
                    logger.info(f"  🎯 Detection:")
                    logger.info(f"    Confidence: {detection.confidence:.1f}%")
                    logger.info(f"    Class: {detection.class_name}")
                    logger.info(f"    Bbox: {detection.bbox}")
                
                if result.result.result:
                    classification = result.result.result
                    logger.info(f"  🔍 Classification:")
                    logger.info(f"    Authentic: {'✅ Yes' if classification.authentic else '❌ No'}")
                    logger.info(f"    Confidence: {classification.confidence:.1f}%")
                    logger.info(f"    Denomination: {classification.denomination}")
                    
                    if classification.features:
                        features = classification.features
                        logger.info(f"  🔒 Security Features:")
                        logger.info(f"    Security Thread: {'✅' if features.security_thread else '❌'}")
                        logger.info(f"    Watermark: {'✅' if features.watermark else '❌'}")
                        logger.info(f"    Microprinting: {'✅' if features.microprinting else '❌'}")
                        logger.info(f"    Color-changing Ink: {'✅' if features.color_changing_ink else '❌'}")
                        logger.info(f"    UV Features: {'✅' if features.uv_features else '❌'}")
                        logger.info(f"    Raised Printing: {'✅' if features.raised_printing else '❌'}")
                
            except Exception as e:
                logger.error(f"❌ Error processing {image_path.name}: {e}")
                
        logger.info(f"\n🎉 Testing completed!")
        
    except Exception as e:
        logger.error(f"❌ Error in testing: {e}")
        import traceback
        traceback.print_exc()

async def test_api_endpoints():
    """Test the API endpoints"""
    logger.info("\n🌐 Testing API Endpoints")
    logger.info("=" * 40)
    
    try:
        import requests
        import time
        
        base_url = "http://localhost:8000"
        
        # Test health endpoint
        logger.info("🏥 Testing health endpoint...")
        response = requests.get(f"{base_url}/api/health", timeout=5)
        
        if response.status_code == 200:
            health_data = response.json()
            logger.info(f"✅ Health check passed")
            logger.info(f"  Status: {health_data.get('status')}")
            logger.info(f"  Uptime: {health_data.get('uptime', 0):.1f}s")
            logger.info(f"  Models: {health_data.get('models_loaded', {})}")
        else:
            logger.error(f"❌ Health check failed: {response.status_code}")
            
        # Test with a real image
        dataset_path = Path("Philippine-Money-1")
        test_images_path = dataset_path / "test" / "images"
        
        if test_images_path.exists():
            image_files = list(test_images_path.glob("*.jpg"))[:1]  # Just one image
            
            if image_files:
                image_path = image_files[0]
                logger.info(f"📸 Testing scan endpoint with: {image_path.name}")
                
                with open(image_path, 'rb') as f:
                    files = {'file': (image_path.name, f, 'image/jpeg')}
                    response = requests.post(f"{base_url}/api/scan", files=files, timeout=30)
                
                if response.status_code == 200:
                    scan_data = response.json()
                    logger.info(f"✅ Scan API test passed")
                    logger.info(f"  Scan ID: {scan_data.get('id')}")
                    logger.info(f"  Processing Time: {scan_data.get('processing_time', 0):.2f}s")
                else:
                    logger.error(f"❌ Scan API test failed: {response.status_code}")
                    logger.error(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        logger.warning("⚠️ API server not running. Start the backend server to test API endpoints.")
    except Exception as e:
        logger.error(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    logger.info("🚀 Starting PesoScan Testing...")
    
    # Run async tests
    asyncio.run(test_detection_with_real_images())
    
    # Test API endpoints
    asyncio.run(test_api_endpoints())
    
    logger.info("\n🏁 Testing completed!")