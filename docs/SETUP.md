# PesoScan Thesis System - Setup Guide

This guide will help you set up and run the complete PesoScan system for your thesis project.

## System Requirements

### Hardware Requirements
- **Minimum**: 4GB RAM, 2GB free disk space
- **Recommended**: 8GB RAM, 4GB free disk space, GPU for model training
- **Camera**: Web camera for live scanning (optional)

### Software Requirements
- **Node.js**: Version 18.0 or higher
- **Python**: Version 3.8 or higher
- **Git**: For version control
- **Code Editor**: VS Code recommended

## Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/pesoscan.git
cd pesoscan
```

### 2. Frontend Setup (ReactJS)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create environment file
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start development server
npm start
```

The frontend will be available at `http://localhost:3000`

### 3. Backend Setup (Python/FastAPI)

```bash
# Navigate to backend directory
cd ../backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
echo "DEBUG=True" > .env
echo "HOST=0.0.0.0" >> .env
echo "PORT=8000" >> .env

# Start development server
python main.py
```

The backend API will be available at `http://localhost:8000`

### 4. API Documentation

Once the backend is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/api/health`

## Project Structure Explained

```
pesoscan/
├── frontend/                 # ReactJS Application
│   ├── public/              # Static files
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   │   ├── Logo.js      # PesoScan logo component
│   │   │   ├── Navbar.js    # Navigation component
│   │   │   └── Footer.js    # Footer component
│   │   ├── pages/           # Main application pages
│   │   │   ├── HomePage.js  # Landing page
│   │   │   ├── ScanPage.js  # Camera/upload interface
│   │   │   ├── ResultsPage.js # Analysis results
│   │   │   ├── HistoryPage.js # Scan history
│   │   │   └── AboutPage.js # About/help page
│   │   ├── services/        # API integration
│   │   │   └── api.js       # API client
│   │   ├── styles/          # CSS stylesheets
│   │   │   └── globals.css  # Global styles
│   │   ├── App.js           # Main app component
│   │   └── index.js         # App entry point
│   ├── package.json         # Dependencies
│   └── README.md
├── backend/                 # Python FastAPI Server
│   ├── app/
│   │   ├── api/             # API route handlers
│   │   │   ├── scan.py      # Scanning endpoints
│   │   │   └── health.py    # Health check endpoints
│   │   ├── core/            # Core configuration
│   │   │   └── config.py    # Settings and config
│   │   ├── models/          # Data models
│   │   │   └── scan_models.py # Request/response models
│   │   └── services/        # Business logic
│   │       └── detection_service.py # AI detection service
│   ├── trained_models/      # AI model files (add your models here)
│   ├── tests/              # Unit tests
│   ├── requirements.txt    # Python dependencies
│   └── main.py            # FastAPI application
├── assets/                 # Shared assets
├── docs/                  # Documentation
└── README.md             # Main documentation
```

## Development Workflow

### 1. Frontend Development

```bash
cd frontend

# Start development server with hot reload
npm start

# Build for production
npm run build

# Run tests
npm test
```

### 2. Backend Development

```bash
cd backend

# Start development server with auto-reload
python main.py

# Run tests
pytest

# Install new dependencies
pip install package-name
pip freeze > requirements.txt
```

### 3. API Testing

You can test the API endpoints using:

#### Using curl:
```bash
# Health check
curl http://localhost:8000/api/health

# Upload image for scanning
curl -X POST "http://localhost:8000/api/scan" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/peso-bill.jpg"
```

#### Using Python requests:
```python
import requests

# Health check
response = requests.get("http://localhost:8000/api/health")
print(response.json())

# Upload image
with open("peso-bill.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/api/scan", files=files)
    print(response.json())
```

## AI Model Integration

### Current Implementation (Demo Mode)

The current system runs in demo mode with simulated AI responses. For your thesis, you'll need to:

### 1. Train YOLOv8 Model

```python
# Example YOLOv8 training script
from ultralytics import YOLO

# Load a model
model = YOLO('yolov8n.pt')  # load a pretrained model

# Train the model
results = model.train(
    data='peso_dataset.yaml',  # path to dataset YAML
    epochs=100,                # number of epochs
    imgsz=640,                # image size
    device='0'                # GPU device
)

# Save the trained model
model.save('trained_models/peso_detection.pt')
```

### 2. Train CNN Classifier

```python
# Example CNN training script
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

# Define your CNN architecture
class PesoClassifier(nn.Module):
    def __init__(self):
        super(PesoClassifier, self).__init__()
        # Define your layers here
        pass
    
    def forward(self, x):
        # Define forward pass
        pass

# Train your model
model = PesoClassifier()
# Training loop...

# Save the trained model
torch.save(model.state_dict(), 'trained_models/peso_classifier.pt')
```

### 3. Update Detection Service

Replace the simulated methods in `app/services/detection_service.py` with actual model inference:

```python
async def _load_yolo_model(self):
    """Load actual YOLOv8 model"""
    from ultralytics import YOLO
    self.yolo_model = YOLO('trained_models/peso_detection.pt')

async def _load_cnn_model(self):
    """Load actual CNN model"""
    import torch
    self.cnn_model = torch.load('trained_models/peso_classifier.pt')
    self.cnn_model.eval()
```

## Database Setup (Optional)

For production deployment, you may want to add a database:

### 1. Install SQLAlchemy
```bash
pip install sqlalchemy alembic psycopg2-binary
```

### 2. Create Database Models
```python
# app/models/database.py
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ScanRecord(Base):
    __tablename__ = "scan_records"
    
    id = Column(String, primary_key=True)
    timestamp = Column(DateTime)
    authentic = Column(Boolean)
    confidence = Column(Float)
    processing_time = Column(Float)
```

## Production Deployment

### 1. Frontend (React)

```bash
# Build for production
cd frontend
npm run build

# Serve with nginx or similar
# Copy build/ contents to web server
```

### 2. Backend (FastAPI)

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 3. Docker Deployment

Create `Dockerfile` for containerized deployment:

```dockerfile
# Frontend Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]

# Backend Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port
   netstat -ano | findstr :3000
   # Kill process
   taskkill /PID <process_id> /F
   ```

2. **CORS Issues**
   - Check `ALLOWED_ORIGINS` in `backend/app/core/config.py`
   - Ensure frontend URL is included

3. **Module Import Errors**
   - Activate virtual environment
   - Install missing dependencies
   - Check Python path

4. **Camera Access Issues**
   - Ensure HTTPS for production (WebRTC requirement)
   - Check browser permissions
   - Test with different browsers

### Performance Optimization

1. **Frontend**
   - Use React.memo for expensive components
   - Implement image compression before upload
   - Add loading states and error boundaries

2. **Backend**
   - Use async/await for I/O operations
   - Implement request rate limiting
   - Add response caching for static results

3. **AI Models**
   - Use model quantization for faster inference
   - Implement batch processing for multiple images
   - Consider GPU acceleration

## Testing

### Frontend Tests
```bash
cd frontend
npm test
```

### Backend Tests
```bash
cd backend
pytest tests/
```

### Integration Tests
```bash
# Test full workflow
python tests/test_integration.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is for educational and research purposes. See LICENSE file for details.

## Support

For thesis-related questions or technical support:
- Check the documentation in `docs/`
- Review the FAQ in `frontend/src/pages/AboutPage.js`
- Create an issue in the repository