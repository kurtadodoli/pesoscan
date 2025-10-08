#!/usr/bin/env python3
"""
Robust Counterfeit Detection Training with Memory Optimization
Optimized for CPU training with progress monitoring
"""
import os
import sys
import time
import torch
import threading
from datetime import datetime
from ultralytics import YOLO
import gc

class OptimizedTrainingMonitor:
    """Enhanced training monitor with memory optimization"""
    
    def __init__(self):
        self.monitoring = False
        self.last_epoch = 0
        self.start_time = datetime.now()
    
    def start_monitoring(self, save_dir):
        """Start monitoring the training progress"""
        self.monitoring = True
        self.save_dir = save_dir
        
        monitor_thread = threading.Thread(target=self._monitor_progress, daemon=True)
        monitor_thread.start()
        print("📊 Training monitor started")
    
    def _monitor_progress(self):
        """Monitor training progress in separate thread"""
        results_file = os.path.join(self.save_dir, "results.csv")
        
        while self.monitoring:
            try:
                if os.path.exists(results_file):
                    with open(results_file, 'r') as f:
                        lines = f.readlines()
                    
                    if len(lines) > 1:
                        last_line = lines[-1].strip()
                        if last_line:
                            parts = last_line.split(',')
                            epoch = int(float(parts[0].strip()))
                            
                            if epoch > self.last_epoch:
                                self.last_epoch = epoch
                                elapsed = datetime.now() - self.start_time
                                
                                # Progress bar
                                progress = (epoch / 100) * 100
                                bar_length = 20
                                filled = int(bar_length * epoch / 100)
                                bar = "█" * filled + "░" * (bar_length - filled)
                                
                                print(f"\n📈 EPOCH {epoch}/100 [{bar}] {progress:.1f}%")
                                print(f"⏰ Elapsed: {elapsed}")
                                
                                # Memory cleanup every 10 epochs
                                if epoch % 10 == 0:
                                    gc.collect()
                                    print("🧹 Memory cleanup performed")
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(60)
    
    def stop_monitoring(self):
        """Stop the monitoring"""
        self.monitoring = False

def optimize_training_environment():
    """Optimize environment for CPU training"""
    print("🔧 Optimizing training environment for CPU...")
    
    # Set CPU optimizations
    torch.set_num_threads(4)  # Limit threads
    os.environ['OMP_NUM_THREADS'] = '4'
    os.environ['MKL_NUM_THREADS'] = '4'
    
    # Disable CUDA if available to force CPU
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    
    # Memory optimization
    torch.backends.cudnn.enabled = False
    
    print("✅ Environment optimized for CPU training")

def train_counterfeit_optimized():
    """Train counterfeit detection model with optimizations"""
    print("🎯 OPTIMIZED COUNTERFEIT DETECTION TRAINING")
    print("💻 CPU-Optimized with Memory Management")
    print("=" * 60)
    
    # Optimize environment
    optimize_training_environment()
    
    # Set working directory
    try:
        os.chdir(r"c:\pesoscan\backend")
        print(f"📁 Working directory: {os.getcwd()}")
    except Exception as e:
        print(f"❌ Error setting directory: {e}")
        return False
    
    # Check dataset
    dataset_path = "Counterfeit-Money-Detector-5/data.yaml"
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found: {dataset_path}")
        return False
    
    print(f"✅ Dataset found: {dataset_path}")
    
    try:
        # Initialize model with memory optimization
        print("🔧 Initializing YOLOv8n model (CPU optimized)...")
        model = YOLO('yolov8n.pt')
        
        # Configure training parameters for CPU
        train_params = {
            'data': dataset_path,
            'epochs': 100,
            'imgsz': 416,  # Smaller image size for CPU
            'batch': 4,    # Smaller batch size
            'device': 'cpu',
            'workers': 2,  # Fewer workers
            'patience': 50,
            'project': 'counterfeit_detection_runs',
            'name': 'counterfeit_cpu_optimized',
            'exist_ok': True,
            'plots': True,
            'save': True,
            'save_period': 10,
            'cache': False,  # Disable caching to save memory
            'amp': False,    # Disable AMP for CPU
        }
        
        print("🏋️ Training Parameters (CPU Optimized):")
        for key, value in train_params.items():
            print(f"   {key}: {value}")
        
        # Start monitor
        save_dir = f"counterfeit_detection_runs/counterfeit_cpu_optimized"
        monitor = OptimizedTrainingMonitor()
        monitor.start_monitoring(save_dir)
        
        print("\n🚀 Starting optimized training...")
        print("⏰ Estimated time: 4-6 hours (CPU)")
        print(f"🕐 Started at: {datetime.now().strftime('%H:%M:%S')}")
        
        # Start training
        results = model.train(**train_params)
        
        print("\n🎉 Training completed successfully!")
        
        # Stop monitoring
        monitor.stop_monitoring()
        
        # Check results
        if os.path.exists(save_dir):
            weights_dir = os.path.join(save_dir, "weights")
            if os.path.exists(weights_dir):
                best_model = os.path.join(weights_dir, "best.pt")
                last_model = os.path.join(weights_dir, "last.pt")
                
                if os.path.exists(best_model):
                    print(f"✅ Best model saved: {best_model}")
                if os.path.exists(last_model):
                    print(f"✅ Last model saved: {last_model}")
        
        return True
        
    except KeyboardInterrupt:
        print("\n🛑 Training interrupted by user")
        if 'monitor' in locals():
            monitor.stop_monitoring()
        return False
        
    except Exception as e:
        print(f"❌ Training error: {e}")
        if 'monitor' in locals():
            monitor.stop_monitoring()
        return False

def resume_training_if_exists():
    """Check if previous training exists and offer to resume"""
    runs_dir = "counterfeit_detection_runs"
    
    if os.path.exists(runs_dir):
        subdirs = [d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))]
        
        if subdirs:
            print("📁 Found existing training runs:")
            for i, subdir in enumerate(subdirs, 1):
                weights_dir = os.path.join(runs_dir, subdir, "weights")
                if os.path.exists(weights_dir):
                    weight_files = [f for f in os.listdir(weights_dir) if f.endswith('.pt')]
                    print(f"   {i}. {subdir} ({len(weight_files)} model files)")
            
            print("\n🔄 Starting fresh training with optimizations...")
    
    return False

if __name__ == "__main__":
    print("🔍 Optimized Counterfeit Detection Training")
    print("💻 CPU-Optimized | Memory Efficient | Progress Monitoring")
    print("=" * 60)
    
    # Check for existing runs
    resume_training_if_exists()
    
    # Start training
    success = train_counterfeit_optimized()
    
    if success:
        print("\n🎉 TRAINING COMPLETED SUCCESSFULLY!")
        print("📊 Check the results in counterfeit_detection_runs/")
        print("💾 Best model available for counterfeit detection service")
    else:
        print("\n❌ Training was not completed")
        print("🔄 You can restart the training script to continue")
    
    print("\n📊 Training session ended")