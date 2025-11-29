# PesoScan API Documentation

## Overview

The PesoScan API provides endpoints for AI-powered counterfeit detection of Philippine peso bills. The API is built with FastAPI and integrates YOLOv8 for object detection and CNN for classification.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required for the demo version.

## API Endpoints

### Health Check

#### GET `/api/health`

Returns the current health status of the API and loaded models.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-09-16T10:30:00.000Z",
  "version": "1.0.0",
  "models_loaded": {
    "yolo": true,
    "cnn": true
  },
  "uptime": 3600.5
}
```

### Scanning Endpoints

#### POST `/api/scan`

Process an image captured from camera for peso bill authenticity detection.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with `file` field containing the image

**Response:**
```json
{
  "id": "scan_1694856600",
  "timestamp": "2025-09-16T10:30:00.000Z",
  "result": {
    "detection": {
      "bbox": [0.2, 0.2, 0.8, 0.8],
      "confidence": 92.5,
      "class_name": "peso_bill"
    },
    "result": {
      "authentic": true,
      "confidence": 87.3,
      "denomination": "100",
      "features": {
        "security_thread": true,
        "watermark": true,
        "microprinting": true,
        "color_changing_ink": false
      }
    }
  },
  "processing_time": 1.24,
  "message": "Scan completed successfully"
}
```

#### POST `/api/upload`

Process an uploaded image file for peso bill authenticity detection.

**Request:**
- Content-Type: `multipart/form-data`
- Body: Form data with `file` field containing the image

**Response:**
Same as `/api/scan` endpoint.

### History Endpoints

#### GET `/api/history`

Retrieve scan history with pagination.

**Parameters:**
- `limit` (optional): Number of records to return (default: 20)
- `offset` (optional): Offset for pagination (default: 0)

**Response:**
```json
{
  "items": [],
  "total": 0,
  "page": 1,
  "limit": 20,
  "message": "History feature coming soon"
}
```

#### GET `/api/scans/{scan_id}`

Retrieve a specific scan result by ID.

**Parameters:**
- `scan_id`: Unique scan identifier

**Response:**
```json
{
  "error": "Not Found",
  "message": "Scan not found. History storage not implemented in demo."
}
```

#### DELETE `/api/scans/{scan_id}`

Delete a scan record from history.

**Parameters:**
- `scan_id`: Unique scan identifier

**Response:**
```json
{
  "error": "Not Found", 
  "message": "Scan not found. History storage not implemented in demo."
}
```

### Statistics

#### GET `/api/stats`

Get system statistics and usage information.

**Response:**
```json
{
  "total_scans": 0,
  "authentic_count": 0,
  "counterfeit_count": 0,
  "average_confidence": 0.0,
  "uptime": 3600.5,
  "last_scan": null,
  "message": "Statistics feature coming soon"
}
```

## Data Models

### DetectionResult

Object detection result from YOLOv8:

```json
{
  "bbox": [0.2, 0.2, 0.8, 0.8],  // [x1, y1, x2, y2] normalized coordinates
  "confidence": 92.5,             // Detection confidence (0-100)
  "class_name": "peso_bill"       // Detected object class
}
```

### SecurityFeatures

Security features analysis result:

```json
{
  "security_thread": true,        // Security thread detected
  "watermark": true,              // Watermark detected  
  "microprinting": false,         // Microprinting detected
  "color_changing_ink": true,     // Color-changing ink detected
  "uv_features": null,            // UV features (optional)
  "raised_printing": null         // Raised printing (optional)
}
```

### ClassificationResult

Classification result from CNN:

```json
{
  "authentic": true,              // Whether bill is authentic
  "confidence": 87.3,             // Classification confidence (0-100)
  "denomination": "100",          // Detected peso denomination
  "features": {                   // Security features analysis
    // SecurityFeatures object
  }
}
```

### ScanResult

Complete scan analysis result:

```json
{
  "detection": {                  // Object detection result (optional)
    // DetectionResult object
  },
  "result": {                     // Classification result
    // ClassificationResult object  
  }
}
```

### ScanResponse

Complete response from scan endpoints:

```json
{
  "id": "scan_1694856600",        // Unique scan identifier
  "timestamp": "2025-09-16T10:30:00.000Z",  // Scan timestamp
  "result": {                     // Scan analysis result
    // ScanResult object
  },
  "processing_time": 1.24,        // Processing time in seconds
  "message": "Scan completed successfully"  // Response message
}
```

## Error Responses

### 400 Bad Request

Invalid request data or image format:

```json
{
  "detail": "Invalid file format. Supported: JPEG, PNG, BMP"
}
```

### 413 Payload Too Large

Image file exceeds size limit:

```json
{
  "detail": "File too large. Maximum size: 10.0MB"
}
```

### 500 Internal Server Error

Server processing error:

```json
{
  "message": "Internal server error",
  "detail": "Error details here"
}
```

## Rate Limiting

Currently no rate limiting is implemented in the demo version. For production deployment, consider implementing:

- Per-IP rate limiting
- API key-based quotas
- Burst protection

## Image Requirements

### Supported Formats
- JPEG/JPG
- PNG  
- BMP

### Size Limits
- Maximum file size: 10MB
- Recommended dimensions: 640x640 to 1920x1080
- Minimum dimensions: 224x224

### Quality Guidelines
- Good lighting without shadows
- Bill should be flat and fully visible
- Avoid blurry or low-quality images
- Ensure entire bill is within frame

## Integration Examples

### JavaScript/React

```javascript
const scanImage = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch('http://localhost:8000/api/scan', {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
};
```

### Python

```python
import requests

def scan_image(image_path):
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            'http://localhost:8000/api/scan',
            files=files
        )
    return response.json()
```

### curl

```bash
curl -X POST "http://localhost:8000/api/scan" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@peso-bill.jpg"
```

## Development Notes

### Demo Mode

The current implementation runs in demo mode with simulated AI responses. For production use:

1. Replace mock detection with actual YOLOv8 model
2. Replace mock classification with trained CNN model  
3. Implement proper database storage for history
4. Add authentication and rate limiting
5. Deploy with production-grade server (gunicorn/uvicorn)

### Model Integration

To integrate actual AI models, update the `DetectionService` class in `app/services/detection_service.py`:

```python
# Load actual YOLOv8 model
from ultralytics import YOLO
self.yolo_model = YOLO('trained_models/peso_detection.pt')

# Load actual CNN model
import torch
self.cnn_model = torch.load('trained_models/peso_classifier.pt')
```

### Database Integration

For persistent storage, implement database models and update endpoints to use actual data persistence instead of mock responses.

## API Testing

The API can be tested using the built-in Swagger UI at:
- http://localhost:8000/docs

Or ReDoc documentation at:
- http://localhost:8000/redoc