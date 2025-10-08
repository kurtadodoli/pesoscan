#!/usr/bin/env python3
"""
Resilient Counterfeit Detection Training
- Handles interruptions gracefully
- Auto-saves progress frequently  
- Can resume from checkpoints
- Memory optimized for CPU training
"""
import os
import sys
import time
import torch
import signal
import threading
from datetime import datetime
from ultralytics import YOLO
import gc

class ResilientTrainer:
    """Resilient training manager with checkpoint recovery"""
    
    def __init__(self):
        self.model = None
        self.training_active = False
        self.checkpoint_interval = 5  # Save every 5 epochs
        self.last_save_epoch = 0
        
    def setup_signal_handlers(self):
        """Setup graceful shutdown handlers"""
        def signal_handler(signum, frame):
            print(f"\n🛑 Received signal {signum}, saving progress...")
            self.training_active = False
            if self.model:
                try:
                    save_path = "checkpoint_emergency.pt"
                    self.model.save(save_path)
                    print(f"💾 Emergency save completed: {save_path}")
                except Exception as e:
                    print(f"❌ Emergency save failed: {e}")
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def optimize_environment(self):
        """Optimize environment for stable CPU training"""
        print("🔧 Optimizing for stable CPU training...")
        
        # CPU optimizations
        torch.set_num_threads(2)  # Conservative thread count
        os.environ['OMP_NUM_THREADS'] = '2'
        os.environ['MKL_NUM_THREADS'] = '2'
        
        # Disable GPU
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
        
        # Memory settings
        torch.backends.cudnn.enabled = False
        
        print("✅ Environment optimized")
    
    def find_latest_checkpoint(self, weights_dir):
        """Find the latest checkpoint to resume from"""
        if not os.path.exists(weights_dir):
            return None
        
        weight_files = [f for f in os.listdir(weights_dir) if f.endswith('.pt')]
        if not weight_files:
            return None
        
        # Look for epoch-specific weights
        epoch_weights = [f for f in weight_files if 'epoch' in f]
        if epoch_weights:
            # Sort by epoch number
            try:
                epoch_weights.sort(key=lambda x: int(x.split('epoch')[1].split('.')[0]))
                latest = os.path.join(weights_dir, epoch_weights[-1])
                print(f"🔄 Found checkpoint: {epoch_weights[-1]}")
                return latest
            except (ValueError, IndexError):
                pass
        
        # Fall back to last.pt
        last_pt = os.path.join(weights_dir, 'last.pt')
        if os.path.exists(last_pt):
            print(f"🔄 Found checkpoint: last.pt")
            return last_pt
        
        return None
    
    def train_with_recovery(self):
        """Main training function with recovery capability"""
        print("🎯 RESILIENT COUNTERFEIT DETECTION TRAINING")
        print("🔄 Auto-Recovery | CPU-Optimized | Progress Saving")
        print("=" * 60)
        
        # Setup
        self.setup_signal_handlers()
        self.optimize_environment()
        
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
        
        print(f"✅ Dataset verified: {dataset_path}")
        
        # Training configuration
        project_dir = "counterfeit_detection_runs"
        run_name = "counterfeit_resilient"
        save_dir = os.path.join(project_dir, run_name)
        weights_dir = os.path.join(save_dir, "weights")
        
        try:
            # Check for existing checkpoint
            checkpoint_path = self.find_latest_checkpoint(weights_dir)
            
            if checkpoint_path:
                print(f"🔄 Resuming from checkpoint: {checkpoint_path}")
                self.model = YOLO(checkpoint_path)
            else:
                print("🆕 Starting fresh training")
                self.model = YOLO('yolov8n.pt')
            
            # Conservative training parameters for stability
            train_params = {
                'data': dataset_path,
                'epochs': 100,
                'imgsz': 320,      # Even smaller for stability
                'batch': 2,        # Very conservative batch size
                'device': 'cpu',
                'workers': 1,      # Single worker for stability
                'patience': 25,    # Shorter patience
                'project': project_dir,
                'name': run_name,
                'exist_ok': True,
                'plots': True,
                'save': True,
                'save_period': self.checkpoint_interval,
                'cache': False,
                'amp': False,
                'half': False,
                'verbose': True,
            }
            
            print("🏋️ Training Parameters (Resilient Mode):")
            for key, value in train_params.items():
                print(f"   {key}: {value}")
            
            self.training_active = True
            
            print(f"\n🚀 Starting resilient training...")
            print(f"⏰ Estimated time: 6-8 hours (ultra-stable)")
            print(f"💾 Checkpoints every {self.checkpoint_interval} epochs")
            print(f"🕐 Started at: {datetime.now().strftime('%H:%M:%S')}")
            
            # Start training with error handling
            try:
                results = self.model.train(**train_params)
                
                print("\n🎉 Training completed successfully!")
                
                # Verify final model
                final_best = os.path.join(weights_dir, "best.pt")
                if os.path.exists(final_best):
                    print(f"✅ Final model saved: {final_best}")
                
                return True
                
            except KeyboardInterrupt:
                print("\n🛑 Training interrupted by user")
                return False
                
            except Exception as e:
                print(f"\n❌ Training error: {e}")
                print("💾 Attempting to save current progress...")
                
                try:
                    emergency_save = "emergency_model.pt"
                    self.model.save(emergency_save)
                    print(f"✅ Emergency save completed: {emergency_save}")
                except Exception as save_error:
                    print(f"❌ Emergency save failed: {save_error}")
                
                return False
                
        except Exception as e:
            print(f"❌ Setup error: {e}")
            return False
        
        finally:
            self.training_active = False
            # Final memory cleanup
            gc.collect()

def main():
    """Main function"""
    print("🛡️ RESILIENT TRAINING SYSTEM")
    print("🔄 Auto-Recovery | Checkpoint System | Memory Optimized")
    print("=" * 60)
    
    trainer = ResilientTrainer()
    success = trainer.train_with_recovery()
    
    if success:
        print("\n🎉 TRAINING SESSION COMPLETED!")
        print("📊 Check counterfeit_detection_runs/counterfeit_resilient/")
        print("💾 Model ready for counterfeit detection service")
    else:
        print("\n⚠️ Training session ended early")
        print("🔄 Restart script to resume from last checkpoint")
    
    print(f"\n📊 Session ended at: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()