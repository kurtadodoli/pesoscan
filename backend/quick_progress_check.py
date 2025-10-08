#!/usr/bin/env python3
"""
Quick Training Progress Checker
Check current training status without interrupting the main process
"""
import os
import glob
from datetime import datetime

def check_training_progress():
    """Quick check of training progress"""
    print("📊 QUICK TRAINING PROGRESS CHECK")
    print("=" * 40)
    
    # Check training directories
    runs_dir = r"c:\pesoscan\backend\counterfeit_detection_runs"
    
    if not os.path.exists(runs_dir):
        print("❌ No training runs found")
        return
    
    # Find latest training run
    subdirs = [d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))]
    
    if not subdirs:
        print("❌ No training directories found")
        return
    
    # Check the most recent resilient run first, then CPU optimized
    target_dir = None
    for subdir in subdirs:
        if "resilient" in subdir:
            target_dir = os.path.join(runs_dir, subdir)
            break
        elif "cpu_optimized" in subdir:
            target_dir = os.path.join(runs_dir, subdir)
            break
    
    if not target_dir and subdirs:
        # Fall back to latest directory
        target_dir = os.path.join(runs_dir, subdirs[-1])
    
    if not target_dir:
        print("❌ No suitable training directory found")
        return
    
    print(f"📁 Checking: {os.path.basename(target_dir)}")
    
    # Check results file
    results_file = os.path.join(target_dir, "results.csv")
    
    if os.path.exists(results_file):
        try:
            with open(results_file, 'r') as f:
                lines = f.readlines()
            
            if len(lines) > 1:
                last_line = lines[-1].strip()
                if last_line:
                    parts = last_line.split(',')
                    epoch = int(float(parts[0].strip()))
                    
                    # Progress bar
                    progress = (epoch / 100) * 100
                    bar_length = 30
                    filled = int(bar_length * epoch / 100)
                    bar = "█" * filled + "░" * (bar_length - filled)
                    
                    print(f"📈 EPOCH {epoch}/100 [{bar}] {progress:.1f}%")
                    
                    # Show latest metrics if available
                    if len(parts) >= 9:
                        try:
                            train_box = float(parts[2].strip())
                            train_cls = float(parts[3].strip())
                            precision = float(parts[5].strip())
                            recall = float(parts[6].strip())
                            map50 = float(parts[7].strip())
                            map50_95 = float(parts[8].strip())
                            
                            print(f"📉 Loss | Box: {train_box:.3f} | Cls: {train_cls:.3f}")
                            print(f"🎯 mAP@50: {map50:.3f} | mAP@50-95: {map50_95:.3f}")
                            print(f"🎯 Precision: {precision:.3f} | Recall: {recall:.3f}")
                            
                        except (ValueError, IndexError):
                            print("📊 Metrics parsing in progress...")
                    
                    if epoch >= 100:
                        print("🎉 TRAINING COMPLETED!")
                    else:
                        remaining = 100 - epoch
                        print(f"⏳ Remaining: {remaining} epochs")
                
            else:
                print("📊 Training just started, no epochs completed yet")
                
        except Exception as e:
            print(f"⚠️ Error reading results: {e}")
    else:
        print("📊 Results file not created yet, training initializing...")
    
    # Check weight files
    weights_dir = os.path.join(target_dir, "weights")
    if os.path.exists(weights_dir):
        weight_files = glob.glob(os.path.join(weights_dir, "*.pt"))
        if weight_files:
            print(f"💾 Model checkpoints: {len(weight_files)}")
            
            # Show latest weights
            latest_weights = sorted(weight_files, key=os.path.getmtime, reverse=True)
            for i, weight_file in enumerate(latest_weights[:3]):  # Show top 3
                file_name = os.path.basename(weight_file)
                file_size = os.path.getsize(weight_file) / (1024 * 1024)
                mod_time = datetime.fromtimestamp(os.path.getmtime(weight_file))
                print(f"   📁 {file_name}: {file_size:.1f}MB ({mod_time.strftime('%H:%M')})")
    else:
        print("💾 No model checkpoints yet")
    
    # Check for plots
    plots = glob.glob(os.path.join(target_dir, "*.png"))
    if plots:
        print(f"📊 Training plots: {len(plots)} available")
    
    print(f"🕐 Check time: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    check_training_progress()