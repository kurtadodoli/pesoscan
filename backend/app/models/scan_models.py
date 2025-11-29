"""
Data models for scan requests and responses
"""

from typing import Optional, Dict, List, Any
from datetime import datetime
import json

class ScanRequest:
    """Request model for peso bill scanning"""
    def __init__(self):
        pass

class DetectionResult:
    """Object detection result from YOLOv8"""
    def __init__(self, bbox: List[float], confidence: float, class_name: str, feature_name: Optional[str] = None):
        self.bbox = bbox  # [x1, y1, x2, y2]
        self.confidence = confidence
        self.class_name = class_name
        self.feature_name = feature_name  # Detailed feature name for security features
    
    def to_dict(self):
        return {
            "bbox": self.bbox,
            "confidence": self.confidence,
            "class_name": self.class_name,
            "feature_name": self.feature_name
        }

class SecurityFeatures:
    """Security features analysis result"""
    def __init__(self, security_thread: bool = False, watermark: bool = False, 
                 microprinting: bool = False, color_changing_ink: bool = False,
                 uv_features: Optional[bool] = None, raised_printing: Optional[bool] = None):
        self.security_thread = security_thread
        self.watermark = watermark
        self.microprinting = microprinting
        self.color_changing_ink = color_changing_ink
        self.uv_features = uv_features
        self.raised_printing = raised_printing
    
    def to_dict(self):
        return {
            "security_thread": self.security_thread,
            "watermark": self.watermark,
            "microprinting": self.microprinting,
            "color_changing_ink": self.color_changing_ink,
            "uv_features": self.uv_features,
            "raised_printing": self.raised_printing
        }

class ClassificationResult:
    """Classification result from CNN"""
    def __init__(self, authentic: bool, confidence: float, denomination: Optional[str] = None,
                 features: Optional[SecurityFeatures] = None, series_year: Optional[str] = None):
        self.authentic = authentic
        self.confidence = confidence
        self.denomination = denomination
        self.features = features or SecurityFeatures()
        self.series_year = series_year
    
    def to_dict(self):
        return {
            "authentic": self.authentic,
            "confidence": self.confidence,
            "denomination": self.denomination,
            "features": self.features.to_dict(),
            "series_year": self.series_year
        }

class ScanResult:
    """Complete scan analysis result"""
    def __init__(self, result: ClassificationResult, detection: Optional[DetectionResult] = None, 
                 detections: Optional[List[DetectionResult]] = None):
        self.detection = detection  # Primary detection (for backward compatibility)
        self.detections = detections or []  # Multiple detections for security features
        self.result = result
    
    def to_dict(self):
        return {
            "detection": self.detection.to_dict() if self.detection else None,
            "detections": [d.to_dict() for d in self.detections],
            "result": self.result.to_dict()
        }

class ScanResponse:
    """Response model for scan endpoint"""
    def __init__(self, id: str, timestamp: datetime, result: ScanResult, 
                 processing_time: float, message: str):
        self.id = id
        self.timestamp = timestamp
        self.result = result
        self.processing_time = processing_time
        self.message = message
    
    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "result": self.result.to_dict(),
            "processing_time": self.processing_time,
            "message": self.message
        }

class HealthResponse:
    """Health check response model"""
    def __init__(self, status: str, timestamp: datetime, version: str, 
                 models_loaded: Dict[str, bool], uptime: float):
        self.status = status
        self.timestamp = timestamp
        self.version = version
        self.models_loaded = models_loaded
        self.uptime = uptime
    
    def to_dict(self):
        return {
            "status": self.status,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version,
            "models_loaded": self.models_loaded,
            "uptime": self.uptime
        }

class ErrorResponse:
    """Error response model"""
    def __init__(self, error: str, message: str, detail: Optional[str] = None, 
                 timestamp: Optional[datetime] = None):
        self.error = error
        self.message = message
        self.detail = detail
        self.timestamp = timestamp or datetime.now()
    
    def to_dict(self):
        return {
            "error": self.error,
            "message": self.message,
            "detail": self.detail,
            "timestamp": self.timestamp.isoformat()
        }