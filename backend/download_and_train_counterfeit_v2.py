"""
Download Counterfeit Detection Dataset using Roboflow Library and Train with Epochs
Similar approach to the first peso dataset download
"""

import os
import sys

def install_roboflow():
    """Install roboflow library if not available"""
    try:
        import roboflow
        print("✅ Roboflow library already installed")
        return True
    except ImportError:
        print("📦 Installing roboflow library...")
        os.system("pip install roboflow")
        try:
            import roboflow
            print("✅ Roboflow library installed successfully")
            return True
        except ImportError:
            print("❌ Failed to install roboflow library")
            return False

def download_counterfeit_dataset_v2():
    """Download counterfeit detection dataset using roboflow library"""
    try:
        print("🔍 Downloading Counterfeit Detection Dataset using Roboflow Library")
        print("=" * 70)
        
        # Install roboflow if needed
        if not install_roboflow():
            return False
        
        from roboflow import Roboflow
        
        print("🔑 Initializing Roboflow with API key...")
        rf = Roboflow(api_key="gZGoQuvlmBgBLq1Ev4Ar")
        
        print("📋 Accessing project: counterfeit-money-detector")
        project = rf.workspace("aileen-crpev").project("counterfeit-money-detector")
        
        print("📊 Getting version 5 of the dataset...")
        version = project.version(5)
        
        print("⬇️ Downloading dataset in YOLOv8 format...")
        dataset = version.download("yolov8")
        
        print("✅ Dataset downloaded successfully!")
        print(f"📁 Dataset location: {dataset.location}")
        
        # Check if dataset was downloaded
        dataset_path = "Counterfeit-Money-Detector-5"
        if os.path.exists(dataset_path):
            print(f"✅ Verified dataset exists at: {dataset_path}")
            
            # Check contents
            for folder in ['train', 'valid', 'test']:
                images_path = os.path.join(dataset_path, folder, 'images')
                labels_path = os.path.join(dataset_path, folder, 'labels')
                
                if os.path.exists(images_path):
                    image_count = len([f for f in os.listdir(images_path) if f.endswith('.jpg')])
                    print(f"📷 {folder}/images: {image_count} images")
                
                if os.path.exists(labels_path):
                    label_count = len([f for f in os.listdir(labels_path) if f.endswith('.txt')])
                    print(f"🏷️ {folder}/labels: {label_count} labels")
            
            # Check data.yaml
            data_yaml_path = os.path.join(dataset_path, 'data.yaml')
            if os.path.exists(data_yaml_path):
                print(f"📋 Found data.yaml configuration file")
                with open(data_yaml_path, 'r') as f:
                    content = f.read()
                    print("📄 Dataset configuration:")
                    print(content[:500] + "..." if len(content) > 500 else content)
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return False

def train_counterfeit_model_with_epochs():
    """Train counterfeit detection model with specified epochs"""
    try:
        print("\n🚀 Training Counterfeit Detection Model with Custom Epochs")
        print("=" * 70)
        
        # Check if dataset exists
        dataset_path = "Counterfeit-Money-Detector-5"
        if not os.path.exists(dataset_path):
            print("❌ Dataset not found. Please download first.")
            return False
        
        from ultralytics import YOLO
        import yaml
        
        # Load dataset configuration
        config_file = os.path.join(dataset_path, "data.yaml")
        with open(config_file, 'r') as f:
            data_config = yaml.safe_load(f)
        
        print(f"📊 Dataset: {data_config['nc']} classes")
        print(f"🏷️ Classes: {data_config['names'][:10]}{'...' if len(data_config['names']) > 10 else ''}")
        
        # Initialize YOLOv8 model
        print("🧠 Initializing YOLOv8n model...")
        model = YOLO('yolov8n.pt')
        
        # Training parameters with custom epochs
        epochs = 100  # Increased epochs for better training
        training_params = {
            'data': config_file,
            'epochs': epochs,
            'patience': 15,  # Early stopping patience
            'batch': 16,
            'imgsz': 640,
            'cache': True,
            'device': 'cpu',  # Change to 'cuda' if GPU available
            'workers': 4,
            'project': 'counterfeit_detection_runs',
            'name': 'counterfeit_yolov8_v2',
            'save_period': 10,  # Save checkpoint every 10 epochs
            'plots': True,  # Generate training plots
            'val': True,  # Validate during training
        }
        
        print(f"⚙️ Training Configuration:")
        for key, value in training_params.items():
            print(f"   {key}: {value}")
        
        print(f"\n🏋️ Starting training for {epochs} epochs...")
        print("⏰ This will take some time depending on your hardware...")
        
        # Train the model
        results = model.train(**training_params)
        
        print("\n✅ Training completed successfully!")
        
        # Get model paths
        best_model_path = os.path.join('counterfeit_detection_runs', 'counterfeit_yolov8_v2', 'weights', 'best.pt')
        last_model_path = os.path.join('counterfeit_detection_runs', 'counterfeit_yolov8_v2', 'weights', 'last.pt')
        
        if os.path.exists(best_model_path):
            print(f"🏆 Best model saved: {best_model_path}")
            
            # Copy to main directory for easy access
            import shutil
            shutil.copy2(best_model_path, "counterfeit_detection_model_v2.pt")
            print("📋 Model copied to: counterfeit_detection_model_v2.pt")
        
        # Print results summary
        print(f"\n📊 Training Results Summary:")
        print(f"📈 Results directory: counterfeit_detection_runs/counterfeit_yolov8_v2/")
        print(f"📉 Training plots available in results directory")
        print(f"🎯 Best model: {best_model_path}")
        
        return best_model_path if os.path.exists(best_model_path) else last_model_path
        
    except Exception as e:
        print(f"❌ Training failed: {e}")
        return False

def main():
    """Main function to download dataset and train model"""
    print("🎯 Counterfeit Detection Dataset Download & Training v2")
    print("=" * 70)
    
    # Step 1: Download dataset
    print("Step 1: Downloading dataset...")
    if download_counterfeit_dataset_v2():
        print("✅ Dataset download completed successfully!")
        
        # Step 2: Train model
        print("\nStep 2: Starting model training...")
        model_path = train_counterfeit_model_with_epochs()
        
        if model_path:
            print(f"\n🎉 SUCCESS! Counterfeit detection model ready at: {model_path}")
            print("\n📝 Next steps:")
            print("1. Update the backend to use the new model")
            print("2. Test the counterfeit detection endpoints")
            print("3. Validate detection accuracy with sample images")
        else:
            print("\n❌ Training failed. Please check the error messages above.")
    else:
        print("\n❌ Dataset download failed. Please check your internet connection and API key.")

if __name__ == "__main__":
    main()