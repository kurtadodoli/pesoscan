"""
Robust Counterfeit Detection Training with Memory Optimization
Optimized for better performance and error handling
"""

import os
import gc
import torch

def train_counterfeit_model_optimized():
    """Train counterfeit detection model with optimized settings"""
    try:
        print("🚀 Starting Optimized Counterfeit Detection Training")
        print("=" * 60)
        
        # Clear GPU/CPU memory
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
        
        from ultralytics import YOLO
        import yaml
        
        # Check dataset
        dataset_path = "Counterfeit-Money-Detector-5"
        config_file = os.path.join(dataset_path, "data.yaml")
        
        if not os.path.exists(config_file):
            print("❌ Dataset not found. Please run download first.")
            return False
        
        # Load dataset config
        with open(config_file, 'r') as f:
            data_config = yaml.safe_load(f)
        
        print(f"📊 Dataset: {data_config['nc']} classes")
        print(f"🏷️ Sample classes: {data_config['names'][:5]}...")
        
        # Initialize model
        print("🧠 Initializing YOLOv8n model...")
        model = YOLO('yolov8n.pt')
        
        # Optimized training parameters
        training_params = {
            'data': config_file,
            'epochs': 50,  # Reduced for faster completion
            'patience': 10,
            'batch': 8,   # Reduced batch size for memory
            'imgsz': 416, # Smaller image size for faster training
            'cache': False,  # Disable caching to save memory
            'device': 'cpu',
            'workers': 2,  # Reduced workers
            'project': 'counterfeit_detection_runs',
            'name': 'counterfeit_optimized',
            'save_period': 5,  # Save more frequently
            'plots': True,
            'val': True,
            'verbose': True,
            'amp': False,  # Disable automatic mixed precision
        }
        
        print("⚙️ Optimized Training Configuration:")
        for key, value in training_params.items():
            print(f"   {key}: {value}")
        
        print(f"\n🏋️ Starting training...")
        print("💡 Using optimized settings for better stability")
        
        # Train with error handling
        try:
            results = model.train(**training_params)
            print("✅ Training completed successfully!")
            
            # Get best model path
            best_model_path = os.path.join('counterfeit_detection_runs', 'counterfeit_optimized', 'weights', 'best.pt')
            
            if os.path.exists(best_model_path):
                # Copy to main directory
                import shutil
                shutil.copy2(best_model_path, "counterfeit_detection_model_optimized.pt")
                print(f"📋 Model saved as: counterfeit_detection_model_optimized.pt")
                return True
            
        except KeyboardInterrupt:
            print("\n⚠️ Training interrupted by user")
            return False
        except Exception as e:
            print(f"\n❌ Training error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

def quick_test_training():
    """Quick test with minimal epochs to verify setup"""
    try:
        print("🧪 Quick Training Test (5 epochs)")
        print("=" * 40)
        
        from ultralytics import YOLO
        
        dataset_path = "Counterfeit-Money-Detector-5"
        config_file = os.path.join(dataset_path, "data.yaml")
        
        if not os.path.exists(config_file):
            print("❌ Dataset not found")
            return False
        
        model = YOLO('yolov8n.pt')
        
        # Minimal test parameters
        test_params = {
            'data': config_file,
            'epochs': 5,
            'batch': 4,
            'imgsz': 320,
            'cache': False,
            'device': 'cpu',
            'workers': 1,
            'project': 'counterfeit_detection_runs',
            'name': 'quick_test',
            'save_period': 1,
            'plots': False,
            'val': True,
            'verbose': True,
        }
        
        print("🏃 Running quick test...")
        results = model.train(**test_params)
        print("✅ Quick test completed!")
        
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("🧪 Running quick test mode")
        quick_test_training()
    else:
        print("🚀 Running optimized training")
        success = train_counterfeit_model_optimized()
        if success:
            print("\n🎉 SUCCESS! Counterfeit detection model ready!")
        else:
            print("\n💡 Try running with --test flag for a quick validation first")