#!/usr/bin/env python3
"""
Train Counterfeit Detection Model using YOLOv8
Uses the downloaded Roboflow dataset for training
"""

import os
import sys
import yaml
import torch
from pathlib import Path
from ultralytics import YOLO
import time
from datetime import datetime


def setup_training_environment():
    """Setup the training environment and paths"""
    print("🔧 Setting up training environment...")
    
    # Check if CUDA is available
    if torch.cuda.is_available():
        device = "cuda"
        print(f"✓ CUDA available - Using GPU: {torch.cuda.get_device_name()}")
        print(f"✓ GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    else:
        device = "cpu"
        print("⚠️ CUDA not available - Using CPU (training will be slower)")
    
    return device


def validate_dataset_path():
    """Validate that the dataset exists and has correct structure"""
    dataset_path = Path("Counterfeit-Money-Detector-v5")
    data_yaml_path = dataset_path / "data.yaml"
    
    print("📁 Validating dataset...")
    
    if not dataset_path.exists():
        print(f"❌ Dataset directory not found: {dataset_path}")
        return None
        
    if not data_yaml_path.exists():
        print(f"❌ Data configuration file not found: {data_yaml_path}")
        return None
    
    # Check if train, valid, test directories exist
    for split in ['train', 'valid', 'test']:
        split_path = dataset_path / split
        if not split_path.exists():
            print(f"⚠️ {split} directory not found: {split_path}")
        else:
            images_path = split_path / 'images'
            labels_path = split_path / 'labels'
            if images_path.exists() and labels_path.exists():
                img_count = len(list(images_path.glob('*.jpg'))) + len(list(images_path.glob('*.png')))
                label_count = len(list(labels_path.glob('*.txt')))
                print(f"✓ {split}: {img_count} images, {label_count} labels")
            else:
                print(f"⚠️ {split} missing images or labels subdirectory")
    
    return str(data_yaml_path)


def update_data_yaml_paths(data_yaml_path):
    """Update the data.yaml file with correct absolute paths"""
    print("📝 Updating data.yaml with correct paths...")
    
    with open(data_yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    # Get the dataset directory
    dataset_dir = Path(data_yaml_path).parent
    
    # Update paths to be absolute
    data['train'] = str(dataset_dir / 'train' / 'images')
    data['val'] = str(dataset_dir / 'valid' / 'images')
    data['test'] = str(dataset_dir / 'test' / 'images')
    
    # Save the updated yaml
    with open(data_yaml_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
    
    print(f"✓ Updated paths in {data_yaml_path}")
    print(f"  - Train: {data['train']}")
    print(f"  - Val: {data['val']}")
    print(f"  - Test: {data['test']}")
    print(f"  - Classes: {data['nc']}")
    
    return data


def train_counterfeit_model(data_yaml_path, device):
    """Train the YOLOv8 model for counterfeit detection"""
    print("🚀 Starting model training...")
    
    try:
        # Load a pre-trained YOLOv8 model
        model = YOLO('yolov8n.pt')  # Start with nano model for faster training
        print("✓ Loaded YOLOv8n pre-trained model")
        
        # Create runs directory if it doesn't exist
        runs_dir = Path("counterfeit_detection_runs")
        runs_dir.mkdir(exist_ok=True)
        
        # Generate a unique project name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_name = f"counterfeit_yolov8_{timestamp}"
        
        # Training parameters
        training_params = {
            'data': data_yaml_path,
            'epochs': 50,  # Start with 50 epochs, can adjust later
            'imgsz': 640,  # Image size
            'batch': 16,   # Batch size (adjust based on GPU memory)
            'device': device,
            'project': str(runs_dir),
            'name': project_name,
            'save': True,
            'save_period': 10,  # Save checkpoint every 10 epochs
            'patience': 15,     # Early stopping patience
            'verbose': True,
            'plots': True,      # Generate training plots
            'val': True,        # Validate during training
        }
        
        # Adjust batch size if using CPU
        if device == "cpu":
            training_params['batch'] = 8
            training_params['workers'] = 2
            print("⚠️ Reduced batch size and workers for CPU training")
        
        print("\n📋 Training Configuration:")
        for key, value in training_params.items():
            print(f"  {key}: {value}")
        
        print(f"\n🏃‍♂️ Starting training with {training_params['epochs']} epochs...")
        print("=" * 60)
        
        # Start training
        results = model.train(**training_params)
        
        print("=" * 60)
        print("✅ Training completed successfully!")
        
        # Get the path to the best trained model
        best_model_path = runs_dir / project_name / "weights" / "best.pt"
        last_model_path = runs_dir / project_name / "weights" / "last.pt"
        
        print(f"📁 Training results saved in: {runs_dir / project_name}")
        print(f"🏆 Best model: {best_model_path}")
        print(f"📝 Last model: {last_model_path}")
        
        # Copy the best model to the main directory for easy access
        import shutil
        if best_model_path.exists():
            shutil.copy2(best_model_path, "counterfeit_detection_best.pt")
            print(f"✓ Copied best model to: counterfeit_detection_best.pt")
        
        return str(best_model_path), results
        
    except Exception as e:
        print(f"❌ Training failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return None, None


def validate_trained_model(model_path, data_yaml_path):
    """Validate the trained model on the test set"""
    print("\n🔍 Validating trained model...")
    
    try:
        # Load the trained model
        model = YOLO(model_path)
        
        # Run validation
        results = model.val(data=data_yaml_path, split='test')
        
        print("✅ Model validation completed!")
        print(f"📊 Validation results:")
        print(f"  - mAP50: {results.box.map50:.4f}")
        print(f"  - mAP50-95: {results.box.map:.4f}")
        
        return results
        
    except Exception as e:
        print(f"❌ Validation failed: {str(e)}")
        return None


def main():
    """Main training function"""
    print("=" * 70)
    print("🎯 Counterfeit Detection Model Training")
    print("=" * 70)
    
    # Setup environment
    device = setup_training_environment()
    
    # Validate dataset
    data_yaml_path = validate_dataset_path()
    if not data_yaml_path:
        print("❌ Dataset validation failed. Please check your dataset.")
        sys.exit(1)
    
    # Update data.yaml paths
    dataset_config = update_data_yaml_paths(data_yaml_path)
    
    # Start training
    start_time = time.time()
    best_model_path, training_results = train_counterfeit_model(data_yaml_path, device)
    
    if best_model_path:
        training_time = time.time() - start_time
        print(f"\n⏱️ Total training time: {training_time/60:.1f} minutes")
        
        # Validate the model
        validation_results = validate_trained_model(best_model_path, data_yaml_path)
        
        print("\n🎉 Training pipeline completed successfully!")
        print(f"🏆 Best model saved at: {best_model_path}")
        print("\n📋 Next steps:")
        print("  1. Check training plots in the runs directory")
        print("  2. Test the model with sample images")
        print("  3. Integrate the model into your detection service")
        
    else:
        print("\n💥 Training failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()