#!/usr/bin/env python3
"""
Fix CashMate dataset structure and create train/val split
"""

import os
import shutil
import yaml
from pathlib import Path
import random

def fix_cashmate_dataset():
    """Fix the CashMate dataset structure by creating train/val split"""
    dataset_path = Path("CASHMATE-PH-BANKNOTES-11")
    
    if not dataset_path.exists():
        print("❌ Dataset not found!")
        return False
    
    print("🔧 Fixing CashMate dataset structure...")
    
    # Check current structure
    train_images = dataset_path / "train" / "images"
    train_labels = dataset_path / "train" / "labels"
    
    if not train_images.exists() or not train_labels.exists():
        print("❌ Train images/labels folders not found!")
        return False
    
    # Get all image files
    image_files = list(train_images.glob("*.jpg")) + list(train_images.glob("*.png"))
    print(f"📊 Found {len(image_files)} images")
    
    # Create validation split (20% of data)
    random.seed(42)  # For reproducible splits
    random.shuffle(image_files)
    
    split_idx = int(0.8 * len(image_files))
    train_files = image_files[:split_idx]
    val_files = image_files[split_idx:]
    
    print(f"📊 Train: {len(train_files)} images")
    print(f"📊 Validation: {len(val_files)} images")
    
    # Create validation directories
    val_images_dir = dataset_path / "valid" / "images"
    val_labels_dir = dataset_path / "valid" / "labels"
    
    val_images_dir.mkdir(parents=True, exist_ok=True)
    val_labels_dir.mkdir(parents=True, exist_ok=True)
    
    # Move validation files
    print("📁 Moving validation files...")
    for img_file in val_files:
        # Move image
        dst_img = val_images_dir / img_file.name
        shutil.move(str(img_file), str(dst_img))
        
        # Move corresponding label
        label_file = train_labels / f"{img_file.stem}.txt"
        if label_file.exists():
            dst_label = val_labels_dir / f"{img_file.stem}.txt"
            shutil.move(str(label_file), str(dst_label))
    
    # Update data.yaml
    print("📝 Updating data.yaml...")
    yaml_path = dataset_path / "data.yaml"
    
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
    
    # Fix paths to be relative
    data['train'] = 'train/images'
    data['val'] = 'valid/images'
    data['test'] = 'valid/images'  # Use valid as test for now
    
    with open(yaml_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)
    
    print("✅ Dataset structure fixed!")
    print(f"📁 Train: {len(list((dataset_path / 'train' / 'images').glob('*')))} images")
    print(f"📁 Valid: {len(list((dataset_path / 'valid' / 'images').glob('*')))} images")
    
    return True

if __name__ == "__main__":
    fix_cashmate_dataset()