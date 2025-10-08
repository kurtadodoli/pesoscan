"""
API routes for peso bill scanning
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import logging
from typing import Optional
import time

from app.services.enhanced_detection_service import enhanced_detection_service
from app.services.counterfeit_detection_service import counterfeit_detection_service
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

async def validate_image(file: UploadFile) -> np.ndarray:
    """Validate and process uploaded image file"""
    try:
        # Check file size
        if hasattr(file, 'size') and file.size > settings.MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {settings.MAX_IMAGE_SIZE / 1024 / 1024:.1f}MB"
            )
        
        # Check file format
        if file.content_type not in ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp']:
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Supported: JPEG, PNG, BMP"
            )
        
        # Read image data
        image_data = await file.read()
        
        # Convert to OpenCV format
        nparr = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(
                status_code=400,
                detail="Could not decode image. Please check file format."
            )
        
        # Convert BGR to RGB (OpenCV uses BGR by default)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        return image
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating image: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Error processing image: {str(e)}"
        )

@router.post("/scan")
async def scan_peso_bill(file: UploadFile = File(...)):
    """
    Scan peso bill from camera capture
    
    - **file**: Image file from camera capture
    - Returns scan result with authenticity classification
    """
    try:
        logger.info(f"Processing scan request: {file.filename}")
        
        # Validate and process image
        image = await validate_image(file)
        
        # Process image through detection pipeline
        result = await enhanced_detection_service.process_image(image)
        
        # Return result as dictionary
        return result.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in scan endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/upload")
async def upload_peso_bill(file: UploadFile = File(...)):
    """
    Analyze uploaded peso bill image
    
    - **file**: Uploaded image file
    - Returns scan result with authenticity classification
    """
    try:
        logger.info(f"Processing upload request: {file.filename}")
        
        # Validate and process image
        image = await validate_image(file)
        
        # Process image through detection pipeline
        result = await enhanced_detection_service.process_image(image)
        
        # Return result as dictionary
        return result.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in upload endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/comprehensive")
async def comprehensive_scan(file: UploadFile = File(...)):
    """
    Comprehensive peso bill analysis with advanced counterfeit detection
    
    - **file**: Image file for analysis
    - Returns detailed counterfeit analysis with security features
    """
    try:
        logger.info(f"🔍 Processing comprehensive scan: {file.filename}")
        
        # Validate and process image
        image = await validate_image(file)
        
        # Step 1: Enhanced peso detection with multiple security features
        logger.info("🎯 Step 1: Detecting peso features...")
        peso_result = await enhanced_detection_service.process_image(image)
        
        # Step 2: Advanced counterfeit analysis
        logger.info("🛡️ Step 2: Analyzing counterfeit features...")
        denomination = peso_result.result.denomination if peso_result.result else None
        counterfeit_analysis = await counterfeit_detection_service.analyze_counterfeit_features(image, denomination)
        
        # Step 3: Combine results for comprehensive assessment
        logger.info("📊 Step 3: Generating comprehensive assessment...")
        
        # Calculate overall authenticity based on both analyses
        peso_confidence = peso_result.result.confidence if peso_result.result else 0.0
        counterfeit_score = counterfeit_analysis.get("authenticity_score", 0.0)
        
        # Weighted combination (counterfeit analysis gets more weight for authenticity)
        overall_authenticity = (counterfeit_score * 0.7) + (peso_confidence / 100.0 * 0.3)
        overall_counterfeit_prob = 1.0 - overall_authenticity
        
        # Determine final recommendation
        if overall_authenticity >= 0.75:
            recommendation = "✅ AUTHENTIC - Bill appears genuine with high confidence"
        elif overall_authenticity >= 0.55:
            recommendation = "⚠️ LIKELY AUTHENTIC - Bill appears genuine but verify security features"
        elif overall_authenticity >= 0.35:
            recommendation = "⚠️ SUSPICIOUS - Authenticity uncertain, professional verification recommended"
        else:
            recommendation = "❌ LIKELY COUNTERFEIT - Bill appears fake, do not accept"
        
        # Build comprehensive response
        comprehensive_result = {
            "id": peso_result.id,
            "timestamp": peso_result.timestamp.isoformat(),
            "processing_time": peso_result.processing_time + 0.5,  # Add counterfeit analysis time
            
            # Overall Assessment
            "overall_assessment": {
                "authenticity_score": overall_authenticity,
                "counterfeit_probability": overall_counterfeit_prob,
                "denomination": denomination,
                "recommendation": recommendation,
                "confidence_level": "High" if overall_authenticity > 0.7 or overall_authenticity < 0.3 else "Medium"
            },
            
            # Detailed Counterfeit Analysis
            "counterfeit_analysis": counterfeit_analysis,
            
            # Original Peso Scan Results
            "peso_scan": peso_result.to_dict(),
            
            # Enhanced Security Analysis
            "security_summary": {
                "total_features_detected": len(peso_result.result.detections) if peso_result.result.detections else 0,
                "high_confidence_features": len([d for d in peso_result.result.detections if d.confidence > 0.7]) if peso_result.result.detections else 0,
                "security_features_found": len(counterfeit_analysis.get("detected_features", [])),
                "authenticity_indicators": _count_authenticity_indicators(counterfeit_analysis),
                "risk_factors": _count_risk_factors(counterfeit_analysis, overall_authenticity)
            }
        }
        
        logger.info(f"🎉 Comprehensive analysis complete: {overall_authenticity:.3f} authenticity score")
        return comprehensive_result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in comprehensive scan: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Comprehensive analysis failed: {str(e)}"
        )

def _count_authenticity_indicators(counterfeit_analysis: dict) -> int:
    """Count positive authenticity indicators"""
    indicators = 0
    security_analysis = counterfeit_analysis.get("security_analysis", {})
    
    if security_analysis.get("watermark_present"): indicators += 1
    if security_analysis.get("security_thread_present"): indicators += 1
    if security_analysis.get("denomination_consistency"): indicators += 1
    if security_analysis.get("expected_features_found", 0) > 0: indicators += 1
    
    return indicators

def _count_risk_factors(counterfeit_analysis: dict, authenticity_score: float) -> int:
    """Count counterfeit risk factors"""
    risk_factors = 0
    security_analysis = counterfeit_analysis.get("security_analysis", {})
    
    if not security_analysis.get("watermark_present"): risk_factors += 1
    if not security_analysis.get("security_thread_present"): risk_factors += 1
    if not security_analysis.get("denomination_consistency"): risk_factors += 1
    if security_analysis.get("unexpected_features_found", 0) > 0: risk_factors += 1
    if authenticity_score < 0.5: risk_factors += 1
    
    return risk_factors

@router.get("/history")
async def get_scan_history(limit: int = 20, offset: int = 0):
    """
    Get scan history (placeholder implementation)
    
    - **limit**: Number of records to return
    - **offset**: Offset for pagination
    """
    try:
        # In production, this would query a database
        # For demo, return empty history
        return {
            "items": [],
            "total": 0,
            "page": offset // limit + 1 if limit > 0 else 1,
            "limit": limit,
            "message": "History feature coming soon"
        }
        
    except Exception as e:
        logger.error(f"Error retrieving history: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving history: {str(e)}"
        )

@router.get("/scans/{scan_id}")
async def get_scan_by_id(scan_id: str):
    """
    Get specific scan result by ID (placeholder implementation)
    
    - **scan_id**: Unique scan identifier
    """
    try:
        # In production, this would query a database
        raise HTTPException(
            status_code=404,
            detail="Scan not found. History storage not implemented in demo."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving scan {scan_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving scan: {str(e)}"
        )

@router.delete("/scans/{scan_id}")
async def delete_scan(scan_id: str):
    """
    Delete scan from history (placeholder implementation)
    
    - **scan_id**: Unique scan identifier
    """
    try:
        # In production, this would delete from database
        raise HTTPException(
            status_code=404,
            detail="Scan not found. History storage not implemented in demo."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting scan {scan_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting scan: {str(e)}"
        )

@router.get("/stats")
async def get_system_stats():
    """
    Get system statistics (placeholder implementation)
    """
    try:
        uptime = enhanced_detection_service.get_uptime()
        
        return {
            "total_scans": 0,
            "authentic_count": 0,
            "counterfeit_count": 0,
            "average_confidence": 0.0,
            "uptime": uptime,
            "last_scan": None,
            "message": "Statistics feature coming soon"
        }
        
    except Exception as e:
        logger.error(f"Error retrieving stats: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving statistics: {str(e)}"
        )