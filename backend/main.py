"""
PesoScan Backend API
Main FastAPI application for Philippine peso bill counterfeit detection
"""

import time
import logging
import os
import sys
from datetime import datetime
import numpy as np
import cv2

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def convert_numpy_types(obj):
    """Convert numpy types to native Python types for JSON serialization"""
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    return obj

try:
    from fastapi import FastAPI, File, UploadFile, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse, FileResponse
    import uvicorn
    import random
    import glob
    FASTAPI_AVAILABLE = True
except ImportError:
    print("FastAPI not installed. This is a demo version.")
    FASTAPI_AVAILABLE = False

from app.core.config import settings
from app.services.enhanced_detection_service import enhanced_detection_service
from app.services.counterfeit_detection_service import counterfeit_detection_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

if FASTAPI_AVAILABLE:
    # Initialize FastAPI app
    app = FastAPI(
        title="PesoScan API",
        description="AI-powered counterfeit detection for Philippine peso bills",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for development
        allow_credentials=True,
        allow_methods=["*"],  # Allow all methods
        allow_headers=["*"],  # Allow all headers
    )

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Global exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error", "detail": str(exc)}
        )

    @app.get("/", response_model=dict)
    async def root():
        """Root endpoint with API information"""
        return {
            "message": "PesoScan API",
            "version": "1.0.0",
            "description": "AI-powered counterfeit detection for Philippine peso bills",
            "docs": "/docs",
            "health": "/api/health"
        }

    @app.get("/api/health")
    async def health_check():
        """Health check endpoint"""
        try:
            model_status = enhanced_detection_service.get_model_status()
            uptime = enhanced_detection_service.get_uptime()
            
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "version": settings.VERSION,
                "models_loaded": {
                    "yolo": model_status.get("yolo_loaded", True),
                    "cnn": model_status.get("cnn_loaded", True)
                },
                "uptime": uptime
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

    @app.post("/api/scan")
    async def scan_peso_bill(file: UploadFile = File(...)):
        """Scan peso bill from camera capture"""
        try:
            logger.info(f"Processing scan request: {file.filename}")
            logger.info(f"Content type: {file.content_type}")
            
            # Read image data first to validate it's actually an image
            image_data = await file.read()
            
            if len(image_data) == 0:
                raise HTTPException(status_code=400, detail="Empty file uploaded")
            
            # Convert to OpenCV format
            import numpy as np
            import cv2
            
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            
            # Decode image - this will fail if it's not a valid image
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                raise HTTPException(status_code=400, detail="Could not decode image. Please upload a valid image file.")
            
            logger.info(f"Image decoded successfully: {image.shape}")
            
            # Process with enhanced detection service
            result = await enhanced_detection_service.process_image(image)
            
            # Get peso denomination for counterfeit analysis
            peso_denomination = None
            if result.result.detection:
                peso_denomination = result.result.detection.class_name
            
            # Run counterfeit detection to get security features
            counterfeit_analysis = await counterfeit_detection_service.analyze_counterfeit_features(
                image, peso_denomination
            )
            
            # Convert result to dict for JSON response
            response_data = {
                "id": result.id,
                "timestamp": result.timestamp.isoformat(),
                "result": {
                    "detection": None,
                    "result": {
                        "authentic": result.result.result.authentic,
                        "confidence": float(result.result.result.confidence),  # Convert numpy types
                        "denomination": result.result.result.denomination,
                        "series_year": getattr(result.result.result, 'series_year', '2022'),
                        "features": {
                            "security_thread": result.result.result.features.security_thread,
                            "watermark": result.result.result.features.watermark,
                            "microprinting": result.result.result.features.microprinting,
                            "color_changing_ink": result.result.result.features.color_changing_ink,
                            "uv_features": result.result.result.features.uv_features,
                            "raised_printing": result.result.result.features.raised_printing
                        }
                    }
                },
                "processing_time": float(result.processing_time),  # Convert numpy types
                "message": result.message
            }
            
            # Add detection info if available
            if result.result.detection:
                response_data["result"]["detection"] = {
                    "bbox": convert_numpy_types(result.result.detection.bbox),  # Convert numpy array
                    "confidence": float(result.result.detection.confidence),  # Convert numpy float
                    "class_name": result.result.detection.class_name
                }
            
            # Add counterfeit analysis with security features
            response_data["counterfeit_analysis"] = convert_numpy_types(counterfeit_analysis)
            
            # Add security features to detections for bounding box visualization
            if counterfeit_analysis.get("detected_features"):
                response_data["result"]["all_detections"] = [
                    {
                        "type": "peso",
                        "class_name": result.result.detection.class_name if result.result.detection else "unknown",
                        "confidence": float(result.result.detection.confidence) if result.result.detection else 0.0,
                        "bbox": convert_numpy_types(result.result.detection.bbox) if result.result.detection else None
                    }
                ] if result.result.detection else []
                
                # Add security features
                for feature in counterfeit_analysis["detected_features"]:
                    response_data["result"]["all_detections"].append({
                        "type": "security",
                        "class_name": feature.get("feature", "unknown"),
                        "confidence": float(feature.get("confidence", 0.0)),
                        "bbox": feature.get("bbox", {"x": 0, "y": 0, "width": 0, "height": 0}),
                        "category": feature.get("category", "unknown")
                    })
            
            # Apply numpy conversion to entire response
            response_data = convert_numpy_types(response_data)
            
            return response_data
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in scan endpoint: {e}")
            raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

    @app.post("/api/upload")
    async def upload_peso_bill(file: UploadFile = File(...)):
        """Upload and analyze peso bill image"""
        # Use the same implementation as scan
        return await scan_peso_bill(file)

    @app.get("/api/sample-bills")
    async def get_sample_bills():
        """Get sample bill images from the dataset"""
        try:
            dataset_path = os.path.join(os.path.dirname(__file__), "Philippine-Money-1", "test", "images")
            
            # Get all image files
            image_files = glob.glob(os.path.join(dataset_path, "*.jpg"))
            
            if not image_files:
                return {"samples": []}
            
            # Get a random selection of images (max 6 for showcase)
            selected_images = random.sample(image_files, min(6, len(image_files)))
            
            samples = []
            for img_path in selected_images:
                filename = os.path.basename(img_path)
                samples.append({
                    "filename": filename,
                    "url": f"/api/images/{filename}"
                })
            
            return {"samples": samples}
            
        except Exception as e:
            logger.error(f"Error getting sample bills: {e}")
            raise HTTPException(status_code=500, detail=f"Error loading sample bills: {str(e)}")

    @app.get("/api/images/{filename}")
    async def get_image(filename: str):
        """Serve images from the dataset"""
        try:
            dataset_path = os.path.join(os.path.dirname(__file__), "Philippine-Money-1", "test", "images")
            image_path = os.path.join(dataset_path, filename)
            
            if not os.path.exists(image_path):
                raise HTTPException(status_code=404, detail="Image not found")
            
            return FileResponse(image_path)
            
        except Exception as e:
            logger.error(f"Error serving image {filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Error serving image: {str(e)}")

    @app.post("/api/analyze-counterfeit")
    async def analyze_counterfeit(file: UploadFile = File(...)):
        """Analyze uploaded image for counterfeit features"""
        try:
            logger.info(f"Processing counterfeit analysis request: {file.filename}")
            
            # Read and process image
            contents = await file.read()
            nparr = np.frombuffer(contents, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                raise HTTPException(status_code=400, detail="Invalid image format")
            
            # First detect the peso denomination
            peso_detection = await enhanced_detection_service.detect_peso_bill(image)
            peso_denomination = peso_detection.class_name if peso_detection else None
            
            # Analyze counterfeit features
            counterfeit_analysis = await counterfeit_detection_service.analyze_counterfeit_features(
                image, peso_denomination
            )
            
            # Combine results
            result = {
                "peso_detection": {
                    "detected": peso_detection is not None,
                    "denomination": peso_denomination,
                    "confidence": peso_detection.confidence if peso_detection else 0.0
                },
                "counterfeit_analysis": convert_numpy_types(counterfeit_analysis),
                "timestamp": datetime.now().isoformat(),
                "filename": file.filename
            }
            
            logger.info(f"Counterfeit analysis completed for {peso_denomination or 'unknown'} peso")
            return result
            
        except Exception as e:
            logger.error(f"Error in counterfeit analysis: {e}")
            raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

    @app.get("/api/counterfeit-model-status")
    async def get_counterfeit_model_status():
        """Get counterfeit detection model status"""
        try:
            model_status = counterfeit_detection_service.get_model_status()
            enhanced_status = enhanced_detection_service.get_model_status()
            
            return {
                "peso_detection": convert_numpy_types(enhanced_status),
                "counterfeit_detection": convert_numpy_types(model_status),
                "timestamp": datetime.now().isoformat(),
                "status": "operational" if model_status.get("counterfeit_model_loaded") else "limited"
            }
            
        except Exception as e:
            logger.error(f"Error getting model status: {e}")
            raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")

    @app.post("/api/comprehensive-scan")
    async def comprehensive_scan(file: UploadFile = File(...)):
        """Comprehensive scan combining peso detection and counterfeit analysis"""
        try:
            logger.info(f"Processing comprehensive scan request: {file.filename}")
            
            # Read and process image
            contents = await file.read()
            nparr = np.frombuffer(contents, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                raise HTTPException(status_code=400, detail="Invalid image format")
            
            # Run peso detection
            scan_response = await enhanced_detection_service.process_image(image)
            
            # Extract peso denomination for counterfeit analysis
            peso_denomination = None
            if scan_response.result and scan_response.result.detection:
                peso_denomination = scan_response.result.detection.class_name
            
            # Run counterfeit analysis using both models
            counterfeit_analysis = await counterfeit_detection_service.analyze_counterfeit_features(
                image, peso_denomination
            )
            
            # Get all detections from both peso detection and counterfeit analysis
            peso_detections = scan_response.result.detections if scan_response.result else []
            counterfeit_detections = counterfeit_analysis.get("detected_features", [])
            
            # Combine and enhance results with proper bounding boxes
            comprehensive_result = {
                "scan_id": scan_response.id,
                "timestamp": scan_response.timestamp.isoformat(),
                "peso_scan": convert_numpy_types(scan_response.to_dict()),
                "counterfeit_analysis": convert_numpy_types(counterfeit_analysis),
                "overall_assessment": {
                    "peso_detected": scan_response.result.detection is not None,
                    "denomination": peso_denomination,
                    "authenticity_score": counterfeit_analysis.get("authenticity_score", 0.0),
                    "counterfeit_probability": counterfeit_analysis.get("counterfeit_probability", 1.0),
                    "recommendation": _get_overall_recommendation(scan_response, counterfeit_analysis),
                    "total_features_detected": len(peso_detections) + len(counterfeit_detections),
                    "model_info": {
                        "peso_model_accuracy": "94.0% mAP50",
                        "counterfeit_model_accuracy": "94.0% mAP50", 
                        "peso_classes": 9,
                        "counterfeit_classes": 41,
                        "training_epochs": 100
                    }
                },
                "processing_time": scan_response.processing_time,
                "filename": file.filename,
                "combined_detections": {
                    "peso_features": [
                        {
                            "feature_name": d.class_name,
                            "confidence": float(d.confidence),
                            "bbox": {
                                "x": float(d.bbox[0]) if hasattr(d, 'bbox') and len(d.bbox) >= 4 else 0.0,
                                "y": float(d.bbox[1]) if hasattr(d, 'bbox') and len(d.bbox) >= 4 else 0.0,
                                "width": float(d.bbox[2] - d.bbox[0]) if hasattr(d, 'bbox') and len(d.bbox) >= 4 else 0.0,
                                "height": float(d.bbox[3] - d.bbox[1]) if hasattr(d, 'bbox') and len(d.bbox) >= 4 else 0.0
                            },
                            "model_source": "peso_model"
                        } for d in peso_detections
                    ] if peso_detections else [],
                    "security_features": [
                        {
                            "feature_name": sf.get("feature", "unknown"),
                            "confidence": float(sf.get("confidence", 0.0)),
                            "bbox": sf.get("bbox", {"x": 0, "y": 0, "width": 0, "height": 0}),
                            "model_source": "security_model"
                        } for sf in counterfeit_detections
                    ],
                    "total_count": len(peso_detections) + len(counterfeit_detections),
                    "model_info": {
                        "peso_model": "philippine_money_final_best.pt",
                        "security_model": "counterfeit_detection_final_best.pt"
                    }
                }
            }
            
            logger.info(f"Comprehensive scan completed for {file.filename}")
            return comprehensive_result
            
        except Exception as e:
            logger.error(f"Error in comprehensive scan: {e}")
            raise HTTPException(status_code=500, detail=f"Comprehensive scan failed: {str(e)}")

    def _get_overall_recommendation(scan_response, counterfeit_analysis):
        """Generate clear overall recommendation for counterfeit detection"""
        try:
            peso_detected = scan_response.result.detection is not None
            authenticity_score = counterfeit_analysis.get("authenticity_score", 0.0)
            counterfeit_probability = counterfeit_analysis.get("counterfeit_probability", 1.0)
            
            if not peso_detected:
                return "❌ NOT A PESO BILL - Object not recognized as Philippine currency"
            elif authenticity_score >= 0.75:
                return "✅ AUTHENTIC BILL - Safe to accept (High confidence)"
            elif authenticity_score >= 0.55:
                return "⚠️ LIKELY AUTHENTIC - Verify security features manually"
            elif authenticity_score >= 0.35:
                return "⚠️ SUSPICIOUS - Professional verification required"
            else:
                return "❌ LIKELY COUNTERFEIT - Do not accept this bill"
                
        except Exception:
            return "🔍 ANALYSIS INCOMPLETE - Manual verification required"

    @app.on_event("startup")
    async def startup_event():
        """Initialize services on startup"""
        logger.info("Starting PesoScan API...")
        try:
            await enhanced_detection_service.initialize()
            logger.info("Enhanced detection service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize detection service: {e}")
        
        try:
            await counterfeit_detection_service.initialize()
            logger.info("Counterfeit detection service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize counterfeit detection service: {e}")
        
        logger.info("PesoScan API started successfully")

    @app.on_event("shutdown")
    async def shutdown_event():
        """Cleanup on shutdown"""
        logger.info("Shutting down PesoScan API...")

    if __name__ == "__main__":
        import asyncio
        uvicorn.run(
            "main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            log_level="info"
        )

else:
    # Fallback for when FastAPI is not available
    print("FastAPI not available. Please install requirements:")
    print("pip install -r requirements.txt")
    
    if __name__ == "__main__":
        print("Demo mode - FastAPI server not started")
        print("Install FastAPI and dependencies to run the server")
        
        # Show configuration
        print(f"\nConfiguration:")
        print(f"Host: {settings.HOST}")
        print(f"Port: {settings.PORT}")
        print(f"Debug: {settings.DEBUG}")
        print(f"Allowed Origins: {settings.ALLOWED_ORIGINS}")
# CashMate Integration
try:
    from cashmate_api import create_cashmate_routes
    create_cashmate_routes(app)
    print("✅ CashMate detector integrated successfully")
except ImportError as e:
    print(f"⚠️ CashMate integration failed: {e}")
except Exception as e:
    print(f"❌ CashMate integration error: {e}")
