#!/usr/bin/env python3
"""
Enhanced YOLOv8 Training Script for CashMate Philippine Banknotes
Features: Progress monitoring, automatic model selection, result visualization
"""

import os
import sys
import yaml
import time
import json
from pathlib import Path
import torch
from ultralytics import YOLO
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('training.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CashMateTrainer:
    def __init__(self, config_path='cashmate_config.yaml'):
        self.config = self.load_config(config_path)
        self.start_time = None
        self.dataset_path = None
        self.model = None
        
    def load_config(self, config_path):
        """Load training configuration"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from: {config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return self.get_default_config()
    
    def get_default_config(self):
        """Default configuration if config file not found"""
        return {
            'epochs': 100,
            'batch_size': 16,
            'image_size': 640,
            'learning_rate': 0.01,
            'patience': 15,
            'save_period': 10,
            'workers': 8,
            'model_architecture': 'yolov8n',
            'use_pretrained': True,
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
    
    def install_dependencies(self):
        """Install required packages"""
        packages = [
            'roboflow',
            'ultralytics',
            'torch',
            'torchvision', 
            'Pillow',
            'opencv-python',
            'numpy',
            'matplotlib',
            'seaborn',
            'pyyaml'
        ]
        
        import subprocess
        for package in packages:
            try:
                __import__(package.replace('-', '_'))
                logger.info(f"✓ {package} available")
            except ImportError:
                logger.info(f"Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    def download_dataset(self):
        """Download CashMate dataset from Roboflow"""
        try:
            from roboflow import Roboflow
            
            logger.info("🔗 Connecting to Roboflow...")
            rf = Roboflow(api_key="gZGoQuvlmBgBLq1Ev4Ar")
            project = rf.workspace("cobra-mi40f").project("cashmate-ph-banknotes-wrvan")
            version = project.version(11)
            
            logger.info("📥 Downloading CashMate Philippine Banknotes dataset...")
            dataset = version.download("yolov8", location="./datasets/")
            
            self.dataset_path = dataset.location
            logger.info(f"✅ Dataset downloaded to: {self.dataset_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Dataset download failed: {e}")
            return False
    
    def analyze_dataset(self):
        """Analyze the downloaded dataset"""
        if not self.dataset_path:
            return
            
        try:
            # Find data.yaml
            data_yaml_path = None
            for root, dirs, files in os.walk(self.dataset_path):
                if 'data.yaml' in files:
                    data_yaml_path = os.path.join(root, files[files.index('data.yaml')])
                    break
            
            if data_yaml_path:
                with open(data_yaml_path, 'r') as f:
                    data_info = yaml.safe_load(f)
                
                logger.info("📊 Dataset Analysis:")
                logger.info(f"  Classes: {len(data_info.get('names', []))}")
                logger.info(f"  Class names: {data_info.get('names', [])}")
                logger.info(f"  Train path: {data_info.get('train', 'N/A')}")
                logger.info(f"  Val path: {data_info.get('val', 'N/A')}")
                logger.info(f"  Test path: {data_info.get('test', 'N/A')}")
                
        except Exception as e:
            logger.error(f"Dataset analysis failed: {e}")
    
    def setup_model(self):
        """Initialize YOLOv8 model"""
        try:
            model_arch = self.config['model_architecture']
            pretrained = self.config['use_pretrained']
            
            if pretrained:
                model_path = f"{model_arch}.pt"
                logger.info(f"🤖 Loading pretrained {model_arch} model...")
            else:
                model_path = f"{model_arch}.yaml"
                logger.info(f"🤖 Loading {model_arch} architecture from scratch...")
            
            self.model = YOLO(model_path)
            logger.info("✅ Model initialized successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Model initialization failed: {e}")
            return False
    
    def train_model(self):
        """Train the YOLOv8 model"""
        if not self.model or not self.dataset_path:
            logger.error("Model or dataset not ready")
            return None
        
        try:
            # Find data.yaml file
            data_yaml_path = None
            for root, dirs, files in os.walk(self.dataset_path):
                if 'data.yaml' in files:
                    data_yaml_path = os.path.join(root, files[files.index('data.yaml')])
                    break
            
            if not data_yaml_path:
                logger.error("data.yaml not found in dataset")
                return None
            
            # Training parameters
            train_args = {
                'data': data_yaml_path,
                'epochs': self.config['epochs'],
                'batch': self.config['batch_size'],
                'imgsz': self.config['image_size'],
                'lr0': self.config['learning_rate'],
                'patience': self.config['patience'],
                'save_period': self.config['save_period'],
                'workers': self.config['workers'],
                'project': 'runs/train',
                'name': f'cashmate_ph_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
                'exist_ok': True,
                'pretrained': self.config['use_pretrained'],
                'optimizer': 'SGD',
                'verbose': True,
                'seed': 42,
                'deterministic': True,
                'amp': True,
                'fraction': 1.0,
                'device': 'auto',
                **self.config['augmentation']
            }
            
            logger.info("🚀 Starting training...")
            logger.info(f"Configuration: {json.dumps(train_args, indent=2)}")
            
            self.start_time = time.time()
            
            # Train the model
            results = self.model.train(**train_args)
            
            training_time = time.time() - self.start_time
            logger.info(f"✅ Training completed in {training_time/3600:.2f} hours")
            
            # Validate
            logger.info("🔍 Running validation...")
            val_results = self.model.val()
            
            # Export model
            logger.info("📦 Exporting model...")
            self.model.export(format='onnx')
            
            return {
                'training_results': results,
                'validation_results': val_results,
                'training_time': training_time,
                'best_weights': results.save_dir / 'weights' / 'best.pt',
                'last_weights': results.save_dir / 'weights' / 'last.pt'
            }
            
        except Exception as e:
            logger.error(f"❌ Training failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def save_results(self, results):
        """Save training results and metrics"""
        if not results:
            return
        
        try:
            # Create results summary
            summary = {
                'timestamp': datetime.now().isoformat(),
                'dataset': 'CashMate Philippine Banknotes v11',
                'model_architecture': self.config['model_architecture'],
                'training_config': self.config,
                'training_time_hours': results['training_time'] / 3600,
                'best_weights_path': str(results['best_weights']),
                'last_weights_path': str(results['last_weights'])
            }
            
            # Add validation metrics if available
            if results['validation_results']:
                val_metrics = results['validation_results']
                summary['metrics'] = {
                    'mAP50': float(val_metrics.box.map50) if hasattr(val_metrics.box, 'map50') else 'N/A',
                    'mAP50-95': float(val_metrics.box.map) if hasattr(val_metrics.box, 'map') else 'N/A',
                    'precision': float(val_metrics.box.mp) if hasattr(val_metrics.box, 'mp') else 'N/A',
                    'recall': float(val_metrics.box.mr) if hasattr(val_metrics.box, 'mr') else 'N/A'
                }
            
            # Save summary
            results_file = f"cashmate_training_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(results_file, 'w') as f:
                json.dump(summary, f, indent=2, default=str)
            
            logger.info(f"📊 Results saved to: {results_file}")
            
            # Print summary
            logger.info("\n" + "=" * 80)
            logger.info("🎉 TRAINING SUMMARY")
            logger.info("=" * 80)
            logger.info(f"Model: {summary['model_architecture']}")
            logger.info(f"Training time: {summary['training_time_hours']:.2f} hours")
            logger.info(f"Best weights: {summary['best_weights_path']}")
            
            if 'metrics' in summary:
                logger.info("Validation Metrics:")
                for metric, value in summary['metrics'].items():
                    logger.info(f"  {metric}: {value}")
            
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    def run_full_training(self):
        """Execute complete training pipeline"""
        logger.info("🎯 CashMate Philippine Banknotes YOLOv8 Training")
        logger.info("=" * 80)
        
        # System info
        if torch.cuda.is_available():
            logger.info(f"🔥 GPU: {torch.cuda.get_device_name(0)}")
            logger.info(f"CUDA: {torch.version.cuda}")
            logger.info(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
        else:
            logger.info("💻 Using CPU (training will be slower)")
        
        # Install dependencies
        logger.info("📦 Checking dependencies...")
        self.install_dependencies()
        
        # Download dataset
        if not self.download_dataset():
            return False
        
        # Analyze dataset
        self.analyze_dataset()
        
        # Setup model
        if not self.setup_model():
            return False
        
        # Train model
        results = self.train_model()
        
        if results:
            self.save_results(results)
            logger.info("🎉 Training pipeline completed successfully!")
            return True
        else:
            logger.error("❌ Training pipeline failed!")
            return False

def main():
    """Main function"""
    trainer = CashMateTrainer()
    success = trainer.run_full_training()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)