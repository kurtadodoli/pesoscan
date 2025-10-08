#!/usr/bin/env python3
"""
Direct dataset download script for Philippine Money Detection
Downloads dataset directly from Roboflow API without requiring roboflow package
"""

import os
import json
import zipfile
import requests
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def download_file(url, filepath):
    """Download file from URL with progress"""
    logger.info(f"📥 Downloading: {url}")
    
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filepath, 'wb') as f:
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    print(f"\r📊 Progress: {percent:.1f}%", end='', flush=True)
    
    print()  # New line after progress
    logger.info(f"✅ Downloaded: {filepath}")

def download_philippine_money_dataset():
    """Download Philippine Money dataset from Roboflow"""
    logger.info("🏦 Philippine Money Dataset Direct Downloader")
    logger.info("=" * 50)
    
    # Dataset configuration
    API_KEY = "gZGoQuvlmBgBLq1Ev4Ar"
    PROJECT_NAME = "philippine-money-hjn3v"
    VERSION = "1"
    FORMAT = "yolov8"
    
    # Create dataset directory
    dataset_dir = Path("datasets") / f"{PROJECT_NAME}-{VERSION}"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Construct download URL
        download_url = f"https://universe.roboflow.com/philippine-money-jczbl/{PROJECT_NAME}/dataset/{VERSION}/download/{FORMAT}"
        
        # Add API key as parameter
        params = {
            'key': API_KEY
        }
        
        logger.info(f"🔗 Download URL: {download_url}")
        logger.info(f"🔑 API Key: {API_KEY[:10]}...")
        
        # Download the dataset
        response = requests.get(download_url, params=params, stream=True)
        
        if response.status_code == 200:
            # Save as zip file
            zip_path = dataset_dir / f"{PROJECT_NAME}.zip"
            
            logger.info(f"💾 Saving to: {zip_path}")
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(zip_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            percent = (downloaded / total_size) * 100
                            print(f"\r📊 Download Progress: {percent:.1f}%", end='', flush=True)
            
            print()  # New line after progress
            logger.info(f"✅ Dataset downloaded: {zip_path}")
            
            # Extract the zip file
            logger.info("📦 Extracting dataset...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(dataset_dir)
            
            logger.info(f"✅ Dataset extracted to: {dataset_dir}")
            
            # Remove zip file to save space
            zip_path.unlink()
            logger.info("🗑️ Cleaned up zip file")
            
            # List contents
            logger.info("\n📂 Dataset structure:")
            for root, dirs, files in os.walk(dataset_dir):
                level = root.replace(str(dataset_dir), '').count(os.sep)
                indent = ' ' * 2 * level
                logger.info(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files[:5]:  # Show first 5 files
                    logger.info(f"{subindent}{file}")
                if len(files) > 5:
                    logger.info(f"{subindent}... and {len(files) - 5} more files")
            
            return True
            
        else:
            logger.error(f"❌ Failed to download dataset: HTTP {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Network error: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False

def create_demo_structure():
    """Create demo dataset structure as fallback"""
    logger.info("🔄 Creating demo dataset structure...")
    
    dataset_dir = Path("datasets") / "philippine-money-hjn3v-1"
    
    # Create directories
    dirs = [
        "train/images",
        "train/labels", 
        "valid/images",
        "valid/labels",
        "test/images",
        "test/labels"
    ]
    
    for dir_path in dirs:
        (dataset_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    # Create data.yaml
    data_yaml = {
        'train': str(dataset_dir / "train" / "images"),
        'val': str(dataset_dir / "valid" / "images"), 
        'test': str(dataset_dir / "test" / "images"),
        'nc': 6,
        'names': ['20-peso', '50-peso', '100-peso', '200-peso', '500-peso', '1000-peso']
    }
    
    with open(dataset_dir / "data.yaml", 'w') as f:
        import yaml
        yaml.dump(data_yaml, f)
    
    logger.info(f"✅ Demo structure created: {dataset_dir}")
    return dataset_dir

if __name__ == "__main__":
    logger.info("🚀 Starting Philippine Money dataset download...")
    
    success = download_philippine_money_dataset()
    
    if not success:
        logger.info("⚠️ Real download failed, creating demo structure...")
        create_demo_structure()
    
    logger.info("\n🎉 Dataset setup completed!")
    logger.info("\n📋 Next steps:")
    logger.info("1. Install ultralytics: pip install ultralytics")
    logger.info("2. Train YOLOv8 model: python train_yolo.py")
    logger.info("3. Update detection service to use trained model")
    logger.info("4. Test with real Philippine peso images")
    logger.info("\n🌐 Dataset source:")
    logger.info("https://universe.roboflow.com/philippine-money-jczbl/philippine-money-hjn3v")