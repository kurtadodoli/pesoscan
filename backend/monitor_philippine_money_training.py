#!/usr/bin/env python3
"""
Monitor training progress for Philippine Money model
"""

import time
import os
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

def monitor_training_progress():
    """Monitor the training progress and show real-time updates"""
    print("🔍 Monitoring Philippine Money model training...")
    print("=" * 50)
    
    runs_dir = Path("runs/detect/philippine_money_complete_training")
    
    # Wait for training to start
    print("⏳ Waiting for training to start...")
    for i in range(60):  # Wait up to 60 seconds
        if runs_dir.exists():
            print(f"✅ Training started! Directory: {runs_dir}")
            break
        time.sleep(1)
        print(f"   Waiting... ({i+1}/60)")
    else:
        print("❌ Training directory not found after 60 seconds")
        return False
    
    # Monitor training files
    last_epoch = 0
    while True:
        try:
            # Check for results.csv (training metrics)
            results_csv = runs_dir / "results.csv"
            if results_csv.exists():
                # Read and display latest metrics
                df = pd.read_csv(results_csv)
                if len(df) > last_epoch:
                    latest = df.iloc[-1]
                    epoch = int(latest['epoch']) + 1
                    
                    print(f"\n📊 Epoch {epoch}:")
                    print(f"   Box Loss: {latest['train/box_loss']:.4f}")
                    print(f"   Class Loss: {latest['train/cls_loss']:.4f}")
                    print(f"   DFL Loss: {latest['train/dfl_loss']:.4f}")
                    
                    if 'metrics/mAP50(B)' in latest:
                        print(f"   mAP50: {latest['metrics/mAP50(B)']:.4f}")
                    if 'metrics/mAP50-95(B)' in latest:
                        print(f"   mAP50-95: {latest['metrics/mAP50-95(B)']:.4f}")
                    
                    last_epoch = len(df)
            
            # Check for weight files
            weights_dir = runs_dir / "weights"
            if weights_dir.exists():
                weight_files = list(weights_dir.glob("*.pt"))
                print(f"🏋️ Weight files: {len(weight_files)}")
                
                for weight_file in weight_files:
                    size_mb = weight_file.stat().st_size / (1024 * 1024)
                    print(f"   {weight_file.name}: {size_mb:.1f} MB")
            
            # Check for training completion
            if (runs_dir / "weights/best.pt").exists():
                print("\n🎉 Training completed!")
                print("✅ Best model weights available")
                break
            
            time.sleep(30)  # Check every 30 seconds
            
        except KeyboardInterrupt:
            print("\n⏹️ Monitoring stopped by user")
            break
        except Exception as e:
            print(f"⚠️ Monitoring error: {e}")
            time.sleep(10)
    
    return True

def show_training_curves():
    """Show training curves if available"""
    runs_dir = Path("runs/detect/philippine_money_complete_training")
    results_csv = runs_dir / "results.csv"
    
    if results_csv.exists():
        print("\n📈 Generating training curves...")
        
        df = pd.read_csv(results_csv)
        
        # Create plots
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('Philippine Money Model Training Progress')
        
        # Loss plots
        axes[0, 0].plot(df['epoch'], df['train/box_loss'], label='Box Loss')
        axes[0, 0].plot(df['epoch'], df['train/cls_loss'], label='Class Loss')
        axes[0, 0].plot(df['epoch'], df['train/dfl_loss'], label='DFL Loss')
        axes[0, 0].set_title('Training Losses')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # mAP plots
        if 'metrics/mAP50(B)' in df.columns:
            axes[0, 1].plot(df['epoch'], df['metrics/mAP50(B)'], label='mAP50')
            if 'metrics/mAP50-95(B)' in df.columns:
                axes[0, 1].plot(df['epoch'], df['metrics/mAP50-95(B)'], label='mAP50-95')
            axes[0, 1].set_title('Validation mAP')
            axes[0, 1].set_xlabel('Epoch')
            axes[0, 1].set_ylabel('mAP')
            axes[0, 1].legend()
            axes[0, 1].grid(True)
        
        # Precision/Recall
        if 'metrics/precision(B)' in df.columns:
            axes[1, 0].plot(df['epoch'], df['metrics/precision(B)'], label='Precision')
            axes[1, 0].plot(df['epoch'], df['metrics/recall(B)'], label='Recall')
            axes[1, 0].set_title('Precision & Recall')
            axes[1, 0].set_xlabel('Epoch')
            axes[1, 0].set_ylabel('Value')
            axes[1, 0].legend()
            axes[1, 0].grid(True)
        
        # Learning rate
        if 'lr/pg0' in df.columns:
            axes[1, 1].plot(df['epoch'], df['lr/pg0'], label='Learning Rate')
            axes[1, 1].set_title('Learning Rate')
            axes[1, 1].set_xlabel('Epoch')
            axes[1, 1].set_ylabel('LR')
            axes[1, 1].legend()
            axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig(runs_dir / "training_progress.png", dpi=150, bbox_inches='tight')
        print(f"✅ Training curves saved to: {runs_dir}/training_progress.png")
        
    else:
        print("⚠️ No training results found to plot")

if __name__ == "__main__":
    try:
        import pandas as pd
        import matplotlib.pyplot as plt
        
        monitor_training_progress()
        show_training_curves()
        
    except ImportError as e:
        print(f"⚠️ Missing required packages: {e}")
        print("💡 Install with: pip install pandas matplotlib")
        
        # Basic monitoring without plots
        monitor_training_progress()