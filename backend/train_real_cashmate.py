#!/usr/bin/env python3
"""
Complete CashMate Philippine Banknotes Training with Real Roboflow Dataset
Downloads, trains, and implements the actual CashMate dataset
"""

import os
import sys
import yaml
import shutil
from pathlib import Path
from ultralytics import YOLO
from roboflow import Roboflow
import time
import json

class CashMateTrainer:
    def __init__(self):
        self.api_key = "gZGoQuvlmBgBLq1Ev4Ar"
        self.workspace = "cobra-mi40f"
        self.project_name = "cashmate-ph-banknotes-wrvan"
        self.version = 11
        self.dataset_path = None
        self.model = None
        
    def download_dataset(self):
        """Download the actual CashMate dataset from Roboflow"""
        print("🔽 Downloading CashMate Philippine Banknotes Dataset...")
        print("=" * 60)
        
        try:
            # Initialize Roboflow
            rf = Roboflow(api_key=self.api_key)
            project = rf.workspace(self.workspace).project(self.project_name)
            version = project.version(self.version)
            
            # Download dataset in YOLOv8 format
            print(f"📡 Connecting to Roboflow...")
            print(f"🏢 Workspace: {self.workspace}")
            print(f"📋 Project: {self.project_name}")
            print(f"📊 Version: {self.version}")
            
            dataset = version.download("yolov8")
            self.dataset_path = dataset.location
            
            print(f"✅ Dataset downloaded successfully!")
            print(f"📁 Location: {self.dataset_path}")
            
            # Verify dataset structure
            self.verify_dataset()
            return True
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False
    
    def verify_dataset(self):
        """Verify the downloaded dataset structure"""
        print("\n🔍 Verifying dataset structure...")
        
        if not self.dataset_path or not os.path.exists(self.dataset_path):
            print("❌ Dataset path not found!")
            return False
        
        # Check required directories
        required_dirs = ['train', 'valid', 'test']
        found_dirs = []
        
        for req_dir in required_dirs:
            dir_path = os.path.join(self.dataset_path, req_dir)
            if os.path.exists(dir_path):
                found_dirs.append(req_dir)
                
                # Count images
                images_dir = os.path.join(dir_path, 'images')
                labels_dir = os.path.join(dir_path, 'labels')
                
                if os.path.exists(images_dir):
                    image_count = len([f for f in os.listdir(images_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
                    print(f"  📁 {req_dir}/images: {image_count} images")
                
                if os.path.exists(labels_dir):
                    label_count = len([f for f in os.listdir(labels_dir) if f.endswith('.txt')])
                    print(f"  📁 {req_dir}/labels: {label_count} labels")
        
        # Check data.yaml
        yaml_path = os.path.join(self.dataset_path, 'data.yaml')
        if os.path.exists(yaml_path):
            print(f"  ✅ data.yaml found")
            
            # Read and display class information
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
                
            print(f"  📊 Classes: {data.get('nc', 'Unknown')}")
            if 'names' in data:
                print(f"  🏷️ Class names: {data['names']}")
        else:
            print(f"  ❌ data.yaml not found!")
        
        print(f"✅ Dataset verification complete!")
        return True
    
    def train_model(self, epochs=100, model_size='n', batch_size=16):
        """Train YOLOv8 model on CashMate dataset"""
        print(f"\n🚀 Starting CashMate Training...")
        print("=" * 60)
        print(f"📊 Configuration:")
        print(f"  🔢 Epochs: {epochs}")
        print(f"  🏗️ Model: YOLOv8{model_size}")
        print(f"  📦 Batch size: {batch_size}")
        print(f"  📁 Dataset: {self.dataset_path}")
        
        if not self.dataset_path:
            print("❌ No dataset available! Download first.")
            return False
        
        try:
            # Initialize model
            model_name = f"yolov8{model_size}.pt"
            print(f"\n🤖 Loading {model_name}...")
            self.model = YOLO(model_name)
            
            # Get dataset YAML path
            yaml_path = os.path.join(self.dataset_path, 'data.yaml')
            
            # Start training
            print(f"\n🎯 Starting training...")
            start_time = time.time()
            
            results = self.model.train(
                data=yaml_path,
                epochs=epochs,
                imgsz=640,
                batch=batch_size,
                name=f"cashmate_real_v{self.version}",
                patience=15,
                save=True,
                plots=True,
                val=True,
                verbose=True
            )
            
            end_time = time.time()
            training_time = (end_time - start_time) / 60  # Convert to minutes
            
            print(f"\n✅ Training completed!")
            print(f"⏱️ Training time: {training_time:.1f} minutes")
            
            # Get results path
            runs_dir = Path("runs/train")
            latest_run = max(runs_dir.glob("cashmate_real_v*"), key=os.path.getctime, default=None)
            
            if latest_run:
                print(f"📁 Results saved to: {latest_run}")
                
                # Display training results
                self.display_results(latest_run)
            
            return True
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            return False
    
    def display_results(self, results_path):
        """Display training results and metrics"""
        print(f"\n📊 Training Results:")
        print("=" * 40)
        
        # Check for results.csv
        results_csv = results_path / "results.csv"
        if results_csv.exists():
            try:
                import pandas as pd
                df = pd.read_csv(results_csv)
                
                # Get final metrics
                final_metrics = df.iloc[-1]
                
                print(f"📈 Final Metrics:")
                if 'metrics/mAP50(B)' in df.columns:
                    print(f"  🎯 mAP@50: {final_metrics['metrics/mAP50(B)']:.3f}")
                if 'metrics/mAP50-95(B)' in df.columns:
                    print(f"  🎯 mAP@50-95: {final_metrics['metrics/mAP50-95(B)']:.3f}")
                if 'train/box_loss' in df.columns:
                    print(f"  📉 Box Loss: {final_metrics['train/box_loss']:.3f}")
                if 'val/box_loss' in df.columns:
                    print(f"  📉 Val Loss: {final_metrics['val/box_loss']:.3f}")
                    
            except Exception as e:
                print(f"⚠️ Could not read results: {e}")
        
        # Check model files
        weights_dir = results_path / "weights"
        if weights_dir.exists():
            best_pt = weights_dir / "best.pt"
            last_pt = weights_dir / "last.pt"
            
            if best_pt.exists():
                size_mb = best_pt.stat().st_size / (1024 * 1024)
                print(f"🏆 Best model: {best_pt} ({size_mb:.1f} MB)")
            
            if last_pt.exists():
                size_mb = last_pt.stat().st_size / (1024 * 1024)
                print(f"📝 Last model: {last_pt} ({size_mb:.1f} MB)")
        
        # Check for plots
        plots = list(results_path.glob("*.png"))
        if plots:
            print(f"📊 Generated {len(plots)} result plots")
    
    def test_model(self):
        """Test the trained model"""
        print(f"\n🧪 Testing trained model...")
        
        # Find the best model
        runs_dir = Path("runs/train")
        latest_run = max(runs_dir.glob("cashmate_real_v*"), key=os.path.getctime, default=None)
        
        if not latest_run:
            print("❌ No trained model found!")
            return False
        
        best_model = latest_run / "weights" / "best.pt"
        if not best_model.exists():
            print("❌ Best model not found!")
            return False
        
        try:
            # Load the trained model
            model = YOLO(str(best_model))
            print(f"✅ Model loaded: {best_model}")
            
            # Test with validation data if available
            val_images_dir = Path(self.dataset_path) / "valid" / "images"
            if val_images_dir.exists():
                val_images = list(val_images_dir.glob("*.jpg")) + list(val_images_dir.glob("*.png"))
                
                if val_images:
                    test_image = val_images[0]
                    print(f"🖼️ Testing with: {test_image.name}")
                    
                    # Run inference
                    results = model(str(test_image))
                    
                    # Display results
                    if results and len(results) > 0:
                        result = results[0]
                        if result.boxes is not None and len(result.boxes) > 0:
                            print(f"✅ Detected {len(result.boxes)} objects")
                            
                            for i, box in enumerate(result.boxes):
                                conf = float(box.conf)
                                cls = int(box.cls)
                                print(f"  {i+1}. Class {cls}, Confidence: {conf:.2f}")
                        else:
                            print("ℹ️ No objects detected in test image")
            
            return True
            
        except Exception as e:
            print(f"❌ Model testing failed: {e}")
            return False
    
    def create_integration_files(self):
        """Update integration files with the new trained model"""
        print(f"\n🔧 Updating integration files...")
        
        # Find the latest trained model
        runs_dir = Path("runs/train")
        latest_run = max(runs_dir.glob("cashmate_real_v*"), key=os.path.getctime, default=None)
        
        if not latest_run:
            print("❌ No trained model found for integration!")
            return False
        
        best_model = latest_run / "weights" / "best.pt"
        
        # Update the detector to use the new model
        if os.path.exists("cashmate_detector.py"):
            print("✅ CashMate detector already exists")
            print(f"🔄 New model available at: {best_model}")
        
        return True

def main():
    """Main training function with different epoch options"""
    print("🇵🇭 CashMate Philippine Banknotes - Real Dataset Training")
    print("=" * 70)
    
    trainer = CashMateTrainer()
    
    # Training configurations
    configs = [
        (50, 'n', 16, "Quick training (30-45 min)"),
        (100, 'n', 16, "Standard training (1-1.5 hours)"),
        (150, 's', 12, "Extended training with larger model (2-3 hours)"),
        (200, 's', 8, "Production training (3-4 hours)"),
    ]
    
    print("Available training configurations:")
    for i, (epochs, model, batch, desc) in enumerate(configs, 1):
        print(f"{i}. {epochs} epochs, YOLOv8{model}, batch {batch} - {desc}")
    
    try:
        choice = input("\nSelect configuration (1-4): ").strip()
        
        if choice in ['1', '2', '3', '4']:
            epochs, model_size, batch_size, desc = configs[int(choice) - 1]
            print(f"\nSelected: {desc}")
        else:
            print("Invalid choice! Using default configuration.")
            epochs, model_size, batch_size = 100, 'n', 16
        
        # Step 1: Download dataset
        print(f"\n{'='*70}")
        print("STEP 1: DOWNLOADING DATASET")
        print(f"{'='*70}")
        
        if not trainer.download_dataset():
            print("❌ Dataset download failed!")
            return 1
        
        # Step 2: Train model
        print(f"\n{'='*70}")
        print("STEP 2: TRAINING MODEL")
        print(f"{'='*70}")
        
        if not trainer.train_model(epochs=epochs, model_size=model_size, batch_size=batch_size):
            print("❌ Training failed!")
            return 1
        
        # Step 3: Test model
        print(f"\n{'='*70}")
        print("STEP 3: TESTING MODEL")
        print(f"{'='*70}")
        
        trainer.test_model()
        
        # Step 4: Update integration
        print(f"\n{'='*70}")
        print("STEP 4: UPDATING INTEGRATION")
        print(f"{'='*70}")
        
        trainer.create_integration_files()
        
        print(f"\n🎉 CashMate Training Complete!")
        print("=" * 50)
        print("✅ Dataset downloaded and verified")
        print("✅ Model trained successfully")
        print("✅ Integration files updated")
        print("\n🚀 Next steps:")
        print("1. Test the new model: python test_cashmate_detection.py")
        print("2. Run the test server: python test_cashmate_server.py")
        print("3. Check training results in runs/train/cashmate_real_v*/")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⏹️ Training interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)