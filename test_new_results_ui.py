#!/usr/bin/env python3
"""
Test script to generate sample results for the new UI design
This will create mock data that matches the expected structure
"""

import json
import base64
from pathlib import Path

def create_sample_result_data():
    """Create sample data that matches our new UI expectations"""
    
    # Sample YOLO detections with multiple features
    sample_detections = [
        {
            "class_name": "20",
            "feature_name": "20 Peso Bill",
            "confidence": 0.793,
            "bbox": [0.15, 0.12, 0.45, 0.38]
        },
        {
            "class_name": "1000", 
            "feature_name": "1000 Peso Bill",
            "confidence": 0.772,
            "bbox": [0.50, 0.15, 0.85, 0.45]
        },
        {
            "class_name": "50",
            "feature_name": "50 Peso Bill", 
            "confidence": 0.610,
            "bbox": [0.25, 0.55, 0.75, 0.85]
        }
    ]
    
    # Mock comprehensive scan result
    mock_result = {
        "id": "test_scan_001",
        "result": {
            "detections": sample_detections,
            "authentic": True,
            "confidence": 0.85,
            "denomination": "Mixed Denominations",
            "features": {
                "security_thread": True,
                "watermark": True,
                "microprinting": False,
                "color_changing_ink": True,
                "uv_features": False,
                "raised_printing": True
            }
        },
        "peso_scan": {
            "result": {
                "detections": sample_detections
            }
        },
        "processing_time": 2.14,
        "timestamp": "2025-10-04T03:30:00Z"
    }
    
    return mock_result

def save_sample_image():
    """Create a sample image data URL for testing"""
    # For demo purposes, we'll use a small placeholder
    # In real usage, this would be the actual scanned image
    sample_image_data = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
    
    return sample_image_data

if __name__ == "__main__":
    # Create sample data
    sample_result = create_sample_result_data()
    sample_image = save_sample_image()
    
    print("Sample Result Data:")
    print(json.dumps(sample_result, indent=2))
    
    print(f"\nSample Image Data Length: {len(sample_image)} characters")
    print("Sample Image Data (first 100 chars):", sample_image[:100])
    
    # Save to file for frontend testing
    test_data = {
        "result": sample_result,
        "imageUrl": sample_image,
        "mode": "file",
        "scanType": "comprehensive"
    }
    
    with open("C:/pesoscan/frontend/public/sample_results.json", "w") as f:
        json.dump(test_data, f, indent=2)
    
    print("\nSample test data saved to frontend/public/sample_results.json")
    print("You can use this data to test the new results UI interface")