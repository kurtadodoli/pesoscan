#!/usr/bin/env python3
"""
Download the exact Philippine money dataset from Roboflow
Using the provided API key and project details
"""

import os
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def download_philippine_money_dataset():
    """Download the exact Philippine money dataset from Roboflow"""
    logger.info("🏦 Downloading Philippine Money Dataset from Roboflow")
    logger.info("=" * 60)
    
    try:
        # Import roboflow
        from roboflow import Roboflow
        logger.info("✅ Roboflow imported successfully")
        
        # Initialize Roboflow with API key
        api_key = "gZGoQuvlmBgBLq1Ev4Ar"
        rf = Roboflow(api_key=api_key)
        logger.info(f"🔑 Roboflow initialized with API key: {api_key[:10]}...")
        
        # Access the workspace and project
        workspace_name = "philippine-money-jczbl"
        project_name = "philippine-money-hjn3v"
        
        logger.info(f"🏢 Accessing workspace: {workspace_name}")
        project = rf.workspace(workspace_name).project(project_name)
        logger.info(f"📁 Accessing project: {project_name}")
        
        # Get version 1 of the dataset
        version_number = 1
        version = project.version(version_number)
        logger.info(f"📦 Getting version: {version_number}")
        
        # Download in YOLOv8 format
        format_type = "yolov8"
        logger.info(f"💾 Downloading dataset in {format_type} format...")
        
        # Download the dataset
        dataset = version.download(format_type)
        logger.info(f"✅ Dataset downloaded successfully!")
        
        # Get the dataset location
        dataset_location = dataset.location
        logger.info(f"📍 Dataset location: {dataset_location}")
        
        # Check dataset structure
        dataset_path = Path(dataset_location)
        if dataset_path.exists():
            logger.info("📂 Dataset structure:")
            for item in dataset_path.iterdir():
                if item.is_dir():
                    file_count = len(list(item.rglob("*")))
                    logger.info(f"  📁 {item.name}/ ({file_count} files)")
                else:
                    logger.info(f"  📄 {item.name}")
                    
            # Check for data.yaml
            data_yaml = dataset_path / "data.yaml"
            if data_yaml.exists():
                logger.info("✅ data.yaml found")
                with open(data_yaml, 'r') as f:
                    content = f.read()
                logger.info("📋 Dataset configuration:")
                print(content[:500] + "..." if len(content) > 500 else content)
            else:
                logger.warning("⚠️ data.yaml not found")
        
        return dataset_location
        
    except ImportError as e:
        logger.error(f"❌ Failed to import roboflow: {e}")
        logger.error("Please install roboflow: pip install roboflow")
        return None
        
    except Exception as e:
        logger.error(f"❌ Error downloading dataset: {e}")
        return None

if __name__ == "__main__":
    logger.info("🚀 Starting Roboflow dataset download...")
    
    dataset_location = download_philippine_money_dataset()
    
    if dataset_location:
        logger.info(f"\n🎉 Dataset download completed successfully!")
        logger.info(f"📍 Dataset saved to: {dataset_location}")
        logger.info("\n📋 Next steps:")
        logger.info("1. Update detection service to use the downloaded dataset")
        logger.info("2. Train YOLOv8 model with the real data")
        logger.info("3. Test with actual Philippine peso images")
    else:
        logger.error("\n❌ Dataset download failed!")
        logger.error("Please check your internet connection and API key")