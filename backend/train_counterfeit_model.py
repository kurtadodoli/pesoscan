"""
Train YOLOv8 Model for Counterfeit Money Detection
This script trains a model specifically for detecting counterfeit features in Philippine peso bills
"""
import os
import sys
from pathlib import Path

def train_counterfeit_detection_model():
    """Train YOLOv8 model for counterfeit detection"""
    try:
        from ultralytics import YOLO
        import yaml
        
        print("🚀 Starting Counterfeit Detection Model Training")
        print("=" * 60)
        
        # Dataset configuration
        dataset_path = "Counterfeit-Money-Detector-5"
        config_file = os.path.join(dataset_path, "data.yaml")
        
        if not os.path.exists(config_file):
            print(f"❌ Dataset not found at {dataset_path}")
            print("Please run download_counterfeit_dataset.py first")
            return None
        
        # Load dataset info
        with open(config_file, 'r') as f:
            data_config = yaml.safe_load(f)
        
        print(f"📊 Dataset classes: {data_config['nc']} classes")
        print(f"🏷️ Class names: {data_config['names'][:10]}{'...' if len(data_config['names']) > 10 else ''}")
        
        # Initialize YOLOv8 model
        print("🧠 Initializing YOLOv8n model...")
        model = YOLO('yolov8n.pt')  # Start with nano model for faster training
        
        # Training parameters
        training_params = {
            'data': config_file,
            'epochs': 50,  # Reasonable number for initial training
            'patience': 10,  # Early stopping patience
            'batch': 16,   # Adjust based on your GPU memory
            'imgsz': 640,  # Standard YOLO image size
            'cache': True,  # Cache images for faster training
            'device': 'cpu',  # Change to 'cuda' if you have GPU
            'workers': 4,  # Number of CPU workers
            'project': 'counterfeit_detection_runs',
            'name': 'counterfeit_yolov8_train',
            'save_period': 10,  # Save checkpoint every 10 epochs
        }
        
        print("⚙️ Training configuration:")
        for key, value in training_params.items():
            print(f"   {key}: {value}")
        
        print("\n🏋️ Starting training process...")
        print("⏰ This may take a while depending on your hardware...")
        
        # Train the model
        results = model.train(**training_params)
        
        # Training completed
        print("\n✅ Training completed successfully!")
        
        # Model paths
        best_model_path = os.path.join('counterfeit_detection_runs', 'counterfeit_yolov8_train', 'weights', 'best.pt')
        last_model_path = os.path.join('counterfeit_detection_runs', 'counterfeit_yolov8_train', 'weights', 'last.pt')
        
        if os.path.exists(best_model_path):
            print(f"🏆 Best model saved: {best_model_path}")
            
            # Copy to main directory for easy access
            import shutil
            shutil.copy2(best_model_path, "counterfeit_detection_model.pt")
            print("📋 Model copied to: counterfeit_detection_model.pt")
        
        if os.path.exists(last_model_path):
            print(f"📁 Last model saved: {last_model_path}")
        
        # Print training results
        print("\n📊 Training Results:")
        print(f"📈 Results saved in: counterfeit_detection_runs/counterfeit_yolov8_train/")
        
        return best_model_path if os.path.exists(best_model_path) else last_model_path
        
    except ImportError:
        print("❌ ultralytics not installed. Installing now...")
        os.system("pip install ultralytics")
        print("✅ Please run the script again after installation")
        return None
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return None

def validate_dataset():
    """Validate the downloaded dataset"""
    dataset_path = "Counterfeit-Money-Detector-5"
    
    if not os.path.exists(dataset_path):
        print("❌ Dataset not found. Please download it first.")
        return False
    
    # Check required folders
    required_folders = ['train/images', 'train/labels', 'valid/images', 'valid/labels', 'test/images', 'test/labels']
    
    for folder in required_folders:
        folder_path = os.path.join(dataset_path, folder)
        if os.path.exists(folder_path):
            file_count = len(os.listdir(folder_path))
            print(f"✅ {folder}: {file_count} files")
        else:
            print(f"❌ Missing: {folder}")
            return False
    
    return True

if __name__ == "__main__":
    print("🔍 Validating dataset...")
    if validate_dataset():
        print("✅ Dataset validation passed!")
        
        print("\n🤖 Starting counterfeit detection model training...")
        model_path = train_counterfeit_detection_model()
        
        if model_path:
            print(f"\n🎯 Success! Trained model available at: {model_path}")
            print("\n📝 Next steps:")
            print("1. Integrate the model into PesoScan backend")
            print("2. Add counterfeit detection to the detection service")
            print("3. Update frontend to show counterfeit analysis results")
        else:
            print("\n❌ Training failed. Please check the error messages above.")
    else:
        print("\n❌ Dataset validation failed. Please download the dataset first.")