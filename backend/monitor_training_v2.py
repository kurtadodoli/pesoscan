#!/usr/bin/env python3
"""
Monitor counterfeit detection training progress - New version
"""
import os
import time
import glob
from datetime import datetime

def monitor_training():
    """Monitor the training progress"""
    print("📊 Monitoring Counterfeit Detection Training Progress")
    print("="*60)
    
    # Set working directory
    os.chdir(r"c:\pesoscan\backend")
    
    training_dir = "counterfeit_detection_runs/counterfeit_yolov8_final"
    weights_dir = os.path.join(training_dir, "weights")
    
    print(f"📁 Monitoring directory: {training_dir}")
    print(f"⚖️ Weights directory: {weights_dir}")
    
    start_time = datetime.now()
    print(f"🕐 Monitoring started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    last_epoch = 0
    
    while True:
        try:
            # Check if training directory exists
            if os.path.exists(training_dir):
                print(f"\n✅ Training directory found: {training_dir}")
                
                # Check for results.csv (training logs)
                results_file = os.path.join(training_dir, "results.csv")
                if os.path.exists(results_file):
                    print(f"📊 Results file found: {results_file}")
                    try:
                        with open(results_file, 'r') as f:
                            lines = f.readlines()
                            if len(lines) > 1:  # Header + at least one data line
                                last_line = lines[-1].strip()
                                if last_line:
                                    parts = last_line.split(',')
                                    if len(parts) > 0:
                                        current_epoch = int(float(parts[0].strip()))
                                        if current_epoch > last_epoch:
                                            print(f"🏃 Training progress: Epoch {current_epoch}/100")
                                            last_epoch = current_epoch
                                            
                                            # Show some metrics if available
                                            if len(parts) >= 4:
                                                try:
                                                    box_loss = float(parts[1].strip())
                                                    cls_loss = float(parts[2].strip())
                                                    print(f"   📉 Box Loss: {box_loss:.4f}, Class Loss: {cls_loss:.4f}")
                                                except (ValueError, IndexError):
                                                    pass
                    except Exception as e:
                        print(f"⚠️ Error reading results: {e}")
                
                # Check for weight files
                if os.path.exists(weights_dir):
                    weight_files = glob.glob(os.path.join(weights_dir, "*.pt"))
                    if weight_files:
                        print(f"⚖️ Weight files found: {len(weight_files)}")
                        for weight_file in weight_files:
                            file_name = os.path.basename(weight_file)
                            file_size = os.path.getsize(weight_file) / (1024 * 1024)  # MB
                            mod_time = datetime.fromtimestamp(os.path.getmtime(weight_file))
                            print(f"   📁 {file_name}: {file_size:.1f} MB (modified: {mod_time.strftime('%H:%M:%S')})")
                    
                    # Check if best.pt exists (training complete)
                    best_model = os.path.join(weights_dir, "best.pt")
                    if os.path.exists(best_model):
                        print(f"\n🎉 TRAINING COMPLETE! Best model found: {best_model}")
                        file_size = os.path.getsize(best_model) / (1024 * 1024)  # MB
                        print(f"📁 Model size: {file_size:.1f} MB")
                        break
                
                # Check for training plots
                plots = glob.glob(os.path.join(training_dir, "*.png")) + glob.glob(os.path.join(training_dir, "*.jpg"))
                if plots:
                    print(f"📈 Training plots: {len(plots)} files")
                
            else:
                print(f"❌ Training directory not found: {training_dir}")
            
            # Wait before next check
            print(f"⏱️ Next check in 30 seconds... (Elapsed: {datetime.now() - start_time})")
            time.sleep(30)
            
        except KeyboardInterrupt:
            print(f"\n🛑 Monitoring stopped by user")
            break
        except Exception as e:
            print(f"❌ Error during monitoring: {e}")
            time.sleep(10)

if __name__ == "__main__":
    monitor_training()