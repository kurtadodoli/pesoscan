"""
Health check API routes
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging
import time

from app.services.detection_service import detection_service
from app.core.config import settings
from app.models.scan_models import HealthResponse

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Returns service status, uptime, and model loading status
    """
    try:
        # Get model status
        model_status = detection_service.get_model_status()
        
        # Get uptime
        uptime = detection_service.get_uptime()
        
        # Determine overall status
        status = "healthy" if model_status.get("overall_status", False) else "degraded"
        
        # Create health response
        health_response = HealthResponse(
            status=status,
            timestamp=datetime.now(),
            version=settings.VERSION,
            models_loaded={
                "yolo": model_status.get("yolo_loaded", False),
                "cnn": model_status.get("cnn_loaded", False)
            },
            uptime=uptime
        )
        
        return health_response.to_dict()
        
    except Exception as e:
        logger.error(f"Health check error: {e}")
        
        # Return degraded status
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "version": settings.VERSION,
            "models_loaded": {
                "yolo": False,
                "cnn": False
            },
            "uptime": 0.0,
            "error": str(e)
        }

@router.get("/ping")
async def ping():
    """
    Simple ping endpoint for load balancer health checks
    """
    return {"message": "pong", "timestamp": datetime.now().isoformat()}

@router.get("/version")
async def get_version():
    """
    Get API version information
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "timestamp": datetime.now().isoformat()
    }