#!/usr/bin/env python3
"""
Monitor training progress and check system status
"""
import os
import time
import glob
from datetime import datetime

def check_training_status():
    print("🔍 Training Status Monitor")
    print("="*50)
    
    backend_dir = r"c:\pesoscan\backend"
    os.chdir(backend_dir)
    
    # Check for new training runs
    runs_dir = "counterfeit_detection_runs"
    if os.path.exists(runs_dir):
        print(f"📁 Training runs directory: {runs_dir}")
        
        # List all training runs
        runs = [d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))]
        print(f"🏃 Training runs found: {len(runs)}")
        
        for run in runs:
            run_path = os.path.join(runs_dir, run)
            print(f"   📂 {run}")
            
            # Check for weights
            weights_dir = os.path.join(run_path, "weights")
            if os.path.exists(weights_dir):
                weights = os.listdir(weights_dir)
                print(f"      🏋️ Weights: {weights}")
                
                # Check best.pt
                best_pt = os.path.join(weights_dir, "best.pt")
                if os.path.exists(best_pt):
                    size = os.path.getsize(best_pt) / (1024*1024)  # MB
                    mtime = datetime.fromtimestamp(os.path.getmtime(best_pt))
                    print(f"      ✅ best.pt: {size:.1f} MB, modified: {mtime}")
                else:
                    print(f"      ⏳ best.pt: Not found (training in progress)")
            
            # Check for results
            results_file = os.path.join(run_path, "results.csv")
            if os.path.exists(results_file):
                with open(results_file, 'r') as f:
                    lines = f.readlines()
                    print(f"      📊 Results: {len(lines)-1} epochs completed")
            else:
                print(f"      📊 Results: Not found")
    else:
        print(f"❌ No training runs directory found")
    
    # Check for running Python processes
    print(f"\n🖥️ System Status:")
    print(f"   📂 Current directory: {os.getcwd()}")
    print(f"   🐍 Python running: Checking...")
    
    # Check if any training files are being written to
    recent_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(('.pt', '.csv', '.yaml', '.log')):
                filepath = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(filepath)
                    if time.time() - mtime < 300:  # Modified in last 5 minutes
                        recent_files.append((filepath, datetime.fromtimestamp(mtime)))
                except:
                    pass
    
    if recent_files:
        print(f"\n📝 Recently modified files (last 5 minutes):")
        for filepath, mtime in sorted(recent_files, key=lambda x: x[1], reverse=True):
            print(f"   {filepath} - {mtime}")
    else:
        print(f"\n📝 No recently modified training files")

if __name__ == "__main__":
    check_training_status()