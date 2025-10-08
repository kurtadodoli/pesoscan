#!/usr/bin/env python3
"""
Quick training script with different epoch configurations
"""

import os
import sys
import subprocess
import yaml

def run_training_with_epochs(epochs, model_arch='yolov8n', batch_size=16):
    """Run training with specified epochs"""
    
    print(f"\n{'='*60}")
    print(f"🚀 TRAINING WITH {epochs} EPOCHS")
    print(f"Model: {model_arch}, Batch: {batch_size}")
    print(f"{'='*60}\n")
    
    # Create temporary config
    config = {
        'epochs': epochs,
        'batch_size': batch_size,
        'image_size': 640,
        'learning_rate': 0.01,
        'patience': max(15, epochs // 10),  # Adaptive patience
        'save_period': max(5, epochs // 20),  # Adaptive save period
        'workers': 8,
        'model_architecture': model_arch,
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
    
    # Save temporary config
    config_file = f'temp_config_{epochs}epochs.yaml'
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    try:
        # Run training
        result = subprocess.run([
            sys.executable, 
            'train_cashmate_enhanced.py'
        ], capture_output=False, text=True)
        
        if result.returncode == 0:
            print(f"✅ Training with {epochs} epochs completed successfully!")
        else:
            print(f"❌ Training with {epochs} epochs failed!")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Error running training: {e}")
        return False
    finally:
        # Clean up temporary config
        if os.path.exists(config_file):
            os.remove(config_file)

def main():
    print("CashMate Philippine Banknotes - Epoch Training Configurations")
    print("="*80)
    
    # Training configurations
    training_configs = [
        # (epochs, model_architecture, batch_size, description)
        (50, 'yolov8n', 16, "Quick test training"),
        (100, 'yolov8n', 16, "Standard training"),
        (200, 'yolov8s', 16, "Extended training with better model"),
        (300, 'yolov8m', 12, "Production training (if you have powerful GPU)"),
    ]
    
    print("Available training configurations:")
    for i, (epochs, model, batch, desc) in enumerate(training_configs, 1):
        print(f"{i}. {epochs} epochs, {model}, batch {batch} - {desc}")
    
    print("0. Custom configuration")
    print()
    
    try:
        choice = input("Select configuration (0-4): ").strip()
        
        if choice == '0':
            # Custom configuration
            epochs = int(input("Enter number of epochs (50-500): "))
            model = input("Enter model architecture (yolov8n/s/m/l/x) [yolov8n]: ").strip() or 'yolov8n'
            batch = int(input("Enter batch size (8-32) [16]: ") or '16')
            
            print(f"\nRunning custom training: {epochs} epochs, {model}, batch {batch}")
            success = run_training_with_epochs(epochs, model, batch)
            
        elif choice in ['1', '2', '3', '4']:
            idx = int(choice) - 1
            epochs, model, batch, desc = training_configs[idx]
            
            print(f"\nRunning configuration {choice}: {desc}")
            success = run_training_with_epochs(epochs, model, batch)
            
        else:
            print("Invalid choice!")
            return 1
            
        if success:
            print("\nTraining completed successfully!")
            print("Check the 'runs/train/' directory for results and trained models.")
            return 0
        else:
            print("\nTraining failed!")
            return 1
            
    except KeyboardInterrupt:
        print("\nTraining interrupted by user")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)