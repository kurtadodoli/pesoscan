#!/usr/bin/env python3
"""
Quick monitor for training progress
"""

import time
from pathlib import Path
import os

def monitor_training():
    """Monitor the training progress"""
    print("🔍 Monitoring training progress...")
    
    # Check if training directory exists
    runs_dir = Path("runs/detect/philippine_money_complete")
    
    for i in range(30):  # Check for 30 seconds
        if runs_dir.exists():
            print(f"✅ Training started! Directory: {runs_dir}")
            
            # Check for log files
            log_files = list(runs_dir.glob("*.txt"))
            weight_files = list((runs_dir / "weights").glob("*.pt")) if (runs_dir / "weights").exists() else []
            
            print(f"📊 Log files: {len(log_files)}")
            print(f"🏋️ Weight files: {len(weight_files)}")
            
            # Check for results.png (training curves)
            if (runs_dir / "results.png").exists():
                print("📈 Training curves generated!")
            
            # List training files
            if runs_dir.exists():
                print("\n📁 Training files:")
                for file in runs_dir.rglob("*"):
                    if file.is_file():
                        size = file.stat().st_size
                        print(f"   {file.relative_to(runs_dir)} ({size} bytes)")
            
            return True
        
        time.sleep(1)
        print(f"⏳ Waiting for training to start... ({i+1}/30)")
    
    print("⚠️ Training directory not found after 30 seconds")
    return False

if __name__ == "__main__":
    monitor_training()