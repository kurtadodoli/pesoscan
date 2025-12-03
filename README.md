PesoScan

## Overview

PesoScan is a web-based counterfeit detection platform for Philippine peso bills, combining a ReactJS frontend with a Python backend that integrates YOLOv8 for object detection and a hybrid ResNet-50 & MobileNetV3 architecture for classification. The system allows users to scan or upload images of Philippine banknotes and receive automated authenticity classification.

## System Architecture

### Frontend (ReactJS)
- **Design Philosophy**: Minimalist, professional, user-friendly
- **Color Scheme**: Dark blue/teal primary, white/silver accents
- **Typography**: Roboto/Montserrat
- **Responsive Design**: Mobile-first approach

### Backend (Python/FastAPI)
- **Object Detection**: YOLOv8 for peso bill localization
- **Classification**: Hybrid ResNet-50 & MobileNetV3 for authenticity determination
- **API**: RESTful endpoints for image processing

## Features

### Core Functionality
- 📸 **Live Camera Scanning**: Real-time peso bill capture
- 📁 **Image Upload**: Support for various image formats
- 🔍 **AI Detection**: YOLOv8 + CNN classification pipeline
- 📊 **Confidence Scoring**: Percentage-based authenticity confidence
- 📱 **Responsive Design**: Works on desktop and mobile devices

### Pages
1. **Landing Page**: System introduction with scan/upload options
2. **Scan/Upload Page**: Camera interface and file upload
3. **Results Page**: Classification results with visual feedback
4. **History Page**: Previous scan records (optional)
5. **About/Help Page**: System information and FAQs

## Project Structure

```
pesoscan/
├── frontend/           # ReactJS application
├── backend/           # Python FastAPI server
├── assets/           # Logos, images, and design assets
├── docs/            # Documentation and thesis materials
└── README.md        # This file
```

## Tech Stack

### Frontend
- **Framework**: ReactJS
- **Styling**: CSS3 with custom design system
- **Camera**: WebRTC for live video capture
- **HTTP Client**: Axios for API communication
- **Routing**: React Router

### Backend
- **Framework**: FastAPI
- **ML Libraries**: YOLOv8, TensorFlow/PyTorch
- **Image Processing**: OpenCV, PIL
- **API Documentation**: Swagger/OpenAPI

### AI/ML
- **Object Detection**: YOLOv8 (Ultralytics)
- **Classification**: Hybrid ResNet-50 & MobileNetV3 with Transfer Learning
- **Training Data**: Philippine peso bill dataset

## Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/pesoscan.git
   cd pesoscan
   ```

2. **Set up the frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```

3. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   python main.py
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## System Workflow

1. **User Input**: Upload or scan peso bill image via ReactJS frontend
2. **API Request**: Image sent to Python backend API
3. **Detection**: YOLOv8 detects and crops peso bill from image























