"""
Download Counterfeit Money Detection Dataset from Roboflow
"""
import os
import sys

def download_counterfeit_dataset():
    """Download the counterfeit money detection dataset"""
    try:
        # Install roboflow if not already installed
        print("📦 Installing/updating roboflow...")
        os.system("pip install roboflow")
        
        # Import after installation
        from roboflow import Roboflow
        
        print("🔐 Initializing Roboflow with API key...")
        rf = Roboflow(api_key="gZGoQuvlmBgBLq1Ev4Ar")
        
        print("📂 Accessing counterfeit money detector project...")
        project = rf.workspace("aileen-crpev").project("counterfeit-money-detector")
        
        print("📋 Getting version 5 of the dataset...")
        version = project.version(5)
        
        print("⬇️ Downloading dataset in YOLOv8 format...")
        dataset = version.download("yolov8")
        
        print("✅ Dataset downloaded successfully!")
        print(f"📁 Dataset location: {dataset.location}")
        
        # Check downloaded content
        if os.path.exists(dataset.location):
            print("\n📊 Dataset structure:")
            for root, dirs, files in os.walk(dataset.location):
                level = root.replace(dataset.location, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files[:5]:  # Show first 5 files
                    print(f"{subindent}{file}")
                if len(files) > 5:
                    print(f"{subindent}... and {len(files) - 5} more files")
        
        return dataset.location
        
    except ImportError:
        print("❌ Failed to import roboflow. Please install it manually:")
        print("pip install roboflow")
        return None
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Starting Counterfeit Money Detection Dataset Download")
    print("=" * 60)
    
    dataset_path = download_counterfeit_dataset()
    
    if dataset_path:
        print(f"\n🎯 Success! Dataset downloaded to: {dataset_path}")
        print("\n📝 Next steps:")
        print("1. Train a YOLOv8 model for counterfeit detection")
        print("2. Integrate the model into the PesoScan backend")
        print("3. Add counterfeit detection to the detection service")
    else:
        print("\n❌ Download failed. Please check your internet connection and API key.")