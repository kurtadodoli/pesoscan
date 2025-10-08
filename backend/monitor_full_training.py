#!/usr/bin/env python3
"""
Real-time Training Progress Monitor
Monitor the full 100-epoch training progress
"""
import os
import time
import glob
from datetime import datetime, timedelta

def monitor_full_training():
    """Monitor the complete training progress"""
    print("📊 FULL TRAINING PROGRESS MONITOR")
    print("=" * 50)
    
    # Set working directory
    os.chdir(r"c:\pesoscan\backend")
    
    training_dir = "counterfeit_detection_runs/counterfeit_yolov8_complete"
    weights_dir = os.path.join(training_dir, "weights")
    results_file = os.path.join(training_dir, "results.csv")
    
    print(f"📁 Monitoring: {training_dir}")
    print(f"⚖️ Weights: {weights_dir}")
    print(f"📊 Results: {results_file}")
    
    start_time = datetime.now()
    last_epoch = 0
    
    while True:
        try:
            current_time = datetime.now()
            elapsed = current_time - start_time
            
            print(f"\n🕐 {current_time.strftime('%H:%M:%S')} | Elapsed: {elapsed}")
            
            # Check if training directory exists
            if os.path.exists(training_dir):
                print(f"✅ Training directory active")
                
                # Check results file
                if os.path.exists(results_file):
                    try:
                        with open(results_file, 'r') as f:
                            lines = f.readlines()
                            
                        if len(lines) > 1:  # Header + data
                            total_epochs = len(lines) - 1
                            last_line = lines[-1].strip()
                            
                            if last_line:
                                parts = last_line.split(',')
                                current_epoch = int(float(parts[0].strip()))
                                
                                # Progress bar
                                progress = (current_epoch / 100) * 100
                                bar_length = 30
                                filled = int(bar_length * current_epoch / 100)
                                bar = "█" * filled + "░" * (bar_length - filled)
                                
                                print(f"📈 EPOCH {current_epoch}/100 [{bar}] {progress:.1f}%")
                                
                                # Training metrics
                                if len(parts) >= 9:
                                    try:
                                        train_box = float(parts[2].strip())
                                        train_cls = float(parts[3].strip())
                                        precision = float(parts[5].strip())
                                        recall = float(parts[6].strip())
                                        map50 = float(parts[7].strip())
                                        map50_95 = float(parts[8].strip())
                                        
                                        print(f"📉 Losses | Box: {train_box:.4f} | Cls: {train_cls:.4f}")
                                        print(f"🎯 Metrics | Precision: {precision:.4f} | Recall: {recall:.4f}")
                                        print(f"🎯 mAP | @50: {map50:.4f} | @50-95: {map50_95:.4f}")
                                        
                                    except (ValueError, IndexError):
                                        pass
                                
                                # Time estimation
                                if current_epoch > 0:
                                    avg_time_per_epoch = elapsed.total_seconds() / current_epoch
                                    remaining_epochs = 100 - current_epoch
                                    eta_seconds = avg_time_per_epoch * remaining_epochs
                                    eta = current_time + timedelta(seconds=eta_seconds)
                                    
                                    print(f"⏱️ Time/Epoch: {avg_time_per_epoch/60:.1f}m")
                                    print(f"🕐 ETA Completion: {eta.strftime('%H:%M:%S')}")
                                
                                last_epoch = current_epoch
                                
                                # Check if training completed
                                if current_epoch >= 100:
                                    print("\n🎉 TRAINING COMPLETED!")
                                    break
                    
                    except Exception as e:
                        print(f"⚠️ Error reading results: {e}")
                
                # Check weight files
                if os.path.exists(weights_dir):
                    weight_files = glob.glob(os.path.join(weights_dir, "*.pt"))
                    if weight_files:
                        print(f"💾 Model files: {len(weight_files)}")
                        for weight_file in sorted(weight_files):
                            file_name = os.path.basename(weight_file)
                            file_size = os.path.getsize(weight_file) / (1024 * 1024)  # MB
                            mod_time = datetime.fromtimestamp(os.path.getmtime(weight_file))
                            print(f"   📁 {file_name}: {file_size:.1f}MB ({mod_time.strftime('%H:%M')})")
                
                # Check for training plots
                plots = glob.glob(os.path.join(training_dir, "*.png"))
                if plots:
                    print(f"📊 Training plots: {len(plots)} generated")
                
            else:
                print("❌ Training directory not found")
            
            print("─" * 50)
            
            # Wait before next check
            time.sleep(60)  # Check every minute
            
        except KeyboardInterrupt:
            print(f"\n🛑 Monitoring stopped by user")
            break
        except Exception as e:
            print(f"❌ Monitor error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    print("🔍 Starting Full Training Monitor")
    print("📊 Monitoring 100-epoch counterfeit detection training")
    print("⏰ Updates every minute")
    print("🛑 Press Ctrl+C to stop monitoring")
    
    monitor_full_training()
    
    print("\n📊 Monitoring complete!")