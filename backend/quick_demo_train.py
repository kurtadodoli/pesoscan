#!/usr/bin/env python3
"""
Quick Training Demo with Subset of Data
"""

import os
import sys
import shutil
import random
from pathlib import Path
from ultralytics import YOLO
import torch


def create_subset_dataset(source_dir, target_dir, subset_size=100):
    """Create a smaller subset of the dataset for faster training"""
    
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    # Create target directories
    for split in ['train', 'valid']:
        for subdir in ['images', 'labels']:
            (target_path / split / subdir).mkdir(parents=True, exist_ok=True)
    
    # Get random sample of training files
    train_images = list((source_path / 'train' / 'images').glob('*.jpg'))
    random.shuffle(train_images)
    
    # Take a small subset
    train_subset = train_images[:subset_size]
    valid_subset = train_images[subset_size:subset_size + 20]  # 20 for validation
    
    print(f"Creating subset with {len(train_subset)} training and {len(valid_subset)} validation images")
    
    # Copy training files
    for img_path in train_subset:
        label_path = source_path / 'train' / 'labels' / f"{img_path.stem}.txt"
        
        # Copy image and label
        shutil.copy2(img_path, target_path / 'train' / 'images' / img_path.name)
        if label_path.exists():
            shutil.copy2(label_path, target_path / 'train' / 'labels' / label_path.name)
    
    # Copy validation files
    for img_path in valid_subset:
        label_path = source_path / 'train' / 'labels' / f"{img_path.stem}.txt"
        
        # Copy image and label
        shutil.copy2(img_path, target_path / 'valid' / 'images' / img_path.name)
        if label_path.exists():
            shutil.copy2(label_path, target_path / 'valid' / 'labels' / label_path.name)
    
    # Create data.yaml for subset
    data_yaml_content = f"""
names:
- 1000_pearl
- 1000_pearl_watermark
- 100_whale
- 100_whale_watermark
- 10_New_Back
- 10_New_Front
- 10_Old_Back
- 10_Old_Front
- 1_New_Back
- 1_New_Front
- 1_Old_Back
- 1_Old_Front
- 200_tarsier
- 200_tarsier_watermark
- 20_New_Back
- 20_New_Front
- 20_civet
- 20_civet_watermark
- 25Cent_New_Back
- 25Cent_New_Front
- 25Cent_Old_Back
- 25Cent_Old_Front
- 500_big_parrot
- 500_parrot_watermark
- 50_maliputo
- 50_maliputo_watermark
- 5_New_Back
- 5_New_Front
- 5_Old_Back
- 5_Old_Front
- clear_window
- concealed_value
- eagle
- optically_variable_device
- sampaguita
- security_thread
- see_through_mark
- serial_number
- value
- value_watermark
- watermark
nc: 41
train: train/images
val: valid/images
"""
    
    with open(target_path / 'data.yaml', 'w') as f:
        f.write(data_yaml_content.strip())
    
    return str(target_path / 'data.yaml')


def main():
    print("=" * 60)
    print("🚀 Quick Training Demo - Counterfeit Detection")
    print("=" * 60)
    
    # Check device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🔧 Using device: {device}")
    
    # Create subset dataset
    subset_dir = "CounterfeitDemo"
    if Path(subset_dir).exists():
        shutil.rmtree(subset_dir)
    
    data_yaml = create_subset_dataset("Counterfeit-Money-Detector-v5", subset_dir, subset_size=50)
    
    # Change to subset directory
    os.chdir(subset_dir)
    print(f"📁 Working directory: {os.getcwd()}")
    
    try:
        # Load YOLOv8 model
        print("🤖 Loading YOLOv8 nano model...")
        model = YOLO('yolov8n.pt')
        
        # Training parameters for quick demo
        params = {
            'data': 'data.yaml',
            'epochs': 5,  # Very few epochs for demo
            'imgsz': 416,  # Smaller image size
            'batch': 2,    # Small batch size
            'device': device,
            'project': '../demo_runs',
            'name': 'counterfeit_demo',
            'save': True,
            'patience': 5,
            'verbose': True,
            'plots': True,
        }
        
        print("\n📋 Demo Training Configuration:")
        for key, value in params.items():
            print(f"  {key}: {value}")
        
        print(f"\n🏃‍♂️ Starting quick demo training...")
        print("=" * 50)
        
        # Start training
        results = model.train(**params)
        
        print("=" * 50)
        print("✅ Demo training completed!")
        
        # Get model paths
        best_model = Path("../demo_runs/counterfeit_demo/weights/best.pt")
        
        if best_model.exists():
            # Copy to main backend directory
            target_path = Path("../counterfeit_demo_model.pt")
            shutil.copy2(best_model, target_path)
            print(f"✓ Demo model saved to: {target_path.absolute()}")
            
            # Test the model on a sample image
            print("\n🧪 Testing the trained model...")
            test_images = list(Path('valid/images').glob('*.jpg'))
            if test_images:
                test_img = test_images[0]
                results = model.predict(source=str(test_img), save=True, project="../demo_runs", name="test_predictions")
                print(f"✓ Test prediction completed for: {test_img}")
        
        print("\n🎉 Demo training completed successfully!")
        print(f"📊 This demonstrates the training pipeline works!")
        print(f"💡 For full training, run the complete dataset with more epochs")
        
    except Exception as e:
        print(f"❌ Demo training failed: {e}")
        return False
        
    return True


if __name__ == "__main__":
    main()