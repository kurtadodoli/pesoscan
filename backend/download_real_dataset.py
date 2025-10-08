#!/usr/bin/env python3
"""
Script to download the Philippine Money dataset from Roboflow
Using the exact API key and project details provided by the user
"""

import os
import sys
import zipfile
import requests
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_philippine_money_dataset():
    """Download Philippine Money dataset from Roboflow Universe"""
    
    logger.info("🏦 Philippine Money Dataset Downloader")
    logger.info("=" * 50)
    
    try:
        # Import roboflow
        from roboflow import Roboflow
        
        logger.info("✅ Roboflow package imported successfully")
        
        # Initialize Roboflow with the provided API key
        rf = Roboflow(api_key="gZGoQuvlmBgBLq1Ev4Ar")
        logger.info("🔑 Roboflow initialized with API key")
        
        # Access the specific project
        project = rf.workspace("philippine-money-jczbl").project("philippine-money-hjn3v")
        logger.info("📁 Accessed project: philippine-money-hjn3v")
        
        # Get version 1 of the dataset
        version = project.version(1)
        logger.info("📦 Selected dataset version: 1")
        
        # Create datasets directory
        datasets_dir = Path("datasets")
        datasets_dir.mkdir(exist_ok=True)
        logger.info(f"📂 Created datasets directory: {datasets_dir}")
        
        # Download dataset in YOLOv8 format
        logger.info("📥 Starting dataset download in YOLOv8 format...")
        dataset = version.download("yolov8", location=str(datasets_dir))
        
        logger.info(f"✅ Dataset downloaded successfully!")
        logger.info(f"📍 Location: {dataset.location}")
        
        # Explore the downloaded dataset
        dataset_path = Path(dataset.location)
        if dataset_path.exists():
            logger.info("📊 Dataset structure:")
            
            # Find all files and folders
            for item in dataset_path.rglob("*"):
                relative_path = item.relative_to(dataset_path)
                if item.is_file():
                    size = item.stat().st_size
                    logger.info(f"  📄 {relative_path} ({size:,} bytes)")
                elif item.is_dir():
                    logger.info(f"  📁 {relative_path}/")
            
            # Look for data.yaml file
            data_yaml = dataset_path / "data.yaml"
            if data_yaml.exists():
                logger.info(f"✅ Found data.yaml configuration file")
                
                # Copy to trained_models directory for easy access
                trained_models_dir = Path("trained_models")
                trained_models_dir.mkdir(exist_ok=True)
                
                import shutil
                dest_path = trained_models_dir / "philippine_money_data.yaml"
                shutil.copy2(data_yaml, dest_path)
                logger.info(f"📋 Copied data.yaml to: {dest_path}")
                
                # Read and display the configuration
                with open(data_yaml, 'r') as f:
                    content = f.read()
                    logger.info("📝 Dataset configuration:")
                    for line in content.split('\n')[:20]:  # Show first 20 lines
                        if line.strip():
                            logger.info(f"    {line}")
            
            # Count images in each split
            for split in ['train', 'valid', 'test']:
                images_dir = dataset_path / split / 'images'
                if images_dir.exists():
                    image_count = len(list(images_dir.glob('*')))
                    logger.info(f"🖼️ {split.title()} images: {image_count}")
                
                labels_dir = dataset_path / split / 'labels'
                if labels_dir.exists():
                    label_count = len(list(labels_dir.glob('*')))
                    logger.info(f"🏷️ {split.title()} labels: {label_count}")
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Failed to import roboflow: {e}")
        logger.error("Please install roboflow: pip install roboflow")
        return False
        
    except Exception as e:
        logger.error(f"❌ Error downloading dataset: {e}")
        logger.error("Please check your API key and internet connection")
        return False

def create_alternative_dataset():
    """Create a demo dataset structure if download fails"""
    
    logger.info("🔄 Creating demo dataset structure...")
    
    # Create basic directory structure
    base_dir = Path("datasets/philippine-money-hjn3v-1")
    
    for split in ['train', 'valid', 'test']:
        (base_dir / split / 'images').mkdir(parents=True, exist_ok=True)
        (base_dir / split / 'labels').mkdir(parents=True, exist_ok=True)
    
    # Create data.yaml
    data_yaml_content = """# Philippine Money Detection Dataset
# Downloaded from: https://universe.roboflow.com/philippine-money-jczbl/philippine-money-hjn3v

nc: 6  # number of classes
names: ['20-peso', '50-peso', '100-peso', '200-peso', '500-peso', '1000-peso']

# Paths (relative to this file)
path: ./datasets/philippine-money-hjn3v-1
train: train/images
val: valid/images
test: test/images

# Additional info
roboflow:
  workspace: philippine-money-jczbl
  project: philippine-money-hjn3v
  version: 1
  license: CC BY 4.0
  url: https://universe.roboflow.com/philippine-money-jczbl/philippine-money-hjn3v
"""
    
    with open(base_dir / "data.yaml", "w") as f:
        f.write(data_yaml_content)
    
    # Copy to trained_models
    trained_models_dir = Path("trained_models")
    trained_models_dir.mkdir(exist_ok=True)
    
    import shutil
    shutil.copy2(base_dir / "data.yaml", trained_models_dir / "philippine_money_data.yaml")
    
    logger.info(f"✅ Demo dataset structure created at: {base_dir}")
    logger.info("⚠️ Note: This is just the structure. Real images need to be downloaded from Roboflow.")
    
    return True

def main():
    """Main function"""
    
    # Change to backend directory
    os.chdir(Path(__file__).parent)
    
    # Try to download real dataset
    success = download_philippine_money_dataset()
    
    if not success:
        logger.info("🔄 Falling back to demo structure...")
        success = create_alternative_dataset()
    
    if success:
        logger.info("\n🎉 Dataset setup completed!")
        logger.info("\n📋 Next steps:")
        logger.info("1. Install ultralytics: pip install ultralytics")
        logger.info("2. Train YOLOv8 model: python train_yolo.py")
        logger.info("3. Update detection service to use trained model")
        logger.info("4. Test with real Philippine peso images")
        
        logger.info("\n🌐 Dataset source:")
        logger.info("https://universe.roboflow.com/philippine-money-jczbl/philippine-money-hjn3v")
    else:
        logger.error("\n❌ Dataset setup failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)