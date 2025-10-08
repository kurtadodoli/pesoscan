#!/usr/bin/env python3
"""
Complete Counterfeit Detection Training with Full 100 Epochs and Progress Monitoring
"""
import os
import sys
import time
import threading
import glob
from datetime import datetime
from ultralytics import YOLO

class TrainingMonitor:
    """Monitor training progress in real-time"""
    
    def __init__(self, training_dir):
        self.training_dir = training_dir
        self.results_file = os.path.join(training_dir, "results.csv")
        self.weights_dir = os.path.join(training_dir, "weights")
        self.monitoring = False
        
    def start_monitoring(self):
        """Start monitoring in a separate thread"""
        self.monitoring = True
        monitor_thread = threading.Thread(target=self._monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        
    def _monitor_loop(self):
        """Main monitoring loop"""
        last_epoch = 0
        start_time = datetime.now()
        
        while self.monitoring:
            try:
                if os.path.exists(self.results_file):
                    with open(self.results_file, 'r') as f:
                        lines = f.readlines()
                        if len(lines) > 1:  # Header + data
                            last_line = lines[-1].strip()
                            if last_line:
                                parts = last_line.split(',')
                                if len(parts) > 0:
                                    current_epoch = int(float(parts[0].strip()))
                                    if current_epoch > last_epoch:
                                        elapsed = datetime.now() - start_time
                                        
                                        print(f"\n📊 EPOCH {current_epoch}/100 COMPLETED")
                                        print(f"⏱️ Elapsed Time: {elapsed}")
                                        print(f"🔄 Progress: {current_epoch/100*100:.1f}%")
                                        
                                        # Show metrics if available
                                        if len(parts) >= 9:
                                            try:
                                                train_box_loss = float(parts[2].strip())
                                                train_cls_loss = float(parts[3].strip())
                                                precision = float(parts[5].strip())
                                                recall = float(parts[6].strip())
                                                map50 = float(parts[7].strip())
                                                
                                                print(f"📈 Train Box Loss: {train_box_loss:.4f}")
                                                print(f"📈 Train Cls Loss: {train_cls_loss:.4f}")
                                                print(f"🎯 Precision: {precision:.4f}")
                                                print(f"🎯 Recall: {recall:.4f}")
                                                print(f"🎯 mAP@50: {map50:.4f}")
                                                
                                                # Estimate time remaining
                                                if current_epoch > 1:
                                                    avg_time_per_epoch = elapsed.total_seconds() / current_epoch
                                                    remaining_epochs = 100 - current_epoch
                                                    eta_seconds = avg_time_per_epoch * remaining_epochs
                                                    eta = datetime.now() + timedelta(seconds=eta_seconds)
                                                    print(f"🕐 ETA: {eta.strftime('%H:%M:%S')}")
                                                
                                            except (ValueError, IndexError):
                                                pass
                                        
                                        last_epoch = current_epoch
                                        print("─" * 50)
                
                # Check for weight files
                if os.path.exists(self.weights_dir):
                    weight_files = glob.glob(os.path.join(self.weights_dir, "*.pt"))
                    if weight_files:
                        for weight_file in weight_files:
                            file_name = os.path.basename(weight_file)
                            file_size = os.path.getsize(weight_file) / (1024 * 1024)  # MB
                            mod_time = datetime.fromtimestamp(os.path.getmtime(weight_file))
                            if file_name in ['best.pt', 'last.pt']:
                                print(f"💾 {file_name}: {file_size:.1f} MB (updated: {mod_time.strftime('%H:%M:%S')})")
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"⚠️ Monitor error: {e}")
                time.sleep(10)

def train_counterfeit_model_full():
    """Train the counterfeit detection model for full 100 epochs"""
    print("🚀 Starting FULL Counterfeit Detection Training")
    print("=" * 60)
    print("🏋️ Training Parameters:")
    print("   📊 Epochs: 100 (COMPLETE)")
    print("   🖼️ Image Size: 640")
    print("   📦 Batch Size: 8")
    print("   ⏳ Patience: 50")
    print("   💾 Save Best Model: Yes")
    print("=" * 60)
    
    # Set working directory
    os.chdir(r"c:\pesoscan\backend")
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Check dataset
    data_yaml = "Counterfeit-Money-Detector-5/data.yaml"
    if not os.path.exists(data_yaml):
        print(f"❌ Dataset not found: {data_yaml}")
        return False
    
    print(f"✅ Dataset found: {data_yaml}")
    
    try:
        # Initialize model
        print("🔧 Initializing YOLOv8n model...")
        model = YOLO('yolov8n.pt')
        
        # Training parameters for FULL training
        train_params = {
            'data': data_yaml,
            'epochs': 100,  # FULL 100 EPOCHS
            'imgsz': 640,
            'batch': 8,
            'patience': 50,
            'save': True,
            'project': 'counterfeit_detection_runs',
            'name': 'counterfeit_yolov8_complete',
            'exist_ok': True,
            'cache': False,
            'verbose': True,
            'workers': 2,
            'plots': True,
            'save_period': 10  # Save every 10 epochs
        }
        
        # Setup monitoring
        training_dir = "counterfeit_detection_runs/counterfeit_yolov8_complete"
        monitor = TrainingMonitor(training_dir)
        
        print("📊 Starting training monitor...")
        monitor.start_monitoring()
        
        print("🏋️ Starting FULL training (100 epochs)...")
        print("⏰ This will take approximately 3-4 hours")
        print("📊 Progress will be shown every epoch")
        
        # Start training
        start_time = datetime.now()
        print(f"🕐 Training started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        results = model.train(**train_params)
        
        # Stop monitoring
        monitor.stop_monitoring()
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print("\n🎉 TRAINING COMPLETED SUCCESSFULLY!")
        print(f"⏱️ Total training time: {duration}")
        print(f"📊 Results: {results}")
        
        # Check final model
        best_model_path = f"{training_dir}/weights/best.pt"
        if os.path.exists(best_model_path):
            file_size = os.path.getsize(best_model_path) / (1024 * 1024)  # MB
            print(f"✅ Best model saved: {best_model_path}")
            print(f"📁 Model size: {file_size:.1f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Training failed: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    from datetime import timedelta
    
    print("🎯 FULL COUNTERFEIT DETECTION TRAINING")
    print("🚨 This will train for ALL 100 epochs")
    print("⏰ Estimated time: 3-4 hours")
    print("📊 Progress monitoring enabled")
    
    success = train_counterfeit_model_full()
    
    if success:
        print("\n🎉 SUCCESS! Full counterfeit detection model training completed!")
        print("📁 Model ready for production use!")
    else:
        print("\n❌ FAILED! Training encountered errors.")
    
    sys.exit(0 if success else 1)