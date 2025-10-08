#!/usr/bin/env python3
"""
Train YOLOv8 model with Roboflow CashMate Philippine Banknotes dataset
"""

import os
import sys
import yaml
from pathlib import Path
import torch
from ultralytics import YOLO
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    
    packages = [
        'roboflow',
        'ultralytics',
        'torch',
        'torchvision',
        'Pillow',
        'opencv-python',
        'numpy',
        'matplotlib',
        'seaborn'
    ]
    
    for package in packages:
        try:
            __import__(package)
            logger.info(f"✓ {package} already installed")
        except ImportError:
            logger.info(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def download_roboflow_dataset():
    """Download the CashMate dataset from Roboflow"""
    try:
        from roboflow import Roboflow
        
        logger.info("Connecting to Roboflow...")
        rf = Roboflow(api_key="gZGoQuvlmBgBLq1Ev4Ar")
        project = rf.workspace("cobra-mi40f").project("cashmate-ph-banknotes-wrvan")
        version = project.version(11)
        
        logger.info("Downloading CashMate Philippine Banknotes dataset...")
        dataset = version.download("yolov8", location="./datasets/")
        
        return dataset.location
        
    except Exception as e:
        logger.error(f"Error downloading dataset: {e}")
        return None

def create_training_config(dataset_path):
    """Create training configuration"""
    config = {
        'training': {
            'epochs': 100,
            'batch_size': 16,
            'image_size': 640,
            'learning_rate': 0.01,
            'patience': 10,
            'save_period': 10,
            'workers': 8,
            'device': 'auto'  # Will use GPU if available
        },
        'model': {
            'architecture': 'yolov8n',  # Start with nano for faster training
            'pretrained': True
        },
        'augmentation': {
            'hsv_h': 0.015,
            'hsv_s': 0.7,
            'hsv_v': 0.4,
            'degrees': 10.0,
            'translate': 0.1,
            'scale': 0.5,
            'shear': 2.0,
            'perspective': 0.0,
            'flipud': 0.0,
            'fliplr': 0.5,
            'mosaic': 1.0,
            'mixup': 0.0
        }
    }
    
    return config

def train_yolov8_model(dataset_path, config):
    """Train YOLOv8 model with the dataset"""
    try:
        logger.info("Initializing YOLOv8 training...")
        
        # Initialize model
        model_arch = config['model']['architecture']
        model = YOLO(f'{model_arch}.pt')  # Load pretrained model
        
        logger.info(f"Using model architecture: {model_arch}")
        logger.info(f"Dataset path: {dataset_path}")
        
        # Find the data.yaml file
        data_yaml_path = None
        for root, dirs, files in os.walk(dataset_path):
            for file in files:
                if file == 'data.yaml':
                    data_yaml_path = os.path.join(root, file)
                    break
            if data_yaml_path:
                break
        
        if not data_yaml_path:
            logger.error("Could not find data.yaml file in dataset")
            return None
        
        logger.info(f"Found data.yaml at: {data_yaml_path}")
        
        # Training parameters
        train_params = {
            'data': data_yaml_path,
            'epochs': config['training']['epochs'],
            'batch': config['training']['batch_size'],
            'imgsz': config['training']['image_size'],
            'lr0': config['training']['learning_rate'],
            'patience': config['training']['patience'],
            'save_period': config['training']['save_period'],
            'workers': config['training']['workers'],
            'device': config['training']['device'],
            'project': 'runs/train',
            'name': 'cashmate_ph_banknotes',
            'exist_ok': True,
            'pretrained': config['model']['pretrained'],
            'optimizer': 'SGD',
            'verbose': True,
            'seed': 42,
            'deterministic': True,
            'single_cls': False,
            'rect': False,
            'cos_lr': False,
            'close_mosaic': 10,
            'resume': False,
            'amp': True,  # Automatic Mixed Precision
            'fraction': 1.0,
            'profile': False,
            'freeze': None,
            # Data augmentation
            'hsv_h': config['augmentation']['hsv_h'],
            'hsv_s': config['augmentation']['hsv_s'],
            'hsv_v': config['augmentation']['hsv_v'],
            'degrees': config['augmentation']['degrees'],
            'translate': config['augmentation']['translate'],
            'scale': config['augmentation']['scale'],
            'shear': config['augmentation']['shear'],
            'perspective': config['augmentation']['perspective'],
            'flipud': config['augmentation']['flipud'],
            'fliplr': config['augmentation']['fliplr'],
            'mosaic': config['augmentation']['mosaic'],
            'mixup': config['augmentation']['mixup'],
        }
        
        logger.info("Starting training...")
        logger.info(f"Training parameters: {train_params}")
        
        # Train the model
        results = model.train(**train_params)
        
        logger.info("Training completed successfully!")
        
        # Validate the model
        logger.info("Running validation...")
        val_results = model.val()
        
        # Export the model
        logger.info("Exporting trained model...")
        model.export(format='onnx')
        
        return {
            'model': model,
            'results': results,
            'validation': val_results,
            'best_weights': model.trainer.best,
            'last_weights': model.trainer.last
        }
        
    except Exception as e:
        logger.error(f"Error during training: {e}")
        import traceback
        traceback.print_exc()
        return None

def save_training_summary(results, config):
    """Save training summary and metrics"""
    try:
        summary = {
            'dataset': 'CashMate Philippine Banknotes',
            'model_architecture': config['model']['architecture'],
            'epochs_completed': config['training']['epochs'],
            'batch_size': config['training']['batch_size'],
            'image_size': config['training']['image_size'],
            'learning_rate': config['training']['learning_rate'],
        }
        
        if results and 'validation' in results:
            val_metrics = results['validation']
            summary.update({
                'final_map50': getattr(val_metrics, 'map50', 'N/A'),
                'final_map50_95': getattr(val_metrics, 'map', 'N/A'),
                'precision': getattr(val_metrics, 'mp', 'N/A'),
                'recall': getattr(val_metrics, 'mr', 'N/A'),
            })
        
        # Save summary
        summary_path = 'training_summary_cashmate.yaml'
        with open(summary_path, 'w') as f:
            yaml.dump(summary, f, default_flow_style=False)
        
        logger.info(f"Training summary saved to: {summary_path}")
        logger.info("Training Summary:")
        for key, value in summary.items():
            logger.info(f"  {key}: {value}")
            
    except Exception as e:
        logger.error(f"Error saving training summary: {e}")

def main():
    """Main training function"""
    logger.info("=" * 60)
    logger.info("CashMate Philippine Banknotes YOLOv8 Training")
    logger.info("=" * 60)
    
    # Check GPU availability
    if torch.cuda.is_available():
        logger.info(f"GPU available: {torch.cuda.get_device_name(0)}")
        logger.info(f"CUDA version: {torch.version.cuda}")
    else:
        logger.info("GPU not available, using CPU (training will be slower)")
    
    # Install dependencies
    logger.info("Checking dependencies...")
    install_dependencies()
    
    # Download dataset
    logger.info("Downloading dataset...")
    dataset_path = download_roboflow_dataset()
    
    if not dataset_path:
        logger.error("Failed to download dataset. Exiting.")
        return
    
    logger.info(f"Dataset downloaded to: {dataset_path}")
    
    # Create training configuration
    config = create_training_config(dataset_path)
    logger.info("Training configuration created")
    
    # Train model
    logger.info("Starting model training...")
    results = train_yolov8_model(dataset_path, config)
    
    if results:
        logger.info("Training completed successfully!")
        
        # Save training summary
        save_training_summary(results, config)
        
        # Print final results
        logger.info("\n" + "=" * 60)
        logger.info("TRAINING COMPLETED")
        logger.info("=" * 60)
        logger.info(f"Best weights: {results.get('best_weights', 'N/A')}")
        logger.info(f"Last weights: {results.get('last_weights', 'N/A')}")
        logger.info("Check 'runs/train/cashmate_ph_banknotes' for detailed results")
        
    else:
        logger.error("Training failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)